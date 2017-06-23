from pirates.piratesgui.GuiPanel import *
from pirates.piratesgui import GuiButton
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory
from pirates.piratesgui import CheckButton

class XButton(GuiButton.GuiButton):

    def __init__(self, parent=None, close=True, **kw):
        optiondefs = ()
        self.defineoptions(kw, optiondefs)
        GuiButton.GuiButton.__init__(self, parent)
        self.initialiseoptions(XButton)
        mainGui = loader.loadModel('models/gui/gui_main')
        if close:
            glowscale = (0.4, 0.4, 0.4)
        else:
            glowscale = (0.6, 0.4, 0.4)
        self.glow = OnscreenImage(parent=self, image=mainGui.find('**/icon_glow'), scale=glowscale, color=(1.0,
                                                                                                           1.0,
                                                                                                           1.0,
                                                                                                           0.4))
        self.glow.hide()
        mainGui.removeNode()
        self.bind(DGG.ENTER, self.highlightOn)
        self.bind(DGG.EXIT, self.highlightOff)

    def highlightOn(self, event):
        self.glow.show()

    def highlightOff(self, event):
        self.glow.hide()


class IgnoreCheck(CheckButton.CheckButton):

    def __init__(self, parent=None, **kw):
        optiondefs = ()
        self.defineoptions(kw, optiondefs)
        CheckButton.CheckButton.__init__(self, parent)
        self.initialiseoptions(IgnoreCheck)
        mainGui = loader.loadModel('models/gui/gui_main')
        self.glow = OnscreenImage(parent=self, image=mainGui.find('**/icon_glow'), scale=0.33, color=(1.0,
                                                                                                      1.0,
                                                                                                      1.0,
                                                                                                      0.6))
        self.glow.hide()
        mainGui.removeNode()
        self.bind(DGG.ENTER, self.highlightOn)
        self.bind(DGG.EXIT, self.highlightOff)

    def setValue(self):
        CheckButton.CheckButton.setValue(self)
        self['geom_hpr'] = (0, 0, 45)
        self['geom_pos'] = (0.03, 0, 0.045)
        self['geom_scale'] = 0.6
        if hasattr(self, 'glow'):
            self.glow.hide()

    def highlightOn(self, event):
        self.glow.show()
        if not self['value']:
            self['geom'] = self['checkedGeom']
            self['geom_hpr'] = (0, 0, 45)
            self['geom_pos'] = (0.03, 0, 0.045)
            self['geom_scale'] = 0.6

    def highlightOff(self, event):
        self.glow.hide()
        if not self['value']:
            self['geom'] = None
        return


