from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import ScratchPad
from pirates.audio import SoundGlobals
from pirates.cutscene import CutsceneData, CutsceneActor
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.tutorial import TutorialGlobals
from pirates.quest import QuestConstants
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.Subtitler import Subtitler
from pirates.audio.SoundGlobals import loadSfx

def Nothing():
    pass


def WaitFrames(frames):
    return WaitInterval(frames / 24.0)


def HideAllNametags():
    render.findAllMatches('**/nametag3d*').hide()


def ShowAllNametags():
    render.findAllMatches('**/nametag3d*').show()


def playAudio(sound, ivalToAppendTo, seqDuration):
    si = SoundInterval(sound, duration=seqDuration)
    si.start()


def placeObject(object, wrt, pos, hpr):
    object.reparentTo(render)
    object.setPos(wrt, pos)
    object.setHpr(wrt, hpr)


def reparentObject(object, wrt, pos, hpr):
    object.reparentTo(wrt)
    object.setPos(pos)
    object.setHpr(hpr)


def SetTimeOfDay(tod, time=0):
    if 'localAvatar' in __builtins__:
        return Func(base.cr.timeOfDayManager.request, base.cr.timeOfDayManager.getStateName(tod), 0)
    else:
        return Wait(0.001)


def setObjectVisibleByUid(uid, hide=True):
    existingObjectId = base.cr.uidMgr.getDoId(uid)
    existingObject = base.cr.doId2do.get(existingObjectId)
    if existingObject:
        if hide:
            funcRef = existingObject.stash
            if hasattr(existingObject, 'setAllowInteract'):
                existingObject.setAllowInteract(False)
        else:
            funcRef = existingObject.unstash
            if hasattr(existingObject, 'setAllowInteract'):
                existingObject.setAllowInteract(True)
        hideObjectFunc = Func(funcRef)
    else:

        def dummyFunc():
            pass

        hideObjectFunc = Func(dummyFunc)
    return hideObjectFunc


def forceLowLODOnAvatars():
    if 'localAvatar' not in __builtins__:
        return
    for item in base.cr.doId2do.items():
        do = item[1]
        if do.dclass.getName() == 'DistributedNPCTownfolk':
            do.forceLOD(0)
        elif do.dclass.getName() == 'DistributedHoldemTable':
            do.dealer.forceLOD(0)
            for i in range(len(do.AIPlayers)):
                if do.AIPlayers[i]:
                    do.AIPlayers[i].forceLOD(0)


def resetLODOnAvatars():
    if 'localAvatar' not in __builtins__:
        return
    for item in base.cr.doId2do.items():
        do = item[1]
        if do.dclass.getName() == 'DistributedNPCTownfolk':
            do.resetLOD()
        elif do.dclass.getName() == 'DistributedHoldemTable':
            do.dealer.resetLOD()
            for i in range(len(do.AIPlayers)):
                if do.AIPlayers[i]:
                    do.AIPlayers[i].resetLOD()


def forceInteract(objUid, doorIndex=None):

    def _forceInteractCallback(objDoId):
        objRef = base.cr.doId2do.get(objDoId)
        if doorIndex != None:
            if len(objRef.links) <= doorIndex:
                print 'warning: could not find door index %s for object %s' % (doorIndex, objDoId)
                return
            doorDoId = objRef.links[doorIndex][0]
            doorObj = base.cr.doId2do.get(doorDoId)
            if doorObj:
                doorObj.handleUseKey()
        else:
            objRef.handleUseKey()
        return

    if 'localAvatar' in __builtins__:
        base.cr.uidMgr.addUidCallback(objUid, _forceInteractCallback)


def Cutscene1_1_1ivals(cutscene):
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Sequence(Func(base.transitions.fadeIn, 7.0)), Sequence(WaitFrames(288), Func(base.transitions.fadeOut)), subs),
     Parallel(Func(base.transitions.fadeIn), clearSubs))


