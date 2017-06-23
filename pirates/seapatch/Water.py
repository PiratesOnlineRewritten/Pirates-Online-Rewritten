from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPRender

class Water(DirectObject):
    notify = directNotify.newCategory('water')
    water_array = []

    def __init__(self, name):
        DirectObject.__init__(self)
        self.water_array.append(self)
        self.name = name
        self.base_texture = None
        self.texture_d = None
        self.texture_n = None
        self.texture_bb = None
        try:
            self.reflect_show_through_only = base.options.reflection == 1
        except:
            self.reflect_show_through_only = base.config.GetBool('want-water-reflection-show-through-only', False)

        self.enable_debug_keys = base.config.GetBool('want-water-debug-keys', False)
        self.enable_parameter_keys = base.config.GetBool('want-water-parameter-ui', False)
        self.enable_water_panel = base.config.GetBool('want-water-panel', False)
        self.use_alpha_map = base.config.GetBool('want-water-alpha', True) and base.win and base.win.getGsg() and base.win.getGsg().getSupportsBasicShaders()
        self.enable_animate_uv = True
        self.enable_ui = True
        self.display_ui = True
        self.first_tick = True
        self.shader = None
        self.shader_file_path = None
        self.reflection = None
        self.reflection_state = False
        self.water_panel = None
        self.use_water_bin = True
        self.enable_alpha_map = True
        self.clamp = True
        self.alpha_clamp = True
        self.texture_filtering = False
        self.water_color_texture = None
        self.water_alpha_texture = None
        self.water_speed = 10.0
        self.water_direction_x = 0.7071
        self.water_direction_y = 0.7071
        self.water_direction = Vec2(self.water_direction_x, self.water_direction_y)
        self.ds_increment = 1.0 / 128.0
        self.p_increment = 0.0005
        self.reflection_increment = 0.005
        self.xyz_increment = 100.0
        self.uv_increment = 0.01
        self.uv_increment2 = 0.005
        self.clear_color = None
        if self.enable_water_panel:
            from pirates.seapatch import WaterPanel
            self.water_panel = WaterPanel.WaterPanel(self.name)
            if self.water_panel == None:
                self.enable_water_panel = False
        self.vector = Vec4(0.0, 0.0, 0.0, 0.0)
        self.map_name = InternalName.make('map')
        self.watercolor_name = InternalName.make('watercolor')
        self.reflectiontexture_name = InternalName.make('reflectiontexture')
        self.reflectionparameters_name = InternalName.make('reflectionparameters')
        self.watercolortexture_name = InternalName.make('watercolortexture')
        self.wateralphatexture_name = InternalName.make('wateralphatexture')
        self.alphamap_name = InternalName.make('alphamap')
        self.watercolorfactor_name = InternalName.make('watercolorfactor')
        self.watercoloradd_name = InternalName.make('watercoloradd')
        self.fogcolor_name = InternalName.make('fogcolor')
        self.fogexpdensity_name = InternalName.make('fogexpdensity')
        self.uvanim_name = InternalName.make('uvanim')
        self.cameraposition_name = InternalName.make('cameraposition')
        self.lightposition_name = InternalName.make('lightposition')
        self.ambientcolor_name = InternalName.make('ambientcolor')
        self.diffusecolor_name = InternalName.make('diffusecolor')
        self.specularcolor_name = InternalName.make('specularcolor')
        self.lightparameters_name = InternalName.make('lightparameters')
        self.update_parameters = True
        self.total = 0.0
        self.total_cycles = 0.0
        self.color_map_texture_stage = None
        self.supports_sky_only = True
        return

    def setup_color_map(self):
        self.color_map_texture_stage = TextureStage('color_map')
        self.color_map_texture_stage.setMode(TextureStage.MReplace)
        self.seamodel.setTexGen(self.color_map_texture_stage, TexGenAttrib.MWorldPosition)
        self.seamodel.setTexture(self.color_map_texture_stage, self.water_color_texture)

    def reflection_enabled(self):
        return base.config.GetBool('want-water-reflection', True)

    def delete_water(self):
        if self.enable_ui and self.enable_parameter_keys:
            self.red_slider.destroy()
            self.green_slider.destroy()
            self.blue_slider.destroy()
            self.alpha_slider.destroy()
            self.reflection_factor_slider.destroy()
            self.purturb_x_slider.destroy()
            self.purturb_y_slider.destroy()
            self.purturb_smoothness_slider.destroy()
            self.water_speed_slider.destroy()
            self.water_direction_x_slider.destroy()
            self.water_direction_y_slider.destroy()
            self.map_x_origin_slider.destroy()
            self.map_y_origin_slider.destroy()
            self.map_x_scale_slider.destroy()
            self.map_y_scale_slider.destroy()
            self.alpha_map_x_origin_slider.destroy()
            self.alpha_map_y_origin_slider.destroy()
            self.alpha_map_x_scale_slider.destroy()
            self.alpha_map_y_scale_slider.destroy()
        if self.reflection:
            self.reflection.delete()
            self.reflection = None
        self.ignoreAll()
        if self in self.water_array:
            self.water_array.remove(self)
        return

    def display_state(self):
        TexturePool.listContents()
        ModelPool.listContents()

    def create_interface(self):
        self.enable_texture_filtering()
        self.set_wrap_or_clamp(not self.clamp)
        self.set_alpha_wrap_or_clamp(not self.alpha_clamp)
        if self.enable_debug_keys:
            self.accept('c', self.set_camera_position)
            self.accept('f', self.toggle_wire_frame)
            self.accept('a', self.add_water_a)
            self.accept('shift-a', self.sub_water_a)
            self.accept(',', self.add_water_r)
            self.accept('shift-,', self.sub_water_r)
            self.accept('.', self.add_water_g)
            self.accept('shift-.', self.sub_water_g)
            self.accept(']', self.add_water_b)
            self.accept('[', self.sub_water_b)
            self.accept('i', self.add_r)
            self.accept('j', self.add_g)
            self.accept('k', self.add_b)
            self.accept('shift-i', self.sub_r)
            self.accept('shift-j', self.sub_g)
            self.accept('shift-k', self.sub_b)
            self.accept('r', self.add_dr)
            self.accept('g', self.add_dg)
            self.accept('b', self.add_db)
            self.accept('shift-r', self.sub_dr)
            self.accept('shift-g', self.sub_dg)
            self.accept('shift-b', self.sub_db)
            self.accept('x', self.add_x)
            self.accept('y', self.add_y)
            self.accept('z', self.add_z)
            self.accept('shift-x', self.sub_x)
            self.accept('shift-y', self.sub_y)
            self.accept('shift-z', self.sub_z)
            self.accept('d', self.add_d)
            self.accept('shift-d', self.sub_d)
            self.accept('s', self.add_s)
            self.accept('shift-s', self.sub_s)
            self.accept('p', self.add_p)
            self.accept('shift-p', self.sub_p)
            self.accept('+', self.add_px)
            self.accept('-', self.sub_px)
            self.accept('*', self.add_py)
            self.accept('/', self.sub_py)
            self.accept('e', self.add_m)
            self.accept('shift-e', self.sub_m)
            self.accept('u', self.add_u)
            self.accept('shift-u', self.sub_u)
            self.accept('v', self.add_v)
            self.accept('shift-v', self.sub_v)
            self.accept('q', self.enable_texture_filtering)
            self.accept('shift-q', self.disable_texture_filtering)
            self.accept('space', self.space)
            self.accept('0', self.setting_0)
            self.accept('1', self.setting_1)
            self.accept('2', self.setting_2)
            self.accept('3', self.setting_3)
            self.accept('4', self.setting_4)
            self.accept('5', self.setting_5)
            self.accept('6', self.setting_6)
            self.accept('7', self.setting_7)
            self.accept('8', self.setting_8)
            self.accept('9', self.toggle_alpha_map)
            self.accept('shift-4', self.toggle_wrap_or_clamp)
            self.accept('shift-9', self.toggle_show_through_only)
            self.accept('shift-0', self.display_state)
        if self.enable_parameter_keys:
            self.accept('shift-1', self.toggle_ui)
            self.accept('shift-2', self.reflection_on)
            self.accept('shift-3', self.reflection_off)

            def display_water_panel():
                from pirates.seapatch import WaterPanel
                self.enable_water_panel = False
                self.water_panel = WaterPanel.WaterPanel(self.name)
                if self.water_panel != None:
                    self.water_panel.setSeaPatch(self)
                    self.enable_water_panel = True
                return

            self.accept('shift-7', display_water_panel)

        def update_slider(slider, update_function):
            string = slider.label + ' %.5f' % slider['value']
            slider['text'] = string
            update_function(slider['value'])

        def create_slider(update_function, default_value, x, y, resolution, label):
            slider = DirectSlider(parent=None, command=update_slider, thumb_relief=DGG.FLAT, pos=(x, 0.0, y), text_align=TextNode.ARight, text_scale=(0.1,
                                                                                                                                                      0.1), text_pos=(0.5,
                                                                                                                                                                      0.1), scale=0.5, pageSize=resolution, text='default', value=default_value)
            slider.label = label
            slider['extraArgs'] = [slider, update_function]
            return slider

        def update_water_r(value):
            self.water_r = value * 255.0
            self.set_water_color_np()

        def update_water_g(value):
            self.water_g = value * 255.0
            self.set_water_color_np()

        def update_water_b(value):
            self.water_b = value * 255.0
            self.set_water_color_np()

        def update_water_a(value):
            self.water_a = value * 255.0
            self.set_water_color_np()

        def update_reflection_factor(value):
            self.reflection_factor = value
            self.set_reflection_parameters_np()

        def update_water_px(value):
            self.px = value
            self.set_reflection_parameters_np()

        def update_water_py(value):
            self.py = value
            self.set_reflection_parameters_np()

        def update_water_ps(value):
            self.ps = value
            self.set_reflection_parameters_np()

        def update_water_speed(value):
            self.water_speed = value * 100.0

        def update_water_direction_x(value):
            self.water_direction_x = value
            self.water_direction = Vec2(self.water_direction_x, self.water_direction_y)

        def update_water_direction_y(value):
            self.water_direction_y = value
            self.water_direction = Vec2(self.water_direction_x, self.water_direction_y)

        def update_map_x_origin(value):
            self.map_x_origin = value
            self.set_map_parameters_np()

        def update_map_y_origin(value):
            self.map_y_origin = value
            self.set_map_parameters_np()

        def update_map_x_scale(value):
            self.map_x_scale = value
            self.set_map_parameters_np()

        def update_map_y_scale(value):
            self.map_y_scale = value
            self.set_map_parameters_np()

        def update_alpha_map_x_origin(value):
            self.alpha_map_x_origin = value
            self.set_alpha_map_parameters_np()

        def update_alpha_map_y_origin(value):
            self.alpha_map_y_origin = value
            self.set_alpha_map_parameters_np()

        def update_alpha_map_x_scale(value):
            self.alpha_map_x_scale = value
            self.set_alpha_map_parameters_np()

        def update_alpha_map_y_scale(value):
            self.alpha_map_y_scale = value
            self.set_alpha_map_parameters_np()

        if self.enable_ui and self.enable_parameter_keys:
            x = -0.8
            y = 0.8
            x_increment = 1.1
            y_increment = -0.15
            resolution = 0.02
            default_value = 0.5
            self.red_slider = create_slider(update_water_r, self.water_r / 255.0, x, y, resolution, 'water red')
            y += y_increment
            self.green_slider = create_slider(update_water_g, self.water_g / 255.0, x, y, resolution, 'water green')
            y += y_increment
            self.blue_slider = create_slider(update_water_b, self.water_b / 255.0, x, y, resolution, 'water blue')
            y += y_increment
            self.alpha_slider = create_slider(update_water_a, self.water_a / 255.0, x, y, resolution, 'water alpha')
            y += y_increment
            self.reflection_factor_slider = create_slider(update_reflection_factor, self.reflection_factor, x, y, resolution, 'reflection_factor')
            y += y_increment
            self.purturb_x_slider = create_slider(update_water_px, self.px, x, y, resolution, 'purturb_x')
            y += y_increment
            self.purturb_y_slider = create_slider(update_water_py, self.py, x, y, resolution, 'purturb_y')
            y += y_increment
            self.purturb_smoothness_slider = create_slider(update_water_ps, self.ps, x, y, resolution, 'purturb_smoothness')
            y += y_increment
            self.water_speed_slider = create_slider(update_water_speed, self.water_speed / 100.0, x, y, resolution, 'water_speed')
            y += y_increment
            self.water_direction_x_slider = create_slider(update_water_direction_x, self.water_direction_x, x, y, resolution, 'water_direction_x')
            self.water_direction_x_slider['range'] = (-1.0, 1.0)
            y += y_increment
            self.water_direction_y_slider = create_slider(update_water_direction_y, self.water_direction_y, x, y, resolution, 'water_direction_y')
            self.water_direction_y_slider['range'] = (-1.0, 1.0)
            y += y_increment
            x += x_increment
            y = 0.8
            map_x_range = 100000.0
            map_y_range = 100000.0
            map_x_scale_range = 10000.0
            map_y_scale_range = 10000.0
            self.map_x_origin_slider = create_slider(update_map_x_origin, self.map_x_origin, x, y, resolution, 'map_x_origin')
            self.map_x_origin_slider['range'] = (-map_x_range, map_x_range)
            y += y_increment
            self.map_y_origin_slider = create_slider(update_map_y_origin, self.map_y_origin, x, y, resolution, 'map_y_origin')
            self.map_y_origin_slider['range'] = (-map_y_range, map_y_range)
            y += y_increment
            self.map_x_scale_slider = create_slider(update_map_x_scale, self.map_x_scale, x, y, resolution, 'map_x_scale')
            self.map_x_scale_slider['range'] = (-map_x_scale_range, map_x_scale_range)
            y += y_increment
            self.map_y_scale_slider = create_slider(update_map_y_scale, self.map_y_scale, x, y, resolution, 'map_y_scale')
            self.map_y_scale_slider['range'] = (-map_y_scale_range, map_y_scale_range)
            y += y_increment
            self.alpha_map_x_origin_slider = create_slider(update_alpha_map_x_origin, self.alpha_map_x_origin, x, y, resolution, 'alpha_map_x_origin')
            self.alpha_map_x_origin_slider['range'] = (-map_x_range, map_x_range)
            y += y_increment
            self.alpha_map_y_origin_slider = create_slider(update_alpha_map_y_origin, self.alpha_map_y_origin, x, y, resolution, 'alpha_map_y_origin')
            self.alpha_map_y_origin_slider['range'] = (-map_y_range, map_y_range)
            y += y_increment
            self.alpha_map_x_scale_slider = create_slider(update_alpha_map_x_scale, self.alpha_map_x_scale, x, y, resolution, 'alpha_map_x_scale')
            self.alpha_map_x_scale_slider['range'] = (-map_x_scale_range, map_x_scale_range)
            y += y_increment
            self.alpha_map_y_scale_slider = create_slider(update_alpha_map_y_scale, self.alpha_map_y_scale, x, y, resolution, 'alpha_map_y_scale')
            self.alpha_map_y_scale_slider['range'] = (-map_y_scale_range, map_y_scale_range)
            y += y_increment
            self.toggle_ui()

    def toggle_show_through_only(self):
        if self.reflection:
            self.reflect_show_through_only = not self.reflect_show_through_only
            self.reflection.reflectShowThroughOnly(self.reflect_show_through_only)

    def update_map_sliders(self):
        if self.enable_ui:
            self.map_x_origin_slider['value'] = self.map_x_origin
            self.map_y_origin_slider['value'] = self.map_y_origin
            self.map_x_scale_slider['value'] = self.map_x_scale
            self.map_y_scale_slider['value'] = self.map_y_scale
            self.alpha_map_x_origin_slider['value'] = self.alpha_map_x_origin
            self.alpha_map_y_origin_slider['value'] = self.alpha_map_y_origin
            self.alpha_map_x_scale_slider['value'] = self.alpha_map_x_scale
            self.alpha_map_y_scale_slider['value'] = self.alpha_map_y_scale

    def toggle_alpha_map(self):
        if self.use_alpha_map:
            self.enable_alpha_map = not self.enable_alpha_map
            self.patchNP.setTransparency(self.enable_alpha_map)

    def update_map_x_origin(self, value):
        self.map_x_origin = value
        self.set_map_parameters_np()

    def update_map_y_origin(self, value):
        self.map_y_origin = value
        self.set_map_parameters_np()

    def update_map_x_scale(self, value):
        self.map_x_scale = value
        self.set_map_parameters_np()

    def update_map_y_scale(self, value):
        self.map_y_scale = value
        self.set_map_parameters_np()

    def update_alpha_map_x_origin(self, value):
        self.alpha_map_x_origin = value
        self.set_map_parameters_np()

    def update_alpha_map_y_origin(self, value):
        self.alpha_map_y_origin = value
        self.set_map_parameters_np()

    def update_alpha_map_x_scale(self, value):
        self.alpha_map_x_scale = value
        self.set_map_parameters_np()

    def update_alpha_map_y_scale(self, value):
        self.alpha_map_y_scale = value
        self.set_map_parameters_np()

    def update_water_direction_and_speed(self, x, y, speed):
        self.water_speed = speed
        self.water_direction_x = x
        self.water_direction_y = y
        self.water_direction = Vec2(self.water_direction_x, self.water_direction_y)

    def set_shader(self, input_file_path, unload_previous_shader=False):
        file_path = Filename.fromOsSpecific(input_file_path)
        file_name = file_path.getBasename()
        directory = file_path.getDirname()
        if self.shader != None and unload_previous_shader:
            self.unload_shader()
        self.shader_file_path = file_path.getFullpath()
        shader = loader.loadShader(self.shader_file_path)
        self.shader = shader
        self.seamodel.setShader(shader)
        shader = None
        return

    def unload_shader(self):
        loader.unloadShader(self.shader_file_path)
        self.shader_file_path = None
        return

    def set_water_color_texture(self, input_file_path, unload_previous_texture=False, texture=None):
        if texture:
            water_color_texture = texture
        else:
            file_path = Filename.fromOsSpecific(input_file_path)
            file_name = file_path.getBasename()
            directory = file_path.getDirname()
            if True:
                water_color_texture = loader.loadTexture(file_path.getFullpath())
            else:
                water_color_texture = loader.loadTexture(file_path)
            if water_color_texture == None:
                pass
        if water_color_texture != None:
            if unload_previous_texture:
                self.unload_water_color_texture()
            self.water_color_texture = water_color_texture
            self.seamodel.setShaderInput(self.watercolortexture_name, self.water_color_texture)
        else:
            self.water_color_texture = None
        self.set_wrap_or_clamp(self.clamp)
        self.set_water_color_texture_filtering()
        water_color_texture = None
        return

    def unload_water_color_texture(self):
        if self.water_color_texture != None:
            loader.unloadTexture(self.water_color_texture)
            self.water_color_texture = None
        return

    def set_water_alpha_texture(self, input_file_path, unload_previous_texture=False, texture=None):
        if texture:
            water_alpha_texture = texture
        else:
            file_path = Filename.fromOsSpecific(input_file_path)
            file_name = file_path.getBasename()
            directory = file_path.getDirname()
            if True:
                water_alpha_texture = loader.loadTexture(file_path.getFullpath())
            else:
                water_alpha_texture = loader.loadTexture(file_path)
            if water_alpha_texture == None:
                pass
        if water_alpha_texture != None:
            if unload_previous_texture:
                self.unload_water_alpha_texture()
            self.water_alpha_texture = water_alpha_texture
            self.seamodel.setShaderInput(self.wateralphatexture_name, self.water_alpha_texture)
        else:
            self.water_alpha_texture = None
        self.set_alpha_wrap_or_clamp(self.alpha_clamp)
        self.set_water_alpha_texture_filtering()
        water_alpha_texture = None
        return

    def unload_water_alpha_texture(self):
        if self.water_alpha_texture:
            loader.unloadTexture(self.water_alpha_texture)
            self.water_alpha_texture = None
        return

    def set_wrap_or_clamp(self, wrap):
        if self.water_color_texture:
            if wrap:
                self.water_color_texture.setWrapU(Texture.WMRepeat)
                self.water_color_texture.setWrapV(Texture.WMRepeat)
            else:
                self.water_color_texture.setWrapU(Texture.WMClamp)
                self.water_color_texture.setWrapV(Texture.WMClamp)
        self.clamp = wrap

    def toggle_wrap_or_clamp(self):
        self.set_wrap_or_clamp(not self.clamp)

    def set_alpha_wrap_or_clamp(self, wrap):
        if self.water_alpha_texture:
            if wrap:
                self.water_alpha_texture.setWrapU(Texture.WMRepeat)
                self.water_alpha_texture.setWrapV(Texture.WMRepeat)
            else:
                self.water_alpha_texture.setWrapU(Texture.WMClamp)
                self.water_alpha_texture.setWrapV(Texture.WMClamp)
        self.alpha_clamp = wrap

    def toggle_alpha_wrap_or_clamp(self):
        self.set_alpha_wrap_or_clamp(not self.alpha_clamp)

    def set_reflection(self, enable):
        if self.reflection:
            self.reflection.enable(enable)

    def reflection_on(self):
        if self.reflection:
            self.reflection.enable(True)
        self.reflection_state = True

    def reflection_off(self):
        if self.reflection:
            self.reflection.enable(False)
        self.reflection_state = False

    def update_reflection(self):
        if self.reflection:
            self.reflection.enable(self.reflection_state)

    def toggle_reflection(self):
        if self.reflection_state:
            self.reflection_off()
        else:
            self.reflection_on()

    def toggle_ui(self):
        if self.enable_ui:
            if self.display_ui:
                self.display_ui = False
            else:
                self.display_ui = True
            if self.display_ui:
                self.red_slider.show()
                self.green_slider.show()
                self.blue_slider.show()
                self.alpha_slider.show()
                self.reflection_factor_slider.show()
                self.purturb_x_slider.show()
                self.purturb_y_slider.show()
                self.purturb_smoothness_slider.show()
                self.water_speed_sliderp.show()
                self.water_direction_x_slider.show()
                self.water_direction_y_slider.show()
                self.map_x_origin_slider.show()
                self.map_y_origin_slider.show()
                self.map_x_scale_slider.show()
                self.map_y_scale_slider.show()
                self.alpha_map_x_origin_slider.show()
                self.alpha_map_y_origin_slider.show()
                self.alpha_map_x_scale_slider.show()
                self.alpha_map_y_scale_slider.show()
            else:
                self.red_slider.hide()
                self.green_slider.hide()
                self.blue_slider.hide()
                self.alpha_slider.hide()
                self.reflection_factor_slider.hide()
                self.purturb_x_slider.hide()
                self.purturb_y_slider.hide()
                self.purturb_smoothness_slider.hide()
                self.water_speed_slider.hide()
                self.water_direction_x_slider.hide()
                self.water_direction_y_slider.hide()
                self.map_x_origin_slider.hide()
                self.map_y_origin_slider.hide()
                self.map_x_scale_slider.hide()
                self.map_y_scale_slider.hide()
                self.alpha_map_x_origin_slider.hide()
                self.alpha_map_y_origin_slider.hide()
                self.alpha_map_x_scale_slider.hide()
                self.alpha_map_y_scale_slider.hide()

    def enable_texture_filtering(self):
        if self.texture_d:
            self.texture_d.setMinfilter(Texture.FTLinearMipmapLinear)
            self.texture_d.setAnisotropicDegree(2)
        if self.texture_n:
            self.texture_n.setMinfilter(Texture.FTLinearMipmapLinear)
            self.texture_n.setAnisotropicDegree(2)
        if self.texture_bb:
            self.texture_bb.setMinfilter(Texture.FTLinearMipmapLinear)
            self.texture_bb.setAnisotropicDegree(2)
        self.texture_filtering = True
        self.set_water_color_texture_filtering()

    def disable_texture_filtering(self):
        if self.texture_d:
            self.texture_d.setMinfilter(Texture.FTLinear)
            self.texture_d.setAnisotropicDegree(1)
        if self.texture_n:
            self.texture_n.setMinfilter(Texture.FTLinear)
            self.texture_n.setAnisotropicDegree(1)
        if self.texture_bb:
            self.texture_bb.setMinfilter(Texture.FTLinear)
            self.texture_bb.setAnisotropicDegree(1)
        self.texture_filtering = False
        self.set_water_color_texture_filtering()

    def set_water_color_texture_filtering(self):
        if self.water_color_texture:
            if self.texture_filtering:
                self.water_color_texture.setMinfilter(Texture.FTLinearMipmapLinear)
                self.water_color_texture.setAnisotropicDegree(2)
            else:
                self.water_color_texture.setMinfilter(Texture.FTLinear)
                self.water_color_texture.setAnisotropicDegree(1)

    def set_water_alpha_texture_filtering(self):
        if self.water_alpha_texture:
            if self.texture_filtering:
                self.water_alpha_texture.setMinfilter(Texture.FTLinear)
                self.water_alpha_texture.setAnisotropicDegree(1)
            else:
                self.water_alpha_texture.setMinfilter(Texture.FTLinear)
                self.water_alpha_texture.setAnisotropicDegree(1)

    def set_map_parameters_np(self):
        if self.shader:
            self.vector.set(self.map_x_origin, self.map_y_origin, 1.0 / self.map_x_scale, 1.0 / self.map_y_scale)
            self.seamodel.setShaderInput(self.map_name, self.vector)
        elif self.color_map_texture_stage:
            self.seamodel.setTexOffset(self.color_map_texture_stage, float(self.map_x_origin), float(self.map_y_origin))
            self.seamodel.setTexScale(self.color_map_texture_stage, 1.0 / self.map_x_scale, 1.0 / self.map_y_scale)

    def set_alpha_map_parameters_np(self):
        self.vector.set(self.alpha_map_x_origin, self.alpha_map_y_origin, 1.0 / self.alpha_map_x_scale, 1.0 / self.alpha_map_y_scale)
        self.seamodel.setShaderInput(self.alphamap_name, self.vector)

    def set_water_color_factor_np(self):
        self.vector.set(self.water_color_factor_r, self.water_color_factor_g, self.water_color_factor_b, 1.0)
        self.seamodel.setShaderInput(self.watercolorfactor_name, self.vector)

    def modify_water_color_factor_np(self, color=Vec3(0, 0, 0)):
        self.water_color_factor_r = color[0]
        self.water_color_factor_g = color[1]
        self.water_color_factor_b = color[2]
        self.set_water_color_factor_np()

    def set_water_color_add_np(self):
        self.vector.set(self.water_color_add_r, self.water_color_add_g, self.water_color_add_b, 1.0)
        self.seamodel.setShaderInput(self.watercoloradd_name, self.vector)

    def modify_water_color_add_np(self, color=Vec3(0, 0, 0)):
        self.water_color_add_r = color[0]
        self.water_color_add_g = color[1]
        self.water_color_add_b = color[2]
        self.set_water_color_add_np()

    def set_fog_np(self):
        self.vector.set(self.fog_r, self.fog_g, self.fog_b, self.fog_a)
        self.seamodel.setShaderInput(self.fogcolor_name, self.vector)

    def set_fog_exp_density_np(self):
        self.vector.set(self.fog_exp_density, 0.0, 0.0, 0.0)
        self.seamodel.setShaderInput(self.fogexpdensity_name, self.vector)

    def set_uvanim(self):
        self.vector.set(self.u, self.v, self.u2, self.v2)
        self.seamodel.setShaderInput(self.uvanim_name, self.vector)

    def print_camera(self):
        print 'camera_position', base.cam.getPos(render)

    def set_camera_position_2(self):
        self.vector.set(self.camera_x, self.camera_y, self.camera_z, 1.0)
        self.seamodel.setShaderInput(self.cameraposition_name, self.vector)

    def set_camera_position(self):
        self.camera_position = base.cam.getPos(render)
        self.vector.set(self.camera_position[0], self.camera_position[1], self.camera_position[2], 1.0)
        self.seamodel.setShaderInput(self.cameraposition_name, self.vector)
        self.print_camera()

    def toggle_wire_frame(self):
        base.toggleWireframe()

    def print_ambient_color(self):
        print 'ambient red', self.ar, 'ambient green', self.ag, 'ambient blue', self.ab

    def set_ambient_color_np(self):
        self.vector.set(self.ar / 255.0, self.ag / 255.0, self.ab / 255.0, 1.0)
        self.seamodel.setShaderInput(self.ambientcolor_name, self.vector)

    def set_ambient_color(self):
        self.set_ambient_color_np()
        self.print_ambient_color()

    def print_diffuse_color(self):
        print 'diffuse red', self.dr, 'diffuse green', self.dg, 'diffuse blue', self.db

    def set_diffuse_color_np(self):
        self.vector.set(self.dr / 255.0, self.dg / 255.0, self.db / 255.0, 1.0)
        self.seamodel.setShaderInput(self.diffusecolor_name, self.vector)

    def set_diffuse_color(self):
        self.set_diffuse_color_np()
        self.print_diffuse_color()

    def print_specular_color(self):
        print 'red', self.r, 'green', self.g, 'blue', self.b

    def set_specular_color_np(self):
        self.vector.set(self.r / 255.0, self.g / 255.0, self.b / 255.0, 1.0)
        self.seamodel.setShaderInput(self.specularcolor_name, self.vector)

    def set_specular_color(self):
        self.set_specular_color_np()
        self.print_specular_color()

    def print_light_parameters(self):
        print 'diffuse_factor', self.d, 'specular_factor', self.s, 'specular_power', self.p

    def set_light_parameters_np(self):
        self.vector.set(self.d, self.s, self.p, 1.0)
        self.seamodel.setShaderInput(self.lightparameters_name, self.vector)

    def set_light_parameters(self):
        self.set_light_parameters_np()
        self.print_light_parameters()

    def print_reflection_parameters(self):
        print 'purturb x', self.px, 'purturb y', self.py, 'reflection_factor', self.reflection_factor

    def print_water_color_map_parameters(self):
        print 'map x', self.map_x_origin, 'map y', self.map_y_origin, 'map size', self.map_x_scale, 'map size', self.map_y_scale

    def set_reflection_parameters_np(self):
        self.vector.set(self.px, self.py, self.reflection_factor, self.ps)
        self.seamodel.setShaderInput(self.reflectionparameters_name, self.vector)
        if self.reflection and self.reflection.reflection_card_node_path:
            reflection_factor = self.reflection_factor
            self.reflection.reflection_card_node_path.setColor(reflection_factor, reflection_factor, reflection_factor)

    def set_reflection_parameters(self):
        self.set_reflection_parameters_np()
        self.print_reflection_parameters()

    def print_water_color(self):
        print 'water color: red', self.water_r, 'green', self.water_g, 'blue', self.water_b, 'alpha', self.water_a

    def set_water_color_np(self):
        self.vector.set(self.water_r / 255.0, self.water_g / 255.0, self.water_b / 255.0, self.water_a / 255.0)
        self.seamodel.setShaderInput(self.watercolor_name, self.vector)

    def set_water_color(self):
        self.set_water_color_np()

    def add_water_r(self):
        self.water_r = self.water_r + 1.0
        if self.water_r > 255:
            self.water_r = 255.0
        self.set_water_color()

    def sub_water_r(self):
        self.water_r = self.water_r - 1.0
        if self.water_r < 0.0:
            self.water_r = 0.0
        self.set_water_color()

    def add_water_g(self):
        self.water_g = self.water_g + 1.0
        if self.water_g > 255:
            self.water_g = 255.0
        self.set_water_color()

    def sub_water_g(self):
        self.water_g = self.water_g - 1.0
        if self.water_g < 0.0:
            self.water_g = 0.0
        self.set_water_color()

    def add_water_b(self):
        self.water_b = self.water_b + 1.0
        if self.water_b > 255:
            self.water_b = 255.0
        self.set_water_color()

    def sub_water_b(self):
        self.water_b = self.water_b - 1.0
        if self.water_b < 0.0:
            self.water_b = 0.0
        self.set_water_color()

    def add_water_a(self):
        self.water_a = self.water_a + 1.0
        if self.water_a > 255:
            self.water_a = 255.0
        self.set_water_color()

    def sub_water_a(self):
        self.water_a = self.water_a - 1.0
        if self.water_a < 0.0:
            self.water_a = 0.0
        self.set_water_color()

    def add_dr(self):
        self.dr = self.dr + 1.0
        if self.dr > 255.0:
            self.dr = 255.0
        self.set_diffuse_color()

    def add_dg(self):
        self.dg = self.dg + 1.0
        if self.dg > 255.0:
            self.dg = 255.0
        self.set_diffuse_color()

    def add_db(self):
        self.db = self.db + 1.0
        if self.db > 255:
            self.db = 255.0
        self.set_diffuse_color()

    def sub_dr(self):
        self.dr = self.dr - 1.0
        if self.dr < 0.0:
            self.dr = 0.0
        self.set_diffuse_color()

    def sub_dg(self):
        self.dg = self.dg - 1.0
        if self.dg < 0.0:
            self.dg = 0.0
        self.set_diffuse_color()

    def sub_db(self):
        self.db = self.db - 1.0
        if self.db < 0.0:
            self.db = 0.0
        self.set_diffuse_color()

    def add_r(self):
        self.r = self.r + 1.0
        if self.r > 255.0:
            self.r = 255.0
        self.set_specular_color()

    def add_g(self):
        self.g = self.g + 1.0
        if self.g > 255.0:
            self.g = 255.0
        self.set_specular_color()

    def add_b(self):
        self.b = self.b + 1.0
        if self.b > 255:
            self.b = 255.0
        self.set_specular_color()

    def sub_r(self):
        self.r = self.r - 1.0
        if self.r < 0.0:
            self.r = 0.0
        self.set_specular_color()

    def sub_g(self):
        self.g = self.g - 1.0
        if self.g < 0.0:
            self.g = 0.0
        self.set_specular_color()

    def sub_b(self):
        self.b = self.b - 1.0
        if self.b < 0.0:
            self.b = 0.0
        self.set_specular_color()

    def print_light_position(self):
        print 'x', self.x, 'y', self.y, 'z', self.z

    def set_light_position_np(self):
        self.vector.set(self.x, self.y, self.z, 1.0)
        self.seamodel.setShaderInput(self.lightposition_name, self.vector)

    def set_light_position(self):
        self.set_light_position_np()
        self.print_light_position()

    def add_x(self):
        self.x = self.x + self.xyz_increment
        self.set_light_position()

    def add_y(self):
        self.y = self.y + self.xyz_increment
        self.set_light_position()

    def add_z(self):
        self.z = self.z + self.xyz_increment
        self.set_light_position()

    def sub_x(self):
        self.x = self.x - self.xyz_increment
        self.set_light_position()

    def sub_y(self):
        self.y = self.y - self.xyz_increment
        self.set_light_position()

    def sub_z(self):
        self.z = self.z - self.xyz_increment
        self.set_light_position()

    def add_d(self):
        self.d = self.d + self.ds_increment
        self.set_light_parameters()

    def sub_d(self):
        self.d = self.d - self.ds_increment
        if self.d < 0.0:
            self.d = 0.0
        self.set_light_parameters()

    def add_s(self):
        self.s = self.s + self.ds_increment
        self.set_light_parameters()

    def sub_s(self):
        self.s = self.s - self.ds_increment
        if self.s < 0.0:
            self.s = 0.0
        self.set_light_parameters()

    def add_p(self):
        self.p = self.p + 1.0
        self.set_light_parameters()

    def sub_p(self):
        self.p = self.p - 1.0
        if self.p < 1.0:
            self.p = 1.0
        self.set_light_parameters()

    def add_px(self):
        self.px = self.px + self.p_increment
        self.set_reflection_parameters()

    def sub_px(self):
        self.px = self.px - self.p_increment
        if self.px < 0.0:
            self.px = 0.0
        self.set_reflection_parameters()

    def add_py(self):
        self.py = self.py + self.p_increment
        self.set_reflection_parameters()

    def sub_py(self):
        self.py = self.py - self.p_increment
        if self.py < 0.0:
            self.py = 0.0
        self.set_reflection_parameters()

    def add_m(self):
        self.reflection_factor = self.reflection_factor + self.reflection_increment
        self.set_reflection_parameters()

    def sub_m(self):
        self.reflection_factor = self.reflection_factor - self.reflection_increment
        if self.reflection_factor < 0.0:
            self.reflection_factor = 0.0
        self.set_reflection_parameters()

    def add_u(self):
        self.u += self.uv_increment
        self.u2 += self.uv_increment2
        if self.u > 1.0:
            self.u -= 1.0
        if self.u2 > 1.0:
            self.u2 -= 1.0
        self.set_uvanim()

    def add_v(self):
        self.v += self.uv_increment
        self.v2 += self.uv_increment2
        if self.v > 1.0:
            self.v -= 1.0
        if self.v2 > 1.0:
            self.v2 -= 1.0
        self.set_uvanim()

    def sub_u(self):
        self.u -= self.uv_increment
        self.u2 -= self.uv_increment2
        if self.u < 0.0:
            self.u += 1.0
        if self.u2 < 0.0:
            self.u2 += 1.0
        self.set_uvanim()

    def sub_v(self):
        self.v -= self.uv_increment
        self.v2 -= self.uv_increment2
        if self.v < 0.0:
            self.v += 1.0
        if self.v2 < 0.0:
            self.v2 += 1.0
        self.set_uvanim()

    def space(self):
        self.print_camera()
        self.print_light_position()
        self.print_light_parameters()
        self.print_ambient_color()
        self.print_diffuse_color()
        self.print_specular_color()
        self.print_water_color()
        self.print_reflection_parameters()
        self.print_water_color_map_parameters()

    def setting_0(self):
        self.ds_increment = 1.0 / 128.0
        self.xyz_increment = 100.0
        self.uv_increment = 0.01
        self.ar = 64.0
        self.ag = 64.0
        self.ab = 64.0
        self.set_ambient_color_np()
        self.dr = 255.0
        self.dg = 255.0
        self.db = 255.0
        self.set_diffuse_color_np()
        self.r = 255.0
        self.g = 255.0
        self.b = 255.0
        self.set_specular_color_np()
        self.x = 0.0
        self.y = 0.0
        self.z = 1000.0
        self.set_light_position_np()
        self.d = 1.0
        self.s = 0.5
        self.p = 20.0
        self.set_light_parameters_np()
        self.px = 0.08
        self.py = 0.0
        self.ps = 1.0
        self.reflection_factor = 0.2
        self.set_reflection_parameters_np()
        if True:
            self.water_r = 17
            self.water_g = 55
            self.water_b = 70
            self.water_a = 255
            self.set_water_color_np()
        else:
            self.water_r = 128
            self.water_g = 255
            self.water_b = 143
            self.water_a = 255
            self.set_water_color_np()
        self.u = 0.0
        self.v = 0.0
        self.u2 = 0.0
        self.v2 = 0.0
        self.set_uvanim()
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.camera_z = 100.0
        self.set_camera_position_2()
        self.fog_r = 0.5
        self.fog_g = 0.5
        self.fog_b = 0.5
        self.fog_a = 1.0
        self.set_fog_np()
        self.fog_exp_density = 1.0 / 7500.0
        self.set_fog_exp_density_np()
        self.map_x_origin = -1400.0
        self.map_y_origin = -1400.0
        self.map_x_scale = 2680.0
        self.map_y_scale = 2680.0
        self.set_map_parameters_np()
        self.alpha_map_x_origin = -1100.0 + 5.0
        self.alpha_map_y_origin = -800.0 + 80.0
        self.alpha_map_x_scale = 1370.0
        self.alpha_map_y_scale = 1370.0
        self.set_alpha_map_parameters_np()
        self.water_color_factor_r = 1.0
        self.water_color_factor_g = 1.0
        self.water_color_factor_b = 1.0
        self.set_water_color_factor_np()
        self.water_color_add_r = 0.0
        self.water_color_add_g = 0.0
        self.water_color_add_b = 0.0
        self.set_water_color_add_np()

    def setting_1(self):
        self.d = 0.35
        self.s = 0.1
        self.p = 20.0
        self.set_light_parameters()
        self.x = 0.0
        self.y = -200.0
        self.z = -1000.0
        self.set_light_position()

    def setting_2(self):
        self.d = 0.5
        self.s = 0.35
        self.p = 20.0
        self.set_light_parameters()
        self.x = 0.0
        self.y = 2500.0
        self.z = -1500.0
        self.set_light_position()

    def setting_3(self):
        self.d = 0.5
        self.s = 0.35
        self.p = 20.0
        self.set_light_parameters()
        self.x = 0.0
        self.y = -1000.0
        self.z = 1500.0
        self.set_light_position()

    def setting_4(self):
        self.d = 1.0
        self.s = 0.35
        self.p = 20.0
        self.set_light_parameters()
        self.x = 0.0
        self.y = 0.0
        self.z = 1500.0
        self.set_light_position()

    def setting_5(self):
        self.d = 1.0
        self.s = 1.0
        self.p = 1.0
        self.set_light_parameters()
        self.x = 0.0
        self.y = -4100.0
        self.z = 13600.0
        self.set_light_position()

    def setting_6(self):
        self.water_r = 77
        self.water_g = 128
        self.water_b = 179
        self.water_a = 255
        self.set_water_color()

    def setting_7(self):
        self.d = 1.0
        self.s = 2.5
        self.p = 80.0
        self.set_light_parameters()
        self.x = 0.0
        self.y = 40000.0
        self.z = 15000.0
        self.set_light_position()
        self.r = 209.0
        self.g = 142.0
        self.b = 58.0
        self.water_a = 255.0
        self.set_specular_color()

    def setting_8(self):
        self.px = 0.035
        self.py = 0.035
        self.reflection_factor = 0.2
        self.set_reflection_parameters()

    def update_water(self, time):
        if self.shader:
            self.set_camera_position_2()
            if self.first_tick:
                elapsed_time = 0.0
                self.first_tick = False
            else:
                elapsed_time = time - self.current_time
            self.current_time = time
            distance = elapsed_time * self.water_speed
            self.update_reflection()
            if self.enable_animate_uv:
                self.u += self.water_direction[0] * distance * self.uv_increment
                self.v += self.water_direction[1] * distance * self.uv_increment
                self.u2 += self.water_direction[0] * distance * self.uv_increment2
                self.v2 += self.water_direction[1] * distance * self.uv_increment2
                if self.u > 1.0:
                    self.u -= 1.0
                if self.u2 > 1.0:
                    self.u2 -= 1.0
                if self.v > 1.0:
                    self.v -= 1.0
                if self.v2 > 1.0:
                    self.v2 -= 1.0
                if self.u < 0.0:
                    self.u += 1.0
                if self.u2 < 0.0:
                    self.u2 += 1.0
                if self.v < 0.0:
                    self.v += 1.0
                if self.v2 < 0.0:
                    self.v2 += 1.0
                self.set_uvanim()
            if self.reflection:
                if self.reflection_state:
                    if self.clear_color:
                        self.reflection.setClearColor(self.clear_color)
                    else:
                        self.reflection.setClearColor(base.backgroundDrawable.getClearColor())
                else:
                    self.reflection.setClearColor(self.reflection.black_clear_color)
            if self.reflection:
                self.reflection.update_reflection(base.camLens, base.cam, self.supports_sky_only)
            if self.update_parameters:
                self.set_fog_np()
                self.set_fog_exp_density_np()
                self.set_ambient_color_np()
                self.set_diffuse_color_np()
                self.set_specular_color_np()
                self.set_light_position_np()
                self.set_light_parameters_np()
                self.set_water_color_factor_np()
                self.set_water_color_add_np()
                if self.reflection_enabled():
                    if self.reflection:
                        self.seamodel.setShaderInput(self.reflectiontexture_name, self.reflection.reflection_texture)
                elif self.reflection:
                    self.seamodel.setShaderInput(self.reflectiontexture_name, self.reflection.black_reflection_texture)
        elif self.reflection:
            if self.reflection_state:
                if self.clear_color:
                    self.reflection.setClearColor(self.clear_color)
                else:
                    self.reflection.setClearColor(base.backgroundDrawable.getClearColor())
            else:
                self.reflection.setClearColor(self.reflection.black_clear_color)
            if self.reflection_enabled():
                self.reflection.update_reflection(base.camLens, base.cam)
            self.reflection.update_reflectuion_no_shader()

    @classmethod
    def all_reflections_off(self):
        index = 0
        total_water_objects = len(Water.water_array)
        while index < total_water_objects:
            water = Water.water_array[index]
            water.reflection_off()
            index += 1

    @classmethod
    def all_reflections_show_through_only(self):
        index = 0
        total_water_objects = len(Water.water_array)
        while index < total_water_objects:
            water = Water.water_array[index]
            water.reflection_on()
            if water.reflection:
                if water.supports_sky_only:
                    water.reflection.reflectShowThroughOnly(True)
                else:
                    water.reflection.reflectShowThroughOnly(False)
            index += 1

    @classmethod
    def all_reflections_on(self):
        index = 0
        total_water_objects = len(Water.water_array)
        while index < total_water_objects:
            water = Water.water_array[index]
            water.reflection_on()
            if water.reflection:
                water.reflection.reflectShowThroughOnly(False)
            index += 1


