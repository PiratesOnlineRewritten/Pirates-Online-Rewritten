from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import StateData
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
import datetime
import time
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import TeleportConfirm
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPGlobals
from otp.friends.FriendInfo import FriendInfo
from pirates.piratesbase import Freebooter
from pirates.band import BandConstance
import GuiButton
from direct.showbase.DirectObject import *
import copy
MODE_FRIEND_AVATAR = 0
MODE_FRIEND_PLAYER = 1
MODE_FRIEND_PLAYER_AVATAR = 6
MODE_CREW = 2
MODE_GUILD = 3
MODE_CREW_HUD = 4
MODE_CREW_HUD_SEA = 5

class PirateMemberButton(GuiButton.GuiButton):
    memberImageColor = (
     Vec4(0.31, 0.3, 0.3, 1), Vec4(0.41, 0.4, 0.4, 1), Vec4(0.41, 0.4, 0.4, 1), Vec4(0.21, 0.2, 0.2, 1))
    OnlineTextColor = PiratesGuiGlobals.TextFG1
    OnlineButtonColor = VBase4(0.7, 0.7, 0.7, 1.0)
    OfflineButtonColor = VBase4(0.3, 0.3, 0.3, 1.0)
    OnlineSubtextColor = (0.8, 0.8, 0.8, 1)
    OfflineTextColor = (0.45, 0.45, 0.45, 1)
    OfflineIndicatorColor = (
     1.0, 0.1, 0.1, 1.0)
    GFXCARD = loader.loadModel('models/gui/ship_battle')
    TOPGUI = loader.loadModel('models/gui/toplevel_gui')
    ICON = loader.loadModel('models/gui/compass_main')
    HP_IMAGE = GFXCARD.find('**/ship_battle_speed_bar')
    SHIP_IMAGE = (
     TOPGUI.find('**/topgui_icon_ship'), TOPGUI.find('**/topgui_icon_ship'), TOPGUI.find('**/topgui_icon_ship'))
    ONLINE_ICON = ICON.find('**/icon_sphere')
    LocalTextColor = PiratesGuiGlobals.TextFG1

    def __init__(self, owner, avId, playerId, mode, modeInfo=None, name=None):
        self.avId = avId
        self.playerId = playerId
        self.avName = None
        self.mode = mode
        self.modeInfo = modeInfo
        self.owner = owner
        self.hp = 0
        self.maxHp = 0
        self.online = False
        self.hudOnline = True
        self.inPvp = False
        self.inParlorGame = False
        self.lastOnline = None
        self.potentialMember = False
        self.potentialName = name
        self.level = None
        self.reloadFrame = None
        if self.mode in [MODE_CREW, MODE_CREW_HUD, MODE_CREW_HUD_SEA]:
            if modeInfo:
                text = modeInfo.name
                self.avName = text
                self.hp = modeInfo.hp
                self.maxHp = modeInfo.maxHp
            elif name:
                text = name
                self.avName = text
                self.hp = 1
                self.maxHp = 1
                self.potentialMember = True
                self.potentialName = name
        if self.mode == MODE_CREW_HUD:
            GuiButton.GuiButton.__init__(self, parent=self.owner.memberFrame.getCanvas(), text='', text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.01, self.owner.memberOffset), text_align=TextNode.ALeft, text_fg=self.OfflineTextColor, text2_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, text_wordwrap=40, image_scale=(self.owner.memberWidth, 1.0, self.owner.memberHeight * 2.62), image_pos=(0.31, 0.0, self.owner.memberHeight * 0.5), command=self.handlePress)
            self.hpMeter = DirectWaitBar(parent=self, relief=DGG.RAISED, state=DGG.DISABLED, borderWidth=(0.001,
                                                                                                          0.001), range=self.maxHp, value=self.hp, frameColor=(0.05,
                                                                                                                                                               0.05,
                                                                                                                                                               0.05,
                                                                                                                                                               1), barColor=(0.1,
                                                                                                                                                                             0.7,
                                                                                                                                                                             0.1,
                                                                                                                                                                             1), pos=(0.13,
                                                                                                                                                                                      0,
                                                                                                                                                                                      0.012), frameSize=(0,
                                                                                                                                                                                                         0.3,
                                                                                                                                                                                                         0,
                                                                                                                                                                                                         0.013), text='', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleTiny, text_fg=PiratesGuiGlobals.TextFG3, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.15, -0.003, 0), textMayChange=1)
            self.hpBar = OnscreenImage(parent=self, image=self.HP_IMAGE, scale=(0.24,
                                                                                1.0,
                                                                                0.4), pos=(0.27,
                                                                                           0,
                                                                                           0.02))
            self.statusLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(1.53,
                                                                                                                                                                0.02), text_fg=self.OnlineSubtextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
            statusOffset = 0.35
            levelOffset = 0.46
            self.bind(DGG.ENTER, self.highlightOnMember)
            self.bind(DGG.EXIT, self.highlightOffMember)
            if self.potentialMember:
                self.hpMeter['text'] = PLocalizer.CrewHUDRequest
                self.hpMeter['text_fg'] = PiratesGuiGlobals.TextFG2
                self.hpMeter['barColor'] = PiratesGuiGlobals.TextFG0
        elif self.mode == MODE_CREW_HUD_SEA:
            GuiButton.GuiButton.__init__(self, parent=self.owner.memberFrame.getCanvas(), text='', text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.01, self.owner.memberOffset), text_align=TextNode.ALeft, text_fg=self.OfflineTextColor, text2_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, text_wordwrap=40, image_scale=(self.owner.memberWidth, 1.0, self.owner.memberHeight * 2.62), image_pos=(0.31, 0.0, self.owner.memberHeight * 0.5), command=self.handlePress)
            self.hpMeter = DirectWaitBar(parent=self, relief=DGG.RAISED, state=DGG.DISABLED, borderWidth=(0.001,
                                                                                                          0.001), range=self.maxHp, value=self.hp, frameColor=(0.05,
                                                                                                                                                               0.05,
                                                                                                                                                               0.05,
                                                                                                                                                               1), barColor=(0.1,
                                                                                                                                                                             0.7,
                                                                                                                                                                             0.1,
                                                                                                                                                                             1), pos=(0.137,
                                                                                                                                                                                      0,
                                                                                                                                                                                      0.015), frameSize=(0,
                                                                                                                                                                                                         0.286,
                                                                                                                                                                                                         0,
                                                                                                                                                                                                         0.013), text='', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleTiny, text_fg=PiratesGuiGlobals.TextFG3, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.143, -0.005, 0), textMayChange=1, scale=0.8)
            self.hpBar = OnscreenImage(parent=self, image=self.HP_IMAGE, scale=(0.184,
                                                                                1.0,
                                                                                0.4), pos=(0.243,
                                                                                           0,
                                                                                           0.02))
            self.statusLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(1.53,
                                                                                                                                                                0.02), text_fg=self.OnlineSubtextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, scale=0.8)
            statusOffset = 0.35
            levelOffset = 0.46
            self.bind(DGG.ENTER, self.highlightOnMember)
            self.bind(DGG.EXIT, self.highlightOffMember)
            if self.potentialMember:
                self.hpMeter['text'] = PLocalizer.CrewHUDRequest
                self.hpMeter['text0_fg'] = PiratesGuiGlobals.TextFG2
                self.hpMeter['barColor'] = PiratesGuiGlobals.TextFG0
        else:
            GuiButton.GuiButton.__init__(self, parent=self.owner.memberFrame.getCanvas(), text='', text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.03 - self.owner.memberWidth * 0.5, self.owner.memberOffset), text_align=TextNode.ALeft, text_fg=self.OfflineTextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, text_wordwrap=40, image_scale=(self.owner.memberWidth, 1.0, self.owner.memberHeight * 2.62), image_pos=(0.0, 0.0, self.owner.memberHeight * 0.5), command=self.handlePress)
            self.hpMeter = DirectWaitBar(parent=self, relief=DGG.RAISED, borderWidth=(0.004,
                                                                                      0.004), range=self.maxHp, value=self.hp, frameColor=(0.05,
                                                                                                                                           0.05,
                                                                                                                                           0.05,
                                                                                                                                           1), barColor=(0.1,
                                                                                                                                                         0.7,
                                                                                                                                                         0.1,
                                                                                                                                                         1), pos=(0.01,
                                                                                                                                                                  0,
                                                                                                                                                                  0.012), frameSize=(0,
                                                                                                                                                                                     0.25,
                                                                                                                                                                                     0,
                                                                                                                                                                                     0.02), text='%s/%s' % (self.hp, self.maxHp), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleTiny, text_fg=PiratesGuiGlobals.TextFG3, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.256,
                                                                                                                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                                                                                                                0.005), textMayChange=1)
            self.statusLabel = DirectLabel(parent=self, relief=None, pos=(0.0, 0, 0), text='', text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.03,
                                                                                                                                                                                 0.02), text_fg=self.OnlineSubtextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
            statusOffset = 0.35
            levelOffset = 0.46
        self.initialiseoptions(PirateMemberButton)
        self.hpMeter.hide()
        self.statusLabel.hide()
        self.shipIcon = DirectButton(parent=self, relief=None, image=self.SHIP_IMAGE, image0_color=VBase4(1.0, 1.0, 1.0, 1.0), image1_color=VBase4(0.4, 0.4, 0.4, 1.0), image2_color=VBase4(0.0, 0.9, 0.0, 1.0), image_scale=0.1, pos=(self.owner.memberWidth - statusOffset, 0, 0.035), command=self.handleShipPress)
        self.shipIcon.shipId = None
        self.shipIcon.hide()
        self.onlineIcon = self.ONLINE_ICON.copyTo(self)
        self.onlineIcon.setPos(self.owner.memberWidth - statusOffset, 0, 0.035)
        self.onlineIcon.setScale(0.2)
        self.onlineIcon.hide()
        self.offlineTimeLabel = DirectLabel(parent=self, pos=(self.owner.memberWidth - statusOffset, 0, 0.025), relief=None, text='', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.0,
                                                                                                                                                                                                                        0.0), text_fg=self.OfflineIndicatorColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
        self.offlineTimeLabel.show()
        self.levelLabel = DirectLabel(parent=self, pos=(self.owner.memberWidth - levelOffset, 0, 0.025), relief=None, text='22', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.0,
                                                                                                                                                                                                                   0.0), text_fg=self.OfflineIndicatorColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
        self.levelLabel.hide()
        self.accept('press-wheel_up-%s' % self.guiId, self.owner.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.guiId, self.owner.mouseWheelDown)
        self.update()
        return

    def destroy(self):
        self.command = None
        if self.mode in [MODE_FRIEND_AVATAR, MODE_FRIEND_PLAYER, MODE_FRIEND_PLAYER_AVATAR, MODE_GUILD]:
            if self.online:
                self.owner.onlineCount -= 1
        GuiButton.GuiButton.destroy(self)
        self.modeInfo = None
        self.ignoreAll()
        return

    def highlightOnMember(self, event):
        if self.reloadFrame:
            self.reloadFrame['image'] = self.TOPGUI.find('**/pir_t_gui_frm_base_circle_over')
        if not self.hudOnline or self.inPvp or self.inParlorGame or self.potentialMember:
            self.hpMeter['barColor'] = (0.5, 0.5, 0.5, 1)
        else:
            hpFraction = float(self.hpMeter['value']) / float(self.hpMeter['range'])
            if hpFraction >= 0.5:
                self.hpMeter['barColor'] = (0.4, 1.0, 0.4, 1)
            elif hpFraction >= 0.25:
                self.hpMeter['barColor'] = (1.0, 1.0, 0.6, 1)
            else:
                self.hpMeter['barColor'] = (1.0, 0.4, 0.4, 1)

    def highlightOffMember(self, event):
        if self.reloadFrame:
            self.reloadFrame['image'] = self.TOPGUI.find('**/pir_t_gui_frm_base_circle')
        if not self.hudOnline or self.inPvp or self.inParlorGame or self.potentialMember:
            self.hpMeter['barColor'] = PiratesGuiGlobals.TextFG0
        else:
            hpFraction = float(self.hpMeter['value']) / float(self.hpMeter['range'])
            if hpFraction >= 0.5:
                self.hpMeter['barColor'] = (0.1, 0.7, 0.1, 1)
            elif hpFraction >= 0.25:
                self.hpMeter['barColor'] = (1.0, 1.0, 0.1, 1)
            else:
                self.hpMeter['barColor'] = (1.0, 0.0, 0.0, 1)

    def updateGuild(self):
        if self.mode == MODE_GUILD:
            rank = localAvatar.getGuildRank()
            self.modeInfo = [self.modeInfo[0], self.modeInfo[1], rank, self.modeInfo[3]]
        self.update()

    def updateOnline(self, status):
        self.onlineIcon.show()
        if status:
            self.onlineIcon.setColor(0.1, 1.0, 0.1, 0.6)
        else:
            self.onlineIcon.setColor(0.6, 0.1, 0.1, 0.6)

    def updateHUDOnline(self, status):
        if status:
            self.hpMeter['text'] = ''
            self.hpMeter['text_fg'] = PiratesGuiGlobals.TextFG3
            self.hpMeter['barColor'] = (0.1, 0.7, 0.1, 1)
            text0_fg = self.OnlineTextColor
            self.hudOnline = True
        else:
            self.updateHp(self.maxHp, self.maxHp)
            self.hpMeter['text'] = PLocalizer.CrewHUDDisconnect
            self.hpMeter['text_fg'] = PiratesGuiGlobals.TextFG2
            self.hpMeter['barColor'] = PiratesGuiGlobals.TextFG0
            text0_fg = self.OfflineTextColor
            self.hudOnline = False
        self.update()

    def updatePVP(self, status):
        if status:
            self.updateHp(self.maxHp, self.maxHp)
            self.hpMeter['text'] = PLocalizer.CrewHUDPVP
            self.hpMeter['text_fg'] = PiratesGuiGlobals.TextFG2
            self.hpMeter['barColor'] = PiratesGuiGlobals.TextFG0
            self.inPvp = True
        else:
            self.hpMeter['text'] = ''
            self.hpMeter['text_fg'] = PiratesGuiGlobals.TextFG3
            self.hpMeter['barColor'] = (0.1, 0.7, 0.1, 1)
            self.inPvp = False
        self.update()

    def updateParlor(self, status):
        if status:
            self.updateHp(self.maxHp, self.maxHp)
            self.hpMeter['text'] = PLocalizer.CrewHUDParlor
            self.hpMeter['text_fg'] = PiratesGuiGlobals.TextFG2
            self.hpMeter['barColor'] = PiratesGuiGlobals.TextFG0
            self.inParlorGame = True
        else:
            self.hpMeter['text'] = ''
            self.hpMeter['text_fg'] = PiratesGuiGlobals.TextFG3
            self.hpMeter['barColor'] = (0.1, 0.7, 0.1, 1)
            self.inParlorGame = False
        self.update()

    def updateHp(self, hp, maxHp):
        if self.hudOnline and not self.inPvp and not self.inParlorGame:
            self.hp = hp
            self.maxHp = maxHp
            if self.mode != MODE_CREW_HUD and self.mode != MODE_CREW_HUD_SEA:
                self.hpMeter['text'] = '%s/%s' % (hp, maxHp)
            self.hpMeter['range'] = maxHp
            self.hpMeter['value'] = hp
            hpFraction = float(hp) / float(maxHp)
            if hpFraction >= 0.5:
                self.hpMeter['barColor'] = (0.1, 0.7, 0.1, 1)
            elif hpFraction >= 0.25:
                self.hpMeter['barColor'] = (1.0, 1.0, 0.1, 1)
            else:
                self.hpMeter['barColor'] = (1.0, 0.0, 0.0, 1)

    def updateName(self, name):
        self.modeInfo.name = name
        self.avName = name
        self.configure(text=name)

    def update(self, modeInfo=None):
        if modeInfo:
            self.modeInfo = modeInfo
        text = 'AV %s' % self.avId
        friendInfo = None
        statusText = 'status HC'
        online = False
        text_cap = 22
        state = DGG.NORMAL
        text0_fg = self.OnlineTextColor
        buttonColor = self.OnlineButtonColor
        statusTextFg = self.OnlineSubtextColor
        self.ignore('Guild Status Updated')
        if self.mode == MODE_FRIEND_AVATAR:
            friendInfo = base.cr.avatarFriendsManager.getFriendInfo(self.avId)
            text = friendInfo.getName()
            self.avName = text
            self.statusLabel.hide()
            self.shipIcon.setPos(self.owner.memberWidth - 0.4, 0, 0.035)
            shipId = base.cr.avatarFriendsManager.getShipId(self.avId)
            if shipId:
                self.shipIcon.shipId = shipId
                shipState = base.cr.avatarFriendsManager.getShipId2State(shipId)
                self.updateShip(shipId, shipState)
                text_cap = 18
            else:
                self.updateShip(None)
        elif self.mode == MODE_FRIEND_PLAYER:
            friendInfo = base.cr.playerFriendsManager.getFriendInfo(self.playerId)
            text = friendInfo.playerName
            self.avName = text
            self.statusLabel.hide()
            self.shipIcon.setPos(self.owner.memberWidth - 0.4, 0, 0.035)
            shipId = base.cr.playerFriendsManager.getShipId(self.playerId)
            if shipId:
                self.shipIcon.shipId = shipId
                shipState = base.cr.playerFriendsManager.getShipId2State(shipId)
                self.updateShip(shipId, shipState)
                text_cap = 18
            else:
                self.updateShip(None)
        else:
            if self.mode == MODE_FRIEND_PLAYER_AVATAR:
                friendInfo = base.cr.playerFriendsManager.getFriendInfo(self.playerId)
                text = (friendInfo.avatarName, friendInfo.avatarName, friendInfo.playerName, friendInfo.avatarName)
                self.avName = friendInfo.avatarName
                self.statusLabel.hide()
                self.shipIcon.setPos(self.owner.memberWidth - 0.4, 0, 0.035)
                shipId = base.cr.playerFriendsManager.getShipId(self.playerId)
                if shipId:
                    self.shipIcon.shipId = shipId
                    shipState = base.cr.playerFriendsManager.getShipId2State(shipId)
                    self.updateShip(shipId, shipState)
                    text_cap = 18
                else:
                    self.updateShip(None)
            else:
                if self.mode == MODE_CREW or self.mode == MODE_CREW_HUD or self.mode == MODE_CREW_HUD_SEA:
                    if not self.potentialMember:
                        text = self.modeInfo.name
                        self.updateHp(self.modeInfo.hp, self.modeInfo.maxHp)
                    else:
                        text = self.potentialName
                    self.avName = text
                    self.statusLabel.hide()
                    self.hpMeter.show()
                    self.shipIcon.setPos(0.395, 0, 0.04)
                    if not self.hudOnline:
                        text0_fg = self.OfflineTextColor
                    else:
                        text0_fg = self.OnlineTextColor
                else:
                    if self.mode == MODE_GUILD:
                        if base.cr.guildManager.id2Rank.has_key(self.avId):
                            self.modeInfo[2] = base.cr.guildManager.id2Rank.get(self.avId)
                        self.shipIcon.setPos(self.owner.memberWidth - 0.4, 0, 0.035)
                        if self.avId == localAvatar.doId:
                            self.accept('Guild Status Updated', self.updateGuild)
                        text = self.modeInfo[1]
                        statusText = self.getGuildRankName(self.modeInfo[2])
                    else:
                        return
                    if self.mode in [MODE_FRIEND_AVATAR, MODE_FRIEND_PLAYER, MODE_FRIEND_PLAYER_AVATAR, MODE_GUILD]:
                        if self.avId == localAvatar.doId:
                            online = True
                        else:
                            if friendInfo:
                                online = friendInfo.isOnline()
                            elif self.mode == MODE_GUILD:
                                online = self.modeInfo[3]
                            self.updateOnline(online)
                            if online:
                                text0_fg = self.OnlineTextColor
                                if self.mode == MODE_FRIEND_PLAYER_AVATAR:
                                    text0_fg = PiratesGuiGlobals.TextFG13
                                if not self.online:
                                    self.owner.onlineCount += 1
                                    messenger.send(self.owner.onlineChangeEvent)
                            else:
                                text0_fg = self.OfflineTextColor
                                buttonColor = self.OfflineButtonColor
                                self.updateShip(None)
                                if self.online:
                                    self.owner.onlineCount -= 1
                                    messenger.send(self.owner.onlineChangeEvent)
                        self.online = online
                    if len(text) > text_cap:
                        text = text[0:text_cap]
                if self.mode == MODE_GUILD:
                    self.statusLabel['text'] = statusText
                    self.statusLabel.show()
                    if self.avId == localAvatar.doId:
                        state = DGG.DISABLED
                        text0_fg = self.LocalTextColor
            if self.mode == MODE_CREW_HUD:
                self.configure(state=state, text=text, text0_fg=text0_fg, image_color=buttonColor, text_pos=(0.14,
                                                                                                             0.045,
                                                                                                             3.45))
            if self.mode == MODE_CREW_HUD_SEA:
                self.configure(state=state, text=text, text0_fg=text0_fg, image_color=buttonColor, text_pos=(0.15,
                                                                                                             0.04,
                                                                                                             1.5))
            self.configure(state=state, text=text, text0_fg=text0_fg, image_color=buttonColor)
        return

    def updateShip(self, shipId, shipHasSpace=0):
        if shipId:
            self.shipIcon.show()
        else:
            self.shipIcon.hide()

    def updateOnline(self, status):
        self.onlineIcon.show()
        if status:
            self.onlineIcon.setColor(0.1, 1.0, 0.1, 0.6)
            self.offlineTimeLabel['text'] = ''
        else:
            self.onlineIcon.setColor(0.6, 0.1, 0.1, 0.6)
            if self.lastOnline != None:
                timestamp = self.lastOnline
                now = datetime.datetime.utcnow()
                td = abs(now - datetime.datetime.fromtimestamp(timestamp))
                if td.days >= 1:
                    sortText = '%s' % td.days
                    self.offlineTimeLabel['text'] = sortText
                    self.offlineTimeLabel.show()
        return

    def updateOnlineTime(self, time):
        self.lastOnline = time
        self.update()

    def handleShipPress(self):
        TC = TeleportConfirm.TeleportConfirm(self.avId, self.avName)
        TC.setPos(-0.75, 0, -0.3)

    def handlePress(self):
        if self.mode == MODE_FRIEND_PLAYER:
            messenger.send(PiratesGlobals.PlayerDetailsEvent, [self.playerId])
        elif self.mode in (MODE_FRIEND_AVATAR, MODE_GUILD, MODE_CREW):
            messenger.send(PiratesGlobals.AvatarDetailsEvent, [self.avId, False])
        elif self.mode in (MODE_CREW_HUD, MODE_CREW_HUD_SEA):
            self.showProfile(self.avId, self.avName)
        elif self.mode == MODE_FRIEND_PLAYER_AVATAR:
            friendInfo = base.cr.playerFriendsManager.getFriendInfo(self.playerId)
            avId = friendInfo.avatarId
            messenger.send(PiratesGlobals.AvatarDetailsEvent, [avId, False])

    def showProfile(self, avId, avName):
        base.localAvatar.guiMgr.profilePage.showProfile(avId, avName)

    def getGuildRankName(self, rank):
        if rank == 3:
            statusText = PLocalizer.GuildRankLeader
        elif rank == 2:
            statusText = PLocalizer.GuildRankSubLead
        elif rank == 4:
            statusText = PLocalizer.GuildRankInviter
        else:
            statusText = PLocalizer.GuildRankMember
        return statusText

    def updateGuildRank(self, rank):
        self.statusLabel['text'] = self.getGuildRankName(rank)


