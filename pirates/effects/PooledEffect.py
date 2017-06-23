from pandac.PandaModules import *
from direct.showbase import Pool
from direct.showbase.DirectObject import DirectObject
import re

class PooledEffect(DirectObject, NodePath):
    GlobalCount = 0
    GlobalLimit = 200
    pool = None
    poolLimit = 30

    @classmethod
    def getEffect(cls, unlimited=False, context=''):
        if cls.pool is None:
            cls.pool = Pool.Pool()
        if unlimited or PooledEffect.GlobalCount < PooledEffect.GlobalLimit:
            if cls.pool.hasFree():
                PooledEffect.GlobalCount += 1
                return cls.pool.checkout()
            else:
                free, used = cls.pool.getNumItems()
                if free + used < cls.poolLimit:
                    PooledEffect.GlobalCount += 1
                    cls.pool.add(cls())
                    return cls.pool.checkout()
        return

    @classmethod
    def checkInEffect(cls, item):
        if cls.pool and cls.pool.isUsed(item):
            PooledEffect.GlobalCount -= 1
            cls.pool.checkin(item)

    @classmethod
    def cleanup(cls):
        if cls.pool:
            cls.pool.cleanup(cls.destroy)
            cls.pool = None
        return

    @classmethod
    def setGlobalLimit(cls, limit):
        PooledEffect.GlobalLimit = limit

    def __init__(self):
        NodePath.__init__(self, self.__class__.__name__)
        self.accept('clientLogout', self.__class__.cleanup)

    def destroy(self, item=None):
        if item:
            self.pool.remove(item)
        self.ignore('clientLogout')
        self.removeNode()