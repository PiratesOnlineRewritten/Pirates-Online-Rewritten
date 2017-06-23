from direct.distributed.DistributedObject import DistributedObject
from GameStatManagerBase import GameStatManagerBase

class DistributedGameStatManager(DistributedObject, GameStatManagerBase):
    from direct.directnotify import DirectNotifyGlobal
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameStatManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        GameStatManagerBase.__init__(self)
        self.aggroModelIndex = None
        base.gsm = self
        return

    def generate(self):
        self.cr.gameStatManager = self
        DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

    def disable(self):
        GameStatManagerBase.disable(self)
        DistributedObject.disable(self)
        self.ignoreAll()
        if self.cr.gameStatManager == self:
            self.cr.gameStatManager = None
        return

    def delete(self):
        GameStatManagerBase.delete(self)
        DistributedObject.delete(self)
        base.gsm = None
        return

    def setAggroModelIndex(self, modelIndex):
        self.aggroModelIndex = modelIndex
        messenger.send('SwitchAgrroModel')

    def getAggroModelIndex(self):
        return self.aggroModelIndex

    def loadSoundList(self):
        try:
            soundFile = open('SoundList.txt', 'r')
        except:
            return

        lineList = soundFile.readlines()
        newDict = {}
        for soundLine in lineList:
            tokens = soundLine.split()
            name = str(tokens[0])
            value = int(tokens[1])
            newDict[name] = value

        loader.addSoundListDict(newDict)

    def saveSoundList(self):
        soundFile = open('SoundList.txt', 'w')
        soundDict = loader.getSoundListDict()
        soundNameList = soundDict.keys()
        soundNameList.sort()
        for soundName in soundNameList:
            outString = '%s %s\n' % (soundName, soundDict[soundName])
            soundFile.write(outString)

        soundFile.close()