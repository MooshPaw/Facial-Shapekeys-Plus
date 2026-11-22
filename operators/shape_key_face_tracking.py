import bpy

from .. import core
from .. import memory


# These folder names are literal shape key / vertex group data (not UI text), so they are
# intentionally not run through core.strings translation.
FACE_TRACKING_FOLDER_NAME = "---Face Tracking---"
ARKIT_FOLDER_NAME = "---ARKit---"
UNIFIED_EXPRESSIONS_FOLDER_NAME = "---Unified Expressions---"
BLENDED_SHAPES_FOLDER_NAME = "---Blended Shapes---"
VISEMES_FOLDER_NAME = "---Visemes---"
MMD_FOLDER_NAME = "---MMD---"

# The marker used in MY_CUSTOM_SHAPES to split "Unified Expressions" entries from "Blended Shapes" entries.
CUSTOM_BLENDED_SHAPES_MARKER = "---Blended Shapes---"


# Visemes folder - uses the 15 visemes from Oculus
VISEMES = (
    'vrc.v_aa', 'vrc.v_ch', 'vrc.v_dd', 'vrc.v_e', 'vrc.v_ff',
    'vrc.v_ih', 'vrc.v_kk', 'vrc.v_nn', 'vrc.v_oh', 'vrc.v_ou',
    'vrc.v_pp', 'vrc.v_rr', 'vrc.v_sil', 'vrc.v_ss', 'vrc.v_th',
)

# The 52 standard ARKit / Apple ARKitFaceAnchor blend shape locations.
ARKIT_SHAPES = (
    'browDownLeft', 'browDownRight', 'browInnerUp', 'browOuterUpLeft', 'browOuterUpRight',
    'cheekPuff', 'cheekSquintLeft', 'cheekSquintRight',
    'eyeBlinkLeft', 'eyeBlinkRight',
    'eyeLookDownLeft', 'eyeLookDownRight', 'eyeLookInLeft', 'eyeLookInRight',
    'eyeLookOutLeft', 'eyeLookOutRight', 'eyeLookUpLeft', 'eyeLookUpRight',
    'eyeSquintLeft', 'eyeSquintRight', 'eyeWideLeft', 'eyeWideRight',
    'jawForward', 'jawLeft', 'jawOpen', 'jawRight',
    'mouthClose', 'mouthDimpleLeft', 'mouthDimpleRight', 'mouthFrownLeft', 'mouthFrownRight',
    'mouthFunnel', 'mouthLeft', 'mouthLowerDownLeft', 'mouthLowerDownRight',
    'mouthPressLeft', 'mouthPressRight', 'mouthPucker', 'mouthRight',
    'mouthRollLower', 'mouthRollUpper', 'mouthShrugLower', 'mouthShrugUpper',
    'mouthSmileLeft', 'mouthSmileRight', 'mouthStretchLeft', 'mouthStretchRight',
    'mouthUpperUpLeft', 'mouthUpperUpRight',
    'noseSneerLeft', 'noseSneerRight',
    'tongueOut',
)

# The Unified Expressions standard's "Base Shapes" (VRCFaceTracking / docs.vrcft.io).
UNIFIED_BASE_SHAPES = (
    'EyeLookOutRight', 'EyeLookInRight', 'EyeLookUpRight', 'EyeLookDownRight',
    'EyeLookOutLeft', 'EyeLookInLeft', 'EyeLookUpLeft', 'EyeLookDownLeft',
    'EyeClosedRight', 'EyeClosedLeft',
    'EyeSquintRight', 'EyeSquintLeft',
    'EyeWideRight', 'EyeWideLeft',
    'EyeDilationRight', 'EyeDilationLeft',
    'EyeConstrictRight', 'EyeConstrictLeft',
    'BrowPinchRight', 'BrowPinchLeft',
    'BrowLowererRight', 'BrowLowererLeft',
    'BrowInnerUpRight', 'BrowInnerUpLeft',
    'BrowOuterUpRight', 'BrowOuterUpLeft',
    'NoseSneerRight', 'NoseSneerLeft',
    'NasalDilationRight', 'NasalDilationLeft',
    'NasalConstrictRight', 'NasalConstrictLeft',
    'CheekSquintRight', 'CheekSquintLeft',
    'CheekPuffRight', 'CheekPuffLeft',
    'CheekSuckRight', 'CheekSuckLeft',
    'JawOpen', 'MouthClosed', 'JawRight', 'JawLeft', 'JawForward', 'JawBackward',
    'JawClench', 'JawMandibleRaise',
    'LipSuckUpperRight', 'LipSuckUpperLeft', 'LipSuckLowerRight', 'LipSuckLowerLeft',
    'LipSuckCornerRight', 'LipSuckCornerLeft',
    'LipFunnelUpperRight', 'LipFunnelUpperLeft', 'LipFunnelLowerRight', 'LipFunnelLowerLeft',
    'LipPuckerUpperRight', 'LipPuckerUpperLeft', 'LipPuckerLowerRight', 'LipPuckerLowerLeft',
    'MouthUpperUpRight', 'MouthUpperUpLeft', 'MouthLowerDownRight', 'MouthLowerDownLeft',
    'MouthUpperDeepenRight', 'MouthUpperDeepenLeft',
    'MouthUpperRight', 'MouthUpperLeft', 'MouthLowerRight', 'MouthLowerLeft',
    'MouthCornerPullRight', 'MouthCornerPullLeft', 'MouthCornerSlantRight', 'MouthCornerSlantLeft',
    'MouthFrownRight', 'MouthFrownLeft', 'MouthStretchRight', 'MouthStretchLeft',
    'MouthDimpleRight', 'MouthDimpleLeft',
    'MouthRaiserUpper', 'MouthRaiserLower',
    'MouthPressRight', 'MouthPressLeft',
    'MouthTightenerRight', 'MouthTightenerLeft',
    'TongueOut', 'TongueUp', 'TongueDown', 'TongueRight', 'TongueLeft', 'TongueRoll',
    'TongueBendDown', 'TongueCurlUp', 'TongueSquish', 'TongueFlat',
    'TongueTwistRight', 'TongueTwistLeft',
    # Reserved by the standard, but not currently used by any tracking interface.
    'SoftPalateClose', 'ThroatSwallow', 'NeckFlexRight', 'NeckFlexLeft',
)

