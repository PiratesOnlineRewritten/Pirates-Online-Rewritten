from MinigameFSM import MinigameFSM
from direct.interval.IntervalGlobal import Sequence, Func, Wait, Parallel
from direct.gui.DirectGui import *
from pirates.audio import SoundGlobals
from pirates.piratesgui import GuiManager
import time
import random

class PotionGameFSM(MinigameFSM):
    Sfxs = None

    def __init__(self, gameObject):
        self.gameObject = gameObject
        MinigameFSM.__init__(self, 'PotionGameFSM')
        self.defaultTransitions = {'Intro': ['Tutorial', 'RecipeSelect'],'RecipeSelect': ['Tutorial', 'StartGame', 'Reset', 'ExitRequest', 'Exit'],'Tutorial': ['Tutorial', 'RecipeSelect', 'Eval', 'Input', 'StartGame', 'SwitchRequest', 'ExitRequest', 'Reset', 'Exit'],'ChestOpened': ['RecipeSelect', 'Eval', 'Input', 'Anim', 'Tutorial', 'ExitRequest', 'SwitchRequest', 'Results', 'Exit'],'StartGame': ['Tutorial', 'Anim'],'Anim': ['Eval', 'Reset', 'Results'],'Eval': ['Results', 'Anim', 'Input', 'Tutorial', 'ExitRequest', 'SwitchRequest', 'Eval'],'Input': ['Tutorial', 'StartGame', 'ExitRequest', 'SwitchRequest', 'Results', 'Anim', 'Eval', 'Reset', 'Exit'],'Results': ['Reset', 'Exit', 'Tutorial', 'ExitRequest'],'Reset': ['Reset', 'RecipeSelect', 'Tutorial', 'ExitRequest', 'SwitchRequest'],'SwitchRequest': ['SwitchRequest', 'Reset', 'Eval', 'Tutorial', 'ExitRequest'],'ExitRequest': ['ExitRequest', 'Exit', 'Eval', 'RecipeSelect', 'Tutorial', 'SwitchRequest'],'Exit': []}
        if not self.Sfxs:
            PotionGameFSM.Sfxs = {'Lose': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_LOSE),'Win': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_WIN),'Fill': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FILL),'Wrong': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_WRONG),'NoDrop': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_CANTPLACE),'Flip': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FLIP),'Drop1': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_DROP),'Drop2': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_DROP_2),'SoftDrop1': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_DROP_SOFT),'SoftDrop2': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_DROP_SOFT_2),'Match': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_MATCH),'SoulMade': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_SOULMADE),'SoulMatch': SoundGlobals.loadSfx(SoundGlobals.SFX_MINIGAME_POTION_SOULMATCH)}
        self.matchMade = False
        self.ingredientMade = False
        self.gameStarted = False
        self.resultsShown = False
        self.animSeq = None
        if base.localAvatar.guiMgr.seaChestActive:
            base.localAvatar.guiMgr.hideSeaChest()
        return None

    def destroy(self):
        if self.animSeq:
            self.animSeq.pause()
            self.animSeq = None
        MinigameFSM.destroy(self)
        return

    def enterIntro(self):
        self.gameObject.introSequence.start()

    def exitIntro(self):
        self.gameObject.fadeIn.setColorScale(1, 1, 1, 0)
        self.gameObject.introSequence.clearToInitial()

    def enterTutorial(self):
        pass

    def exitTutorial(self):
        self.gameObject.infoScreen.stash()
        self.gameObject.hintScreen.stash()

    def enterRecipeSelect(self):
        self.gameObject.recipePicker.setEnabled(True)

    def exitRecipeSelect(self):
        self.gameObject.recipePicker.setEnabled(False)

    def enterStartGame(self, recipe):
        if not self.gameStarted:
            self.gameObject.recipePicker.hide()
            self.gameObject.currentRecipe = recipe
            self.gameObject.currentRecipe.showDetails()
            self.gameObject.returnButton.unstash()
            self.gameObject.gameBoard.addNewPiece()
            self.gameStarted = True
            self.resultsShown = False
        if self.gameObject.hintScreen.show('RecipeStart'):
            self.demand('Tutorial')
        else:
            self.demand('Anim')

    def exitStartGame(self):
        pass

    def enterInput(self):
        if self.gameObject.gameBoard.checkAvailableMoves():
            self.gameObject.gameBoard.enableInputEvents()
        else:
            base.playSfx(self.Sfxs['Lose'])
            self.demand('Results')

    def exitInput(self):
        self.gameObject.gameBoard.disableInputEvents()

    def playDrop(self):
        base.playSfx(random.choice([self.Sfxs['Drop1'], self.Sfxs['Drop2']]))

    def playSoftDrop(self):
        base.playSfx(random.choice([self.Sfxs['SoftDrop1'], self.Sfxs['SoftDrop2']]))

    def playFlip(self):
        base.playSfx(self.Sfxs['Flip'])

    def playMatch(self):
        base.playSfx(self.Sfxs['Match'])

    def playFill(self):
        base.playSfx(self.Sfxs['Fill'])

    def playSoulMade(self):
        base.playSfx(self.Sfxs['SoulMade'])

    def playSoulMatch(self):
        base.playSfx(self.Sfxs['SoulMatch'])

    def enterAnim(self):
        if self.gameObject.gameBoard.pieceNotDropped:
            self.gameObject.gameBoard.pieceNotDropped = False
            base.playSfx(self.Sfxs['NoDrop'])
        if len(self.gameObject.animationList) > 0:
            if self.gameObject.gameBoard.pieceDropped:
                self.gameObject.gameBoard.pieceDropped = False
                self.gameObject.animationList.append(Sequence(Wait(0.3), Func(self.playDrop)))
            if self.gameObject.gameBoard.delayDropped:
                self.gameObject.gameBoard.delayDropped = False
                self.gameObject.animationList.append(Sequence(Wait(0.8), Func(self.playSoftDrop)))
            if self.gameObject.gameBoard.pieceFlipped:
                self.gameObject.gameBoard.pieceFlipped = False
                base.playSfx(self.Sfxs['Flip'])
            if self.gameObject.gameBoard.experementMatched:
                self.gameObject.gameBoard.experementMatched = False
                base.playSfx(self.Sfxs['Fill'])
            if self.gameObject.gameBoard.experementFailed:
                self.gameObject.gameBoard.experementFailed = False
                base.playSfx(self.Sfxs['Wrong'])
            if self.gameObject.soulMade:
                self.gameObject.soulMade = False
                self.gameObject.animationList.append(Sequence(Wait(0.1), Func(self.playSoulMade)))
            if self.gameObject.soulMatch:
                self.gameObject.soulMatch = False
                self.gameObject.animationList.append(Sequence(Wait(0.1), Func(self.playSoulMatch)))
            if self.matchMade:
                self.matchMade = False
                self.gameObject.animationList.append(Sequence(Wait(0.1), Func(self.playMatch)))
            if self.ingredientMade:
                self.ingredientMade = False
                self.gameObject.animationList.append(Sequence(Wait(0.1), Func(self.playFill)))
            self.animSeq = Sequence(Parallel(*self.gameObject.animationList), Func(self.request, 'Eval'))
            self.animSeq.start()
        else:
            self.demand('Eval')

    def exitAnim(self):
        if len(self.gameObject.postAnimationList) > 0:
            self.animSeq = Parallel(*self.gameObject.postAnimationList)
            self.animSeq.start()
        self.gameObject.animationList = []
        self.gameObject.postAnimationList = []

    def enterEval(self):
        if self.gameObject.askToExit:
            self.gameObject.askToExit = False
            self.gameObject.confirmQuit()
        elif self.gameObject.askToReturn:
            self.gameObject.askToReturn = False
            self.gameObject.confirmReturn()
        elif self.gameObject.askForHint:
            self.gameObject.askForHint = False
            self.gameObject.hintScreen.showLastHint()
        elif self.gameObject.askForInfo:
            self.gameObject.askForInfo = False
            self.gameObject.infoScreen.show()
        elif len(self.gameObject.animationList) > 0:
            self.demand('Anim')
        else:
            self.gameObject.checkRecipe()
            if len(self.gameObject.animationList) > 0:
                self.ingredientMade = True
                knownRecipe = True
                for i in range(self.gameObject.ingredientsCompleted):
                    self.gameObject.dist.d_completeRecipe(self.gameObject.currentRecipe.potionID, knownRecipe)

                if self.gameObject.hintScreen.show('IngredientMatch'):
                    self.demand('Tutorial')
                else:
                    self.demand('Anim')
            elif self.gameObject.currentRecipe.complete:
                base.playSfx(self.Sfxs['Win'])
                self.demand('Results')
            else:
                self.gameObject.gameBoard.checkFall(False)
                if len(self.gameObject.animationList) > 0:
                    self.demand('Anim')
                else:
                    self.gameObject.gameBoard.findGroups()
                    if len(self.gameObject.animationList) > 0:
                        if not self.gameObject.soulMatch and not self.gameObject.soulMade:
                            self.matchMade = True
                        if self.gameObject.soulMade and self.gameObject.hintScreen.show('SoulMade') or self.gameObject.hintScreen.show('MatchMade'):
                            self.demand('Tutorial')
                        else:
                            self.demand('Anim')
                        self.gameObject.soulMade = False
                    elif not self.gameObject.gameBoard.playerPieceActive():
                        self.gameObject.gameBoard.addNewPiece()
                        self.demand('Anim')
                    else:
                        self.demand('Input')

    def exitEval(self):
        pass

    def enterExitRequest(self):
        pass

    def exitExitRequest(self):
        pass

    def enterSwitchRequest(self):
        pass

    def exitSwitchRequest(self):
        pass

    def enterResults(self):
        self.gameStarted = False
        if not self.resultsShown:
            self.resultsShown = True
            if self.gameObject.currentRecipe.complete:
                self.gameObject.completeSequence.start()
            else:
                if len(self.gameObject.currentRecipe.ingredients) == 0:
                    self.gameObject.dist.d_completeSurvival(self.gameObject.currentRecipe.ingredientsMade, self.gameObject.currentRecipe.tilesUsed)
                self.gameObject.failSequence.start()
            self.gameObject.returnButton.stash()

    def exitResults(self):
        pass

    def enterReset(self):
        self.gameStarted = False
        self.gameObject.infoScreen.stash()
        self.gameObject.hintScreen.stash()
        self.gameObject.gameBoard.disableInputEvents()
        self.gameObject.returnButton.stash()
        self.gameObject.restartSequence.start()
        self.gameObject.dist.d_reset()

    def exitReset(self):
        pass

    def enterExit(self):
        self.gameObject.outroSequence.start()

    def exitExit(self):
        pass