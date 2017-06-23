from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import PythonUtil
from direct.fsm import FSM
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiTray
from pirates.piratesgui import PiratesGuiGlobals
from pirates.minigame import BishopsHandGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfxString
from math import atan2
from random import randint

class Hand(NodePath):

    def __init__(self, *args, **kwargs):
        NodePath.__init__(self, *args, **kwargs)
        model = loader.loadModel('models/props/BH_images')
        shadow = model.find('**/*hand_shadow')
        shadow.setScale(-1, 1, 1)
        shadow.reparentTo(self)
        hand = model.find('**/*hand')
        hand.setScale(-1, 1, 1)
        hand.reparentTo(self)


class Burn(DirectFrame):

    def __init__(self, *args, **kwargs):
        DirectFrame.__init__(self, *args, **kwargs)
        self.initialiseoptions(Burn)
        model = loader.loadModel('models/props/BH_burn')
        cm = CardMaker('Burns')
        cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        self.rings = []
        for x in range(3):
            cm.setName(`x` + '-back')
            c = NodePath(cm.generate())
            c.setTexture(model.findTexture('BH_burn_' + `(x + 1)` + '_b'))
            back = DirectFrame(parent=self, relief=None, geom=c)
            back.setColorScale(1, 1, 1, 0)
            back.setTransparency(True)
            cm.setName(`x` + '-front')
            c = NodePath(cm.generate())
            c.setTexture(model.findTexture('BH_burn_' + `(x + 1)` + '_f'))
            front = DirectFrame(parent=self, relief=None, geom=c)
            front.setColorScale(0, 0, 0, 0)
            front.setTransparency(True)
            self.rings.append([back, front])

        return

    def burnIn(self, ring=None, time=0.25, light=True):
        if ring != None:
            rings = range(3)[:ring + 1]
            rings = [ring]
        else:
            rings = range(3)
        par = Parallel()
        for r in rings:
            front = self.rings[r][1]
            back = self.rings[r][0]
            seqFront = Sequence()
            seqFront.append(front.colorScaleInterval(duration=time / 4.0, colorScale=Vec4(0, 0, 0, 1), startColorScale=Vec4(0, 0, 0, 0)))
            seqFront.append(Wait(time / 4.0 * 3.0))
            par.append(seqFront)
            if light:
                seqBack = Sequence()
                seqBack.append(back.colorScaleInterval(duration=time / 4.0, colorScale=Vec4(1, 1, 0.5, 0.4), startColorScale=Vec4(1, 0, 0, 0)))
                seqBack.append(back.colorScaleInterval(duration=time / 4.0, colorScale=Vec4(1, 1, 1, 0.6)))
                seqBack.append(back.colorScaleInterval(duration=time / 2.0, colorScale=Vec4(1, 1, 0.5, 0)))
                par.append(seqBack)

        par.start()
        return

    def burnOut(self, ring=None, time=0.125):
        if ring != None:
            rings = [
             ring]
        else:
            rings = range(3)
        val = Vec4(0, 0, 0, 0)
        if time == 0:
            for r in rings:
                front = self.rings[r][1]
                front.setColorScale(val)

        else:
            for r in rings:
                front = self.rings[r][1]
                front.colorScaleInterval(duration=time, colorScale=val).start()

        return


class Burns(DirectFrame):

    def __init__(self, *args, **kwargs):
        DirectFrame.__init__(self, *args, **kwargs)
        self.initialiseoptions(Burns)
        self.rings = []
        for x in range(5):
            burn = Burn(parent=self, relief=None, scale=0.3, hpr=(0, 0, random.randint(0, 359)), pos=BishopsHandGlobals.TARGET_POS[x])
            self.rings.append(burn)

        return

    def burnIn(self, index, ring=None, time=0.25, light=True):
        self.rings[index].burnIn(ring, time, light)

    def burnOut(self, index, ring=None, time=0.125):
        self.rings[index].burnOut(ring, time)

    def reset(self):
        for x in range(5):
            self.burnOut(x, time=0)


