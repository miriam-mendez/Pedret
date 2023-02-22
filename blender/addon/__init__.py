
bl_info={
    "name":"Radiance Addon",
    "author":"Míriam Méndez",
    "description":"Radiance rendering",
    "version":(0,0,0),
    "location":"View3D && Properties > Material && Properties > Light",
    "category":"Generic",
    "support":"COMMUNITY",
    "blender":(3,0,1)
}

PYTHON_PATH = "/home/miriam/Documentos/FBX/addon"

import bpy, sys, os
sys.path.append(PYTHON_PATH)

#if __name__ == "radiance":
#    from . import ui
#    from . import settings
#    from . import operators
#else:
from ui import *
from settings import *
from operators import *

RADIANCE_BIN_FOLDER = "/usr/local/bin"
RADIANCE_LIB_FOLDER = "/usr/local/lib/radiance"


classes = [SceneSettingsRadiance, MaterialSettingsRadiance, ModifiersSettingsRadiance, LightSettingsRadiance, MOD_OT_Remove, MOD_OT_Add, MOD_OT_Clear, LIGHT_OT_Color, RAD_OT_Preview, RAD_OT_Export, RAD_OT_Render, RAD_PT_Scene, RAD_PT_Sky, RAD_PT_Render, RAD_PT_Material, RAD_PT_Light]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.radiance = PointerProperty(type=SceneSettingsRadiance)
    bpy.types.Material.radiance = PointerProperty(type=MaterialSettingsRadiance)
    bpy.types.Material.modifier = CollectionProperty(type=ModifiersSettingsRadiance)
    bpy.types.Light.radiance = PointerProperty(type=LightSettingsRadiance)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.radiance
    del bpy.types.Material.radiance
    del bpy.types.Material.modifier
    del bpy.types.Light.radiance

    
if __name__ == "__main__":
    register()