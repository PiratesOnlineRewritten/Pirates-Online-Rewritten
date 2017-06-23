from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import DelayedCall, makeList
from direct.showbase.DirectObject import DirectObject
from pirates.pirate import AvatarTypes
from pirates.cutscene import CutsceneData, CutsceneActor, CutsceneIvals
from pirates.effects.CameraShaker import CameraShaker
from direct.gui.DirectGui import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import TimeOfDayManager, TODGlobals
from direct.task import Task

class Cutscene(NodePath, DirectObject):
    notify = directNotify.newCategory('Cutscene')

    def __init__(self, cr, cutsceneName, doneCallback=None, giverId=None):
        self._destroyed = False
        self.cr = cr
        self._serial = serialNum()
        self._ival = None
        self._data = CutsceneData.CutsceneData[cutsceneName]
        NodePath.__init__(self, 'Cutscene(%s)' % self.getName())
        self.cutsceneName = cutsceneName
        self.showTimer = False
        self.timerStartTime = 0
        self.timerTotalPauseTime = 0
        self.timerPauseTime = 0
        self.allowSkip = True
        self.initialize(doneCallback, giverId)
        self._loadActors()
        self._loadSound()
        self.startedCallback = None
        self.setShowTimer(self.showTimer)
        self.delayedStarts = []
        return

    def initialize(self, doneCallback=None, giverId=None, patch=False):
        self._callback = doneCallback
        originNode = None
        if self.cr is not None:
            self.cr.currentCutscene = self
            originNode = self.cr.activeWorld.getCutsceneOriginNode(self.cutsceneName)
        if originNode is not None:
            if 'localAvatar' in __builtins__:
                if localAvatar.ship:
                    self.reparentTo(render)
                    self.setPos(originNode.getPos(render))
                else:
                    self.reparentTo(originNode)
                    self.clearMat()
        else:
            giverObject = None
            if giverId:
                giverObject = self.cr.doId2do.get(giverId)
            if giverObject and giverObject.getParent().getParent().getName() == 'GameArea':
                self.reparentTo(giverObject.getParent().getParent())
            else:
                if 'localAvatar' in __builtins__:
                    if localAvatar.ship:
                        self.reparentTo(render)
                        self.setPos(localAvatar.ship.getPos(render))
                    else:
                        self.reparentTo(localAvatar.getParent().getParent())
                else:
                    self.reparentTo(render)
                self.forceOriginNode()
            self.getEnvEffects()
            self.oldTodState = None
            if self.envEffects and self._data.id == CutsceneData.Cutscene2_2:
                if self.cr:
                    self.oldTodState = self.cr.timeOfDayManager.environment
                    self.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_OFF)
                    self.gameArea.builder.turnOnLights()
                else:
                    self.oldTodState = base.pe.todManager.getTimeOfDayState()
                    base.pe.disableTOD()
            if self.cr and localAvatar.ship:
                self.addFlatWell()
            if base.config.GetBool('cutscene-axis'):
                self._axis = loader.loadModel('models/misc/xyzAxis')
                self._axis.reparentTo(self)
            if patch:
                self.patch()
        return

    def patch(self):
        for actor in self._actors:
            if actor.Uid:
                actor.handleModelHiding()

    def getEnvEffects(self):
        self.envEffects = None
        if self.cr:
            ga = localAvatar.getParentObj()
            if ga and hasattr(ga, 'envEffects'):
                self.envEffects = ga.envEffects
                self.gameArea = ga
        else:
            self.envEffects = base.pe.envEffects
        return

    def setShowTimer(self, showTimer):
        if showTimer:
            if not hasattr(self, 'timer'):
                self.timer = DirectLabel(parent=render2d, pos=(0.0, 0, 0.9), frameSize=(0,
                                                                                        0.16,
                                                                                        0,
                                                                                        0.12), text='0.0', text_align=TextNode.ARight, text_scale=0.05, text_pos=(0.15,
                                                                                                                                                                  0.05), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
        elif hasattr(self, 'timer'):
            self.timer.removeNode()
            self.timer = None
        return

    def addFlatWell(self):
        water = None
        if self.cr is not None:
            water = self.cr.activeWorld.getWater()
        if water:
            water.patch.addFlatWell(self.getName(), self, 0, 0, 400, 400 + 200)
        return

    def destroy(self):
        if self._destroyed:
            return
        self._destroyed = True
        if hasattr(self, '_axis'):
            self._axis.removeNode()
            del self._axis
        if self._ival:
            self._ival.finish()
            base.sfxManagerList[0].stopAllSounds()
        self._ival = None
        for currDelayedStart in self.delayedStarts:
            currDelayedStart.destroy()

        self.delayedStarts = []
        water = None
        if self.cr is not None and self.cr.activeWorld is not None:
            water = self.cr.activeWorld.getWater()
        if water:
            water.patch.removeFlatWell(self.getName())
        self._unloadActors()
        self._unloadSound()
        del self._serial
        self.removeNode()
        if hasattr(self, 'timer'):
            self.timer.removeNode()
            self.timer = None
        self.ignore('cutscene-finish')
        return

    def getName(self):
        return '%s-%s' % (self._data.id, self._serial)

    def getDoneEvent(self):
        return '%s-done' % self.getName()

    def setCallback(self, callback):
        self._callback = callback

    def getActor(self, actorKey):
        return self._actorKey2actor[actorKey]

    def forceOriginNode(self):
        if self.cr is None:
            self.setPos(render, 0, 0, 0)
        if self._data.id == CutsceneData.Cutscene1_1_5_a:
            self.setPos(render, 1.5, 34.837, 1.082)
        elif self._data.id == CutsceneData.Cutscene1_1_5_b:
            self.setPos(render, 1.5, 34.837, 1.082)
        elif self._data.id == CutsceneData.Cutscene1_1_5_c:
            self.setPos(render, 1.5, 34.837, 1.082)
        elif self._data.id == CutsceneData.Cutscene2_2:
            self.setPos(-393.0, -487.0, 5.406)
        elif self._data.id == CutsceneData.Cutscene3_1:
            self.setPos(253.226, -430.155, 1.241)
            self.setH(120.39)
        return

    def _loadActors(self):
        cutCam = CutsceneActor.CutCam(self._data)
        locators = CutsceneActor.CutLocators(self._data)
        self._locators = locators
        self._locators.setOrigin(self)
        self.notify.debug('cutscene origin %s' % self.getPos())
        self._actors = [cutCam, locators]
        for ctor in self._data.actorFunctors:
            self._actors.append(ctor(self._data))

        self._actorKey2actor = {}
        for actor in self._actors:
            self._actorKey2actor[actor.getThisActorKey()] = actor

    def _unloadActors(self):
        del self._actorKey2actor
        for actor in self._actors:
            actor.destroy()

        del self._locators
        del self._actors

    def getActor(self, actorKey):
        return self._actorKey2actor[actorKey]

    def _loadSound(self):
        self._sounds = []
        for soundFile in makeList(self._data.soundFile):
            self._sounds.append(loader.loadSfx(soundFile))

    def _unloadSound(self):
        del self._sounds

    def _startCutscene(self):
        if not base.win.getGsg():
            self.skipNow()
            return
        if self.cr:
            localAvatar.stopCombatMusic()
            base.musicMgr.requestCurMusicFadeOut(1.0, 0.0)
        aspect2d.hide()
        for actor in self._actors:
            actor.startCutscene(self._locators)

        CameraShaker.setCutsceneScale(0.1)
        self.acceptOnce('escape', self._skip)
        if self.startedCallback:
            self.startedCallback()
        render.prepareScene(base.win.getGsg())

    def _skip(self):
        if self.allowSkip:
            self._ival.finish()
            base.sfxManagerList[0].stopAllSounds()
            messenger.send('cutscene-skipped')
        else:
            messenger.send('cutscene-not-skipped')

    def skipNow(self):
        self._ival.finish()
        base.sfxManagerList[0].stopAllSounds()
        messenger.send('cutscene-skipped')

    def _finishCutscene(self):
        if self.cr:
            if base.musicMgr.current:
                vol = base.musicMgr.current.volume
                base.musicMgr.requestCurMusicFadeIn(3.0, vol)
        self.ignore('escape')
        CameraShaker.clearCutsceneScale()
        for actor in self._actors:
            actor.finishCutscene()

        base.sfxManagerList[0].stopAllSounds()
        aspect2d.show()
        if self.oldTodState:
            if self.cr:
                self.cr.timeOfDayManager.setEnvironment(self.oldTodState)
            else:
                base.pe.changeTimeOfDay()
        messenger.send('cutscene-finish')

    def startTimer(self):
        self._resetTimer()
        taskMgr.add(self.updateTimer, 'cutsceneTimerUpdate')
        self.acceptOnce('cutscene-finish', self.stopTimer)

    def stopTimer(self):
        taskMgr.remove('cutsceneTimerUpdate')

    def updateTimer(self, task=None):
        if self._ival.isPlaying():
            totalPlayTime = globalClock.getRealTime() - self.timerStartTime - self.timerTotalPauseTime
            self.timer['text'] = '%.2f' % totalPlayTime
        return Task.cont

    def play(self):
        self._ival = Sequence()
        self._ival.extend((Func(self._startCutscene),))
        scene = Parallel()
        seqDuration = None
        for actor in self._actors:
            scene.append(actor.getInterval(duration=seqDuration))

        if self.showTimer:
            scene.append(Func(self.startTimer))
        ivalFunc = CutsceneIvals.CutsceneIvals.get(self._data.id)
        if ivalFunc is not None:
            bodyIval, endIval = ivalFunc(self)
            scene.append(bodyIval)
        self._ival.append(scene)
        if ivalFunc is not None:
            self._ival.append(endIval)
        self._ival.append(Func(self._finishCutscene))
        if self._callback is not None:
            self._ival.append(Func(self._callback))
        seqDuration = scene.getDuration()
        print 'seqDuration = %s' % seqDuration
        for sound in self._sounds:
            scene.append(SoundInterval(sound, duration=seqDuration))

        self.delayedStarts.append(DelayedCall(self._ival.start, 'cutscene-start-sync', delay=0.001))
        self.delayedStarts.append(DelayedCall(self._ival.pause, 'cutscene-start-sync', delay=1))
        self.delayedStarts.append(DelayedCall(self._ival.resume, 'cutscene-start-sync', delay=1.01))
        return

    def isPlaying(self):
        return self._ival and self._ival.isPlaying()

    def _resetTimer(self):
        self.timerStartTime = globalClock.getRealTime()
        self.timerTotalPauseTime = 0
        self.timerPauseTime = globalClock.getRealTime()

    def pause(self):
        if self._ival:
            self._ival.pause()
            self.timerPauseTime = globalClock.getRealTime()

    def resume(self):
        if self._ival:
            self.timerTotalPauseTime += globalClock.getRealTime() - self.timerPauseTime
            self._ival.resume()

    def restart(self):
        if self._ival:
            self._resetTimer()
            self._ival.setT(0)

    def overrideOldAvState(self, avState):
        localAvActor = self.getActor(CutsceneActor.CutLocalPirate.getActorKey())
        localAvActor.setOldAvState(avState)

    def setStartCallback(self, callback):
        self.startedCallback = callback