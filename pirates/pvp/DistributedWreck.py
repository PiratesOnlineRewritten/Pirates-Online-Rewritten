from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedNode
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase

class DistributedWreck(DistributedNode.DistributedNode):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWreck')

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedWreck')
        DistributedNode.DistributedNode.__init__(self, cr)

    def generate(self):
        DistributedNode.DistributedNode.generate(self)

    def announceGenerate(self):
        DistributedNode.DistributedNode.announceGenerate(self)
        self.model = loader.loadModel('models/shipparts/merchantL2-geometry_High')
        self.model.reparentTo(self)
        self.model.setColorScale(1, 1, 1, 1, 1)
        self.addCollision()
        self.reparentTo(self.cr.activeWorld.worldGrid)

    def disable(self):
        DistributedNode.DistributedNode.disable(self)
        self.model.removeNode()
        del self.model

    def addCollision(self):
        cSphere = CollisionSphere(0.0, 0.0, 0.0, 200)
        cSphere.setTangible(0)
        cSphereNode = CollisionNode('wreckSphere')
        cSphereNode.setTag('objType', str(PiratesGlobals.COLL_AV))
        cSphereNode.setTag('avId', str(self.doId))
        cSphereNode.addSolid(cSphere)
        cSphereNode.setFromCollideMask(BitMask32.allOff())
        cSphereNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask | PiratesGlobals.RadarShipBitmask)
        cSphereNodePath = self.attachNewNode(cSphereNode)

    def sink(self):
        sinking = Sequence(LerpPosInterval(self, duration=10, startPos=self.getPos(), pos=self.getPos() - Point3(0, 0, 70), blendType='easeIn', name='SunkSinkLerp'), Func(self.hide), Func(self.removeNode)).start()

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def setValue(self, value):
        self.value = value

    def setStatus(self, status):
        self.status = status

    def getTeam(self):
        return 0