def Cutscene1_1_2ivals(cutscene):
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    cballHitTrack = loadSfx(SoundGlobals.SFX_WEAPON_CANNON_HIT)
    loader.loadModel('models/effects/explosion')
    loader.loadModel('models/effects/shockwaveRing')
    KickFrame = 245
    CannonStartFrame = 330
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Sequence(WaitFrames(KickFrame), Func(av.openJailDoor)), Sequence(WaitFrames(KickFrame), SoundInterval(cballHitTrack, volume=0.6)), Sequence(WaitFrames(CannonStartFrame), Func(messenger.send, 'startTutorialCannons')), subs),
     Parallel(Func(av.closeJailDoor), clearSubs))


def Cutscene1_1_5_aivals(cutscene):
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    Dan = cutscene.getActor('Pirate-m-1')
    Nell = cutscene.getActor('Pirate-f-1')
    mugLeft = loader.loadModel('models/handheld/mug_high')
    mugLeft.flattenStrong()
    mugRight = loader.loadModel('models/handheld/mug_high')
    mugRight.flattenStrong()
    seachestDan = loader.loadModel('models/handheld/sea_chest_high')
    if seachestDan == None or seachestDan.isEmpty():
        seachestDan = loader.loadModel('models/props/treasureChest')
    seachestDan.flattenStrong()
    seachestTable = loader.loadModel('models/handheld/sea_chest_high')
    if seachestTable == None or seachestTable.isEmpty():
        seachestTable = loader.loadModel('models/props/treasureChest')
    seachestTable.setScale(0.8)
    seachestTable.flattenStrong()
    if 'localAvatar' in __builtins__:
        av.localAvatar.tutObject = seachestTable
        endFunc = Func(Nothing)
    else:
        endFunc = Func(seachestTable.removeNode)
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Sequence(Func(base.transitions.fadeIn, 4.0)), Sequence(Func(av.adjustPos, 9.561, 26.215, 5.255)), Sequence(Func(av.recordEvent, 'beginSeachest')), Sequence(WaitFrames(125), Func(Nell.attachHandheld, mugRight, True)), Sequence(WaitFrames(126), Func(Nell.attachHandheld, mugLeft, False)), Sequence(WaitFrames(215), Func(Nell.detachHandheld, mugLeft, True)), Sequence(WaitFrames(216), Func(Nell.detachHandheld, mugRight, True)), Sequence(WaitFrames(719), Func(Dan.attachHandheld, seachestDan, True)), Sequence(WaitFrames(754), Func(Dan.detachHandheld, seachestDan, True)), Sequence(WaitFrames(754), Func(reparentObject, seachestTable, render, VBase3(9.53, 33.22, 5.11), VBase3(180, 0, 90))), subs),
     Parallel(endFunc, clearSubs))


def Cutscene1_1_5_bivals(cutscene):
    cutcam = cutscene.getActor(CutsceneActor.CutCam.getActorKey())
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(subs), Parallel(clearSubs))


def Cutscene1_1_5_civals(cutscene):
    cutcam = cutscene.getActor(CutsceneActor.CutCam.getActorKey())
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Sequence(WaitFrames(814), Func(base.transitions.fadeOut, 2.0)), subs),
     Parallel(Func(forceInteract, TutorialGlobals.TAVERN_INTERIOR, 1), clearSubs))


def Cutscene1_2ivals(cutscene):
    interceptor = cutscene.getActor(CutsceneActor.CutShip.getActorKey(ShipGlobals.STUMPY_SHIP))
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    if 'localAvatar' in __builtins__:
        hideInterceptorFunc = setObjectVisibleByUid(TutorialGlobals.STUMPY_BOAT_UID)
        showInterceptorFunc = setObjectVisibleByUid(TutorialGlobals.STUMPY_BOAT_UID, False)
    else:
        hideInterceptorFunc = Func(Nothing)
        showInterceptorFunc = Func(Nothing)
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(hideInterceptorFunc, Sequence(Func(av.recordEvent, 'sendToBoat')), subs),
     Parallel(Sequence(showInterceptorFunc), clearSubs))