class PotionHint(DirectFrame):

    def __init__(self, potionGame):
        self.potionGame = potionGame
        topGui = loader.loadModel('models/gui/toplevel_gui')
        mainGui = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, parent=potionGame.dialogs, relief=None)
        self.glow = OnscreenImage(parent=self, image=mainGui.find('**/icon_glow'), color=(0.0,
                                                                                          0.0,
                                                                                          0.0,
                                                                                          1.0), scale=(12.0,
                                                                                                       1.0,
                                                                                                       8.0))
        parch = topGui.find('**/pir_t_gui_gen_parchment')
        parch.setScale(0.4725, 1.0, 0.6375)
        self.background = parch.copyTo(self)
        self.titleLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.PotionGui['HintTitle'], text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_fg=(0.6,
                                                                                                                                                                                                0.0,
                                                                                                                                                                                                0.0,
                                                                                                                                                                                                1.0), text_font=PiratesGlobals.getPirateOutlineFont(), text_wordwrap=24, textMayChange=0, pos=(0.0,
                                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                                               0.2))
        self.toggleLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.PotionGui['HintToggle'], text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG0, text_wordwrap=24, textMayChange=0, pos=(-0.2, 0, -0.13))
        self.bClose = XButton(parent=self, relief=None, pos=(0.42, 0, 0.24), image=topGui.find('**/pir_t_gui_gen_Xred'), image_scale=0.6, command=self.showNextMessage)
        self.bClose.stash()
        self.noHintsCheck = IgnoreCheck(parent=self, relief=None, image=topGui.find('**/pir_t_gui_gen_box_empty'), image_scale=0.75, checkedGeom=topGui.find('**/pir_t_gui_gen_Check_Red'), pos=(-0.25, 0, -0.12), command=self.noHintsCheckCB)
        self.bAccept = XButton(text=PLocalizer.PotionGui['HintAccept'], image=(None,
                                                                               None,
                                                                               None,
                                                                               None), text0_fg=PiratesGuiGlobals.TextFG23, text1_fg=PiratesGuiGlobals.TextFG23, text2_fg=PiratesGuiGlobals.TextFG23, text3_fg=PiratesGuiGlobals.TextFG9, text_pos=(0.03, 0, -0.02), text_font=PiratesGlobals.getPirateOutlineFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ARight, close=False, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, command=self.showNextMessage)
        self.bAccept.reparentTo(self)
        self.bAccept.setPos(0.42, 0, 0.22)
        self.bAccept.stash()
        self.message = None
        self.showHints = True
        self.lastHint = None
        self.messageQueue = []
        inv = localAvatar.getInventory()
        if inv.getStackQuantity(InventoryType.PotionCraftingInstructionsToken) > 0:
            self.showHints = False
        self.hintCB = self.showHints
        self.noHintsCheck['value'] = self.hintCB
        self.hintShown = {}
        for hintKey in PLocalizer.PotionHints.keys():
            self.hintShown[hintKey] = False

        topGui.removeNode()
        mainGui.removeNode()
        return

    def destroy(self):
        self.bAccept.destroy()
        self.bClose.destroy()
        self.noHintsCheck.destroy()
        DirectFrame.destroy(self)

    def noHintsCheckCB(self, val):
        self.hintCB = val
        if self.hintCB and len(self.messageQueue) > 0:
            self.bAccept.unstash()
            self.bClose.stash()
        else:
            self.bAccept.stash()
            self.bClose.unstash()

    def setHintsEnabled(self, hintsOn):
        self.showHints = hintsOn
        for hintKey in PLocalizer.PotionHints.keys():
            self.hintShown[hintKey] = not hintsOn

        self.potionGame.dist.d_setHintsActive(hintsOn)
        self.hintCB = self.showHints
        self.noHintsCheck['value'] = self.hintCB

    def showLastHint(self):
        self.setHintsEnabled(True)
        if self.lastHint is not None and len(self.messageQueue) == 0:
            if self.show(self.lastHint):
                self.hintShown[self.lastHint] = False
                self.potionGame.gameFSM.demand('Tutorial')
        return

    def showNextMessage(self):
        if len(self.messageQueue) > 0 and self.hintCB:
            if self.message is not None:
                self.message.removeNode()
            self.messageText = self.messageQueue.pop()
            self.message = DirectLabel(parent=self, relief=None, text=self.messageText, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG0, text_shadow=None, text_wordwrap=32, pos=(0.02,
                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                              0.1), textMayChange=0)
            if len(self.messageQueue) > 0:
                self.bAccept.unstash()
                self.bClose.stash()
            else:
                self.bAccept.stash()
                self.bClose.unstash()
        elif self.hintCB:
            self.accept()
        else:
            self.dismiss()
        return

    def forceShow(self, hintKey, forced=True):
        self.hintShown[hintKey] = True
        self.messageQueue.reverse()
        self.messageQueue.extend(PLocalizer.PotionHints[hintKey])
        self.messageQueue.reverse()
        if forced:
            self.noHintsCheck.stash()
        else:
            self.noHintsCheck.unstash()
        self.showNextMessage()
        self.unstash()
        self.potionGame.closeCurrentDialog = self.cleanUp
        self.potionGame.disableButtons()

    def show(self, hintKey):
        self.lastHint = hintKey
        if self.showHints and not self.hintShown[hintKey]:
            if self.potionGame.closeCurrentDialog is not None:
                self.potionGame.closeCurrentDialog()
            self.forceShow(hintKey, False)
            return True
        else:
            return False
        return

    def toggle(self):
        if self.isStashed():
            self.showLastHint()
        else:
            self.showNextMessage()

    def dismiss(self):
        self.setHintsEnabled(False)
        self.accept()

    def cleanUp(self):
        while len(self.messageQueue) > 0:
            self.messageQueue.pop()

        self.stash()
        self.potionGame.closeCurrentDialog = None
        self.potionGame.enableButtons()
        return

    def accept(self):
        self.cleanUp()
        if self.potionGame.gameFSM.gameStarted:
            self.potionGame.gameFSM.demand('Eval')
        else:
            self.potionGame.gameFSM.demand('RecipeSelect')