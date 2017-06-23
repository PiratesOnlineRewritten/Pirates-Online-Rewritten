from pirates.piratesbase.PiratesGlobals import *
from direct.interval.IntervalGlobal import *
from direct.interval.AnimControlInterval import AnimControlInterval
from pirates.piratesbase import PiratesGlobals
from pandac.PandaModules import *
from direct.actor import Actor
from pirates.ship import ShipGlobals
from pirates.effects.Bonfire import Bonfire
from pirates.battle.EnemySkills import EnemySkills
CannonPortDict = {InventoryType.CannonL1: 'plain',InventoryType.CannonL2: 'plain',InventoryType.CannonL3: 'plain',InventoryType.CannonL4: 'plain',ShipGlobals.Cannons.BP: 'blackPearl',ShipGlobals.Cannons.Skel_L1: 'skeleton',ShipGlobals.Cannons.Skel_L2: 'skeleton',ShipGlobals.Cannons.Skel_L3: 'skeleton'}
DefaultAnimDict = (
 ('zero', '_zero'), ('Fire', '_fire'), ('Open', '_open'), ('Close', '_close'))

class PortCache():

    def __init__(self, root):
        self.root = root

    def getPort(self):
        root = self.root.copyTo(NodePath())
        char = root.find('+Character')
        lod = char.find('+LODNode')
        controls = []
        charBundle = char.node().getBundle(0)
        return (
         root, char, lod)


class CannonPort(NodePath):
    notify = directNotify.newCategory('cannonPort')
    portModels = {}
    portBundles = []

    def __init__(self, cannonType, side, index):
        NodePath.__init__(self, 'cannonPort')
        if not self.portModels:
            self.setupPortModels()
        self.cannonType = cannonType
        self.side = side
        self.index = index
        self.locator = None
        if side == 0:
            self.skillId = EnemySkills.LEFT_BROADSIDE
        else:
            self.skillId = EnemySkills.RIGHT_BROADSIDE
        self.CannonPortAnimDict = {}
        self._loadModel(self.cannonType)
        self.loaded = False
        self.openIval = Sequence()
        self.fireIval = Sequence()
        self.closeIval = Sequence()
        return

    def _loadModel(self, cannonType):
        root, char, lod = self.portModels[cannonType].getPort()
        self.bundleHandle = char.node().getBundleHandle(0)
        self.root = char
        self.lod = lod
        self.loaded = True

    def delete(self):
        self.removeNode()
        self.ship = None
        return

    def playOpen(self, offset=0):
        self.openIval.start(offset, playRate=2.0)

    def playClosed(self, offset=0):
        self.closeIval.start(offset)

    def playFire(self, offset=0):
        self.fireIval.start(offset)

    def finalize(self):
        self.bundle = self.bundleHandle.getBundle()
        self.openControl = self.bundle.bindAnim(self.portBundles[0], -1)
        self.fireControl = self.bundle.bindAnim(self.portBundles[1], -1)
        self.closeControl = self.bundle.bindAnim(self.portBundles[2], -1)
        self.openIval = Sequence(AnimControlInterval(self.openControl))
        self.fireIval = Sequence(AnimControlInterval(self.fireControl))
        self.closeIval = Sequence(AnimControlInterval(self.closeControl))

    def setupPortModels(self):
        for name in ['open', 'fire', 'close']:
            model = loader.loadModel('models/shipparts/pir_a_shp_can_broadside_%s' % name)
            CannonPort.portBundles.append(model.find('**/+AnimBundleNode').node().getBundle())

        for val, suffix in CannonPortDict.iteritems():
            model = loader.loadModel('models/shipparts/pir_r_shp_can_broadside_%s' % suffix)
            char = model.find('**/+Character')
            root = NodePath('Port')
            high = char.find('**/cannon_port_high')
            med = char.find('**/cannon_port_med')
            low = char.find('**/cannon_port_low')
            for node in char.findAllMatches('**/+ModelNode'):
                node.node().setPreserveTransform(ModelNode.PTDropNode)

            high.detachNode()
            med.detachNode()
            low.detachNode()
            char.node().removeAllChildren()
            lod = LODNode('lodRoot')
            lod.addSwitch(200, 0)
            lod.addSwitch(500, 200)
            lod.addSwitch(100000, 500)
            lod = NodePath(lod)
            high.reparentTo(lod)
            med.reparentTo(lod)
            low.reparentTo(lod)
            lod.reparentTo(char)
            char.flattenStrong()
            char.reparentTo(root)
            portModel = PortCache(root)
            CannonPort.portModels[val] = portModel