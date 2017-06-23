from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import Freebooter
from pirates.piratesgui.GuiButton import GuiButton
import SkillButton
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.minigame import CannonDefenseGlobals

class AmmoSkillButton(SkillButton.SkillButton):

    def __init__(self, skillId, slotId, callback, quantity=0, skillRank=0, showQuantity=False, showHelp=False, showRing=False, hotkey=None, name='', showIcon=True, showLock=False, rechargeSkillId=False, assocAmmo=[]):
        if skillId in [InventoryType.DefenseCannonRoundShot, InventoryType.DefenseCannonEmpty]:
            showQuantity = False
        if not Freebooter.getPaidStatus(base.localAvatar.doId) and slotId >= CannonDefenseGlobals.FREEBOOTER_MAX_AMMO_SLOTS:
            showLock = True
        SkillButton.SkillButton.__init__(self, skillId, callback, quantity, skillRank, showQuantity, showHelp, showRing, hotkey, name, showIcon, showLock, rechargeSkillId, assocAmmo)
        self.toggleFrame['image_scale'] = 0.55
        self.toolTipBox = None
        self.slotId = slotId
        self._initButtons()
        self.updateSkillId(skillId)
        return

    def _initButtons(self):
        self.sellButtonModel = loader.loadModel('models/gui/pir_m_gui_can_buttonSell')
        self.sellButton = GuiButton(parent=self, image=(self.sellButtonModel.find('**/idle'), self.sellButtonModel.find('**/idle'), self.sellButtonModel.find('**/over')), image_scale=1, scale=0.4, sortOrder=100, pos=(0, 0, -0.125), command=self.onSellClick)
        self.sellButton.bind(DGG.ENTER, self.showToolTip)
        self.sellButton.bind(DGG.EXIT, self.hideToolTip)

    def updateSkillId(self, skillId):
        SkillButton.SkillButton.updateSkillId(self, skillId)
        if not hasattr(self, 'sellButton'):
            return
        if skillId == InventoryType.DefenseCannonEmpty:
            self.sellButton['state'] = DGG.DISABLED
            self.sellButton.hide()
            if skillId == InventoryType.DefenseCannonEmpty:
                self.setShowIcon(False)
        else:
            self.sellButton['state'] = DGG.NORMAL
            self.sellButton.show()
            self.setShowIcon(True)

    def createToolTip(self):
        if self.toolTipBox:
            return
        self.label = DirectLabel(parent=None, relief=None, text=PLocalizer.SellButton, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=12)
        height = -self.label.getHeight()
        width = self.label.getWidth()
        toolTipScale = 2.5
        self.toolTipBox = None
        self.toolTipBox = BorderFrame(parent=self.sellButton, frameSize=(-0.01, width, height, 0.05), scale=toolTipScale, pos=(-(width * toolTipScale * 0.5), 0, height * toolTipScale * 2.25), state=DGG.DISABLED)
        self.label.reparentTo(self.toolTipBox)
        return

    def showToolTip(self, event):
        self.createToolTip()

    def hideToolTip(self, event):
        if self.toolTipBox:
            self.toolTipBox.destroy()
            self.toolTipBox = None
        return

    def onSellClick(self):
        messenger.send('onSellClick', [self.skillId])