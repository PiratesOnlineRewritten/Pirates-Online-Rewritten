from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.task import Task
from pirates.ai import HolidayGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import EmoteGlobals
from pirates.economy import StoreGUI, AccessoriesStoreGUI, TattooStoreGUI, JewelryStoreGUI, BarberStoreGUI, SimpleStoreGUI
from pirates.chat.PChatInputSpeedChat import PChatInputSpeedChat
from pirates.chat.PChatInputEmote import PChatInputEmote
from pirates.piratesgui import PiratesGuiGlobals
from pirates.makeapirate import TattooGlobals
from pirates.makeapirate import ClothingGlobals
from pirates.makeapirate import JewelryGlobals
from pirates.makeapirate import BarberGlobals
from pirates.piratesbase import Freebooter
from pirates.world.LocationConstants import LocationIds
import random
import time
import re
messages = {0: PLocalizer.FullMoonWarning1,1: PLocalizer.FullMoonWarning2,2: PLocalizer.JollyRogerCurseComing,3: PLocalizer.JollyRogerCurseActive,4: PLocalizer.JollyRogerCurseIndoors,5: PLocalizer.JollyRogerCurseOutdoors,6: PLocalizer.JollyRogerCurseJail,7: PLocalizer.JollyRogerCurseEnd,8: PLocalizer.InvasionWarn30min,9: PLocalizer.InvasionWarn20min,10: PLocalizer.InvasionWarn10min,11: PLocalizer.InvasionWarn5min,12: PLocalizer.InvasionWarn1min,13: PLocalizer.InvasionWarn30min,14: PLocalizer.InvasionWarn20min,15: PLocalizer.InvasionWarn10min,16: PLocalizer.InvasionWarn5min,17: PLocalizer.InvasionWarn1min,18: PLocalizer.InvasionWarn30min,19: PLocalizer.InvasionWarn20min,20: PLocalizer.InvasionWarn10min,21: PLocalizer.InvasionWarn5min,22: PLocalizer.InvasionWarn1min}

class NewsManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.holidays = {}
        self.holidayIdList = []
        self.holidayEndTimes = {}
        self.noteablePathList = set()
        base.cr.newsManager = self
        localAvatar.chatMgr.emoteEntry.updateEmoteList()

    def delete(self):
        for holidayId in HolidayGlobals.getAllHolidayIds():
            taskMgr.remove('showHolidayMessage-holidayId:' + str(holidayId))

        if localAvatar and localAvatar.guiMgr and localAvatar.guiMgr.mapPage:
            for waypointId in self.noteablePathList:
                localAvatar.guiMgr.mapPage.removePath(waypointId)

        self.cr.newsManager = None
        DistributedObject.DistributedObject.delete(self)
        return

    def displayMessage(self, messageId):
        if not self.inNewsWorld():
            return
        message = None
        icon = icon = ('admin', '')
        if messageId < 30:
            message = messages.get(messageId)
            if isinstance(message, list):
                message = random.choice(message)
            if message:
                if messageId < 13:
                    location = PLocalizer.InvasionLocationPortRoyal
                elif messageId < 18:
                    location = PLocalizer.InvasionLocationTortuga
                else:
                    location = PLocalizer.InvasionLocationDelFuego
                if messageId <= 7:
                    pass
                else:
                    message = message % location
            icon = ('admin', '')
            if self.inTutorial(level=PiratesGlobals.TUT_GOT_COMPASS):
                return
        if messageId >= 30 and messageId < 50:
            message = PLocalizer.FleetHolidayMsgs.get(messageId)
            icon = ('ship', '')
        if messageId >= 50 and messageId < 60:
            message = PLocalizer.KrakenHolidayMsgs.get(messageId)
            icon = ('ship', '')
        if messageId >= 60 and messageId < 70:
            message = PLocalizer.QueenAnnesHolidayMsgs.get(messageId)
            icon = ('ship', '')
        if not message:
            return
        if isinstance(message, list):
            message = random.choice(message)
        base.localAvatar.guiMgr.messageStack.addModalTextMessage(message, seconds=45, priority=0, color=PiratesGuiGlobals.TextFG14, icon=icon, modelName='general_frame_f')
        base.talkAssistant.receiveGameMessage(message)
        return

    def playMusic(self, musicInfo):
        if musicInfo[-1] and not base.cr.getDo(musicInfo[-1]):
            return
        base.musicMgr.requestCurMusicFadeOut(duration=1)
        base.musicMgr.request(musicInfo[0], priority=2, looping=False)
        base.musicMgr.requestCurMusicFadeIn()

    def showHolidayMessage(self, holidayId, msgType):
        self.notify.debug('showHolidayMessage-holidayId:' + str(holidayId))
        taskMgr.remove('showHolidayMessage-holidayId:' + str(holidayId))
        if not hasattr(base, 'localAvatar'):
            return
        paidStatus = Freebooter.getPaidStatus(localAvatar.getDoId(), checkHoliday=False)
        if base.localAvatar.getTutorialState() < PiratesGlobals.TUT_MET_JOLLY_ROGER or self.inNewsWorld() == None:
            taskMgr.doMethodLater(15, self.showHolidayMessage, 'showHolidayMessage-holidayId:' + str(holidayId), extraArgs=[holidayId, msgType])
            return
        if msgType == 1:
            hours, minutes = self.getTimeRemaining(holidayId)
            message = HolidayGlobals.getHolidayStartMsg(holidayId, paidStatus)
            if message and re.findall('%\\(hours\\)s', message) and re.findall('%\\(minutes\\)s', message):
                message = message % {'hours': hours,'minutes': minutes}
            chatMessage = HolidayGlobals.getHolidayStartChatMsg(holidayId, paidStatus)
            if chatMessage and re.findall('%\\(hours\\)s', chatMessage) and re.findall('%\\(minutes\\)s', chatMessage):
                chatMessage = chatMessage % {'hours': hours,'minutes': minutes}
        elif msgType == 0:
            message = HolidayGlobals.getHolidayEndMsg(holidayId, paidStatus)
            chatMessage = HolidayGlobals.getHolidayEndChatMsg(holidayId, paidStatus)
        if message:
            base.localAvatar.guiMgr.messageStack.addModalTextMessage(message, seconds=45, priority=0, color=PiratesGuiGlobals.TextFG14, icon=(HolidayGlobals.getHolidayIcon(holidayId), ''), modelName='general_frame_f')
        if chatMessage:
            base.talkAssistant.receiveGameMessage(chatMessage)
        return

    def setHoliday(self, holidayId, value):
        self.holidays[holidayId] = value

    def getHoliday(self, holidayId):
        return self.holidays.get(holidayId)

    def getHolidayList(self):
        return self.holidays

    def getActiveHolidayList(self):
        return [ hId for hId in self.holidays if self.holidays[hId] ]

    def startHoliday(self, holidayId):
        if holidayId not in self.holidayIdList:
            self.notify.debug('setHolidayId: Starting Holiday %s' % holidayId)
            self.holidayIdList.append(holidayId)
            self.setHoliday(holidayId, 1)
            SimpleStoreGUI.SimpleStoreGUI.holidayIdList.append(holidayId)
            AccessoriesStoreGUI.AccessoriesStoreGUI.holidayIdList.append(holidayId)
            JewelryStoreGUI.JewelryStoreGUI.holidayIdList.append(holidayId)
            BarberStoreGUI.BarberStoreGUI.holidayIdList.append(holidayId)
            TattooStoreGUI.TattooStoreGUI.holidayIdList.append(holidayId)
            localAvatar.chatMgr.emoteEntry.updateEmoteList()
            self.showHolidayMessage(holidayId, 1)
            if holidayId == HolidayGlobals.JOLLYROGERCURSE:
                currentTime = base.cr.timeOfDayManager.getCurrentIngameTime()
                if currentTime > 18.0 or currentTime < 1.0:
                    self.displayMessage(3)
                else:
                    self.displayMessage(2)
            if holidayId == HolidayGlobals.ALLACCESSWEEKEND:
                Freebooter.setAllAccess(True)
                localAvatar.guiMgr.stashPrevPanel()
            if holidayId == HolidayGlobals.APRILFOOLS:
                messenger.send('moustacheFlip', [1])
            if holidayId == HolidayGlobals.HALFOFFCUSTOMIZATION:
                paidStatus = Freebooter.getPaidStatus(localAvatar.getDoId())
                if paidStatus:
                    self.divideAllAccessories(2)
            messenger.send('HolidayStarted', [HolidayGlobals.getHolidayName(holidayId)])

    def endHoliday(self, holidayId):
        if holidayId in self.holidayIdList:
            self.notify.debug('setHolidayId: Ending Holiday %s' % holidayId)
            self.holidayIdList.remove(holidayId)
            self.setHoliday(holidayId, 0)
            SimpleStoreGUI.SimpleStoreGUI.holidayIdList.remove(holidayId)
            AccessoriesStoreGUI.AccessoriesStoreGUI.holidayIdList.remove(holidayId)
            JewelryStoreGUI.JewelryStoreGUI.holidayIdList.remove(holidayId)
            BarberStoreGUI.BarberStoreGUI.holidayIdList.remove(holidayId)
            TattooStoreGUI.TattooStoreGUI.holidayIdList.remove(holidayId)
            localAvatar.chatMgr.emoteEntry.updateEmoteList()
            self.showHolidayMessage(holidayId, 0)
            if holidayId == HolidayGlobals.HALFOFFCUSTOMIZATION:
                paidStatus = Freebooter.getPaidStatus(localAvatar.getDoId())
                if paidStatus:
                    self.multiplyAllAccessories(2)
            if holidayId == HolidayGlobals.ALLACCESSWEEKEND:
                Freebooter.setAllAccess(False)
            if holidayId == HolidayGlobals.APRILFOOLS:
                messenger.send('moustacheFlip', [0])
            messenger.send('HolidayEnded', [HolidayGlobals.getHolidayName(holidayId)])

    def setHolidayIdList(self, holidayIdArray):
        holidayIdList = []
        for hid in holidayIdArray:
            if hid[0] != None:
                holidayIdList.append(hid[0])
            self.holidayEndTimes[hid[0]] = hid[1]

        def isEnding(id):
            return id not in holidayIdList

        def isStarting(id):
            return id not in self.holidayIdList

        toEnd = filter(isEnding, self.holidayIdList)
        for endingHolidayId in toEnd:
            self.endHoliday(endingHolidayId)

        toStart = filter(isStarting, holidayIdList)
        for startingHolidayId in toStart:
            self.startHoliday(startingHolidayId)

        messenger.send('setHolidayIdList', [holidayIdList])
        return

    def getHolidayIdList(self):
        return self.holidayIdList

    def holidayNotify(self):
        pass

    def inTutorial(self, level=PiratesGlobals.TUT_CHAPTER3_STARTED):
        if base.localAvatar.getTutorialState() <= level:
            return True
        else:
            return False

    def inNewsWorld(self):
        w = base.localAvatar.getWorld()
        if not w:
            return
        ourInstance = w.type
        if ourInstance == None:
            return
        for iType in PiratesGlobals.INSTANCE_NO_NEWS_MESSAGES:
            if ourInstance == iType:
                return False

        return True

    def getTimeRemaining(self, holidayId):
        t = self.holidayEndTimes.get(holidayId, -1)
        if t == -1:
            return [
             0, 0]
        t = int(t)
        epochNow = int(time.time())
        epochRemain = t - epochNow
        minutesTotal, seconds = divmod(epochRemain, 60)
        hours, minutes = divmod(minutesTotal, 60)
        return [
         hours, minutes]

    def displayHolidayStatus(self):
        anyMessages = False
        paidStatus = Freebooter.getPaidStatus(localAvatar.getDoId())
        for holidayId in self.holidayIdList:
            h, m = self.getTimeRemaining(holidayId)
            message = HolidayGlobals.getHolidayStatusMsg(holidayId, paidStatus)
            if message:
                anyMessages = True
                try:
                    base.talkAssistant.receiveGameMessage(message % (h, m))
                except TypeError:
                    base.talkAssistant.receiveGameMessage(message)

        if not anyMessages:
            base.talkAssistant.receiveGameMessage(PLocalizer.NO_CURRENT_HOLIDAYS)
            return

    def setNoteablePathList(self, newPathList):
        if localAvatar and localAvatar.guiMgr and localAvatar.guiMgr.mapPage:
            for pathInfo in self.noteablePathList:
                localAvatar.guiMgr.mapPage.removePath(pathInfo)

            self.noteablePathList = newPathList
            for pathInfo in self.noteablePathList:
                localAvatar.guiMgr.mapPage.addPath(pathInfo)

    def divideTattooPrices(self, divisor):
        for k, v in TattooGlobals.tattoos.iteritems():
            currentPrice = v[4]
            newPrice = int(currentPrice / divisor)
            TattooGlobals.tattoos[k][4] = newPrice

    def divideClothingPrices(self, divisor):
        for k, v in ClothingGlobals.UNIQUE_ID.iteritems():
            currentPrice = v[5]
            newPrice = int(currentPrice / divisor)
            ClothingGlobals.UNIQUE_ID[k][5] = newPrice

    def divideJewelryPrices(self, divisor):
        for k, v in JewelryGlobals.jewelry_id.iteritems():
            currentPrice = v[3]
            newPrice = int(currentPrice / divisor)
            JewelryGlobals.jewelry_id[k][3] = newPrice

    def divideBarberPrices(self, divisor):
        for k, v in BarberGlobals.barber_id.iteritems():
            currentPrice = v[4]
            newPrice = int(currentPrice / divisor)
            BarberGlobals.barber_id[k][4] = newPrice

    def multiplyTattooPrices(self, factor):
        for k, v in TattooGlobals.tattoos.iteritems():
            currentPrice = v[4]
            newPrice = int(currentPrice * factor)
            TattooGlobals.tattoos[k][4] = newPrice

    def multiplyClothingPrices(self, factor):
        for k, v in ClothingGlobals.UNIQUE_ID.iteritems():
            currentPrice = v[5]
            newPrice = int(currentPrice * factor)
            ClothingGlobals.UNIQUE_ID[k][5] = newPrice

    def multiplyJewelryPrices(self, factor):
        for k, v in JewelryGlobals.jewelry_id.iteritems():
            currentPrice = v[3]
            newPrice = int(currentPrice * factor)
            JewelryGlobals.jewelry_id[k][3] = newPrice

    def multiplyBarberPrices(self, factor):
        for k, v in BarberGlobals.barber_id.iteritems():
            currentPrice = v[4]
            newPrice = int(currentPrice * factor)
            BarberGlobals.barber_id[k][4] = newPrice

    def divideAllAccessories(self, divisor):
        self.divideTattooPrices(divisor)
        self.divideClothingPrices(divisor)
        self.divideJewelryPrices(divisor)
        self.divideBarberPrices(divisor)

    def multiplyAllAccessories(self, factor):
        self.multiplyTattooPrices(factor)
        self.multiplyClothingPrices(factor)
        self.multiplyJewelryPrices(factor)
        self.multiplyBarberPrices(factor)
