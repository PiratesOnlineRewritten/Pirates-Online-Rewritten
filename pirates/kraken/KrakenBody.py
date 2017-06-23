from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.creature.Creature import Creature
from pirates.kraken.BodyGameFSM import BodyGameFSM
from pirates.piratesbase import PiratesGlobals
from pandac.PandaModules import *

class KrakenBody(Creature):
    ModelInfo = ('models/char/live_kraken_zero', 'models/char/live_kraken_zero')
    AnimList = {}

    def __init__(self):
        Creature.__init__(self)
        self.enableMixing()
        self.collideBattleMask = PiratesGlobals.TargetBitmask | PiratesGlobals.BattleAimBitmask

    def setupCollisions(self):
        from pandac.PandaModules import *
        coll = CollisionSphere((0, 0, 0), 1)
        cn = CollisionNode('KrakenCollisions')
        cn.addSolid(coll)
        self.collision = self.attachNewNode(cn)
        self.collision.node().setIntoCollideMask(self.collideBattleMask)
        self.collision.setScale(100)
        self.collision.setZ(-80)
        self.collision.flattenStrong()

    def generateCreature(self):
        self.loadModel(ModelInfo[0])
