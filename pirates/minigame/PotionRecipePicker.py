import time
from direct.interval.IntervalGlobal import Sequence, Func
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from direct.actor import Actor
from direct.task import Task
from pandac.PandaModules import *
from pandac.PandaModules import CardMaker
from pirates.piratesgui.GuiPanel import *
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from pirates.quest.QuestTaskDNA import PotionsTaskDNA
import PotionGlobals

class PotionRecipePicker(DirectFrame):

    def __init__(self, potionGame):
        DirectFrame.__init__(self, parent=potionGame.background, relief=None)
        self.potionGame = potionGame
        self.enabled = True
        self.setupScene()
        return

    def setupScene(self):
        self.background = self.attachNewNode('background')
        guiAssets = loader.loadModel('models/minigames/pir_m_gui_pot_textureCard')
        parch = guiAssets.find('**/pir_t_gui_pot_scroll')
        parch.setTransparency(1, 1)
        parch.setScale(1.9, 1, 3.4)
        parch.setPos(0.5, 0, 0.0)
        parch.copyTo(self.background)
        self.title = DirectLabel(parent=self.background, relief=None, text=PLocalizer.PotionGui['RecipeList'], text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_fg=PotionGlobals.TextColor, text_wordwrap=30, pos=(0.57, 0, 0.77), textMayChange=0)
        self.recipeList = DirectScrolledList(parent=self, numItemsVisible=23, pos=(0.25, 0, -0.4), decButton_pos=(0.72, 0.0, 1.04), incButton_pos=(0.72, 0.0, -0.18), decButton_hpr=(0, 0.0, 0), incButton_hpr=(0, 0.0, 180), itemFrame_pos=(0, 0, 1.1), decButton_scale=0.07, decButton_image=(guiAssets.find('**/pir_t_gui_pot_scrollbutton'), guiAssets.find('**/pir_t_gui_pot_scrollbuttonOn'), guiAssets.find('**/pir_t_gui_pot_scrollbuttonOn'), guiAssets.find('**/pir_t_gui_pot_scrollbuttonDisable')), decButton_image_scale=(2.0, 2.0, 2.0), decButton_relief=None, incButton_scale=0.07, incButton_image=(guiAssets.find('**/pir_t_gui_pot_scrollbutton'), guiAssets.find('**/pir_t_gui_pot_scrollbuttonOn'), guiAssets.find('**/pir_t_gui_pot_scrollbuttonOn'), guiAssets.find('**/pir_t_gui_pot_scrollbuttonDisable')), incButton_image_scale=(2.0, 2.0, 2.0), incButton_relief=None, itemFrame_scale=1.0, forceHeight=0.0616)
        self.buttons = []
        self.inactiveButtons = []
        self.updateList()
        guiAssets.removeNode()
        return

    def updateList(self):
        self.recipeList.removeAndDestroyAllItems()
        self.buttons = []
        self.inactiveButtons = []
        playerLevel = self.potionGame.dist.getPlayerPotionLevel()
        notNew_list = self.potionGame.dist.getPlayerNotNewFlags()
        for recipe in self.potionGame.recipes:
            if playerLevel >= recipe.level:
                recipe.enabled = True
            else:
                recipe.enabled = False
            if recipe.enabled and recipe.potionID not in notNew_list:
                recipe.haveMade = False
            else:
                recipe.haveMade = True

        self.potionGame.recipes.sort()
        for recipe in self.potionGame.recipes:
            if recipe.questOnly and localAvatar.getInventory():

                class brewable(Exception):
                    pass

                try:
                    for currQuest in localAvatar.getInventory().getQuestList():
                        bonusComplete = currQuest.isComplete(bonus=True)
                        primaryComplete = currQuest.isComplete()
                        if not bonusComplete or not primaryComplete:
                            tasks = currQuest.getQuestDNA().getTaskDNAs()
                            for currTask in tasks:
                                if isinstance(currTask, PotionsTaskDNA) and (PotionGlobals.getPotionItemID(recipe.potionID) == currTask.potionType and not primaryComplete or PotionGlobals.getPotionItemID(recipe.potionID) == currTask.potionTypeBonus and not bonusComplete):
                                    raise brewable

                except brewable:
                    pass

                continue
            if recipe.level - playerLevel > 3 and not recipe.questOnly:
                continue
            buttonImage = None
            recipe.loadIngredients()
            buttonImageScale = 0.0
            text = recipe.name
            helptext = recipe.desc
            if not recipe.haveMade and len(recipe.ingredients) > 0:
                if recipe.questOnly:
                    iconText = PLocalizer.PotionGui['QuestLabel']
                    iconTextColor = PiratesGuiGlobals.TextFG13
                else:
                    iconText = PLocalizer.PotionGui['NewLabel']
                    iconTextColor = PiratesGuiGlobals.TextFG1
                guiAssets = loader.loadModel('models/minigames/pir_m_gui_pot_textureCard')
                buttonImage = guiAssets.find('**/pir_t_gui_pot_seal').copyTo(NodePath())
                buttonImageScale = 0.08
                buttonText = DirectLabel(parent=buttonImage, relief=None, text=iconText, text_scale=PiratesGuiGlobals.TextScaleLarge / buttonImageScale, text_font=PiratesGlobals.getPirateOutlineFont(), text_align=TextNode.ACenter, text_fg=iconTextColor, text_shadow=PiratesGuiGlobals.TextFG14, hpr=(0,
                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                           20), pos=(-0.25, 0, 0), textMayChange=0)
                guiAssets.removeNode()
            if Freebooter.getPaidStatus(localAvatar.doId) or recipe.isFree:
                cmd = self.potionGame.selectRecipe
                buttonGeom = None
                buttonGeomScale = 1
                buttonGeomPos = (0, 0, 0)
                args = None
            else:
                gui = loader.loadModel('models/gui/toplevel_gui')
                buttonGeom = gui.find('**/pir_t_gui_gen_key_subscriber')
                buttonGeomScale = 0.16
                buttonGeomPos = (-0.05, 0, 0.01)
                cmd = base.localAvatar.guiMgr.showNonPayer
                args = ['Restricted_Potion_Crafting_Recipe', 9]
                gui.removeNode()
            if recipe.enabled and recipe.available:
                button = GuiButton.GuiButton(text=(text, text, text, text), canReposition=True, text_wordwrap=0, image_scale=buttonImageScale, image_pos=(-0.04, 0.0, 0.01), image=(buttonImage, buttonImage, buttonImage, buttonImage), geom=buttonGeom, geom_scale=buttonGeomScale, geom_pos=buttonGeomPos, text0_fg=PotionGlobals.TextColor, text1_fg=PiratesGuiGlobals.TextFG0, text2_fg=PiratesGuiGlobals.TextFG15, text3_fg=PotionGlobals.TextColorDisabled, text_align=TextNode.ALeft, text_shadow=None, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, command=cmd, state=DGG.NORMAL, extraArgs=[recipe])
                button.bind(DGG.ENTER, recipe.showDetails)
                button.bind(DGG.EXIT, recipe.hideDetails)
                if button['image'][0]:
                    button['image_pos'] = (
                     button.getBounds()[1] + 0.075, 0, 0.01)
                self.buttons.append(button)
            else:
                button = GuiButton.GuiButton(text=(text, text, text, text), canReposition=True, text_wordwrap=0, image_scale=buttonImageScale, image_pos=(-0.04, 0.0, 0.01), image=(buttonImage, buttonImage, buttonImage, buttonImage), geom=buttonGeom, geom_scale=buttonGeomScale, geom_pos=buttonGeomPos, text0_fg=PotionGlobals.TextColorDisabled, text1_fg=PotionGlobals.TextColorDisabled, text2_fg=PotionGlobals.TextColorDisabled, text3_fg=PotionGlobals.TextColorDisabled, text_shadow=None, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_align=TextNode.ALeft, state=DGG.NORMAL, extraArgs=[recipe])
                button.bind(DGG.ENTER, recipe.showDetails)
                button.bind(DGG.EXIT, recipe.hideDetails)
                if button['image'][0]:
                    button['image_pos'] = (
                     button.getBounds()[1] + 0.075, 0, 0.01)
                self.inactiveButtons.append(button)
            self.recipeList.addItem(button)

        self.recipeList.refresh()
        self.lastIncButtonState = self.recipeList.incButton['state']
        self.lastDecButtonState = self.recipeList.decButton['state']
        self.recipeList.incButton['command'] = self.recipeList.scrollBy
        self.recipeList.incButton['extraArgs'] = [1]
        self.recipeList.decButton['command'] = self.recipeList.scrollBy
        self.recipeList.decButton['extraArgs'] = [-1]
        return

    def hide(self):
        for b in self.buttons:
            b.unbind(DGG.ENTER)
            b.unbind(DGG.EXIT)

        for b in self.inactiveButtons:
            b.unbind(DGG.ENTER)
            b.unbind(DGG.EXIT)

        self.stash()

    def setEnabled(self, enabled):
        if enabled != self.enabled:
            self.enabled = enabled
            if enabled:
                self.recipeList.incButton['state'] = self.lastIncButtonState
                self.recipeList.decButton['state'] = self.lastDecButtonState
                for button in self.buttons:
                    button['state'] = DGG.NORMAL

                for button in self.buttons + self.inactiveButtons:
                    button.bind(DGG.ENTER, button['extraArgs'][0].showDetails)
                    button.bind(DGG.EXIT, button['extraArgs'][0].hideDetails)

                self.accept('wheel_up', self.recipeList.scrollBy, [-1])
                self.accept('wheel_down', self.recipeList.scrollBy, [1])
            else:
                self.lastIncButtonState = self.recipeList.incButton['state']
                self.lastDecButtonState = self.recipeList.decButton['state']
                self.recipeList.incButton['state'] = DGG.DISABLED
                self.recipeList.decButton['state'] = DGG.DISABLED
                for button in self.buttons:
                    button['state'] = DGG.DISABLED

                for button in self.buttons + self.inactiveButtons:
                    button.unbind(DGG.ENTER)
                    button.unbind(DGG.EXIT)

                self.ignoreAll()

    def destroy(self):
        DirectFrame.destroy(self)
        self.ignoreAll()
        self.background.removeNode()
        del self.background
        for b in self.buttons:
            b.unbind(DGG.ENTER)
            b.unbind(DGG.EXIT)
            b.destroy()

        for b in self.inactiveButtons:
            b.unbind(DGG.ENTER)
            b.unbind(DGG.EXIT)
            b.destroy()

        del self.buttons