# The Unified Expressions standard's "Blended Shapes" - shapes that blend together several Base Shapes.
UNIFIED_BLENDED_SHAPES = (
    'EyeClosed', 'EyeWide', 'EyeSquint', 'EyeDilation', 'EyeConstrict',
    'BrowDownRight', 'BrowDownLeft', 'BrowDown',
    'BrowInnerUp',
    'BrowUpRight', 'BrowUpLeft', 'BrowUp',
    'NoseSneer',
    'NasalDilation', 'NasalConstrict',
    'CheekPuff', 'CheekSuck', 'CheekSquint',
    'LipSuckUpper', 'LipSuckLower', 'LipSuck',
    'LipFunnelUpper', 'LipFunnelLower', 'LipFunnel',
    'LipPuckerUpper', 'LipPuckerLower', 'LipPucker',
    'MouthUpperUp', 'MouthLowerDown', 'MouthOpen',
    'MouthRight', 'MouthLeft',
    'MouthSmileRight', 'MouthSmileLeft', 'MouthSmile',
    'MouthSadRight', 'MouthSadLeft', 'MouthSad',
    'MouthStretch',
    'MouthDimple',
    'MouthTightener',
    'MouthPress',
)

# MooshPaw's CUSTOM PRESET for UE Expressions that are actually in use.
# The '---Blended Shapes---' marker splits base (Unified Expressions) entries from Blended Shapes entries;
# comment it (and everything after it) out to exclude Blended Shapes from the custom set entirely.
MY_CUSTOM_SHAPES = (
    # Eye Brows
    'BrowPinchLeft', 'BrowPinchRight',
    'BrowLowererLeft', 'BrowLowererRight',
    'BrowInnerUpLeft', 'BrowInnerUpRight',
    'BrowOuterUpLeft', 'BrowOuterUpRight',
    
    # Cheeks
    'CheekPuffLeft', 'CheekPuffRight',
    'CheekSquintLeft', 'CheekSquintRight',
    'CheekSuckLeft', 'CheekSuckRight',
    
    # Eyes
    'EyeClosedLeft', 'EyeClosedRight',
    'EyeSquintLeft', 'EyeSquintRight',
    'EyeWideLeft', 'EyeWideRight',
    'EyeLookDownLeft', 'EyeLookDownRight',
    'EyeLookInLeft', 'EyeLookInRight',
    'EyeLookOutLeft', 'EyeLookOutRight',
    'EyeLookUpLeft', 'EyeLookUpRight',
    'EyeDilationLeft', 'EyeDilationRight',
    'EyeConstrictLeft', 'EyeConstrictRight',
    
    # Jaw
    'JawOpen', 'MouthClosed',
    'JawLeft', 'JawRight',
    'JawForward', 'JawBackward',
    'JawClench',
    
    # Lips
    'LipSuckUpperLeft', 'LipSuckUpperRight',
    'LipSuckLowerLeft', 'LipSuckLowerRight',
    'LipSuckCornerLeft', 'LipSuckCornerRight',
    
    # Mouth
    'MouthDimpleLeft', 'MouthDimpleRight',
    'MouthFrownLeft', 'MouthFrownRight',
    'MouthPressLeft', 'MouthPressRight',
    'MouthRaiserUpper', 'MouthRaiserLower',
    'MouthStretchLeft', 'MouthStretchRight',
    'MouthUpperUpLeft', 'MouthUpperUpRight',
    'MouthLowerDownLeft', 'MouthLowerDownRight',
    'MouthUpperDeepenLeft', 'MouthUpperDeepenRight',
    'MouthTightenerLeft', 'MouthTightenerRight',
    
    # Nose
    'NoseSneerLeft', 'NoseSneerRight',
    'NasalDilationLeft', 'NasalDilationRight',
    'NasalConstrictLeft', 'NasalConstrictRight',
    
    # Tongue
    'TongueOut',
    'TongueUp', 'TongueDown',
    'TongueLeft', 'TongueRight',
    'TongueRoll',
    'TongueBendDown', 'TongueCurlUp',
    'TongueSquish', 'TongueFlat',
    'TongueTwistLeft', 'TongueTwistRight',
    
    # IF YOU DON'T PLAN ON USING BLENDED SHAPES, PUT A # NEXT TO '---BLENDED SHAPES---,'
    '---Blended Shapes---',
    'BrowDownLeft', 'BrowDownRight',
    'BrowInnerUp',
    'CheekPuff',
    'LipSuckLower', 'LipSuckUpper',
    'LipFunnel', 'LipPucker',
    'MouthLeft', 'MouthRight',
    'MouthSmileLeft', 'mouthSmileRight',
)

