import bpy

from .. import core
from .. import memory


# These folder names are literal shape key / vertex group data (not UI text), so they are
# intentionally not run through core.strings translation.
FACE_TRACKING_FOLDER_NAME = "---Face Tracking---"
BLENDED_SHAPES_FOLDER_NAME = "---Blended Shapes---"


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
# MooshPaw's CUSTSOM PRESET for UE Expressions that are actually in use
MY_CUSTOM_SHAPES = (
    # Eye Brows
    'BrowDownLeft', 'BrowDownRight',
    'BrowInnerUpLeft', 'BrowInnerUpRight',
    'BrowLowererLeft', 'BrowLowererRight',
    'BrowOuterUpLeft', 'browOuterUpRight',
    'BrowPinchLeft', 'BrowPinchRight',

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
    'JawBackward', 'JawForward',
    'JawLeft', 'JawOpen', 'JawRight',

    # Lips
    'LipSuckUpperLeft', 'LipSuckUpperRight',
    'LipSuckLowerLeft', 'LipSuckLowerRight',

    # Mouth
    'MouthClosed',
    'MouthDimpleLeft', 'MouthDimpleRight',
    'MouthFrownLeft', 'MouthFrownRight',
    'MouthLeft', 'MouthRight',
    'MouthPressLeft', 'MouthPressRight',
    'MouthRaiserUpper', 'MouthRaiserLower',
    'MouthSmileLeft', 'mouthSmileRight',
    'MouthStretchLeft', 'MouthStretchRight',
    'MouthUpperUpLeft', 'MouthUpperUpRight',
    'MouthLowerDownLeft', 'MouthLowerDownRight',

    #Nose
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
    'BrowInnerUp',
    'CheekPuff',
    'LipSuckLower',
    'LipSuckUpper',
    'LipFunnel', 'LipPucker',
    'EyesLookDown', 'EyesLookUp',
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
        
        folder = _find_folder(key_blocks, FACE_TRACKING_FOLDER_NAME)
        
        if not folder:
            folder = _create_folder(FACE_TRACKING_FOLDER_NAME)
        
        created = _add_empty_shapes(obj, ARKIT_SHAPES, existing_names)
        
        if created:
            tree = memory.tree()
            
            for name in created:
                tree.transfer(name, folder.name)
            
            tree.apply()
        
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
        
        face_tracking_folder = _find_folder(key_blocks, FACE_TRACKING_FOLDER_NAME)
        
        if not face_tracking_folder:
            face_tracking_folder = _create_folder(FACE_TRACKING_FOLDER_NAME)
        
        blended_folder = _find_folder(key_blocks, BLENDED_SHAPES_FOLDER_NAME)
        blended_folder_created_now = False
        
        if not blended_folder:
            blended_folder = _create_folder(BLENDED_SHAPES_FOLDER_NAME)
            blended_folder_created_now = True
        
        base_created = _add_empty_shapes(obj, UNIFIED_BASE_SHAPES, existing_names)
        blended_created = _add_empty_shapes(obj, UNIFIED_BLENDED_SHAPES, existing_names)
        
        tree = memory.tree()
        
        # Nest "Blended Shapes" inside "Face Tracking", but only the first time it's created,
        # so that a user's own re-organization of the hierarchy isn't undone on subsequent runs.
        if blended_folder_created_now:
            tree.transfer(blended_folder.name, face_tracking_folder.name)
        
        for name in base_created:
            tree.transfer(name, face_tracking_folder.name)
        
        for name in blended_created:
            tree.transfer(name, blended_folder.name)
        
        tree.apply()
        
        core.utils.show(hidden)
        
        skipped = (len(UNIFIED_BASE_SHAPES) - len(base_created)) + (len(UNIFIED_BLENDED_SHAPES) - len(blended_created))
        
        if skipped:
            self.report(
                {'INFO'},
                core.strings['operators.ShapeKeyAddUnifiedExpressions.execute.report[Skipped %s]'] % skipped)
        
        return {'FINISHED'}
