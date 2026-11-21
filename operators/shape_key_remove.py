import bpy

from .. import core
from .. import memory


class OBJECT_OT_skp_shape_key_remove(bpy.types.Operator):
    bl_idname = 'object.skp_shape_key_remove'
    bl_label = core.strings['operators.ShapeKeyRemove.bl_label']
    bl_description = core.strings['operators.ShapeKeyRemove.bl_description']
    bl_options = {'REGISTER', 'UNDO'}
    
    type: bpy.props.EnumProperty(
        items=(
            ('DEFAULT', "", ""),
            ('CLEAR', "", ""),
            ('DEFAULT_SELECTED', "", "")
        ),
        default='DEFAULT',
        options={'HIDDEN', 'SKIP_SAVE'})
    
    @classmethod
    def poll(cls, context):
        return context.object.mode != 'EDIT' and context.object.data.shape_keys
    
    def execute(self, context):
        obj = bpy.context.object
        key_blocks = obj.data.shape_keys.key_blocks
        
        # NOTE: Shape keys are removed with core.key.remove(), which removes them by reference. Never use
        # bpy.ops.object.shape_key_remove() for anything but clearing every key: it deletes whatever key is at the
        # active index at that moment, which is what used to delete the wrong keys (Basis, the top of a folder...)
        # whenever the active index wasn't where this operator expected it to be.
        
        if self.type == 'CLEAR':
            bpy.ops.object.shape_key_remove(all=True)
        elif self.type == 'DEFAULT':
            active_key = obj.active_shape_key
            
            if not active_key:
                return {'CANCELLED'}
            
            # Everything below goes by name, and the highlighted key is read exactly once, right here.
            active_name = active_key.name
            first_index = key_blocks.find(active_name)
            
            tree = memory.tree()
            ancestry = tree.ancestry(active_name)
            location = tree.locate(active_name, ancestry[-1])
            
            # The highlighted key, plus everything inside of it if it's a folder.
            doomed = [active_name] + [key.name for key in core.folder.get_children(active_key)]
            
            # Selections are stored as indices, which are about to shift, so they're remembered by name instead.
            selections = core.key.deselect()
            
            if len(ancestry) > 1:
                core.folder.shift_block_value(key_blocks[ancestry[-1][0]], 'children', -1)
            
            core.key.remove(obj, doomed)
            
            if obj.data.shape_keys and len(obj.data.shape_keys.key_blocks):
                key_blocks = obj.data.shape_keys.key_blocks
                
                # Highlight the key that was right above the removed one, rather than trusting Blender to land there.
                obj.active_shape_key_index = max(first_index - 1, 0)
                
                core.key.reselect(selections)
                
                if obj.active_shape_key.name == key_blocks[0].name and len(key_blocks) > 1:
                    # Don't let the reference key be automatically highlighted unless it's the only key left.
                    obj.active_shape_key_index = 1
                if len(location[0]) > 2:
                    if location[1] == 1:
                        # Don't let the parent key be automatically highlighted unless there are no more family members.
                        if type(location[0][2]) == list:
                            obj.active_shape_key_index = key_blocks.find(location[0][2][0])
                        else:
                            obj.active_shape_key_index = key_blocks.find(location[0][2])
                    else:
                        # Ensure that it's the previous sibling that's selected, not just the previous key.
                        if type(location[0][location[1] - 1]) == list:
                            obj.active_shape_key_index = key_blocks.find(location[0][location[1] - 1][0])
                        else:
                            obj.active_shape_key_index = key_blocks.find(location[0][location[1] - 1])
        elif self.type == 'DEFAULT_SELECTED':
            selections = core.key.deselect()
            selected = set(selections)
            
            tree = memory.tree()
            doomed = []
            
            for name in selections:
                if name not in key_blocks:
                    continue
                
                parents = tree.get_parents(name)
                
                # This key is inside of a folder that is also selected, so it goes when that folder does.
                if any(p in selected for p in parents):
                    continue
                
                key = key_blocks[name]
                
                if parents:
                    # The parent folder is losing a child, so it has to be told, or it will start holding on to
                    # whatever shape keys come after it.
                    core.folder.shift_block_value(key_blocks[parents[0]], 'children', -1)
                
                doomed += [name] + [child.name for child in core.folder.get_children(key)]
            
            first_index = min((key_blocks.find(name) for name in doomed), default=0)
            
            core.key.remove(obj, doomed)
            
            if obj.data.shape_keys and len(obj.data.shape_keys.key_blocks):
                key_blocks = obj.data.shape_keys.key_blocks
                
                obj.active_shape_key_index = max(first_index - 1, 0)
                
                if obj.active_shape_key.name == key_blocks[0].name and len(key_blocks) > 1:
                    # Don't let the reference key be automatically highlighted unless it's the only key left.
                    obj.active_shape_key_index = 1
        
        return {'FINISHED'}
