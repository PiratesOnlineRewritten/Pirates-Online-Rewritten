from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.inventory.InventoryUIGlobals import *

class InventoryRemoveConfirm(BorderFrame):

    def __init__(self, cell, manager):
        self.manager = manager
        textMessage = PLocalizer.InventoryRemoveDropTitle
        self.sizeX = 0.8
        self.sizeZ = 0.6
        textScale = PiratesGuiGlobals.TextScaleTitleSmall
        optiondefs = (('state', DGG.DISABLED, None), ('frameSize', (-0.0 * self.sizeX, 1.0 * self.sizeX, -0.0 * self.sizeZ, 1.0 * self.sizeZ), None), ('text', textMessage, None), ('text_align', TextNode.ACenter, None), ('text_font', PiratesGlobals.getPirateBoldOutlineFont(), None), ('text_fg', (1, 1, 1, 1), None), ('text_shadow', PiratesGuiGlobals.TextShadow, None), ('textMayChange', 1, None), ('text_scale', textScale, None), ('text_pos', (self.sizeX * 0.5, self.sizeZ * 0.9 - textScale), None))
        self.defineoptions({}, optiondefs)
        BorderFrame.__init__(self, parent=NodePath())
        self.initialiseoptions(InventoryRemoveConfirm)
        self.fromCell = cell
        self.setup()
        return

    def destroy(self):
        self.ignoreAll()
        BorderFrame.destroy(self)

    def setup(self):
        self.setBin('gui-fixed', 1)
        self.itemLabel = DirectLabel(parent=self, relief=None, text='%s' % self.fromCell.inventoryItem.getName(), text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, image=self.fromCell.inventoryItem['image'], image_color=(self.fromCell.inventoryItem.iconColor[0], self.fromCell.inventoryItem.iconColor[1], self.fromCell.inventoryItem.iconColor[2], self.fromCell.inventoryItem.iconColor[3]), image_scale=self.fromCell.inventoryItem['image_scale'], text_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0.066), pos=(self.sizeX * 0.5, 0.0, self.sizeZ * 0.5))
        Gui = loader.loadModel('models/gui/toplevel_gui')
        buttonImage = (Gui.find('**/generic_button'), Gui.find('**/generic_button_down'), Gui.find('**/generic_button_over'), Gui.find('**/generic_button_disabled'))
        confirmMessage = PLocalizer.InventoryRemoveDrop
        self.confirmButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=(0.22,
                                                                                                    1.0,
                                                                                                    0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=confirmMessage, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(self.sizeX * 0.25, 0, 0.1), command=self.manager.discardFromRemover)
        self.cancelButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=(0.22,
                                                                                                   1.0,
                                                                                                   0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.InventoryRemoveCancel, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(self.sizeX * 0.75, 0, 0.1), command=self.manager.closeRemover)
        generic_x = Gui.find('**/generic_x')
        generic_box = Gui.find('**/generic_box')
        generic_box_over = Gui.find('**/generic_box_over')
        self.closeButton = DirectButton(parent=self, relief=None, pos=(self.sizeX - 0.035, 0, self.sizeZ - 0.035), scale=0.28, geom=generic_x, image=(generic_box, generic_box, generic_box_over, generic_box), image_scale=0.7, text='', textMayChange=1, command=self.manager.closeRemover)
        return