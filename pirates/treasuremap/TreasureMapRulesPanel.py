from pandac.PandaModules import *
from direct.task import Task
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiTray
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class TreasureMapRulesPanel():

    def __init__(self, panelTitle, instructions, parent=base.a2dTopCenter, duration=8.0):
        self.panelTitle = panelTitle
        self.instructions = instructions
        self.showPanelIval = None
        self.duration = duration
        self.load(parent)
        return

    def load(self, parent=None):
        self.frame = BorderFrame(parent=parent, frameSize=(-0.55, 0.55, -0.125, 0.125), pos=(0, 0, -0.15))
        self.panelTitleText = DirectLabel(parent=self.frame, relief=None, text=self.panelTitle, text_scale=0.07, text_align=TextNode.ACenter, text_font=PiratesGlobals.getPirateFont(), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                        1), pos=(0,
                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                 0.025))
        self.instructionsText = DirectLabel(parent=self.frame, relief=None, text=self.instructions, text_scale=0.05, text_align=TextNode.ACenter, text_wordwrap=40, text_fg=(1,
                                                                                                                                                                             1,
                                                                                                                                                                             1,
                                                                                                                                                                             1), text_shadow=(0,
                                                                                                                                                                                              0,
                                                                                                                                                                                              0,
                                                                                                                                                                                              1), pos=(0, 0, -0.03))
        self.frame.stash()
        self.openSfx = loadSfx(SoundGlobals.SFX_GUI_SHOW_PANEL)
        self.showPanelIval = Sequence(Wait(2.0), Func(self.frame.unstash), Func(base.playSfx, self.openSfx), LerpPosInterval(self.frame, 0.5, Point3(0, 0, -0.15), startPos=Point3(0, 0, 0.5), blendType='easeOut'), Wait(self.duration), LerpPosInterval(self.frame, 0.5, Point3(0, 0, 0.5), startPos=Point3(0, 0, -0.15), blendType='easeOut'), Func(self.frame.stash))
        return

    def destroy(self):
        self.frame.destroy()
        taskMgr.remove('hideTMRulesTask')
        if self.showPanelIval:
            self.showPanelIval.pause()
            self.showPanelIval = None
        del self.openSfx
        del self.frame
        del self.panelTitleText
        del self.instructionsText
        return

    def setInstructions(self, instructions):
        self.instructionsText['text'] = instructions

    def show(self):
        self.frame.show()
        if self.showPanelIval.isPlaying():
            self.showPanelIval.finish()
        self.showPanelIval.start()

    def hide(self, task=None):
        self.frame.stash()