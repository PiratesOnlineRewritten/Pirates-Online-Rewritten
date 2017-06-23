from direct.distributed import DistributedObject

class PiratesTutorialManager(DistributedObject.DistributedObject):
    notify = directNotify.newCategory('PiratesTutorialManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def disable(self):
        self.ignoreAll()
        DistributedObject.DistributedObject.disable(self)

    def enterTutorial(self, tutorialZone):
        messenger.send('startTutorial', [self.doId, tutorialZone])