class Knife(DirectFrame):
    SOUNDS = {'miss': loadSfxString(SoundGlobals.SFX_MINIGAME_BH_MISS),'hit': loadSfxString(SoundGlobals.SFX_MINIGAME_BH_HIT)}
    POSHPR = {'neutral': (Vec3(0.12, 0, 1.25), Vec3(0.0, 0.0, 10.0)),'in': (Vec3(0.03, 0, 1.13), Vec3(0.0, 0.0, 0.0)),'out': (Vec3(0.12, 0, 1.35), Vec3(0.0, 0.0, 15.0))}

    def __init__(self, *args, **kwargs):
        DirectFrame.__init__(self, *args, **kwargs)
        self.initialiseoptions(Knife)
        model = loader.loadModel('models/props/BH_images')
        self.shadowTurner = DirectFrame(parent=self, relief=None)
        self.shadow = DirectFrame(parent=self.shadowTurner, relief=None, geom=model.find('**/BH_shadow'), scale=0.075, pos=(0.0,
                                                                                                                            0.0,
                                                                                                                            0.8))
        self.shadow.setColorScale(1.0, 0.0, 0.0, 1.0)
        self.knifeTurner = DirectFrame(parent=self, relief=None)
        self.knife = DirectFrame(parent=self.knifeTurner, relief=None, geom=model.find('**/BH_bone'), scale=0.75, pos=self.POSHPR['neutral'][0], hpr=self.POSHPR['neutral'][1])
        self.seq = None
        self.initSounds()
        return

    def initSounds(self):
        self.sounds = {}
        for key in Knife.SOUNDS.keys():
            self.sounds[key] = loader.loadSfx(self.SOUNDS[key])

    def turn(self, angle):
        self.knifeTurner.setR(angle)
        self.shadowTurner.setR(angle)

    def strike(self, danger):
        if self.seq:
            self.seq.finish()

        def check(angle):
            if angle <= BishopsHandGlobals.FINGER_RANGES[0][0]:
                mistake = 0
                id = 0
            elif BishopsHandGlobals.FINGER_RANGES[0][0] < angle <= BishopsHandGlobals.FINGER_RANGES[0][1]:
                mistake = 1
                id = 1
            elif BishopsHandGlobals.FINGER_RANGES[0][1] < angle <= BishopsHandGlobals.FINGER_RANGES[1][0]:
                mistake = 0
                id = 1
            elif BishopsHandGlobals.FINGER_RANGES[1][0] < angle <= BishopsHandGlobals.FINGER_RANGES[1][1]:
                mistake = 1
                id = 2
            elif BishopsHandGlobals.FINGER_RANGES[1][1] < angle <= BishopsHandGlobals.FINGER_RANGES[2][0]:
                mistake = 0
                id = 2
            elif BishopsHandGlobals.FINGER_RANGES[2][0] < angle <= BishopsHandGlobals.FINGER_RANGES[2][1]:
                mistake = 1
                id = 3
            elif BishopsHandGlobals.FINGER_RANGES[2][1] < angle <= BishopsHandGlobals.FINGER_RANGES[3][0]:
                mistake = 0
                id = 3
            elif BishopsHandGlobals.FINGER_RANGES[3][0] < angle <= BishopsHandGlobals.FINGER_RANGES[3][1]:
                mistake = 1
                id = 4
            else:
                mistake = 0
                id = 4
            return (mistake, id)

        def getSound(checkVal):
            result = check(angle)
            if result[0]:
                return self.sounds['hit']
            return self.sounds['miss']

        angle = self.knifeTurner.getR()
        checkVal = check(angle)
        if danger:
            sound = getSound(checkVal)
            self.seq = Sequence()
            pos = self.POSHPR['in'][0]
            hpr = self.POSHPR['in'][1]
            self.seq.append(Func(self.knife.setPosHpr, pos, hpr))
            self.seq.append(Func(sound.setVolume, 1.0))
            self.seq.append(Func(sound.play))
            self.seq.append(Wait(0.1))
            pos = self.POSHPR['neutral'][0]
            hpr = self.POSHPR['neutral'][1]
            self.seq.append(Func(self.knife.setPosHpr, pos, hpr))
            self.seq.start()
            return checkVal
        else:
            sound = self.sounds['miss']
            self.seq = Sequence()
            pos = self.POSHPR['out'][0]
            hpr = self.POSHPR['out'][1]
            self.seq.append(Func(self.knife.setPosHpr, pos, hpr))
            self.seq.append(Func(sound.setVolume, 0.25))
            self.seq.append(Func(sound.play))
            self.seq.append(Wait(0.1))
            pos = self.POSHPR['neutral'][0]
            hpr = self.POSHPR['neutral'][1]
            self.seq.append(Func(self.knife.setPosHpr, pos, hpr))
            self.seq.start()
            return (-1, 0)


