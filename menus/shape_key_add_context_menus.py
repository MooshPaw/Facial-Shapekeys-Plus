import bpy

from .. import core


class MESH_MT_skp_shape_key_add_context_menu(bpy.types.Menu):
    bl_label = core.strings['menus.ShapeKeyAddContextMenu.bl_label']
    
    def draw(self, context):
        layout = self.layout
        selections = core.key.get_selected()
        
        if selections:
            row = layout.row()
            
            row.menu(
                menu='MESH_MT_skp_shape_key_add_context_menu_selected',
                text=core.strings['Selected (%s)'] % len(selections),
                translate=False,
                icon='CHECKBOX_HLT')
            
            layout.separator()
        
        row = layout.row()
        row.enabled = not selections
        
        op = row.operator(
            operator='object.skp_shape_key_add',
            icon='MOD_HUE_SATURATION',
            text=core.strings['menus.ShapeKeyAddContextMenu.draw.operator[New Combined]'],
            translate=False)
        
        op.type = 'FROM_MIX'
        
        row = layout.row()
        
        row.enabled = not selections
        
        op = row.operator(
            operator='object.skp_shape_key_add',
            icon='NEWFOLDER',
            text=core.strings['menus.ShapeKeyAddContextMenu.draw.operator[New Folder]'],
            translate=False)
        
        op.type = 'FOLDER'
        
        layout.separator(factor=0.5)
        
        row = layout.row()
        row.enabled = not selections
        
        op = row.operator(
            operator='object.skp_shape_key_add_arkit',
            icon='FACESEL',
            text=core.strings['menus.ShapeKeyAddContextMenu.draw.operator[Add ARKit Blend Shapes]'],
            translate=False)
        
        row = layout.row()
        row.enabled = not selections
        
        op = row.operator(
            operator='object.skp_shape_key_add_unified_expressions',
            icon='FACESEL',
            text=core.strings['menus.ShapeKeyAddContextMenu.draw.operator[Add Unified Expressions Blend Shapes]'],
            translate=False)
        
        row = layout.row()
        row.enabled = not selections
        
        op = row.operator(
            operator='object.skp_shape_key_add_unified_expressions_custom',
            icon='FACESEL',
            text=core.strings['menus.ShapeKeyAddContextMenu.draw.operator[Add Custom Blend Shapes]'],
            translate=False)
        
        row = layout.row()
        row.enabled = not selections
        
        op = row.operator(
            operator='object.skp_shape_key_add_visemes',
            icon='FACESEL',
            text=core.strings['menus.ShapeKeyAddContextMenu.draw.operator[Add Visemes]'],
            translate=False)
        
        layout.separator(factor=0.5)
        
        row = layout.row()
        row.enabled = not selections
        
        op = row.operator(
            operator='object.skp_shape_key_translate_face_tracking',
            icon='FILE_REFRESH',
            text=core.strings['menus.ShapeKeyAddContextMenu.draw.operator[Translate ARKit -> Unified Expressions]'],
            translate=False)
        
        op.direction = 'ARKIT_TO_UNIFIED'
        
        row = layout.row()
        row.enabled = not selections
        
        op = row.operator(
            operator='object.skp_shape_key_translate_face_tracking',
            icon='FILE_REFRESH',
            text=core.strings['menus.ShapeKeyAddContextMenu.draw.operator[Translate Unified Expressions -> ARKit]'],
            translate=False)
        
        op.direction = 'UNIFIED_TO_ARKIT'


class MESH_MT_skp_shape_key_add_context_menu_selected(bpy.types.Menu):
    bl_label = core.strings['menus.ShapeKeyAddContextMenu.bl_label']
    
    def draw(self, context):
        layout = self.layout
        
        op = layout.operator(
            operator='object.skp_shape_key_add',
            icon='MOD_HUE_SATURATION',
            text=core.strings['menus.ShapeKeyAddContextMenu.draw.operator[New Combined]'],
            translate=False)
        
        op.type = 'COMBINED_SELECTED'
