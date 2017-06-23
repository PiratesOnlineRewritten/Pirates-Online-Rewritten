from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.tkwidgets.AppShell import *
from direct.tkwidgets import Slider
from tkFileDialog import askopenfilename
import math
import string
import Pmw
from Tkinter import *

class WaterPanel(AppShell):
    appversion = '1.0'
    frameWidth = 500
    frameHeight = 550

    def __init__(self, name, **kw):
        self.name = name
        DGG.INITOPT = Pmw.INITOPT
        optiondefs = (
         (
          'title', name + ' Panel', None),)
        self.defineoptions(kw, optiondefs)
        AppShell.__init__(self)
        self.initialiseoptions(WaterPanel)
        self.region_version = 3
        self.texture_filename = None
        self.alpha_texture_filename = None
        self.region_texture_filename = None
        self.region_alpha_texture_filename = None
        self.shader_filename = None
        self.seapatch = None
        self.enable_region_update = True
        return

    def appInit(self):
        self.widgetDict = {}
        self.variableDict = {}

    def toggle_reflection(self):
        if self.seapatch != None:
            self.seapatch.toggle_reflection()
        return

    def toggle_clamp(self):
        if self.seapatch != None:
            self.seapatch.toggle_wrap_or_clamp()
        return

    def toggle_alpha_clamp(self):
        if self.seapatch != None:
            self.seapatch.toggle_alpha_wrap_or_clamp()
        return

    def toggle_alpha_map(self):
        if self.seapatch != None:
            self.seapatch.toggle_alpha_map()
        return

    def toggle_realtime_controls(self):
        if self.seapatch != None:
            self.seapatch.toggle_ui()
        return

    def get_region_x_offset(self):
        self.region_x_offset = self.region_thousands_x_offset + self.region_hundreds_x_offset + self.region_ones_x_offset
        return self.region_x_offset

    def get_region_y_offset(self):
        self.region_y_offset = self.region_thousands_y_offset + self.region_hundreds_y_offset + self.region_ones_y_offset
        return self.region_y_offset

    def get_region_x_size(self):
        self.region_x_size = self.region_hundreds_x_size + self.region_ones_x_size
        return self.region_x_size

    def get_region_y_size(self):
        self.region_y_size = self.region_hundreds_y_size + self.region_ones_y_size
        return self.region_y_size

    def get_region_alpha_x_offset(self):
        self.region_alpha_x_offset = self.region_alpha_thousands_x_offset + self.region_alpha_hundreds_x_offset + self.region_alpha_ones_x_offset
        return self.region_alpha_x_offset

    def get_region_alpha_y_offset(self):
        self.region_alpha_y_offset = self.region_alpha_thousands_y_offset + self.region_alpha_hundreds_y_offset + self.region_alpha_ones_y_offset
        return self.region_alpha_y_offset

    def get_region_alpha_x_size(self):
        self.region_alpha_x_size = self.region_alpha_hundreds_x_size + self.region_alpha_ones_x_size
        return self.region_alpha_x_size

    def get_region_alpha_y_size(self):
        self.region_alpha_y_size = self.region_alpha_hundreds_y_size + self.region_alpha_ones_y_size
        return self.region_alpha_y_size

    def write_integer(self, output_file, value):
        output_file.write(value.__repr__())
        output_file.write('\n')

    def write_float(self, output_file, value):
        output_file.write(value.__repr__())
        output_file.write('\n')

    def write_string(self, output_file, string):
        output_file.write(string)
        output_file.write('\n')

    def save_region(self, output_file):
        if self.region_texture_filename != None and self.region_alpha_texture_filename != None:
            self.write_integer(output_file, self.region_version)
            self.write_string(output_file, self.region_texture_filename)
            self.write_string(output_file, self.region_alpha_texture_filename)
            self.write_float(output_file, self.region_thousands_x_offset)
            self.write_float(output_file, self.region_hundreds_x_offset)
            self.write_float(output_file, self.region_ones_x_offset)
            self.write_float(output_file, self.region_thousands_y_offset)
            self.write_float(output_file, self.region_hundreds_y_offset)
            self.write_float(output_file, self.region_ones_y_offset)
            self.write_float(output_file, self.region_hundreds_x_size)
            self.write_float(output_file, self.region_ones_x_size)
            self.write_float(output_file, self.region_hundreds_y_size)
            self.write_float(output_file, self.region_ones_y_size)
            self.write_float(output_file, self.region_alpha_thousands_x_offset)
            self.write_float(output_file, self.region_alpha_hundreds_x_offset)
            self.write_float(output_file, self.region_alpha_ones_x_offset)
            self.write_float(output_file, self.region_alpha_thousands_y_offset)
            self.write_float(output_file, self.region_alpha_hundreds_y_offset)
            self.write_float(output_file, self.region_alpha_ones_y_offset)
            self.write_float(output_file, self.region_alpha_hundreds_x_size)
            self.write_float(output_file, self.region_alpha_ones_x_size)
            self.write_float(output_file, self.region_alpha_hundreds_y_size)
            self.write_float(output_file, self.region_alpha_ones_y_size)
            output_file.close()
        return

    def read_integer(self, input_file):
        s = string.strip(input_file.readline())
        print s
        return string.atoi(s)

    def read_float(self, input_file):
        s = string.strip(input_file.readline())
        print s
        return string.atof(s)

    def read_string(self, input_file):
        return string.strip(input_file.readline())

    def load_region(self, filename):
        state = False
        input_file = open(filename, 'r')
        if input_file != None:
            region_version = self.read_integer(input_file)
            if region_version == self.region_version:
                self.region_texture_filename = self.read_string(input_file)
                self.set_message_bar_text(self.region_texture_message_bar, self.region_texture_filename)
                print self.region_texture_filename
                self.region_alpha_texture_filename = self.read_string(input_file)
                self.set_message_bar_text(self.region_alpha_texture_message_bar, self.region_alpha_texture_filename)
                print self.region_alpha_texture_filename
                self.region_thousands_x_offset = self.read_float(input_file)
                self.region_hundreds_x_offset = self.read_float(input_file)
                self.region_ones_x_offset = self.read_float(input_file)
                self.region_thousands_y_offset = self.read_float(input_file)
                self.region_hundreds_y_offset = self.read_float(input_file)
                self.region_ones_y_offset = self.read_float(input_file)
                self.region_hundreds_x_size = self.read_float(input_file)
                self.region_ones_x_size = self.read_float(input_file)
                self.region_hundreds_y_size = self.read_float(input_file)
                self.region_ones_y_size = self.read_float(input_file)
                self.region_alpha_thousands_x_offset = self.read_float(input_file)
                self.region_alpha_hundreds_x_offset = self.read_float(input_file)
                self.region_alpha_ones_x_offset = self.read_float(input_file)
                self.region_alpha_thousands_y_offset = self.read_float(input_file)
                self.region_alpha_hundreds_y_offset = self.read_float(input_file)
                self.region_alpha_ones_y_offset = self.read_float(input_file)
                self.region_alpha_hundreds_x_size = self.read_float(input_file)
                self.region_alpha_ones_x_size = self.read_float(input_file)
                self.region_alpha_hundreds_y_size = self.read_float(input_file)
                self.region_alpha_ones_y_size = self.read_float(input_file)
                category = self.region_text + '0'
                self.getWidget(category, self.region_thousands_x_offset_text).set(self.region_thousands_x_offset, 0)
                self.getWidget(category, self.region_hundreds_x_offset_text).set(self.region_hundreds_x_offset, 0)
                self.getWidget(category, self.region_ones_x_offset_text).set(self.region_ones_x_offset, 0)
                self.getWidget(category, self.region_thousands_y_offset_text).set(self.region_thousands_y_offset, 0)
                self.getWidget(category, self.region_hundreds_y_offset_text).set(self.region_hundreds_y_offset, 0)
                self.getWidget(category, self.region_ones_y_offset_text).set(self.region_ones_y_offset, 0)
                self.getWidget(category, self.region_hundreds_x_size_text).set(self.region_hundreds_x_size, 0)
                self.getWidget(category, self.region_ones_x_size_text).set(self.region_ones_x_size, 0)
                self.getWidget(category, self.region_hundreds_y_size_text).set(self.region_hundreds_y_size, 0)
                self.getWidget(category, self.region_ones_y_size_text).set(self.region_ones_y_size, 0)
                category = self.alpha_region_text + '1'
                self.getWidget(category, self.region_alpha_thousands_x_offset_text).set(self.region_alpha_thousands_x_offset, 0)
                self.getWidget(category, self.region_alpha_hundreds_x_offset_text).set(self.region_alpha_hundreds_x_offset, 0)
                self.getWidget(category, self.region_alpha_ones_x_offset_text).set(self.region_alpha_ones_x_offset, 0)
                self.getWidget(category, self.region_alpha_thousands_y_offset_text).set(self.region_alpha_thousands_y_offset, 0)
                self.getWidget(category, self.region_alpha_hundreds_y_offset_text).set(self.region_alpha_hundreds_y_offset, 0)
                self.getWidget(category, self.region_alpha_ones_y_offset_text).set(self.region_alpha_ones_y_offset, 0)
                self.getWidget(category, self.region_alpha_hundreds_x_size_text).set(self.region_alpha_hundreds_x_size, 0)
                self.getWidget(category, self.region_alpha_ones_x_size_text).set(self.region_alpha_ones_x_size, 0)
                self.getWidget(category, self.region_alpha_hundreds_y_size_text).set(self.region_alpha_hundreds_y_size, 0)
                self.getWidget(category, self.region_alpha_ones_y_size_text).set(self.region_alpha_ones_y_size, 0)
                self.set_message_bar_text(self.region_file_path_message_bar, filename)
                state = True
            else:
                print 'ERROR: incorrect version number'
            input_file.close()
        return state

    def createInterface(self):
        interior = self.interior()
        mainFrame = Frame(interior)
        mainFrame.pack()
        fileMenu = self.menuBar.component('File-menu')
        fileMenu.insert_command(fileMenu.index('Quit'), label='Load and Apply Parameters', command=self.load_and_apply_water_parameters)
        fileMenu.insert_command(fileMenu.index('Quit'), label='Save Parameters', command=self.save_water_parameters)
        fileMenu.insert_command(fileMenu.index('Quit'), label='Load Parameters', command=self.load_water_parameters)
        self.menuBar.addmenu('Texture', 'Texture-menu')
        texture_menu = self.menuBar.component('Texture-menu')
        texture_menu.insert_command(0, label='Select Texture', command=self.select_texture)
        texture_menu.insert_command(0, label='Update Texture', command=self.update_texture)
        self.menuBar.addmenu('Alpha-Texture', 'Alpha-Texture-menu')
        alpha_texture_menu = self.menuBar.component('Alpha-Texture-menu')
        alpha_texture_menu.insert_command(0, label='Select Alpha Texture', command=self.select_alpha_texture)
        alpha_texture_menu.insert_command(0, label='Update Alpha Texture', command=self.update_alpha_texture)
        self.menuBar.addmenu('Shader', 'Shader-menu')
        shader_menu = self.menuBar.component('Shader-menu')
        shader_menu.insert_command(0, label='Select Shader', command=self.select_shader)
        shader_menu.insert_command(0, label='Update Shader', command=self.update_shader)
        self.mainNotebook = Pmw.NoteBook(interior)
        self.mainNotebook.pack(fill=BOTH, expand=1)
        minimum_offset = -50000.0
        maximum_offset = 50000.0
        offset_resolution = 1.0 / (maximum_offset - minimum_offset)
        hundreds_minimum_offset = -5000.0
        hundreds_maximum_offset = 5000.0
        hundreds_offset_resolution = 1.0
        ones_minimum_offset = -100.0
        ones_maximum_offset = 100.0
        ones_offset_resolution = 1.0
        default_offset = 0.0
        hundreds_minimum_size = 1000.0
        hundreds_maximum_size = 11000.0
        hundreds_size_resolution = 1.0
        ones_minimum_size = 0.0
        ones_maximum_size = 100.0
        ones_size_resolution = 1.0
        default_hundreds_size = 1000.0
        default_size = 0.0
        self.region_text = 'Region'
        self.region_thousands_x_offset_text = 'Map X Offset (thousands)'
        self.region_hundreds_x_offset_text = 'Map X Offset (hundreds)'
        self.region_ones_x_offset_text = 'Map X Offset (0 - 100)'
        self.region_thousands_y_offset_text = 'Map Y Offset (thousands)'
        self.region_hundreds_y_offset_text = 'Map Y Offset (hundreds)'
        self.region_ones_y_offset_text = 'Map Y Offset (0 - 100)'
        self.region_hundreds_x_size_text = 'Map X Size (hundreds)'
        self.region_ones_x_size_text = 'Map X Size (0 - 100)'
        self.region_hundreds_y_size_text = 'Map Y Size (hundreds)'
        self.region_ones_y_size_text = 'Map Y Size (0 - 100)'
        texture_slider_definitions = (
         (
          self.region_text, self.region_thousands_x_offset_text, 'x-axis offset in world coordinates', self.set_x_offset, minimum_offset, maximum_offset, offset_resolution, default_offset), (self.region_text, self.region_hundreds_x_offset_text, 'x-axis offset in world coordinates', self.set_hundreds_x_offset, hundreds_minimum_offset, hundreds_maximum_offset, hundreds_offset_resolution, default_offset), (self.region_text, self.region_ones_x_offset_text, 'x-axis offset in world coordinates', self.set_ones_x_offset, ones_minimum_offset, ones_maximum_offset, ones_offset_resolution, default_offset), (self.region_text, self.region_thousands_y_offset_text, 'y-axis offset in world coordinates', self.set_y_offset, minimum_offset, maximum_offset, offset_resolution, default_offset), (self.region_text, self.region_hundreds_y_offset_text, 'y-axis offset in world coordinates', self.set_hundreds_y_offset, hundreds_minimum_offset, hundreds_maximum_offset, hundreds_offset_resolution, default_offset), (self.region_text, self.region_ones_y_offset_text, 'y-axis offset in world coordinates', self.set_ones_y_offset, ones_minimum_offset, ones_maximum_offset, ones_offset_resolution, default_offset), (self.region_text, self.region_hundreds_x_size_text, 'x-axis size in world coordinates', self.set_hundreds_x_size, hundreds_minimum_size, hundreds_maximum_size, hundreds_size_resolution, default_hundreds_size), (self.region_text, self.region_ones_x_size_text, 'x-axis size in world coordinates', self.set_ones_x_size, ones_minimum_size, ones_maximum_size, ones_size_resolution, default_size), (self.region_text, self.region_hundreds_y_size_text, 'y-axis size in world coordinates', self.set_hundreds_y_size, hundreds_minimum_size, hundreds_maximum_size, hundreds_size_resolution, default_hundreds_size), (self.region_text, self.region_ones_y_size_text, 'y-axis size in world coordinates', self.set_ones_y_size, ones_minimum_size, ones_maximum_size, ones_size_resolution, default_size))
        self.region_thousands_x_offset = default_offset
        self.region_hundreds_x_offset = default_offset
        self.region_ones_x_offset = default_offset
        self.region_thousands_y_offset = default_offset
        self.region_hundreds_y_offset = default_offset
        self.region_ones_y_offset = default_offset
        self.region_hundreds_x_size = default_hundreds_size
        self.region_ones_x_size = default_size
        self.region_hundreds_y_size = default_hundreds_size
        self.region_ones_y_size = default_size
        self.alpha_region_text = 'Region'
        self.region_alpha_thousands_x_offset_text = 'Alpha Map X Offset (thousands)'
        self.region_alpha_hundreds_x_offset_text = 'Alpha Map X Offset (hundreds)'
        self.region_alpha_ones_x_offset_text = 'Alpha Map X Offset (0 - 100)'
        self.region_alpha_thousands_y_offset_text = 'Alpha Map Y Offset (thousands)'
        self.region_alpha_hundreds_y_offset_text = 'Alpha Map Y Offset (hundreds)'
        self.region_alpha_ones_y_offset_text = 'Alpha Map Y Offset (0 - 100)'
        self.region_alpha_hundreds_x_size_text = 'Alpha Map X Size (hundreds)'
        self.region_alpha_ones_x_size_text = 'Alpha Map X Size (0 - 100)'
        self.region_alpha_hundreds_y_size_text = 'Alpha Map Y Size (hundreds)'
        self.region_alpha_ones_y_size_text = 'Alpha Map Y Size (0 - 100)'
        alpha_texture_slider_definitions = (
         (
          self.alpha_region_text, self.region_alpha_thousands_x_offset_text, 'x-axis offset in world coordinates', self.set_alpha_x_offset, minimum_offset, maximum_offset, offset_resolution, default_offset), (self.alpha_region_text, self.region_alpha_hundreds_x_offset_text, 'x-axis offset in world coordinates', self.set_alpha_hundreds_x_offset, hundreds_minimum_offset, hundreds_maximum_offset, hundreds_offset_resolution, default_offset), (self.alpha_region_text, self.region_alpha_ones_x_offset_text, 'x-axis offset in world coordinates', self.set_alpha_ones_x_offset, ones_minimum_offset, ones_maximum_offset, ones_offset_resolution, default_offset), (self.alpha_region_text, self.region_alpha_thousands_y_offset_text, 'y-axis offset in world coordinates', self.set_alpha_y_offset, minimum_offset, maximum_offset, offset_resolution, default_offset), (self.alpha_region_text, self.region_alpha_hundreds_y_offset_text, 'y-axis offset in world coordinates', self.set_alpha_hundreds_y_offset, hundreds_minimum_offset, hundreds_maximum_offset, hundreds_offset_resolution, default_offset), (self.alpha_region_text, self.region_alpha_ones_y_offset_text, 'y-axis offset in world coordinates', self.set_alpha_ones_y_offset, ones_minimum_offset, ones_maximum_offset, ones_offset_resolution, default_offset), (self.alpha_region_text, self.region_alpha_hundreds_x_size_text, 'x-axis size in world coordinates', self.set_alpha_hundreds_x_size, hundreds_minimum_size, hundreds_maximum_size, hundreds_size_resolution, default_hundreds_size), (self.alpha_region_text, self.region_alpha_ones_x_size_text, 'x-axis size in world coordinates', self.set_alpha_ones_x_size, ones_minimum_size, ones_maximum_size, ones_size_resolution, default_size), (self.alpha_region_text, self.region_alpha_hundreds_y_size_text, 'y-axis size in world coordinates', self.set_alpha_hundreds_y_size, hundreds_minimum_size, hundreds_maximum_size, hundreds_size_resolution, default_hundreds_size), (self.alpha_region_text, self.region_alpha_ones_y_size_text, 'y-axis size in world coordinates', self.set_alpha_ones_y_size, ones_minimum_size, ones_maximum_size, ones_size_resolution, default_size))
        self.region_alpha_thousands_x_offset = default_offset
        self.region_alpha_hundreds_x_offset = default_offset
        self.region_alpha_ones_x_offset = default_offset
        self.region_alpha_thousands_y_offset = default_offset
        self.region_alpha_hundreds_y_offset = default_offset
        self.region_alpha_ones_y_offset = default_offset
        self.region_alpha_hundreds_x_size = default_hundreds_size
        self.region_alpha_ones_x_size = default_size
        self.region_alpha_hundreds_y_size = default_hundreds_size
        self.region_alpha_ones_y_size = default_size
        water_page = self.mainNotebook.add(self.name)
        id = 0
        if True:
            tab_name = 'Texture'
            page = self.mainNotebook.add(tab_name)
            button_list = (
             (
              'Apply Region Parameters', self.apply_region_parameters),)
            self.create_button_box(page, tab_name, 'Region Options:', 'help', button_list)
            button_list = (
             (
              'Assign Current Texture', self.assign_texture_to_region), ('Update Texture', self.update_texture), ('Update Shader', self.update_shader))
            self.create_button_box(page, tab_name, 'Options:', 'help', button_list)
            self.region_texture_message_bar = self.create_message_bar(page, tab_name, 'Texture:', 'Texture')
            self.texture_sliders_array = self.createSliders(id, page, texture_slider_definitions)
            id = id + 1
        if True:
            tab_name = 'Alpha'
            page = self.mainNotebook.add(tab_name)
            button_list = (
             (
              'Apply Region Parameters', self.apply_region_parameters),)
            self.create_button_box(page, tab_name, 'Region Options:', 'help', button_list)
            button_list = (
             (
              'Assign Current Alpha Texture', self.assign_alpha_texture_to_region), ('Update Alpha Texture', self.update_alpha_texture))
            self.create_button_box(page, tab_name, 'Options:', 'help', button_list)
            self.region_alpha_texture_message_bar = self.create_message_bar(page, tab_name, 'Alpha Texture:', 'Alpha Texture')
            self.alpha_sliders_array = self.createSliders(id, page, alpha_texture_slider_definitions)
            id = id + 1
        self.region_file_path_message_bar = self.create_message_bar(water_page, tab_name + 'file_path', 'File:', 'Filename')
        self.texture_message_bar = self.create_message_bar(water_page, 'Water', 'Current Texture:', 'Current Texture')
        self.alpha_texture_message_bar = self.create_message_bar(water_page, 'Water', 'Current Alpha Texture:', 'Current Alpha Texture')
        self.shader_message_bar = self.create_message_bar(water_page, 'Shader', 'Current Shader:', 'Current Shader')
        self.createCheckbutton(water_page, 'Water', 'Display Water', 'Turn Water on/off', self.toggle_display, 1)
        self.createCheckbutton(water_page, 'Water', 'Reflection', 'Turn relfection on/off', self.toggle_reflection, 1)
        self.createCheckbutton(water_page, 'Water', 'Texture Clamp', 'Turn texture clamping on/off', self.toggle_clamp, 1)
        self.createCheckbutton(water_page, 'Water', 'Alpha Texture Clamp', 'Turn alpha texture clamping on/off', self.toggle_alpha_clamp, 1)
        self.createCheckbutton(water_page, 'Water', 'Alpha Map', 'Turn alpha map on/off', self.toggle_alpha_map, 1)
        self.createCheckbutton(water_page, 'Water', 'Real-Time Controls', 'Turn real-time controls on/off', self.toggle_realtime_controls, 0)
        geomPage = self.mainNotebook.add('Geometry')
        self.createCheckbutton(geomPage, 'Geom', 'WireFrame', 'Toggle WireFrame', self.toggleWF, 0)

    def toggle_display(self):
        if self.seapatch != None:
            self.seapatch.toggle_display()
        return

    def update_region_shader_parameters(self):
        if self.seapatch != None and self.enable_region_update:
            self.seapatch.update_map_x_origin(self.get_region_x_offset())
            self.seapatch.update_map_y_origin(self.get_region_y_offset())
            self.seapatch.update_map_x_scale(self.get_region_x_size())
            self.seapatch.update_map_y_scale(self.get_region_y_size())
            self.seapatch.update_alpha_map_x_origin(self.get_region_alpha_x_offset())
            self.seapatch.update_alpha_map_y_origin(self.get_region_alpha_y_offset())
            self.seapatch.update_alpha_map_x_scale(self.get_region_alpha_x_size())
            self.seapatch.update_alpha_map_y_scale(self.get_region_alpha_y_size())
            self.seapatch.update_map_sliders()
        return

    def apply_region_parameters(self):
        if self.region_texture_filename != None:
            self.set_texture(self.region_texture_filename)
        if self.region_alpha_texture_filename != None:
            self.set_alpha_texture(self.region_alpha_texture_filename)
        self.update_region_shader_parameters()
        return

    def assign_texture_to_region(self):
        if self.texture_filename != None:
            self.set_message_bar_text(self.region_texture_message_bar, self.texture_filename)
            self.region_texture_filename = self.texture_filename
        return

    def assign_alpha_texture_to_region(self):
        if self.alpha_texture_filename != None:
            self.set_message_bar_text(self.region_alpha_texture_message_bar, self.alpha_texture_filename)
            self.region_alpha_texture_filename = self.alpha_texture_filename
        return

    def set_x_offset(self, value, command_data):
        self.region_thousands_x_offset = value
        self.update_region_shader_parameters()

    def set_hundreds_x_offset(self, value, command_data):
        self.region_hundreds_x_offset = value
        self.update_region_shader_parameters()

    def set_ones_x_offset(self, value, command_data):
        self.region_ones_x_offset = value
        self.update_region_shader_parameters()

    def set_y_offset(self, value, command_data):
        self.region_thousands_y_offset = value
        self.update_region_shader_parameters()

    def set_hundreds_y_offset(self, value, command_data):
        self.region_hundreds_y_offset = value
        self.update_region_shader_parameters()

    def set_ones_y_offset(self, value, command_data):
        self.region_ones_y_offset = value
        self.update_region_shader_parameters()

    def set_hundreds_x_size(self, value, command_data):
        self.region_hundreds_x_size = value
        self.update_region_shader_parameters()

    def set_ones_x_size(self, value, command_data):
        self.region_ones_x_size = value
        self.update_region_shader_parameters()

    def set_hundreds_y_size(self, value, command_data):
        self.region_hundreds_y_size = value
        self.update_region_shader_parameters()

    def set_ones_y_size(self, value, command_data):
        self.region_ones_y_size = value
        self.update_region_shader_parameters()

    def set_alpha_x_offset(self, value, command_data):
        self.region_alpha_thousands_x_offset = value
        self.update_region_shader_parameters()

    def set_alpha_hundreds_x_offset(self, value, command_data):
        self.region_alpha_hundreds_x_offset = value
        self.update_region_shader_parameters()

    def set_alpha_ones_x_offset(self, value, command_data):
        self.region_alpha_ones_x_offset = value
        self.update_region_shader_parameters()

    def set_alpha_y_offset(self, value, command_data):
        self.region_alpha_thousands_y_offset = value
        self.update_region_shader_parameters()

    def set_alpha_hundreds_y_offset(self, value, command_data):
        self.region_alpha_hundreds_y_offset = value
        self.update_region_shader_parameters()

    def set_alpha_ones_y_offset(self, value, command_data):
        self.region_alpha_ones_y_offset = value
        self.update_region_shader_parameters()

    def set_alpha_hundreds_x_size(self, value, command_data):
        self.region_alpha_hundreds_x_size = value
        self.update_region_shader_parameters()

    def set_alpha_ones_x_size(self, value, command_data):
        self.region_alpha_ones_x_size = value
        self.update_region_shader_parameters()

    def set_alpha_hundreds_y_size(self, value, command_data):
        self.region_alpha_hundreds_y_size = value
        self.update_region_shader_parameters()

    def set_alpha_ones_y_size(self, value, command_data):
        self.region_alpha_ones_y_size = value
        self.update_region_shader_parameters()

    def setSeaPatch(self, seapatch):
        self.seapatch = seapatch
        self.enable_region_update = False
        base_ten = BaseTen(seapatch.map_x_origin)
        self.texture_sliders_array[0].set(base_ten.thousands)
        self.texture_sliders_array[1].set(base_ten.hundreds)
        self.texture_sliders_array[2].set(base_ten.ones)
        print self.texture_sliders_array[0].get()
        print self.texture_sliders_array[1].get()
        print self.texture_sliders_array[2].get()
        base_ten = BaseTen(seapatch.map_y_origin)
        self.texture_sliders_array[3].set(base_ten.thousands)
        self.texture_sliders_array[4].set(base_ten.hundreds)
        self.texture_sliders_array[5].set(base_ten.ones)
        base_ten = BaseTen(seapatch.map_x_scale)
        self.texture_sliders_array[6].set(base_ten.thousands + base_ten.hundreds)
        self.texture_sliders_array[7].set(base_ten.ones)
        base_ten = BaseTen(seapatch.map_y_scale)
        self.texture_sliders_array[8].set(base_ten.thousands + base_ten.hundreds)
        self.texture_sliders_array[9].set(base_ten.ones)
        base_ten = BaseTen(seapatch.alpha_map_x_origin)
        self.alpha_sliders_array[0].set(base_ten.thousands)
        self.alpha_sliders_array[1].set(base_ten.hundreds)
        self.alpha_sliders_array[2].set(base_ten.ones)
        base_ten = BaseTen(seapatch.alpha_map_y_origin)
        self.alpha_sliders_array[3].set(base_ten.thousands)
        self.alpha_sliders_array[4].set(base_ten.hundreds)
        self.alpha_sliders_array[5].set(base_ten.ones)
        base_ten = BaseTen(seapatch.alpha_map_x_scale)
        self.alpha_sliders_array[6].set(base_ten.thousands + base_ten.hundreds)
        self.alpha_sliders_array[7].set(base_ten.ones)
        base_ten = BaseTen(seapatch.alpha_map_y_scale)
        self.alpha_sliders_array[8].set(base_ten.thousands + base_ten.hundreds)
        self.enable_region_update = True
        self.alpha_sliders_array[9].set(base_ten.ones)

    def updateWidgets(self):
        pass

    def _load_water_parameters(self):
        default_directory = base.config.GetString('water-panel-default-path', '.')
        filename = askopenfilename(initialdir=default_directory, filetypes=[('WTR', 'wtr')], title='Open Water File')
        if not filename:
            return False
        return self.load_region(filename)

    def load_water_parameters(self):
        if self._load_water_parameters():
            self.updateWidgets()

    def load_and_apply_water_parameters(self):
        if self._load_water_parameters():
            self.updateWidgets()
            self.apply_region_parameters()

    def save_water_parameters(self):
        if self.region_texture_filename != None and self.region_alpha_texture_filename != None:
            default_directory = base.config.GetString('water-panel-default-path', '.')
            filename = asksaveasfilename(initialdir=default_directory, filetypes=[('WTR', 'wtr')], title='Save Water File')
            if not filename:
                return
            if string.find(filename, '.wtr') != -1:
                output_file = open(filename, 'w')
            else:
                output_file = open(filename + '.wtr', 'w')
            self.save_region(output_file)
            self.set_message_bar_text(self.region_file_path_message_bar, filename)
        else:
            print 'ERROR: texture(s) not selected'
        return

    def set_texture(self, filename):
        if filename != None:
            file_path = Filename.fromOsSpecific(filename)
            self.texture_file_name = file_path.getBasename()
            self.texture_file_path = file_path
            if filename == self.texture_filename:
                self.seapatch.water_color_texture.reload()
            else:
                self.seapatch.set_water_color_texture(filename, True)
            self.texture_filename = filename
            self.set_message_bar_text(self.texture_message_bar, filename)
        return

    def update_texture(self):
        if self.texture_filename != None:
            self.set_texture(self.texture_filename)
        return

    def select_texture(self):
        default_directory = base.config.GetString('water-panel-default-texture-path', '.')
        filename = askopenfilename(initialdir=default_directory, filetypes=[('BMP JPG TIF', 'bmp jpg tif')], title='Select Texture')
        if not filename:
            return
        else:
            print filename
            self.set_texture(filename)

    def set_alpha_texture(self, filename):
        if filename != None:
            file_path = Filename.fromOsSpecific(filename)
            self.alpha_texture_file_name = file_path.getBasename()
            self.alpha_texture_file_path = file_path
            if filename == self.alpha_texture_filename:
                self.seapatch.water_alpha_texture.reload()
            else:
                self.seapatch.set_water_alpha_texture(filename, True)
            self.alpha_texture_filename = filename
            self.set_message_bar_text(self.alpha_texture_message_bar, filename)
        return

    def update_alpha_texture(self):
        if self.alpha_texture_filename != None:
            self.set_alpha_texture(self.alpha_texture_filename)
        return

    def select_alpha_texture(self):
        default_directory = base.config.GetString('water-panel-default-texture-path', '.')
        filename = askopenfilename(initialdir=default_directory, filetypes=[('BMP JPG TIF', 'bmp jpg tif')], title='Select Alpha Texture')
        if not filename:
            return
        else:
            print filename
            self.set_alpha_texture(filename)

    def set_shader(self, filename):
        if filename != None:
            file_path = Filename.fromOsSpecific(filename)
            self.shader_file_name = file_path.getBasename()
            self.shader_file_path = file_path
            self.seapatch.set_shader(filename, True)
            self.shader_filename = filename
            self.set_message_bar_text(self.shader_message_bar, filename)
        return

    def update_shader(self):
        if self.shader_filename != None:
            self.set_shader(self.shader_filename)
        return

    def select_shader(self):
        default_directory = base.config.GetString('water-panel-default-shader-path', '.')
        filename = askopenfilename(initialdir=default_directory, filetypes=[('CG', 'cg')], title='Select Shader')
        if not filename:
            return
        else:
            print filename
            self.set_shader(filename)

    def toggleWF(self):
        base.toggleWireframe()

    def createCheckbutton(self, parent, category, text, balloonHelp, command, initialState, side='top'):
        bool = BooleanVar()
        bool.set(initialState)
        widget = Checkbutton(parent, text=text, anchor=W, variable=bool)
        widget['command'] = command
        widget.pack(fill=X, side=side)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        self.variableDict[category + '-' + text] = bool
        return widget

    def createRadiobutton(self, parent, side, category, text, balloonHelp, variable, value, command):
        widget = Radiobutton(parent, text=text, anchor=W, variable=variable, value=value)
        widget['command'] = command
        widget.pack(side=side, fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createFloaters(self, parent, widgetDefinitions):
        widgets = []
        for category, label, balloonHelp, command, min, resolution in widgetDefinitions:
            widgets.append(self.createFloater(parent, category, label, balloonHelp, command, min, resolution))

        return widgets

    def createFloater(self, parent, category, text, balloonHelp, command=None, min=0.0, resolution=None, numDigits=4, **kw):
        kw['text'] = text
        kw['min'] = min
        kw['resolution'] = resolution
        kw['numDigits'] = numDigits
        widget = apply(Floater.Floater, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createAngleDial(self, parent, category, text, balloonHelp, command=None, **kw):
        kw['text'] = text
        kw['style'] = 'mini'
        widget = apply(Dial.AngleDial, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createSlider(self, id, parent, category, text, balloonHelp, command=None, min=0.0, max=1.0, resolution=0.001, default=0.0, **kw):
        kw['text'] = text
        kw['min'] = min
        kw['max'] = max
        kw['resolution'] = resolution
        kw['value'] = default
        widget = apply(Slider.Slider, (parent,), kw)
        widget.id = id
        widget['command'] = command
        widget['commandData'] = [widget]
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + id.__repr__() + '-' + text] = widget
        return widget

    def createSliders(self, id, parent, widgetDefinitions):
        widgets = []
        for category, label, balloonHelp, command, min, max, resolution, default in widgetDefinitions:
            widgets.append(self.createSlider(id, parent, category, label, balloonHelp, command, min, max, resolution, default))

        return widgets

    def createVector2Entry(self, parent, category, text, balloonHelp, command=None, **kw):
        kw['text'] = text
        widget = apply(VectorWidgets.Vector2Entry, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createVector3Entry(self, parent, category, text, balloonHelp, command=None, **kw):
        kw['text'] = text
        widget = apply(VectorWidgets.Vector3Entry, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createColorEntry(self, parent, category, text, balloonHelp, command=None, **kw):
        kw['text'] = text
        widget = apply(VectorWidgets.ColorEntry, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createOptionMenu(self, parent, category, text, balloonHelp, items, command):
        optionVar = StringVar()
        if len(items) > 0:
            optionVar.set(items[0])
        widget = Pmw.OptionMenu(parent, labelpos=W, label_text=text, label_width=12, menu_tearoff=1, menubutton_textvariable=optionVar, items=items)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget.component('menubutton'), balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        self.variableDict[category + '-' + text] = optionVar
        return optionVar

    def createComboBox(self, parent, category, text, balloonHelp, items, command, history=0):
        widget = Pmw.ComboBox(parent, labelpos=W, label_text=text, label_anchor='w', label_width=12, entry_width=16, history=history, scrolledlist_items=items)
        if len(items) > 0:
            widget.selectitem(items[0])
        widget['selectioncommand'] = command
        widget.pack(side='left', expand=0)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def create_message_bar(self, parent, category, text, balloonHelp):
        widget = Pmw.MessageBar(parent, entry_width=40, entry_relief='groove', labelpos='w', label_text=text)
        widget.pack(side='top', fill='x', expand=0, padx=0, pady=4)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def set_message_bar_text(self, message_bar, text):
        if message_bar != None:
            message_bar.message('state', text)
        return

    def create_button_box(self, parent, category, text, balloonHelp, button_list):
        widget = Pmw.ButtonBox(parent, labelpos='nw', label_text=text, frame_borderwidth=2, frame_relief='groove')
        widget.pack(side='top', fill='both', expand=0, padx=0, pady=4)
        for button_text, function in button_list:
            widget.add(button_text, command=function)

        widget.alignbuttons()
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def getWidget(self, category, text):
        return self.widgetDict[category + '-' + text]

    def getVariable(self, category, text):
        return self.variableDict[category + '-' + text]


class BaseTen():

    def __init__(self, value):
        original_value = value
        resolution = 1000.0
        thousands = self.floor(value / resolution) * resolution
        value = value - thousands
        resolution = 100.0
        hundreds = self.floor(value / resolution) * resolution
        value = value - hundreds
        self.thousands = thousands
        self.hundreds = hundreds
        self.ones = value
        print original_value, thousands, hundreds, value

    def mod(self, numerator, denominator):
        return math.fmod(numerator, denominator)

    def floor(self, value):
        if value >= 0:
            return math.floor(value)
        else:
            return math.ceil(value)