def Cutscene1_3ivals(cutscene):
    jollyRoger = cutscene.getActor(CutsceneActor.CutJollyRoger.getActorKey())
    interceptor = cutscene.getActor(CutsceneActor.CutShip.getActorKey(ShipGlobals.STUMPY_SHIP))
    interceptor.ship.computeDimensions()
    skelship = cutscene.getActor(CutsceneActor.CutShip.getActorKey(ShipGlobals.SKEL_DEATH_OMEN))
    skelship.ship.modelRoot.setColorScale(Vec4(0, 0, 0, 0))
    skelship.buildCannons()
    loader.loadModel('models/effects/darkglow')
    loader.loadModel('models/effects/flareGlow')
    if 'localAvatar' in __builtins__:
        hideInterceptorFunc = setObjectVisibleByUid(TutorialGlobals.STUMPY_BOAT_UID)
    else:
        hideInterceptorFunc = Func(Nothing)
    captBeck = cutscene.getActor('Pirate-m-1')
    captBeckSkel = cutscene.getActor('Skeleton-1')
    captBeckSkel.hide()
    captBeckSkel.setDepthTest(0)
    captBeckSkel.setBin('fixed', 150)
    moneybag = loader.loadModel('models/handheld/moneybag_high')
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Func(messenger.send, 'toggleGlows'), Func(jollyRoger.setColorScale, Vec4(0, 0, 0, 0)), hideInterceptorFunc, Sequence(WaitFrames(12), Func(skelship.ship.startDarkFog, -80)), Sequence(Func(messenger.send, 'introduceJR'), WaitFrames(83)), Sequence(WaitFrames(75), Func(skelship.ship.playStormEffect)), Sequence(WaitFrames(85), Func(skelship.ship.fadeIn)), Sequence(WaitFrames(140), Func(skelship.ship.stopDarkFog)), Sequence(Func(messenger.send, 'JRAttackShip'), WaitFrames(274)), Sequence(WaitFrames(295), Func(jollyRoger.startTeleportEffect, 1.25)), Sequence(WaitFrames(310), Func(jollyRoger.fadeInBlack, 2.0)), Sequence(WaitFrames(385), Func(jollyRoger.spawnSkeletons, cutscene)), Sequence(WaitFrames(731), Func(captBeck.attachHandheld, moneybag, False)), Sequence(WaitFrames(1000), Func(jollyRoger.startAttuneEffect)), Sequence(WaitFrames(1120), Func(jollyRoger.startSoulSuckEffect)), Sequence(WaitFrames(1147), Func(captBeck.detachHandheld, moneybag, True)), Sequence(WaitFrames(1144), Func(captBeck.setBin, 'fixed', 140), Func(captBeckSkel.fadeIn, 1.0), Func(captBeck.fadeOut, 1.5)), Sequence(WaitFrames(1240), Func(jollyRoger.stopSoulSuckEffect)), Sequence(WaitFrames(1547)), Sequence(WaitFrames(1760), Func(jollyRoger.startTeleportEffect, -1.0)), Sequence(WaitFrames(1765), Func(jollyRoger.fadeOutBlack, 1.5)), Sequence(WaitFrames(1910), Func(skelship.fireCannon, 0, ammo=InventoryType.CannonFirebrand, targetNode=interceptor.ship.modelRoot, offset=Vec3(0, 0, 10), wantCollisions=1, flightTime=0.3, preciseHit=1)), Sequence(WaitFrames(1928), Func(skelship.fireCannon, 3, ammo=InventoryType.CannonFirebrand, targetNode=interceptor.ship.modelRoot, offset=Vec3(0, 0, 15), wantCollisions=1, flightTime=0.5, preciseHit=1)), Sequence(WaitFrames(1948), Func(skelship.fireCannon, 1, ammo=InventoryType.CannonFirebrand, targetNode=interceptor.ship.modelRoot, offset=Vec3(0, 0, 50), wantCollisions=1, flightTime=0.5, preciseHit=1)), Sequence(WaitFrames(1955), Func(interceptor.explosionVFX, node=interceptor.ship.modelRoot, offset=Vec3(0, 0, 50))), Sequence(WaitFrames(1968), Func(skelship.fireCannon, 4, ammo=InventoryType.CannonFirebrand, targetNode=interceptor.ship.modelRoot, offset=Vec3(0, 0, 10), wantCollisions=1, flightTime=0.5, preciseHit=1)), Sequence(WaitFrames(1980), Func(interceptor.explosionVFX, node=interceptor.ship.modelRoot, offset=Vec3(0, 0, 15))), Sequence(WaitFrames(1980), Func(skelship.fireCannon, 0, ammo=InventoryType.CannonFirebrand, targetNode=interceptor.ship.modelRoot, offset=Vec3(0, 0, 10), wantCollisions=1, flightTime=0.5, preciseHit=1)), Sequence(WaitFrames(2008), Func(skelship.fireCannon, 4, ammo=InventoryType.CannonFirebrand, targetNode=interceptor.ship.modelRoot, offset=Vec3(0, 0, 15), wantCollisions=1, flightTime=0.5, preciseHit=1)), Sequence(WaitFrames(2020), Func(interceptor.explosionVFX, node=interceptor.ship.modelRoot, offset=Vec3(0, 0, 10))), Sequence(WaitFrames(1980), Func(interceptor.ship.startSinkEffects)), Sequence(WaitFrames(1960), Func(interceptor.ship.breakMast, 0)), Sequence(WaitFrames(2020), Func(skelship.ship.startDarkFog, -70)), Sequence(WaitFrames(2112), Func(skelship.ship.stopDarkFog), Func(skelship.ship.fadeOut), Func(skelship.ship.stopStormEffect)), Sequence(WaitFrames(2110), Func(interceptor.ship.endSinkEffects)), subs),
     Parallel(clearSubs, Func(messenger.send, 'JRDestroyShip')))


