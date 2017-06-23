from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.inventory.InventoryUIGlobals import *
from pirates.piratesgui import GuiButton

class InventoryStackSeller(BorderFrame):

    def __init__(self, cell, parent):
        self.sizeX = 0.64
        self.sizeZ = 0.64
        textScale = PiratesGuiGlobals.TextScaleTitleSmall
        frameSize = (-0.0 * self.sizeX, 1.0 * self.sizeX, -0.0 * self.sizeZ, 1.0 * self.sizeZ)
        modelName = 'pir_m_gui_frm_subframe'
        imageColorScale = VBase4(0.75, 0.75, 0.9, 1.0)
        optiondefs = (
         (
          'state', DGG.DISABLED, None), ('frameSize', frameSize, None), ('modelName', modelName, None), ('imageColorScale', imageColorScale, None))
        self.defineoptions({}, optiondefs)
        BorderFrame.__init__(self, parent=NodePath())
        self.initialiseoptions(InventoryStackSeller)
        self.doubleFrame = BorderFrame(parent=self, frameSize=frameSize, modelName=modelName, imageColorScale=imageColorScale)
        self.tripleFrame = BorderFrame(parent=self, frameSize=frameSize, modelName=modelName, imageColorScale=imageColorScale, text=PLocalizer.InventorySplitterTitle, text_align=TextNode.ACenter, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=VBase4(1, 1, 1, 1), text_shadow=PiratesGuiGlobals.TextShadow, text_scale=textScale, text_pos=(self.sizeX * 0.5, self.sizeZ * 0.95 - textScale))
        self.fromCell = cell
        self.parent = parent
        self.amount = self.fromCell.inventoryItem.getAmount()
        self.setup()
        return

    def setup(self):
        self.setBin('gui-fixed', 1)
        self.itemLabel = DirectLabel(parent=self, relief=None, text='%s' % self.fromCell.inventoryItem.getName(), text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, image=self.fromCell.inventoryItem['image'], image_scale=self.fromCell.inventoryItem['image_scale'], text_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                            0.066), pos=(self.sizeX * 0.5, 0.0, self.sizeZ * 0.6))
        self.amountEntry = DirectEntry(parent=self, relief=DGG.GROOVE, scale=PiratesGuiGlobals.TextScaleExtraLarge, initialText='%s' % self.amount, width=1.5, numLines=1, focus=1, cursorKeys=1, frameColor=(1.0,
                                                                                                                                                                                                              1.0,
                                                                                                                                                                                                              1.0,
                                                                                                                                                                                                              0.2), entryFont=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=(1.0,
                                                                                                                                                                                                                                                                                  1.0,
                                                                                                                                                                                                                                                                                  1.0,
                                                                                                                                                                                                                                                                                  1.0), pos=(self.sizeX * 0.325, 0.0, self.sizeZ * 0.355), suppressKeys=1, suppressMouse=1, autoCapitalize=0, command=self.selectStackAmount)
        self.amountLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.InventorySellAmount % self.amount, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                               0.066), pos=(self.sizeX * 0.55, 0.0, self.sizeZ * 0.25))
        self.confirmButton = GuiButton.GuiButton(parent=self, text=PLocalizer.lOk, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.014), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image=GuiButton.GuiButton.blueGenericButton, image_scale=(0.6,
                                                                                                                                                                                                                                                                                                                            0.6,
                                                                                                                                                                                                                                                                                                                            0.6), pos=(self.sizeX * 0.25, 0, 0.1), relief=None, command=self.selectStackAmount)
        self.cancelButton = GuiButton.GuiButton(parent=self, text=PLocalizer.lCancel, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.014), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image=GuiButton.GuiButton.blueGenericButton, image_scale=(0.6,
                                                                                                                                                                                                                                                                                                                               0.6,
                                                                                                                                                                                                                                                                                                                               0.6), pos=(self.sizeX * 0.75, 0, 0.1), relief=None, command=self.cancelItem)
        return

    def destroy(self):
        self.parent = None
        self.fromCell = None
        self.doubleFrame.destroy()
        self.tripleFrame.destroy()
        BorderFrame.destroy(self)
        return

    def selectStackAmount(self, amount=None):
        if not amount:
            amount = self.amountEntry.get()
        if not amount or len(amount) == 0:
            base.localAvatar.guiMgr.createWarning(PLocalizer.InventorySellWarning, PiratesGuiGlobals.TextFG6)
            return
        try:
            amount = int(amount)
        except:
            base.localAvatar.guiMgr.createWarning(PLocalizer.InventorySellWarning, PiratesGuiGlobals.TextFG6)
            return

        if amount < 0 or amount > self.amount:
            base.localAvatar.guiMgr.createWarning(PLocalizer.InventorySellWarning, PiratesGuiGlobals.TextFG6)
            return
        if amount == 0:
            self.cancelItem()
            return
        else:
            self.parent.setStackAmount(self.fromCell, amount)
            self.destroy()

    def cancelItem(self):
        self.parent.cancelItem()
        self.destroy()