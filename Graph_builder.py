# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {"name":"Graph","category": "object" ,
           "version": (1, 0),
          "blender": (2, 70, 0),
           "location": "View3D >Tools ",
           "Author":"Deependra Singh Rathore"}
import bpy 
import math
    

#<---------------->

class base(bpy.types.Operator):
    """Graph"""   
    bl_idname = "objects.generate_base"   # Unique identifier for buttons and menu items to reference.
    bl_label = "Generate Graph"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'} 
    data = []
    
    def data_input(self):
        data_string = bpy.context.scene.base_data
        self.data = data_string.split(",")
    
    
    def value(self,object,text):
        if bpy.context.scene.bar_text_Vertical == True:
            rotx = 90
        else:
            rotx = 0
        
        if bpy.context.scene.bar_text_onTop == True:
            bpy.ops.object.text_add(location=(object.location[0], object.location[1]-(object.scale[1]/2), object.location[2]+object.scale[2]), rotation=(math.radians(rotx),0,math.radians(90)))
        elif bpy.context.scene.bar_text_onFace == True:
            bpy.ops.object.text_add(location=(object.location[0]+object.scale[0]*2, object.location[1]-(object.scale[1]*2), object.location[2]+object.scale[2]-1), rotation=(math.radians(rotx),0,math.radians(90)))
        else:
            bpy.ops.object.text_add(location=(object.location[0]+(object.scale[1]/2 +1), object.location[1]-(object.scale[1]/2),(object.location[2])+0.5), rotation=(math.radians(rotx),0,0))
    
        text_obj = bpy.context.object
        text_obj.name = "Value" 
        text_obj.data.body = str(text) + bpy.context.scene.text_value
        text_obj.data.size = bpy.context.scene.bar_text_size
        text_obj.data.extrude     = 0.05
        text_obj.data.bevel_depth = 0.01   
    
    def execute(self,context):
        self.data_input()
        no_of_bars = len(self.data)
        gap = bpy.context.scene.graph_bars_gap
        Bars = []
        lx = bpy.context.scene.graph_originx
        ly = bpy.context.scene.graph_originy
        lz = bpy.context.scene.graph_originz
        #CODE
        #Add Bar
        while(no_of_bars>0):
            bpy.ops.mesh.primitive_plane_add(location = (lx,ly,lz), radius = bpy.context.scene.graph_bar_size)
            bpy.context.active_object.name = "Bar"
            Bars.append(bpy.context.active_object)
            # Go to edit mode, face selection mode and select all faces
            bpy.ops.object.mode_set( mode   = 'EDIT'   )
            bpy.ops.mesh.select_mode( type  = 'FACE'   )
            bpy.ops.mesh.select_all( action = 'SELECT' ) 
            bpy.ops.mesh.extrude_region_move(
                TRANSFORM_OT_translate={"value":(0, 0,bpy.context.scene.base_size)}
            )
            #select_all Unwrap
            bpy.ops.mesh.select_all( action = 'SELECT' ) 
            bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
            bpy.ops.object.mode_set( mode = 'OBJECT' )
            ly += gap  
            no_of_bars -= 1
            
            
        for i in Bars:
            if bpy.context.scene.bar_text == True:
                self.value(i,self.data[Bars.index(i)])
        return {'FINISHED'}

#<----------------------------------------------------------------------->


