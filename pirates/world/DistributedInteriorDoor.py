from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.otpgui import OTPDialog
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import TimeOfDayManager
from direct.showbase.PythonUtil import report
from pirates.piratesgui import PDialog
from pirates.world.DistributedDoor import DistributedDoor
from pirates.piratesgui import SkipTutorialFrame
from pirates.world.LocationConstants import LocationIds
from pirates.tutorial import TutorialGlobals

class DistributedInteriorDoor(DistributedDoor):
    notify = directNotify.newCategory('DistributedInteriorDoor')

    def __init__(self, cr):
        DistributedDoor.__init__(self, cr, 'DistributedInteriorDoor')
        self.islandRequest = None
        self.doorDisableDialog = None
        self.skipTutorialBox = None
        return

    def delete(self):
        if self.islandRequest:
            self.cr.relatedObjectMgr.abortRequest(self.islandRequest)
            self.islandRequest = None
        DistributedDoor.delete(self)
        return

    def disable(self):
        self.cleanupDoorDisableDialog()
        if self.skipTutorialBox:
            self.skipTutorialBox.destroy()
            self.skipTutorialBox = None
        del self.interior
        DistributedDoor.disable(self)
        return

    def setInteriorId(self, interiorDoId, interiorParentId, interiorZoneId):
        self.interiorDoId = interiorDoId
        self.interiorParentId = interiorParentId
        self.interiorZoneId = interiorZoneId
        self.interior = self.cr.doId2do[self.interiorDoId]
        self.interiorUId = self.interior.uniqueId

    def setExteriorId(self, exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId):
        self.exteriorDoId = exteriorDoId
        self.exteriorWorldParentId = exteriorWorldParentId
        self.exteriorWorldZoneId = exteriorWorldZoneId

    def setBuildingDoorId(self, buildingDoorId):
        self.buildingDoorId = buildingDoorId

    def getParentModel(self):
        return self.interior.geom

    def getOtherSideParentModel(self):
        island = base.cr.doId2do.get(self.exteriorDoId)
        building = island.find('**/=uid=%s;+s' % self.buildingUid)
        return building

    def loadOtherSide(self):
        return
        localAvatar.setInterest(self.exteriorWorldParentId, self.exteriorWorldZoneId, ['instanceInterest-Door'])

        def extFinishedCallback(ext):
            self.islandRequest = None
            self.loadExteriorFinished()
            return

        self.islandRequest = self.cr.relatedObjectMgr.requestObjects([self.exteriorDoId], eachCallback=extFinishedCallback)

    def cleanupDoorDisableDialog(self, extraArgs=None):
        if self.doorDisableDialog:
            self.doorDisableDialog.destroy()
            self.doorDisableDialog = None
        return

    def requestInteraction(self, avId, interactType=0):
        locationId = base.localAvatar.getLocation()[0]
        location = None
        if locationId:
            locationObj = base.cr.doId2do.get(locationId)
            if locationObj:
                location = locationObj.uniqueId
        if location == TutorialGlobals.JAIL_INTERIOR and base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_CUTLASS:
            if not self.skipTutorialBox:
                base.localAvatar.motionFSM.moveLockIfOn()
                self.avId = avId
                self.interactType = interactType
                self.skipTutorialBox = SkipTutorialFrame.SkipTutorialFrame(callback=self.handleSkipTutorial)
            return
        elif not base.launcher.getPhaseComplete(3):
            if not self.doorDisableDialog:
                base.cr.centralLogger.writeClientEvent('Player encountered phase 3 blocker')
                self.doorDisableDialog = PDialog.PDialog(text=PLocalizer.NoRambleshack, style=OTPDialog.Acknowledge, command=self.cleanupDoorDisableDialog)
            return
        if self.buildingUid == LocationIds.PARLOR_BUILDING:
            if avId == base.localAvatar.doId:
                base.transitions.fadeOut(self.tOpen)
                self.openDoorIval.start()
                self.cr.teleportMgr.d_requestShardTeleport(base.localAvatar.getDefaultShard())
                return
        DistributedDoor.requestInteraction(self, avId, interactType)
        return

    def handleSkipTutorial(self, skip):
        localAvatar.motionFSM.onIfMoveLock()
        if self.skipTutorialBox:
            self.skipTutorialBox.destroy()
            self.skipTutorialBox = None
        if skip:
            self.skipTutorial = True
            if not base.launcher.getPhaseComplete(4):
                if not self.doorDisableDialog:
                    base.cr.centralLogger.writeClientEvent('Player encountered phase 4 blocker trying to skip tutorial before PR downloaded')
                    self.doorDisableDialog = PDialog.PDialog(text=PLocalizer.NoPortRoyal, style=OTPDialog.Acknowledge, command=self.cleanupDoorDisableDialog)
                return
            base.cr.tutorialObject.skipTutorial()
        else:
            self.askedTutorial = True
            if not base.launcher.getPhaseComplete(3):
                if not self.doorDisableDialog:
                    base.cr.centralLogger.writeClientEvent('Player encountered phase 3 blocker trying to leave starting jail')
                    self.doorDisableDialog = PDialog.PDialog(text=PLocalizer.NoRambleshack, style=OTPDialog.Acknowledge, command=self.cleanupDoorDisableDialog)
                return
            DistributedDoor.requestInteraction(self, self.avId, self.interactType)
        return

    def loadExteriorFinished(self):
        island = self.cr.doId2do.get(self.exteriorDoId)
        base.cr.loadingScreen.showTarget(island.uniqueId)
        base.cr.loadingScreen.show()
        self.interior.handleExitGameArea(None)
        self.interior.disableFloors()
        island.ensureLoaded()
        base.loadingScreen.tick()
        world = self.interior.getParentObj()
        world.removeWorldInterest()
        localAvatar.clearInterestNamed(None, ['instanceInterest'])
        localAvatar.replaceInterestTag('instanceInterest-Door', 'instanceInterest')
        base.loadingScreen.tick()
        building = self.getOtherSideParentModel()
        doorLocator = building.find(self.doorLocatorStr)
        if doorLocator.isEmpty():
            doorLocator = building.find(self.doorLeftStr)
            if doorLocator.isEmpty():
                doorLocator = building.find(self.doorRightStr)
        localAvatar.reparentTo(doorLocator)
        localAvatar.setPos(0, 10, 0)
        localAvatar.setHpr(0, 0, 0)
        localAvatar.wrtReparentTo(island)
        localAvatar.setScale(1)
        areaParentWorld = island.getParentObj()
        areaParentWorld.addWorldInterest(island)
        base.loadingScreen.tick()
        base.loadingScreen.tick()
        self.setupOtherSideDoors()
        messenger.send('doorToExteriorFadeIn', [self.getParentObj().uniqueId])
        self.fadeIn()
        base.loadingScreen.tick()
        island.handleEnterGameArea(None)
        base.cr.loadingScreen.hide()
        return

    def handleEnterProximity(self, collEntry):
        DistributedDoor.handleEnterProximity(self, collEntry)

    def getDoorInfo(self):
        geom = self.getParentModel()
        doorList = {'left': [],'right': [],'locator': []}
        for doorStr in doorList:
            nodeList = []
            nodes = geom.findAllMatches('**/door_%s*;+s' % doorStr)
            for i in range(nodes.getNumPaths()):
                if i < 1:
                    doorList[doorStr].append(geom.find('**/door_%s;+s' % doorStr))
                else:
                    doorList[doorStr].append(geom.find('**/door_%s_%d;+s' % (doorStr, i + 1)))

        return doorList

    def getPrompt(self):
        buildingName = PLocalizer.LocationNames.get(self.interiorUId)
        if buildingName:
            return PLocalizer.InteractExitNamedBuilding % buildingName
        return PLocalizer.InteractOpenDoor

    def reparentConnectorToArea(self, area):
        pass