def Cutscene2_1ivals(cutscene):
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    willTurner = cutscene.getActor(CutsceneActor.CutWillTurner.getActorKey())
    cutlass = loader.loadModel('models/handheld/cutlass_rusty_high')
    motion_blur = cutlass.find('**/motion_blur')
    if motion_blur:
        motion_blur.stash()
    cutlass.flattenStrong()
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Func(base.transitions.fadeIn), Func(willTurner.attachHandheld, cutlass, True), Func(av.adjustPos, 30, -8, -5.975), Sequence(WaitFrames(522), Func(willTurner.detachHandheld, cutlass)), Sequence(WaitFrames(530), Func(av.attachHandheld, cutlass, True)), Sequence(WaitFrames(668), Func(av.detachHandheld, cutlass, True)), Sequence(WaitFrames(787), Func(willTurner.recordTransAtCutscene, 787)), Sequence(WaitFrames(801), Func(base.transitions.fadeOut, 0.66)), Sequence(WaitFrames(817), Func(base.transitions.fadeIn, 2.0)), subs), clearSubs)


def Cutscene2_1_bivals(cutscene):
    cutcam = cutscene.getActor(CutsceneActor.CutCam.getActorKey())
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    willTurner = cutscene.getActor(CutsceneActor.CutWillTurner.getActorKey())
    cutlass = loader.loadModel('models/handheld/cutlass_rusty_high')
    motion_blur = cutlass.find('**/motion_blur')
    if motion_blur:
        motion_blur.stash()
    cutlass.flattenStrong()
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Func(av.attachHandheld, cutlass, True), Sequence(WaitFrames(80), Func(av.detachHandheld, cutlass)), Sequence(WaitFrames(206), Func(willTurner.spawnSkeletons, cutscene)), Sequence(WaitFrames(314), Func(cutcam.changeCameraParams, 0, 35)), Sequence(WaitFrames(346), Func(willTurner.attachHandheld, cutlass, True)), Sequence(WaitFrames(393), Func(base.transitions.fadeOut)), subs),
     Parallel(Func(willTurner.detachHandheld, cutlass, True), Func(forceInteract, TutorialGlobals.PIT_INTERIOR, 1), clearSubs))


