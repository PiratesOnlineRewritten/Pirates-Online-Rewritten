import math
from direct.task import Task
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.interval.IntervalGlobal import LerpPosInterval, LerpFunc
from pandac.PandaModules import MouseButton, Point2, Point3, Vec2, Vec4
import RepairGlobals
from pirates.audio import SoundGlobals
from MinigameUtils import getAcuteAngle
from pirates.audio.SoundGlobals import loadSfx
from pirates.piratesgui.GuiPanel import *

class RepairSaw(DirectButton):

    def __init__(self, parent, **kw):
        optiondefs = (
         ('clickDownCommand', None, None), ('clickUpCommand', None, None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent, **kw)
        self.initialiseoptions(RepairSaw)
        self.sawingGame = parent
        self._initVars()
        self._initGUI()
        self._initIntervals()
        self.accept(self.guiItem.getEnterEvent(), self.onMouseEnter)
        self.accept(self.guiItem.getExitEvent(), self.onMouseExit)
        self.guiItem.addClickButton(MouseButton.one())
        self.bind(DGG.B1PRESS, self.onMouseDown)
        self.bind(DGG.B1RELEASE, self.onMouseUp)
        return None

    def _initVars(self):
        self.isMouseDown = False
        self.isMouseInButton = False

    def _initGUI(self):
        mainGui = loader.loadModel('models/gui/pir_m_gui_srp_sawing_main')
        self.sawGlow = self.glow = OnscreenImage(parent=self, image=mainGui.find('**/glow'))
        self.sawGlow.setR(193)
        self.sawGlow.setPos(0.9, 0.0, -0.165)
        self.sawGlow.setBin('fixed', 50)
        self.sawGlow.reparentTo(self)
        self.totalTime = 0
        taskMgr.add(self.updateGlow, self.uniqueName('RepairSaw.UpdateGlow'))

    def updateGlow(self, task):
        dt = globalClock.getDt()
        self.totalTime += dt * 1.75
        alphaVal = self.totalTime - math.floor(self.totalTime)
        if math.floor(self.totalTime) % 2 == 0:
            alphaVal = 1.0 - alphaVal
        alphaVal = alphaVal * alphaVal
        self.sawGlow.setColorScale(1.0, 1.0, 1.0, alphaVal)
        return Task.cont

    def _initIntervals(self):
        pass

    def destroy(self):
        taskMgr.remove(self.uniqueName('RepairSaw.UpdateGlow'))
        taskMgr.remove(self.uniqueName('RepairSaw.updateTask'))
        taskMgr.remove(DGG.B1PRESS)
        taskMgr.remove(DGG.B1RELEASE)
        DirectFrame.destroy(self)

    def onMouseEnter(self, event):
        self.sawGlow.setColorScale(0.5, 1.0, 0.5, 1.0)
        taskMgr.remove(self.uniqueName('RepairSaw.UpdateGlow'))
        self.isMouseInButton = True

    def onMouseExit(self, event):
        self.totalTime = 0
        self.sawGlow.setColorScale(1.0, 1.0, 1.0, 0.0)
        taskMgr.add(self.updateGlow, self.uniqueName('RepairSaw.UpdateGlow'))
        self.isMouseInButton = False

    def onMouseDown(self, event):
        if self.isMouseInButton:
            self.sawGlow.stash()
            self.isMouseDown = True
            apply(self['clickDownCommand'])
            taskMgr.add(self.updateTask, self.uniqueName('RepairSaw.updateTask'), priority=1, extraArgs=[])

    def onMouseUp(self, event):
        self.sawGlow.unstash()
        self.isMouseDown = False
        apply(self['clickUpCommand'])
        taskMgr.remove(self.uniqueName('RepairSaw.updateTask'))
        self.setR(180)

    def deactivate(self):
        self.stash()
        self.ignore(self.guiItem.getEnterEvent())
        self.ignore(self.guiItem.getExitEvent())
        self.onMouseUp(None)
        return

    def activate(self):
        self.ignore(self.guiItem.getEnterEvent())
        self.ignore(self.guiItem.getExitEvent())
        self.accept(self.guiItem.getEnterEvent(), self.onMouseEnter)
        self.accept(self.guiItem.getExitEvent(), self.onMouseExit)
        self.unstash()
        self.setR(180)

    def updateTask(self):
        dt = globalClock.getDt()
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            relative = Point3(mpos.getX(), 0.0, mpos.getY())
            relative = self.sawingGame.getRelativePoint(render2d, relative)
            moveDiff = (relative - self.getPos()).length()
            self.setPos(relative.getX(), 0.0, relative.getZ())
            goalR = self.getR()
            nextPos = None
            if self.sawingGame.lastHitIndex >= 0:
                if self.sawingGame.sawWaypoints[0].hit:
                    dir = 1
                else:
                    dir = -1
                if len(self.sawingGame.sawWaypoints) > self.sawingGame.lastHitIndex + dir >= 0 and not self.sawingGame.sawWaypoints[self.sawingGame.lastHitIndex + dir].hit:
                    nextPos = self.sawingGame.sawWaypoints[self.sawingGame.lastHitIndex + dir].getPos(self.sawingGame)
                    dif = self.sawingGame.sawWaypoints[self.sawingGame.lastHitIndex].getPos(self.sawingGame) - nextPos
                    goalR = math.degrees(math.atan2(-dif.getZ(), dif.getX()))
            else:
                validWaypointPositions = [
                 self.sawingGame.sawWaypoints[0].getPos(self.sawingGame), self.sawingGame.sawWaypoints[-1].getPos(self.sawingGame)]
                lookAtIndex = self.sawingGame.getClosestPosition(validWaypointPositions)
                if lookAtIndex == 0:
                    dif = validWaypointPositions[lookAtIndex] - self.sawingGame.sawWaypoints[1].getPos(self.sawingGame)
                else:
                    dif = validWaypointPositions[lookAtIndex] - self.sawingGame.sawWaypoints[-2].getPos(self.sawingGame)
                goalR = math.degrees(math.atan2(-dif.getZ(), dif.getX()))
            if moveDiff > 0.0:
                anglediff = getAcuteAngle(self.getR(), goalR)
                if abs(anglediff) <= RepairGlobals.Sawing.sawTurnSpeed * dt:
                    self.setR(goalR)
                else:
                    self.setR(self.getR() + RepairGlobals.Sawing.sawTurnSpeed * dt * (-anglediff / abs(anglediff)))
        return Task.cont