# The official ARKit <-> Unified Expressions conversion table (docs.vrcft.io/.../compatibility/arkit).
# Every entry here is a verified, direct 1:1 correspondence - no shape is split or combined.
ARKIT_UNIFIED_PAIRS = (
    ('eyeLookUpRight', 'EyeLookUpRight'),
    ('eyeLookDownRight', 'EyeLookDownRight'),
    ('eyeLookInRight', 'EyeLookInRight'),
    ('eyeLookOutRight', 'EyeLookOutRight'),
    ('eyeLookUpLeft', 'EyeLookUpLeft'),
    ('eyeLookDownLeft', 'EyeLookDownLeft'),
    ('eyeLookInLeft', 'EyeLookInLeft'),
    ('eyeLookOutLeft', 'EyeLookOutLeft'),
    ('eyeBlinkRight', 'EyeClosedRight'),
    ('eyeBlinkLeft', 'EyeClosedLeft'),
    ('eyeSquintRight', 'EyeSquintRight'),
    ('eyeSquintLeft', 'EyeSquintLeft'),
    ('eyeWideRight', 'EyeWideRight'),
    ('eyeWideLeft', 'EyeWideLeft'),
    ('browDownRight', 'BrowDownRight'),
    ('browDownLeft', 'BrowDownLeft'),
    ('browInnerUp', 'BrowInnerUp'),
    ('browOuterUpRight', 'BrowOuterUpRight'),
    ('browOuterUpLeft', 'BrowOuterUpLeft'),
    ('noseSneerRight', 'NoseSneerRight'),
    ('noseSneerLeft', 'NoseSneerLeft'),
    ('cheekSquintRight', 'CheekSquintRight'),
    ('cheekSquintLeft', 'CheekSquintLeft'),
    ('cheekPuff', 'CheekPuff'),
    ('jawOpen', 'JawOpen'),
    ('mouthClose', 'MouthClosed'),
    ('jawRight', 'JawRight'),
    ('jawLeft', 'JawLeft'),
    ('jawForward', 'JawForward'),
    ('mouthRollUpper', 'LipSuckUpper'),
    ('mouthRollLower', 'LipSuckLower'),
    ('mouthFunnel', 'LipFunnel'),
    ('mouthPucker', 'LipPucker'),
    ('mouthUpperUpRight', 'MouthUpperUpRight'),
    ('mouthUpperUpLeft', 'MouthUpperUpLeft'),
    ('mouthLowerDownRight', 'MouthLowerDownRight'),
    ('mouthLowerDownLeft', 'MouthLowerDownLeft'),
    ('mouthSmileRight', 'MouthSmileRight'),
    ('mouthSmileLeft', 'MouthSmileLeft'),
    ('mouthFrownRight', 'MouthFrownRight'),
    ('mouthFrownLeft', 'MouthFrownLeft'),
    ('mouthStretchRight', 'MouthStretchRight'),
    ('mouthStretchLeft', 'MouthStretchLeft'),
    ('mouthDimpleRight', 'MouthDimpleRight'),
    ('mouthDimpleLeft', 'MouthDimpleLeft'),
    ('mouthShrugUpper', 'MouthRaiserUpper'),
    ('mouthShrugLower', 'MouthRaiserLower'),
    ('mouthPressRight', 'MouthPressRight'),
    ('mouthPressLeft', 'MouthPressLeft'),
    ('tongueOut', 'TongueOut'),
)

ARKIT_TO_UNIFIED = 'ARKIT_TO_UNIFIED'
UNIFIED_TO_ARKIT = 'UNIFIED_TO_ARKIT'