def Cutscene2_2ivals(cutscene):
    cutcam = cutscene.getActor(CutsceneActor.CutCam.getActorKey())
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    tiaDalma = cutscene.getActor(CutsceneActor.CutTiaDalma.getActorKey())
    compass = loader.loadModel('models/props/compass_high')
    compass.flattenStrong()
    lantern = cutscene.getActor('GenericActor-lantern')
    lantern.loadEffects(cutscene)
    if lantern.effect:
        lantern.effect.setZ(lantern.effect.getZ() - 0.55)
        lantern.effect.setScale(0.4)
    lanternLight = None
    if 'localAvatar' not in __builtins__:
        lanternLightObject = base.pe.objectMgr.findObjectById('1175893134.2dzlu')
        if lanternLightObject:
            lanternLight = lanternLightObject[0]
    else:
        lanternLight = base.cr.uidMgr.getUidObj('1175893134.2dzlu')
        base.cr.loadingScreen.hide()
    base.transitions.fadeIn(0.5)
    if lanternLight:
        wrtNode = lantern.find('**/def_root')
        if wrtNode.isEmpty():
            wrtNode = lantern
        oldPos = lanternLight.getPos()
        oldHpr = lanternLight.getHpr()
        reparentFunc1 = Func(reparentObject, lanternLight, wrtNode, Vec3(0, 0, 0), Vec3(0, 0, 0))
        reparentFunc2 = Func(reparentObject, lanternLight, render, oldPos, oldHpr)
    else:
        reparentFunc1 = Func(Nothing)
        reparentFunc2 = Func(Nothing)

    def addFog():
        self.fog = Fog('TimeOfDayFog')
        self.fog.setExpDensity(0.04)
        render.setFog(self.fog)

    bg1Cutlass = loader.loadModel('models/handheld/cutlass_steel_high')
    motion_blur = bg1Cutlass.find('**/motion_blur')
    if motion_blur:
        motion_blur.stash()
    bg1Cutlass.flattenStrong()
    bg2Cutlass = loader.loadModel('models/handheld/cutlass_steel_high')
    motion_blur = bg2Cutlass.find('**/motion_blur')
    if motion_blur:
        motion_blur.stash()
    bg2Cutlass.flattenStrong()
    bg3Cutlass = loader.loadModel('models/handheld/cutlass_steel_high')
    motion_blur = bg3Cutlass.find('**/motion_blur')
    if motion_blur:
        motion_blur.stash()
    bg3Cutlass.flattenStrong()
    loader.loadModel('models/effects/particleMaps')
    cutlassDict = [
     bg1Cutlass, bg2Cutlass, bg3Cutlass]
    func1 = Sequence(Func(base.ambientMgr.requestChangeVolume, SoundGlobals.AMBIENT_JUNGLE, 3.0, 0.15, priority=1))
    func2 = Sequence(Func(base.ambientMgr.requestFadeIn, SoundGlobals.AMBIENT_JUNGLE, 10, finalVolume=PiratesGlobals.DEFAULT_AMBIENT_VOLUME, priority=1))
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(func1, Func(tiaDalma.hideVision, cutscene, cutlassDict, False), Sequence(WaitFrames(784), Func(tiaDalma.showVisionBG, cutscene)), Sequence(WaitFrames(990), Func(tiaDalma.showVisionJR, cutscene)), Sequence(WaitFrames(1010), Func(tiaDalma.spawnSkeleton1, cutscene)), Sequence(WaitFrames(1100), Func(tiaDalma.spawnSkeleton2, cutscene)), Sequence(WaitFrames(1295), Func(tiaDalma.hideVision, cutscene, cutlassDict, True)), Sequence(WaitFrames(1524), Func(tiaDalma.attachHandheld, compass, True)), Sequence(WaitFrames(1685), reparentFunc1), Sequence(WaitFrames(1690), Func(tiaDalma.detachHandheld, compass, True)), Sequence(WaitFrames(2192), Func(base.transitions.fadeOut, 1.0)), subs),
     Parallel(func2, reparentFunc2, Func(lantern.unloadEffects), Func(base.transitions.fadeIn), clearSubs))


