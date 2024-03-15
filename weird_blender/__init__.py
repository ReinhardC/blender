bl_info = {
    "name": "Weird Blender", 
    "author": "RClaus",
    "version": (0, 0, 1),
    "blender": (4, 0, 2),
    "location": "",
    "description": "I put everything in here that I need!!!",
    "warning": "Blender is weird",
    "doc_url": "",
    "tracker_url": "",
    "category": "Node"
}

import bpy
from bpy.utils import register_class
from bpy.types import Header, Menu, Panel

# this copies the selected node name into a "special cliboard" along with the material it came from
# currently only works with ImageTextures... please extend who reads this
class MultiCopyOp(bpy.types.Operator):
    bl_idname = "wm.multi_copy_operator"
    bl_label = "MultiCopy"

    def execute(self, context):     
        #area = next(area for area in bpy.context.window.screen.areas if area.type == 'NODE_EDITOR') 
        #with bpy.context.temp_override(window=bpy.context.window, area=area, region=next(region for region in area.regions if region.type == 'WINDOW'), screen=bpy.context.window.screen):        
        selected_obj = context.active_object     
        selected_nodes = context.selected_nodes
        context.scene.clipboard_properties.clipboard_mat = selected_obj.active_material
        context.scene.clipboard_properties.clipboard_nodes.clear()
        for node in selected_nodes:
            new_element = context.scene.clipboard_properties.clipboard_nodes.add()
            new_element.node = node.name
            
        if(len(selected_nodes) == 1):
            ShowMessageBox("Copied name " + selected_nodes[0].name + " in material " + str(selected_obj.active_material.name), "Weird Blender", 'INFO')
        else:
            ShowMessageBox("Copied " + str(len(selected_nodes)) + " names in material " + str(selected_obj.active_material.name), "Weird Blender", 'INFO')
            
        return {'FINISHED'}
    

# this deletes the node with copied name from multiple selected materials
class MultiKillOp(bpy.types.Operator):
    bl_idname = "wm.multi_kill_operator"
    bl_label = "MultiKill"

    def execute(self, context):     
        src_mat = context.scene.clipboard_properties.clipboard_mat
        first_clipboard_node_name = context.scene.clipboard_properties.clipboard_nodes[0].node
      
        area = next(area for area in bpy.context.window.screen.areas if area.type == 'OUTLINER') 
        with bpy.context.temp_override(window=bpy.context.window, area=area, region=next(region for region in area.regions if region.type == 'WINDOW'), screen=bpy.context.window.screen):
            selected_obj = bpy.context.active_object
            selected_items = bpy.context.selected_ids # confusing naming, they use "ids" but mean "items"
            if(len(selected_items) == 0):  
                ShowMessageBox("Blender is weird. This addon sometimes doesn't work. Try switching to another layout and try again.", "Weird Blender Error", 'ERROR')
                return {'FINISHED'}
            
            num_deleted_items = 0
            for item in selected_items:
                if(str(type(item))=="<class 'bpy.types.Material'>"):     
                    for ix in range(len(selected_obj.material_slots)):
                        mat = bpy.context.object.material_slots[ix].material
                        if(item == mat):
                            selected_obj.active_material_index = ix
                            texnode = mat.node_tree.nodes.get(first_clipboard_node_name)
                            if(texnode != None):
                                mat.node_tree.nodes.remove( texnode )
                                num_deleted_items = num_deleted_items + 1
                            
            ShowMessageBox("Deleted " + str(num_deleted_items) + " items from " + str(len(selected_items)) + " selected materials", "Weird Blender", 'INFO')
            
        return {'FINISHED'}
    
    
# this pastes the node with copied name from multiple selected materials
class MultiPasteOp(bpy.types.Operator):
    bl_idname = "wm.multi_paste_operator"
    bl_label = "MultiPaste"

    def execute(self, context):
        src_mat = context.scene.clipboard_properties.clipboard_mat
        first_clipboard_node_name = context.scene.clipboard_properties.clipboard_nodes[0].node
        src_txtnodeimg = bpy.data.images[src_mat.node_tree.nodes[first_clipboard_node_name].image.name]
        
        area = next(area for area in bpy.context.window.screen.areas if area.type == 'OUTLINER') 
        with bpy.context.temp_override(window=bpy.context.window, area=area, region=next(region for region in area.regions if region.type == 'WINDOW'), screen=bpy.context.window.screen):
            selected_obj = bpy.context.active_object
            selected_items = bpy.context.selected_ids # confusing naming, they use "ids" but mean "items"
            if(len(selected_items) == 0):  
                ShowMessageBox("Blender is weird. This addon sometimes doesn't work. Try switching to another layout and try again.", "Weird Blender Error", 'ERROR')
                return {'FINISHED'}
                                
            num_pasted_items = 0
            for item in selected_items:
                if(str(type(item))=="<class 'bpy.types.Material'>"):     
                    for ix in range(len(selected_obj.material_slots)):
                        mat = bpy.context.object.material_slots[ix].material
                        if(item == mat):
                            selected_obj.active_material_index = ix
                            newnode = mat.node_tree.nodes.new("ShaderNodeTexImage")
                            newnode.image = src_txtnodeimg
                            newnode.name = first_clipboard_node_name
                            
                            for node in mat.node_tree.nodes:
                                node.select = False
                                
                            newnode.select = True
                            mat.node_tree.nodes.active = node
                            
                            num_pasted_items = num_pasted_items + 1
                            
            ShowMessageBox("Pasted " + str(num_pasted_items) + " items from " + str(len(selected_items)) + " selected materials", "Weird Blender", 'INFO')
            
        return {'FINISHED'}
        
def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    
class OUTLINER_MT_context_menu_view(Menu):
    bl_label = "Weird Blender"
    def draw(self, _context):
        layout = self.layout
        layout.operator("wm.multi_paste_operator")
        layout.operator("wm.multi_kill_operator")

class NodesListElement(bpy.types.PropertyGroup):
    node: bpy.props.StringProperty()
    
class CliboardPropertyGroup(bpy.types.PropertyGroup):
    clipboard_mat: bpy.props.PointerProperty(type=bpy.types.Material)
    clipboard_nodes: bpy.props.CollectionProperty(type=NodesListElement)
    
class WeirdBlenderMenu(bpy.types.Menu):
    bl_label = "Weird Blender"
    bl_idname = "VIEW3D_MT_blabla_menu"
    
    def draw(self, context):
        layout = self.layout            
        layout.operator("wm.multi_copy_operator", text="MultiCopy")
    
def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.menu(WeirdBlenderMenu.bl_idname)
    
def register():
    from bpy.utils import register_class
    register_class(MultiCopyOp)
    register_class(MultiPasteOp)
    register_class(MultiKillOp)
    register_class(WeirdBlenderMenu)
    register_class(OUTLINER_MT_context_menu_view)  
    register_class(NodesListElement)
    register_class(CliboardPropertyGroup)
    
    bpy.types.Scene.clipboard_properties = bpy.props.PointerProperty(type=CliboardPropertyGroup)
    
    bpy.types.NODE_MT_context_menu.append(draw_menu) # have to use old style append for node popup (better alternative?)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(MultiCopyOp)
    unregister_class(MultiPasteOp)
    unregister_class(MultiKillOp)
    unregister_class(WeirdBlenderMenu)
    unregister_class(OUTLINER_MT_context_menu_view)
    unregister_class(CliboardPropertyGroup)
    unregister_class(NodesListElement)
    
    bpy.types.NODE_MT_context_menu.remove(draw_menu)