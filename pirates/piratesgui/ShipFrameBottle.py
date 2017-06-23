from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ShipFrame import ShipFrame
from pirates.piratesgui.ShipStatFrame import ShipStatFrame

class ShipFrameBottle(ShipFrame):

    def __init__(self, parent, **kw):
        optiondefs = (
         (
          'frameSize', (0, 0.9, 0.0, 0.53), None), ('frameColor', PiratesGuiGlobals.ButtonColor1, None), ('relief', DGG.FLAT, None), ('shipPos', VBase3(0.58, 0, 0.13), None), ('shipHpr', VBase3(-70, 6, 15), None), ('shipScale', VBase3(0.65), None), ('inBottle', True, self.setInBottle))
        self.nameLabel = None
        self.classLabel = None
        self.statFrame = None
        self.statTrigger = None
        self.defineoptions(kw, optiondefs)
        ShipFrame.__init__(self, parent, **kw)
        self.initialiseoptions(ShipFrameBottle)
        self.accept('within-%s' % self.guiId, self.mouseOver)
        self.accept('without-%s' % self.guiId, self.mouseOff)
        return

    def destroy(self):
        self.ignore('within-%s' % self.guiId)
        self.ignore('without-%s' % self.guiId)
        if self.statTrigger:
            self.ignore('within-%s' % self.statTrigger.guiId)
            self.ignore('without-%s' % self.statTrigger.guiId)
        self.nameLabel = None
        self.classLabel = None
        self.statFrame = None
        if self.statTrigger:
            self.statTrigger.destroy()
            self.statTrigger = None
        ShipFrame.destroy(self)
        return

    def createGui(self):
        ShipFrame.createGui(self)
        if self['shipName']:
            self.nameLabel = DirectLabel(parent=self, relief=DGG.FLAT, state=DGG.DISABLED, text=self['shipName'], text_font=PiratesGlobals.getInterfaceFont(), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.04,
                                                                                                                                                                                                                                               0.015), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, frameColor=PiratesGuiGlobals.ButtonColor1[3], frameSize=(self['frameSize'][0] + 0.02, self['frameSize'][1] - 0.02, 0, 0.05), pos=(0, 0, self['frameSize'][3] - 0.06))
        if self['shipClass']:
            self.classLabel = DirectLabel(parent=self.nameLabel, relief=None, state=DGG.DISABLED, text=PLocalizer.ShipClassNames.get(self['shipClass']), text_scale=PiratesGuiGlobals.TextScaleMed, text_align=TextNode.ARight, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=(0,
                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                1), text_wordwrap=15, textMayChange=0, text_pos=(self.nameLabel['frameSize'][1] - 0.02, 0.015), text_font=PiratesGlobals.getInterfaceFont())
        return

    def setPos(self, *args, **kwargs):
        ShipFrame.setPos(self, *args, **kwargs)
        if self.statTrigger:
            self.statTrigger.reparentTo(self)
            self.statTrigger.setPos(self.statFrame.getPos())
            self.statTrigger.wrtReparentTo(self.getParent())
            self.reparentTo(self.getParent())

    def setInBottle(self):
        if self.shipMeter:
            if self['inBottle']:
                self.shipMeter.clearColorScale()
                self.shipMeter.clearTransparency()
            else:
                self.shipMeter.setColorScale(1, 1, 1, 0)
                self.shipMeter.setTransparency(1)

    def enableStats(self, shipName='', shipClass=0, mastInfo=[], hp=0, maxHp=0, sp=0, maxSp=0, cargo=0, maxCargo=0, crew=0, maxCrew=0, time=0):
        self.statFrame = ShipStatFrame(self, None, shipName, shipClass, mastInfo, hp, maxHp, sp, maxSp, cargo, maxCargo, crew, maxCrew, time)
        self.__enableStats()
        return

    def enableStatsOV(self, shipOv):
        self.statFrame = ShipStatFrame(self, shipOv, pos=(0.21, 0, 0.03))
        self.__enableStats()

    def __enableStats(self):
        self.statFrame.hide()
        self.statTrigger = DirectFrame(parent=self, relief=DGG.FLAT, frameSize=self.statFrame['frameSize'], frameColor=(1,
                                                                                                                        1,
                                                                                                                        1,
                                                                                                                        0), pos=self.statFrame.getPos(), suppressMouse=False)
        self.accept('within-%s' % self.statTrigger.guiId, self.mouseOverStat)
        self.accept('without-%s' % self.statTrigger.guiId, self.mouseOffStat)

    def mouseOver(self, *args):
        if self.nameLabel:
            self.nameLabel['frameColor'] = PiratesGuiGlobals.ButtonColor1[1]

    def mouseOff(self, *args):
        if self.nameLabel:
            self.nameLabel['frameColor'] = PiratesGuiGlobals.ButtonColor1[3]

    def mouseOverStat(self, *args):
        if self.statFrame:
            self.statFrame.scheduleShow(0.0)

    def mouseOffStat(self, *args):
        if self.statFrame:
            self.statFrame.hide()