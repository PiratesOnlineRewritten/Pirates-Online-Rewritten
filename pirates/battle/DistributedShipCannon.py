from direct.showbase.PythonUtil import quickProfile
from pirates.shipparts import DistributedShippart
from pirates.shipparts import CannonDNA
from direct.task import Task
from pandac.PandaModules import *
import DistributedPCCannon
import DistributedWeapon
import Cannon

class DistributedShipCannon(DistributedPCCannon.DistributedPCCannon, DistributedShippart.DistributedShippart):

    def __init__(self, cr):
        DistributedPCCannon.DistributedPCCannon.__init__(self, cr)
        DistributedShippart.DistributedShippart.__init__(self, cr)
        self.ship = None
        self.pendingPlaceCannon = None
        return

    def generate(self):
        self.setDefaultDNA()
        DistributedPCCannon.DistributedPCCannon.generate(self)
        DistributedShippart.DistributedShippart.generate(self)

    def announceGenerate(self):
        DistributedWeapon.DistributedWeapon.announceGenerate(self)
        DistributedShippart.DistributedShippart.announceGenerate(self)
        if self.proximityCollisionNodePath:
            self.proximityCollisionNodePath.reparentTo(self.prop.propCollisions)
        self.accept(self.ship.uniqueName('shipSinking'), self.shipSinking)
        self.accept(self.ship.uniqueName('disable'), self.shipDisable)
        self.cannonExitEvent = self.ship.uniqueName('stopCannon')
        self.setAllowInteract(1)

    def disable(self):
        if self.pendingPlaceCannon:
            base.cr.relatedObjectMgr.abortRequest(self.pendingPlaceCannon)
            self.pendingPlaceCannon = None
        self.ignore(self.ship.uniqueName('shipSinking'))
        self.ignore(self.ship.uniqueName('disable'))
        DistributedPCCannon.DistributedPCCannon.disable(self)
        DistributedShippart.DistributedShippart.disable(self)
        return

    def delete(self):
        if self.ship.cannons.get(self.cannonIndex, 0):
            self.ship.cannons[self.cannonIndex][1] = None
        del self.dna
        self.ship = None
        DistributedPCCannon.DistributedPCCannon.delete(self)
        DistributedShippart.DistributedShippart.delete(self)
        return

    def createProp(self):
        cannon = self.ship.cannons.get(self.cannonIndex, 0)
        if cannon:
            if cannon[0]:
                self.prop = cannon[0]
                self.ship.cannons[self.cannonIndex][1] = self
                return
        self.prop = Cannon.Cannon(self.cr, True)
        self.ship.cannons[self.cannonIndex] = [self.prop, self]

    def cleanupProp(self):
        self.prop = None
        return

    def loadModel(self):
        self.prop.cannonPost = self.ship.findLocator('**/cannon_%s;+s' % self.cannonIndex)
        self.prop.shipId = self.shipId
        self.prop.doId = self.doId
        self.prop.reparentTo(self)
        self.prop.loadModel(self.dna)

    def setupParent(self, parent):
        DistributedShippart.DistributedShippart.setupParent(self, parent)

    def linkToShip(self, ship):
        ship.cannons.append(self)
        self.ship = ship
        DistributedShippart.DistributedShippart.linkToShip(self, ship)

    def setShipId(self, shipId):
        self.shipId = shipId

        def putCannonOnShip(ship, self=self):
            self.ship = ship

        self.pendingPlaceCannon = base.cr.relatedObjectMgr.requestObjects([self.shipId], eachCallback=putCannonOnShip)

    def setGeomParentId(self, geomParentId):
        self.geomParentId = geomParentId

    def setCannonIndex(self, cannonIndex):
        self.cannonIndex = cannonIndex

    def shipSinking(self):
        if self.localAvatarUsingWeapon:
            self.stopWeapon(base.localAvatar)

    def shipDisable(self):
        if self.localAvatarUsingWeapon:
            self.ignore('escape')
            self.ignore(self.cannonExitEvent)
            self.modeFSM.request('off')
            base.cannon = None
            self.av = None
            self.prop.av = None
            self.setLocalAvatarUsingWeapon(0)
        return

    def enterFireCannon(self):
        DistributedPCCannon.DistributedPCCannon.enterFireCannon(self)
        base.localAvatar.controlManager.collisionsOn()
        if self.ship:
            keel = self.ship.find('**/keel')
            if not keel.isEmpty():
                keel.hide()

    def exitFireCannon(self):
        DistributedPCCannon.DistributedPCCannon.exitFireCannon(self)
        base.localAvatar.controlManager.collisionsOff()
        if self.ship:
            keel = self.ship.find('**/keel')
            if not keel.isEmpty():
                keel.show()

    def loadTargetIndicator(self):
        DistributedPCCannon.DistributedPCCannon.loadTargetIndicator(self)
        if self.isGenerated():
            self.disk.reparentTo(self.ship.getHighDetail())
            self.disk.setPos(self.prop.cannonPost.getPos(self.ship.getModelRoot()))

    def setDefaultDNA(self):
        newDNA = CannonDNA.CannonDNA()
        self.setDNA(newDNA)

    def setDNA(self, dna):
        if self.dna:
            self.updateDNA(dna)
        else:
            self.dna = dna

    def updateDNA(self, newDNA, fForce=0):
        oldDna = self.dna
        self.dna = newDNA

    def setBaseTeam(self, val):
        self.dna.setBaseTeam(val)

    def setCannonType(self, val):
        self.dna.setCannonType(val)

    def addPropToShip(self):
        pass

    def enterFireCannon(self):
        self.ship.avCannonNode.setPos(self.prop.cannonPost.getPos(self.ship.getModelRoot()))
        self.ship.avCannonNode.setHpr(self.prop.cannonPost.getHpr(self.ship.getModelRoot()))
        self.ship.avCannonRotate.setPos(0, 0, 4)
        self.ship.avCannonRotate.setHpr(0, 0, 0)
        self.ship.avCannonPivot.setPos(0, 6, 0)
        DistributedPCCannon.DistributedPCCannon.enterFireCannon(self)

    def startWeapon(self, av):
        if av == base.localAvatar:
            if base.localAvatar.cannon:
                return
            base.localAvatar.b_setGameState('Cannon')
            self.acceptInteraction()
            self.setLocalAvatarUsingWeapon(1)
            base.localAvatar.cannon = self
            if self.ship:
                self.ship.hideMasts()
                self.ship.hideSmoke()
                self.ship.listenForFloorEvents(0)
            localAvatar.guiMgr.request('MouseLook')
            self.modeFSM.request('fireCannon')
            base.localAvatar.collisionsOn()
        self.prop.hNode.setHpr(0, 0, 0)
        self.prop.pivot.setHpr(0, 0, 0)
        shipH = (self.ship.getH(self.prop) + 360) % 360
        self.prop.shipH = shipH
        self.prop.oldShipH = shipH
        self.prop.currentHpr = (shipH, 0, 0)
        av.stopSmooth()
        av.setPos(self.prop.cannonPost, 0, -2.5, 0)
        av.setHpr(self.prop.cannonPost, 0, 0, 0)
        av.play('kneel_fromidle', toFrame=16)
        self.av = av
        self.prop.av = av
        if av:
            av.stopCompassEffect()

    def stopWeapon(self, av, fromDefeat=0):
        if av == base.localAvatar:
            self.ship.showSmoke()
            self.ship.showMasts()
            self.ship.listenForFloorEvents(1)
        if av:
            av.startCompassEffect()
        DistributedPCCannon.DistributedPCCannon.stopWeapon(self, av, fromDefeat)