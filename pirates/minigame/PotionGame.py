from direct.interval.IntervalGlobal import Sequence, Func
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pirates.piratesgui.GuiPanel import *
from direct.showbase import DirectObject
from direct.task import Task
from pandac.PandaModules import *
from pandac.PandaModules import CardMaker
from PotionGameFSM import PotionGameFSM
from PotionRecipePicker import PotionRecipePicker
from PotionRecipe import PotionRecipe
from PotionResults import PotionResults
from PotionFail import PotionFail
from PotionBoardPiece import PotionBoardPiece
from PotionGameBoard import PotionGameBoard
from PotionHint import PotionHint
from PotionInfo import PotionInfo
import PotionGlobals
import PotionRecipeData
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import PiratesConfirm
from pirates.piratesgui import ReputationMeter
from pirates.piratesgui import GuiManager
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory
import math

class PotionGame(DirectObject.DirectObject):

    def __init__(self, dist):
        self.dist = dist
        self.askToExit = False
        self.askToReturn = False
        self.askForHint = False
        self.askForInfo = False
        self.soulMade = False
        self.soulMatch = False
        self.closeCurrentDialog = None
        self.animationList = []
        self.postAnimationList = []
        self.setupScene()
        self.gameFSM = PotionGameFSM(self)
        self.gameFSM.request('Intro')
        self.accept('clientLogout', self.destroy)
        self.confirm = None
        return

    def chestOpened(self):
        pass

    def chestClosed(self):
        pass

    def setupScene(self):
        base.loadingScreen.tick()
        base.disableMouse()
        self._initGUI()
        base.loadingScreen.beginStep('setupScene', 9, 45)
        base.loadingScreen.tick()
        self.hintScreen = PotionHint(self)
        self.hintScreen.stash()
        base.loadingScreen.tick()
        self.infoScreen = PotionInfo(self)
        self.infoScreen.stash()
        base.loadingScreen.tick()
        self.currentRecipe = None
        self.recipes = []
        for recipeData in PotionRecipeData.PotionRecipeList:
            valid = True
            if recipeData.get('disabled', False):
                continue
            for ingredient in recipeData['ingredients']:
                if ingredient['color'] not in PotionRecipeData.PotionColorSets[self.dist.colorSet]:
                    valid = False

            newRecipe = PotionRecipe(self, recipeData['potionID'], recipeData['name'], recipeData['desc'], recipeData['ingredients'], recipeData['level'], recipeData['free'], recipeData.get('questOnly', False))
            if valid:
                newRecipe.available = True
            else:
                newRecipe.available = False
            self.recipes.append(newRecipe)

        for recipe in self.recipes:
            recipe.setPos(-1.1, 0, -0.65)

        self.recipePicker = PotionRecipePicker(self)
        base.loadingScreen.tick()
        (self.recipePicker.setPos(0.0, 0.0, 0.0),)
        self.recipePicker.setEnabled(False)
        self.recipePicker.stash()
        self.resultsScreen = PotionResults(self)
        self.resultsScreen.stash()
        base.loadingScreen.tick()
        self.failScreen = PotionFail(self)
        self.failScreen.stash()
        base.loadingScreen.tick()
        self._initIntervals()
        base.loadingScreen.tick()
        self.gameBoard = PotionGameBoard(self)
        self.gameBoard.setPos(0.1, 0, -0.705)
        base.loadingScreen.tick()
        self.unlockList = []
        base.musicMgr.request(SoundGlobals.MUSIC_MINIGAME_POTION, priority=1, volume=0.4)
        base.loadingScreen.endStep('setupScene')
        return

    def resetScene(self):
        self.gameBoard.resetBoard()
        if self.currentRecipe is not None:
            self.currentRecipe.stash()
        return

    def _initGUI(self):
        base.loadingScreen.beginStep('init Gui', 4, 55)
        cm = CardMaker('PotionBackground')
        cm.setFrame(-10, 10, -10, 10)
        cm.setColor(0, 0, 0, 1)
        self.background = NodePath(cm.generate())
        self.background.reparentTo(aspect2d)
        self.background.setBin('background', -100)
        self.xpBackground = NodePath('PotionXPBackground')
        self.xpBackground.reparentTo(aspect2d)
        self.xpBackground.setBin('background', -95)
        base.loadingScreen.tick()
        self.dialogs = NodePath('DialogBackground')
        self.dialogs.reparentTo(aspect2d)
        self.dialogs.setBin('background', -70)
        self.buttonsBackground = NodePath('PotionButtonBackground')
        self.buttonsBackground.reparentTo(base.a2dBottomRight)
        self.buttonsBackground.setBin('background', -90)
        textureCard = loader.loadModel('models/minigames/pir_m_gui_pot_textureCard')
        self.stretchedBackgroundTextureCard = textureCard.find('**/pir_t_gui_pot_background')
        self.stretchedBackgroundTextureCard.reparentTo(self.background)
        self.stretchedBackgroundTextureCard.setScale(3.4, 1.0, 3.4)
        self.stretchedBackgroundTextureCard.setPos(0.0, 20.0, 0.0)
        fadecm = CardMaker('card')
        fadecm.setFrameFullscreenQuad()
        self.fadeIn = render2d.attachNewNode(fadecm.generate())
        self.fadeIn.setBin('background', -50)
        self.fadeIn.setPos(0.0, -30.0, 0.0)
        self.fadeIn.setColor(0, 0, 0, 1.0)
        self.fadeIn.setTransparency(True)
        base.loadingScreen.tick()
        cm = CardMaker('card')
        cm.setFrame(0, 1, 0.01, 0.01)
        self.foregroundLayer = aspect2d.attachNewNode(cm.generate())
        self.foregroundTextureCard = textureCard.find('**/pir_t_gui_pot_foreground')
        self.foregroundTextureCard.setScale(0.8, 1.0, 0.4)
        self.foregroundTextureCard.setPos(-0.7, -20.0, 0.8)
        self.foregroundTextureCard.setBin('background', -80)
        self.foregroundTextureCard.copyTo(self.foregroundLayer)
        self.repMeter = ReputationMeter.ReputationMeter(InventoryType.PotionsRep, width=0.56)
        inv = localAvatar.getInventory()
        self.repMeter.reparentTo(self.xpBackground)
        self.repMeter.setPos(0, 0, -0.95)
        self.repMeter.update(inv.getAccumulator(InventoryType.PotionsRep))
        localAvatar.guiMgr.registerReputationHandler(self.updateRepMeter)
        base.loadingScreen.tick()
        self.closeButton = GuiButton.GuiButton(image=(textureCard.find('**/pir_t_gui_pot_escape'), textureCard.find('**/pir_t_gui_pot_escapeOn'), textureCard.find('**/pir_t_gui_pot_escapeOn'), textureCard.find('**/pir_t_gui_pot_escape')), image_scale=(0.1,
                                                                                                                                                                                                                                                            0.1,
                                                                                                                                                                                                                                                            0.1), image_pos=(0.075,
                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                             0.08), hotkeys=['Escape'], hotkeyLabel=PLocalizer.PotionGui['ExitButton'], pos=(-0.4, 0.0, 0.01), text0_fg=PotionGlobals.TextColor, text1_fg=PiratesGuiGlobals.TextFG0, text2_fg=PiratesGuiGlobals.TextFG15, text3_fg=PotionGlobals.TextColorDisabled, parent=self.buttonsBackground, command=self.confirmQuit)
        self.returnButton = GuiButton.GuiButton(text=(PLocalizer.PotionGui['SwitchRecipe'], PLocalizer.PotionGui['SwitchRecipe'], PLocalizer.PotionGui['SwitchRecipe'], PLocalizer.PotionGui['SwitchRecipe']), pos=(-0.58, 0.0, -0.62), text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_shadow=None, image=(None,
                                                                                                                                                                                                                                                                                                                   None,
                                                                                                                                                                                                                                                                                                                   None,
                                                                                                                                                                                                                                                                                                                   None), text0_fg=PotionGlobals.TextColor, text1_fg=PiratesGuiGlobals.TextFG0, text2_fg=PiratesGuiGlobals.TextFG15, text3_fg=PotionGlobals.TextColorDisabled, parent=self.background, command=self.confirmReturn)
        self.returnButton.stash()
        self.hintsButton = GuiButton.GuiButton(text=(PLocalizer.PotionGui['ShowTutorial'], PLocalizer.PotionGui['ShowTutorial'], PLocalizer.PotionGui['ShowTutorial'], PLocalizer.PotionGui['ShowTutorial']), text_scale=PiratesGuiGlobals.TextScaleSmall, image_scale=(0.25,
                                                                                                                                                                                                                                                                        0.1,
                                                                                                                                                                                                                                                                        0.18), image_pos=(0,
                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                          0), pos=(-0.53, 0.0, 0.075), parent=self.buttonsBackground, command=self.showLastHint)
        self.InfoButton = GuiButton.GuiButton(text=(PLocalizer.PotionGui['IngredientList'], PLocalizer.PotionGui['IngredientList'], PLocalizer.PotionGui['IngredientList'], PLocalizer.PotionGui['IngredientList']), text_scale=PiratesGuiGlobals.TextScaleSmall, image_scale=(0.3,
                                                                                                                                                                                                                                                                               0.1,
                                                                                                                                                                                                                                                                               0.18), image_pos=(0,
                                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                                 0), pos=(-0.84, 0.0, 0.075), parent=self.buttonsBackground, command=self.showInfo)
        textureCard.removeNode()
        base.loadingScreen.endStep('init Gui')
        return

    def updateRepMeter(self, catagory, value):
        if catagory == InventoryType.PotionsRep:
            self.repMeter.update(value)

    def disableButtons(self):
        pass

    def enableButtons(self):
        pass

    def confirmQuit(self):
        if self.gameFSM.getCurrentOrNextState() in ['Intro', 'Exit']:
            return
        if self.gameFSM.getCurrentOrNextState() not in ['Anim']:
            if self.closeCurrentDialog is not None:
                self.closeCurrentDialog()
            if self.gameFSM.gameStarted:
                self.confirm = PiratesConfirm.PiratesConfirm(PLocalizer.PotionGui['ExitTitle'], PLocalizer.PotionGui['AbortAndExitText'], self.onCloseConfirmed)
                self.confirm.bNo['command'] = self.onCloseDeclined
                self.closeCurrentDialog = self.cleanUpConfirm
                self.gameBoard.disableInputEvents()
                self.disableButtons()
                self.gameFSM.demand('ExitRequest')
            else:
                self.confirm = PiratesConfirm.PiratesConfirm(PLocalizer.PotionGui['ExitTitle'], PLocalizer.PotionGui['ExitText'], self.onCloseConfirmed)
                self.confirm.bNo['command'] = self.onQuitDeclined
                self.closeCurrentDialog = self.cleanUpConfirm
                self.gameFSM.demand('ExitRequest')
            self.confirm.setPos(0.35, 0, -0.17)
        else:
            self.askToExit = True
        return

    def confirmReturn(self):
        if self.gameFSM.getCurrentOrNextState() in ['Intro', 'Exit']:
            return
        if self.gameFSM.getCurrentOrNextState() not in ['Anim']:
            if self.closeCurrentDialog is not None:
                self.closeCurrentDialog()
            self.closeCurrentDialog = self.cleanUpConfirm
            self.confirm = PiratesConfirm.PiratesConfirm(PLocalizer.PotionGui['SwitchTitle'], PLocalizer.PotionGui['SwitchText'], self.onReturnConfirmed)
            self.confirm.setPos(0.35, 0, -0.17)
            self.confirm.bNo['command'] = self.onCloseDeclined
            self.gameBoard.disableInputEvents()
            self.disableButtons()
            self.gameFSM.demand('SwitchRequest')
        else:
            self.askToReturn = True
        return

    def showLastHint(self):
        if self.gameFSM.getCurrentOrNextState() in ['Intro', 'Exit']:
            return
        if self.gameFSM.getCurrentOrNextState() not in ['Anim']:
            self.hintScreen.toggle()
        else:
            self.askForHint = True

    def showInfo(self):
        if self.gameFSM.getCurrentOrNextState() in ['Intro', 'Exit']:
            return
        if self.gameFSM.getCurrentOrNextState() not in ['Anim']:
            self.gameFSM.demand('Tutorial')
            self.infoScreen.toggle()
        else:
            self.askForInfo = True

    def cleanUpConfirm(self):
        self.closeCurrentDialog = None
        self.enableButtons()
        if self.confirm:
            self.confirm.destroy()
            self.confirm = None
        return

    def onQuitDeclined(self):
        self.cleanUpConfirm()
        self.gameFSM.request('RecipeSelect')

    def onCloseDeclined(self):
        self.cleanUpConfirm()
        self.gameFSM.request('Eval')

    def onCloseConfirmed(self):
        self.enableButtons()
        self.closeCurrentDialog = None
        self.gameFSM.request('Exit')
        return

    def onReturnConfirmed(self):
        self.enableButtons()
        self.closeCurrentDialog = None
        self.gameFSM.request('Reset')
        return

    def onIntroComplete(self):
        if self.hintScreen.show('RecipeList'):
            self.gameFSM.request('Tutorial')
        else:
            self.gameFSM.request('RecipeSelect')

    def _initIntervals(self):
        self.introSequence = Sequence(Wait(0.1), Func(self.recipePicker.unstash), LerpColorScaleInterval(self.fadeIn, colorScale=(1,
                                                                                                                                  1,
                                                                                                                                  1,
                                                                                                                                  0), duration=2.0), Func(self.onIntroComplete), name='PotionsGame.introSequence')
        self.outroSequence = Sequence(Wait(0.1), LerpColorScaleInterval(self.fadeIn, colorScale=(1,
                                                                                                 1,
                                                                                                 1,
                                                                                                 1), duration=1.5), Func(base.transitions.fadeOut, 0), Func(self.destroy), name='PotionsGame.outroSequence')
        self.completeSequence = Sequence(Wait(0.1), Func(self.resultsScreen.show), name='PotionsGame.completeSequence')
        self.failSequence = Sequence(Wait(0.1), Func(self.failScreen.show), name='PotionsGame.failSequence')
        self.restartSequence = Sequence(Func(self.resetScene), Wait(0.1), Func(self.resetRecipes), Func(self.recipePicker.updateList), Func(self.recipePicker.unstash), Func(self.onIntroComplete), name='PotionsGame.restartSequence')

    def resetRecipes(self):
        self.recipePicker.setEnabled(True)
        for recipe in self.recipes:
            recipe.reset()

    def selectRecipe(self, recipe):
        if self.gameFSM.state != 'RecipeSelect':
            return
        itemId = PotionGlobals.potionBuffIdToInventoryTypeId(recipe.potionID)
        inv = localAvatar.getInventory()
        if not inv:
            return
        quantity = inv.getItemQuantity(InventoryType.ItemTypeConsumable, itemId)
        limit = inv.getItemLimit(InventoryType.ItemTypeConsumable, itemId)
        if quantity >= limit:
            self.cleanUpConfirm()
            self.confirm = PiratesConfirm.PiratesConfirm(PLocalizer.PotionGui['MaxedOutTitle'], PLocalizer.PotionGui['MaxedOutText'], self.onSelectConfirmed)
            self.confirm.setPos(0.35, 0, -0.17)
            self.confirm.bOk['command'] = self.onSelectConfirmed
            self.confirm.bOk['extraArgs'] = [recipe]
            self.confirm.bNo['command'] = self.onSelectDeclined
            self.closeCurrentDialog = self.cleanUpConfirm
            self.gameBoard.disableInputEvents()
            self.disableButtons()
        else:
            self.gameFSM.request('StartGame', recipe)

    def onSelectDeclined(self):
        self.cleanUpConfirm()

    def onSelectConfirmed(self, recipe):
        self.cleanUpConfirm()
        self.enableButtons()
        self.closeCurrentDialog = None
        if self.gameFSM:
            self.gameFSM.request('StartGame', recipe)
        return

    def testRecipe(self):
        for column in self.gameBoard.boardPieces:
            for piece in column:
                if piece is not None:
                    for ingredient in self.currentRecipe.ingredients:
                        if ingredient.completed == False and piece.colorIndex == ingredient.colorIndex and piece.level == ingredient.level:
                            return True

        return False

    def showIngredientXP(self, ingredient):
        if not self.currentRecipe.complete:
            xpAmt = PotionGlobals.getPotionBuffXP(self.currentRecipe.potionID)
            if len(self.currentRecipe.ingredients) > 1:
                xpAmt = int(math.ceil(float(xpAmt) / (2.0 * float(len(self.currentRecipe.ingredients) - 1))))
            xpLabel = DirectLabel(parent=aspect2d, relief=None, text='+ ' + str(xpAmt) + ' ' + PLocalizer.PotionGui['XPLabel'], text_scale=PiratesGuiGlobals.TextScaleTitleMed, text_font=PiratesGlobals.getPirateOutlineFont(), text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=37, pos=(ingredient.getX(aspect2d) + 0.1, 0, ingredient.getZ(aspect2d) - 0.05), textMayChange=0)
            xpLabel.setTransparency(True)
            xpLabel.stash()
            return Sequence(Func(xpLabel.unstash), Parallel(LerpPosInterval(xpLabel, duration=1.5, pos=(ingredient.getX(aspect2d) + 0.1, 0.0, ingredient.getZ(aspect2d) + 0.1), blendType='easeOut'), LerpColorScaleInterval(xpLabel, duration=1.5, colorScale=(1,
                                                                                                                                                                                                                                                                1,
                                                                                                                                                                                                                                                                1,
                                                                                                                                                                                                                                                                0), blendType='easeIn')), Func(xpLabel.removeNode))
        else:
            return Wait(0.1)
        return

    def checkRecipe(self):
        self.ingredientsCompleted = 0
        if len(self.currentRecipe.ingredients) != 0:
            for column in self.gameBoard.boardPieces:
                for piece in column:
                    if piece is not None:
                        pieceUsed = False
                        for ingredient in self.currentRecipe.ingredients:
                            if ingredient.completed == False and piece.colorIndex == ingredient.colorIndex and piece.level == ingredient.level and not pieceUsed:
                                ingredient.completed = True
                                self.ingredientsCompleted += 1
                                self.gameBoard.boardPieces[piece.column][piece.row] = None
                                pieceUsed = True
                                self.currentRecipe.complete = True
                                for testingredient in self.currentRecipe.ingredients:
                                    if testingredient.completed == False:
                                        self.currentRecipe.complete = False

                                piece.wrtReparentTo(self.currentRecipe)
                                piece.setY(-5)
                                print 'adding animation for completed ingredient'
                                self.animationList.append(Sequence(piece.moveToBoardVerySlow(ingredient.column, ingredient.row), Func(ingredient.updateDisplay), Func(piece.removeNode), Func(self.gameBoard.kill, piece)))
                                self.postAnimationList.append(self.showIngredientXP(ingredient))

        return

    def destroy(self):
        self.ignoreAll()
        self.gameFSM.ignoreAll()
        self.ignore('seachestOpened')
        self.ignore('seachestClosed')
        if self.introSequence:
            self.introSequence.pause()
            self.introSequence = None
        if self.outroSequence:
            self.outroSequence.pause()
            self.outroSequence = None
        if self.completeSequence:
            self.completeSequence.pause()
            self.completeSequence = None
        if self.restartSequence:
            self.restartSequence.pause()
            self.restartSequence = None
        self.cleanUpConfirm()
        self.closeButton.destroy()
        del self.closeButton
        self.returnButton.destroy()
        del self.returnButton
        self.background.removeNode()
        del self.background
        self.buttonsBackground.removeNode()
        del self.buttonsBackground
        self.fadeIn.removeNode()
        del self.fadeIn
        self.xpBackground.removeNode()
        del self.xpBackground
        self.foregroundLayer.removeNode()
        del self.foregroundLayer
        self.foregroundTextureCard.removeNode()
        del self.foregroundTextureCard
        self.recipePicker.destroy()
        del self.recipePicker
        self.resultsScreen.destroy()
        self.resultsScreen = None
        self.failScreen.destroy()
        del self.failScreen
        self.infoScreen.destroy()
        del self.infoScreen
        self.hintScreen.destroy()
        del self.hintScreen
        self.gameBoard.destroy()
        del self.gameBoard
        base.musicMgr.stop(SoundGlobals.MUSIC_MINIGAME_POTION)
        self.dist.done()
        self.gameFSM.destroy()
        del self.gameFSM
        self.gameFSM = None
        for recipe in self.recipes:
            recipe.reset()
            recipe.destroy()

        del self.recipes
        return

    def updateResultsScreen(self):
        if self.resultsScreen:
            self.resultsScreen.show()