# MMD (MikuMikuDance) model morphs, unlike ARKit/Unified Expressions, aren't a formal tracking spec - they're
# a community naming convention that most PMX models follow (established by early Vocaloid models and
# documented across MMD modding wikis/guides). Each entry below is (mmd_name, ue_components, arkit_components):
# the set of Unified Expressions and/or ARKit shape(s) whose data is duplicated (or, for more than one
# component, blended together at full strength) to build that MMD morph. Only morphs with a clear,
# well-documented correspondence to tracking data are included here - purely stylistic MMD morphs with no
# tracking equivalent (highlights, pupil size, blush, eye sparkle/heart/star variants, etc.) are intentionally
# left out rather than guessed at. An empty arkit_components tuple means that morph has no sensible ARKit-only
# equivalent (it relies on a Unified Expressions "Blended Shape" or Base Shape that ARKit has no counterpart
# for), so it's skipped when translating from ARKit alone.
MMD_SHAPE_RECIPES = (
    # Brows
    ('上', ('BrowUp',), ('browOuterUpLeft', 'browOuterUpRight', 'browInnerUp')),
    ('下', ('BrowDown',), ('browDownLeft', 'browDownRight')),
    ('困る', ('BrowInnerUp',), ('browInnerUp',)),

    # Eyes
    ('まばたき', ('EyeClosed',), ('eyeBlinkLeft', 'eyeBlinkRight')),
    ('笑い', ('EyeClosed',), ('eyeBlinkLeft', 'eyeBlinkRight')),
    ('ウィンク', ('EyeClosedLeft',), ('eyeBlinkLeft',)),
    ('ウィンク右', ('EyeClosedRight',), ('eyeBlinkRight',)),
    ('びっくり', ('EyeWide',), ('eyeWideLeft', 'eyeWideRight')),
    ('じと目', ('EyeSquint',), ('eyeSquintLeft', 'eyeSquintRight')),

    # Mouth
    ('あ', ('JawOpen',), ('jawOpen',)),
    ('い', ('MouthStretchLeft', 'MouthStretchRight'), ('mouthStretchLeft', 'mouthStretchRight')),
    ('う', ('LipPucker',), ('mouthPucker',)),
    ('え', ('JawOpen', 'MouthStretchLeft', 'MouthStretchRight'), ('jawOpen', 'mouthStretchLeft', 'mouthStretchRight')),
    ('お', ('JawOpen', 'LipFunnel'), ('jawOpen', 'mouthFunnel')),
    ('ん', ('MouthClosed',), ('mouthClose',)),
    ('にっこり', ('MouthSmile',), ('mouthSmileLeft', 'mouthSmileRight')),
    ('にやり', ('MouthCornerPullRight',), ()),
    ('口角上げ', ('MouthCornerPullLeft', 'MouthCornerPullRight'), ()),
    ('口角下げ', ('MouthSad',), ('mouthFrownLeft', 'mouthFrownRight')),
)


def _lr(name):
    """Returns the Left and Right Base Shape names for `name` (e.g. 'EyeClosed' -> EyeClosedLeft, EyeClosedRight)."""
    return name + 'Left', name + 'Right'


# Each Unified Expressions "Blended Shape" and the Base Shapes whose poses it combines. Always written in terms
# of Base Shapes only (never other Blended Shapes), so the result never depends on the order they're updated in.
# NOTE: edit this table if your rig combines a Blended Shape differently.
UNIFIED_BLENDED_RECIPES = (
    # Eyes
    ('EyeClosed', _lr('EyeClosed')),
    ('EyeWide', _lr('EyeWide')),
    ('EyeSquint', _lr('EyeSquint')),
    ('EyeDilation', _lr('EyeDilation')),
    ('EyeConstrict', _lr('EyeConstrict')),

    # Brows
    ('BrowDownRight', ('BrowLowererRight', 'BrowPinchRight')),
    ('BrowDownLeft', ('BrowLowererLeft', 'BrowPinchLeft')),
    ('BrowDown', ('BrowLowererRight', 'BrowPinchRight', 'BrowLowererLeft', 'BrowPinchLeft')),
    ('BrowInnerUp', _lr('BrowInnerUp')),
    ('BrowUpRight', ('BrowInnerUpRight', 'BrowOuterUpRight')),
    ('BrowUpLeft', ('BrowInnerUpLeft', 'BrowOuterUpLeft')),
    ('BrowUp', ('BrowInnerUpRight', 'BrowOuterUpRight', 'BrowInnerUpLeft', 'BrowOuterUpLeft')),

    # Nose / Cheeks
    ('NoseSneer', _lr('NoseSneer')),
    ('NasalDilation', _lr('NasalDilation')),
    ('NasalConstrict', _lr('NasalConstrict')),
    ('CheekPuff', _lr('CheekPuff')),
    ('CheekSuck', _lr('CheekSuck')),
    ('CheekSquint', _lr('CheekSquint')),

    # Lips
    ('LipSuckUpper', _lr('LipSuckUpper')),
    ('LipSuckLower', _lr('LipSuckLower')),
    ('LipSuck', _lr('LipSuckUpper') + _lr('LipSuckLower')),
    ('LipFunnelUpper', _lr('LipFunnelUpper')),
    ('LipFunnelLower', _lr('LipFunnelLower')),
    ('LipFunnel', _lr('LipFunnelUpper') + _lr('LipFunnelLower')),
    ('LipPuckerUpper', _lr('LipPuckerUpper')),
    ('LipPuckerLower', _lr('LipPuckerLower')),
    ('LipPucker', _lr('LipPuckerUpper') + _lr('LipPuckerLower')),

    # Mouth
    ('MouthUpperUp', _lr('MouthUpperUp')),
    ('MouthLowerDown', _lr('MouthLowerDown')),
    ('MouthOpen', _lr('MouthUpperUp') + _lr('MouthLowerDown')),
    ('MouthRight', ('MouthUpperRight', 'MouthLowerRight')),
    ('MouthLeft', ('MouthUpperLeft', 'MouthLowerLeft')),
    ('MouthSmileRight', ('MouthCornerPullRight', 'MouthCornerSlantRight')),
    ('MouthSmileLeft', ('MouthCornerPullLeft', 'MouthCornerSlantLeft')),
    ('MouthSmile', ('MouthCornerPullRight', 'MouthCornerSlantRight', 'MouthCornerPullLeft', 'MouthCornerSlantLeft')),
    ('MouthSadRight', ('MouthFrownRight', 'MouthStretchRight')),
    ('MouthSadLeft', ('MouthFrownLeft', 'MouthStretchLeft')),
    ('MouthSad', ('MouthFrownRight', 'MouthStretchRight', 'MouthFrownLeft', 'MouthStretchLeft')),
    ('MouthStretch', _lr('MouthStretch')),
    ('MouthDimple', _lr('MouthDimple')),
    ('MouthTightener', _lr('MouthTightener')),
    ('MouthPress', _lr('MouthPress')),

    # Extra Blended Shapes from MY_CUSTOM_SHAPES that aren't part of the official list.
    ('EyesLookDown', _lr('EyeLookDown')),
    ('EyesLookUp', _lr('EyeLookUp')),
)