class graph(bpy.types.Operator):
    """Graph"""   
    bl_idname = "objects.generate_graph"   # Unique identifier for buttons and menu items to reference.
    bl_label = "Generate Graph"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'} 
    data = []
    currframe = 0
           
    def value(self,object,text):
        if bpy.context.scene.bar_text_Vertical == True:
            rotx = 90
        else:
            rotx = 0
        
        if bpy.context.scene.bar_text_onTop == True:
            bpy.ops.object.text_add(location=(object.location[0], object.location[1]-(object.scale[1]/2), object.location[2]+object.scale[2]), rotation=(math.radians(rotx),0,math.radians(90)))
        elif bpy.context.scene.bar_text_onFace == True:
            bpy.ops.object.text_add(location=(object.location[0]+object.scale[0], object.location[1]-(object.scale[1]/2), object.location[2]+object.scale[2]-1), rotation=(math.radians(rotx),0,math.radians(90)))
        else:
            bpy.ops.object.text_add(location=(object.location[0]+(object.scale[1]/2 +1), object.location[1]-(object.scale[1]/2),(object.location[2])+0.5), rotation=(math.radians(rotx),0,0))
           
        #print("test")
        text_obj = bpy.context.object
        text_obj.name = "Value" 
        text_obj.data.body = str(text) + bpy.context.scene.text_value
        text_obj.data.size = bpy.context.scene.bar_text_size
        text_obj.data.extrude     = 0.05
        text_obj.data.bevel_depth = 0.01   
    
    def data_input(self):
        data_string = bpy.context.scene.graph_data
        self.data = data_string.split(",")
        for i in range(0,len(self.data)):
            try:
                self.data[i] = int(self.data[i])
            except:
                self.data[i] = float(self.data[i])

    def animate(self,object,property,value,frames):
        self.currframe = self.currframe + bpy.context.scene.graph_animation_delay
        bpy.context.scene.frame_current =  self.currframe
        object.scale[2] = bpy.context.scene.graph_init_height
        object.keyframe_insert(data_path = property)
        
        self.currframe = self.currframe + bpy.context.scene.graph_animation_duration
        bpy.context.scene.frame_current =+ self.currframe
        object.scale[2] = value*bpy.context.scene.graph_mult_factor
        object.keyframe_insert(data_path = property) 
      
    def execute(self,context):
        self.data_input()
        no_of_bars = len(self.data)
        gap = bpy.context.scene.graph_bars_gap
        Grid_size = bpy.context.scene.graph_grid_size
        Bars = []
        lx = bpy.context.scene.graph_originx
        ly = bpy.context.scene.graph_originy
        lz = bpy.context.scene.graph_originz
        #CODE
        #Add Grid
        bpy.ops.mesh.primitive_grid_add(location=(-1,Grid_size/2,Grid_size/2),radius = Grid_size , rotation = (0,math.radians(90),0))
        bpy.ops.object.modifier_add(type='WIREFRAME')
        #Add Plane
        bpy.ops.mesh.primitive_plane_add( location = (0,0,0),radius = 50)

        #Add Bar
        while(no_of_bars>0):
            bpy.ops.mesh.primitive_plane_add(location = (lx,ly,lz), radius = bpy.context.scene.graph_bar_size)
            bpy.context.active_object.name = "Bar"
            Bars.append(bpy.context.active_object)
            # Go to edit mode, face selection mode and select all faces
            bpy.ops.object.mode_set( mode   = 'EDIT'   )
            bpy.ops.mesh.select_mode( type  = 'FACE'   )
            bpy.ops.mesh.select_all( action = 'SELECT' ) 
            bpy.ops.mesh.extrude_region_move(
                TRANSFORM_OT_translate={"value":(0, 0, 1)}
            )
            bpy.ops.object.mode_set( mode = 'OBJECT' )
            ly += gap  
            no_of_bars -= 1

        #Set initial frame 
        bpy.context.scene.frame_current = 0
        
        for i in Bars:
            i.select = True
            scl = self.data[Bars.index(i)]
            if bpy.context.scene.animate_bar == True:
                self.animate(i,"scale",scl,30)
            else:
                i.scale[2] = scl
                
            if bpy.context.scene.bar_text == True:
                self.value(i,scl)
        return {'FINISHED'}

#<----------------------------------------------------------------------->
 
class graph_builder_panel(bpy.types.Panel):
    bl_idname = "panel.panel1"
    bl_label = "Graph Builder"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    # bl_category = "Tools"
    bl_category = "GraphBuilder"

    def draw(self, context):
        ob = context.object
        row = self.layout.row()
        row.label("Generate Graph")
        row = self.layout.row()
        row.prop(context.scene,"graph_data")
        row = self.layout.row()
        row.prop(context.scene,"graph_mult_factor")
        row = self.layout.row()
        row.operator("objects.generate_graph", icon='MESH_CUBE', text="Generate")
        row = self.layout.row()
        row.prop(context.scene,"graph_originx")
        row = self.layout.row()
        row.prop(context.scene,"graph_originy")
        row = self.layout.row()
        row.prop(context.scene,"graph_originz")
        row = self.layout.row()
        row.prop(context.scene,"graph_bars_gap")
        row = self.layout.row()
        row.prop(context.scene,"graph_grid_size")
        row = self.layout.row()
        row.prop(context.scene,"grap_bar_size")
        row = self.layout.row()
        row.prop(context.scene,"graph_init_height")
        

class graph_builder_panel2(bpy.types.Panel):
    bl_idname = "panel.panel2"
    bl_label = "Animation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "GraphBuilder"

    def draw(self, context):
        row = self.layout.row()
        row.prop(context.scene,"animate_bar")
        row = self.layout.row()
        row.prop(context.scene,"graph_animation_duration")
        row = self.layout.row()
        row.prop(context.scene,"graph_animation_delay")
        
