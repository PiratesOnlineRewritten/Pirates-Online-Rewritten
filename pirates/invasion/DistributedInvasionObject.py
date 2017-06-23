from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.distributed import DistributedObject
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.gui.DirectGui import *
from direct.distributed.GridChild import GridChild
from pirates.audio import SoundGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import EmoteGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.ai import HolidayGlobals
from pirates.world.LocationConstants import LocationIds
from pirates.piratesbase import PLocalizer
from pirates.effects.DarkShipFog import DarkShipFog
from pirates.effects.LightningStrike import LightningStrike
from pirates.invasion import InvasionGlobals
from pirates.map.MinimapObject import GridMinimapObject
from pirates.piratesgui.GameOptions import Options
from pirates.effects.PooledEffect import PooledEffect
import copy
import random

class DistributedInvasionObject(DistributedObject.DistributedObject, GridChild):
    notify = directNotify.newCategory('DistributedInvasionObject')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        GridChild.__init__(self)
        self.currentPhase = -1
        self.canPlaySfx = False
        self.capturePointNodes = None
        self.parentObj = None
        self.brigadeText = None
        self.invasionShip = None
        self.shipNode = None
        self.shipShowingIval = None
        self.shipHidingIval = None
        self.lerpFogIval = None
        self.minimapObjs = {}
        self.endPos = None
        self.fogStarted = False
        self.lightingEffects = []
        self.cleanedUp = False
        return

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.notify.debug('generate')

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.parentObj = self.getParentObj()
        self.linearFog = Fog('LinearInvasionFog')
        localAvatar.b_setInInvasion(True)
        base.options.setInvasion(True)
        PooledEffect.setGlobalLimit(20)
        messenger.send('grid-detail-changed', [Options.option_low])
        base.options.setRuntimeSpecialEffects()
        base.setNoticeSystem(0)
        islandMusic = SoundGlobals.getMainMusic(self.parentObj.uniqueId)
        if islandMusic:
            base.musicMgr.requestFadeOut(islandMusic)
        base.musicMgr.request(SoundGlobals.MUSIC_TORMENTA, looping=True)
        numCapturePoints = InvasionGlobals.getTotalCapturePoints(self.holidayId)
        if base.launcher.getPhaseComplete(5):
            self.canPlaySfx = True
        else:
            self.canPlaySfx = False
        self.cleanedUp = False

    def cleanup(self):
        localAvatar.b_setInInvasion(False)
        base.options.setInvasion(False)
        PooledEffect.setGlobalLimit(200)
        messenger.send('grid-detail-changed', [base.options.terrain_detail_level])
        base.options.setRuntimeSpecialEffects()
        render.clearFog()
        base.setNoticeSystem(1)
        if not localAvatar.belongsInJail():
            base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_TORMENTA)
            base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_TORMENTA_COMBAT)
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_INVASION_VICTORY)
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_INVASION_DEFEAT)
        if not self.cleanedUp:
            islandMusic = SoundGlobals.getMainMusic(self.parentObj.uniqueId)
            if islandMusic and not localAvatar.belongsInJail():
                base.musicMgr.request(islandMusic, priority=-1, volume=0.6)
        for minimapObj in self.minimapObjs.values():
            minimapObj.destroy()

        self.minimapObjs = {}
        if self.brigadeText:
            self.brigadeText.destroy()
            self.brigadeText = None
        if self.shipShowingIval:
            self.shipShowingIval.pause()
            self.shipShowingIval = None
        if self.shipHidingIval:
            self.shipHidingIval.pause()
            self.shipHidingIval = None
        if self.lerpFogIval:
            self.lerpFogIval.pause()
            self.lerpFogIval = None
        self.stopLightingEffects()
        taskMgr.remove('invasionWinCheer')
        if self.invasionShip:
            self.invasionShip.destroy()
            self.invasionShip = None
        if self.shipNode:
            self.shipNode.removeNode()
            self.shipNode = None
        self.cleanedUp = True
        return

    def disable(self):
        self.cleanup()
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        self.cleanup()
        self.holidayId = None
        self.holidayName = None
        GridChild.delete(self)
        DistributedObject.DistributedObject.delete(self)
        return

    def setHolidayId(self, holidayId):
        self.holidayId = HolidayGlobals.getHolidayClass(holidayId)
        self.holidayName = HolidayGlobals.getHolidayName(self.holidayId)
        self.totalPhases = InvasionGlobals.getTotalPhases(self.holidayId)
        self.mainZone = InvasionGlobals.getTotalCapturePoints(self.holidayId)

    def setNextPhase(self, phase, message):
        self.currentPhase = phase
        self.notify.debug('setting next phase of invasion to %s' % self.currentPhase)
        text = PLocalizer.InvasionJollyRogerNextBrigade % (self.currentPhase, self.totalPhases - self.currentPhase)
        base.localAvatar.guiMgr.messageStack.addModalTextMessage(text, seconds=10, priority=0, color=PiratesGuiGlobals.TextFG14, icon=(HolidayGlobals.getHolidayIcon(self.holidayId), ''), modelName='general_frame_f')
        if self.brigadeText:
            self.brigadeText['text'] = PLocalizer.InvasionJollyRogerBrigadeUpdate % (self.currentPhase, self.totalPhases - self.currentPhase)
        if self.canPlaySfx:
            if self.currentPhase == 1:
                sfx = self.startMessages[message]
            elif self.currentPhase == 2:
                sfx = self.secondWaveMessages[message]
            elif self.currentPhase == 7:
                sfx = self.lastWaveMessages[message]
            else:
                sfx = self.waveMessages[message]
            base.playSfx(sfx)

    def setPlayerWin(self, value, message):
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_TORMENTA)
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_TORMENTA_COMBAT)
        for minimapObj in self.minimapObjs.values():
            minimapObj.destroy()

        if value:
            base.musicMgr.request(SoundGlobals.MUSIC_INVASION_VICTORY, looping=False)
            taskMgr.doMethodLater(random.random(), self.invasionWinCheer, 'invasionWinCheer')
            text, sfx = self.winMessages[message]
        else:
            base.musicMgr.request(SoundGlobals.MUSIC_INVASION_DEFEAT, looping=False)
            text, sfx = self.loseMessages[message]
        if self.brigadeText:
            self.brigadeText.destroy()
            self.brigadeText = None
        text = PLocalizer.JollySays % text
        base.localAvatar.guiMgr.messageStack.addModalTextMessage(text, seconds=8, priority=0, color=PiratesGuiGlobals.TextFG14, icon=('jolly',
                                                                                                                                      ''), modelName='general_frame_f')
        if self.canPlaySfx:
            base.playSfx(sfx)
        return

    def invasionWinCheer(self, task=None):
        localAvatar.requestEmote(EmoteGlobals.EMOTE_CHEER)

    def updateCapturePoints(self, capturePoints):
        if self.parentObj and self.parentObj.minimap and not self.parentObj.minimapArea:
            for cp in capturePoints:
                capturePoint = self.parentObj.minimap.getCapturePoint(self.holidayName, cp[0])
                if capturePoint:
                    needToStash = capturePoint.setHp(cp[1], cp[2])
                    if needToStash:
                        self.parentObj.findAllMatches('**/=Zone=%s;+s' % (cp[0],)).stash()

    def removeCapturePoint(self, zone):
        localAvatar.guiMgr.createProgressMsg(PLocalizer.CapturePointDestroyed % PLocalizer.CapturePointNames[self.holidayName][zone], PiratesGuiGlobals.TextFG2)

    def sendAttackMessage(self, zone, capturePointId):
        capturePoint = self.cr.doId2do.get(capturePointId)
        if capturePoint and capturePoint.hpMeter:
            return
        localAvatar.guiMgr.createProgressMsg(PLocalizer.CapturePointAttacked % PLocalizer.CapturePointNames[self.holidayName][zone], PiratesGuiGlobals.TextFG2)

    def sendLowHealthMessage(self, zone, message):
        if zone == self.mainZone:
            text, sfx = self.mainZoneMessages[message]
            text = PLocalizer.JollySays % text
            base.localAvatar.guiMgr.messageStack.addModalTextMessage(text, seconds=8, priority=0, color=PiratesGuiGlobals.TextFG14, icon=('jolly',
                                                                                                                                          ''), modelName='general_frame_f')
            if self.canPlaySfx:
                base.playSfx(sfx)
        localAvatar.guiMgr.createProgressMsg(PLocalizer.CapturePointLowHealth % PLocalizer.CapturePointNames[self.holidayName][zone], PiratesGuiGlobals.TextFG2)

    def sendBossMessage(self, message, good):
        if good:
            text, sfx = self.goodBossMessages[message]
        else:
            text, sfx = self.badBossMessages[message]
        text = PLocalizer.JollySays % text
        base.localAvatar.guiMgr.messageStack.addModalTextMessage(text, seconds=8, priority=0, color=PiratesGuiGlobals.TextFG14, icon=('jolly',
                                                                                                                                      ''), modelName='general_frame_f')
        if self.canPlaySfx:
            base.playSfx(sfx)
        localAvatar.guiMgr.createProgressMsg(PLocalizer.InvasionJollyRogerComing % PLocalizer.getInvasionMainZoneName(self.holidayName), PiratesGuiGlobals.TextFG2)

    def updateNPCMinimaps(self, npcList):
        self.updateBrigadeText()
        if self.parentObj and self.parentObj.minimap and not self.parentObj.minimapArea:
            minimapObjs = {}
            for npcInfo in npcList:
                minimapObj = self.minimapObjs.pop(npcInfo[0], None)
                if not minimapObj:
                    minimapObj = MinimapInvasionObject(self.parentObj, npcInfo[0], npcInfo[1], npcInfo[2], npcInfo[3])
                else:
                    minimapObj.updatePos(npcInfo[1], npcInfo[2])
                minimapObjs[npcInfo[0]] = minimapObj

            for id in self.minimapObjs.keys():
                minimapObj = self.minimapObjs.pop(id)
                minimapObj.destroy()
                minimapObj = None

            self.minimapObjs = None
            self.minimapObjs = minimapObjs
        return

    def spawnShip(self, shipClass, startPosHpr, midPosHpr, endPosHpr):
        pass

    def placeShip(self, shipClass, midPosHpr, endPosHpr):
        pass

    def hideShip(self):
        pass

    def startMainFog(self, lerp=True):
        self.fogStarted = True
        fogColor = InvasionGlobals.getFogColor(self.holidayId)
        render.clearFog()
        render.setFog(self.linearFog)
        self.linearFog.setColor(fogColor)
        fogRanges = InvasionGlobals.getFogRange(self.holidayId)
        if lerp:
            fogOnset = fogRanges[0]
            fogPeak = fogRanges[1]
            farFogRanges = InvasionGlobals.getFarFogRange(self.holidayId)
            self.currFogOnset = farFogRanges[0]
            self.currFogPeak = farFogRanges[1]
            self.linearFog.setLinearRange(self.currFogOnset, self.currFogPeak)
            self.lerpLinearFog(fogOnset, fogPeak, 10.0)
        else:
            self.currFogOnset = fogRanges[0]
            self.currFogPeak = fogRanges[1]
            self.linearFog.setLinearRange(self.currFogOnset, self.currFogPeak)
        base.farCull.setPos(0, self.currFogPeak + 10, 0)
        base.backgroundDrawable.setClearColor(fogColor)

    def stopMainFog(self):
        if self.fogStarted:
            fogRanges = InvasionGlobals.getFarFogRange(self.holidayId)
            fogOnset = fogRanges[0]
            fogPeak = fogRanges[1]
            self.lerpLinearFog(fogOnset, fogPeak, 10.0)

    def lerpLinearFog(self, targetOnset, targetPeak, lerpTime=1.0):
        if self.lerpFogIval:
            self.lerpFogIval.pause()
        baseOnset = self.currFogOnset
        basePeak = self.currFogPeak

        def setLinearFog(v):
            self.currFogOnset = baseOnset * (1 - v) + targetOnset * v
            self.currFogPeak = basePeak * (1 - v) + targetPeak * v
            base.farCull.setPos(0, self.currFogPeak + 10, 0)
            self.linearFog.setLinearRange(self.currFogOnset, self.currFogPeak)

        self.lerpFogIval = LerpFunctionInterval(setLinearFog, duration=lerpTime, fromData=0.0, toData=1.0, name='LerpFogIval')
        self.lerpFogIval.start()

    def startDarkFog(self, pos):
        self.fogEffect = DarkShipFog.getEffect()
        if self.fogEffect:
            self.fogEffect.reparentTo(self.getParentObj())
            self.fogEffect.setPos(pos)
            self.fogEffect.setY(self.fogEffect, 80)
            self.fogEffect.setZ(self.fogEffect, 50)
            self.fogEffect.startLoop()

    def stopDarkFog(self):
        if self.fogEffect:
            self.fogEffect.stopLoop()
            self.fogEffect = None
        return

    def startLightingEffects(self, pos):
        self.lightingEffects = []
        stormSequence = Sequence(Wait(5.0))
        for i in range(4):
            lighting = LightningStrike.getEffect(unlimited=True)
            if lighting:
                randomOffset = Point3(random.randint(-20, 20), random.randint(-20, 20), random.randint(-20, 20))
                lighting.reparentTo(self.getParentObj())
                lighting.setPos(Point3(pos) + randomOffset)
                lighting.setScale(5.0)
                lighting.fadeColor = Vec4(0.8, 1, 0.1, 1)
                self.lightingEffects.append(lighting)
                stormSequence.append(Wait(random.randint(5, 15) / 10.0))
                stormSequence.append(Func(lighting.play))

        return stormSequence

    def stopLightingEffects(self):
        for lighting in self.lightingEffects:
            lighting.cleanUpEffect()

        self.lightingEffects = []


