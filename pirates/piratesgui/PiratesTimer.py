from otp.otpbase import OTPTimer
from direct.showbase.ShowBaseGlobal import *
from direct.task import Task
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiButton
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import time

class PiratesTimer(OTPTimer.OTPTimer):
    BGImage = None

    def __init__(self, showMinutes=0, mode=None, titleText='', titleFg=None, infoText='', cancelText='', cancelCallback=None, alarmTime=0):
        self.showMinutes = showMinutes
        self.mode = mode
        OTPTimer.OTPTimer.__init__(self)
        self['text_pos'] = (0, 0)
        self['text_font'] = PiratesGlobals.getPirateOutlineFont()
        self['text'] = ''
        self.setFontColor(PiratesGuiGlobals.TextFG8)
        self.initialiseoptions(PiratesTimer)
        self.loadDials()
        self.setScale(1)
        self.alarmTime = alarmTime
        self.dialInterval = None
        self.alarmInterval = None
        self.alarmStarted = None
        if self.alarmTime > 0:
            self.alarmSfx = loadSfx(SoundGlobals.SFX_GUI_ALARM)
            self.outOfTimeSfx = loadSfx(SoundGlobals.SFX_GUI_OUT_OF_TIME)
        if titleText or infoText:
            self.createTimerText(titleText, titleFg, infoText)
        if cancelCallback:
            self.createCancelButton(cancelCallback, cancelText)
        self.slide = False
        self.end = False
        return

    def destroy(self):
        self.stopAlarm()
        self.stopDial()
        OTPTimer.OTPTimer.destroy(self)

    def getImage(self):
        return None

    def loadDials(self):
        model = loader.loadModel('models/gui/gui_timer')
        model.setScale(0.2)
        model.flattenLight()
        PiratesTimer.ClockImage = model.find('**/timer_front')
        PiratesTimer.BGImage = model.find('**/timer_back')
        model.removeNode()
        self.bgDial = DirectFrame(parent=self, state=DGG.DISABLED, relief=None, image=self.BGImage)
        self.fgLabel = DirectLabel(parent=self, state=DGG.DISABLED, relief=None, image=self.ClockImage, image_pos=(-0.01,
                                                                                                                   0,
                                                                                                                   0.035), image_scale=(1.1,
                                                                                                                                        1,
                                                                                                                                        0.8), text_scale=0.07, text_align=TextNode.ACenter, text_font=PiratesGlobals.getPirateOutlineFont())
        return

    def setTime(self, currTime):
        if currTime < 0:
            currTime = 0
        if self.slide:
            elapsedTime = self.getElapsedTime()
            if elapsedTime <= self.startTime:
                self.setPos(self.startPosition)
            if elapsedTime > self.startTime:
                if elapsedTime < self.endTime:
                    duration = self.endTime - self.startTime
                    delta_time = self.getElapsedTime() - self.startTime
                    t = delta_time / duration
                    delta = self.endPosition - self.startPosition
                    self.setPos(self.startPosition + delta * t)
                if elapsedTime >= self.endTime:
                    self.setPos(self.endPosition)
            if currTime == self.currentTime:
                return
            self.currentTime = currTime
            if currTime >= 60 and self.showMinutes:
                t = time.gmtime(currTime)
                timeStr = '%s:%s' % (t[4], str(t[5]).zfill(2))
            else:
                timeStr = str(currTime)
                self.fgLabel['text_scale'] = 0.07
            timeStrLen = len(timeStr)
            if 0 >= currTime < self.alarmTime:
                fgColor = Vec4(0.9, 0.1, 0.1, 1)
                self.alarmStarted or self.startAlarm()
        else:
            fgColor = self.vFontColor
        if timeStrLen == 1:
            self.setTimeStr(timeStr, 0.09, (0, -0.02), fgColor)
        elif timeStrLen == 2:
            self.setTimeStr(timeStr, 0.08, (0, -0.015))
        elif timeStrLen == 3:
            self.setTimeStr(timeStr, 0.08, (0, -0.015))
        else:
            self.setTimeStr(timeStr, 0.07, (0, -0.012))

    def setTimeStr(self, timeStr, scale=0.08, pos=(0, -0.015), fg=None):
        self.fgLabel['text'] = ''
        self.fgLabel['text_fg'] = fg or self.vFontColor
        self.fgLabel['text_scale'] = scale
        self.fgLabel['text_pos'] = pos
        self.fgLabel['text'] = timeStr

    def countdown(self, duration, callback=None):
        OTPTimer.OTPTimer.countdown(self, duration, callback)
        self.fgLabel['text_font'] = PiratesGlobals.getInterfaceFont()
        self.fgLabel['text_scale'] = 0.07
        self.startDial()

    def timerExpired(self):
        self.stop()
        self.stopDial()
        if self.alarmTime > 0:
            base.playSfx(self.outOfTimeSfx)
        self.stopAlarm()

    def createTimerText(self, titleText, titleFg, infoText):
        self.titleText = DirectFrame(parent=self, state=DGG.DISABLED, relief=None, text=titleText, text_align=TextNode.ACenter, text_scale=0.05, text_fg=titleFg, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), textMayChange=1, text_wordwrap=6, pos=(0,
                                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                                    0.7))
        self.infoText = DirectFrame(parent=self, state=DGG.DISABLED, relief=None, text=infoText, text_align=TextNode.ACenter, text_scale=0.14, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), textMayChange=1, text_wordwrap=6, pos=(0, 0, -0.75))
        return

    def createCancelButton(self, cancelCallback, cancelText):
        if self.mode != PiratesGlobals.HIGHSEAS_ADV_WAIT:
            return
        if not base.localAvatar.isCrewCaptain():
            return
        self.cancelButton = GuiButton.GuiButton(parent=self, helpText=cancelText, command=cancelCallback, borderWidth=PiratesGuiGlobals.BorderWidth, text=PLocalizer.Cancel, frameColor=PiratesGuiGlobals.ButtonColor3, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0,
                                                                                                                                                                                                                                                                     0.015), frameSize=(-0.09, 0.09, -0.015, 0.065), text_scale=PiratesGuiGlobals.TextScaleLarge, pad=(0.01,
                                                                                                                                                                                                                                                                                                                                                                       0.01), pos=(0,
                                                                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                                                                   -1.55), scale=2.3)

    def startDial(self, t=6):
        if self.dialInterval:
            self.dialInterval.pause()
            self.dialInterval = None
        self.dialInterval = LerpHprInterval(self.bgDial, t, Vec3(0, 0, 360), Vec3(0, 0, 0))
        self.dialInterval.loop()
        return

    def stopDial(self):
        if self.dialInterval:
            self.dialInterval.pause()
            self.dialInterval = None
        return

    def startAlarm(self):
        if self.end == False:
            self.alarmStarted = 1
            origScale = self.getScale()
            scale = origScale * 1.2
            t = 0.5
            self.alarmInterval = Sequence(Parallel(SoundInterval(self.alarmSfx), LerpScaleInterval(self, t, scale, origScale, blendType='noBlend')), Parallel(SoundInterval(self.alarmSfx), LerpScaleInterval(self, t, origScale, scale, blendType='noBlend')))
            self.alarmInterval.loop()
            self.startDial(t=2)

    def stopAlarm(self):
        self.alarmStarted = 0
        if self.alarmInterval:
            self.alarmInterval.pause()
            self.alarmInterval = None
        self.end = True
        return

    def setSlide(self, startTime, endTime, startPosition, endPosition):
        self.slide = True
        self.startTime = startTime
        self.endTime = endTime
        self.startPosition = startPosition
        self.endPosition = endPosition