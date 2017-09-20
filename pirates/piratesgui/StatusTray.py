from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task import Task
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import RadialMenu
from pirates.piratesgui import GuiTray
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import StatusEffectsPanel
from pirates.battle.EnemySkills import *
from pirates.battle import EnemyGlobals
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.pvp import Beacon
from pirates.pvp import PVPGlobals
from pirates.pirate import AvatarTypes
import copy

class StatusTray(GuiTray.GuiTray):
    SHOW_SKILL_DURATION = 2.0

    def __init__(self, parent, showSkills=0, **kw):
        GuiTray.GuiTray.__init__(self, parent, 0.75, 0.15, **kw)
        self.initialiseoptions(StatusTray)
        self.name = ''
        self.sticky = False
        self.level = 0
        self.doId = 0
        self.prevDoId = 0
        self.hideValues = 0
        self.card = None
        self.prevChange = 0
        self.prevRange = 0
        self.prevValue = 0
        self.fader = None
        self.skillEffects = {}
        self.durationTask = None
        self.nameLabel = DirectLabel(parent=self, state=DGG.DISABLED, relief=None, text='', text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=Vec4(0.8, 0.7, 0.6, 1), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.04,
                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                    0.11), text_font=PiratesGlobals.getPirateBoldOutlineFont())
        self.stickyLabel = DirectLabel(parent=self, state=DGG.DISABLED, relief=None, text='', text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.57,
                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                          0.025), text_font=PiratesGlobals.getInterfaceOutlineFont())
        self.hpLabel = DirectLabel(parent=self, state=DGG.DISABLED, relief=None, frameColor=(0,
                                                                                             0,
                                                                                             0,
                                                                                             0.2), frameSize=(-0.01, 0.4, -0.015, 0.04), pos=(0.32,
                                                                                                                                              0,
                                                                                                                                              0.006), text=PLocalizer.StatusTrayHp, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceFont(), textMayChange=0)
        self.hpLabel.hide()
        self.voodooMeter = DirectWaitBar(parent=self, state=DGG.DISABLED, relief=DGG.RAISED, borderWidth=(0.005,
                                                                                                          0.005), frameSize=(0.0,
                                                                                                                             0.53,
                                                                                                                             0.007,
                                                                                                                             0.035), frameColor=(0,
                                                                                                                                                 0,
                                                                                                                                                 0,
                                                                                                                                                 1), pos=(0.2, 0, -0.055), range=100, value=100, barColor=(0.6,
                                                                                                                                                                                                           0.6,
                                                                                                                                                                                                           0.95,
                                                                                                                                                                                                           1), text='', text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.5, -0.035, 0), text_font=PiratesGlobals.getInterfaceFont(), textMayChange=1, sortOrder=0)
        self.voodooMeter.setTransparency(1)
        self.voodooMeter.component('text0').hide()
        self.hpMeter = DirectWaitBar(parent=self, state=DGG.DISABLED, relief=DGG.RAISED, borderWidth=(0.005,
                                                                                                      0.005), frameSize=(0.0,
                                                                                                                         0.53,
                                                                                                                         0.002,
                                                                                                                         0.03), frameColor=(0,
                                                                                                                                            0,
                                                                                                                                            0,
                                                                                                                                            1), pos=(0.2,
                                                                                                                                                     0,
                                                                                                                                                     0.05), range=100, value=100, barColor=(0.1,
                                                                                                                                                                                            0.7,
                                                                                                                                                                                            0.1,
                                                                                                                                                                                            1), text='', text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.5, -0.045, 0), text_font=PiratesGlobals.getInterfaceFont(), textMayChange=1, sortOrder=0)
        self.hpMeter.setTransparency(1)
        self.hpMeter.component('text0').hide()
        self.hpMeterChange = DirectFrame(parent=self, state=DGG.DISABLED, frameSize=(0.0,
                                                                                     0.53,
                                                                                     0.0,
                                                                                     0.026), frameColor=(1.0,
                                                                                                         0.0,
                                                                                                         0.0,
                                                                                                         1.0), pos=(0,
                                                                                                                    0,
                                                                                                                    0))
        self.hpMeterChange.setBin('gui-fixed', 0)
        self.hpMeterChange.hide()
        self.hpMeterDownIval = Sequence(Func(self.hpMeterChange.show), Wait(0.1), LerpColorInterval(self.hpMeterChange, 0.5, color=VBase4(0.7, 0.1, 0.1, 1.0), blendType='easeOut'), LerpColorInterval(self.hpMeterChange, 0.25, color=VBase4(0.0, 0.0, 0.0, 1.0), blendType='easeOut'), Func(self.hpMeterChange.hide))
        self.hpMeterUpGreenIval = Sequence(Func(self.hpMeterChange.show), Wait(0.1), LerpColorInterval(self.hpMeterChange, 0.75, color=VBase4(0.1, 0.7, 0.1, 1.0)), Func(self.hpMeterChange.hide))
        self.hpMeterUpRedIval = Sequence(Func(self.hpMeterChange.show), Wait(0.1), LerpColorInterval(self.hpMeterChange, 0.75, color=VBase4(1.0, 0.0, 0.0, 1.0)), Func(self.hpMeterChange.hide))
        self.hpMeterUpYellowIval = Sequence(Func(self.hpMeterChange.show), Wait(0.1), LerpColorInterval(self.hpMeterChange, 0.75, color=VBase4(1.0, 1.0, 0.1, 1.0)), Func(self.hpMeterChange.hide))
        self.meterChangeOffset = (0.0, 0.0, 0.05)
        self.prevTargetName = ''
        self.voodooLabel = DirectLabel(parent=self, state=DGG.DISABLED, relief=None, frameColor=(0,
                                                                                                 0,
                                                                                                 0,
                                                                                                 0.2), frameSize=(-0.01, 0.4, -0.015, 0.04), pos=(0.32, 0, -0.092), text=PLocalizer.StatusTrayVoodoo, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceFont(), textMayChange=0)
        self.voodooLabel.hide()
        self.statusEffectsPanel = StatusEffectsPanel.StatusEffectsPanel(parent=self)
        flagModel = loader.loadModel('models/gui/flag_icons')
        flagModel2 = loader.loadModel('models/gui/gui_icons_weapon')
        flagModels = [flagModel.find('**/flag_undead'), flagModel.find('**/flag_navy'), flagModel.find('**/flag_eitc'), flagModel2.find('**/pir_t_ico_dol_straw')]
        for icon in flagModels:
            if icon == flagModel2.find('**/pir_t_ico_dol_straw'):
                icon.setScale(0.1)
            else:
                icon.setScale(0.44)
            icon.flattenStrong()

        self.icons = {PiratesGlobals.UNDEAD_TEAM: flagModels[0],PiratesGlobals.NAVY_TEAM: flagModels[1],PiratesGlobals.TRADING_CO_TEAM: flagModels[2],PiratesGlobals.FRENCH_UNDEAD_TEAM: flagModels[0],PiratesGlobals.SPANISH_UNDEAD_TEAM: flagModels[0],PiratesGlobals.PLAYER_TEAM: flagModels[3],PiratesGlobals.VOODOO_ZOMBIE_TEAM: flagModels[0],PiratesGlobals.BOUNTY_HUNTER_TEAM: flagModels[0]}
        self.pvpIcon = Beacon.getBeaconModel()
        self.pvpIcon.setScale(0.12)
        self.pvpIcon.flattenStrong()
        privateerLogos = loader.loadModel('models/textureCards/sailLogo')
        self.privateerLogos = {PVPGlobals.FrenchTeam: privateerLogos.find('**/logo_french_flag'),PVPGlobals.SpanishTeam: privateerLogos.find('**/logo_spanish_flag')}
        for logo in self.privateerLogos.itervalues():
            logo.setScale(0.074)
            logo.flattenStrong()

        self.currentIcon = None
        if showSkills:
            self.card = loader.loadModel('models/textureCards/skillIcons')
            icons = loader.loadModel('models/gui/gui_icons_weapon')
            icons.reparentTo(self.card)
            self.reloadFrame = DirectFrame(parent=self, state=DGG.DISABLED, relief=None)
            self.reloadFrame.hide()
            self.activeName = DirectLabel(parent=self.reloadFrame, state=DGG.DISABLED, relief=None, text='Using Skill', text_align=TextNode.ARight, text_scale=0.06, pos=(-0.05, 0, 0.01), text_fg=PiratesGuiGlobals.TextFG11, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont())
            tex = self.card.find('**/base')
            self.reloadFrame['scale'] = 0.5
            self.reloadFrame['image'] = tex
            self.reloadFrame['image_scale'] = 0.085
            self.reloadFrame['image_pos'] = (0, 0, 0.02)
            self.reloadFrame.setPos(0.12, 0, -0.019)
            self.reloadFrame.setScale(0.7)
            tex = self.card.find('**/cutlass_sweep')
            self.skillFrame = DirectFrame(parent=self.reloadFrame, state=DGG.DISABLED, relief=None, sortOrder=20, image_pos=(0,
                                                                                                                             0,
                                                                                                                             0))
            self.skillFrame.setTransparency(1)
            self.skillFrame['image'] = tex
            self.skillFrame['image_scale'] = 0.1
            self.skillFrame['image_pos'] = (0, 0, 0.02)
            self.activeName['text_align'] = TextNode.ALeft
            self.activeName.setPos(0.09, 0, 0.01)

    def show(self):
        if not self.doId:
            return

        if base.cr.doId2do[self.doId].state != 'Spawn' and base.cr.doId2do[self.doId].state != 'Death' and base.cr.doId2do[self.doId].state != 'Waiting':
            GuiTray.GuiTray.show(self)

    def destroy(self):
        taskMgr.remove(self.taskName('updateStatusPanelTask'))
        taskMgr.remove('hideSkillTask')
        if self.card:
            self.card.removeNode()
            self.card = None

        self.hpMeterDownIval.pause()
        self.hpMeterUpGreenIval.pause()
        self.hpMeterUpRedIval.pause()
        self.hpMeterUpYellowIval.pause()
        del self.hpMeterDownIval
        del self.hpMeterUpGreenIval
        del self.hpMeterUpRedIval
        del self.hpMeterUpYellowIval
        self.statusEffectsPanel.destroy()
        del self.statusEffectsPanel
        for key in self.icons.keys():
            self.icons[key].removeNode()

        del self.icons
        GuiTray.GuiTray.destroy(self)

    def updateName(self, name, level, doId):
        self.name = name
        self.level = level
        self.prevDoId = self.doId
        self.doId = doId
        target = base.cr.doId2do.get(doId)
        if not target:
            return

        color = base.cr.battleMgr.getExperienceColor(base.localAvatar, target)
        avType = target.getAvatarType()
        if avType.isA(AvatarTypes.JollyRoger):
            color = '\x01red\x01'
            text = '%s  \x01smallCaps\x01%s%s%s\x02\x02' % (name, color, PLocalizer.Lv, PLocalizer.InvasionLv)
        elif target.isInInvasion():
            text = '%s' % self.name
        elif color:
            text = '%s  \x01smallCaps\x01%s%s%s\x02\x02' % (name, color, PLocalizer.Lv, self.level)
        else:
            text = '%s' % self.name

        self.nameLabel['text'] = text
        self.updateIcon(doId)

    def updateIcon(self, doId):
        target = base.cr.doId2do.get(doId)
        if not target:
            return

        if self.currentIcon:
            self.currentIcon.hide()

        pvpTeam = target.getPVPTeam()
        siegeTeam = target.getSiegeTeam()
        if pvpTeam:
            icon = self.pvpIcon
            self.pvpIcon.setColor(PVPGlobals.getTeamColor(pvpTeam))
        else:
            if siegeTeam:
                icon = self.privateerLogos[siegeTeam]
            else:
                icon = self.icons.get(target.getTeam(), None)
            if icon:
                icon.reparentTo(self.enemyFrame)
                icon.show()

        self.currentIcon = icon

    def updateSticky(self, bool):
        self.sticky = bool
        if self.sticky:
            self.stickyLabel['text'] = PLocalizer.Sticky
        else:
            self.stickyLabel['text'] = ''

    def updateHp(self, hp, maxHp, srcDoId=None):
        hp = max(0, hp)
        if localAvatar.gameFSM.getCurrentOrNextState() == 'Death':
            hp = 0

        if not maxHp:
            return

        if srcDoId != self.doId and srcDoId:
            return

        if self.doId != self.prevDoId and self.doId:
            self.prevDoId = self.doId
            hp = base.cr.doId2do[self.doId].getHp()
            maxHp = base.cr.doId2do[self.doId].getMaxHp()
            self.hpMeter['range'] = maxHp
            self.hpMeter['value'] = hp
            self.prevChange = 0
            self.prevRange = maxHp
            self.prevValue = hp
            hpFraction = float(hp) / float(maxHp)
            if hpFraction >= 0.5:
                barColor = (0.1, 0.7, 0.1, 1)
            else:
                if hpFraction >= 0.25:
                    barColor = (1.0, 1.0, 0.1, 1)
                else:
                    barColor = (1.0, 0.0, 0.0, 1)
                self.hpMeter['barColor'] = barColor
                if self.hpMeterDownIval.isPlaying():
                    self.hpMeterDownIval.finish()
                elif self.hpMeterUpGreenIval.isPlaying():
                    self.hpMeterUpGreenIval.finish()
                elif self.hpMeterUpRedIval.isPlaying():
                    self.hpMeterUpRedIval.finish()
                elif self.hpMeterUpYellowIval.isPlaying():
                    self.hpMeterUpYellowIval.finish()
            return

        hpFraction = float(hp) / float(maxHp)
        if hpFraction >= 0.5:
            barColor = (0.1, 0.7, 0.1, 1)
        else:
            if hpFraction >= 0.25:
                barColor = (1.0, 1.0, 0.1, 1)
            else:
                barColor = (1.0, 0.0, 0.0, 1)

        self.hpMeter['barColor'] = barColor
        self.hpMeter['range'] = maxHp
        self.hpMeter['value'] = hp
        if localAvatar.guiMgr.gameGui.hpModMeter:
            if not self.doId:
                localAvatar.guiMgr.gameGui.hpModMeter['value'] = hp
                localAvatar.guiMgr.gameGui.hpModMeter['barColor'] = barColor

        if not self.hideValues:
            if not self.doId:
                inv = localAvatar.getInventory()
                vtLevel = None
                if inv:
                    vtLevel = inv.getStackQuantity(InventoryType.Vitae_Level)
                if not vtLevel:
                    self.hpMeter['text'] = '%s/%s' % (hp, maxHp)
                else:
                    modHp = int(maxHp * 0.75)
                    self.hpMeter['text'] = '%s\x01Bred\x01/%s\x02' % (hp, modHp)
            else:
                self.hpMeter['text'] = '%s/%s' % (hp, maxHp)

        if self.hpMeterDownIval.isPlaying():
            currentTime = self.hpMeterDownIval.getT()
        else:
            currentTime = None

        if currentTime is not None:
            if currentTime < 0.5:
                self.prevValue = self.prevValue + self.prevChange
                if self.prevValue > maxHp:
                    self.prevValue = maxHp

        if self.prevValue > hp:
            self.hpMeterChange.setColor(1.0, 0.0, 0.0, 1.0)
            change = float(self.prevValue - hp)
            valueScale = float(hp) / float(maxHp)
            changeScale = float(change) / float(maxHp)
            frameSize = tuple(self.hpMeter['frameSize'])
            frameRight = float(changeScale * 0.52)
            frameBottom = float(frameSize[2] + 0.005)
            frameTop = float(frameSize[3] - 0.005)
            frameLeft = float(valueScale * 0.52)
            frameX = float(0.205 + frameLeft) - 0.001
            self.hpMeterChange.setPos(frameX + float(self.meterChangeOffset[0]), 0.0, float(self.meterChangeOffset[2]))
            self.hpMeterChange['frameSize'] = (0.0, frameRight, frameBottom, frameTop)
            if self.hpMeterUpGreenIval.isPlaying():
                self.hpMeterUpGreenIval.finish()

            if self.hpMeterUpRedIval.isPlaying():
                self.hpMeterUpRedIval.finish()

            if self.hpMeterUpYellowIval.isPlaying():
                self.hpMeterUpYellowIval.finish()

            self.prevChange = change
            self.prevRange = maxHp
            self.prevValue = hp
            if currentTime is None:
                self.hpMeterDownIval.start()
                return
            if currentTime >= 0.5:
                self.hpMeterDownIval.start()
            else:
                self.hpMeterDownIval.start(startT=currentTime)
        elif self.prevValue < hp:
            self.hpMeterChange.setColor(0.0, 0.0, 0.0, 1.0)
            change = float(hp - self.prevValue)
            valueScale = float(hp) / float(maxHp)
            changeScale = float(change) / float(maxHp)
            frameSize = tuple(self.hpMeter['frameSize'])
            frameRight = float(changeScale * 0.52)
            frameBottom = float(frameSize[2] + 0.005)
            frameTop = float(frameSize[3] - 0.005)
            frameLeft = float(valueScale * 0.52)
            frameX = float(0.205 + frameLeft) - frameRight
            self.hpMeterChange.setPos(frameX + float(self.meterChangeOffset[0]), 0.0, float(self.meterChangeOffset[2]))
            if frameLeft > 0.52:
                diff = frameLeft - 0.52
                frameRight = float(frameRight - diff)

            self.prevChange = change
            if self.hpMeterDownIval.isPlaying():
                self.hpMeterDownIval.finish()

            if self.hpMeterUpGreenIval.isPlaying():
                self.hpMeterUpGreenIval.finish()

            if self.hpMeterUpRedIval.isPlaying():
                self.hpMeterUpRedIval.finish()

            if self.hpMeterUpYellowIval.isPlaying():
                self.hpMeterUpYellowIval.finish()

            self.prevRange = maxHp
            self.prevValue = hp
            self.hpMeterChange['frameSize'] = (0.0, frameRight, frameBottom, frameTop)
            if hpFraction >= 0.5:
                self.hpMeterUpGreenIval.start()
            elif hpFraction >= 0.25:
                self.hpMeterUpYellowIval.start()
            else:
                self.hpMeterUpRedIval.start()

    def updateVoodoo(self, voodoo, maxVoodoo, srcDoId=None):
        self.voodooMeter['range'] = maxVoodoo
        self.voodooMeter['value'] = voodoo

        if srcDoId != self.doId:
            if localAvatar.guiMgr.gameGui.voodooModMeter:
                if not self.doId:
                    localAvatar.guiMgr.gameGui.voodooModMeter['value'] = voodoo

            if not self.hideValues:
                if not self.doId:
                    inv = localAvatar.getInventory()
                    vtLevel = None
                    if inv:
                        vtLevel = inv.getStackQuantity(InventoryType.Vitae_Level)

                    self.voodooMeter['text'] = str(vtLevel or ('%s/%s' % (voodoo, maxVoodoo)))
                else:
                    modVoodoo = int(maxVoodoo * 0.75)
                    self.voodooMeter['text'] = '%s\x01Bred\x01/%s\x02' % (voodoo, modVoodoo)
            else:
                self.voodooMeter['text'] = '%s/%s' % (voodoo, maxVoodoo)

    def updateLuck(self, luck, maxLuck):
        pass

    def updateSwiftness(self, swiftness, maxSwiftness):
        pass

    def fadeOut(self, *args, **kwargs):
        self.doId = 0
        GuiTray.GuiTray.fadeOut(self, *args, **kwargs)

    def hide(self, *args, **kwargs):
        self.removeDurationTask()
        self.doId = 0
        GuiTray.GuiTray.hide(self, *args, **kwargs)

    def updateStatusEffects(self, effects):
        effectIdList = effects.keys()
        for effectKeyId in effectIdList:
            effectId, attackerId, duration, timeLeft, ts, buffs = effects[effectKeyId]
            if effectKeyId not in self.skillEffects.keys() and effectId not in [WeaponGlobals.C_VOODOO_STUN, WeaponGlobals.C_VOODOO_HEX_STUN, WeaponGlobals.C_INTERRUPTED, WeaponGlobals.C_OPENFIRE, WeaponGlobals.C_TAKECOVER, WeaponGlobals.C_ATTUNE, WeaponGlobals.C_SPIRIT, WeaponGlobals.C_BANE, WeaponGlobals.C_MOJO, WeaponGlobals.C_WRECKHULL, WeaponGlobals.C_WRECKMASTS, WeaponGlobals.C_SINKHER, WeaponGlobals.C_INCOMING, WeaponGlobals.C_SUMMON_GHOST]:
                self.statusEffectsPanel.addStatusEffect(effectId, duration, timeLeft, ts, attackerId)
            else:
                self.statusEffectsPanel.updateStatusEffect(effectId, duration, timeLeft, ts, attackerId)

        for effectKeyId in self.skillEffects.keys():
            if effectKeyId not in effectIdList:
                buff = self.skillEffects.get(effectKeyId)
                if buff:
                    effectId = buff[0]
                    attackerId = buff[1]
                    self.statusEffectsPanel.removeStatusEffect(effectId, attackerId)

        self.skillEffects = copy.copy(effects)
        if self.skillEffects:
            self.addDurationTask()
        else:
            self.removeDurationTask()

    def addDurationTask(self):
        if not self.durationTask:
            self.durationTask = taskMgr.add(self.updateDurationTask, self.taskName('updateStatusPanelTask'))

    def removeDurationTask(self):
        if self.durationTask:
            taskMgr.remove(self.taskName('updateStatusPanelTask'))
            self.durationTask = None

    def updateDurationTask(self, task):
        if len(self.skillEffects) > 0:
            if self.statusEffectsPanel:
                self.statusEffectsPanel.updateDurations()
            return Task.cont
        else:
            self.durationTask = None
            return Task.done

    def updateSkill(self, skillInfo, srcDoId=None):
        if srcDoId != self.doId:
            return
        if skillInfo:
            self.showSkill(skillInfo[0], skillInfo[1], skillInfo[2])

    def showSkill(self, skillId, ammoSkillId=0, timestamp=0):
        if ammoSkillId and skillId != EnemySkills.PISTOL_RELOAD and skillId != EnemySkills.GRENADE_RELOAD:
            visSkillId = ammoSkillId
        else:
            visSkillId = skillId

        self.activeName['text'] = PLocalizer.InventoryTypeNames[visSkillId]
        asset = RadialMenu.getSkillIconName(visSkillId, 0)
        if self.card:
            tex = self.card.find('**/%s' % asset)
            self.skillFrame['image'] = tex
            self.skillFrame['image_scale'] = 0.075
            self.skillFrame.setPos(-0.105, 0, -0.255)

        ts = globalClockDelta.localElapsedTime(timestamp)
        delay = self.SHOW_SKILL_DURATION - ts
        if delay > 0:
            if self.fader:
                self.fader.finish()
            self.reloadFrame.show()
            self.reloadFrame.setAlphaScale(1.0)
            taskMgr.remove('hideSkillTask')
            taskMgr.doMethodLater(delay, self.hideSkill, 'hideSkillTask')

    def hideSkill(self, args=None):
        fadeOut = LerpFunctionInterval(self.reloadFrame.setAlphaScale, fromData=self.getColorScale()[3], toData=0, duration=0.5)
        self.fader = Sequence(fadeOut, Func(self.reloadFrame.hide))
        self.fader.start()
