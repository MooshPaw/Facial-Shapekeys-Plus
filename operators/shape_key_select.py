import bpy

from .. import core


class OBJECT_OT_skp_shape_key_select(bpy.types.Operator):
    bl_idname = 'object.skp_shape_key_select'
    bl_label = core.strings['operators.ShapeKeySelect.bl_label']
    bl_description = core.strings['operators.ShapeKeySelect.bl_description']
    bl_options = {'REGISTER', 'UNDO'}
    
    mode: bpy.props.EnumProperty(
        items=(
            ('TOGGLE', "", ""),
            ('ALL', "", ""),
            ('NONE', "", ""),
            ('INVERSE', "", "")
        ),
        options={'HIDDEN'})
    
    index: bpy.props.IntProperty(options={'HIDDEN'})
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.data.shape_keys
    
    def invoke(self, context, event):
        if self.mode != 'TOGGLE':
            return self.execute(context)
        
        obj = context.object
        key_props = obj.data.shape_keys.shape_keys_plus
        # Fall back to the clicked row itself if there's no anchor yet (e.g. the very first click).
        anchor = key_props.select_anchor if key_props.select_anchor >= 0 else self.index
        
        if event.shift or event.ctrl:
            selected = set(core.key.get_selected_indices())
            
            if event.shift:
                # Range-select (like most file explorers), but toggles off instead if the whole range is
                # already selected.
                start, end = sorted((anchor, self.index))
                indices = list(range(start, end + 1))
                
                all_selected = all(i in selected for i in indices if i > 0)
                value = not all_selected
                
                for i in indices:
                    core.key.select(i, value)
            else:
                # Ctrl+Click (like most file explorers): selects the active row and the clicked row,
                # without touching anything in between. If the clicked row is already selected, only it
                # is unselected.
                if self.index in selected:
                    core.key.select(self.index, False)
                else:
                    core.key.select(anchor, True)
                    core.key.select(self.index, True)
            
            key_props.select_anchor = self.index
            
            # Move the blue "active" highlight to the clicked row, purely as a visual indicator of where
            # the Shift/Ctrl+Click selection landed. A plain click deliberately leaves it untouched, so the
            # active shape key doesn't jump around while just ticking checkboxes.
            obj.active_shape_key_index = self.index
            
            return {'FINISHED'}
        
        key_props.select_anchor = self.index
        
        return self.execute(context)
    
    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks
        selections = shape_keys.shape_keys_plus.selections
        
        if self.mode == 'TOGGLE':
            core.key.select(self.index, str(self.index) not in selections)
        elif self.mode == 'ALL':
            for index, key in enumerate(key_blocks):
                if str(index) not in selections:
                    core.key.select(index, True)
        elif self.mode == 'NONE':
            selections.clear()
        elif self.mode == 'INVERSE':
            for index, key in enumerate(key_blocks):
                core.key.select(index, str(index) not in selections)
        
        return {'FINISHED'}