def _find_folder(key_blocks, name):
    for key in key_blocks:
        if core.key.is_folder(key) and key.name == name:
            return key
    
    return None


def _ensure_basis(obj):
    if not obj.data.shape_keys:
        core.key.add()


def _create_folder(name):
    folder = core.key.add(type='FOLDER')
    folder.name = name
    return folder


def _ensure_folder(key_blocks, name, parent, transfers):
    """
    Finds or creates a folder by `name`. If it's newly created and `parent` is given, queues a
    (folder_name, parent_name) transfer onto `transfers`, to be applied later in a single memory.tree()
    pass. Existing folders (and their current placement in the hierarchy) are left untouched.
    """
    folder = _find_folder(key_blocks, name)
    
    if not folder:
        folder = _create_folder(name)
        
        if parent is not None:
            transfers.append((folder.name, parent.name))
    
    return folder


def _add_empty_shapes(obj, names, existing_names):
    """
    Adds an empty (no deformation) shape key for each name not already present on the object.
    Returns the list of newly created shape key names, in creation order.
    """
    created = []
    
    for name in names:
        if name in existing_names:
            continue
        
        new_key = obj.shape_key_add(from_mix=False)
        new_key.name = name
        
        created.append(new_key.name)
        existing_names.add(new_key.name)
    
    return created


def _split_custom_shapes():
    """Splits MY_CUSTOM_SHAPES into (base_shapes, blended_shapes) using the marker string."""
    if CUSTOM_BLENDED_SHAPES_MARKER in MY_CUSTOM_SHAPES:
        i = MY_CUSTOM_SHAPES.index(CUSTOM_BLENDED_SHAPES_MARKER)
        return MY_CUSTOM_SHAPES[:i], MY_CUSTOM_SHAPES[i + 1:]
    
    return MY_CUSTOM_SHAPES, ()


def _apply_transfers(transfers, shape_targets):
    """
    Applies queued folder-nesting `transfers` (a list of (child_name, parent_name) tuples) and
    shape-to-folder placements `shape_targets` (a list of (shape_name, folder_name) tuples), in a
    single memory.tree() pass, preserving the given order (earlier entries end up placed first).
    """
    if not transfers and not shape_targets:
        return
    
    tree = memory.tree()
    
    for child, parent in transfers:
        tree.transfer(child, parent)
    
    for name, folder_name in shape_targets:
        tree.transfer(name, folder_name)
    
    tree.apply()


class OBJECT_OT_skp_shape_key_add_arkit(bpy.types.Operator):
    bl_idname = 'object.skp_shape_key_add_arkit'
    bl_label = core.strings['operators.ShapeKeyAddARKit.bl_label']
    bl_description = core.strings['operators.ShapeKeyAddARKit.bl_description']
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.object
        valid_types = {'MESH', 'LATTICE', 'CURVE', 'SURFACE'}
        
        return obj and obj.mode != 'EDIT' and obj.type in valid_types
    
    def execute(self, context):
        obj = context.object
        hidden = core.utils.hide(obj)
        
        _ensure_basis(obj)
        
        key_blocks = obj.data.shape_keys.key_blocks
        existing_names = {key.name for key in key_blocks}
        transfers = []
        
        face_tracking_folder = _ensure_folder(key_blocks, FACE_TRACKING_FOLDER_NAME, None, transfers)
        arkit_folder = _ensure_folder(key_blocks, ARKIT_FOLDER_NAME, face_tracking_folder, transfers)
        
        created = _add_empty_shapes(obj, ARKIT_SHAPES, existing_names)
        
        _apply_transfers(transfers, [(name, arkit_folder.name) for name in created])
        
        core.utils.show(hidden)
        
        skipped = len(ARKIT_SHAPES) - len(created)
        
        if skipped:
            self.report({'INFO'}, core.strings['operators.ShapeKeyAddARKit.execute.report[Skipped %s]'] % skipped)
        
        return {'FINISHED'}


