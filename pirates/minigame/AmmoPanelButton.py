from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui import RadialMenu
from pirates.minigame import CannonDefenseGlobals

class AmmoPanelButton(DirectButton):
    SkillIcons = None

    def __init__(self, callback, skillId, skillRank):
        if not AmmoPanelButton.SkillIcons:
            AmmoPanelButton.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
            AmmoPanelButton.Image = (AmmoPanelButton.SkillIcons.find('**/base'), AmmoPanelButton.SkillIcons.find('**/base_down'), AmmoPanelButton.SkillIcons.find('**/base_over'))
        self.locked = True
        self.purchaseable = True
        self.cost = CannonDefenseGlobals.getDefenseCannonAmmoCost(skillId)
        self.amount = CannonDefenseGlobals.getDefenseCannonAmmoAmount(skillId)
        if self.amount == -1:
            self.amount = PLocalizer.Unlimited
        self.skillId = skillId
        self.skillRank = skillRank
        self.infoBox = None
        self.flashIval = None
        asset = RadialMenu.getSkillIconName(skillId, 0)
        geom = AmmoPanelButton.SkillIcons.find('**/%s' % asset)
        self.geom = geom
        if self.locked:
            asset = None
            geom = None
        DirectButton.__init__(self, relief=None, pos=(0, 0, 0), text='?', text_scale=0.1, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.005, -0.035), text_align=TextNode.ACenter, image=AmmoPanelButton.Image, image_scale=0.12, geom=geom, geom_scale=0.12, command=callback, textMayChange=1, sortOrder=70, extraArgs=[skillId])
        self.initialiseoptions(AmmoPanelButton)
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.lockIcon = gui.find('**/pir_t_gui_gen_key_subscriber')
        if not Freebooter.getPaidStatus(base.localAvatar.doId) and skillId > CannonDefenseGlobals.FREEBOOTER_LAST_AMMO_AVAILABLE:
            self.lock = DirectFrame(parent=self, relief=None, image=self.lockIcon, image_scale=0.14, image_pos=(0.05, 0, -0.025), sortOrder=99)
        self.bind(DGG.ENTER, self.showDetails)
        self.bind(DGG.EXIT, self.hideDetails)
        return

    def createTextBox(self):
        if self.infoBox:
            return
        globalPos = self.getPos(base.a2dLeftCenter)
        self.infoBox = None
        self.infoBox = BorderFrame(parent=base.a2dLeftCenter, frameSize=(-0.04, 0.5, -0.25, 0.05), pos=(globalPos.getX() + 0.12, 0, globalPos.getZ()), state=DGG.DISABLED)
        self.label = DirectLabel(parent=self.infoBox, relief=None, text=PLocalizer.CannonDefenseAmmoDesc % (PLocalizer.makeHeadingString(PLocalizer.InventoryTypeNames[self.skillId], 2), self.cost, self.amount, PLocalizer.CannonDefenseAmmoTypeDesc[self.skillId]), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=12, textMayChange=1)
        if self.locked:
            memberText = ''
            if self.skillId > CannonDefenseGlobals.FREEBOOTER_LAST_AMMO_AVAILABLE:
                memberText = PLocalizer.VR_AuthAccess
            self.label['text'] = PLocalizer.CannonDefenseAmmoUnlockedAt % (CannonDefenseGlobals.getLevelUnlockedAt(self.skillId), memberText)
        self.infoBox.setBin('gui-cannonDefense', 4)
        return

    def showDetails(self, event):
        self.createTextBox()

    def hideDetails(self, event):
        if self.infoBox:
            self.infoBox.destroy()
            self.infoBox = None
        return

    def isLocked(self):
        return self.locked

    def unlock(self):
        if self.locked:
            self['text'] = ''
            self['geom'] = self.geom
            self['geom_scale'] = 0.12
            self.locked = False

    def canPurchase(self, bankNotes):
        if not self.purchaseable:
            return False
        return bankNotes >= self.cost

    def enablePurchase(self):
        self.purchaseable = True
        self.setAlphaScale(1.0)

    def disablePurchase(self):
        self.purchaseable = False
        self.setAlphaScale(0.4)

    def flash(self):
        if self.flashIval:
            self.flashIval.pause()
        self.flashIval = Sequence(LerpColorInterval(self, 0.25, color=VBase4(0.7, 0.1, 0.1, 1.0), blendType='easeOut'), LerpColorInterval(self, 0.25, color=VBase4(1.0, 1.0, 1.0, 1.0), blendType='easeOut'))
        self.flashIval.start()