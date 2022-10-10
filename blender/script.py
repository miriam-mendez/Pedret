import bpy
import os
from mathutils import Vector


class Scene:
    """Holds the radiance scene definitions"""

    def __init__(self, filename):
        self.filename = filename
        self.content = ""

    def save(self):
        f = open(self.filename, "w")
        f.write(self.content)
        f.close()

    # Material defintions
    def addMaterialLight(self, id, r, g, b):
        self.content += f"void light {id} \n0 \n0 \n3 {r} {g} {b}\n"
        self.content += "\n"

    def addMaterialGlass(self, id, r, g, b):
        self.content += f"void glass {id} \n0 \n0 \n3 {r} {g} {b}\n"
        self.content += "\n"

    def addMaterialPlastic(self, id, r, g, b, specular=0.0, roughness=0.0):
        self.content += f"void plastic {id} \n0 \n0 \n5 {r} {g} {b} \
            {specular} {roughness}\n"
        self.content += "\n"

    def addMaterialColorTexture(self, id, textureHdr, specular=0, roughness=0):
        self.content += f"void colorpict {id + '_map'} \n7 red green blue \
            {textureHdr} . frac(Lu)  frac(Lv) \n0 \n0"
        self.content += "\n"
        self.content += f"{id + '_map'} plastic {id} \n0 \n0 \n5 1 1 1 \
            {specular} {roughness}\n"
        self.content += "\n"

    # Geometry definitions
    def addMeshRtm(self, id, mat, file_rtm, xform=""):
        s = f"{mat} mesh {id} \n1 {file_rtm} \n0 \n0 \n"
        s += "\n"
        f = open("tmp.rad", "w")
        f.write(s)
        f.close()

        if xform:
            command = f"xform {xform} tmp.rad > tmp.rad"
            os.system(command)
        f = open("tmp.rad")
        self.content += f.read()
        f.close()

        command = f"rm tmp.rad"
        os.system(command)

    def addSky(self, latitude, longitude, day, month, hour, year=""):
        self.content += f"!gensky {month} {day} {hour} -a {latitude} -o \
            {longitude}"
        self.content += f" -y {year}\n\n" if year != "" else "\n\n"

        self.content += f"skyfunc glow sky_glow \n0 \n0 \n4 .9 .9 1.15 0\n"
        self.content += f"sky_glow source sky \n0 \n0 \n4 0 0 1 180\n"
        self.content += f"skyfunc glow ground_glow \n0 \n0 \n4 1.4 .9 .6 0\n"
        self.content += f"ground_glow source ground \n0 \n0 \n4 0 0 -1 180\n"


def blend2mesh(materials, *argv):
    """Converts the blender scene meshes to radiance meshes"""
    bpy.ops.object.select_all(action="DESELECT")
    for arg in argv:
        ob = bpy.data.objects[arg]
        if ob.type == "MESH":
            ob.select_set(True)
            bpy.ops.export_scene.obj(
                filepath=f"{ob.name}.obj",
                use_selection=True,
                axis_forward="Y",
                axis_up="Z",
            )

            command = f"obj2mesh -a {materials} {ob.name}.obj {ob.name}.rtm"
            os.system(command)
            ob.select_set(False)
        else:
            raise Exception(f"{ob} is not a Blender mesh")


def objview(*argv):
    """Runs Radiance objview  program"""
    command = f"objview"
    for arg in argv:
        command += f" {arg}"
    os.system(command)


def cam2view(camera):
    """Converts the Blender camera to Radiance view file"""
    ob = bpy.data.objects[camera]
    if ob.type == "CAMERA":
        lx, ly, lz = ob.location
        ux, uy, uz = ob.rotation_euler.to_matrix() @ Vector((0.0, 1.0, 0.0))
        dx, dy, dz = ob.rotation_euler.to_matrix() @ Vector((0.0, 0.0, -1.0))
        v = f"rvu -vtv -vp {lx} {ly} {lz} -vd {dx} {dy} {dz} -vu {ux} {uy} {uz}"

        f = open(f"{camera}.vf", "w")
        f.write(v)
        f.close()
        return f"{camera}.vf"
    else:
        raise Exception(f"{camera} is not a Blender camera")


def rad_interact(view, *argv):
    """Runs Radiance rvu program"""
    command = f"oconv {' '.join(argv)} > scene.oct"
    os.system(command)
    command = f"rvu -vf {view} -ab 4 scene.oct"
    os.system(command)


def rad_image(view, *argv):
    """Runs Radiance rpict program"""
    command = f"oconv {' '.join(argv)} > scene.oct"
    os.system(command)
    command = f"rpict -vf {view} -ab 4 scene.oct > output.hdr"
    os.system(command)


def main():
    m = Scene("materials.mat")
    m.addMaterialColorTexture("grass", "Pedret_IX_grass.hdr")
    m.addMaterialColorTexture("wood", "Pedret_IX_wood.hdr", 0.07, 0.15)
    m.addMaterialColorTexture("sedimentary", "Pedret_IX_sedimentary.hdr", 0, 0.2)
    m.addMaterialGlass("window", 0.96, 0.96, 0.96)
    m.save()

    blend2mesh(m.filename, "pedret2", "windows")

    s = Scene("geometry.rad")
    s.addMeshRtm("pedret1", "void", "pedret2.rtm")
    s.addMeshRtm("gwindow", "void", "windows.rtm")
    s.addSky(42.10745931228419, 1.8836540623509863, 1, 8, "16:00CEST", 1990)
    s.save()
    # objview(s.filename)

    view = cam2view("Door")
    rad_interact(view, s.filename)


main()
