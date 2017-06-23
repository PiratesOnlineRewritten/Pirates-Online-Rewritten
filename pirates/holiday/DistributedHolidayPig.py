from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.uberdog.RejectCode import RejectCode
from pirates.holiday.DistributedHolidayObject import DistributedHolidayObject
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.effects.SmallFire import SmallFire
from pirates.ai import HolidayGlobals

class DistributedHolidayPig(DistributedHolidayObject):

    def __init__(self, cr):
        holiday = None
        proximityText = ''
        if base.cr.newsManager.getHoliday(HolidayGlobals.FOUNDERSFEAST):
            holiday = HolidayGlobals.FOUNDERSFEAST
        elif base.cr.newsManager.getHoliday(HolidayGlobals.MARDIGRAS):
            holiday = HolidayGlobals.MARDIGRAS
        holidayMsgs = PLocalizer.holidayMessages.get(holiday)
        if holidayMsgs:
            proximityText = holidayMsgs.get(HolidayGlobals.MSG_PIG)
        DistributedHolidayObject.__init__(self, cr, proximityText=proximityText)
        self.pigRoasting = False
        self.fireEffect = None
        self.pigInterval = None
        self.pigModel = None
        return

    def delete(self):
        if self.pigInterval:
            self.pigInterval.finish()
            self.pigInterval = None
        if self.pigModel:
            self.pigModel.removeNode()
        if self.fireEffect:
            self.fireEffect.stopLoop()
            self.fireEffect = None
        DistributedHolidayObject.delete(self)
        return

    def setPigRoasting(self, value=False):
        self.pigRoasting = value
        if self.pigRoasting:
            self.startRoastingPig()
        else:
            self.stopRoastingPig()

    def getPigRoasting(self):
        return self.pigRoasting

    def acceptInteraction(self):
        DistributedHolidayObject.acceptInteraction(self)
        base.cr.interactionMgr.stop()

    def rejectInteraction(self):
        DistributedHolidayObject.rejectInteraction(self)
        localAvatar.guiMgr.createWarning(PLocalizer.NoPigRoasting)

    def startRoastingPig(self):
        if not self.pigModel:
            self.pigModel = loader.loadModel('models/props/pir_m_prp_foo_barbecuepig')
            self.pigModel.setTransparency(1)
            self.pigModel.reparentTo(self)
        self.pigInterval = LerpColorScaleInterval(self.pigModel, 2.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0))
        self.fireEffect = SmallFire()
        if self.fireEffect:
            self.fireEffect.reparentTo(self)
            self.fireEffect.setScale(Vec3(1.5, 1, 1))
            self.fireEffect.startLoop()
        self.pigInterval.start()

    def stopRoastingPig(self):
        if self.pigModel:
            self.pigInterval = LerpColorScaleInterval(self.pigModel, 2.0, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1))
            self.pigInterval.start()
        if self.fireEffect:
            self.fireEffect.stopLoop()
            self.fireEffect = None
        return

    def makeTradeResponse(self, result):
        if result == 0:
            localAvatar.guiMgr.createWarning(PLocalizer.TradeItemFullWarning, PiratesGuiGlobals.TextFG6)
        elif result == 1:
            holiday = None
            if base.cr.newsManager.getHoliday(HolidayGlobals.FOUNDERSFEAST):
                holiday = HolidayGlobals.FOUNDERSFEAST
            elif base.cr.newsManager.getHoliday(HolidayGlobals.MARDIGRAS):
                holiday = HolidayGlobals.MARDIGRAS
            holidayMsgs = PLocalizer.holidayMessages.get(holiday)
            if holidayMsgs:
                localAvatar.guiMgr.messageStack.addModalTextMessage(holidayMsgs.get(HolidayGlobals.MSG_PORK_RECEIVED), seconds=10, icon=('pork',
                                                                                                                                         ''))
            localAvatar.guiMgr.combatTray.tonicButton.getBestTonic()
            localAvatar.guiMgr.weaponPage.refreshList()
        else:
            localAvatar.guiMgr.createWarning(PLocalizer.TradeFailedWarning, PiratesGuiGlobals.TextFG6)
        base.cr.interactionMgr.start()
        self.refreshState()
        return