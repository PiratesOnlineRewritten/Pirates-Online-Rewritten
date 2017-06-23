from pandac.PandaModules import AudioSound
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import LerpFunc, Sequence
from direct.showbase.DirectObject import DirectObject

class AmbientSound():
    notify = DirectNotifyGlobal.directNotify.newCategory('AmbientSound')

    def __init__(self, path, masterAmbientVolume, loop=True, isMusic=False):
        self.isMusic = isMusic
        if self.isMusic:
            self.sfx = loader.loadMusic(path)
        else:
            self.sfx = loader.loadSfx(path)
        self.path = path
        self.loop = loop
        self.setLoop(loop)
        self.setVolume(0)
        self.masterAmbientVolume = masterAmbientVolume
        self.reloadAttempt = 0
        self.curPriority = 0
        self.duration = 0
        self.finalVolume = 0
        self.startVolume = 0
        self.activeInterval = None
        return

    def unload(self):
        if self.activeInterval:
            self.activeInterval.finish()
        del self.activeInterval
        self.sfx.stop()
        del self.sfx

    def play(self):
        self.sfx.play()

    def getVolume(self):
        return self.sfx.getVolume()

    def setVolume(self, vol):
        self.sfx.setVolume(vol)

    def getLoop(self):
        return self.sfx.getLoop()

    def setLoop(self, loop):
        self.sfx.setLoop(loop)

    def set3dAttributes(self, *args):
        self.sfx.set3dAttributes(*args)

    def requestChangeVolume(self, duration, finalVolume, priority):
        if priority < self.curPriority:
            return
        self.curPriority = priority
        if not self.sfx.getActive():
            if self.reloadAttempt < 1:
                self.reloadAttempt += 1
                if self.isMusic:
                    self.sfx = loader.loadMusic(self.path)
                else:
                    self.sfx = loader.loadSfx(self.path)
                if self.sfx:
                    self.sfx.setLoop(self.loop)
        self.duration = duration
        self.startVolume = self.getVolume()
        self.finalVolume = finalVolume
        if self.activeInterval:
            self.activeInterval.pause()
            del self.activeInterval
        self.activeInterval = Sequence(LerpFunc(self.changeVolumeTask, fromData=self.startVolume, toData=self.finalVolume, duration=self.duration))
        self.activeInterval.start()

    def changeMasterAmbientVolume(self, newMasterAmbientVolume):
        if not self.masterAmbientVolume == newMasterAmbientVolume:
            self.masterAmbientVolume = newMasterAmbientVolume
            if self.activeInterval and self.activeInterval.isPlaying():
                pass
            elif self.sfx.status() == 2:
                newVol = float(self.finalVolume) * self.masterAmbientVolume
                self.sfx.setVolume(newVol)

    def changeVolumeTask(self, t):
        curVolume = t * self.masterAmbientVolume
        self.sfx.setVolume(curVolume)
        if not hasattr(self, 'reportCounter'):
            self.reportCounter = 0
        self.reportCounter += 1
        if self.reportCounter % 10 == 0:
            pass
        if curVolume > 0 and self.sfx.status() == 1:
            self.sfx.play()
        if curVolume <= 0 and self.sfx.status() == 2:
            self.sfx.stop()
            self.curPriority = 0


class AmbientManagerBase(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('AmbientManagerBase')

    def __init__(self):
        self.ambientDict = {}
        self.masterAmbientVolume = 1.0

    def load(self, name, path, looping=True, isMusic=False):
        retval = False
        if self.ambientDict.has_key(name):
            if self.ambientDict[name].path == path:
                self.notify.warning('ambient name=%s path=%s already loaded' % (name, path))
            else:
                self.notify.warning('ambient name %s is already bound to %s' % self.ambientDict[name].path)
        else:
            newAmbient = AmbientSound(path, self.masterAmbientVolume, looping, isMusic)
            self.ambientDict[name] = newAmbient

    def unload(self, name):
        if self.ambientDict.has_key(name):
            self.ambientDict[name].unload()
            del self.ambientDict[name]
        else:
            self.notify.warning('music: %s not in ambientDict' % name)

    def requestFadeIn(self, name, duration=5, finalVolume=1.0, priority=0):
        self.requestChangeVolume(name, duration, finalVolume, priority)

    def requestFadeOut(self, name, duration=5, finalVolume=0.0, priority=0):
        self.requestChangeVolume(name, duration, finalVolume, priority)

    def requestChangeVolume(self, name, duration, finalVolume, priority=0):
        if self.ambientDict.has_key(name):
            self.ambientDict[name].requestChangeVolume(duration, finalVolume, priority)

    def delete(self):
        for name in self.ambientDict.keys():
            self.ambientDict[name].unload()

        self.ambientDict = {}

    def silence(self):
        for name in self.ambientDict.keys():
            self.ambientDict[name].requestChangeVolume(0.0, 0.0, priority=1)

    def changeMasterAmbientVolume(self, newMasterAmbientVolume):
        if not newMasterAmbientVolume == self.masterAmbientVolume:
            self.masterAmbientVolume = newMasterAmbientVolume
            for name in self.ambientDict.keys():
                self.ambientDict[name].changeMasterAmbientVolume(self.masterAmbientVolume)