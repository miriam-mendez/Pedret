import bpy
from bpy.props import *
from bpy.types import PropertyGroup


class SceneSettingsRadiance(PropertyGroup):
    file_name: StringProperty(
        name="File name", default="scene", description="Output file name"
    )
    sky_type: EnumProperty(
        name="Sky type",
        items=[
            ("+s", "sunny sky", ""),
            ("-c", "cloudy sky", ""),
            ("+i", "intermediate sky", ""),
            ("-u", "uniform cloudy sky", ""),
        ],
        default="+s",
        description="CIE standard sky distribution",
    )
    sky_day: IntProperty(
        name="dd",
        soft_min=1,
        soft_max=31,
        default=1,
        description="CIE standard sky distribution day",
    )
    sky_month: IntProperty(
        name="mm",
        soft_min=1,
        soft_max=12,
        default=1,
        description="CIE standard sky distribution month",
    )
    is_sky_year: BoolProperty(
        name="year",
        default=True,
        description="Indicates if the year is specified; if so, a more accurate solar position algorithm will be used",
    )
    sky_year: IntProperty(
        name="yyyy",
        soft_min=1950,
        soft_max=2050,
        default=1950,
        description="Year to compute an accurate solar position",
    )
    sky_time_h: IntProperty(
        name="HH",
        soft_min=0,
        soft_max=23,
        default=0,
        subtype="TIME",
        description="CIE standard sky distribution hour",
    )
    sky_time_min: IntProperty(
        name="MM",
        soft_min=0,
        soft_max=59,
        default=0,
        subtype="TIME_ABSOLUTE",
        description="CIE standard sky distribution minute",
    )
    is_sky_time_zone: BoolProperty(
        name="time zone",
        default=True,
        description="Indicates whether the time should be interpreted by the meridian or the time zone",
    )
    is_sky_DST: BoolProperty(
        name="Summer time",
        default=False,
        description="Indicates  whether the time zone is a local standard time or a daylight saving time",
    )
    sky_LST: EnumProperty(
        name="LST",
        items=[
            ("YST", "YST ( 9)", ""),
            ("PST", "PST ( 8)", ""),
            ("MST", "MST ( 7)", ""),
            ("CST", "CST ( 6)", ""),
            ("EST", "EST ( 5)", ""),
            ("GMT", "GMT ( 0)", ""),
            ("CET", "CEST (-1)", ""),
            ("EET", "EEST (-2)", ""),
            ("AST", "AST (-3)", ""),
            ("GST", "GST (-4)", ""),
            ("IST", "IST (-5.5)", ""),
            ("JST", "JST (-9)", ""),
            ("NZST", "NZST (-12)", ""),
        ],
        default="CET",
        description="CIE standard sky distribution local standard time zone",
    )
    sky_DST: EnumProperty(
        name="DST",
        items=[
            ("YDT", "YDT ( 8)", ""),
            ("PDT", "PDT ( 7)", ""),
            ("MDT", "MDT ( 6)", ""),
            ("CDT", "CDT ( 5)", ""),
            ("EDT", "EDT ( 4)", ""),
            ("BST", "BST (-1)", ""),
            ("CEST", "CEST (-2)", ""),
            ("EEST", "EEST (-3)", ""),
            ("ADT", "ADT (-4)", ""),
            ("GDT", "GDT (-5)", ""),
            ("IDT", "IDT (-6.5)", ""),
            ("JDT", "JDT (-10)", ""),
            ("NZDT", "NZDT (-13)", ""),
        ],
        default="CEST",
        description="CIE standard sky distribution daylight saving time zone",
    )
    sky_meridian: FloatProperty(
        name="Meridian",
        soft_min=-180,
        soft_max=180,
        precision=4,
        default=0,
        description="CIE standard sky distribution meridian",
    )
    sky_latitude: FloatProperty(
        name="Latitude",
        soft_min=-90,
        soft_max=90,
        precision=4,
        default=0.0,
        description=" CIE standard sky distribution latitude",
    )
    sky_longitude: FloatProperty(
        name="Longitude",
        soft_min=-180,
        soft_max=180,
        precision=4,
        default=0.0,
        description="CIE standard sky distribution longitude",
    )
    camera: PointerProperty(
        name="Camera", type=bpy.types.Camera, description="Camera used to render"
    )
    exposure: FloatProperty(
        name="Exposure",
        soft_min=0,
        default=1,
        description="Exposure used for rendering",
    )
    resolution: IntVectorProperty(
        name="Resolution",
        soft_min=1,
        soft_max=1024,
        size=2,
        default=(512, 512),
        subtype="XYZ",
        description="(X,Y) resolution, in pixels",
    )
    quality: EnumProperty(
        name="Quality",
        items=[("H", "High", ""), ("M", "Medium", ""), ("L", "Low", "")],
        default="L",
        description="The overall rendering quality",
    )
    detail: EnumProperty(
        name="Detail",
        items=[("H", "High", ""), ("M", "Medium", ""), ("L", "Low", "")],
        default="L",
        description="The overall level of visual  detail",
    )
    variability: EnumProperty(
        name="Variability",
        items=[("H", "High", ""), ("M", "Medium", ""), ("L", "Low", "")],
        default="L",
        description=" Indicates how much light varies over  the  surfaces",
    )
    penumbras: BoolProperty(
        name="Penumbras",
        default=False,
        description="Indicates if penumbras are desired or not",
    )
    indirect: IntProperty(
        name="Indirect light",
        soft_min=0,
        soft_max=8,
        default=0,
        description="Indicates the number of ambient bounces",
    )
    amb_file: StringProperty(
        name="Ambient file",
        subtype="FILE_PATH",
        description="Ambient file that acts as a cache",
    )
    is_false_color: BoolProperty(
        name="False color",
        default=False,
        description="Indicates wether the image is rendered in false color or not",
    )


