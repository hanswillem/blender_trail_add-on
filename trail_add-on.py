# ----------------------------------------------------------------------
#
# Trails the active object for 10 frames.
# For this to work there needs to be a goup named 'trailGroup'
#
# ----------------------------------------------------------------------


bl_info = {
    'name' : 'Trail',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 0),
    'blender' : (2, 79),
    'location' : 'View 3D > Tools > Trail',
    'description' : 'Trails the active object',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'Motion Graphics'
    }


#imports
import bpy


#some global vars
trailLength = 10
l = []
isTrailing = False


def main_trail(scene):
    ob = bpy.context.active_object
    if scene.frame_current == 0:
        del l[:]
        for i in bpy.data.objects:
            if i.type == 'EMPTY':    
                bpy.data.objects.remove(i)
                
    else:
        inst = bpy.data.objects.new('Instance', None)
        inst.dupli_type = 'GROUP'
        inst.empty_draw_size = 0
        inst.dupli_group = bpy.data.groups["trailGroup"]
        inst.location = ob.location
        inst.rotation_euler = ob.rotation_euler
        inst.hide_select = True
        bpy.context.scene.objects.link(inst)
        l.append(inst)  
        if len(l) > trailLength:

            bpy.data.objects.remove(l[0])
            l.remove(l[0])


def main_startTrail():
    global isTrailing
    isTrailing = True
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.frame_change_pre.append(main_trail)
    

def main_stopTrail():
    global isTrailing
    isTrailing = False
    bpy.app.handlers.frame_change_pre.clear()
    
def groupExists():
    a = False;
    for i in bpy.data.groups:
        if i.name == 'trailGroup':
            return True
    return a
    
    
#panel class
class Panel_trail(bpy.types.Panel):
    
    #panel attributes
    """What does this panel do?"""
    bl_label = 'Trail'
    bl_idname = 'tools_my_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Trail'
    
    #draw loop
    def draw(self, context):
        layout = self.layout
        if not groupExists():
            layout.label('no trailGroup!')
        col = layout.column(align = True)
        if isTrailing:
            col.operator('script.operator_stop_trail', text="Stop Trail")
        else:
            col.operator('script.operator_start_trail', text="Start Trail")
        
        

#operator class
class Operator_startTrail(bpy.types.Operator):
    
    #operator attributes
    """What does this operator do?"""
    bl_label = 'My Operator'
    bl_idname = 'script.operator_start_trail'
    bl_options = {'REGISTER', 'UNDO'}
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return groupExists()
    
    #execute
    def execute(self, context):
        main_startTrail()
        
        return {'FINISHED'}


#operator class
class Operator_stopTrail(bpy.types.Operator):
    
    #operator attributes
    """What does this operator do?"""
    bl_label = 'My Operator'
    bl_idname = 'script.operator_stop_trail'
    bl_options = {'REGISTER', 'UNDO'}
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return 2 > 1
    
    #execute
    def execute(self, context):
        main_stopTrail()
        
        return {'FINISHED'}

        
#registration
def register():
    bpy.utils.register_class(Panel_trail)
    bpy.utils.register_class(Operator_startTrail)
    bpy.utils.register_class(Operator_stopTrail)
    

def unregister():
    bpy.utils.unregister_class(Panel_trail)
    bpy.utils.unregister_class(Operator_startTrail)
    bpy.utils.unregister_class(Operator_stopTrail)


#enable to test the addon by running this script
if __name__ == '__main__':
    register()
