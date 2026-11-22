import bpy
import array

from bpy.app.translations import pgettext_data

from .. import core
from .. import memory


def is_folder(key):
    return key.vertex_group.startswith(core.folder.blocks['prefix']['id'] + ".")


def is_selected(key):
    return str(key.id_data.key_blocks.find(key.name)) in key.id_data.shape_keys_plus.selections


def get_selected_indices():
    obj = bpy.context.object
    
    if not obj or not obj.data.shape_keys:
        return []
    
    selections = obj.data.shape_keys.shape_keys_plus.selections
    
    # A set, so that a duplicate entry (from an older version, or a .blend saved with one) can't count twice.
    return sorted({int(x.name) for x in selections if x.name.isdigit()})


def get_selected():
    """Returns a list of selected bpy.types.ShapeKey."""
    obj = bpy.context.object
    
    # The panel and the menus call this on every redraw, including for objects that have no shape keys yet (e.g. right
    # after importing a model), where `shape_keys` is None.
    if not obj or not obj.data.shape_keys:
        return []
    
    key_blocks = obj.data.shape_keys.key_blocks
    
    # Selections are stored as indices, so one can end up past the end of the list if shape keys were removed
    # without the selection being updated. Ignore those instead of raising an IndexError.
    return [key_blocks[index] for index in get_selected_indices() if index < len(key_blocks)]


def get_driver(key, fcurve=False):
    data_path = "key_blocks[\"%s\"].value" % key.name
    anim = key.id_data.animation_data
    
    if anim and anim.drivers:
        for fc in anim.drivers:
            if fc.data_path == data_path:
                return fc if fcurve else fc.driver
    
    return None


def invert_data(key):
    """
    Inverts a shape key's vertex offsets relative to its relative key, in place.
    
    This has the same result as blending the shape key to a value of -1.0 relative to its relative key
    (usually the Basis), then baking that pose into a new shape key at a value of 1.0.
    """
    rel = key.relative_key
    
    if not rel or rel == key or not len(key.data):
        return
    
    count = len(key.data) * 3
    
    key_co = array.array('f', [0.0]) * count
    rel_co = array.array('f', [0.0]) * count
    
    key.data.foreach_get('co', key_co)
    rel.data.foreach_get('co', rel_co)
    
    # new = rel - (key - rel) = (2 * rel) - key
    inverted_co = array.array('f', (2.0 * r - k for r, k in zip(rel_co, key_co)))
    
    key.data.foreach_set('co', inverted_co)


def blend(sources, name):
    """
    Creates a new shape key that is the full-strength (value 1.0) combination of the given `sources`
    (an iterable of bpy.types.ShapeKey), using Blender's native shape_key_add(from_mix=True).

    Every other, non-muted shape key is temporarily muted so it can't bleed into the mix, and every
    source's value is temporarily forced to 1.0 even if it's currently at 0 or partially blended. Both are
    restored to their original state afterwards, so nothing about the object's existing shape keys changes.
    """
    obj = bpy.context.object
    key_blocks = obj.data.shape_keys.key_blocks
    source_indices = {key_blocks.find(key.name) for key in sources}
    exclude = []
    forced = []

    for i, key in enumerate(key_blocks):
        if i in source_indices:
            if key.value != 1.0:
                forced.append((i, key.value))
                key.value = 1.0
        elif not key.mute:
            key.mute = True
            exclude.append(i)

    new_key = obj.shape_key_add(from_mix=True)
    new_key.name = name

    for i in exclude:
        key_blocks[i].mute = False

    for i, old_value in forced:
        key_blocks[i].value = old_value

    return new_key