class OBJECT_OT_skp_shape_key_add_unified_expressions(bpy.types.Operator):
    bl_idname = 'object.skp_shape_key_add_unified_expressions'
    bl_label = core.strings['operators.ShapeKeyAddUnifiedExpressions.bl_label']
    bl_description = core.strings['operators.ShapeKeyAddUnifiedExpressions.bl_description']
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.object
        valid_types = {'MESH', 'LATTICE', 'CURVE', 'SURFACE'}
        
        return obj and obj.mode != 'EDIT' and obj.type in valid_types
    
    def execute(self, context):
        obj = context.object
        hidden = core.utils.hide(obj)
        
        _ensure_basis(obj)
        
        key_blocks = obj.data.shape_keys.key_blocks
        existing_names = {key.name for key in key_blocks}
        transfers = []
        
        face_tracking_folder = _ensure_folder(key_blocks, FACE_TRACKING_FOLDER_NAME, None, transfers)
        # "---Unified Expressions---" is queued first, then "---Blended Shapes---" - so that, for a
        # freshly created hierarchy, Blended Shapes always ends up positioned below Unified Expressions.
        unified_folder = _ensure_folder(key_blocks, UNIFIED_EXPRESSIONS_FOLDER_NAME, face_tracking_folder, transfers)
        blended_folder = _ensure_folder(key_blocks, BLENDED_SHAPES_FOLDER_NAME, face_tracking_folder, transfers)
        
        base_created = _add_empty_shapes(obj, UNIFIED_BASE_SHAPES, existing_names)
        blended_created = _add_empty_shapes(obj, UNIFIED_BLENDED_SHAPES, existing_names)
        
        shape_targets = [(name, unified_folder.name) for name in base_created]
        shape_targets += [(name, blended_folder.name) for name in blended_created]
        
        _apply_transfers(transfers, shape_targets)
        
        core.utils.show(hidden)
        
        skipped = (len(UNIFIED_BASE_SHAPES) - len(base_created)) + (len(UNIFIED_BLENDED_SHAPES) - len(blended_created))
        
        if skipped:
            self.report(
                {'INFO'},
                core.strings['operators.ShapeKeyAddUnifiedExpressions.execute.report[Skipped %s]'] % skipped)
        
        return {'FINISHED'}


class OBJECT_OT_skp_shape_key_add_unified_expressions_custom(bpy.types.Operator):
    bl_idname = 'object.skp_shape_key_add_unified_expressions_custom'
    bl_label = core.strings['operators.ShapeKeyAddUnifiedExpressionsCustom.bl_label']
    bl_description = core.strings['operators.ShapeKeyAddUnifiedExpressionsCustom.bl_description']
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.object
        valid_types = {'MESH', 'LATTICE', 'CURVE', 'SURFACE'}
        
        return obj and obj.mode != 'EDIT' and obj.type in valid_types
    
    def execute(self, context):
        obj = context.object
        hidden = core.utils.hide(obj)
        
        _ensure_basis(obj)
        
        key_blocks = obj.data.shape_keys.key_blocks
        existing_names = {key.name for key in key_blocks}
        transfers = []
        
        base_shapes, blended_shapes = _split_custom_shapes()
        
        face_tracking_folder = _ensure_folder(key_blocks, FACE_TRACKING_FOLDER_NAME, None, transfers)
        unified_folder = _ensure_folder(key_blocks, UNIFIED_EXPRESSIONS_FOLDER_NAME, face_tracking_folder, transfers)
        
        base_created = _add_empty_shapes(obj, base_shapes, existing_names)
        
        shape_targets = [(name, unified_folder.name) for name in base_created]
        blended_created = []
        
        if blended_shapes:
            blended_folder = _ensure_folder(key_blocks, BLENDED_SHAPES_FOLDER_NAME, face_tracking_folder, transfers)
            blended_created = _add_empty_shapes(obj, blended_shapes, existing_names)
            shape_targets += [(name, blended_folder.name) for name in blended_created]
        
        _apply_transfers(transfers, shape_targets)
        
        core.utils.show(hidden)
        
        skipped = (len(base_shapes) - len(base_created)) + (len(blended_shapes) - len(blended_created))
        
        if skipped:
            self.report(
                {'INFO'},
                core.strings['operators.ShapeKeyAddUnifiedExpressionsCustom.execute.report[Skipped %s]'] % skipped)
        
        return {'FINISHED'}


