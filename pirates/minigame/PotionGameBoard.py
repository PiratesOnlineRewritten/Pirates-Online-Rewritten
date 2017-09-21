from direct.interval.IntervalGlobal import Sequence, Func
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pirates.piratesgui.GuiPanel import *
from direct.showbase import DirectObject
from direct.task import Task
from pandac.PandaModules import *
from pandac.PandaModules import CardMaker
from pandac.PandaModules import Vec2
from direct.task import Task
from pirates.piratesbase import PLocalizer
from PotionBoardPiece import PotionBoardPiece
from pirates.piratesgui import PiratesGuiGlobals
import PotionGlobals

class PotionGameBoard(DirectFrame):

    def __init__(self, potionGame):
        self.numColumns = 8
        self.numRows = 10
        DirectFrame.__init__(self, parent=potionGame.background, relief=None)
        cm = CardMaker('card')
        cm.setFrame(0, 0, 1.0, 1.0)
        self.background = self.attachNewNode(cm.generate())
        self.background.setColor(0.2, 0.2, 0.2, 1)
        self.potionGame = potionGame
        self.pieceDropped = False
        self.pieceFlipped = False
        self.pieceNotDropped = False
        self.delayDropped = False
        self.experementMatched = False
        self.experementFailed = False
        self.initBoard()
        return

    def initBoard(self):
        self.boardPieces = []
        ColumnList = range(self.numColumns)
        RowList = range(self.numRows)
        for columnIndex in ColumnList:
            self.boardPieces.append([])
            for rowIndex in RowList:
                self.boardPieces[columnIndex].append(None)

        self.rightPlayerPiece = None
        self.leftPlayerPiece = None
        self.leftPreviewPiece = None
        self.rightPreviewPiece = None
        self.lastLeftCol = 0
        self.lastRightCol = 1
        self.lastDragPos = None
        self.dragPiece = None
        return

    def resetBoard(self):
        for column in self.boardPieces:
            for piece in column:
                if piece is not None:
                    piece.removeNode()
                    del piece

        if self.rightPlayerPiece is not None:
            self.rightPlayerPiece.removeNode()
        if self.leftPlayerPiece is not None:
            self.leftPlayerPiece.removeNode()
        if self.leftPreviewPiece is not None:
            self.leftPreviewPiece.removeNode()
        if self.rightPreviewPiece is not None:
            self.rightPreviewPiece.removeNode()
        del self.rightPlayerPiece
        del self.leftPlayerPiece
        del self.leftPreviewPiece
        del self.rightPreviewPiece
        self.initBoard()
        return

    def jumpLeft(self):
        if self.leftPlayerPiece.column > 0:
            self.leftPlayerPiece.column -= 1
            self.leftPlayerPiece.setBoardPos(self.leftPlayerPiece.column, self.leftPlayerPiece.row)
            self.rightPlayerPiece.column -= 1
            self.rightPlayerPiece.setBoardPos(self.rightPlayerPiece.column, self.leftPlayerPiece.row)

    def jumpRight(self):
        if self.rightPlayerPiece.column < self.numColumns - 1:
            self.leftPlayerPiece.column += 1
            self.leftPlayerPiece.setBoardPos(self.leftPlayerPiece.column, self.leftPlayerPiece.row)
            self.rightPlayerPiece.column += 1
            self.rightPlayerPiece.setBoardPos(self.rightPlayerPiece.column, self.leftPlayerPiece.row)

    def moveLeft(self):
        if self.leftPlayerPiece.column > 0:
            self.disableInputEvents()
            self.potionGame.animationList.append(self.leftPlayerPiece.moveLeft())
            self.potionGame.animationList.append(self.rightPlayerPiece.moveLeft())
            self.potionGame.gameFSM.request('Anim')

    def moveRight(self):
        if self.rightPlayerPiece.column < self.numColumns - 1:
            self.disableInputEvents()
            self.potionGame.animationList.append(self.leftPlayerPiece.moveRight())
            self.potionGame.animationList.append(self.rightPlayerPiece.moveRight())
            self.potionGame.gameFSM.request('Anim')

    def moveUp(self):
        self.disableInputEvents()
        self.potionGame.animationList.append(self.leftPlayerPiece.moveRight())
        self.potionGame.animationList.append(self.rightPlayerPiece.moveLeft())
        temp = self.leftPlayerPiece
        self.leftPlayerPiece = self.rightPlayerPiece
        self.rightPlayerPiece = temp
        self.pieceFlipped = True
        self.potionGame.gameFSM.request('Anim')

    def moveDown(self):
        self.disableInputEvents()
        if self.boardPieces[self.leftPlayerPiece.column][self.leftPlayerPiece.row - 1] is None and self.boardPieces[self.rightPlayerPiece.column][self.rightPlayerPiece.row - 1] is None:
            self.boardPieces[self.leftPlayerPiece.column][self.leftPlayerPiece.row] = self.leftPlayerPiece
            self.boardPieces[self.rightPlayerPiece.column][self.rightPlayerPiece.row] = self.rightPlayerPiece
            self.checkFall(True)
            self.pieceDropped = True
            self.potionGame.currentRecipe.useTiles(2)
            self.potionGame.gameFSM.request('Anim')
            self.lastLeftCol = self.leftPlayerPiece.column
            self.lastRightCol = self.rightPlayerPiece.column
            self.rightPlayerPiece = None
            self.leftPlayerPiece = None
        else:
            self.pieceNotDropped = True
            self.leftPlayerPiece.setY(-5)
            self.rightPlayerPiece.setY(-5)
            self.potionGame.animationList.append(Sequence(Parallel(LerpPosInterval(self.leftPlayerPiece, duration=0.1, pos=(self.leftPlayerPiece.getX(), self.leftPlayerPiece.getY(), self.leftPlayerPiece.getZ() - 0.05)), LerpPosInterval(self.rightPlayerPiece, duration=0.1, pos=(self.rightPlayerPiece.getX(), self.rightPlayerPiece.getY(), self.rightPlayerPiece.getZ() - 0.05))), Parallel(LerpPosInterval(self.leftPlayerPiece, duration=0.1, pos=(self.leftPlayerPiece.getX(), self.leftPlayerPiece.getY(), self.leftPlayerPiece.getZ())), LerpPosInterval(self.rightPlayerPiece, duration=0.1, pos=(self.rightPlayerPiece.getX(), self.rightPlayerPiece.getY(), self.rightPlayerPiece.getZ()))), Func(self.leftPlayerPiece.setY, 0), Func(self.rightPlayerPiece.setY, 0)))
            self.potionGame.gameFSM.request('Anim')
        return

    def checkFall(self, drop):
        for columnIndex in range(self.numColumns):
            for rowIndex in range(self.numRows - 1):
                if self.boardPieces[columnIndex][rowIndex] is None:
                    filled = False
                    for rowIndex2 in range(rowIndex + 1, self.numRows):
                        if self.boardPieces[columnIndex][rowIndex2] is not None and filled == False:
                            filled = True
                            self.boardPieces[columnIndex][rowIndex] = self.boardPieces[columnIndex][rowIndex2]
                            self.boardPieces[columnIndex][rowIndex2] = None
                            piece = self.boardPieces[columnIndex][rowIndex]
                            self.potionGame.animationList.append(Sequence(Func(piece.setY, -5), piece.moveToBoard(columnIndex, rowIndex), Func(piece.setY, 0)))

        return

    def showSoulXP(self, Xloc, Zloc, count):
        xpAmt = PotionGlobals.BONUS_XP_AMT[count]
        xpLabel = DirectLabel(parent=aspect2d, relief=None, text='+ ' + str(xpAmt) + ' ' + PLocalizer.PotionGui['XPLabel'], text_scale=PiratesGuiGlobals.TextScaleTitleLarge, text_font=PiratesGlobals.getPirateOutlineFont(), text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=37, pos=(Xloc, 0, Zloc - 0.1), textMayChange=0)
        xpLabel.setTransparency(True)
        xpLabel.stash()
        return Sequence(Func(xpLabel.unstash), Parallel(LerpPosInterval(xpLabel, duration=2.5, pos=(Xloc, 0.0, Zloc + 0.3), blendType='easeOut'), LerpColorScaleInterval(xpLabel, duration=1.5, colorScale=(1, 1, 1, 0), blendType='easeIn')), Func(xpLabel.removeNode))

    def findGroups(self):
        self.groups = []
        for column in self.boardPieces:
            for piece in column:
                if piece is not None:
                    piece.findConnections(self)

        self.removeList = []
        self.upgradeList = []
        for column in self.boardPieces:
            for piece in column:
                if piece is not None:
                    piece.pendingMatch = False
                    if len(piece.connections) > 0:
                        found = False
                        for group in self.groups:
                            if piece in group:
                                found = True

                        if not found:
                            self.groups.append([])
                            self.addToGroup(self.groups[-1], piece)

        for group in self.groups:
            if len(group) > 2:
                group.sort(reverse=True)
                removePiece = group[0]
                self.removeList.append(removePiece)
                group.remove(removePiece)
                for piece in group:
                    if removePiece in piece.connections:
                        piece.connectionsRemoved += 1

                group.sort(reverse=True)
                removePiece = group[0]
                self.removeList.append(removePiece)
                group.remove(removePiece)
                bonusPieces = 0
                avgX = 0
                avgZ = 0
                for piece in group:
                    if piece.level < 6:
                        self.upgradeList.append(piece)
                        if piece.level == 5:
                            self.potionGame.soulMade = True
                    else:
                        self.removeList.append(piece)
                        bonusPieces += 1
                        avgX += piece.getX(aspect2d)
                        avgZ += piece.getZ(aspect2d)

                if bonusPieces > 0:
                    avgX /= float(len(group))
                    avgZ /= float(len(group))
                    self.potionGame.soulMatch = True
                    self.potionGame.currentRecipe.clearedSouls(bonusPieces + 2)
                    self.potionGame.animationList.append(self.showSoulXP(avgX, avgZ, bonusPieces - 1))
                    self.potionGame.dist.d_claimXPBonus(bonusPieces - 1)

        if len(self.removeList) > 0:
            self.previewGroups = []
            for column in self.boardPieces:
                for piece in column:
                    if piece is not None:
                        piece.previewConnections(self)

            for column in self.boardPieces:
                for piece in column:
                    if piece is not None:
                        if len(piece.pendingConnections) > 0:
                            found = False
                            for group in self.previewGroups:
                                if piece in group:
                                    found = True

                            if not found:
                                self.previewGroups.append([])
                                self.addToPreviewGroup(self.previewGroups[-1], piece)

            for group in self.previewGroups:
                if len(group) > 2:
                    for piece in group:
                        piece.pendingMatch = True

            upgradeCount = len(self.upgradeList)
            self.potionGame.currentRecipe.madeIngredients(upgradeCount)
            self.removePieces()
            self.upgradePieces()
        return

    def addToPreviewGroup(self, group, piece):
        group.append(piece)
        for nextPiece in piece.pendingConnections:
            if nextPiece not in group:
                self.addToPreviewGroup(group, nextPiece)

    def addToGroup(self, group, piece):
        group.append(piece)
        for nextPiece in piece.connections:
            if nextPiece not in group:
                self.addToGroup(group, nextPiece)

    def removePieces(self):
        for piece in self.removeList:
            self.boardPieces[piece.column][piece.row] = None
            mergePiece = None
            for adjPiece in piece.connections:
                if adjPiece in self.upgradeList:
                    mergePiece = adjPiece

            if mergePiece is None:
                for adjPiece in piece.connections:
                    for adjadjPiece in adjPiece.connections:
                        if adjadjPiece in self.upgradeList:
                            mergePiece = adjadjPiece

            if mergePiece is not None:
                rotQuat = Quat()
                rotQuat.setHpr((piece.getH(), piece.getP() + 90, piece.getR()))
                outInterval = Parallel(LerpQuatInterval(piece.background, duration=0.4, quat=rotQuat, blendType='easeIn'), piece.moveToBoardSlow(mergePiece.column, mergePiece.row))
            else:
                outInterval = LerpColorInterval(piece.background, duration=0.6, color=(1, 1, 1, 0))
            self.potionGame.animationList.append(Sequence(Func(piece.setY, 5), outInterval, Func(piece.removeNode), Func(self.kill, piece)))

        return

    def upgradePieces(self):
        for columnIndex in range(self.numColumns):
            for rowIndex in range(self.numRows - 1):
                if self.boardPieces[columnIndex][rowIndex] is None:
                    filled = False
                    for rowIndex2 in range(rowIndex + 1, self.numRows):
                        if self.boardPieces[columnIndex][rowIndex2] is not None:
                            if filled == False:
                                filled = True
                                piece = self.boardPieces[columnIndex][rowIndex2]
                                if not piece.pendingMatch:
                                    self.boardPieces[columnIndex][rowIndex] = self.boardPieces[columnIndex][rowIndex2]
                                    self.boardPieces[columnIndex][rowIndex2] = None
                                    if piece in self.upgradeList:
                                        rotQuat = Quat()
                                        rotQuat2 = Quat()
                                        rotQuat3 = Quat()
                                        rotQuat.setHpr((piece.getH(), piece.getP() + 90, piece.getR()))
                                        rotQuat2.setHpr((piece.getH(), piece.getP() + 270, piece.getR()))
                                        rotQuat3.setHpr((piece.getH(), piece.getP() + 360, piece.getR()))
                                        self.potionGame.animationList.append(Sequence(Func(piece.setY, -10), LerpQuatInterval(piece.background, duration=0.4, quat=rotQuat, blendType='easeIn'), Func(piece.upgrade), Parallel(piece.moveToBoardSlow(columnIndex, rowIndex), LerpQuatInterval(piece.background, duration=0.4, quat=rotQuat3, startQuat=rotQuat2, blendType='easeOut')), Func(piece.setY, 0)))
                                        self.delayDropped = True
                                        self.upgradeList.remove(piece)
                                    else:
                                        self.delayDropped = True
                                        self.potionGame.animationList.append(Sequence(Func(piece.setY, -5), Wait(0.5), piece.moveToBoard(columnIndex, rowIndex), Func(piece.setY, 0)))

        for piece in self.upgradeList:
            rotQuat = Quat()
            rotQuat2 = Quat()
            rotQuat3 = Quat()
            rotQuat.setHpr((piece.getH(), piece.getP() + 90, piece.getR()))
            rotQuat2.setHpr((piece.getH(), piece.getP() + 270, piece.getR()))
            rotQuat3.setHpr((piece.getH(), piece.getP() + 360, piece.getR()))
            piece.setY(-10)
            OutSeq = LerpQuatInterval(piece.background, duration=0.4, quat=rotQuat3, startQuat=rotQuat2, blendType='easeOut')
            self.potionGame.animationList.append(Sequence(LerpQuatInterval(piece.background, duration=0.4, quat=rotQuat, blendType='easeIn'), Func(piece.upgrade), OutSeq, Func(piece.setY, 0)))

        return

    def kill(self, piece):
        del piece

    def handleMouseDown(self):
        if base.mouseWatcherNode.hasMouse():
            screenx = base.mouseWatcherNode.getMouseX()
            screeny = base.mouseWatcherNode.getMouseY()
            self.lastDragPos = self.getRelativePoint(render2d, (screenx, 0, screeny))
            self.dragDist = 0

    def handleMouseUp(self):
        dragHandled = False
        if self.lastDragPos is not None:
            if base.mouseWatcherNode.hasMouse():
                screenx = base.mouseWatcherNode.getMouseX()
                screeny = base.mouseWatcherNode.getMouseY()
                dragPos = self.getRelativePoint(render2d, (screenx, 0, screeny))
                self.dragDist += (dragPos - self.lastDragPos).length()
                if self.dragDist < 0.01:
                    if self.dragPiece is not None:
                        self.dragPiece.wrtReparentTo(self)
                        self.potionGame.animationList.append(Sequence(self.dragPiece.moveToBoard(self.dragPiece.column, self.dragPiece.row), Func(self.dragPiece.setY, 0)))
                        self.dragPiece = None
                    if screenx > 0 and screeny > -0.8 and screenx < 0.88 and screeny < 0.92:
                        self.moveDown()
                if self.dragPiece is not None:
                    if False:
                        recipePos = self.potionGame.currentRecipe.getRelativePoint(render2d, (screenx, 0, screeny))
                        neededIngredient = None
                        for ingredient in self.potionGame.currentRecipe.ingredients:
                            if ingredient.hiddenColor == self.dragPiece.colorIndex and ingredient.hiddenLevel == self.dragPiece.level and not ingredient.completed:
                                neededIngredient = ingredient

                        if neededIngredient is not None:
                            for ingredient in self.potionGame.currentRecipe.ingredients:
                                if not ingredient.completed and not dragHandled:
                                    ingredientDist = (ingredient.getPos() - recipePos).length()
                                    if ingredientDist < 0.2:
                                        neededIngredient.completed = True
                                        self.dragPiece.wrtReparentTo(self.potionGame.currentRecipe)
                                        self.boardPieces[self.dragPiece.column][self.dragPiece.row] = None
                                        self.lastDragPos = None
                                        self.potionGame.animationList.append(Sequence(self.dragPiece.moveToBoard(neededIngredient.column, neededIngredient.row), Func(neededIngredient.setColor, self.dragPiece.colorIndex, self.dragPiece.level), Func(self.killDragPiece)))
                                        dragHandled = True
                                        self.experementMatched = True
                                        self.potionGame.gameFSM.request('Anim')

                        else:
                            for ingredient in self.potionGame.currentRecipe.ingredients:
                                if not ingredient.completed:
                                    ingredientDist = (ingredient.getPos() - recipePos).length()
                                    if ingredientDist < 0.2:
                                        self.experementFailed = True

                if self.dragPiece is not None and not dragHandled:
                    self.dragPiece.wrtReparentTo(self)
                    self.potionGame.animationList.append(Sequence(self.dragPiece.moveToBoard(self.dragPiece.column, self.dragPiece.row), Func(self.dragPiece.setY, 0)))
                    self.potionGame.gameFSM.request('Anim')
                    self.dragPiece = None
                self.lastDragPos = None
        return

    def killDragPiece(self):
        self.dragPiece.removeNode()
        del self.dragPiece
        self.dragPiece = None
        return

    def enableInputEvents(self):
        self.accept('mouse1', self.handleMouseDown)
        self.accept('mouse1-up', self.handleMouseUp)
        self.accept('mouse3', self.moveUp)
        self.accept('space', self.moveUp)
        taskMgr.add(self.handleMouseLoc, 'PotionMinigameMouseInputTask')

    def disableInputEvents(self):
        self.ignore('j')
        self.ignore('l')
        self.ignore('k')
        self.ignore('i')
        self.ignore('mouse1')
        self.ignore('mouse1-up')
        self.ignore('mouse3')
        self.ignore('space')
        taskMgr.remove('PotionMinigameMouseInputTask')

    def handleMouseLoc(self, task):
        if base.mouseWatcherNode.hasMouse():
            screenx = base.mouseWatcherNode.getMouseX()
            screeny = base.mouseWatcherNode.getMouseY()
            localMousePos = self.getRelativePoint(render2d, (screenx, 0, screeny))
            if self.lastDragPos is None and self.leftPlayerPiece is not None and self.rightPlayerPiece is not None:
                if localMousePos[0] < self.leftPlayerPiece.Xpos:
                    self.jumpLeft()
                if localMousePos[0] > self.rightPlayerPiece.Xpos:
                    self.jumpRight()
            elif self.lastDragPos is not None:
                self.dragDist += (localMousePos - self.lastDragPos).length()
                self.lastDragPos = localMousePos
                if self.dragDist > 0.01 and self.dragPiece is not None:
                    globalMousePos = self.potionGame.background.getRelativePoint(render2d, (screenx, 0, screeny))
                    self.dragPiece.setPiecePosition(globalMousePos[0], globalMousePos[2])
        return Task.cont

    def playerPieceActive(self):
        return self.rightPlayerPiece is not None and self.leftPlayerPiece is not None

    def checkAvailableMoves(self):
        movesLeft = False
        for columnIndex in range(self.numColumns - 1):
            if self.boardPieces[columnIndex][self.numRows - 2] is None and self.boardPieces[columnIndex + 1][self.numRows - 2] is None:
                movesLeft = True

        return movesLeft

    def addNewPiece(self):
        currentRecipe = self.potionGame.currentRecipe
        if self.leftPreviewPiece is None:
            self.leftPreviewPiece = PotionBoardPiece(self, recipe=currentRecipe)
            self.rightPreviewPiece = PotionBoardPiece(self, recipe=currentRecipe)
            self.leftPreviewPiece.setBoardPos(-4, self.numRows - 1)
            self.rightPreviewPiece.setBoardPos(-3, self.numRows - 1)
        self.leftPlayerPiece = self.leftPreviewPiece
        self.rightPlayerPiece = self.rightPreviewPiece
        self.leftPreviewPiece = PotionBoardPiece(self, colorSet=self.potionGame.dist.colorSet, recipe=currentRecipe)
        self.rightPreviewPiece = PotionBoardPiece(self, colorSet=self.potionGame.dist.colorSet, recipe=currentRecipe)
        self.leftPreviewPiece.setBoardPos(-4, self.numRows - 1)
        self.rightPreviewPiece.setBoardPos(-3, self.numRows - 1)
        self.leftPlayerPiece.setY(-5)
        self.leftPlayerPiece.reparentTo(self)
        self.rightPlayerPiece.setY(-5)
        self.rightPlayerPiece.reparentTo(self)
        self.leftPlayerPiece.moveFast = True
        self.rightPlayerPiece.moveFast = True
        self.potionGame.animationList.append(Sequence(self.leftPlayerPiece.moveToBoard(self.lastLeftCol, self.numRows - 1), Func(self.leftPlayerPiece.setY, 0)))
        self.potionGame.animationList.append(Sequence(self.rightPlayerPiece.moveToBoard(self.lastRightCol, self.numRows - 1), Func(self.rightPlayerPiece.setY, 0)))
        return