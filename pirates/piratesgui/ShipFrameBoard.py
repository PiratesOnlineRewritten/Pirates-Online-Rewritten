from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import PiratesTimer
from pirates.piratesgui.ShipFrame import ShipFrame
from pirates.piratesgui.DialogButton import DialogButton
from pirates.piratesgui.ShipSnapshot import ShipSnapshot
from pirates.ship import ShipGlobals

class ShipFrameBoard(ShipFrame):

    def __init__(self, parent, **kw):
        gui = loader.loadModel('models/gui/toplevel_gui')
        image = (gui.find('**/generic_button'), gui.find('**/generic_button_down'), gui.find('**/generic_button_over'), gui.find('**/generic_button_disabled'))
        optiondefs = (
         (
          'relief', 0, None), ('frameSize', (0.0, 0.9, 0.0, 0.42), None), ('image', image[3], None), ('image_pos', (0.45, 0.0, 0.208), None), ('image_scale', (0.94, 1, 1.1), None), ('image_color', (0.8, 0.8, 0.8, 1), None), ('frameColor', (1, 1, 1, 0.9), None), ('snapShotPos', (-0.04, 0, -0.08), None), ('shipPos', VBase3(0.2, 0, 0.08), None), ('shipHpr', VBase3(-70, 6, 15), None), ('shipScale', VBase3(0.55), None), ('time', 0, None), ('command', None, None), ('extraArgs', [], None))
        self.nameLabel = None
        self.classLabel = None
        self.typeLabel = None
        self.stateLabel = None
        self.button = None
        self.snapShot = None
        self.defineoptions(kw, optiondefs)
        ShipFrame.__init__(self, parent, **kw)
        self.initialiseoptions(ShipFrameBoard)
        return None

    def destroy(self):
        self.nameLabel = None
        self.classLabel = None
        self.typeLabel = None
        self.stateLabel = None
        self.button = None
        self.snapShot = None
        ShipFrame.destroy(self)
        return

    def createGui(self):
        ShipFrame.createGui(self)
        self.nameLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=PLocalizer.makeHeadingString(self['shipName'], 2), text_align=TextNode.ALeft, text_scale=0.05, text_pos=(0.06,
                                                                                                                                                                                                 0.015), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, frameColor=PiratesGuiGlobals.ButtonColor1[3], frameSize=(self['frameSize'][0] + 0.04, self['frameSize'][1] - 0.03, -0.0, 0.05), pos=(0, 0, self['frameSize'][3] - 0.09))
        self.classLabel = DirectLabel(parent=self.nameLabel, relief=None, state=DGG.DISABLED, text=PLocalizer.makeHeadingString(PLocalizer.ShipClassNames.get(self['shipClass']), 1), text_font=PiratesGlobals.getInterfaceFont(), text_scale=PiratesGuiGlobals.TextScaleMed, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                                                                                                         1), textMayChange=1, text_pos=(self.nameLabel['frameSize'][0] + 0.02, -0.03))
        self.timer = PiratesTimer.PiratesTimer(showMinutes=True, mode=None, titleText='', titleFg='', infoText='', cancelText='', cancelCallback=None)
        self.timer.setFontColor(PiratesGuiGlobals.TextFG2)
        self.timer.reparentTo(self)
        self.timer.setScale(0.55)
        self.timer.setPos(0.62, 0, 0.315)
        self.timer.unstash()
        self.timer.countdown(self['time'])
        self.mainText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text='How will you lead your crew?', text_pos=(0.62,
                                                                                                                                 0.2), text_font=PiratesGlobals.getInterfaceFont(), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=10, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                                                1), textMayChange=1)
        gui = loader.loadModel('models/gui/toplevel_gui')
        geomCheck = gui.find('**/generic_check')
        self.yesButton = DialogButton(parent=self, buttonStyle=DialogButton.YES, pos=(0.5,
                                                                                      0,
                                                                                      0.08), text=PLocalizer.BoardShip, text_scale=PiratesGuiGlobals.TextScaleLarge, text_font=PiratesGlobals.getInterfaceFont(), text_pos=(0.035, -0.014), geom=(geomCheck,) * 4, geom_pos=(-0.06, 0, 0), geom_scale=0.5, geom0_color=PiratesGuiGlobals.ButtonColor6[0], geom1_color=PiratesGuiGlobals.ButtonColor6[1], geom2_color=PiratesGuiGlobals.ButtonColor6[2], geom3_color=PiratesGuiGlobals.ButtonColor6[3], image3_color=(0.8,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     0.8,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     0.8,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     1), helpPos=(0, 0, -0.12), helpDelay=0.3, command=self['command'], extraArgs=[True])
        self.noButton = DialogButton(parent=self, buttonStyle=DialogButton.NO, pos=(0.74,
                                                                                    0,
                                                                                    0.08), text=PLocalizer.ParlayShip, text_scale=PiratesGuiGlobals.TextScaleLarge, text_font=PiratesGlobals.getInterfaceFont(), text_pos=(0.035, -0.014), helpPos=(0, 0, -0.12), helpDelay=0.3, command=self['command'], extraArgs=[False])
        return

    def enableStats(self, shipName='', shipClass=0, mastInfo=[], hp=0, sp=0, cargo=0, crew=0, time=0):
        pass