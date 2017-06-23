from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals

class ComboMeter(DirectObject.DirectObject):
    COMBO_METER_RESET = 2.0
    COMBO_NUM_SCALE = 0.14
    BACKSTAB_SCALE = 0.09
    TEXT_COLOR = PiratesGuiGlobals.TextFG1
    TEAM_COMBO_TEXT_COLOR = PiratesGuiGlobals.TextFG4
    SUB_TEXT_COLOR = PiratesGuiGlobals.TextFG2
    NUMBER_COLOR = PiratesGuiGlobals.TextFG1
    BACKSTAB_COLOR = Vec4(0.8, 0.4, 0.2, 1)

    def __init__(self):
        DirectObject.DirectObject.__init__(self)
        self.combo = 0
        self.totalDamage = 0
        self.text = DirectLabel(parent=base.a2dTopLeft, relief=None, text=PLocalizer.HitCombo, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleTitleLarge, text_fg=self.TEXT_COLOR, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.5, 0, -0.5), text_font=PiratesGlobals.getPirateOutlineFont())
        self.text.setTransparency(1)
        self.subText = DirectLabel(parent=self.text, relief=None, text=PLocalizer.Damage, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_fg=self.SUB_TEXT_COLOR, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.09, 0, -0.07), text_font=PiratesGlobals.getPirateOutlineFont())
        self.comboCounter = DirectLabel(parent=self.text, relief=None, text='', text_align=TextNode.ARight, text_scale=self.COMBO_NUM_SCALE, text_fg=self.NUMBER_COLOR, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(-0.026, 0, -0.01), text_font=PiratesGlobals.getPirateOutlineFont())
        self.backstabText = DirectLabel(parent=base.a2dTopLeft, relief=None, text='Backstab!', text_align=TextNode.ALeft, text_scale=self.BACKSTAB_SCALE, text_fg=self.BACKSTAB_COLOR, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(1.165, 0, -0.97), text_font=PiratesGlobals.getPirateOutlineFont())
        self.text.hide()
        self.backstabText.hide()
        self.faderIn = None
        self.faderOut = None
        self.animIval = None
        self.backstabFaderIn = None
        self.backstabFaderOut = None
        self.backstabAnimIval = None
        self.accept('trackCombo', self.newHit)
        return

    def destroy(self):
        if self.animIval:
            self.animIval.pause()
            self.animIval = None
        if self.faderIn:
            self.faderIn.pause()
            self.faderIn = None
        if self.faderOut:
            self.faderOut.pause()
            self.faderOut = None
        if self.backstabAnimIval:
            self.backstabAnimIval.pause()
            self.backstabAnimIval = None
        if self.backstabFaderIn:
            self.backstabFaderIn.pause()
            self.backstabFaderIn = None
        if self.backstabFaderOut:
            self.backstabFaderOut.pause()
            self.backstabFaderOut = None
        if self.text:
            self.text.destroy()
            self.text = None
        if self.backstabText:
            self.backstabText.destroy()
            self.backstabText = None
        self.ignoreAll()
        taskMgr.remove(self.__getResetComboMeter())
        return

    def newHit(self, value, numAttackers, totalDamage):
        if value == 0 and numAttackers == 0 and totalDamage == 0:
            self.resetMeter()
        if value <= 1:
            return
        self.__showMeter()
        if self.combo < value:
            self.combo = value
            self.comboCounter['text'] = str(self.combo)
            color = Vec4(0.6 + value * 0.1, 1.0 - value * 0.1, 0, 1)
            self.comboCounter['text_fg'] = color
            if self.animIval:
                self.animIval.finish()
                self.animIval = None
            scaleIval = self.comboCounter.scaleInterval(0.2, 1.0, startScale=2.0, blendType='easeIn')
            self.animIval = Parallel(scaleIval)
            self.animIval.start()
        if numAttackers > 1:
            self.text['text'] = PLocalizer.TeamCombo
            self.text['text_fg'] = self.TEAM_COMBO_TEXT_COLOR
        if abs(self.totalDamage) < abs(totalDamage):
            self.totalDamage = totalDamage
            self.subText['text'] = str(abs(self.totalDamage)) + ' ' + PLocalizer.Damage
        taskMgr.remove(self.__getResetComboMeter())
        taskMgr.doMethodLater(self.COMBO_METER_RESET, self.resetMeter, self.__getResetComboMeter())
        return

    def newBackstab(self):
        self.__showBackstab()
        if self.backstabAnimIval:
            self.backstabAnimIval.finish()
            self.backstabAnimIval = None
        scaleIval = self.backstabText.scaleInterval(0.2, 1.0, startScale=2.0, blendType='easeIn')
        self.backstabAnimIval = Parallel(scaleIval)
        self.backstabAnimIval.start()
        taskMgr.remove(self.__getResetBackstab())
        taskMgr.doMethodLater(self.COMBO_METER_RESET, self.resetBackstab, self.__getResetBackstab())
        return

    def resetMeter(self, args=None):
        self.__fadeOutMeter()
        self.combo = 0
        self.totalDamage = 0

    def resetBackstab(self, args=None):
        self.__fadeOutBackstab()

    def __getResetComboMeter(self):
        return 'resetComboMeter'

    def __getResetBackstab(self):
        return 'resetBackstab'

    def __hideMeter(self):
        if self.faderIn:
            self.faderIn.pause()
            self.faderIn = None
        if self.faderOut:
            self.faderOut.pause()
            self.faderOut = None
        self.text.hide()
        self.backstabText.hide()
        return

    def __showMeter(self):
        if self.faderIn:
            self.faderIn.pause()
            self.faderIn = None
        if self.faderOut:
            self.faderOut.pause()
            self.faderOut = None
        self.text.show()
        self.text.setAlphaScale(1.0)
        self.text['text_fg'] = self.TEXT_COLOR
        return

    def __showBackstab(self):
        if self.backstabFaderIn:
            self.backstabFaderIn.pause()
            self.backstabFaderIn = None
        if self.backstabFaderOut:
            self.backstabFaderOut.pause()
            self.backstabFaderOut = None
        self.backstabText.show()
        self.backstabText.setAlphaScale(1.0)
        return

    def __fadeInMeter(self):
        self.text.show()
        if self.faderOut:
            self.faderOut.pause()
            self.faderOut = None
        if self.faderIn:
            return
        self.faderIn = LerpFunctionInterval(self.text.setAlphaScale, fromData=0, toData=1, duration=1.0)
        self.faderIn.start()
        return

    def __fadeOutMeter(self):
        if self.faderIn:
            self.faderIn.pause()
            self.faderIn = None
        if self.faderOut:
            return

        def restoreColor():
            self.text['text_fg'] = self.TEXT_COLOR
            self.text['text'] = PLocalizer.HitCombo
            self.subText['text'] = str(0) + ' ' + PLocalizer.Damage
            self.comboCounter['text'] = str(0)

        self.text.setAlphaScale(1.0)
        fadeOut = LerpFunctionInterval(self.text.setAlphaScale, fromData=1, toData=0, duration=1.0)
        self.faderOut = Sequence(fadeOut, Func(self.text.hide), Func(restoreColor))
        self.faderOut.start()
        return

    def __fadeOutBackstab(self):
        if self.backstabFaderIn:
            self.backstabFaderIn.pause()
            self.backstabFaderIn = None
        if self.backstabFaderOut:
            return
        self.backstabText.setAlphaScale(1.0)
        fadeOut = LerpFunctionInterval(self.backstabText.setAlphaScale, fromData=1, toData=0, duration=1.0)
        self.backstabFaderOut = Sequence(fadeOut, Func(self.backstabText.hide))
        self.backstabFaderOut.start()
        return