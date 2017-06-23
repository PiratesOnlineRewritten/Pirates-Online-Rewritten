from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.audio import AmbientManagerBase
from pirates.uberdog import UberDogGlobals
from pirates.audio import SoundGlobals

class MusicManager(AmbientManagerBase.AmbientManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('MusicManager')

    class MusicData():

        def __init__(self, name, priority=0, looping=1, volume=0.8):
            self.name = name
            self.priority = priority
            self.looping = looping
            self.volume = volume

    def __init__(self):
        AmbientManagerBase.AmbientManagerBase.__init__(self)
        self.current = None
        self.playlist = []
        self.wantMusic = base.config.GetBool('audio-music-active', 1)
        self.accept('PandaRestarted', self.requestCurMusicFadeIn)
        return

    def delete(self):
        AmbientManagerBase.AmbientManagerBase.delete(self)
        self.ignore('PandaRestarted')
        self.current = None
        self.playlist = []
        return

    def load(self, name, looping=True):
        path = 'audio/' + name
        AmbientManagerBase.AmbientManagerBase.load(self, name, path, isMusic=True, looping=looping)
        if self.ambientDict[name].sfx == None:
            self.notify.warning('music: %s failed to load' % name)
            del self.ambientDict[name]
            return 0
        return 1

    def unload(self, name):
        AmbientManagerBase.AmbientManagerBase.unload(self, name)
        if self.current and self.current.name == name:
            self.current = None
        for song in self.playlist:
            if song.name == name:
                self.playlist.remove(song)
                break

        return

    def request(self, name, priority=0, looping=True, volume=0.8):
        if not self.ambientDict.has_key(name):
            if not self.load(name, looping):
                return
        found = 0
        for song in self.playlist:
            if song.name == name:
                song.priority = priority
                found = 1

        if found == 0:
            song = self.MusicData(name, priority, looping, volume)
            self.playlist.append(song)
        self.update()

    def stop(self, name):
        if self.current:
            if self.current.name == name:
                self.requestFadeOut(name, 0, removeFromPlaylist=True)
                self.current = None
        for song in self.playlist:
            if song.name == name:
                self.playlist.remove(song)
                break

        self.update()
        return

    def update(self):
        self.notify.debug('playlistLength = %d' % len(self.playlist))
        if len(self.playlist) == 0:
            return

        def compFunc(a, b):
            if a.priority < b.priority:
                return 1
            elif a.priority > b.priority:
                return -1
            return 0

        self.playlist.sort(compFunc)
        self.notify.debug('playlist == ')
        for musicData in self.playlist:
            self.notify.debug('    musicData=%s' % musicData.name)

        if self.current == self.playlist[0]:
            return
        elif self.current != None:
            if self.ambientDict[self.current.name].finalVolume > 0:
                self.notify.debug('calling requestFadeOut on %s' % self.current.name)
                self.requestFadeOut(self.current.name, removeFromPlaylist=False)
        self.current = self.playlist[0]
        if self.wantMusic:
            songLength = SoundGlobals.getMusicLength(self.current.name)
            if self.current.looping == False:
                if songLength is not None:
                    taskMgr.doMethodLater(songLength, self.handleCurrentTrackFinished, 'currentTrackFinished', extraArgs=[self.current.name])
                else:
                    self.notify.warning('non-looping song %s has no length!' % self.current.name)
            self.requestFadeIn(self.current.name, finalVolume=self.current.volume)
        return

    def requestFadeOut(self, name, duration=3, finalVolume=0.0, priority=0, removeFromPlaylist=True):
        self.requestChangeVolume(name, duration, finalVolume, priority, removeFromPlaylist)

    def requestChangeVolume(self, name, duration, finalVolume, priority=0, removeFromPlayList=False):
        AmbientManagerBase.AmbientManagerBase.requestChangeVolume(self, name, duration, finalVolume, priority)
        if finalVolume == 0:
            needToDoUpdate = False
            if removeFromPlayList:
                for song in self.playlist:
                    if song.name == name:
                        self.playlist.remove(song)
                        needToDoUpdate = True
                        break

            if needToDoUpdate:
                self.notify.debug('requestChangeVolume doing update')
                self.update()

    def requestCurMusicFadeOut(self, duration=3, finalVolume=0.0, removeFromPlaylist=False, priority=0):
        if self.playlist and self.current:
            curMusic = self.current.name
            self.requestFadeOut(curMusic, duration, finalVolume, removeFromPlaylist=removeFromPlaylist, priority=priority)

    def requestCurMusicFadeIn(self, duration=3.0, finalVolume=1.0):
        if self.playlist and self.current:
            curMusic = self.current.name
            self.requestFadeIn(curMusic, duration, finalVolume)

    def handleCurrentTrackFinished(self, task=None, name=None):
        if name:
            self.requestFadeOut(name, duration=0, removeFromPlaylist=True)
        else:
            self.requestCurMusicFadeOut(duration=0, removeFromPlaylist=True)
        return Task.done

    def offsetMusic(self, offset):
        if self.playlist and self.current:
            curMusic = self.ambientDict[self.current.name]
            if curMusic.activeInterval:
                curMusic.activeInterval.finish()
            curMusic.sfx.stop()
            curMusic.sfx.setTime(offset)
            curMusic.sfx.play()
            if self.current.looping == False:
                taskMgr.remove('currentTrackFinished')
                songLength = SoundGlobals.getMusicLength(self.current.name)
                if songLength is not None:
                    taskMgr.doMethodLater(songLength - offset, self.handleCurrentTrackFinished, 'currentTrackFinished', extraArgs=[self.current.name])
        return