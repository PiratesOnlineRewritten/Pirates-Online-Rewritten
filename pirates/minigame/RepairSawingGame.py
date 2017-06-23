import math
import random
from pandac.PandaModules import NodePath, Point3, TextNode, Vec3, Vec4
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.interval.IntervalGlobal import LerpPosInterval, LerpFunc
from direct.gui.DirectGui import DirectButton, DGG, DirectFrame, DirectLabel
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from RepairMincroGame import RepairMincroGame
from MinigameUtils import getAcuteAngle
from RepairSawingLine import RepairSawingLine
from RepairSaw import RepairSaw
from pirates.piratesbase import PiratesGlobals
import RepairGlobals
SAW_COLLIDE_MASK = 16

class SawWaypoint(NodePath):

    def __init__(self, index, parent, pos):
        NodePath.__init__(self, 'SawWaypoint%i' % index)
        self.index = index
        self.setPos(pos)
        self.reparentTo(parent)
        self.hit = False


class RepairSawingGame(RepairMincroGame):
    sawSounds = None
    boardComplet = None
    boardDestroyed = None

    def __init__(self, repairGame):
        self.config = RepairGlobals.Sawing
        notify = DirectNotifyGlobal.directNotify.newCategory('RepairSawingGame')
        RepairMincroGame.__init__(self, repairGame, 'sawing', PLocalizer.Minigame_Repair_Sawing_Start)

    def _initVars(self):
        RepairMincroGame._initVars(self)
        self.boardsPool = {}
        self.currentBoard = None
        self.currentBoardIndex = 0
        self.onDeckBoard = None
        self.onDeckBoardIndex = 0
        self.totalScore = 0.0
        self.hitZone1Penalty = False
        self.hitZone2Penalty = False
        self.hitBoardPenalty = False
        self.moveDiffForSound = 0.0
        self.startPositions = (
         Point3(0.0, 0.0, 0.0),)
        self.currentStartIndex = 0
        self.lastMousePos = None
        self.board_left = None
        self.board_right = None
        self.cut = None
        self.zone1_right = None
        self.zone1_left = None
        self.zone2_right = None
        self.zone2_left = None
        self.piece1 = None
        self.piece2 = None
        self.lastHitIndex = -1
        self.sawWaypoints = []
        return

    def _initAudio(self):
        RepairMincroGame._initAudio(self)
        if not self.sawSounds:
            RepairSawingGame.sawSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_SAW_INOUT01), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_SAW_INOUT02), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_SAW_INOUT03), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_SAW_INOUT04))
            RepairSawingGame.boardComplete = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_SAW_COMPLETE)
            RepairSawingGame.boardDestroyed = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_SAW_FAIL)

    def _initVisuals(self):
        RepairMincroGame._initVisuals(self)
        self.setBin('fixed', 36)
        self.model = loader.loadModel('models/gui/pir_m_gui_srp_sawing_main')
        sawModel = self.model.find('**/saw')
        sawModel.setR(193)
        sawModel.setPos(0.9, 0.0, -0.165)
        sawModel.setBin('gui-popup', 0)
        self.sawButton = RepairSaw(parent=self, clickDownCommand=self.sawAttachedToMouse, clickUpCommand=self.sawRemovedFromMouse, geom=sawModel, text_pos=(0.2, -0.3), text_fg=(1,
                                                                                                                                                                                 0,
                                                                                                                                                                                 0,
                                                                                                                                                                                 1), scale=(0.3,
                                                                                                                                                                                            0.3,
                                                                                                                                                                                            0.3), relief=None, pressEffect=0, frameSize=(-0.05, 1.05, -0.3, 0.05), rolloverSound=None, clickSound=None)
        self.sawingLine = RepairSawingLine(self, self.config.sawlineLineThickness, self.config.sawlineColor, self.config.sawlineLinespawnDist)
        self.progressDescriptionLabel = DirectLabel(text=PLocalizer.Minigame_Repair_Sawing_Description, text_fg=(1.0,
                                                                                                                 1.0,
                                                                                                                 1.0,
                                                                                                                 1.0), text_pos=(0.0,
                                                                                                                                 0.0), text_shadow=(0.0,
                                                                                                                                                    0.0,
                                                                                                                                                    0.0,
                                                                                                                                                    1.0), text_font=PiratesGlobals.getPirateFont(), text_align=TextNode.ARight, relief=None, scale=(0.08,
                                                                                                                                                                                                                                                    0.08,
                                                                                                                                                                                                                                                    0.08), pos=(-0.2, 0.0, 0.5), parent=self)
        self.progressLabel = DirectLabel(text=PLocalizer.Minigame_Repair_Sawing_Thresholds[3], text_fg=(1.0,
                                                                                                        1.0,
                                                                                                        1.0,
                                                                                                        1.0), text_pos=(0.0,
                                                                                                                        0.0), text_shadow=(0.0,
                                                                                                                                           0.0,
                                                                                                                                           0.0,
                                                                                                                                           1.0), text_font=PiratesGlobals.getPirateFont(), text_align=TextNode.ALeft, relief=None, scale=(0.08,
                                                                                                                                                                                                                                          0.08,
                                                                                                                                                                                                                                          0.08), pos=(-0.18, 0.0, 0.5), parent=self)
        self.boardDestroyedLabel = DirectLabel(text=PLocalizer.Minigame_Repair_Sawing_Board_Destroyed, text_fg=(1.0,
                                                                                                                0.0,
                                                                                                                0.0,
                                                                                                                1.0), text_pos=(0.0,
                                                                                                                                0.0), text_font=PiratesGlobals.getPirateFont(), text_shadow=(0.0,
                                                                                                                                                                                             0.0,
                                                                                                                                                                                             0.0,
                                                                                                                                                                                             1.0), relief=None, scale=(0.1,
                                                                                                                                                                                                                       0.1,
                                                                                                                                                                                                                       0.1), pos=(0.0,
                                                                                                                                                                                                                                  0.0,
                                                                                                                                                                                                                                  0.1), parent=self)
        self.boardDestroyedLabel.setBin('fixed', 38)
        self.boardDestroyedLabel.stash()
        return

    def _initIntervals(self):
        RepairMincroGame._initIntervals(self)
        self.newBoardSequence = Sequence(name='RepairSawingGame.newBoardSequence')
        self.splitBoardSequence = Sequence(name='RepairSawGame.splitBoardSequence')
        self.dropBoardSequence = Sequence(name='RepairSawGame.dropBoardSequence')

    def getNewBoard(self, boardIndex):
        board = self.model.find('**/wood%i' % boardIndex).copyTo(NodePath('board%i' % len(self.boardsPool)))
        board.reparentTo(self)
        piece1 = board.find('**/piece_1')
        piece1.setPythonTag('piece_1', self.piece1)
        piece1.setY(self.config.boardYDist)
        piece2 = board.find('**/piece_2')
        piece2.setPythonTag('piece_2', self.piece2)
        piece2.setY(self.config.boardYDist)
        pieceCut = board.find('**/piece_cut')
        pieceCut.setPythonTag('cut', self.cut)
        pieceCut.setColor(self.config.cutColor)
        pieceCut.setY(self.config.boardYDist)
        board_left = piece1.find('**/board')
        board_left.setPythonTag('left', self.board_left)
        board_right = piece2.find('**/board')
        board_right.setPythonTag('right', self.board_right)
        zone1_right = piece2.find('**/zone_1')
        zone1_right.setPythonTag('zone1_right', self.zone1_right)
        zone1_right.setColor(self.config.zone1Color)
        zone1_left = piece1.find('**/zone_1')
        zone1_left.setPythonTag('zone1_left', self.zone1_left)
        zone1_left.setColor(self.config.zone1Color)
        zone2_right = piece2.find('**/zone_2')
        zone2_right.setPythonTag('zone2_right', self.zone2_right)
        zone2_right.setColor(self.config.zone2Color)
        zone2_left = piece1.find('**/zone_2')
        zone2_left.setPythonTag('zone2_left', self.zone2_left)
        zone2_left.setColor(self.config.zone2Color)
        board.stash()
        return board

    def reset(self):
        for key in self.boardsPool.keys():
            board = self.boardsPool[key]
            board.removeNode()

        self.boardsPool.clear()
        if self.currentBoard:
            self.currentBoard.removeNode()
            self.currentBoard = None
        if self.onDeckBoard:
            self.onDeckBoard.removeNode()
            self.onDeckBoard = None
        for boardIndex in self.currentDifficultySet:
            boardIndex -= 1
            if 'copy1_%s' % boardIndex not in self.boardsPool:
                board = self.getNewBoard(boardIndex)
                self.boardsPool['copy1_%s' % boardIndex] = board
            if 'copy2_%s' % boardIndex not in self.boardsPool:
                board = self.getNewBoard(boardIndex)
                self.boardsPool['copy2_%s' % boardIndex] = board

        self.currentBoardIndex = 0
        self.currentBoard = None
        self.moveNewBoardOnDeck()
        self.onDeckBoard.unstash()
        self.totalScore = 0
        self.startPositions = (Point3(0.0, 0.0, 0.0),)
        self.sawButton.stash()
        self.sawButton.reparentTo(self)
        self.lastHitIndex = -1
        self.moveDiffForSound = 0.0
        RepairMincroGame.reset(self)
        self.repairGame.gui.setTutorial(self.name)
        self.repairGame.gui.setTitle(self.name)
        return

    def destroy(self):
        RepairMincroGame.destroy(self)
        taskMgr.remove('SawingGame.updateSawTask')
        self.sawButton.destroy()
        self.sawButton.removeNode()
        del self.sawButton
        if self.currentBoard:
            self.currentBoard.removeNode()
            self.currentBoard = None
        if self.onDeckBoard:
            self.onDeckBoard.removeNode()
            self.onDeckBoard = None
        self.sawingLine = None
        self.progressDescriptionLabel.destroy()
        self.progressDescriptionLabel = None
        self.progressLabel.destroy()
        self.progressLabel = None
        self.boardDestroyedLabel.destroy()
        self.boardDestroyedLabel = None
        for key in self.boardsPool.keys():
            board = self.boardsPool[key]
            if not board.isEmpty():
                board.removeNode()

        self.boardsPool.clear()
        self.newBoardSequence.clearToInitial()
        del self.newBoardSequence
        self.splitBoardSequence.clearToInitial()
        del self.splitBoardSequence
        self.dropBoardSequence.clearToInitial()
        del self.dropBoardSequence
        return

    def setDifficulty(self, difficulty):
        RepairMincroGame.setDifficulty(self, difficulty)
        percent = difficulty / self.repairGame.difficultyMax
        difIndex = int(math.floor(percent * (len(self.config.difficultySets) - 1)))
        self.currentDifficultySet = self.config.difficultySets[difIndex]

    def splitBoard(self):
        self.sawingLine.reset()
        board = self.currentBoard
        boardIndex = self.currentBoardIndex
        if self.hitZone2Penalty:
            boardSplitAnim = Parallel(LerpPosInterval(self.board_left, duration=self.config.splitBoardAnimTime, pos=Point3(-2.0, 0.0, 0.0)), LerpPosInterval(self.board_right, duration=self.config.splitBoardAnimTime, pos=Point3(2.0, 0.0, 0.0)), LerpFunc(self.zone2_left.setSa, duration=self.config.splitBoardAnimTime / 2.0, fromData=1.0, toData=0.0), LerpFunc(self.zone2_right.setSa, duration=self.config.splitBoardAnimTime / 2.0, fromData=1.0, toData=0.0), LerpFunc(self.zone1_left.setSa, duration=self.config.splitBoardAnimTime / 2.0, fromData=1.0, toData=0.0), LerpFunc(self.zone1_right.setSa, duration=self.config.splitBoardAnimTime / 2.0, fromData=1.0, toData=0.0), LerpFunc(self.cut.setSa, duration=self.config.splitBoardAnimTime / 2.0, fromData=1.0, toData=0.0))
        elif self.hitZone1Penalty:
            boardSplitAnim = Parallel(LerpPosInterval(self.board_left, duration=self.config.splitBoardAnimTime, pos=Point3(-2.0, 0.0, 0.0)), LerpPosInterval(self.board_right, duration=self.config.splitBoardAnimTime, pos=Point3(2.0, 0.0, 0.0)), LerpPosInterval(self.zone2_left, duration=self.config.splitBoardAnimTime, pos=Point3(-2.0, 0.0, 0.0)), LerpPosInterval(self.zone2_right, duration=self.config.splitBoardAnimTime, pos=Point3(2.0, 0.0, 0.0)), LerpFunc(self.zone1_left.setSa, duration=self.config.splitBoardAnimTime / 2.0, fromData=1.0, toData=0.0), LerpFunc(self.zone1_right.setSa, duration=self.config.splitBoardAnimTime / 2.0, fromData=1.0, toData=0.0), LerpFunc(self.cut.setSa, duration=self.config.splitBoardAnimTime / 2.0, fromData=1.0, toData=0.0))
        else:
            boardSplitAnim = Parallel(LerpPosInterval(self.piece1, duration=self.config.splitBoardAnimTime, pos=Point3(-2.0, self.config.boardYDist, 0.0)), LerpPosInterval(self.piece2, duration=self.config.splitBoardAnimTime, pos=Point3(2.0, self.config.boardYDist, 0.0)), LerpFunc(self.cut.setSa, duration=self.config.splitBoardAnimTime / 2.0, fromData=1.0, toData=0.0))
        self.splitBoardSequence = Sequence(Func(self.updateScore), Func(self.boardComplete.play), boardSplitAnim, Func(board.stash), Func(self.piece1.setPos, self.piece1.getPos()), Func(self.piece2.setPos, self.piece2.getPos()), Func(self.board_right.setPos, self.board_right.getPos()), Func(self.board_left.setPos, self.board_left.getPos()), Func(self.zone2_right.setPos, self.zone2_right.getPos()), Func(self.zone2_left.setPos, self.zone2_left.getPos()), Func(self.zone1_right.setPos, self.zone1_right.getPos()), Func(self.zone1_left.setPos, self.zone1_left.getPos()), Func(self.cut.setSa, 1.0), Func(self.zone1_right.setSa, 1.0), Func(self.zone1_left.setSa, 1.0), Func(self.zone2_right.setSa, 1.0), Func(self.zone2_left.setSa, 1.0), Func(self.board_right.setSa, 1.0), Func(self.board_left.setSa, 1.0), Func(self.loadNewBoard), Func(self.addBoardBackToPool, board, boardIndex), name='RepairSawGame.splitBoardSequence')
        self.splitBoardSequence.start()

    def dropBoard(self):
        board = self.currentBoard
        boardIndex = self.currentBoardIndex
        self.dropBoardSequence = Sequence(Parallel(Sequence(Func(self.boardDestroyedLabel.unstash), Wait(1.5), Func(self.boardDestroyedLabel.stash)), Sequence(Wait(0.5), Func(self.boardDestroyed.play), Func(self.sawingLine.reset), LerpPosInterval(board, duration=self.config.splitBoardAnimTime, pos=Point3(0.0, 0.0, -2.0)), Func(board.stash), Wait(0.5), Func(self.loadNewBoard), Func(self.addBoardBackToPool, board, boardIndex))), name='RepairSawGame.dropBoardSequence')
        self.dropBoardSequence.start()

    def addBoardBackToPool(self, board, boardIndex):
        if 'copy1_%s' % boardIndex not in self.boardsPool:
            self.boardsPool['copy1_%s' % boardIndex] = board
        elif 'copy2_%s' % boardIndex not in self.boardsPool:
            self.boardsPool['copy2_%s' % boardIndex] = board
        else:
            self.notify.error('Two copies of board type %i already in the boardsPool!' % boardIndex)

    def updateScoreText(self):
        self.progressLabel.unstash()
        self.progressDescriptionLabel.unstash()
        if self.hitBoardPenalty:
            self.progressLabel['text'] = PLocalizer.Minigame_Repair_Sawing_Thresholds[0]
            self.progressLabel['text_fg'] = Vec4(1.0, 0.0, 0.0, 1.0)
            self.progressLabel.setText()
        elif self.hitZone2Penalty:
            self.progressLabel['text'] = PLocalizer.Minigame_Repair_Sawing_Thresholds[1]
            self.progressLabel['text_fg'] = Vec4(1.0, 0.5, 0.0, 1.0)
            self.progressLabel.setText()
        elif self.hitZone1Penalty:
            self.progressLabel['text'] = PLocalizer.Minigame_Repair_Sawing_Thresholds[2]
            self.progressLabel['text_fg'] = Vec4(1.0, 1.0, 0.0, 1.0)
            self.progressLabel.setText()
        else:
            self.progressLabel['text'] = PLocalizer.Minigame_Repair_Sawing_Thresholds[3]
            self.progressLabel['text_fg'] = Vec4(0.0, 1.0, 0.0, 1.0)
            self.progressLabel.setText()

    def moveNewBoardOnDeck(self):
        boardIndex = random.randint(0, len(self.currentDifficultySet) - 1)
        boardType = self.currentDifficultySet[boardIndex]
        boardType -= 1
        if 'copy1_%s' % boardType in self.boardsPool:
            self.onDeckBoard = self.boardsPool['copy1_%s' % boardType]
            del self.boardsPool['copy1_%s' % boardType]
        elif 'copy2_%s' % boardType in self.boardsPool:
            self.onDeckBoard = self.boardsPool['copy2_%s' % boardType]
            del self.boardsPool['copy2_%s' % boardType]
        else:
            self.notify.error('No copies of board type %i in the boardsPool!' % boardType)
        self.onDeckBoardIndex = boardType
        self.onDeckBoard.setScale(0.25)
        self.onDeckBoard.setPos(0.5, -2.0, 0.56)
        self.onDeckBoard.unstash()

    def loadNewBoard(self):
        self.progressLabel.stash()
        self.progressDescriptionLabel.stash()
        if self.totalScore >= self.config.totalPoints:
            if self.onDeckBoard:
                self.onDeckBoard.stash()
            self.progressDescriptionLabel.stash()
            taskMgr.remove('SawingGame.updateSawTask')
            self.request('Outro')
            return
        self.currentBoard = self.onDeckBoard
        self.currentBoardIndex = self.onDeckBoardIndex
        self.piece1 = self.currentBoard.find('**/piece_1')
        self.piece1.setTransparency(1)
        self.piece2 = self.currentBoard.find('**/piece_2')
        self.piece2.setTransparency(1)
        self.cut = self.currentBoard.find('**/piece_cut')
        self.cut.setColor(self.config.cutColor)
        self.cut.setTransparency(1)
        self.board_left = self.piece1.find('**/board')
        self.board_left.setTransparency(1)
        self.zone1_left = self.piece1.find('**/zone_1')
        self.zone1_left.setTransparency(1)
        self.zone2_left = self.piece1.find('**/zone_2')
        self.zone2_left.setTransparency(1)
        self.board_right = self.piece2.find('**/board')
        self.board_right.setTransparency(1)
        self.zone1_right = self.piece2.find('**/zone_1')
        self.zone1_right.setTransparency(1)
        self.zone2_right = self.piece2.find('**/zone_2')
        self.zone2_right.setTransparency(1)
        self.board_left.setCollideMask(SAW_COLLIDE_MASK)
        self.board_right.setCollideMask(SAW_COLLIDE_MASK)
        self.cut.setCollideMask(SAW_COLLIDE_MASK)
        self.zone1_right.setCollideMask(SAW_COLLIDE_MASK)
        self.zone1_left.setCollideMask(SAW_COLLIDE_MASK)
        self.zone2_right.setCollideMask(SAW_COLLIDE_MASK)
        self.zone2_left.setCollideMask(SAW_COLLIDE_MASK)
        self.startPositions = (
         self.currentBoard.find('**/locator_start_0').getPos() + Point3(*self.config.activeBoardPosition), self.currentBoard.find('**/locator_start_1').getPos() + Point3(*self.config.activeBoardPosition))
        self.currentStartIndex = 0
        for waypoint in self.sawWaypoints:
            waypoint.removeNode()

        self.sawWaypoints = []
        locator = self.currentBoard.find('**/locator_0')
        index = 0
        while not locator.isEmpty():
            self.sawWaypoints.append(SawWaypoint(index, self.currentBoard, locator.getPos()))
            locator = self.currentBoard.find('**/locator_%i' % (index + 1))
            index += 1

        self.sawButton.deactivate()
        self.sawButton.setPos(self.startPositions[self.currentStartIndex])
        self.hitBoardPenalty = False
        self.hitZone1Penalty = False
        self.hitZone2Penalty = False
        self.lastMousePos = None
        self.moveDiffForSound = self.config.playSawingSoundDelta + 0.1
        self.newBoardSequence = Sequence(Parallel(self.currentBoard.posInterval(self.config.newBoardAnimTime, Point3(*self.config.activeBoardPosition)), self.currentBoard.scaleInterval(self.config.newBoardAnimTime, 1.0)), name='RepairSawingGame.newBoardSequence')
        if self.state in ['Game']:
            self.newBoardSequence.append(Func(self.sawButton.activate))
        self.newBoardSequence.append(Wait(0.5))
        self.newBoardSequence.append(Func(self.moveNewBoardOnDeck))
        self.newBoardSequence.start()
        return

    def updateSawTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            relative = Point3(mpos.getX(), 0.0, mpos.getY())
            relative = self.getRelativePoint(render2d, relative)
            moveDiff = 0.0
            if self.lastMousePos != None:
                moveDiff = (relative - self.lastMousePos).length()
            pickedObjects = self.repairGame.mousePicker.getCollisions(self.currentBoard, useIntoNodePaths=True)
            self.updateWaypoints()
            if len(pickedObjects) > 0:
                self.moveDiffForSound += moveDiff
                if self.moveDiffForSound > self.config.playSawingSoundDelta:
                    sawSoundPlaying = False
                    for sound in self.sawSounds:
                        if sound.status() == 2:
                            sawSoundPlaying = True
                            break

                    if sawSoundPlaying == False:
                        sound = random.choice(self.sawSounds)
                        sound.play()
                        self.moveDiffForSound = 0.0
                if self.board_right in pickedObjects or self.board_left in pickedObjects:
                    for waypoint in self.sawWaypoints:
                        waypoint.hit = False

                    self.hitBoardPenalty = True
                    self.dropBoard()
                    self.sawButton.deactivate()
                elif self.cut in pickedObjects:
                    self.updateWaypoints()
                elif self.zone1_right in pickedObjects or self.zone1_left in pickedObjects:
                    self.updateWaypoints()
                    if self.hitZone1Penalty == False:
                        self.hitZone1Penalty = True
                elif self.zone2_right in pickedObjects or self.zone2_left in pickedObjects:
                    self.updateWaypoints()
                    if self.hitZone2Penalty == False:
                        self.hitZone2Penalty = True
                self.updateScoreText()
            else:
                boardComplete = True
                for waypoint in self.sawWaypoints:
                    if not waypoint.hit:
                        boardComplete = False
                        break

                if boardComplete:
                    self.splitBoard()
                    self.sawButton.deactivate()
            self.lastMousePos = self.sawButton.getPos()
        return Task.cont

    def updateScore(self):
        if not self.hitBoardPenalty:
            currBoardScore = self.config.pointsPerBoard
            currBoardScore -= self.config.pointsLostForZone1 * (self.hitZone1Penalty or self.hitZone2Penalty)
            currBoardScore -= self.config.pointsLostForZone2 * self.hitZone2Penalty
            rating = 4 - 1 * self.hitZone2Penalty - 3 * self.hitZone1Penalty
            self.totalScore += currBoardScore
            self.totalScore = min(self.totalScore, self.config.totalPoints)
            percent = int(self.totalScore / self.config.totalPoints * 100.0)
            self.repairGame.d_reportMincroGameProgress(percent, rating)

    def resetWaypoints(self):
        for waypoint in self.sawWaypoints:
            waypoint.hit = False

    def updateWaypoints(self):
        waypointList = self.getHitWaypoints()
        for waypointIndex in waypointList:
            self.lastHitIndex = waypointIndex
            self.sawWaypoints[waypointIndex].hit = True
            if waypointIndex == 0 and not self.sawWaypoints[-1].hit:
                self.currentStartIndex = 0
            elif waypointIndex == len(self.sawWaypoints) - 1 and not self.sawWaypoints[0].hit:
                self.currentStartIndex = 1

    def getHitWaypoints(self):
        waypointsHit = []
        testDelta = self.config.testWaypointDelta
        for i in range(len(self.sawWaypoints)):
            waypointPos = self.sawWaypoints[i].getPos(self)
            closestDistance = 9999
            if self.lastMousePos != None:
                currMousePos = self.sawButton.getPos()
                lastMousePos = self.lastMousePos
                totalLength = (currMousePos - lastMousePos).length()
                testLength = testDelta
                while testLength < totalLength:
                    testPos = (currMousePos - lastMousePos) * (testLength / totalLength) + lastMousePos
                    self.updateSawLine(testPos)
                    testDistance = (testPos - waypointPos).length()
                    closestDistance = min(testDistance, closestDistance)
                    testLength += testDelta

            self.updateSawLine(self.sawButton.getPos())
            testDistance = (self.sawButton.getPos() - waypointPos).length()
            closestDistance = min(testDistance, closestDistance)
            if closestDistance < self.config.waypointRange[self.currentBoardIndex]:
                waypointsHit.append(i)

        return waypointsHit

    def updateSawLine(self, pos):
        if pos.getX() < -0.633 or pos.getX() > 0.633:
            self.sawingLine.reset()
            return
        if pos.getZ() < -0.183 or pos.getZ() > 0.375:
            self.sawingLine.reset()
            return
        self.sawingLine.update(pos)

    def getClosestPosition(self, positions):
        closestIndex = -1
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            relative = Point3(mpos.getX(), 0.0, mpos.getY())
            relative = self.getRelativePoint(base.a2dBackground, relative)
            bestDistance = 99999.0
            for i in range(len(positions)):
                dX = relative.getX() - positions[i].getX()
                dZ = relative.getZ() - positions[i].getZ()
                newDistance = dX * dX + dZ * dZ
                if newDistance < bestDistance:
                    bestDistance = newDistance
                    closestIndex = i

        return closestIndex

    def sawAttachedToMouse(self):
        self.lastHitIndex = -1
        if not taskMgr.hasTaskNamed('SawingGame.updateSawTask'):
            taskMgr.add(self.updateSawTask, 'SawingGame.updateSawTask', priority=2)

    def sawRemovedFromMouse(self):
        if not self.sawButton.isStashed():
            self.sawButton.setPos(self.startPositions[self.currentStartIndex])
            self.lastHitIndex = -1
            self.resetWaypoints()
            self.lastMousePos = None
            self.progressLabel.stash()
            self.progressDescriptionLabel.stash()
            self.sawingLine.reset()
            self.hitBoardPenalty = False
            self.hitZone1Penalty = False
            self.hitZone2Penalty = False
        taskMgr.remove('SawingGame.updateSawTask')
        return

    def enterIntro(self):
        RepairMincroGame.enterIntro(self)
        self.loadNewBoard()

    def enterGame(self):
        RepairMincroGame.enterGame(self)
        self.repairGame.mousePicker.setCollisionMask(SAW_COLLIDE_MASK)
        self.sawButton.activate()

    def exitGame(self):
        RepairMincroGame.exitGame(self)
        self.sawButton.deactivate()
        self.repairGame.mousePicker.clearCollisionMask()
        taskMgr.remove('SawingGame.updateSawTask')
        self.splitBoardSequence.clearToInitial()
        self.dropBoardSequence.clearToInitial()
        localAvatar.guiMgr._showCursor()

    def enterOutro(self):
        RepairMincroGame.enterOutro(self)
        self.repairGame.d_reportMincroGameScore(150)