class graph_builder_panel3(bpy.types.Panel):
    bl_idname = "panel.panel3"
    bl_label = "Base"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "GraphBuilder"

    def draw(self, context):
        row = self.layout.row()
        row.prop(context.scene,"base_data")
        row = self.layout.row()
        row.operator("objects.generate_base", icon='MESH_CUBE', text="Generate")
        row = self.layout.row()
        row.prop(context.scene,"base_size")
        
class graph_builder_panel4(bpy.types.Panel):
    bl_idname = "panel.panel4"
    bl_label = "Text"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "GraphBuilder"

    def draw(self, context):
        row = self.layout.row()
        row.prop(context.scene,"text_value")
        row = self.layout.row()
        row.prop(context.scene,"bar_text")
        row = self.layout.row()
        row.prop(context.scene,"bar_text_size")
        row = self.layout.row()
        row.prop(context.scene,"bar_text_onFace")
        row = self.layout.row()
        row.prop(context.scene,"bar_text_onTop")
        row = self.layout.row()
        row.prop(context.scene,"bar_text_Vertical")
       

        

#<-----------------------------------------------------------------------------> 
  
def register():
    #String
    bpy.types.Scene.graph_data = bpy.props.StringProperty(name = "Graph Data",description = "Data values",default = "1,2,3")
    bpy.types.Scene.base_data = bpy.props.StringProperty(name = "Base Data",description = "Data values",default = "Name1,Name2,Name3")
    bpy.types.Scene.text_value = bpy.props.StringProperty(name = "Text",description = "Suffix for value",default = "Units")
    #Integers
    bpy.types.Scene.graph_animation_duration = bpy.props.IntProperty(name = "Animation Duration(In Frames)",description = "Data values",default = 30,min =0)
    bpy.types.Scene.graph_animation_delay = bpy.props.IntProperty(name = "Animation Dealy(In Frames)",description = "Data values",default = 30,min=0)

    #Floats
    bpy.types.Scene.graph_originx = bpy.props.FloatProperty(name = "Originx",description = "Data values",default = 1,min=0)
    bpy.types.Scene.graph_originy = bpy.props.FloatProperty(name = "Originy",description = "Data values",default = 1,min=0)
    bpy.types.Scene.graph_originz = bpy.props.FloatProperty(name = "Originz",description = "Data values",default = 1,min=0)
    bpy.types.Scene.graph_bars_gap = bpy.props.FloatProperty(name = "Gap",description = "Data values",default = 4,min=0)
    bpy.types.Scene.graph_grid_size = bpy.props.FloatProperty(name = "Grid Size",description = "Data values",default = 10,min=0)
    bpy.types.Scene.graph_bar_size = bpy.props.FloatProperty(name = "Bar Size",description = "Data values",default = 1,min=0)
    bpy.types.Scene.base_size = bpy.props.FloatProperty(name = "Base Size",description = "Data values",default = 1,min=0)
    bpy.types.Scene.graph_init_height = bpy.props.FloatProperty(name = "Bar Initial Size",description = "Data values",default = 1,min=0)
    bpy.types.Scene.graph_mult_factor = bpy.props.FloatProperty(name = "Factor",description = "Data values",default = 1,min=0)
    bpy.types.Scene.bar_text_size = bpy.props.FloatProperty(name = "Size",description = "Bar Text Size",default = 1.0)
    #Bools
    bpy.types.Scene.bar_text_Vertical = bpy.props.BoolProperty(name = "Vertical",description = "Data values",default = True)
    bpy.types.Scene.bar_text_onFace = bpy.props.BoolProperty(name = "Front of Bar",description = "Text in front of bar",default = True)
    bpy.types.Scene.bar_text_onTop = bpy.props.BoolProperty(name = "Top of Bar",description = "Text on top of bar",default = True)
    bpy.types.Scene.bar_text = bpy.props.BoolProperty(name = "Show Text/Value",description = "Show Text or Values",default = True)
    bpy.types.Scene.animate_bar = bpy.props.BoolProperty(name = "Animate",description = "Whether to Animate Bars or Not",default = True)

    
    bpy.utils.register_class(graph)
    bpy.utils.register_class(base)
    bpy.utils.register_class(graph_builder_panel)
    bpy.utils.register_class(graph_builder_panel2)
    bpy.utils.register_class(graph_builder_panel3)
    bpy.utils.register_class(graph_builder_panel4)
    
def unregister():
    bpy.utils.register_class(graph)
    bpy.utils.register_class(base)
    bpy.utils.register_class(graph_builder_panel)
    bpy.utils.register_class(graph_builder_panel2)
    bpy.utils.register_class(graph_builder_panel3)
    bpy.utils.register_class(graph_builder_panel4)
    
if __name__ == "__main__" :
    register()
