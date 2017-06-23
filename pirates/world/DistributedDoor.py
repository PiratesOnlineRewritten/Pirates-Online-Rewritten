from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.world.LocationConstants import LocationIds
from pirates.piratesbase import Freebooter
import string
from direct.showbase.PythonUtil import quickProfile

class DistributedDoor(DistributedInteractive.DistributedInteractive):
    notify = directNotify.newCategory('DistributedDoor')
    notify.setDebug(0)
    openSfxDict = {}
    closeSfx = None

    def __init__(self, cr, name='DistributedDoor'):
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        NodePath.__init__(self, name)
        self.otherDoorId = 0
        self.doorState = PiratesGlobals.DOOR_CLOSED
        self.doorTrack = None
        self.fadeInTrack = None
        self.fadeOutTrack = None
        self.openOtherDoorIval = None
        self.closeOtherDoorIval = None
        self.soundNode = render
        self.locked = False
        self.hasDoors = 0
        self.tOpen = 0.5
        if not self.closeSfx:
            DistributedDoor.openSfxDict['english'] = base.loadSfx('audio/sfx_door_english_open.mp3')
            DistributedDoor.openSfxDict['shanty'] = base.loadSfx('audio/sfx_door_shanty_open.mp3')
            DistributedDoor.openSfxDict['spanish'] = base.loadSfx('audio/sfx_door_spanish_open.mp3')
            DistributedDoor.closeSfx = base.loadSfx('audio/sfx_door_shanty_slam.mp3')
            DistributedDoor.openSfx = DistributedDoor.openSfxDict['english']
        self.questNeeded = 1
        return

    def disable(self):
        self.ignoreAll()
        if self.doorTrack:
            self.doorTrack.pause()
            self.doorTrack = None
        self.openDoorIval.pause()
        del self.openDoorIval
        self.closeDoorIval.pause()
        del self.closeDoorIval
        if self.closeOtherDoorIval:
            self.closeOtherDoorIval.pause()
            self.closeOtherDoorIval = None
        if self.openOtherDoorIval:
            self.openOtherDoorIval.pause()
            self.openOtherDoorIval = None
        self.fadeOutTrack = None
        self.fadeInTrack = None
        DistributedInteractive.DistributedInteractive.disable(self)
        return

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        if hasattr(self, 'buildingUid') and self.buildingUid == LocationIds.PORT_ROYAL_FORT_CHARLES:
            tutFlag = localAvatar.style.getTutorial()
            if tutFlag > PiratesGlobals.TUT_GOT_CUTLASS and tutFlag < PiratesGlobals.TUT_GOT_COMPASS:
                self.setLocked(True)
            else:
                self.setLocked(False)
        self.setupDoors()
        self.setInteractOptions(proximityText=self.getPrompt(), diskRadius=12.0, sphereScale=7.0, endInteract=0, allowInteract=self.allowInteract)

    def getPrompt(self):
        return PLocalizer.InteractOpenDoor

    def setDoorIndex(self, doorIndex):
        self.doorIndex = doorIndex
        doorIndexStr = ''
        if doorIndex > 0:
            doorIndexStr = '_' + str(doorIndex + 1)
        self.doorLeftStr = '**/door_left' + doorIndexStr + ';+s'
        self.doorRightStr = '**/door_right' + doorIndexStr + ';+s'
        self.doorLocatorStr = '**/door_locator' + doorIndexStr + ';+s'

    def setBuildingUid(self, buildingUid):
        self.buildingUid = buildingUid

    def getBuildingUid(self):
        return self.buildingUid

    def setMovie(self, mode, avId, timestamp):
        if avId == localAvatar.doId:
            self.loadOtherSide()
            return
        if timestamp is None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        if mode == PiratesGlobals.DOOR_OPEN and self.hasDoors:
            if self.doorTrack:
                self.doorTrack.pause()
                self.doorTrack = None
            self.doorTrack = Sequence(Func(base.playSfx, self.openSfx, node=self.soundNode, volume=0.7, cutoff=100), self.openDoorIval, Wait(2.0), self.closeDoorIval, Func(base.playSfx, self.closeSfx, node=self.soundNode, volume=0.7, cutoff=100))
            self.doorTrack.start(ts)
        return

    def getParentModel(self):
        pass

    def setupDoors(self):
        self.openDoorIval = Parallel()
        self.closeDoorIval = Parallel()
        doors = self.getDoorInfo()
        if doors:
            self.noDoors = False
        else:
            self.noDoors = True
            return
        if self.doorIndex < len(doors['left']):
            doorLeft = doors['left'][self.doorIndex]
            self.openDoorIval.append(LerpHprInterval(doorLeft, self.tOpen, Vec3(-90, 0, 0)))
            self.closeDoorIval.append(LerpHprInterval(doorLeft, self.tOpen, Vec3(0, 0, 0)))
        else:
            doorLeft = None
        if self.doorIndex < len(doors['right']):
            doorRight = doors['right'][self.doorIndex]
            self.openDoorIval.append(LerpHprInterval(doorRight, self.tOpen, Vec3(90, 0, 0)))
            self.closeDoorIval.append(LerpHprInterval(doorRight, self.tOpen, Vec3(0, 0, 0)))
        else:
            doorRight = None
        modelName = ''
        if self.doorIndex < len(doors['locator']):
            doorLocator = doors['locator'][self.doorIndex]
            self.soundNode = doorLocator
            self.reparentTo(doorLocator)
            self.setPos(0, 0, 0)
            self.wrtReparentTo(self.getParentObj())
            modelName = doorLocator.getNetTag('ModelName')
        else:
            if doorLeft and doorRight:
                doorLocator = None
                doorPos = doorRight.getPos(doorLeft) * 0.5
                self.reparentTo(doorLeft)
                self.setPos(doorPos)
                self.wrtReparentTo(self.getParentObj())
                modelName = doorLeft.getNetTag('ModelName')
                self.soundNode = doorRight
            elif doorLeft:
                self.reparentTo(doorLeft)
                self.setPos(4, 0, 0)
                self.wrtReparentTo(self.getParentObj())
                modelName = doorLeft.getNetTag('ModelName')
                self.soundNode = doorLeft
            elif doorRight:
                self.reparentTo(doorRight)
                self.setPos(-4, 0, 0)
                self.wrtReparentTo(self.getParentObj())
                modelName = doorRight.getNetTag('ModelName')
                self.soundNode = doorRight
            self.hasDoors = doorLeft or doorRight
            for name in self.openSfxDict:
                if name in modelName:
                    self.openSfx = self.openSfxDict[name]

        self.openDoorIval.append(Func(base.playSfx, self.openSfx, node=self.soundNode, volume=0.7, cutoff=100))
        return

    def getOtherSideParentModel(self):
        pass

    def setupOtherSideDoors(self):
        otherParent = self.getOtherSideParentModel()
        doorLeft = otherParent.find(self.doorLeftStr)
        doorRight = otherParent.find(self.doorRightStr)
        self.openOtherDoorIval = Parallel()
        self.closeOtherDoorIval = Parallel()
        if not doorLeft.isEmpty():
            self.openOtherDoorIval.append(LerpHprInterval(doorLeft, self.tOpen, Vec3(-90, 0, 0)))
            self.closeOtherDoorIval.append(LerpHprInterval(doorLeft, self.tOpen, Vec3(0, 0, 0)))
        if not doorRight.isEmpty():
            self.openOtherDoorIval.append(LerpHprInterval(doorRight, self.tOpen, Vec3(90, 0, 0)))
            self.closeOtherDoorIval.append(LerpHprInterval(doorRight, self.tOpen, Vec3(0, 0, 0)))
        if self.closeSfx is not None:
            self.closeOtherDoorIval.append(Sequence(Wait(0.25), Func(base.playSfx, self.closeSfx, node=self.soundNode, volume=0.7, cutoff=100)))
        return

    def requestInteraction(self, avId, interactType=0):
        if self.buildingUid == LocationIds.KINGSHEAD_OUTER_DOOR and not Freebooter.getPaidStatus(localAvatar.getDoId()):
            localAvatar.guiMgr.showNonPayer(quest='Restricted_Location', focus=0)
            return
        print 'requestinteraction', 0
        if avId == localAvatar.doId:
            self.fadeOut()
            return
        if self.questNeeded:
            questHistory = localAvatar.getQuestLadderHistory()
            currentQuests = localAvatar.getQuests()
            container = QuestLadderDB.getContainer(self.questNeeded)
            canEnter = False
            for quest in currentQuests:
                if container.getQuestId() == quest.getQuestId() or container.hasQuest(quest.getQuestId()):
                    canEnter = True

            if not canEnter:
                if self.buildingUid == LocationIds.UNDEAD_POKER_SHACK:
                    localAvatar.guiMgr.createWarning(PLocalizer.ClubheartsQuestWarning, PiratesGuiGlobals.TextFG6)
                return
        print 'requestinteraction', 2
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        if self.fadeOutTrack:
            self.fadeOutTrack.finish()
        si = Sequence(Func(base.transitions.fadeIn, self.tOpen), Func(localAvatar.gameFSM.request, 'LandRoam'))
        self.fadeInTrack = si
        self.fadeInTrack.start()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def fadeOut(self):
        base.transitions.setFadeColor(0, 0, 0)

        def doFadeOut():
            base.transitions.fadeOut(self.tOpen)

        if localAvatar.gameFSM is None:
            return
        si = Sequence(Func(localAvatar.b_setGameState, 'DoorInteract'), Func(doFadeOut), self.openDoorIval, self.closeDoorIval, Func(DistributedInteractive.DistributedInteractive.requestInteraction, self, base.localAvatar.doId, 0))
        self.fadeOutTrack = si
        self.fadeOutTrack.start()
        return

    def fadeIn(self):
        sf = Sequence(Func(localAvatar.gameFSM.request, 'DoorInteract'), Func(base.transitions.fadeIn, self.tOpen), self.openOtherDoorIval, self.closeOtherDoorIval, Func(localAvatar.gameFSM.request, 'LandRoam'))
        self.fadeInTrack = sf
        self.fadeInTrack.start()

    def setLocked(self, locked):
        self.setAllowInteract(not locked)
        self.locked = locked

    def showProximityStuff(self):
        DistributedInteractive.DistributedInteractive.showProximityStuff(self)
        base.cr.interactionMgr.useLifter(self.disk)

    def getDoorInfo(self):
        pass

    def setOtherDoorId(self, doorDoId):
        self.otherDoorId = doorDoId

    def getOtherDoorId(self):
        return self.otherDoorId

    def getDoorLocator(self):
        return self.getDoorInfo()['locator'][self.doorIndex]

    def getDoorLeft(self):
        return self.getDoorInfo()['left'][self.doorIndex]

    def getDoorRight(self):
        return self.getDoorInfo()['right'][self.doorIndex]

    def goOnStage(self):
        pass

    def goOffStage(self):
        pass

    def setQuestNeeded(self, questNeeded):
        self.questNeeded = questNeeded