class FaceSpot(DirectFrame):
    NUMSTEPS = 24

    def __init__(self, faceId, *args, **kwargs):
        DirectFrame.__init__(self, *args, **kwargs)
        self.initialiseoptions(FaceSpot)
        model = loader.loadModel('models/props/BH_images')
        self.back = DirectFrame(parent=self, relief=None, geom=model.find('**/*bevel'))
        self.dots = DirectFrame(parent=self, relief=None, geom=model.find('**/*dots'))
        spot = model.find('**/*dot')
        self.spots = [ DirectFrame(parent=self, relief=None, geom=spot, hpr=(0.0, 0.0, 360.0 / 24.0 * x)) for x in range(self.NUMSTEPS) ]
        self.face = DirectFrame(parent=self, relief=None, geom=model.find('**/*face_' + `faceId`))
        self.cross = DirectFrame(parent=self, relief=None, geom=model.find('**/*x'))
        self.statusLabel = DirectLabel(parent=self, relief=None, pos=(0, 0, 0.5), text_scale=0.25, text='0', text_fg=(1,
                                                                                                                      1,
                                                                                                                      1,
                                                                                                                      1), text_shadow=(0,
                                                                                                                                       0,
                                                                                                                                       0,
                                                                                                                                       1), textMayChange=1, text_font=PiratesGlobals.getPirateOutlineFont())
        self.disable()
        return

    def setProgressPercent(self, percent):
        percent = PythonUtil.clampScalar(percent / 100.0, 0.0, 1.0)
        steps = int(self.NUMSTEPS * percent)
        for x in range(steps, self.NUMSTEPS):
            self.spots[x].hide()

        for x in range(steps):
            self.spots[x].show()

    def setStatus(self, status):
        self.statusLabel['text'] = `status`

    def disable(self):
        self.dots.hide()
        self.setProgressPercent(0)
        self.face.hide()
        self.cross.hide()
        self.statusLabel.hide()

    def enable(self, faceGeom=None):
        self.dots.show()
        self.setProgressPercent(0)
        if faceGeom:
            self.face['geom'] = faceGeom
        self.face.show()
        self.cross.hide()
        self.statusLabel.show()
        self.setProgressPercent(0)


