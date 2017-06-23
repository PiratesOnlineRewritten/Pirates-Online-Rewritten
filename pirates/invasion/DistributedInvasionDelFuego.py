from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pirates.ai import HolidayGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
from pirates.invasion import DistributedInvasionObject
from pirates.ship import ShipGlobals
import copy
import random

class DistributedInvasionDelFuego(DistributedInvasionObject.DistributedInvasionObject):
    notify = directNotify.newCategory('DistributedInvasionDelFuego')

    def __init__(self, cr):
        DistributedInvasionObject.DistributedInvasionObject.__init__(self, cr)
        self.setHolidayId(HolidayGlobals.INVASIONDELFUEGO)

    def announceGenerate(self):
        DistributedInvasionObject.DistributedInvasionObject.announceGenerate(self)
        if self.canPlaySfx:
            self.startMessages = [
             loadSfx(SoundGlobals.SFX_MONSTER_JR_FORWARD_ATTACK)]
            self.secondWaveMessages = [
             loadSfx(SoundGlobals.SFX_MONSTER_JR_NEXT_BRIGADE)]
            self.waveMessages = [
             loadSfx(SoundGlobals.SFX_MONSTER_JR_BREAK), loadSfx(SoundGlobals.SFX_MONSTER_JR_TONIGHT), loadSfx(SoundGlobals.SFX_MONSTER_JR_NOT_BAD), loadSfx(SoundGlobals.SFX_MONSTER_JR_ACCEPT), loadSfx(SoundGlobals.SFX_MONSTER_JR_HOWS_THIS), loadSfx(SoundGlobals.SFX_MONSTER_JR_RIP), loadSfx(SoundGlobals.SFX_MONSTER_JR_FIGHT), loadSfx(SoundGlobals.SFX_MONSTER_JR_BRING), loadSfx(SoundGlobals.SFX_MONSTER_JR_ITCHING_TO_FIGHT), loadSfx(SoundGlobals.SFX_MONSTER_JR_FORWARD), loadSfx(SoundGlobals.SFX_MONSTER_JR_SPINELESS_FOOLS), loadSfx(SoundGlobals.SFX_MONSTER_JR_STORM_THE_BEACHES), loadSfx(SoundGlobals.SFX_MONSTER_JR_FIGHT_ON), loadSfx(SoundGlobals.SFX_MONSTER_JR_FEAST_SOULS), loadSfx(SoundGlobals.SFX_MONSTER_JR_FASTER_YOU_SCABS), loadSfx(SoundGlobals.SFX_MONSTER_JR_DISPATCH), loadSfx(SoundGlobals.SFX_MONSTER_JR_DESTROY_EVERYTHING), loadSfx(SoundGlobals.SFX_MONSTER_JR_BEG_MERCY), loadSfx(SoundGlobals.SFX_MONSTER_JR_BARRICADES_A), loadSfx(SoundGlobals.SFX_MONSTER_JR_ATTACK_THE_TOWN), loadSfx(SoundGlobals.SFX_MONSTER_JR_ATTACK), loadSfx(SoundGlobals.SFX_MONSTER_JR_RUBBLE), loadSfx(SoundGlobals.SFX_MONSTER_JR_CRABS)]
            self.lastWaveMessages = [
             loadSfx(SoundGlobals.SFX_MONSTER_JR_STAND)]
            self.goodBossMessages = [
             (
              PLocalizer.InvasionJollyRogerBoss1, loadSfx(SoundGlobals.SFX_MONSTER_JR_NO_TIME)), (PLocalizer.InvasionJollyRogerBoss3, loadSfx(SoundGlobals.SFX_MONSTER_JR_USELESS_SCABS)), (PLocalizer.InvasionJollyRogerBoss4, loadSfx(SoundGlobals.SFX_MONSTER_JR_FOOLS)), (PLocalizer.InvasionJollyRogerBoss5, loadSfx(SoundGlobals.SFX_MONSTER_JR_FOLLOW_ME_NOW))]
            self.badBossMessages = [
             (
              PLocalizer.InvasionJollyRogerBoss2, loadSfx(SoundGlobals.SFX_MONSTER_JR_NO_MERCY))]
            self.mainZoneMessages = [
             (
              PLocalizer.InvasionJollyRogerMainZone1, loadSfx(SoundGlobals.SFX_MONSTER_JR_FUNERAL_FIRE)), (PLocalizer.InvasionJollyRogerMainZone2, loadSfx(SoundGlobals.SFX_MONSTER_JR_YOUR_DESTINY))]
            self.winMessages = [
             (
              PLocalizer.InvasionJollyRogerEndPlayerWin4, loadSfx(SoundGlobals.SFX_MONSTER_JR_RETREAT))]
            self.loseMessages = [
             (
              PLocalizer.InvasionJollyRogerEndPlayerLose1, loadSfx(SoundGlobals.SFX_MONSTER_JR_VICTORY_MINE)), (PLocalizer.InvasionJollyRogerEndPlayerLose2, loadSfx(SoundGlobals.SFX_MONSTER_JR_NEXT_CONQUEST)), (PLocalizer.InvasionJollyRogerEndPlayerLose3, loadSfx(SoundGlobals.SFX_MONSTER_JR_NEXT_TARGET))]
        else:
            self.goodBossMessages = [
             (
              PLocalizer.InvasionJollyRogerBoss1, None), (PLocalizer.InvasionJollyRogerBoss3, None), (PLocalizer.InvasionJollyRogerBoss4, None), (PLocalizer.InvasionJollyRogerBoss5, None)]
            self.badBossMessages = [
             (
              PLocalizer.InvasionJollyRogerBoss2, None)]
            self.mainZoneMessages = [
             (
              PLocalizer.InvasionJollyRogerMainZone1, None), (PLocalizer.InvasionJollyRogerMainZone2, None)]
            self.winMessages = [
             (
              PLocalizer.InvasionJollyRogerEndPlayerWin4, None)]
            self.loseMessages = [
             (
              PLocalizer.InvasionJollyRogerEndPlayerLose1, None), (PLocalizer.InvasionJollyRogerEndPlayerLose2, None), (PLocalizer.InvasionJollyRogerEndPlayerLose3, None)]
        return None

    def disable(self):
        DistributedInvasionObject.DistributedInvasionObject.disable(self)

    def delete(self):
        DistributedInvasionObject.DistributedInvasionObject.delete(self)

    def spawnShip(self, shipClass, startPosHpr, midPosHpr, endPosHpr):
        self.shipNode = self.parentObj.attachNewNode('invasionShipNode')
        self.invasionShip = base.shipFactory.getShip(shipClass, ShipGlobals.Styles.Undead, 0)
        self.invasionShip.setOwner(self.shipNode)
        startPos = (startPosHpr[0], startPosHpr[1], startPosHpr[2])
        startHpr = (startPosHpr[3], startPosHpr[4], startPosHpr[5])
        midPos = (midPosHpr[0], midPosHpr[1], midPosHpr[2])
        midHpr = (midPosHpr[3], midPosHpr[4], midPosHpr[5])
        self.endPos = (endPosHpr[0], endPosHpr[1], endPosHpr[2])
        self.shipNode.setPos(startPos)
        self.shipNode.setHpr(startHpr)
        self.invasionShip.modelRoot.setColorScale(0, 0, 0, 0)
        self.invasionShip.modelRoot.setTransparency(1)
        self.invasionShip.modelRoot.hide()
        self.shipShowingIval = Parallel(self.startLightingEffects(startPos), Sequence(Wait(8.5), Func(self.invasionShip.modelRoot.show)), Sequence(Wait(8.5), Func(self.startDarkFog, startPos)), Sequence(Wait(10.0), Func(self.invasionShip.playStormEffect), Func(self.invasionShip.fadeIn)), Sequence(Wait(10.0), LerpPosInterval(self.shipNode, 18.0, midPos, blendType='easeOut')), Sequence(Wait(15.0), Func(self.stopDarkFog)), Sequence(Wait(28.0), Func(self.startMainFog)), Sequence(Wait(28.0), Func(base.musicMgr.requestFadeOut, SoundGlobals.MUSIC_TORMENTA)), Sequence(Wait(28.0), LerpHprInterval(self.shipNode, 10.0, midHpr, blendType='easeInOut')), Sequence(Wait(36.0), Func(base.musicMgr.request, SoundGlobals.MUSIC_TORMENTA_COMBAT, looping=True)))
        self.shipShowingIval.start()

    def placeShip(self, shipClass, midPosHpr, endPosHpr):
        if not self.invasionShip:
            self.shipNode = self.parentObj.attachNewNode('invasionShipNode')
            self.invasionShip = base.shipFactory.getShip(shipClass, ShipGlobals.Styles.Undead, 0)
            self.invasionShip.setOwner(self.shipNode)
            midPos = (midPosHpr[0], midPosHpr[1], midPosHpr[2])
            midHpr = (midPosHpr[3], midPosHpr[4], midPosHpr[5])
            self.endPos = (endPosHpr[0], endPosHpr[1], endPosHpr[2])
            self.invasionShip.playStormEffect()
            self.shipNode.setPos(midPos)
            self.shipNode.setHpr(midHpr)
            base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_TORMENTA)
            base.musicMgr.request(SoundGlobals.MUSIC_TORMENTA_COMBAT, looping=True)
            self.startMainFog(False)

    def hideShip(self):
        self.shipHidingIval = Parallel(Sequence(Wait(0.5), LerpPosInterval(self.shipNode, 18.0, self.endPos, blendType='easeIn')), Sequence(Wait(0.5), Func(self.stopMainFog)), Sequence(Wait(13.5), Func(self.startDarkFog, self.endPos)), Sequence(Wait(16.5), Func(self.invasionShip.fadeOut), Func(self.invasionShip.stopStormEffect)), Sequence(Wait(18.5), Func(self.invasionShip.modelRoot.hide)), Sequence(Wait(19.0), Func(self.stopDarkFog)))
        self.shipHidingIval.start()

    def updateBrigadeText(self):
        if self.brigadeText and self.parentObj.minimapArea:
            self.brigadeText.destroy()
            self.brigadeText = None
        elif not self.brigadeText and not self.parentObj.minimapArea and self.parentObj.minimap:
            self.brigadeText = DirectLabel(parent=self.parentObj.minimap.getOverlayNode(), relief=None, text=PLocalizer.InvasionJollyRogerBrigadeUpdate % (self.currentPhase, self.totalPhases - self.currentPhase), text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_font=PiratesGlobals.getPirateOutlineFont(), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, scale=60, pos=(-800,
                                                                                                                                                                                                                                                                                                                                                                                                              -200,
                                                                                                                                                                                                                                                                                                                                                                                                              0), hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                       -90,
                                                                                                                                                                                                                                                                                                                                                                                                                       0))
        return