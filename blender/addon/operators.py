import bpy
import os
import subprocess
from mathutils import Vector


def generate_sky(context):
    s = context.scene.radiance
    with open("sky.rad", "w") as f:
        f.write(f"!gensky {s.sky_month} {s.sky_day} ")
        if s.is_sky_time_zone:
            TZone = s.sky_DST if s.is_sky_DST else s.sky_LST
            f.write(f"{s.sky_time_h}:{s.sky_time_min}{TZone} ")
        else:
            f.write(f"{s.sky_meridian}")

        if s.is_sky_year:
            f.write(f"-y {s.sky_year} {s.sky_type}")
        f.write(f" -a {s.sky_latitude} -o {s.sky_longitude}\n\n")
        f.write("skyfunc glow sky_glow\n0\n0\n4 .9 .9 1.15 0\n")
        f.write("sky_glow source sky\n0\n0\n4 0 0 1 180\n")
        f.write("skyfunc glow ground_glow\n0\n0\n4 1.4 .9 .6 0\n")
        f.write("ground_glow source ground\n0\n0\n4 0 0 -1 180")


def generate_view(context, cam_name):
    cam = bpy.data.objects[cam_name]
    lx, ly, lz = cam.location
    ux, uy, uz = cam.rotation_euler.to_matrix() @ Vector((0.0, 1.0, 0.0))
    dx, dy, dz = cam.rotation_euler.to_matrix() @ Vector((0.0, 0.0, -1.0))
    with open(f"{cam_name}.vf", "w") as f:
        f.write(f"rvu -vtv -vp {lx} {ly} {lz} -vd {dx} {dy} {dz} -vu {ux} {uy} {uz}")


def generate_rif(context, cam_name):
    s = context.scene.radiance
    resol = s.resolution
    with open(f"{s.file_name}.rif", "w") as f:
        f.write(f"OCTREE= {s.file_name}.oct\n")
        f.write(f"AMB = {s.amb_file}\n")
        f.write(f"scene = sky.rad {s.file_name}.rad\n\n")
        f.write(f"EXPOSURE = {str(s.exposure)}\n")
        f.write(f"VARIABILITY = {s.variability}\n")
        f.write(f"DETAIL = {s.detail}\n")
        f.write(f"QUALITY = {s.quality}\n\n")
        f.write(f"INDIRECT = {str(s.indirect)}\n")
        f.write(f"PENUMBRAS = {str(s.penumbras)}\n")
        f.write(f"RESOLUTION = {str(resol[0])} {str(resol[1])}\n")
        if s.is_false_color:
            f.write("render = -i\n")
        f.write(f"PICTURE = {s.file_name}\n")
        f.write(f"view = {cam_name} -vf {cam_name}.vf\n")
        f.write(f"REPORT = 0.2")