class Round(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('BishopsHandRound')

    def __init__(self, game, roundNum, sequence):
        DirectObject.DirectObject.__init__(self)
        self.sequence = []
        self.step = 0
        self.leadCount = 0
        self.progress = [0, 0, 0, 0]
        self.startTime = 0
        self.game = game
        self.sequence = sequence
        self.stepCount = len(sequence)
        self.leadCount = 3
        self.ignoreAll()
        self.acceptOnce('BishopsHand-hit-0', self.prepStep, [self.leadCount - 1])
        self.acceptOnce('BishopsHand-hit-1', self.prepStep, [self.leadCount - 1])
        self.acceptOnce('BishopsHand-hit-2', self.prepStep, [self.leadCount - 1])
        self.acceptOnce('BishopsHand-hit-3', self.prepStep, [self.leadCount - 1])
        self.acceptOnce('BishopsHand-hit-4', self.prepStep, [self.leadCount - 1])

    def updateProgress(self, step=False, misses=False, hits=False):
        dirty = False
        if step:
            self.progress[0] += 1
            dirty = True
        if misses:
            self.progress[1] += 1
            dirty = True
        if hits:
            self.progress[2] += 1
            dirty = True
        if dirty:
            self.notify.debug('DIRTY')
            self.progress[3] = globalClock.getFrameTime() - self.startTime
            self.game.gameCallback(BishopsHandGlobals.PLAYER_ACTIONS.Progress, self.progress)

    def prepStep(self, countDown):
        self.ignoreAll()
        self.takeStep()
        if countDown > 0:
            self.ignoreAll()
            self.acceptOnce('BishopsHand-hit-0', self.prepStep, [countDown - 1])
            self.acceptOnce('BishopsHand-hit-1', self.prepStep, [countDown - 1])
            self.acceptOnce('BishopsHand-hit-2', self.prepStep, [countDown - 1])
            self.acceptOnce('BishopsHand-hit-3', self.prepStep, [countDown - 1])
            self.acceptOnce('BishopsHand-hit-4', self.prepStep, [countDown - 1])

    def takeStep(self):
        if 0 <= self.step - self.leadCount < len(self.sequence):
            self.game.burnOut(self.sequence[self.step - self.leadCount])
        for x in range(self.leadCount):
            if 0 <= self.step - x < self.stepCount:
                if x > 0:
                    light = True
                else:
                    light = False
                self.game.burnIn(self.sequence[self.step - x], x, light=light)
                if x == self.leadCount - 1:
                    newTarget = self.sequence[self.step - x]
                    nonTargets = range(5)
                    nonTargets.remove(newTarget)
                    self.ignoreAll()
                    self.acceptOnce('BishopsHand-hit-' + `newTarget`, self.reportTargetHit)
                    for nonTarget in nonTargets:
                        self.accept('BishopsHand-hit-' + `nonTarget`, self.reportTargetMiss)

        self.step += 1
        self.notify.debug('\nstep:\t%d\tstepCount\t%d:leadCount:\t%d' % (self.step, self.stepCount, self.leadCount))
        if self.step - self.leadCount > 0:
            self.updateProgress(step=True)
        if self.step >= self.stepCount + self.leadCount:
            self.stop()

    def reportTargetHit(self):
        self.notify.debug('target hit')
        self.takeStep()

    def reportTargetMiss(self):
        self.notify.debug('target missed')
        self.updateProgress(misses=True)

    def getProgress(self):
        return self.progress

    def start(self):
        self.stopKnife()
        self.startTime = globalClock.getFrameTime()
        self.startKnife(0.5, 2)

    def stop(self):
        self.ignoreAll()
        self.stopKnife()

    def startKnife(self, period, hitsPerStep):
        t = taskMgr.add(self.strikerTask, 'BishopsHand-striker')
        t.t0 = 0
        t.tSum = 0
        t.period = period
        t.danger = 0
        t.safeHits = hitsPerStep - 1
        self.strikeTask = t

    def stopKnife(self):
        taskMgr.remove('BishopsHand-striker')

    def strikerTask(self, task):
        dt = task.time - task.t0
        task.t0 = task.time
        task.tSum += dt
        if task.tSum >= task.period:
            task.tSum -= task.period
            task.danger += 1
            if task.danger > task.safeHits:
                task.danger = 0
            if task.danger == 0:
                result = self.game.knife.strike(danger=True)
            else:
                result = self.game.knife.strike(danger=False)
            if result[0] > -1:
                if result[0] == 0:
                    messenger.send('BishopsHand-hit-' + `(result[1])`)
                else:
                    self.updateProgress(hits=True)
                    self.notify.debug('finger hit')
        return Task.cont


class BishopsHandGame(DirectFrame, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('BishopsHandGame')

    def __init__(self, gameCallback, seatPos):
        DirectFrame.__init__(self, relief=None)
        FSM.FSM.__init__(self, 'BishopsHandGameFSM')
        self.initialiseoptions(BishopsHandGame)
        self.reparentTo(self.getParent(), sort=-100)
        self.gameCallback = gameCallback
        self.seatPos = seatPos
        self.round = None
        self.gameInterface = DirectFrame(parent=self, relief=None)
        self.gameInterface.hide()
        model = loader.loadModel('models/props/BH_images')
        self.bgImage = DirectFrame(parent=self.gameInterface, relief=None, geom=model.find('**/*table'), scale=(8.0 / 3.0, 2, 2))
        self.faces = [ FaceSpot(0, parent=self.gameInterface, relief=None, pos=BishopsHandGlobals.FACE_SPOT_POS[p], scale=0.333) for p in BishopsHandGlobals.FACE_SPOT_POS.keys()[1:] ]
        base.faces = self.faces
        for f in self.faces:
            f.enable()

        self.dealerFace = FaceSpot(0, parent=self.gameInterface, relief=None, pos=(), scale=0.333)
        self.burns = Burns(parent=self.gameInterface, relief=None)
        self.hand = DirectFrame(parent=self.gameInterface, relief=None, geom=Hand('Hand'), scale=2.0)
        self.knife = Knife(parent=self.gameInterface, relief=None, pos=(0.07, 0.0, -0.16))
        self.menu = GuiTray.GuiTray(0.75, 0.2)
        self.menu.setPos(-0.4, 0, -1)
        self.menu.hide()
        self.joinButton = DirectButton(parent=self.menu, relief=DGG.RAISED, state=DGG.NORMAL, text='Join: 2 Gold', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, frameColor=PiratesGuiGlobals.ButtonColor1, frameSize=(0,
                                                                                                                                                                                                                                                                                      0.4,
                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                      0.08), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.2,
                                                                                                                                                                                                                                                                                                                                                  0.03), textMayChange=1, pos=(0.05,
                                                                                                                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                                                                                                                               0.1), command=self.gameCallback, extraArgs=[BishopsHandGlobals.PLAYER_ACTIONS.JoinGame])
        self.joinButton.hide()
        self.unjoinButton = DirectButton(parent=self.menu, relief=DGG.RAISED, state=DGG.NORMAL, text='Unjoin', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, frameColor=PiratesGuiGlobals.ButtonColor1, frameSize=(0,
                                                                                                                                                                                                                                                                                  0.4,
                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                  0.08), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.2,
                                                                                                                                                                                                                                                                                                                                              0.03), textMayChange=1, pos=(0.05,
                                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                                           0.1), command=self.gameCallback, extraArgs=[BishopsHandGlobals.PLAYER_ACTIONS.UnjoinGame])
        self.unjoinButton.hide()
        self.rejoinButton = DirectButton(parent=self.menu, relief=DGG.RAISED, state=DGG.NORMAL, text='Rejoin: 2 Gold', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, frameColor=PiratesGuiGlobals.ButtonColor1, frameSize=(0,
                                                                                                                                                                                                                                                                                          0.4,
                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                          0.08), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.2,
                                                                                                                                                                                                                                                                                                                                                      0.03), textMayChange=1, pos=(0.05,
                                                                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                                                                   0.1), command=self.gameCallback, extraArgs=[BishopsHandGlobals.PLAYER_ACTIONS.RejoinGame])
        self.rejoinButton.hide()
        self.continueButton = DirectButton(parent=self.menu, relief=DGG.RAISED, state=DGG.NORMAL, text='Practice', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, frameColor=PiratesGuiGlobals.ButtonColor1, frameSize=(0,
                                                                                                                                                                                                                                                                                      0.4,
                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                      0.08), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.2,
                                                                                                                                                                                                                                                                                                                                                  0.03), textMayChange=1, pos=(0.05,
                                                                                                                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                                                                                                                               0.0), command=self.gameCallback, extraArgs=[BishopsHandGlobals.PLAYER_ACTIONS.Continue])
        self.continueButton.hide()
        self.resignButton = DirectButton(parent=self.menu, relief=DGG.RAISED, state=DGG.NORMAL, text='Resign Game', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, frameColor=PiratesGuiGlobals.ButtonColor1, frameSize=(0,
                                                                                                                                                                                                                                                                                       0.27,
                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                       0.08), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.13,
                                                                                                                                                                                                                                                                                                                                                   0.03), textMayChange=1, pos=(0.46,
                                                                                                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                                                                                                0.1), command=self.gameCallback, extraArgs=[BishopsHandGlobals.PLAYER_ACTIONS.Resign])
        self.resignButton.hide()
        self.leaveButton = DirectButton(parent=self.menu, relief=DGG.RAISED, state=DGG.NORMAL, text='Leave with winnings', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, frameColor=PiratesGuiGlobals.ButtonColor1, frameSize=(0,
                                                                                                                                                                                                                                                                                              0.27,
                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                              0.08), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.13,
                                                                                                                                                                                                                                                                                                                                                          0.03), textMayChange=1, pos=(0.46,
                                                                                                                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                                                                                                                       0.1), command=self.gameCallback, extraArgs=[BishopsHandGlobals.PLAYER_ACTIONS.Resign])
        self.leaveButton.hide()
        self.exitButton = DirectButton(parent=self.menu, relief=DGG.RAISED, text='X', text_align=TextNode.ACenter, text_scale=0.04, text_pos=(0.02,
                                                                                                                                              0.01), text_fg=(0.75,
                                                                                                                                                              0.75,
                                                                                                                                                              0.75,
                                                                                                                                                              1), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, frameColor=PiratesGuiGlobals.ButtonColor1, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameSize=(0,
                                                                                                                                                                                                                                                                                                                                   0.04,
                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                   0.04), pos=(0.75 - 0.01 - 0.04, 0, 0.01), command=self.gameCallback, extraArgs=[-1])
        self.roundLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=0.06, pos=(-0.1, 0, 0.45), text_fg=(1,
                                                                                                                                                   1,
                                                                                                                                                   1,
                                                                                                                                                   1), text_shadow=(0,
                                                                                                                                                                    0,
                                                                                                                                                                    0,
                                                                                                                                                                    1), textMayChange=1, text_font=PiratesGlobals.getPirateOutlineFont())
        self.potSizeLabel = DirectLabel(parent=self, relief=None, text_align=TextNode.ALeft, text_scale=0.08, pos=(-0.1, 0, 0.5), text_fg=(1,
                                                                                                                                           1,
                                                                                                                                           1,
                                                                                                                                           1), text_shadow=(0,
                                                                                                                                                            0,
                                                                                                                                                            0,
                                                                                                                                                            1), textMayChange=1, text_font=PiratesGlobals.getPirateOutlineFont())
        self.tableStateLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ACenter, text_scale=0.08, pos=(0,
                                                                                                                                 0,
                                                                                                                                 0), text_fg=(1,
                                                                                                                                              1,
                                                                                                                                              1,
                                                                                                                                              1), text_shadow=(0,
                                                                                                                                                               0,
                                                                                                                                                               0,
                                                                                                                                                               1), textMayChange=1, text_font=PiratesGlobals.getPirateOutlineFont())
        self.timerLabel = DirectLabel(parent=self, relief=None, text='', pos=(1, 0,
                                                                              0.55), scale=0.1, text_fg=(1,
                                                                                                         1,
                                                                                                         1,
                                                                                                         1), text_shadow=(0,
                                                                                                                          0,
                                                                                                                          0,
                                                                                                                          1), textMayChange=1, text_font=PiratesGlobals.getPirateOutlineFont())
        self.mouseNode = base.mouseWatcherNode
        t = taskMgr.add(self.mouseWatcherTask, 'mouse')
        t.run = True
        self.text = OnscreenText(pos=(-0.75, 0.75), mayChange=True)
        self.text.reparentTo(self)
        localAvatar.guiMgr.hideTrays()
        buttons = ['normalButton', 'scButton', 'whisperButton', 'whisperCancelButton', 'whisperScButton']
        for b in buttons:
            button = getattr(localAvatar.chatMgr, b)
            button.reparentTo(button.getParent())

        self.request('WaitingForPlayers')
        return

    def hideAll(self):
        self.gameInterface.hide()
        self.roundLabel.hide()
        self.potSizeLabel.hide()
        self.tableStateLabel.hide()
        self.timerLabel.hide()
        self.menu.hide()
        self.joinButton.hide()
        self.unjoinButton.hide()
        self.rejoinButton.hide()
        self.continueButton.hide()
        self.resignButton.hide()
        self.leaveButton.hide()
        render.show()

    def enterByStander(self):
        self.hideAll()

    def enterSeatedUnjoined(self):
        self.hideAll()
        self.menu.show()
        self.joinButton.show()

    def enterSeatedJoined(self):
        self.hideAll()
        self.menu.show()
        self.unjoinButton.show()

    def enterWaitingForRound(self):
        self.hideAll()
        self.menu.show()
        self.resignButton.show()
        self.gameInterface.show()
        self.timerLabel.show()
        render.hide()

    def enterPlaying(self):
        self.hideAll()
        self.gameInterface.show()
        render.hide()

    def enterContinue(self):
        self.notify.debug('EnteringContinue')
        self.hideAll()
        self.menu.show()
        self.continueButton.show()
        self.continueButton['text'] = 'Practice'
        self.resignButton.show()
        self.gameInterface.show()
        self.timerLabel.show()
        render.hide()

    def enterRejoin(self):
        self.notify.debug('EnteringRejoin')
        self.hideAll()
        self.menu.show()
        self.rejoinButton.show()
        self.continueButton.show()
        self.continueButton['text'] = 'Practice'
        self.resignButton.show()
        self.gameInterface.show()
        self.timerLabel.show()
        render.hide()

    def enterLeave(self):
        self.notify.debug('EnteringLeave')
        self.hideAll()
        self.menu.show()
        self.continueButton.show()
        self.continueButton['text'] = 'Continue'
        self.leaveButton.show()
        self.gameInterface.show()
        self.timerLabel.show()
        render.hide()

    def enterOff(self):
        self.hideAll()

    def startTimer(self, time):
        if time > 0:

            def timerTask(task):
                if task.time < task.timer:
                    self.timerLabel['text'] = `(int(PythonUtil.bound(task.timer - task.time, 0, time) + 1.0))`
                    return Task.cont
                else:
                    self.timerLabel['text'] = ''
                    return Task.done

            self.stopTimer()
            t = taskMgr.add(timerTask, 'BH-game-timer')
            t.timer = time

    def stopTimer(self):
        tasks = taskMgr.getTasksNamed('BH-game-timer')
        for t in tasks:
            t.timer = 0

    def setTableState(self, tableState, oldSeatStatus, newSeatStatus):
        for face, oldStatus, newStatus in zip(self.faces, oldSeatStatus, newSeatStatus):
            if newStatus != oldStatus:
                avId, status = newStatus
                face.setStatus(status)

    def resetBurns(self):
        self.burns.reset()

    def burnIn(self, *args, **kwargs):
        self.burns.burnIn(*args, **kwargs)

    def burnOut(self, *args, **kwargs):
        self.burns.burnOut(*args, **kwargs)

    def mouseWatcherTask(self, task):
        if task.run and self.mouseNode.hasMouse():
            pivot = (
             0.07, -0.1567)

            def turn(a, b):
                d = [ x - y for x, y in zip(a, b) ]
                return atan2(d[0], d[1]) * 180.0 / math.pi

            point = (
             self.mouseNode.getMouseX() * 4.0 / 3.0, self.mouseNode.getMouseY())
            a = turn(point, pivot)
            self.text['text'] = `(point[0])`[:10] + '\n' + `(point[1])`[:10] + '\n' + `a`[:5]
            self.text['text'] = ''
            self.knife.turn(PythonUtil.bound(a, -60, 80))
        return Task.cont

    def reportProgress(self, report):
        for line in report:
            seat, percent = line
            if seat < 6:
                self.faces[seat].setProgressPercent(percent)

    def initRound(self, sequence):
        self.round = Round(self, 0, sequence)
        self.resetBurns()

    def startRound(self):
        self.round.start()

    def stopRound(self):
        if self.round:
            self.round.stop()
        self.round = None
        return

    def destroy(self):
        self.cleanup()
        self.stopTimer()
        taskMgr.remove('mouse')
        render.show()
        localAvatar.guiMgr.showTrays()
        del self.gameCallback
        del self.seatPos
        self.exitButton.destroy()
        self.potSizeLabel.destroy()
        self.timerLabel.destroy()
        self.roundLabel.destroy()
        self.tableStateLabel.destroy()
        self.menu.destroy()
        DirectFrame.destroy(self)