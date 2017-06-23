from pirates.piratesgui.GuiPanel import *
from pirates.piratesgui.RequestButton import RequestButton
from pirates.piratesbase import PLocalizer
import math

class PotionFail(GuiPanel):

    def __init__(self, potionGame):
        self.potionGame = potionGame
        GuiPanel.__init__(self, PLocalizer.PotionGui['FailTitle'], 1, 0.4, showClose=False, titleSize=1.5)
        self.setPos((-0.5, 0, 0))
        self.bQuit = RequestButton(width=2.0, text=PLocalizer.PotionGui['StopButton'], command=self.quit)
        self.bQuit.reparentTo(self)
        self.bQuit.setPos(0.25, 0, 0.05)
        self.bPlayAgain = RequestButton(width=2.0, text=PLocalizer.PotionGui['PlayAgainButton'], command=self.playAgain)
        self.bPlayAgain.reparentTo(self)
        self.bPlayAgain.setPos(0.65, 0, 0.05)
        self.message = None
        self.message2 = None
        self.message3 = None
        return

    def destroy(self):
        self.bQuit.destroy()
        self.bPlayAgain.destroy()
        GuiPanel.destroy(self)

    def show(self):
        if self.potionGame.closeCurrentDialog is not None:
            self.potionGame.closeCurrentDialog()
        if self.message is not None:
            self.message.removeNode()
        if self.message2 is not None:
            self.message2.removeNode()
        if self.message3 is not None:
            self.message3.removeNode()
        if len(self.potionGame.currentRecipe.ingredients) > 0:
            self.messageText = PLocalizer.PotionGui['FailText']
            self.message = DirectLabel(parent=self, relief=None, text=self.messageText, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=17, pos=(0.5,
                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                      0.25), textMayChange=0)
        else:
            self.messageText = PLocalizer.PotionGui['IngredientCount'] + ' : ' + str(self.potionGame.currentRecipe.ingredientsMade)
            self.message = DirectLabel(parent=self, relief=None, text=self.messageText, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=17, pos=(0.5,
                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                      0.28), textMayChange=0)
            effBonus = 0
            xpEarned = 0
            if self.potionGame.currentRecipe.tilesUsed > 0:
                effBonus = int(math.ceil(100.0 * float(self.potionGame.currentRecipe.ingredientsMade) / float(self.potionGame.currentRecipe.tilesUsed)))
                xpEarned = int(math.ceil(float(self.potionGame.currentRecipe.ingredientsMade) * float(self.potionGame.currentRecipe.ingredientsMade) / (10.0 * float(self.potionGame.currentRecipe.tilesUsed))))
            self.messageText2 = PLocalizer.PotionGui['Efficiency'] + ' : ' + str(effBonus) + '%'
            self.message2 = DirectLabel(parent=self, relief=None, text=self.messageText2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=17, pos=(0.5,
                                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                                        0.24), textMayChange=0)
            self.messageText3 = PLocalizer.PotionGui['XPEarned'] + ' : ' + str(xpEarned)
            self.message3 = DirectLabel(parent=self, relief=None, text=self.messageText3, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=17, pos=(0.5,
                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                             0.18), textMayChange=0)
        self.unstash()
        self.potionGame.closeCurrentDialog = self.cleanUp
        self.potionGame.disableButtons()
        return

    def cleanUp(self):
        self.stash()
        self.potionGame.closeCurrentDialog = None
        self.potionGame.enableButtons()
        return

    def playAgain(self):
        self.cleanUp()
        self.potionGame.gameFSM.request('Reset')

    def quit(self):
        self.cleanUp()
        self.potionGame.gameFSM.request('Exit')