def add(type='DEFAULT'):
    obj = bpy.context.object
    
    # Add the key.
    if type == 'FROM_MIX':
        new_key = obj.shape_key_add(from_mix=True)
    elif type == 'FROM_MIX_SELECTED' and obj.data.shape_keys:
        exclude = []
        
        for i, key in enumerate(obj.data.shape_keys.key_blocks):
            if not is_selected(key) and not key.mute:
                key.mute = True
                exclude.append(i)
        
        new_key = obj.shape_key_add(from_mix=True)
        
        for i in exclude:
            obj.data.shape_keys.key_blocks[i].mute = False
        
        deselect()
    elif type == 'COMBINED_SELECTED' and obj.data.shape_keys:
        # Like FROM_MIX_SELECTED, but every selected shape key is temporarily forced to a value of 1.0,
        # so that a full-strength combination is created even if some (or all) selected values are 0.
        exclude = []
        forced = []
        
        for i, key in enumerate(obj.data.shape_keys.key_blocks):
            if is_selected(key):
                if key.value != 1.0:
                    forced.append((i, key.value))
                    key.value = 1.0
            elif not key.mute:
                key.mute = True
                exclude.append(i)
        
        new_key = obj.shape_key_add(from_mix=True)
        
        for i in exclude:
            obj.data.shape_keys.key_blocks[i].mute = False
        
        for i, old_value in forced:
            obj.data.shape_keys.key_blocks[i].value = old_value
        
        deselect()
    else:
        new_key = obj.shape_key_add(from_mix=False)
    
    # Only create a reference to shape_keys.key_blocks after a key is sure to exist, so that shape_keys is not None.
    key_blocks = obj.data.shape_keys.key_blocks
    folder_count = len([key for key in key_blocks if is_folder(key)])
    
    translate_new_dataname = bpy.context.preferences.view.use_translate_new_dataname
    
    if type == 'FOLDER':
        new_key.name = (core.strings['Folder'] if translate_new_dataname else "Folder") + " " + str(folder_count + 1)
        new_key.vertex_group = core.folder.generate()
    else:
        if len(key_blocks) == 1:
            new_key.name = pgettext_data("Basis")
        else:
            new_key.name = pgettext_data("Key") + " " + str(
                len(key_blocks) - folder_count - (not is_folder(key_blocks[0])))
    
    return new_key


def select(i, v):
    obj = bpy.context.object
    shape_keys = obj.data.shape_keys
    key_blocks = shape_keys.key_blocks
    selections = shape_keys.shape_keys_plus.selections
    
    if type(i) == bpy.types.ShapeKey:
        key = i
        i = key_blocks.find(key.name)
    elif type(i) == str:
        assert i in key_blocks, "Invalid name given for shape key selection."
        key = key_blocks[i]
        i = key_blocks.find(key.name)
    elif type(i) == int:
        key = core.utils.get(key_blocks, i, None)
        assert key, "Invalid index given for shape key selection."
    
    if i <= 0:
        return
    
    i = str(i)
    
    if v:
        # Not core.utils.get(selections, i, selections.add()): `i` is a string there, so that always fell back to its
        # default and added a duplicate (plus a nameless entry) every time an already-selected key was selected again.
        if i not in selections:
            selections.add().name = i
    else:
        while i in selections:
            selections.remove(selections.find(i))


def deselect():
    """Deselects all shape keys and returns a list of names to be passed as the argument to reselect()."""
    selections = [key.name for key in get_selected()]
    bpy.context.object.data.shape_keys.shape_keys_plus.selections.clear()
    return selections


def reselect(selections):
    """Selects the shape keys from the list of names in `selections`, such as those returned by deselect()."""
    for name in selections:
        # Check if the shape key hasn't been deleted since the `selections` list was created.
        if name in bpy.context.object.data.shape_keys.key_blocks:
            select(name, True)


def remove(obj, names):
    """
    Removes the shape keys called `names` (and their drivers) from `obj`, in the order given.
    
    Every shape key is removed *by reference*, with `Object.shape_key_remove()`. `bpy.ops.object.shape_key_remove()`
    is deliberately not used here: that operator deletes whatever shape key happens to be at
    `Object.active_shape_key_index` at the exact moment it runs, so whenever that index isn't pointing at the key that
    was meant to go (it was left somewhere else by an earlier add/move/parent, it's relying on the index shifting by
    exactly the right amount after every removal, etc.), the wrong key is deleted, and every removal after it repeats
    the mistake. Removing by reference can only ever delete the key that was asked for.
    
    Blender nudges the active shape key index on its own as keys disappear, so callers should set
    `Object.active_shape_key_index` themselves afterwards. Don't keep any `bpy.types.ShapeKey` of the removed keys
    around afterwards either, since they become invalid. Hold on to their names instead.
    """
    for name in names:
        # Fetched every time, because it is not safe to hold on to these across a removal.
        shape_keys = obj.data.shape_keys
        
        if not shape_keys:
            return
        
        key_blocks = shape_keys.key_blocks
        index = key_blocks.find(name)
        
        if index == -1:
            # Already gone, e.g. a child of a folder that was removed earlier in this same list.
            continue
        
        key = key_blocks[index]
        anim = shape_keys.animation_data
        
        # Remove the driver first. The matching drivers are collected before any of them are removed, because
        # removing an F-curve while iterating over `anim.drivers` invalidates the iterator.
        if anim and anim.drivers:
            data_path = "key_blocks[\"%s\"].value" % name
            
            for fc in [fc for fc in anim.drivers if fc.data_path == data_path]:
                anim.drivers.remove(fc)
        
        obj.shape_key_remove(key)