class IslandWaterParameters():
    debug = False
    default_water_alpha_file_path = 'maps/default_inv_alpha.jpg'
    default_water_color_file_path = 'maps/ocean_color_default.jpg'

    def __init__(self):
        self.map_x_origin = 0.0
        self.map_y_origin = 0.0
        self.map_x_scale = 1000.0
        self.map_y_scale = 1000.0
        self.alpha_map_x_origin = 0.0
        self.alpha_map_y_origin = 0.0
        self.alpha_map_x_scale = 1000.0
        self.alpha_map_y_scale = 1000.0
        self.water_color_file_path = self.default_water_color_file_path
        self.water_alpha_file_path = self.default_water_alpha_file_path
        self.water_color_texture = None
        self.water_alpha_texture = None
        self.unload_previous_texture = False
        self.swamp_water = None
        return

    def setIslandWaterParameters(self, water, use_alpha_map):
        if water:
            water.map_x_origin = self.map_x_origin
            water.map_y_origin = self.map_y_origin
            water.map_x_scale = self.map_x_scale
            water.map_y_scale = self.map_y_scale
            water.set_map_parameters_np()
            water.alpha_map_x_origin = self.alpha_map_x_origin
            water.alpha_map_y_origin = self.alpha_map_y_origin
            water.alpha_map_x_scale = self.alpha_map_x_scale
            water.alpha_map_y_scale = self.alpha_map_y_scale
            water.set_alpha_map_parameters_np()
            if use_alpha_map:
                water.set_water_color_texture(self.water_color_file_path, self.unload_previous_texture, self.water_color_texture)
                water.set_water_alpha_texture(self.water_alpha_file_path, self.unload_previous_texture, self.water_alpha_texture)
                if self.debug:
                    print 'WATER ALPHA ON'
            else:
                water.set_water_color_texture(self.default_water_color_file_path, self.unload_previous_texture, None)
                water.set_water_alpha_texture(self.default_water_alpha_file_path, self.unload_previous_texture, None)
                if self.debug:
                    print 'WATER ALPHA OFF'
        if self.swamp_water:
            self.swamp_water.map_x_origin = self.swamp_map_x_origin
            self.swamp_water.map_y_origin = self.swamp_map_y_origin
            self.swamp_water.map_x_scale = self.swamp_map_x_scale
            self.swamp_water.map_y_scale = self.swamp_map_y_scale
            self.swamp_water.set_map_parameters_np()
            self.swamp_water.alpha_map_x_origin = self.swamp_map_x_origin
            self.swamp_water.alpha_map_y_origin = self.swamp_map_y_origin
            self.swamp_water.alpha_map_x_scale = self.swamp_map_x_scale
            self.swamp_water.alpha_map_y_scale = self.swamp_map_y_scale
            self.swamp_water.set_alpha_map_parameters_np()
            self.swamp_water.water_r = self.swamp_color_r
            self.swamp_water.water_g = self.swamp_color_g
            self.swamp_water.water_b = self.swamp_color_b
            self.swamp_water.set_water_color_np()
            self.swamp_water.update_water_direction_and_speed(self.swamp_direction_x, self.swamp_direction_y, self.swamp_speed)
        return