class Material:
    """ Define the materials of the Scene in Radiance language"""

    def __init__(self, filename):
        self.filename = filename
        self.content = ""

    def addMaterialLight(self, id, input, modifier=""):
        color = input.color
        self.content += f"void light {id} \n 0 \n 0 \n 3 {color[0]} {color[1]} {color[2]}"
        self.content += "\n"
       
    def addMaterialIllum(self, id, input, modifier=""):
        color = input.color
        mod = "void" if len(modifier) == 0 else modifier[0].material
        self.content += f"void illum {id} \n 1 {mod} \n 0 \n 3 {color[0]} {color[1]} {color[2]}"
        self.content += "\n"

    def addMaterialGlow(self, id, input, modifier=""):
        color = input.color
        self.content += f"void glow {id} \n 0 \n 0 \n 4 {color[0]} {color[1]} {color[2]} {input.maxrad}"
        self.content += "\n"
       
    def addMaterialSpotlight(self, id, input, modifier=""):
        color = input.color
        dir = input.direction
        self.content += f"void spotlight {id} \n 0 \n 0 \n 7 {color[0]} {color[1]} {color[2]} {input.angle} {dir[0]} {dir[1]} {dir[2]}"
        self.content += "\n"
       
    def addMaterialMirror(self, id, input, modifier):
        color = input.color
        if modifier.values() == []:
            self.content += f"void mirror {id} \n 0 \n 0 \n 3 {color[0]} {color[1]} {color[2]}"
        else:
            self.content += f"void mirror {id} \n 1 {modifier[0].material} \n 0 \n 3 {color[0]} {color[1]} {color[2]}"
        self.content += "\n"
       
    def addMaterialPlastic(self,id, input, modifier = ""): 
        color = input.color
        self.content += f"void plastic {id} \n 0 \n 0 \n 5 {color[0]} {color[1]} {color[2]} {input.spec} {input.rough}"
        self.content += "\n"
        
    def addMaterialMetal(self,id, input, modifier = ""):
        color = input.color
        self.content += f"void metal {id} \n 0 \n 0 \n 5 {color[0]} {color[1]} {color[2]} {input.spec} {input.rough}"
        self.content += "\n"
        
    def addMaterialTrans(self,id, input, modifier = ""):
        color = input.color
        self.content += f"void trans {id} \n 0 \n 0 \n 7 {color[0]} {color[1]} {color[2]} {input.spec} {input.rough} {input.trans} {input.tspec}"
        self.content += "\n"

    def addMaterialDielectric(self,id, input, modifier = ""):
        colortn = input.color
        self.content += f"void dielectric {id} \n 0 \n 0 \n 5 {colortn[0]} {colortn[1]} {colortn[2]} {input.n1} {input.hc}"
        self.content += "\n"
            
    def addMaterialGlass(self,id, input, modifier = ""):
        colortn = input.color
        self.content += f"void glass {id} \n 0 \n 0 \n 5 {colortn[0]} {colortn[1]} {colortn[2]}"
        self.content += "\n"
        
    def addMaterialAntimatter(self,id,input="", modifier=""):
        mods = [m.material for m in modifier]
        self.content += f"void antimatter {id} \n {len(mods)} {' '.join(mods)} \n 0 \n 0"
        self.content += "\n"

    def addMaterialColorTexture(self, id, textureHdr, inp):
        mat = inp.material_type
        self.content += f"void colorpict {id}_map\n 7 red green blue {textureHdr}.hdr .  frac(Lu)  frac(Lv) \n 0 \n 0"
        self.content += "\n"
        self.content += f"{id}_map {mat} {id} \n 0 \n 0 \n 5 1 1 1 {inp.spec} {inp.rough}"
        self.content += "\n"


def obj2rad(context, ob, materials, mod):
    """Specifies the materials (mod) of the mesh"""

    bpy.ops.export_scene.obj(
        filepath=f"{ob.name}.obj", use_selection=True, axis_forward="Y", axis_up="Z"
    )

    command = f"obj2mesh -a {materials} {ob.name}.obj {ob.name}.rtm"
    os.system(command)

    with open(f"{ob.name}.rad", "w") as f:
        f.write(f"{mod} mesh {ob.name}\n")
        f.write(f"1 {ob.name}.rtm\n0\n0\n")


def get_text2hdr(context, m):
    """Converts all the blender textures to hdr textures"""

    surface = (
        m.node_tree.nodes.get("Material Output").inputs["Surface"].links[0].from_node
    )
    if surface.inputs["Base Color"].is_linked:
        texture = surface.inputs["Base Color"].links[0].from_node

        texture.image.save_render(m.name)
        command = f"mogrify -format hdr {m.name}"
        os.system(command)
        return m.name
    else:
        raise Exception("There is no texture linked in Base Color")


def generate_material(context, mat, file):
    """Converts all the object materials (visibles) in Radiance material"""

    rad = mat.radiance
    if rad.is_texture:
        hdr = get_text2hdr(context, mat)
        file.addMaterialColorTexture(mat.name, hdr, rad)
    else:
        mod = mat.modifier
        addMaterials = {
            "light": file.addMaterialLight,
            "illum": file.addMaterialIllum,
            "glow": file.addMaterialGlow,
            "spotlight": file.addMaterialSpotlight,
            "mirror": file.addMaterialMirror,
            "plastic": file.addMaterialPlastic,
            "metal": file.addMaterialMetal,
            "trans": file.addMaterialTrans,
            "dielectric": file.addMaterialDielectric,
            "glass": file.addMaterialGlass,
            "antimatter": file.addMaterialAntimatter,
        }
        addMaterials[rad.material_type](mat.name, rad, mod)