class ModifiersSettingsRadiance(PropertyGroup):
    material: EnumProperty(
        name="Material Modifier",
        items=[
            (
                "light",
                "Light",
                "The basic material for self-luminous surfaces (i.e., light sources).",
            ),
            (
                "illum",
                "Illum",
                "Used for secondary light sources with broad distributions. A secondary light source is treated like any other light source, except when viewed directly. It then acts like it is made of a different material, or becomes invisible. Secondary sources are useful when modeling windows or brightly illuminated surfaces.",
            ),
            (
                "glow",
                "Glow",
                "Glow is used for surfaces that are self-luminous, but limited in their effect.",
            ),
            (
                "spotlight",
                "Spotlight",
                "Spotlight is used for self-luminous surfaces having directed output.",
            ),
            (
                "mirror",
                "Mirror",
                "Mirror is used for planar surfaces that produce secondary source reflections.",
            ),
            ("plastic", "Plastic", "Plastic is a material with uncolored highlights."),
            (
                "metal",
                "Metal",
                "Metal is similar to plastic, but specular highlights are modified by the material color.",
            ),
            (
                "trans",
                "Trans",
                "Trans is a translucent material, whose reflection characteristics are similar to plastic. Light is also transmitted both diffusely and specularly. Transmitted and diffusely reflected light is modified by the material color.",
            ),
            (
                "dielectric",
                "Dielectric",
                "A dielectric material is transparent, and it refracts light as well as reflecting it. Its behavior is determined by the index of refraction and transmission coefficient in each wavelength band per unit length.",
            ),
            (
                "glass",
                "Glass",
                "Glass is similar to dielectric, but it is optimized for thin glass surfaces (n = 1.52). One transmitted ray and one reflected ray is produced.",
            ),
        ],
        default="glass",
    )


