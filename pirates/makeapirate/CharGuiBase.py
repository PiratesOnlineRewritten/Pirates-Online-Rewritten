from direct.gui.DirectGui import *
from pandac.PandaModules import *

class CharGuiSlider(DirectSlider):

    def __init__(self, main, parent, text, command, range=(
 -0.5, 0.5)):
        DirectSlider.__init__(self, parent=parent, relief=None, frameSize=(-0.6, 0.6, 0.1, -0.1), image=main.charGui.find('**/chargui_slider_small'), image_scale=1.33, thumb_image=(main.charGui.find('**/chargui_slider_node'), main.charGui.find('**/chargui_slider_node_down'), main.charGui.find('**/chargui_slider_node_over')), thumb_scale=1.2, thumb_relief=None, text=text, text_fg=(1,
                                                                                                                                                                                                                                                                                                                                                                                               1,
                                                                                                                                                                                                                                                                                                                                                                                               1,
                                                                                                                                                                                                                                                                                                                                                                                               1), text_scale=0.18, text_pos=(0.7, -0.04), text_align=TextNode.ALeft, scale=1, value=0, range=range, command=command)
        self.initialiseoptions(CharGuiSlider)
        return


class CharGuiPicker(DirectFrame):

    def __init__(self, main, parent, text, nextCommand, backCommand):
        DirectFrame.__init__(self, parent=parent, relief=None, text=text, text_fg=(1,
                                                                                   1,
                                                                                   1,
                                                                                   1), text_scale=0.18, text_pos=(0,
                                                                                                                  0), scale=0.7)
        self.initialiseoptions(CharGuiPicker)
        self.nextButton = DirectButton(parent=self, relief=None, image=(main.triangleGui.find('**/triangle'), main.triangleGui.find('**/triangle_down'), main.triangleGui.find('**/triangle_over')), pos=(0.6,
                                                                                                                                                                                                          0,
                                                                                                                                                                                                          0.07), scale=0.2, command=nextCommand)
        self.backButton = DirectButton(parent=self, relief=None, image=(main.triangleGui.find('**/triangle'), main.triangleGui.find('**/triangle_down'), main.triangleGui.find('**/triangle_over')), hpr=(0,
                                                                                                                                                                                                          0,
                                                                                                                                                                                                          180), pos=(-0.6, 0, 0.07), scale=0.2, command=backCommand)
        return