class RAD_OT_Export(bpy.types.Operator):
    """Esport the scene in Radiance"""

    bl_idname = "radiance.export"
    bl_label = "Export Export the thebjects to rad"

    def execute(self, context):
        file_name = context.scene.radiance.file_name

        scene = ""
        bpy.ops.object.select_all(action="DESELECT")
        for ob in context.scene.objects:
            if ob.visible_get() and ob.type == "MESH":
                ob.select_set(True)

                # material automatitzation
                file = Material(f"{ob.name}.mat")
                for mat in ob.material_slots:
                    generate_material(context, mat.material, file)

                with open(f"{file.filename}", "w") as f:
                    f.write(file.content)

                obj2rad(context, ob, file.filename, "void")
                ob.select_set(False)

            if ob.visible_get() and (ob.type == "MESH" or ob.type == "LIGHT"):
                lx, ly, lz = ob.location
                rx, ry, rz = ob.rotation_euler
                scene += f"!xform -t {lx} {ly} {lz} -rx {rx} -ry {ry} -rz {rz} {ob.name}.rad\n"

        with open(f"{file_name}.rad", "w") as f:
            f.write(scene)

        return {"FINISHED"}


class RAD_OT_Preview(bpy.types.Operator):
    """Preview the scene in Radiance"""

    bl_idname = "radiance.preview"
    bl_label = "Preview rendering"
    
    def execute(self, context):
        s = context.scene.radiance
        cam_name = context.scene.radiance.camera.name_full

        generate_sky(context)
        generate_view(context, cam_name)
        generate_rif(context, cam_name)
        command = f"rad -o x11 {s.file_name}.rif"
        os.system(command)
        return {"FINISHED"}


class RAD_OT_Render(bpy.types.Operator):
    """Render the scene in Radiance"""

    bl_idname = "radiance.render"
    bl_label = "Preview rendering"

    def execute(self, context):
        s = context.scene.radiance
        cam_name = context.scene.radiance.camera.name_full
        
        generate_sky(context)
        generate_view(context, cam_name)
        generate_rif(context, cam_name)
        command = f"rad  {s.file_name}.rif"
        os.system(command)
        if s.is_false_color:
            file = f"{s.file_name}_{s.camera.name_full}.hdr"
            command = f"falsecolor -ip {file} -l Lux > falseC_{file}"
            os.system(command)
        return {"FINISHED"}


class MOD_OT_Add(bpy.types.Operator):
    """Add another material type to active_material.modifiers"""

    bl_idname = "modifiers.add"
    bl_label = "Add"

    def execute(self, context):
        item = bpy.context.object.active_material.modifiers.add()
        item.material = context.object.active_material.radiance.material_type
        return {"FINISHED"}


class MOD_OT_Remove(bpy.types.Operator):
    """Remove a material type in active_material.modifiers"""

    bl_idname = "modifiers.remove"
    bl_label = "Remove"

    index: bpy.props.IntProperty()

    def execute(self, context):
        bpy.context.object.active_material.modifiers.remove(self.index)
        return {"FINISHED"}


class MOD_OT_Clear(bpy.types.Operator):
    """Remove a material type in active_material.modifiers"""

    bl_idname = "modifiers.clear"
    bl_label = "Clean all"

    def execute(self, context):
        bpy.context.object.active_material.modifiers.clear()
        return {"FINISHED"}


class LIGHT_OT_Color(bpy.types.Operator):
    """Obtain the color from the lampcolor program"""

    bl_idname = "radiance.get_color"
    bl_label = "Get color"

    def execute(self, context):

        rad = context.light.radiance

        params = f'"{rad.lamp_type}\n{rad.lamp_unit}\n{rad.lamp_geom}\n'
        if rad.lamp_geom == "polygon":
            params = f'{rad.area}\n{rad.lamp_lm}"'
        else:
            params = f'{rad.radius}\n{rad.lamp_lm}"'
            if rad.lamp_geom == "cylinder":
                params = f'{rad.radius}\n{rad.length}\n{rad.lamp_lm}"'

        out = subprocess.check_output(
            f"echo {params} | lampcolor", shell=True, encoding="cp437"
        )
        print(f"{params}")
        print(out)
        res = out.split("\n")[-2].split(" ")[-3:]
        color = [float(x) for x in res]
        print(color)
        rad.lamp_color = color
        return {"FINISHED"}