class MinimapInvasionObject(DirectObject):
    ICON = None
    BOSS_ICON = None
    BOSS_SORT = 5

    def __init__(self, parent, avId, xPos, yPos, isBoss):
        name = 'MinimapInvasionObject-%s' % avId
        self.worldNode = parent.attachNewNode(name)
        self.worldNode.setPos(xPos, yPos, 0)
        if isBoss and not MinimapInvasionObject.BOSS_ICON:
            gui = loader.loadModel('models/effects/effectCards')
            MinimapInvasionObject.BOSS_ICON = gui.find('**/effectJolly')
            MinimapInvasionObject.BOSS_ICON.clearTransform()
            MinimapInvasionObject.BOSS_ICON.setHpr(180, 90, 0)
            MinimapInvasionObject.BOSS_ICON.setScale(100)
            MinimapInvasionObject.BOSS_ICON.flattenStrong()
        elif not MinimapInvasionObject.ICON:
            gui = loader.loadModel('models/gui/compass_main')
            MinimapInvasionObject.ICON = gui.find('**/icon_sphere')
            MinimapInvasionObject.ICON.clearTransform()
            MinimapInvasionObject.ICON.setHpr(90, 90, 0)
            MinimapInvasionObject.ICON.setScale(200)
            MinimapInvasionObject.ICON.setColor(1, 0, 0, 1)
            MinimapInvasionObject.ICON.flattenStrong()
        if isBoss:
            self.minimapObj = GridMinimapObject(name, self.worldNode, MinimapInvasionObject.BOSS_ICON)
            self.minimapObj.mapGeom.setBin('gui-fixed', 1)
        else:
            self.minimapObj = GridMinimapObject(name, self.worldNode, MinimapInvasionObject.ICON)
        self.accept('transferMinimapObjects', self.transferMinimapObject)
        parent.minimap.addObject(self.minimapObj)
        self.moveIval = None
        return

    def transferMinimapObject(self, guiMgr):
        guiMgr.transferMinimapObject(self.minimapObj)

    def destroy(self):
        self.ignore('transferMinimapObjects')
        if self.minimapObj:
            self.minimapObj.removeFromMap()
        self.minimapObj = None
        if self.worldNode:
            self.worldNode.removeNode()
        self.worldNode = None
        if self.moveIval:
            self.moveIval.finish()
        self.moveIval = None
        return

    def updatePos(self, xPos, yPos):
        if self.moveIval:
            self.moveIval.finish()
            self.moveIval = None
        self.moveIval = LerpPosInterval(self.worldNode, 1.5, Point3(xPos, yPos, 0))
        self.moveIval.start()
        return