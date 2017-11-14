from pandac.PandaModules import Vec4, TextNode
from direct.gui.DirectGui import DirectLabel, DGG
from pirates.piratesgui.DialMeter import DialMeter
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.GuiPanel import OnscreenImage

class RepairGameButton(GuiButton):

    def __init__(self, parent, **kw):
        optiondefs = (
         ('nodePath', None, None), ('image_scale', (1.0, 1.0, 1.0), None))
        self.defineoptions(kw, optiondefs)
        GuiButton.__init__(self, parent)
        self.initialiseoptions(RepairGameButton)
        self.disabledStateNode = self.stateNodePath[3].getChild(0)
        self.downStateNode = self.stateNodePath[1].getChild(0)
        self.overStateNode = self.stateNodePath[2].getChild(0)
        self.inProgress = False
        self._initGUI()
        return

    def _initGUI(self):
        self.setBin('fixed', 33)
        mainGui = loader.loadModel('models/gui/gui_main')
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.checkMark = gui.find('**/generic_check')
        self.checkMark.reparentTo(self)
        self.checkMark.stash()
        self.checkMark.setScale(1.0)
        self.checkMark.setColorScale(0.0, 1.0, 0.0, 1.0)
        self.checkMark.setPos(0.02, 0.0, 0.02)
        self.checkMark.setBin('fixed', 34)
        self.skillRing = DialMeter(self, wantCover=False, dangerRatio=0.0, meterColor=Vec4(0.9, 0.9, 0.1, 1.0), baseColor=Vec4(0.15, 0.07, 0.03, 1.0), completeColor=Vec4(0.1, 0.9, 0.1, 1.0))
        self.skillRing.reparentTo(self)
        self.skillRing.setScale(0.285, 0.3, 0.265)
        self.skillRing.setBin('fixed', 32)
        self.skillGlow = self.glow = OnscreenImage(parent=self, image=mainGui.find('**/icon_glow'), scale=(1.0,
                                                                                                           1.0,
                                                                                                           1.0), color=(1.0,
                                                                                                                        1.0,
                                                                                                                        0.6,
                                                                                                                        1.0))
        self.skillGlow.reparentTo(self)
        self.skillGlow.setBin('fixed', 31)
        self.skillGlow.stash()
        self.pirateNameBox = None
        self.pirateNameLabel = None
        return

    def showGlow(self):
        self.inProgress = False
        if self.pirateNameLabel == None and self.checkMark.isStashed():
            self.skillGlow.unstash()
        return

    def hideGlow(self):
        self.inProgress = True
        self.skillGlow.stash()

    def setProgress(self, percent):
        self.skillGlow.stash()
        ratio = max(0.0, percent / 100.0)
        if ratio >= 1.0:
            if self.checkMark.isStashed():
                self.checkMark.unstash()
        else:
            if not self.checkMark.isStashed():
                self.checkMark.stash()

        if self.pirateNameLabel == None and not self.inProgress:
            self.skillGlow.unstash()

        self.skillRing.update(ratio, 1.0)
        self.skillRing.wrtReparentTo(self.getParent())
        self.reparentTo(self.getParent())

    def updatePirateNameBox(self, pirateName):
        if self.pirateNameLabel != None and self.pirateNameLabel['text'] != pirateName:
            if self.pirateNameBox:
                self.pirateNameBox.destroy()
            if self.pirateNameLabel:
                self.pirateNameLabel.destroy()
            self.pirateNameBox = None
            self.pirateNameLabel = None
        if pirateName != '' and not (self.pirateNameBox and self.pirateNameLabel['text'] == pirateName):
            self.createPirateNameBox(pirateName)
        return

    def createPirateNameBox(self, pirateName):
        self.pirateNameLabel = DirectLabel(relief=None, state=DGG.DISABLED, text=pirateName, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG1, text_wordwrap=12, textMayChange=0, sortOrder=91)
        self.pirateNameLabel.setBin('fixed', 33)
        height = self.pirateNameLabel.getHeight()
        width = self.pirateNameLabel.getWidth() + 0.05
        pos = [0.0, 0.0, height / 2 - 0.035]
        fs = [-(width / 2 + 0.01), width / 2 + 0.01, -(height / 2 + 0.015), height / 2 + 0.015]
        self.pirateNameBox = BorderFrame(parent=self, state=DGG.DISABLED, frameSize=(fs[0], fs[1], fs[2], fs[3]), modelName='general_frame_f', pos=(0.0,
                                                                                                                                                    0.0,
                                                                                                                                                    0.0))
        self.pirateNameLabel.reparentTo(self.pirateNameBox)
        self.pirateNameLabel.setPos(pos[0], pos[1], pos[2])
        self.pirateNameBox.setClipPlaneOff()
        pos = self.pirateNameBox.getPos(aspect2d)
        x = min(pos[0], base.a2dRight - width)
        z = max(pos[2], base.a2dBottom - height)
        self.pirateNameBox.setPos(aspect2d, x, 0, z - 0.175)
        self.pirateNameBox.flattenLight()
        self.pirateNameBox.setBin('fixed', 32)
        self.pirateNameBox.reparentTo(self)
        return
