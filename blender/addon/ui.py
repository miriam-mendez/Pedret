import bpy


class RAD_PT_Scene(bpy.types.Panel):
    """Creates a panel to generate a
    Radaince scene in the 3D viewport
    """

    bl_label = "Radiance Panel"
    bl_idname = "RAD_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Radiance"

    def draw(self, context):
        layout = self.layout

        radiance = context.scene.radiance
        layout.prop(radiance, "file_name")


class RAD_PT_Sky(bpy.types.Panel):
    """Creates a subpanel to generate the
    Radiance gensky in the RAD_PT_PANEL
    """

    bl_label = "Sky"
    bl_idname = "SKY_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Radiance"
    bl_parent_id = "RAD_PT_Panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        radiance = context.scene.radiance
        layout = self.layout

        row = layout.row()
        row.prop(radiance, "sky_type")

        row = layout.row()
        row.prop(radiance, "sky_day")
        row.prop(radiance, "sky_month")

        row = layout.row()
        row.prop(radiance, "is_sky_time_zone")
        row.prop(radiance, "is_sky_year")
        if radiance.is_sky_year:
            row.prop(radiance, "sky_year")

        row = layout.row()
        row.prop(radiance, "sky_time_h")
        row.prop(radiance, "sky_time_min")
        row = layout.row()
        if radiance.is_sky_time_zone:
            row.prop(radiance, "is_sky_DST")
            if radiance.is_sky_DST:
                row.prop(radiance, "sky_DST")
            else:
                row.prop(radiance, "sky_LST")
        else:
            row.prop(radiance, "sky_meridian")
        row = layout.row()
        row.prop(radiance, "sky_latitude")
        row.prop(radiance, "sky_longitude")


class RAD_PT_Render(bpy.types.Panel):
    """Creates a subpanel to render the
    Radiance scene in the RAD_PT_PANEL
    """

    bl_label = "Render"
    bl_idname = "RENDER_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Radiance"
    bl_parent_id = "RAD_PT_Panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        radiance = context.scene.radiance
        layout = self.layout

        row = layout.row()
        row.prop(radiance, "camera", icon="OUTLINER_DATA_CAMERA")
        row = layout.row()
        row.prop(radiance, "amb_file")
        row = layout.row()
        row.prop(radiance, "penumbras")
        row.prop(radiance, "indirect")
        row = layout.row()
        row.prop(radiance, "resolution")

        row = layout.row()
        row.prop(radiance, "quality")
        row = layout.row()
        row.prop(radiance, "detail")
        row = layout.row()
        row.prop(radiance, "variability")
        row = layout.row()
        row.prop(radiance, "is_false_color")
        row.prop(radiance, "exposure")
        row = layout.row()

        row.operator("radiance.export", text="Export")
        row = layout.row()
        row.operator("radiance.preview", text="Preview")
        row.operator("radiance.render", text="Render")


class RAD_PT_Material(bpy.types.Panel):
    """Creates a Panel to specify in pysical units
    a Radaince material in the Material Properties
    """

    bl_idname = "MATERIAL_PT_radiance"
    bl_label = "Radiance material"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        radiance = context.object.active_material.radiance

        row = layout.row()
        row.prop(radiance, "material_type")
        row = layout.row()

        row.prop(radiance, "is_window")
        if radiance.is_window:
            row.prop(radiance, "transmissivity")
            row = layout.row()

        m = radiance.material_type
        if m != "antimatter":
            row.prop(radiance, "is_texture")
            if not radiance.is_texture:
                if not radiance.is_window:
                    row = layout.row()
                row.prop(radiance, "color")
            row = layout.row()

            if m == "illum" or m == "mirror":
                mod = context.object.active_material.modifier
                if len(mod) == 0:
                    row.operator("modifier.add")
                else:
                    row.prop(mod[0], "material")
                    row.operator("modifier.clear", text="", icon="REMOVE")

            elif m == "glow":
                row.prop(radiance, "maxrad")

            elif m == "spotlight":
                row.prop(radiance, "direction")
                row.prop(radiance, "angle")

            elif m == "plastic" or m == "metal" or m == "trans":
                row.prop(radiance, "spec")
                row.prop(radiance, "rough")

                if m == "trans":
                    row = layout.row()
                    row.prop(radiance, "tspec")
                    row.prop(radiance, "trans")

            elif m == "dielectric":
                row.prop(radiance, "n")
                row.prop(radiance, "hc")

        else:
            if m == "antimatter":
                row.operator("modifiers.add")
                mods = context.object.active_material.modifiers
                for i in range(len(mods)):
                    row = layout.row()
                    row.prop(mods[i], "material", text=f"mod {i}")
                    row.operator("modifier.remove", text="", icon="REMOVE").index = i


class RAD_PT_Light(bpy.types.Panel):
    bl_idname = "LIGHT_PT_radiance"
    bl_label = "Radiance light"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    def draw(self, context):
        layout = self.layout
        radiance = context.light.radiance

        row = layout.row()
        row.prop(radiance, "IES_file")
        row = layout.row()
        row.prop(radiance, "deprec_factor")
        row = layout.row()
        row.prop(radiance, "is_lampcolor")
        row.prop(radiance, "lamp_color")
        if radiance.is_lampcolor:
            row = layout.row()
            row.prop(radiance, "lamp_type")
            row = layout.row()
            row.prop(radiance, "lamp_unit")
            row = layout.row()
            row.prop(radiance, "lamp_geom")
            row = layout.row()

            lg = radiance.lamp_geom
            if lg == "polygon":
                row.prop(radiance, "area")
            else:
                row.prop(radiance, "radius")
                if lg == "cylinder":
                    row = layout.row()
                    row.prop(radiance, "length")
            row = layout.row()
            row.prop(radiance, "lamp_lm")
            row.operator("radiance.get_color")