def Cutscene2_3ivals(cutscene):
    cutcam = cutscene.getActor(CutsceneActor.CutCam.getActorKey())
    elizabethSwan = cutscene.getActor(CutsceneActor.CutElizabethSwan.getActorKey())
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Func(base.transitions.fadeIn), Sequence(WaitFrames(144), Func(cutcam.changeCameraParams, 0, 45)), Sequence(WaitFrames(918), Func(cutcam.changeCameraParams, 0, 32)), Sequence(WaitFrames(1348), Func(base.transitions.fadeOut, 1.0)), Sequence(WaitFrames(1372), Func(forceInteract, TutorialGlobals.MANSION_INTERIOR, 0)), subs), clearSubs)


def Cutscene2_4ivals(cutscene):
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    captBarbossa = cutscene.getActor(CutsceneActor.CutCaptBarbossa.getActorKey())
    pistol = loader.loadModel('models/handheld/pistol_high')
    pistol.flattenStrong()
    if 'localAvatar' in __builtins__:
        hideMunkieFunkie = setObjectVisibleByUid(TutorialGlobals.JACK_THE_MONKEY)
    else:
        hideMunkieFunkie = Func(Nothing)
    if 'localAvatar' in __builtins__:
        localAvatar.getParentObj().envEffects.soundVolumeDown()
    if 'localAvatar' in __builtins__:
        base.cr.loadingScreen.hide()
    base.transitions.fadeIn(0.5)
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(hideMunkieFunkie, Func(av.adjustPos, -5.4, 11.6, 4.2, 230), Sequence(WaitFrames(230), Func(captBarbossa.attachHandheld, pistol, False)), Sequence(WaitFrames(264), Func(captBarbossa.detachHandheld, pistol)), Sequence(WaitFrames(265), Func(av.attachHandheld, pistol, True)), Sequence(WaitFrames(496), Func(av.detachHandheld, pistol, True)), subs), clearSubs)


def Cutscene2_4_bivals(cutscene):
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    av.hideZombie()
    captBarbossa = cutscene.getActor(CutsceneActor.CutCaptBarbossa.getActorKey())
    pistol = loader.loadModel('models/handheld/pistol_cb_high')
    if pistol == None:
        pistol = loader.loadModel('models/handheld/pistol_high')
    pistol.flattenStrong()
    if 'localAvatar' in __builtins__:
        localAvatar.getParentObj().envEffects.soundVolumeDown()
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Sequence(WaitFrames(980), Func(base.transitions.fadeOut, 1.0)), subs), clearSubs)


def Cutscene2_5ivals(cutscene):
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    jackSparrow = cutscene.getActor(CutsceneActor.CutJackSparrow.getActorKey())
    if 'localAvatar' not in __builtins__:
        hideJackFunc = Func(Nothing)
    else:
        hideJackFunc = setObjectVisibleByUid(QuestConstants.NPCIds.JACK)
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Sequence(WaitFrames(24), Func(HideAllNametags)), Func(forceLowLODOnAvatars), Func(base.transitions.fadeIn), Func(av.adjustPos, -5, 23, 1.0, 130), hideJackFunc, subs),
     Parallel(Func(ShowAllNametags), Func(resetLODOnAvatars), clearSubs))


def Cutscene3_1ivals(cutscene):
    fadeOutFrame = 1740
    tFadeOut = 3.0
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Sequence(Func(base.transitions.fadeIn), WaitFrames(fadeOutFrame), base.transitions.getFadeOutIval(tFadeOut)), subs), Parallel(clearSubs))


def Cutscene3_2ivals(cutscene):
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    jackSparrow = cutscene.getActor(CutsceneActor.CutJackSparrow.getActorKey())
    goldbag = loader.loadModel('models/handheld/moneybag_high')
    if 'localAvatar' not in __builtins__:
        hideJackFunc = Func(Nothing)
        showJackFunc = Func(Nothing)
    else:
        hideJackFunc = setObjectVisibleByUid(QuestConstants.NPCIds.JACK)
        showJackFunc = setObjectVisibleByUid(QuestConstants.NPCIds.JACK, False)
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Func(base.transitions.fadeIn), Sequence(WaitFrames(24), Func(HideAllNametags)), Sequence(WaitFrames(1387), Func(jackSparrow.attachHandheld, goldbag, True)), Sequence(WaitFrames(1403), Func(jackSparrow.detachHandheld, goldbag)), Sequence(WaitFrames(1438), Func(av.attachHandheld, goldbag, True)), Sequence(WaitFrames(1445), Func(av.detachHandheld, goldbag, True)), hideJackFunc, subs),
     Parallel(Func(ShowAllNametags), showJackFunc, clearSubs))