class PirateMemberList(DirectObject):

    def __init__(self, numShown, parent, title=None, height=0.6, memberHeight=0.065, memberOffset=0.021, memberWidth=0.45, bottom=0, hud=False, width=0.48, sort=0):
        if hasattr(self, 'initialized'):
            self.arrangeMembers()
            return
        self.shown = numShown
        self.memberHeight = memberHeight
        self.memberWidth = memberWidth
        self.memberOffset = memberOffset
        self.title = title
        self.wantSortButtons = sort
        self.width = width
        self.bottom = bottom
        self.height = height
        self.hud = hud
        self.baseFrame = DirectFrame(relief=None, parent=parent)
        if self.hud:
            self.baseFrame['state'] = DGG.DISABLED
        self.members = []
        self.memberAvatarDict = {}
        self.memberPlayerDict = {}
        self.onlineCheckTaskName = base.cr.specialName('memberList_checkLastOnline')
        self.prearrangeTaskName = base.cr.specialName('memberList_prearrangeMembers')
        self.onlineChangeEvent = base.cr.specialName('memberList_onlineChange')
        self.setup()
        self.arrangeMembers()
        self.initialized = 1
        self.show()
        self.sortMode = 'Name'
        self.onlineDataProbe = DirectObject()
        self.onlineCount = 0
        return

    def mouseWheelUp(self, task=None):
        if len(self.members) > self.shown:
            amountScroll = self.shown / (1.0 * len(self.members))
            self.memberFrame.verticalScroll['value'] -= amountScroll

    def mouseWheelDown(self, task=None):
        if len(self.members) > self.shown:
            amountScroll = self.shown / (1.0 * len(self.members))
            self.memberFrame.verticalScroll['value'] += amountScroll

    def countMembers(self):
        return len(self.members)

    def show(self):
        self.baseFrame.show()
        self.accept('press-wheel_up-%s' % self.memberFrame.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.memberFrame.guiId, self.mouseWheelDown)
        self.accept('press-wheel_up-%s' % self.memberFrame.verticalScroll.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.memberFrame.verticalScroll.guiId, self.mouseWheelDown)
        self.accept('press-wheel_up-%s' % self.memberFrame.verticalScroll.thumb.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.memberFrame.verticalScroll.thumb.guiId, self.mouseWheelDown)
        self.accept('press-wheel_up-%s' % self.memberFrame.verticalScroll.incButton.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.memberFrame.verticalScroll.incButton.guiId, self.mouseWheelDown)
        self.accept('press-wheel_up-%s' % self.memberFrame.verticalScroll.decButton.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.memberFrame.verticalScroll.decButton.guiId, self.mouseWheelDown)
        self.accept('socailPanelWheelUp', self.mouseWheelUp)
        self.accept('socailPanelWheelDown', self.mouseWheelDown)

    def hide(self):
        self.baseFrame.hide()
        self.ignoreAll()

    def destroy(self):
        taskMgr.remove(self.onlineCheckTaskName)
        taskMgr.remove(self.prearrangeTaskName)
        self.onlineDataProbe.ignore(base.cr.statusDatabase.avatarDoneTaskName)
        self.ignoreAll()
        for member in self.members:
            member.detachNode()
            member.destroy()

        self.memberAvatarDict = {}
        self.memberPlayerDict = {}
        self.members = []
        self.baseFrame.destroy()

    def setPos(self, x, y, z):
        self.baseFrame.setPos(x, y, z)

    def setup(self):
        charGui = loader.loadModel('models/gui/char_gui')
        knob = (charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over'))
        self.memberFrame = DirectScrolledFrame(parent=self.baseFrame, relief=None, state=DGG.NORMAL, manageScrollBars=0, autoHideScrollBars=1, frameSize=(0, self.width, self.bottom, self.height), canvasSize=(0, self.width - 0.05, self.bottom + 0.025, self.height - 0.025), verticalScroll_relief=None, verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, self.bottom, self.height), verticalScroll_image=charGui.find('**/chargui_slider_small'), verticalScroll_image_scale=(self.height - self.bottom + 0.05, 1, 0.75), verticalScroll_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      90), verticalScroll_image_pos=(self.width - PiratesGuiGlobals.ScrollbarSize * 0.5 - 0.0, 0, (self.bottom + self.height) * 0.5), verticalScroll_image_color=(0.61,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  1), verticalScroll_thumb_image=knob, verticalScroll_thumb_relief=None, verticalScroll_thumb_image_scale=0.3, verticalScroll_resizeThumb=0, horizontalScroll_relief=None, sortOrder=5)
        if self.hud:
            self.memberFrame['state'] = DGG.DISABLED
        self.memberFrame.verticalScroll.incButton.destroy()
        self.memberFrame.verticalScroll.decButton.destroy()
        self.memberFrame.horizontalScroll.incButton.destroy()
        self.memberFrame.horizontalScroll.decButton.destroy()
        self.memberFrame.horizontalScroll.hide()
        self.memberFrame.show()
        charGui = loader.loadModel('models/gui/toplevel_gui')
        buttonImage = (charGui.find('**/generic_button'), charGui.find('**/generic_button_down'), charGui.find('**/generic_button_over'), charGui.find('**/generic_button_disabled'))
        if self.wantSortButtons:
            sortButtonWidth = self.memberWidth
            nameProp = 0.75
            nameSize = nameProp * sortButtonWidth
            onlineProp = 0.25
            onlineSize = onlineProp * sortButtonWidth
            levelSize = 0.0
            sortNameButton = DirectButton(parent=self.memberFrame, relief=None, image=buttonImage, image_scale=(nameSize, 1.0, 0.15), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text='Name', text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(nameSize * 0.5, 0, self.height + 0.04), command=self.sortByName)
            sortNameButton.show()
            sortOnlineButton = DirectButton(parent=self.memberFrame, relief=None, image=buttonImage, image_scale=(onlineSize, 1.0, 0.15), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text='Online', text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(onlineSize * 0.5 + nameSize + levelSize, 0, self.height + 0.04), command=self.sortByOnline)
            sortOnlineButton.show()
        charGui.removeNode()
        return

    def sortByName(self):
        self.sortMode = 'Name'
        self.arrangeMembers()

    def sortByOnline(self):
        self.sortMode = 'Online'
        self.arrangeMembers()

    def getMemberByAvId(self, avId):
        for member in self.members:
            if avId and member.avId == avId:
                return member

        return None

    def getMemberByPlayerId(self, playerId):
        for member in self.members:
            if playerId and member.playerId == playerId:
                return member

        return None

    def removeNotOnAvList(self, cullAvList):
        for member in self.members:
            if member.avId not in cullAvList:
                self.removeMember(member.avId, member.playerId, member.mode)

    def updateOrAddMember(self, avId, playerId, mode, modeInfo=None):
        tryAv = self.memberAvatarDict.get(avId)
        tryPlayer = self.memberPlayerDict.get(playerId)
        if tryAv and tryAv.isEmpty():
            if tryAv in self.members:
                self.members.remove(tryAv)
            tryAv = None
            del self.memberAvatarDict[avId]
        if tryPlayer and tryPlayer.isEmpty():
            if tryPlayer in self.members:
                self.members.remove(tryPlayer)
            tryPlayer = None
            del self.memberPlayerDict[playerId]
        if tryAv:
            if tryAv.mode == mode:
                self.updateMemberInfo(avId, playerId, mode, modeInfo)
            elif mode == MODE_FRIEND_AVATAR and tryAv.mode == MODE_FRIEND_PLAYER_AVATAR:
                self.addMember(avId, playerId, mode, modeInfo)
            elif mode == MODE_FRIEND_PLAYER_AVATAR and tryAv.mode == MODE_FRIEND_AVATAR:
                return
        elif tryPlayer and tryPlayer.mode == mode:
            self.updateMemberInfo(avId, playerId, mode, modeInfo)
        else:
            self.addMember(avId, playerId, mode, modeInfo)
        return

    def updateMemberInfo(self, avId, playerId, mode, modeInfo=None):
        tryAv = self.memberAvatarDict.get(avId)
        tryPlayer = self.memberPlayerDict.get(playerId)
        member = None
        if tryAv and tryAv.mode == mode:
            member = tryAv
        elif tryPlayer and tryPlayer.mode == mode:
            member = tryPlayer
        if member:
            member.update(modeInfo)
            self.prearrangeMembers()
        return

    def addMember(self, avId, playerId, mode, modeInfo=None, fromClearList=0):
        if mode == MODE_FRIEND_AVATAR:
            someMember = self.getMemberByPlayerId(playerId)
            if someMember:
                playerId = someMember.playerId
        if mode == MODE_FRIEND_PLAYER_AVATAR:
            avId = base.cr.playerFriendsManager.findAvIdFromPlayerId(playerId)
        if self.memberAvatarDict.get(avId) or self.memberPlayerDict.get(playerId):
            self.removeMember(avId, playerId, mode)
        texcolor = (0.9, 1, 0.9, 1)
        fcolor = PiratesGuiGlobals.ButtonColor5
        addMe = PirateMemberButton(self, avId, playerId, mode, modeInfo)
        self.members.append(addMe)
        if avId:
            self.memberAvatarDict[avId] = addMe
        if playerId:
            self.memberPlayerDict[playerId] = addMe
        if mode == MODE_GUILD and len(self.members) > 0:
            self.accept('guildMemberOnlineStatus', self.updateGuildMemberOnline)
        taskMgr.remove(self.onlineCheckTaskName)
        task = taskMgr.doMethodLater(1.0, self.requestLastOnlineTimes, self.onlineCheckTaskName)
        self.onlineDataProbe.ignore(base.cr.statusDatabase.avatarDoneTaskName)
        self.onlineDataProbe.accept(base.cr.statusDatabase.avatarDoneTaskName, self.updateOnlineData)
        self.prearrangeMembers()
        return addMe

    def addPotentialMember(self, avId, avName, mode):
        self.removeMember(avId, None, mode)
        texcolor = (0.9, 1, 0.9, 1)
        fcolor = PiratesGuiGlobals.ButtonColor5
        addMe = PirateMemberButton(self, avId, None, mode, name=avName)
        self.members.append(addMe)
        self.memberAvatarDict[avId] = addMe
        self.prearrangeMembers()
        if mode == MODE_GUILD and len(self.members) > 0:
            self.accept('guildMemberOnlineStatus', self.updateGuildMemberOnline)
        taskMgr.remove(self.onlineCheckTaskName)
        task = taskMgr.doMethodLater(1.0, self.requestLastOnlineTimes, self.onlineCheckTaskName)
        self.onlineDataProbe.ignore(base.cr.statusDatabase.avatarDoneTaskName)
        self.onlineDataProbe.accept(base.cr.statusDatabase.avatarDoneTaskName, self.updateOnlineData)
        return addMe

    def removeMember(self, avId, playerId, mode):
        removedAvId = None
        removedPlayerId = None
        if not playerId and avId:
            avMemeber = self.memberAvatarDict.get(avId)
            if avMemeber:
                playerId = avMemeber.playerId
        elif playerId and not avId:
            playerMemeber = self.memberPlayerDict.get(avId)
            if playerMemeber:
                avId = playerMemeber.playerId
        if avId:
            removeMe = self.memberAvatarDict.get(avId)
            removedAvId = avId
            if removeMe:
                removedPlayerId = removeMe.playerId
                if removeMe in self.members:
                    self.members.remove(removeMe)
                removeMe.detachNode()
                removeMe.destroy()
                del self.memberAvatarDict[avId]
        if playerId:
            removeMe = self.memberPlayerDict.get(playerId)
            removedPlayerId = playerId
            if removeMe:
                removedAvId = removeMe.avId
                if removeMe in self.members:
                    self.members.remove(removeMe)
                removeMe.detachNode()
                removeMe.destroy()
                del self.memberPlayerDict[playerId]
        if mode == MODE_GUILD and len(self.members) == 0:
            self.ignore('guildMemberOnlineStatus')
        self.prearrangeMembers()
        return (
         removedAvId, removedPlayerId)

    def removeMemberWithRefill(self, avId, playerId, mode):
        self.removeMember(avId, playerId, mode)
        if mode in (MODE_FRIEND_AVATAR, MODE_FRIEND_PLAYER_AVATAR):
            self.refillMember(avId, playerId, mode)

    def refillMember(self, avId, playerId, mode):
        if mode == MODE_FRIEND_AVATAR:
            if playerId and base.cr.playerFriendsManager.isFriend(playerId):
                info = base.cr.playerFriendsManager.getFriendInfo(playerId)
                self.updateOrAddMember(None, playerId, MODE_FRIEND_PLAYER_AVATAR, info)
        elif mode == MODE_FRIEND_PLAYER_AVATAR:
            if avId and base.cr.avatarFriendsManager.isFriend(avId):
                info = base.cr.avatarFriendsManager.getFriendInfo(avId)
                self.updateOrAddMember(avId, None, MODE_FRIEND_AVATAR, info)
        return

    def requestLastOnlineTimes(self, task):
        memberIds = []
        for member in self.members:
            if member.avId:
                memberIds.append(member.avId)

        base.cr.statusDatabase.queueOfflineAvatarStatus(memberIds)
        self.accept(base.cr.statusDatabase.avatarDoneTaskName, self.updateOnlineData)
        return task.done

    def updateOnlineData(self):
        for member in self.members:
            if member.avId:
                onlineTime = base.cr.statusDatabase.avatarData.get(member.avId)
                if onlineTime:
                    member.updateOnlineTime(onlineTime)

    def updateGuildMemberOnline(self, avId, onlineStatus):
        for member in self.members:
            if member.avId == avId:
                member.modeInfo[3] = onlineStatus
                member.update()

    def updateGuildMemberRank(self, avId, rank):
        for member in self.members:
            if member.avId == avId:
                member.updateGuildRank(rank)

    def updateAll(self):
        for member in self.members:
            member.update()

    def updateAv(self, avId):
        member = self.memberAvatarDict.get(avId)
        if member:
            member.update()

    def prearrangeMembers(self):
        taskMgr.remove(self.prearrangeTaskName)
        taskMgr.doMethodLater(0.1, self.arrangeMembers, self.prearrangeTaskName)

    def arrangeMembers(self, task=None):
        numMembers = len(self.members)
        if numMembers == 0:
            return
        self.members.sort(self.compareMembers)
        self.memberFrame['canvasSize'] = (
         0, 0.0, 0, numMembers * self.memberHeight)
        self.placement = self.memberHeight * numMembers
        for index in range(numMembers):
            self.placement -= self.memberHeight
            self.members[index].setPos(self.memberWidth * 0.5 - 0.0, 0, self.placement)

        self.updateAll()
        taskMgr.remove(self.prearrangeTaskName)
        if task:
            return task.done

    def getSize(self):
        return len(self.members)

    def clearMembers(self):
        for member in self.members:
            member.detachNode()
            member.destroy()

        self.members = []
        self.memberAvatarDict = {}
        self.memberPlayerDict = {}
        self.onlineCount = 0

    def compareMembers(self, first, other):
        if other is None:
            return -1
        if first.online and not other.online:
            return -1
        elif not first.online and other.online:
            return 1
        if first.mode == MODE_CREW or first.mode == MODE_CREW_HUD or first.mode == MODE_CREW_HUD_SEA:
            if not hasattr(other, 'modeInfo') or not other.modeInfo:
                return 1
            elif first.modeInfo:
                if first.modeInfo.isManager:
                    return -1
                elif other.modeInfo.isManager:
                    return 1
        if first.mode == MODE_GUILD:
            if not hasattr(other, 'modeInfo') or not other.modeInfo:
                return 1
            elif first.modeInfo:
                if first.modeInfo[2] in (2, 3) and other.modeInfo[2] == 4:
                    return -1
                elif first.modeInfo[2] == 4 and other.modeInfo[2] in (2, 3):
                    return 1
                elif first.modeInfo[2] > other.modeInfo[2]:
                    return -1
                elif first.modeInfo[2] < other.modeInfo[2]:
                    return 1
        if (first.mode == MODE_FRIEND_PLAYER or first.mode == MODE_FRIEND_PLAYER_AVATAR) and first.mode == MODE_FRIEND_AVATAR:
            return -1
        elif first.mode == MODE_FRIEND_AVATAR and (first.mode == MODE_FRIEND_PLAYER or first.mode == MODE_FRIEND_PLAYER_AVATAR):
            return 1
        elif self.sortMode == 'Online':
            if first.lastOnline == None:
                return 1
            elif other.lastOnline == None:
                return -1
            elif first.lastOnline > other.lastOnline:
                return -1
            return 1
        else:
            if first.mode == MODE_FRIEND_PLAYER_AVATAR:
                text1 = first['text'][0]
            else:
                text1 = first['text']
            if other.mode == MODE_FRIEND_PLAYER_AVATAR:
                text2 = other['text'][0]
            else:
                text2 = other['text']
            return cmp(text1.lower(), text2.lower())
        return