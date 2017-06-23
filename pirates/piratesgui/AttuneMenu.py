from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.battle.EnemySkills import *
from pirates.piratesgui.GuiPanel import GuiPanel
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.reputation import ReputationGlobals
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.pirate import AvatarTypes

class AvatarInfoButton(GuiButton):
    memberImageColor = (
     Vec4(0.31, 0.3, 0.3, 1), Vec4(0.41, 0.4, 0.4, 1), Vec4(0.41, 0.4, 0.4, 1), Vec4(0.21, 0.2, 0.2, 1))
    OnlineTextColor = (1, 1, 1, 1)
    WIDTH = 0.38
    HEIGHT = 0.035

    def __init__(self, owner, avId):
        self.owner = owner
        self.avId = avId
        self.hp = 0
        self.maxHp = 0
        GuiButton.__init__(self, text='', text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.025,
                                                                                                 0.085), text_align=TextNode.ALeft, text_fg=self.OnlineTextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, text_wordwrap=14, relief=None, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameColor=(0.45,
                                                                                                                                                                                                                                                                                                                        0.45,
                                                                                                                                                                                                                                                                                                                        0.35,
                                                                                                                                                                                                                                                                                                                        1.0), image_scale=(0.45,
                                                                                                                                                                                                                                                                                                                                           1,
                                                                                                                                                                                                                                                                                                                                           0.2), image_pos=(0.215,
                                                                                                                                                                                                                                                                                                                                                            0.0,
                                                                                                                                                                                                                                                                                                                                                            0.08), command=self.select)
        self.initialiseoptions(AvatarInfoButton)
        self.hpMeter = DirectWaitBar(parent=self, relief=DGG.RAISED, borderWidth=(0.004,
                                                                                  0.004), range=50, value=20, frameColor=(0.05,
                                                                                                                          0.35,
                                                                                                                          0.05,
                                                                                                                          1), barColor=(0.1,
                                                                                                                                        0.7,
                                                                                                                                        0.1,
                                                                                                                                        1), pos=(0.015,
                                                                                                                                                 0,
                                                                                                                                                 0.06), frameSize=(0,
                                                                                                                                                                   0.25,
                                                                                                                                                                   0,
                                                                                                                                                                   0.018), text='%s/%s' % (self.hp, self.maxHp), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleMicro, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.256,
                                                                                                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                                                                                                0.005), textMayChange=1)
        return

    def destroy(self):
        GuiButton.destroy(self)

    def updateItem(self, avatar):
        self.avatar = avatar
        if self.avatar:
            color = base.cr.battleMgr.getExperienceColor(base.localAvatar, avatar)
            try:
                avType = self.avatar.getAvatarType()
                if avType.isA(AvatarTypes.JollyRoger):
                    name = '%s\x02  %s\x01smallCaps\x01%s%s\x02\x02' % (avatar.getShortName(), color, PLocalizer.Lv, PLocalizer.InvasionLv)
                elif self.avatar.isInInvasion():
                    name = '%s' % avatar.getShortName()
                else:
                    name = '%s\x02  %s\x01smallCaps\x01%s%s\x02\x02' % (avatar.getShortName(), color, PLocalizer.Lv, avatar.level)
            except StandardError, e:
                self.notify.error('updateItem(%s, %s)' % (str(avatar), str(e)))

            self['text'] = name
            self.hp = avatar.hp
            self.maxHp = avatar.maxHp
            self.hpMeter['value'] = self.hp
            self.hpMeter['range'] = self.maxHp
            if self.avatar.getName() == 'Jolly Roger':
                self.hpMeter['text'] = ' ??/??'
            else:
                self.hpMeter['text'] = '%s/%s' % (self.hp, self.maxHp)
            if avatar.getTeam() == base.localAvatar.getTeam():
                self.setColorScale(Vec4(1, 1, 1, 1))
            else:
                self.setColorScale(Vec4(1.0, 0.7, 0.7, 1.0))
            self.hpMeter.show()
        else:
            self['text'] = PLocalizer.UnattuneAll
            self.setColorScale(Vec4(1, 1, 1, 1))
            self.hpMeter.hide()

    def select(self):
        self.owner.select(self.avId)


class AttuneMenu(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('AttuneMenu')
    WIDTH = 0.45
    HEIGHT = 0.09

    def __init__(self, parent=base.a2dRightCenter, command=None, draggable=0, **kw):
        optiondefs = (('relief', None, None), ('state', DGG.DISABLED, None), ('frameSize', (0, self.WIDTH, 0, self.HEIGHT), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, relief=None)
        self.initialiseoptions(AttuneMenu)
        titleFont = PiratesGuiGlobals.TextScaleMed
        textColor = PiratesGuiGlobals.TextFG1
        textShadow = PiratesGuiGlobals.TextShadow
        wordwrap = 13
        self.titleLabel = DirectLabel(parent=self, relief=None, pos=(0.05, 0, self.HEIGHT - PiratesGuiGlobals.TextScaleMed * 2.5), text=PLocalizer.UnattuneGui, text_align=TextNode.ALeft, text_scale=titleFont, text_pos=(0.015,
                                                                                                                                                                                                                           0.05), text_fg=textColor, text_shadow=textShadow, text_font=PiratesGlobals.getPirateOutlineFont(), textMayChange=1, text_wordwrap=wordwrap, sortOrder=21)
        self.buttons = {}
        self.updateButton(0)
        self.hide()
        return

    def updateButton(self, avId):
        av = base.cr.doId2do.get(avId)
        button = self.buttons.get(avId)
        if button:
            button.updateItem(av)
        else:
            button = AvatarInfoButton(self, avId)
            button.reparentTo(self)
            button.setPos(0.026, 0, self.HEIGHT * len(self.buttons) + 0.02)
            button.updateItem(av)
            self.buttons[avId] = button
            self.updateSize()

    def removeButton(self, avId):
        button = self.buttons.get(avId)
        if button:
            y = button.getZ()
            button.hide()
            del self.buttons[avId]
            button.destroy()
            for b in self.buttons.values():
                if b.getZ() > y:
                    b.setZ(b.getZ() - self.HEIGHT)

            self.updateSize()

    def updateSize(self):
        self['frameSize'] = (0, self.WIDTH, 0, self.HEIGHT * len(self.buttons) + 0.09)
        self.titleLabel.setZ(self.HEIGHT * len(self.buttons) + 0.02)

    def update(self):
        for avId in localAvatar.stickyTargets:
            self.updateButton(avId)
            self.buttons[avId].show()

        for avId in self.buttons.keys():
            if avId > 0 and localAvatar.stickyTargets.count(avId) < 1:
                self.removeButton(avId)

    def select(self, avId):
        if avId < 0:
            pass
        elif avId == 0:
            self.unattuneAll()
        else:
            localAvatar.sendRequestRemoveStickyTargets([avId])

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        for button in self.buttons.values():
            button.destroy()
            button = None

        self.buttons = {}
        DirectFrame.destroy(self)
        return

    def unattuneAll(self):
        localAvatar.sendRequestRemoveStickyTargets(self.buttons.keys())