class OBJECT_OT_skp_shape_key_add_visemes(bpy.types.Operator):
    bl_idname = 'object.skp_shape_key_add_visemes'
    bl_label = core.strings['operators.ShapeKeyAddVisemes.bl_label']
    bl_description = core.strings['operators.ShapeKeyAddVisemes.bl_description']
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.object
        valid_types = {'MESH', 'LATTICE', 'CURVE', 'SURFACE'}
        
        return obj and obj.mode != 'EDIT' and obj.type in valid_types
    
    def execute(self, context):
        obj = context.object
        hidden = core.utils.hide(obj)
        
        _ensure_basis(obj)
        
        key_blocks = obj.data.shape_keys.key_blocks
        existing_names = {key.name for key in key_blocks}
        
        # The Visemes folder is intentionally standalone - not nested under "---Face Tracking---".
        visemes_folder = _find_folder(key_blocks, VISEMES_FOLDER_NAME)
        
        if not visemes_folder:
            visemes_folder = _create_folder(VISEMES_FOLDER_NAME)
        
        created = _add_empty_shapes(obj, VISEMES, existing_names)
        
        _apply_transfers([], [(name, visemes_folder.name) for name in created])
        
        core.utils.show(hidden)
        
        skipped = len(VISEMES) - len(created)
        
        if skipped:
            self.report({'INFO'}, core.strings['operators.ShapeKeyAddVisemes.execute.report[Skipped %s]'] % skipped)
        
        return {'FINISHED'}


class OBJECT_OT_skp_shape_key_translate_face_tracking(bpy.types.Operator):
    bl_idname = 'object.skp_shape_key_translate_face_tracking'
    bl_label = core.strings['operators.ShapeKeyTranslateFaceTracking.bl_label']
    bl_options = {'REGISTER', 'UNDO'}
    
    direction: bpy.props.EnumProperty(
        items=(
            (ARKIT_TO_UNIFIED, "", ""),
            (UNIFIED_TO_ARKIT, "", "")
        ),
        options={'HIDDEN', 'SKIP_SAVE'})
    
    @classmethod
    def description(cls, context, properties):
        key = (
            'operators.ShapeKeyTranslateFaceTracking.description[ARKit -> Unified]'
            if properties.direction == ARKIT_TO_UNIFIED else
            'operators.ShapeKeyTranslateFaceTracking.description[Unified -> ARKit]')
        
        return core.strings[key]
    
    @classmethod
    def poll(cls, context):
        obj = context.object
        valid_types = {'MESH', 'LATTICE', 'CURVE', 'SURFACE'}
        
        return obj and obj.mode != 'EDIT' and obj.type in valid_types and obj.data.shape_keys
    
    def execute(self, context):
        obj = context.object
        key_blocks = obj.data.shape_keys.key_blocks
        
        # Find every pair whose source shape exists and whose destination shape doesn't yet exist.
        pairs = []
        
        for arkit_name, unified_name in ARKIT_UNIFIED_PAIRS:
            if self.direction == ARKIT_TO_UNIFIED:
                src_name, dst_name = arkit_name, unified_name
            else:
                src_name, dst_name = unified_name, arkit_name
            
            if src_name in key_blocks and dst_name not in key_blocks:
                pairs.append((src_name, dst_name, unified_name))
        
        if not pairs:
            self.report(
                {'WARNING'},
                core.strings['operators.ShapeKeyTranslateFaceTracking.execute.report[No Shapes Found]'])
            
            return {'CANCELLED'}
        
        hidden = core.utils.hide(obj)
        
        transfers = []
        target_folder_name = (
            UNIFIED_EXPRESSIONS_FOLDER_NAME if self.direction == ARKIT_TO_UNIFIED else ARKIT_FOLDER_NAME)
        
        face_tracking_folder = _ensure_folder(key_blocks, FACE_TRACKING_FOLDER_NAME, None, transfers)
        target_folder = _ensure_folder(key_blocks, target_folder_name, face_tracking_folder, transfers)
        blended_folder = None
        
        shape_targets = []
        
        for src_name, dst_name, unified_name in pairs:
            source_key = key_blocks[src_name]
            new_key = core.key.copy(source_key, rename=dst_name)
            
            if self.direction == ARKIT_TO_UNIFIED and unified_name in UNIFIED_BLENDED_SHAPES:
                if blended_folder is None:
                    blended_folder = _ensure_folder(
                        key_blocks, BLENDED_SHAPES_FOLDER_NAME, face_tracking_folder, transfers)
                
                shape_targets.append((new_key.name, blended_folder.name))
            else:
                shape_targets.append((new_key.name, target_folder.name))
        
        _apply_transfers(transfers, shape_targets)
        
        core.utils.show(hidden)
        
        self.report(
            {'INFO'},
            core.strings['operators.ShapeKeyTranslateFaceTracking.execute.report[%s Translated]'] % len(pairs))

        return {'FINISHED'}