class MaterialSettingsRadiance(PropertyGroup):
    def my_material_color(self, context):
        ob = context.object
        if ob is not None:
            surf = (
                ob.active_material.node_tree.nodes.get("Material Output")
                .inputs["Surface"]
                .links[0]
                .from_node
            )
            if not surf.inputs["Base Color"].is_linked:
                surf.inputs[
                    "Base Color"
                ].default_value = ob.active_material.radiance.color

    material_type: EnumProperty(
        name="Material Type",
        items=[
            (
                "light",
                "Light",
                "The basic material for self-luminous surfaces (i.e., light sources).",
            ),
            (
                "illum",
                "Illum",
                "Used for secondary light sources with broad distributions. A secondary light source is treated like any other light source, except when viewed directly. It then acts like it is made of a different material, or becomes invisible. Secondary sources are useful when modeling windows or brightly illuminated surfaces.",
            ),
            (
                "glow",
                "Glow",
                "Glow is used for surfaces that are self-luminous, but limited in their effect.",
            ),
            (
                "spotlight",
                "Spotlight",
                "Spotlight is used for self-luminous surfaces having directed output.",
            ),
            (
                "mirror",
                "Mirror",
                "Mirror is used for planar surfaces that produce secondary source reflections.",
            ),
            ("plastic", "Plastic", "Plastic is a material with uncolored highlights."),
            (
                "metal",
                "Metal",
                "Metal is similar to plastic, but specular highlights are modified by the material color.",
            ),
            (
                "trans",
                "Trans",
                "Trans is a translucent material, whose reflection characteristics are similar to plastic. Light is also transmitted both diffusely and specularly. Transmitted and diffusely reflected light is modified by the material color.",
            ),
            (
                "dielectric",
                "Dielectric",
                "A dielectric material is transparent, and it refracts light as well as reflecting it. Its behavior is determined by the index of refraction and transmission coefficient in each wavelength band per unit length.",
            ),
            (
                "interface",
                "Interface",
                "An interface is a boundary between two dielectrics.",
            ),
            (
                "glass",
                "Glass",
                "Glass is similar to dielectric, but it is optimized for thin glass surfaces (n = 1.52). One transmitted ray and one reflected ray is produced.",
            ),
            (
                "antimatter",
                "Antimatter",
                "Antimatter is a material that can subtract volumes from other volumes.",
            ),
        ],
        default="glass",
    )
    is_texture: BoolProperty(name="Texture", default=False)
    color: FloatVectorProperty(  # It is sync with BaseColor
        name="Color",
        soft_min=0,
        soft_max=1,
        size=4,
        default=(1, 1, 1, 1),
        subtype="COLOR",
        update=my_material_color,
    )
    spec: FloatProperty(name="Specularity", soft_min=0, soft_max=1, default=0)
    rough: FloatProperty(name="Roughness", soft_min=0, soft_max=1, default=0)
    trans: FloatProperty(name="Translucent", soft_min=0, soft_max=1, default=0)
    tspec: FloatProperty(name="Transmitted specular", soft_min=0, soft_max=1, default=0)
    maxrad: FloatProperty(name="maxrad", soft_min=-1, default=-1)
    direction: IntVectorProperty(name="direction", subtype="XYZ", default=(0, 0, 0))
    angle: FloatProperty(name="angle", soft_min=0, soft_max=360, default=0)
    n: FloatProperty(name="index of refraction", soft_min=0, default=1.5)
    hc: FloatProperty(
        name="transmission coefficient", soft_min=0, soft_max=1, default=0.92
    )
    is_window: BoolProperty(name="window", default=False)
    transmissivity: FloatVectorProperty(
        name="transmissivity",
        soft_min=0,
        soft_max=1,
        size=3,
        default=(1, 1, 1),
        subtype="COLOR_GAMMA",
        description="The window transmissivity",
    )