def Cutscene6_1ivals(cutscene):
    cutcam = cutscene.getActor(CutsceneActor.CutCam.getActorKey())
    av = cutscene.getActor(CutsceneActor.CutLocalPirate.getActorKey())
    tiaDalma = cutscene.getActor(CutsceneActor.CutTiaDalma.getActorKey())
    vdoll = loader.loadModel('models/handheld/voodoo_doll_high')
    vdoll.setP(180)
    subs, clearSubs = subtitleSequence(cutscene.cutsceneName)
    return (
     Parallel(Func(av.localAvatar.hide), Sequence(WaitFrames(280), Func(tiaDalma.attachHandheld, vdoll, True)), Sequence(WaitFrames(585), Func(tiaDalma.detachHandheld, vdoll, True)), subs),
     Parallel(Func(av.localAvatar.show), clearSubs))


def subtitleSequence(cutsceneId):
    if hasattr(base, 'pe') and base.pe.panel.showCutsceneSubtitle.get() == 0:
        return (
         Func(Nothing), Func(Nothing))
    if config.GetBool('force-cut-sub-reloads', 0):
        reload(CutsceneData)
    subData = CutsceneData.CutsceneSubtitles.get(cutsceneId)
    if 'localAvatar' not in __builtins__:
        if not __builtins__.has_key('subtitler'):
            __builtins__['subtitler'] = Subtitler()
        subtitler = __builtins__['subtitler']
    else:
        subtitler = base.localAvatar.guiMgr.subtitler
    if subData == None:
        return (
         Func(Nothing), Func(Nothing))
    allSubs = Parallel()
    EscTextSeq = Sequence()
    EscTextSeq.append(Func(subtitler.showEscapeText, PLocalizer.CutEscCutscene))
    allSubs.append(EscTextSeq)
    for currSubData in subData:
        currSeq = Sequence()
        waitTime = currSubData.get('beginTime')
        currSeq.append(WaitInterval(waitTime))
        text = currSubData.get('text')
        currSeq.append(Func(subtitler.showText, text))
        allSubs.append(currSeq)
        durationTime = currSubData.get('endTime')
        if durationTime:
            currSeq = Sequence()
            currSeq.append(WaitInterval(durationTime))
            currSeq.append(Func(subtitler.clearText))
            allSubs.append(currSeq)

    clearSubs = Sequence()
    clearSubs.append(Func(subtitler.clearText))
    clearSubs.append(Func(subtitler.hideEscapeText))
    return (
     allSubs, clearSubs)


CutsceneIvals = {CutsceneData.Cutscene1_1_1: Cutscene1_1_1ivals,CutsceneData.Cutscene1_1_2: Cutscene1_1_2ivals,CutsceneData.Cutscene1_1_5_a: Cutscene1_1_5_aivals,CutsceneData.Cutscene1_1_5_b: Cutscene1_1_5_bivals,CutsceneData.Cutscene1_1_5_c: Cutscene1_1_5_civals,CutsceneData.Cutscene1_2: Cutscene1_2ivals,CutsceneData.Cutscene1_3: Cutscene1_3ivals,CutsceneData.Cutscene2_1: Cutscene2_1ivals,CutsceneData.Cutscene2_1_b: Cutscene2_1_bivals,CutsceneData.Cutscene2_2: Cutscene2_2ivals,CutsceneData.Cutscene2_3: Cutscene2_3ivals,CutsceneData.Cutscene2_4: Cutscene2_4ivals,CutsceneData.Cutscene2_4_b: Cutscene2_4_bivals,CutsceneData.Cutscene2_5: Cutscene2_5ivals,CutsceneData.Cutscene3_1: Cutscene3_1ivals,CutsceneData.Cutscene3_2: Cutscene3_2ivals,CutsceneData.Cutscene6_1: Cutscene6_1ivals}