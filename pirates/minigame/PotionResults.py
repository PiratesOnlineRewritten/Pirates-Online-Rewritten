from pirates.piratesgui.GuiPanel import *
from pirates.piratesgui.RequestButton import RequestButton
from pirates.piratesbase import PLocalizer
from pirates.inventory import ItemGlobals
import PotionGlobals
import math

class PotionResults(GuiPanel):

    def __init__(self, potionGame):
        self.potionGame = potionGame
        GuiPanel.__init__(self, '', 1.5, 1.0, showClose=False, titleSize=1.5)
        self.setPos((-0.75, 0, -0.4))
        self.bQuit = RequestButton(width=1.5, text=PLocalizer.PotionGui['StopButton'], command=self.quit)
        self.bQuit.reparentTo(self)
        self.bQuit.setPos(0.15, 0, 0.05)
        self.bQuit.setScale(1.2, 1.2, 1.2)
        self.bAgain = RequestButton(width=1.5, text=PLocalizer.PotionGui['PlayAgainButton'], command=self.playAgain)
        self.bAgain.reparentTo(self)
        self.bAgain.setPos(1.25, 0, 0.05)
        self.bAgain.setScale(1.2, 1.2, 1.2)
        self.titleText = PLocalizer.PotionGui['WinTitle']
        self.messageText = PLocalizer.PotionGui['WinText']
        self.Title = DirectLabel(parent=self, relief=None, text=self.titleText, text_scale=PiratesGuiGlobals.TextScaleTitleJumbo, text_font=PiratesGlobals.getPirateOutlineFont(), text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextLT14, pos=(0.75,
                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                0.83), textMayChange=0)
        self.message = DirectLabel(parent=self, relief=None, text=self.messageText, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=17, pos=(0.75,
                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                       0.72), textMayChange=0)
        self.potionName = None
        self.potionDesc = None
        self.potionXp = None
        self.potionImg = None
        return

    def destroy(self):
        self.bQuit.destroy()
        self.bAgain.destroy()
        GuiPanel.destroy(self)

    def show(self):
        if self.potionName is not None:
            self.potionName.removeNode()
        if self.potionDesc is not None:
            self.potionDesc.removeNode()
        if self.potionXp is not None:
            self.potionXp.removeNode()
        if self.potionImg is not None:
            self.potionImg.removeNode()
        self.potionName = DirectLabel(parent=self, relief=None, text=self.potionGame.currentRecipe.name, text_scale=PiratesGuiGlobals.TextScaleTitleMed, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=17, pos=(0.75,
                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                          0.65), textMayChange=0)
        self.potionDesc = DirectLabel(parent=self, relief=None, text=self.potionGame.currentRecipe.desc, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=34, pos=(0.75,
                                                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                                                            0.22), textMayChange=0)
        xpAmt = PotionGlobals.getPotionBuffXP(self.potionGame.currentRecipe.potionID)
        xpAmt = int(math.ceil(float(xpAmt) / 2.0))
        xpBonus = self.potionGame.dist.getXpBonus()
        labelTxt = '+ ' + str(xpAmt) + ' ' + PLocalizer.PotionGui['XPLabel']
        if xpBonus:
            xpAmt = xpAmt + xpBonus
            labelTxt = PLocalizer.PotionGui['XPLabelBonus'] % (str(xpAmt), str(xpBonus))
        self.potionXp = DirectLabel(parent=self, relief=None, text=labelTxt, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=17, pos=(0.75,
                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                0.29), textMayChange=0)
        asset = ItemGlobals.getIcon(PotionGlobals.potionBuffIdToInventoryTypeId(self.potionGame.currentRecipe.potionID))
        skillIcons = loader.loadModel('models/textureCards/skillIcons')
        geom = skillIcons.find('**/%s' % asset)
        if geom.isEmpty():
            geom = skillIcons.find('**/base')
        geom_scale = 0.24
        self.potionImg = DirectFrame(parent=self, geom=geom, geom_scale=geom_scale, pos=(0.75,
                                                                                         0,
                                                                                         0.5), image=None, relief=None)
        self.unstash()
        self.potionGame.closeCurrentDialog = self.cleanUp
        self.potionGame.disableButtons()
        skillIcons.removeNode()
        return

    def cleanUp(self):
        self.stash()
        self.potionGame.closeCurrentDialog = None
        self.potionGame.enableButtons()
        return

    def playAgain(self):
        if self.potionGame.gameFSM.getCurrentOrNextState() not in ['Anim', 'ChestOpened', 'ExitRequest', 'Exit', 'Eval']:
            self.cleanUp()
            self.potionGame.gameFSM.request('Reset')

    def quit(self):
        if self.potionGame.gameFSM.getCurrentOrNextState() not in ['Anim']:
            self.cleanUp()
            self.potionGame.gameFSM.request('Exit')