def copy(original_key, mirror=0, custom=False, invert=False, rename=None):
    obj = bpy.context.object
    shape_keys = obj.data.shape_keys
    key_blocks = shape_keys.key_blocks
    anim = shape_keys.animation_data
    cc = obj.data.shape_keys.shape_keys_plus.copy_customization
    is_folder = core.key.is_folder(original_key)
    
    # Store original values.
    old_data = [data.co for data in original_key.data]
    old_name = original_key.name
    old_slider_min = original_key.slider_min
    old_slider_max = original_key.slider_max
    old_value = original_key.value
    old_vertex_group = original_key.vertex_group
    old_relative_key = getattr(original_key.relative_key, 'name', "")
    old_interpolation = original_key.interpolation
    old_mute = original_key.mute
    
    new_key = obj.shape_key_add(from_mix=False)
    
    # Copy the original shape key's raw data to the new shape key.
    if custom and cc.use_data:
        if cc.data:
            for i, vec in enumerate([data.co for data in key_blocks[cc.data].data]):
                new_key.data[i].co[:] = vec
    else:
        for i, vec in enumerate(old_data):
            new_key.data[i].co[:] = vec
    
    # Select the new key, which was sent to the bottom.
    obj.active_shape_key_index = len(key_blocks) - 1
    
    new_name = old_name
    
    if mirror > 0:
        bpy.ops.object.shape_key_mirror(use_topology=mirror == 2)
        
        # bpy.utils.flip_name() handles many more naming conventions than a plain ".L"/".R" suffix,
        # including "_L"/"_R", "Left"/"Right", "LEFT"/"RIGHT", etc. If no side is detected in the name,
        # it returns the name unchanged, in which case the copy keeps its original name (Blender will
        # auto-disambiguate it, e.g. "Name.001").
        flipped_name = bpy.utils.flip_name(old_name)
        
        if flipped_name != old_name:
            new_name = flipped_name
    
    if invert and not is_folder:
        new_name = core.strings['core.key.copy.new_name[%s Inverted]'] % new_name
    
    # An explicit rename (e.g. for face tracking standard translation/conversion) always wins.
    if rename is not None:
        new_name = rename
    
    new_relative_key = old_relative_key if (not custom or not cc.use_relative_key) else cc.relative_key
    
    # Copy original values.
    new_key.name = new_name
    new_key.slider_min = old_slider_min if (not custom or not cc.use_slider_min) else cc.slider_min
    new_key.slider_max = old_slider_max if (not custom or not cc.use_slider_max) else cc.slider_max
    new_key.value = old_value if (not custom or not cc.use_value) else cc.value
    new_key.vertex_group = old_vertex_group if is_folder or (not custom or not cc.use_vertex_group) else cc.vertex_group
    new_key.relative_key = key_blocks[new_relative_key] if new_relative_key else key_blocks[0]
    new_key.interpolation = old_interpolation if (not custom or not cc.use_interpolation) else cc.interpolation
    new_key.mute = old_mute if (not custom or not cc.use_mute) else cc.mute
    
    if invert and not is_folder:
        invert_data(new_key)
    
    if anim and anim.drivers:
        data_path = "key_blocks[\"%s\"].value" % new_key.name
        driver = None
        
        # Remove all conflicting drivers to make room for the copied one.
        for fc in anim.drivers:
            if fc.data_path == data_path:
                anim.drivers.remove(fc)
        
        # Copy the driver.
        if custom and cc.use_driver:
            driver = get_driver(key_blocks[cc.driver], fcurve=True) if cc.driver else None
        else:
            driver = get_driver(key_blocks[old_name], fcurve=True)
        
        if driver:
            new_driver = anim.drivers.from_existing(src_driver=driver)
            new_driver.data_path = data_path
    
    return new_key
