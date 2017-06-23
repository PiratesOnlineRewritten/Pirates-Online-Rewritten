from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from direct.showbase.PythonUtil import *

class DistributedCellDoor(DistributedInteractive.DistributedInteractive):
    notify = directNotify.newCategory('DistributedCellDoor')
    notify.setDebug(0)
    DSUndef = -1
    DSOpen = 0
    DSShut = 1
    OpenSfx = None
    CloseSfx = None

    def __init__(self, cr, name='DistributedCellDoor'):
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        NodePath.__init__(self, name)
        self.doorState = PiratesGlobals.DOOR_CLOSED
        self.doorTrack = None
        self.tOpen = 0.5
        self.health = 0
        self.cellIndex = -1
        self.cellLocatorStr = ''
        self.doorGeomNodePath = None
        self.collisionNodePath = None
        self.collisionPlanarNodePath = None
        self.shutH = 0
        self.openH = 0
        self.open = self.DSUndef
        self.doorTrack = None
        self.kickEvents = []
        return

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        self.setupDoor()
        self.setInteractOptions(proximityText=PLocalizer.InteractKickDoor, diskRadius=9.0, sphereScale=6.0, allowInteract=self.allowInteract)
        self.setHealth(self.health, doAnim=True)
        if localAvatar.getDoId() in self.captives:
            self.collisionPlanarNodePath.unstash()
            self.setAllowInteract(True)
        else:
            self.setAllowInteract(False)

    def disable(self):
        self.ignoreAll()
        self.doorGeomNodePath = None
        self.collisionNodePath = None
        self.collisionPlanarNodePath = None
        if self.doorTrack:
            self.doorTrack.pause()
            self.doorTrack = None
        DistributedInteractive.DistributedInteractive.disable(self)
        return

    def showUseInfo(self):
        localAvatar.guiMgr.workMeter.updateText(PLocalizer.InteractKicking)
        localAvatar.guiMgr.workMeter.update(self.health / 100.0)
        localAvatar.guiMgr.workMeter.show()

    def hideUseInfo(self):
        DistributedInteractive.DistributedInteractive.hideUseInfo(self)
        localAvatar.guiMgr.workMeter.hide()

    def setupDoor(self):
        interior = self.cr.doId2do[self.getLocation()[0]]
        self.doorGeomNodePath = interior.find(self.doorModelStr)
        self.collisionNodePath = interior.find(self.doorCollisionStr)
        self.collisionPlanarNodePath = interior.find(self.doorCollisionPlanarStr)
        self.collisionPlanarNodePath.stash()
        self.shutH = self.doorGeomNodePath.getH()
        self.openH = self.shutH + 120
        self.kickEvents = (
         self.uniqueName('kickStart'), self.uniqueName('kickEnd'))
        self.accept(self.kickEvents[0], self.d_doorKicked)
        self.accept(self.kickEvents[1], self.localDoorKicked)

    def setCaptives(self, avIds):
        self.captives = avIds

    def acceptInteraction(self):
        DistributedInteractive.DistributedInteractive.acceptInteraction(self)
        localAvatar.setKickEvents(*self.kickEvents)
        localAvatar.b_setGameState('DoorKicking')
        localAvatar.cameraFSM.request('FPS')
        if not localAvatar.cameraFSM.getCurrentCamera():
            print '***JCW*** DistributedCellDoor.acceptInteraction'
            print '***JCW*** no current camera'
            localAvatar.printState()
        else:
            oldXform = localAvatar.cameraFSM.getCurrentCamera().getTransform(render)
            localAvatar.lookAt(self)
            localAvatar.setP(0)
            localAvatar.setR(0)
            localAvatar.cameraFSM.getCurrentCamera().setTransform(render, oldXform)

    def rejectInteraction(self):
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)
        localAvatar.b_setGameState('LandRoam')

    def doorShake(self):
        pass

    def doorOpen(self):
        if self.open == self.DSOpen:
            return
        self.setAllowInteract(False)
        self.open = self.DSOpen
        self.collisionNodePath.stash()
        self.collisionPlanarNodePath.stash()
        if self.doorTrack:
            self.doorTrack.pause()
        startHpr = self.doorGeomNodePath.getHpr()
        hpr = Vec3(self.openH, startHpr[1], startHpr[2])
        if not self.OpenSfx:
            self.OpenSfx = loadSfx(SoundGlobals.SFX_DOOR_OPEN_SPANISH)
        self.doorTrack = Sequence(Func(base.playSfx, self.OpenSfx, node=self.doorGeomNodePath), LerpHprInterval(self.doorGeomNodePath, 0.2, hpr=hpr, startHpr=startHpr))
        self.doorTrack.start()

    def doorShut(self):
        if self.open == self.DSShut:
            return
        self.setAllowInteract(True)
        self.open = self.DSShut
        self.collisionNodePath.unstash()
        if self.doorTrack:
            self.doorTrack.pause()
        startHpr = self.doorGeomNodePath.getHpr()
        hpr = Vec3(self.shutH, startHpr[1], startHpr[2])
        if not self.CloseSfx:
            self.CloseSfx = loadSfx(SoundGlobals.SFX_DOOR_SLAM)
        self.doorTrack = Sequence(Func(base.playSfx, self.CloseSfx, node=self.doorGeomNodePath), LerpHprInterval(self.doorGeomNodePath, 0.2, hpr=hpr, startHpr=startHpr))
        self.doorTrack.start()

    def b_doorKicked(self):
        self.d_doorKicked()
        self.localDoorKicked()

    def d_doorKicked(self):
        self.sendUpdate('doorKicked')

    def localDoorKicked(self):
        self.doorShake()

    def setCellIndex(self, index):
        self.cellIndex = index
        self.cellLocatorStr = '**/cell_door_locator_%0.2d' % (index + 1)
        self.doorModelStr = '**/jail_door%0.2d' % (index + 1)
        self.doorCollisionStr = '**/door_collision_%0.2d;+s' % (index + 1)
        self.doorCollisionPlanarStr = '**/door_collision_planar_%0.2d;+s' % (index + 1)

    @report(types=['frameCount', 'args'], dConfigParam='jail')
    def setHealth(self, health, doAnim=False):
        self.health = health
        if self.state == 'Use':
            localAvatar.guiMgr.workMeter.update(health / 100.0)
        if self.isGenerated() or doAnim:
            if self.health > 0:
                self.doorShut()
            else:
                self.doorOpen()