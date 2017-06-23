from pirates.piratesbase import PiratesGlobals
from pirates.teleport.DoorTeleportActorOV import DoorTeleportActorOV

class ExteriorDoorTeleportActorOV(DoorTeleportActorOV):

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, name='ExteriorDoorTeleportActorOV'):
        DoorTeleportActorOV.__init__(self, cr, name)
        self.doorArriveCallback = None
        return

    def disable(self):
        if self.doorArriveCallback:
            base.cr.relatedObjectMgr.abortRequest(self.doorArriveCallback)
            self.doorArriveCallback = None
        DoorTeleportActorOV.disable(self)
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenGame(self, areaDoId, doorZone, doorId):
        self.areaDoId = areaDoId
        self.doorId = doorId
        world = self.cr.getDo(self.worldDoId)
        world.goOnStage()
        area = self.cr.getDo(areaDoId)
        area.goOnStage()
        if hasattr(area, 'setZoneLevel'):
            area.setZoneLevel(0)

        def doorArrived(door):
            door = self.cr.getDo(self.doorId)
            area = self.cr.getDo(self.areaDoId)
            doorLocator = door.getDoorLocator()
            localAvatar.reparentTo(doorLocator)
            localAvatar.setPosHpr(0, 10, 0, 0, 0, 0)
            localAvatar.wrtReparentTo(area)
            localAvatar.setP(0)
            localAvatar.setR(0)
            localAvatar.setScale(1)
            area.parentObjectToArea(localAvatar)
            area.handleEnterGameArea(None)
            localAvatar.enableGridInterest()
            area.manageChild(localAvatar)
            self.cr.removeTaggedInterest(self.areaInterest)
            self.areaInterest = None
            self._requestWhenInterestComplete('GameOpen')
            self.doorArriveCallback = None
            return

        self.doorArriveCallback = base.cr.relatedObjectMgr.requestObjects([self.doorId], eachCallback=doorArrived)
        self.areaInterest = self.cr.addTaggedInterest(areaDoId, doorZone, self.cr.ITAG_GAME, 'area-temp')

    @report(types=['args'], dConfigParam=['dteleport'])
    def exitOpenGame(self):
        if self.areaInterest:
            self.cr.removeTaggedInterest(self.areaInterest)
            self.areaInterest = None
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterStartShow(self, *args):
        DoorTeleportActorOV.enterStartShow(self, *args)
        door = self.cr.getDo(self.doorId)
        messenger.send('fadeInExteriorDoor', [door.getBuildingUid()])
        base.cr.loadingScreen.hide()