class LightSettingsRadiance(PropertyGroup):
    # update id is render in cycles and there is a node IES File
    def my_light(self, context):
        if context.scene.render.engine == "CYCLES":
            light = context.object.data
            lnodes = light.node_tree
            if lnodes is not None:
                if lnodes.nodes.find("IES Texture") != -1:
                    lnodes.nodes["IES Texture"].filepath = light.radiance.IES_file
                else:
                    l1 = light.node_tree.nodes.new("ShaderNodeOutputLight")
                    l2 = light.node_tree.nodes.new("ShaderNodeEmission")
                    light.node_tree.links.new(
                        l1.inputs["Surface"], l2.outputs["Emission"]
                    )
                    l3 = light.node_tree.nodes.new("ShaderNodeTexIES")
                    light.node_tree.links.new(l2.inputs["Strength"], l3.outputs["Fac"])
                    light.node_tree.nodes[
                        "IES Texture"
                    ].filepath = light.radiance.IES_file
            else:
                light.use_nodes = True
                l1 = light.node_tree.nodes.new("ShaderNodeOutputLight")
                l2 = light.node_tree.nodes.new("ShaderNodeEmission")
                light.node_tree.links.new(l1.inputs["Surface"], l2.outputs["Emission"])
                l3 = light.node_tree.nodes.new("ShaderNodeTexIES")
                light.node_tree.links.new(l2.inputs["Strength"], l3.outputs["Fac"])
                light.node_tree.nodes["IES Texture"].filepath = light.radiance.IES_file

    def my_light_color(self, context):
        if context.scene.render.engine == "CYCLES":
            light = context.object.data
            lnodes = light.node_tree
            if lnodes is not None:
                if lnodes.nodes.find("IES Texture") != -1:
                    lnodes.nodes["IES Texture"].color = light.radiance.lamp_color

    is_lampcolor: BoolProperty(
        name="lampcolor",
        default=False,
        description="Indicates whether the light should be an IES file or defined with lampcolor",
    )
    IES_file: StringProperty(
        name="IES file",
        subtype="FILE_PATH",
        update=my_light,
        description="The IES path file",
    )
    deprec_factor: FloatProperty(
        name="depreciation factor",
        soft_min=0,
        soft_max=1,
        default=0,
        description="Indicates the lamp depreciation factor",
    )
    lamp_color: FloatVectorProperty(
        name="color",
        soft_min=0,
        soft_max=1,
        size=3,
        default=(1, 1, 1),
        subtype="COLOR_GAMMA",
        update=my_light_color,
        description="The IES lamp color",
    )
    lamp_type: EnumProperty(
        name="lamp type",
        items=[
            ("warm white deluxe", "warm white deluxe", ".440 .403 .85"),
            ("cool white deluxe", "cool white deluxe", ""),
            ("warm white", "warm white", ".436 .406 .85"),
            ("cool white", "cool white", ".373 .385 .85"),
            ("white fluor", "white fluor", ".41 .398 .85"),
            ("daylight fluor", "daylight fluor", ".316 .345 .85"),
            ("clear mercury", "clear mercury", ".326 .39 .8"),
            ("phosphor mercury", "phosphor mercury", ".373 .415 .8"),
            ("clear metal halide", "clear metal halide", ".396 .390 .8"),
            ("xenon", "xenon", ".324 .324 1"),
            ("high pressure sodium", "high pressure sodium", ".519 .418 .9"),
            ("low pressure sodium", "low pressure sodium", ".569 .421 .93"),
            ("halogen", "halogen", ".424 .399 1"),
            ("incandescent", "incandescent", ".453 .405 .95"),
            ("D65WHITE", "D65WHITE", ".313 .329 1"),
            ("WHITE", "WHITE", ".3333 .3333 1"),
        ],
        description="The lamp type  corresponds to one of the types registered in the lamp table file of Radiance.  A value of WHITE means an uncolored source, which may be preferable because it results in a color balanced image.",
    )
    lamp_unit: EnumProperty(
        name="length unit",
        items=[
            ("meter", "meter", ""),
            ("centimeter", "centimeter", ""),
            ("foot", "foot", ""),
            ("inch", "inch", ""),
        ],
        default="meter",
        description="The length unit",
    )
    lamp_geom: EnumProperty(
        name="lamp geometry",
        items=[
            ("polygon", "polygon", ""),
            ("sphere", "sphere", ""),
            ("cylinder", "cylinder", ""),
            ("ring", "ring", ""),
        ],
        default="polygon",
        description="The lamp geometry",
    )
    area: FloatProperty(
        name="area", soft_min=0, default=0, description="The polygon area"
    )
    radius: FloatProperty(
        name="radius",
        soft_min=0,
        default=0,
        description="The radius of the geometry specified",
    )
    length: FloatProperty(
        name="length", soft_min=0, default=0, description="The cylinder length"
    )
    lamp_lm: FloatProperty(
        name="lamp lumens", soft_min=0, default=0, description="The output lamp lumens"
    )