class OBJECT_OT_skp_shape_key_translate_mmd(bpy.types.Operator):
    bl_idname = 'object.skp_shape_key_translate_mmd'
    bl_label = core.strings['operators.ShapeKeyTranslateMMD.bl_label']
    bl_description = core.strings['operators.ShapeKeyTranslateMMD.bl_description']
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        valid_types = {'MESH', 'LATTICE', 'CURVE', 'SURFACE'}

        return obj and obj.mode != 'EDIT' and obj.type in valid_types and obj.data.shape_keys

    def execute(self, context):
        obj = context.object
        key_blocks = obj.data.shape_keys.key_blocks

        has_arkit = any(name in key_blocks for name in ARKIT_SHAPES)
        has_unified = any(name in key_blocks for name in UNIFIED_BASE_SHAPES + UNIFIED_BLENDED_SHAPES)

        if not has_arkit and not has_unified:
            self.report({'WARNING'}, core.strings['operators.ShapeKeyTranslateMMD.execute.report[No Shapes Found]'])

            return {'CANCELLED'}

        # If both standards are present, Unified Expressions is preferred: it already provides the bilateral
        # "Blended Shapes" (e.g. a single, combined "EyeClosed") that most MMD morphs need, where ARKit only
        # has separate Left/Right primitives.
        from_unified = has_unified

        created = []

        for mmd_name, ue_components, arkit_components in MMD_SHAPE_RECIPES:
            if mmd_name in key_blocks:
                continue

            component_names = ue_components if from_unified else arkit_components

            if not component_names:
                continue

            source_keys = [key_blocks[name] for name in component_names if name in key_blocks]

            if len(source_keys) != len(component_names):
                continue

            if len(source_keys) == 1:
                new_key = core.key.copy(source_keys[0], rename=mmd_name)
            else:
                new_key = core.key.blend(source_keys, mmd_name)

            created.append(new_key.name)

        if not created:
            self.report({'WARNING'}, core.strings['operators.ShapeKeyTranslateMMD.execute.report[No Shapes Found]'])

            return {'CANCELLED'}

        hidden = core.utils.hide(obj)

        # The "---MMD---" folder is intentionally standalone, like "---Visemes---" - not nested under
        # "---Face Tracking---".
        mmd_folder = _find_folder(key_blocks, MMD_FOLDER_NAME)

        if not mmd_folder:
            mmd_folder = _create_folder(MMD_FOLDER_NAME)

        _apply_transfers([], [(name, mmd_folder.name) for name in created])

        core.utils.show(hidden)

        self.report(
            {'INFO'},
            core.strings['operators.ShapeKeyTranslateMMD.execute.report[%s Translated]'] % len(created))

        return {'FINISHED'}


class OBJECT_OT_skp_shape_key_update_unified_blended(bpy.types.Operator):
    bl_idname = 'object.skp_shape_key_update_unified_blended'
    bl_label = core.strings['operators.ShapeKeyUpdateUnifiedBlended.bl_label']
    bl_description = core.strings['operators.ShapeKeyUpdateUnifiedBlended.bl_description']
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        valid_types = {'MESH', 'LATTICE', 'CURVE', 'SURFACE'}

        return obj and obj.mode != 'EDIT' and obj.type in valid_types and obj.data.shape_keys

    def execute(self, context):
        obj = context.object
        key_blocks = obj.data.shape_keys.key_blocks

        updated = 0

        for blended_name, component_names in UNIFIED_BLENDED_RECIPES:
            target = key_blocks.get(blended_name)

            # The model doesn't have this Blended Shape (e.g. no "EyeClosed"), so skip it.
            if target is None or core.key.is_folder(target):
                continue

            components = []

            for name in component_names:
                key = key_blocks.get(name)

                if key is not None and key is not target and not core.key.is_folder(key):
                    components.append(key)

            # None of the regular shapes it's made from exist on the model, so there's nothing to blend from.
            if not components:
                continue

            _blend_from_shapes(target, components)

            updated += 1

        if not updated:
            self.report(
                {'WARNING'},
                core.strings['operators.ShapeKeyUpdateUnifiedBlended.execute.report[No Shapes Found]'])

            return {'CANCELLED'}

        obj.data.update()

        self.report(
            {'INFO'},
            core.strings['operators.ShapeKeyUpdateUnifiedBlended.execute.report[%s Updated]'] % updated)

        return {'FINISHED'}


def _blend_from_shapes(target, components):
    """
    Rebuilds `target` from scratch as its relative key plus the full-strength offset of every shape in
    `components` (each offset measured against that component's own relative key, normally the Basis).

    This is the same result as running "Blend from Shape" (Additive, Blend 1.0) for each component on an
    otherwise reset shape key, but works directly on the shape key data, so it doesn't need Edit Mode, doesn't
    change the selection and doesn't depend on any vertex being selected.
    """
    import numpy as np

    count = len(target.data) * 3
    buffer = np.empty(count, dtype=np.float32)

    target.relative_key.data.foreach_get('co', buffer)
    result = buffer.copy()

    for component in components:
        component.data.foreach_get('co', buffer)
        result += buffer

        component.relative_key.data.foreach_get('co', buffer)
        result -= buffer

    target.data.foreach_set('co', result)
