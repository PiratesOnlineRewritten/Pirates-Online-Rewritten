import math
from direct.interval.IntervalGlobal import LerpFunc, LerpPosInterval
from direct.task import Task
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from direct.fsm import FSM
from pirates.audio.SoundGlobals import loadSfx
from pandac.PandaModules import MouseButton, Point2, Point3, Vec2, NodePath, VBase3
import RepairGlobals
from pirates.audio import SoundGlobals
GOAL_EMPTY = -1
GOAL_NONE = 0
GOAL_HORIZ_1 = 1
GOAL_HORIZ_2 = 2
GOAL_VERT_1 = 3
GOAL_CROSS_1_1 = 4
GOAL_TO_TEXTURE = {GOAL_EMPTY: 'empty',GOAL_NONE: 'blank',GOAL_HORIZ_1: 'red',GOAL_HORIZ_2: 'blue',GOAL_VERT_1: 'green',GOAL_CROSS_1_1: 'cross'}
TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3
SPACING = 0.15

class RepairGridPiece(DirectButton, FSM.FSM):

    def __init__(self, name, parent, allWoodSquaresGeom, selectedOutlineGeom, command, location, **kw):
        optiondefs = ()
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent, **kw)
        self.initialiseoptions(RepairGridPiece)
        FSM.FSM.__init__(self, 'RepairGridPiece_%sFSM' % name)
        self.name = name
        self.allWoodSquaresGeom = allWoodSquaresGeom
        self.selectedOutlineGeom = selectedOutlineGeom
        self.command = command
        self.location = location
        self._initVars()
        self._initGUI()
        self._initIntervals()
        self.accept(self.guiItem.getEnterEvent(), self.onMouseEnter)
        self.accept(self.guiItem.getExitEvent(), self.onMouseExit)
        self.bind(DGG.B1PRESS, self.onMouseDown)
        self.bind(DGG.B1RELEASE, self.onMouseUp)
        self.bind(DGG.B2PRESS, self.onMouseUp)
        self.bind(DGG.B2RELEASE, self.onMouseUp)
        self.bind(DGG.B3PRESS, self.onMouseUp)
        self.bind(DGG.B3RELEASE, self.onMouseUp)
        self.idleGeom = NodePath('idleGeom')
        self.highlightedGeom = NodePath('highlightedGeom')
        self.haveMoved = False
        self.grabPoint = None
        self.setType(GOAL_NONE)
        return

    def _initVars(self):
        self.pieceType = GOAL_NONE
        self.enabled = True
        self.isMouseDown = False
        self.isMouseInButton = False

    def _initGUI(self):
        self.selectedOutlineGeom.reparentTo(self)
        self.selectedOutlineGeom.hide()
        self.selectedOutlineGeom.setBin('fixed', 38)

    def _initIntervals(self):
        self.moveInterval = LerpPosInterval(self, duration=RepairGlobals.Bracing.moveTime, pos=self.getPos(), name='RepairGridPiece_%s.moveInterval' % self.name)

    def destroy(self):
        taskMgr.remove(self.uniqueName('RepairGridPiece.updateTask'))
        taskMgr.remove(DGG.B1PRESS)
        taskMgr.remove(DGG.B1RELEASE)
        taskMgr.remove(DGG.B2PRESS)
        taskMgr.remove(DGG.B2RELEASE)
        taskMgr.remove(DGG.B3PRESS)
        taskMgr.remove(DGG.B3RELEASE)
        self.idleGeom.detachNode()
        self.idleGeom = None
        self.highlightedGeom.detachNode()
        self.highlightedGeom = None
        self.ignore(self.guiItem.getEnterEvent())
        self.ignore(self.guiItem.getExitEvent())
        self.moveInterval.clearToInitial()
        del self.moveInterval
        DirectFrame.destroy(self)
        self.clearPiece()
        self.allWoodSquaresGeom.removeNode()
        del self.allWoodSquaresGeom
        return

    def setGeomState(self, state):
        if state == 'idle':
            self.idleGeom.show()
            self.highlightedGeom.hide()
        elif state == 'highlighted':
            self.highlightedGeom.show()
            self.idleGeom.hide()

    def onMouseEnter(self, event):
        self.isMouseInButton = True
        if self.isMouseDown:
            self.setGeomState('idle')
        else:
            self.setGeomState('highlighted')

    def onMouseExit(self, event):
        self.isMouseInButton = False
        self.setGeomState('idle')

    def onMouseDown(self, event):
        if self.isMouseInButton:
            self.selectedOutlineGeom.show()
            self.setGeomState('idle')
            self.isMouseDown = True
            self.haveMoved = False
            screenx = base.mouseWatcherNode.getMouseX()
            screeny = base.mouseWatcherNode.getMouseY()
            self.grabPoint = aspect2d.getRelativePoint(render2d, (screenx, 0, screeny))
            taskMgr.add(self.updateTask, self.uniqueName('RepairGridPiece.updateTask'), extraArgs=[])

    def onMouseUp(self, event):
        if self.isMouseDown:
            self.isMouseDown = False
            if not self.haveMoved:
                self.checkMovePiece(True)
            self.grabPoint = None
            if self.isMouseInButton:
                self.setGeomState('highlighted')
            else:
                self.setGeomState('idle')
            self.selectedOutlineGeom.hide()
            taskMgr.remove(self.uniqueName('RepairGridPiece.updateTask'))

    def onMoveButtonPressed(self, dir1, dir2):
        if not self.moveInterval.isPlaying():
            self.haveMoved = True
            args = self.location[:]
            args.append((dir1, dir2))
            return self.command(*args)

    def updateTask(self):
        if not self.isMouseInButton and not self.moveInterval.isPlaying():
            self.checkMovePiece()
        return Task.cont

    def checkMovePiece(self, isPush=False):
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        if self.grabPoint is None:
            self.grabPoint = self.getPos(aspect2d)
        screenx = base.mouseWatcherNode.getMouseX()
        screeny = base.mouseWatcherNode.getMouseY()
        cursorPos = aspect2d.getRelativePoint(render2d, (screenx, 0, screeny))
        diff = self.grabPoint - cursorPos
        absX = math.fabs(diff.getX())
        absZ = math.fabs(diff.getZ())
        moveDirection = None
        if isPush:
            threshold = RepairGlobals.Bracing.pushPieceThreshold
        else:
            threshold = RepairGlobals.Bracing.movePieceThreshold
        if absZ > absX and diff.getZ() > 0.0 and absZ > threshold:
            moveDirection = directions[1]
        else:
            if absZ > absX and diff.getZ() < 0.0 and absZ > threshold:
                moveDirection = directions[0]
            elif absX > absZ and diff.getX() > 0.0 and absX > threshold:
                moveDirection = directions[2]
            elif absX > absZ and diff.getX() < 0.0 and absX > threshold:
                moveDirection = directions[3]

        if moveDirection:
            if self.onMoveButtonPressed(*moveDirection) and self.grabPoint is not None:
                self.grabPoint += VBase3(SPACING * moveDirection[0], 0.0, SPACING * moveDirection[1])

    def setType(self, type):
        self.pieceType = type
        activeWoodSquareGeom = self.allWoodSquaresGeom.find('**/%s' % GOAL_TO_TEXTURE[type])
        self.idleGeom.detachNode()
        self.idleGeom = None
        self.highlightedGeom.detachNode()
        self.highlightedGeom = None
        self.idleGeom = NodePath('idleGeom')
        self.highlightedGeom = NodePath('highlightedGeom')
        self.idleGeom.reparentTo(self)
        self.highlightedGeom.reparentTo(self)
        if activeWoodSquareGeom.isEmpty():
            self.stash()
        else:
            activeWoodSquareGeom.find('**/idle').copyTo(self.idleGeom)
            activeWoodSquareGeom.find('**/over').copyTo(self.highlightedGeom)
            self.setGeomState('idle')
            self.unstash()
        return

    def setEnabled(self, enabled):
        self.onMouseUp(None)
        self.enabled = enabled
        if not enabled:
            self['state'] = DGG.DISABLED
        else:
            self['state'] = DGG.NORMAL
        return

    def isGoalPiece(self):
        return self.pieceType != GOAL_NONE and self.pieceType != GOAL_EMPTY

    def isEmptyPiece(self):
        return self.pieceType == GOAL_EMPTY

    def setGridLocation(self, location, pos):
        self.location = location
        self.setPos(pos)

    def enterIdle(self):
        self.stash()
        self.setEnabled(False)

    def exitIdle(self):
        self.unstash()

    def enterBlank(self):
        self.setType(GOAL_NONE)

    def exitBlank(self):
        self.unstash()

    def enterGoal(self, pieceType):
        self.setType(pieceType)

    def exitGoal(self):
        self.unstash()

    def enterEmpty(self):
        self.setEnabled(False)
        self.setType(GOAL_EMPTY)

    def exitEmpty(self):
        self.unstash()
