from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from direct.interval.IntervalGlobal import *

class GuiPanel(BorderFrame):

    def __init__(self, title, w, h, showClose=True, titleSize=0, modelName='general_frame_f', **kw):
        self.width = w
        self.height = h
        BorderFrame.__init__(self, frameSize=(0, w, 0, h), modelName=modelName, sortOrder=20, **kw)
        self.initialiseoptions(GuiPanel)
        titleFont = PiratesGuiGlobals.TextScaleMed
        textColor = PiratesGuiGlobals.TextFG1
        textShadow = PiratesGuiGlobals.TextShadow
        wordwrap = 13
        if titleSize == 0:
            titleFont = PiratesGuiGlobals.TextScaleMed
            textColor = PiratesGuiGlobals.TextFG1
            textShadow = PiratesGuiGlobals.TextShadow
            wordwrap = 13
        else:
            if titleSize == 1:
                titleFont = PiratesGuiGlobals.TextScaleLarge
                textColor = PiratesGuiGlobals.TextFG2
                textShadow = None
                wordwrap = 10
            elif titleSize == 1.5:
                titleFont = PiratesGuiGlobals.TextScaleExtraLarge
                textColor = PiratesGuiGlobals.TextFG1
                textShadow = None
                wordwrap = 10
            if title:
                self.titleLabel = DirectLabel(parent=self, relief=None, pos=(0.05, 0, h - PiratesGuiGlobals.TextScaleSmall * 2.5), text=title, text_align=TextNode.ALeft, text_scale=titleFont, text_pos=(0.015,
                                                                                                                                                                                                          0.015), text_fg=textColor, text_shadow=textShadow, text_font=PiratesGlobals.getPirateOutlineFont(), textMayChange=1, text_wordwrap=wordwrap, sortOrder=21)
            else:
                self.titleLabel = None
            if showClose:
                lookoutUI = loader.loadModel('models/gui/lookout_gui')
                self.closeButton = DirectButton(parent=self, relief=None, image=(lookoutUI.find('**/lookout_close_window'), lookoutUI.find('**/lookout_close_window_down'), lookoutUI.find('**/lookout_close_window_over'), lookoutUI.find('**/lookout_close_window_disabled')), pos=(w - 0.055, 0, h - 0.055), scale=0.125, command=self.closePanel, sortOrder=21)
                lookoutUI.removeNode()
            self.closeButton = None
        self.fadeLerp = None
        return

    def changeTitle(self, text):
        self.titleLabel['text'] = text

    def destroy(self):
        if self.fadeLerp:
            self.fadeLerp.pause()
            del self.fadeLerp
        DirectFrame.destroy(self)

    def closePanel(self):
        self.hide()

    def setMouseFade(self, fade):
        if fade:
            self.bind(DGG.WITHIN, self.withinFrame)
            self.bind(DGG.WITHOUT, self.withoutFrame)
            self.setAlphaScale(0)
        else:
            self.unbind(DGG.WITHIN)
            self.unbind(DGG.WITHOUT)

    def withinFrame(self, event):
        if self.fadeLerp:
            self.fadeLerp.pause()
            del self.fadeLerp
        self.fadeLerp = LerpFunctionInterval(self.setAlphaScale, fromData=self.getColorScale()[3], toData=1, duration=0.5)
        self.fadeLerp.start()

    def withoutFrame(self, event):
        if self.fadeLerp:
            self.fadeLerp.pause()
            del self.fadeLerp
        self.fadeLerp = LerpFunctionInterval(self.setAlphaScale, fromData=self.getColorScale()[3], toData=0, duration=0.5)
        self.fadeLerp.start()