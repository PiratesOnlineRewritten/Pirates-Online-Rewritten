from direct.directnotify.DirectNotifyGlobal import giveNotify
import PiratesGlobals

class PiratesPreloader(object):

    def __init__(self):
        self.baseLoadCounter = 0
        self.preloadPool = []
        self.doLoad()

    def doLoad(self):
        if self.baseLoadCounter >= len(PiratesGlobals.preLoadSet):
            return
        loader.loadModel(PiratesGlobals.preLoadSet[self.baseLoadCounter], callback=self.callback)

    def callback(self, model):
        self.preloadPool.append(model)
        self.baseLoadCounter += 1
        self.doLoad()


giveNotify(PiratesPreloader)