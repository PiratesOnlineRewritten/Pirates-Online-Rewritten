from direct.gui.DirectGui import DirectFrame, DirectButton, DGG, OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report, Functor
from otp.otpgui import OTPDialog
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesbase import PLocalizer
from pirates.minigame import PlayingCardGlobals
from pirates.piratesbase import CollectionMap
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.reputation import ReputationGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class StackMessage(BorderFrame):
    guiLoaded = False
    corner = None
    popupSfx = None
    lootSfx = None
    CoinTex = None
    CrateTex = None
    ChestTex = None
    RoyalChestTex = None
    SkillIcons = None
    WeaponIcons = None
    TreasureGui = None
    QuestTex = None
    WeaponTex = None
    AdminTex = None
    HatTex = None
    TattooTex = None
    CircleTex = None

    def __init__(self, parent=None, **kwargs):
        self.loadModels()
        self.cornerGeom = None
        self.text = None
        self.circle = None
        self.icon = None
        self.icon2 = None
        if not StackMessage.popupSfx:
            StackMessage.popupSfx = loadSfx(SoundGlobals.SFX_GUI_STACK_POPUP)
            StackMessage.lootSfx = loadSfx(SoundGlobals.SFX_GUI_LOOT)
            StackMessage.lootSfx.setVolume(0.75)
        optiondefs = (
         ('relief', None, None), ('frameSize', (0, 0.8, -0.18, 0), None), ('state', DGG.DISABLED, None), ('time', 7, None), ('priority', 0, None), ('modelName', 'general_frame_b', None), ('borderScale', 0.7, None), ('icon', (), self.setIcon), ('buttonStyle', None, None), ('noCallback', None, None), ('yesCallback', None, None), ('cancelCallback', None, None))
        self.defineoptions(kwargs, optiondefs, dynamicGroups=())
        BorderFrame.__init__(self, parent, **kwargs)
        self.initialiseoptions(StackMessage)
        self.ival = None
        self.cornerGeom = self.corner.copyTo(self)
        self.cornerGeom.setScale(0.4)
        self.cornerGeom.setPos(0.068, 0, -0.066)
        self.cornerGeom.setColorScale(*PiratesGuiGlobals.TextFG1)
        self.setTransparency(True)
        return

    def __cmp__(self, other):
        if other:
            return cmp(other['priority'], self['priority'])
        else:
            return -1

    def __hash__(self):
        return id(self)

    def destroy(self, autoDestroy=1):
        if self.ival:
            self.ival.pause()
            self.ival = None
        if autoDestroy:
            BorderFrame.destroy(self)
        return

    def loadModels(self):
        if StackMessage.guiLoaded:
            return
        StackMessage.TopLevel = gui = loader.loadModel('models/gui/toplevel_gui')
        StackMessage.corner = gui.find('**/topgui_general_corner')
        StackMessage.CoinTex = gui.find('**/treasure_w_coin*')
        StackMessage.SkillTex = gui.find('**/topgui_icon_skills')
        StackMessage.QuestTex = gui.find('**/topgui_icon_journal')
        StackMessage.WeaponTex = gui.find('**/topgui_icon_weapons')
        StackMessage.LookoutTex = gui.find('**/telescope_button')
        StackMessage.ShipTex = gui.find('**/topgui_icon_ship')
        StackMessage.CircleTex = gui.find('**/pir_t_gui_frm_base_circle')
        StackMessage.CrateTex = gui.find('**/icon_crate*')
        card = loader.loadModel('models/textureCards/icons')
        StackMessage.ChestTex = card.find('**/icon_chest*')
        StackMessage.RoyalChestTex = card.find('**/topgui_icon_ship_chest03*')
        StackMessage.HatTex = card.find('**/icon_bandana')
        StackMessage.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
        StackMessage.PorkChunkTex = StackMessage.SkillIcons.find('**/pir_t_ico_pot_porkTonic')
        StackMessage.TreasureGui = loader.loadModel('models/gui/treasure_gui')
        StackMessage.WeaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        StackMessage.guiLoaded = True
        icons = loader.loadModel('models/textureCards/icons')
        StackMessage.CrewTex = icons.find('**/pir_t_gui_gen_crew_mug')
        StackMessage.FriendTex = icons.find('**/icon_stickman')
        StackMessage.GuildTex = icons.find('**/pir_t_gui_gen_guild')
        adminGui = loader.loadModel('models/gui/chat_frame_skull')
        StackMessage.AdminTex = adminGui.find('**/chat_frame_skull_over')
        tattooGui = loader.loadModel('models/textureCards/shopCoins')
        StackMessage.TattooTex = tattooGui.find('**/shopCoin_tattoo')
        jollyGui = loader.loadModel('models/effects/effectCards')
        StackMessage.JollyTex = jollyGui.find('**/effectJolly')

    def setText(self):
        BorderFrame.setText(self)
        lines = self.component('text0').textNode.getHeight()
        textSpace = (0.0348 * lines - 0.0276) * self['text_scale'][1] / 0.035
        if textSpace > 100:
            textSpace = 0.0
        self['frameSize'] = (0, 0.8, -0.028 - 0.044 - 0.044 - max(0.042, textSpace), 0)

    def setIcon(self):
        if self.circle:
            self.circle.destroy()
            self.circle = None
        if self.icon:
            self.icon.destroy()
            self.icon = None
        if self.icon2:
            self.icon2.destroy()
            self.icon2 = None
        icon = self['icon']
        if icon:
            category, detail = icon
            imagePos = (0.1, 0, -0.08)
            extraArgs = []
            if category == 'gold':
                image = StackMessage.CoinTex
                imageScale = 0.27
                command = localAvatar.guiMgr.showCollectionMain
            elif category == 'skills':
                image = StackMessage.SkillTex
                imageScale = 0.27
                command = localAvatar.guiMgr.showSkillPage
            elif category == 'reputation':
                repId = detail
                if repId == InventoryType.OverallRep:
                    model = StackMessage.TopLevel
                    imageScale = 0.09
                elif repId == InventoryType.SailingRep:
                    model = StackMessage.SkillIcons
                    imageScale = 0.12
                else:
                    model = StackMessage.WeaponIcons
                    imageScale = 0.12
                asset = ReputationGlobals.RepIcons.get(repId)
                image = model.find('**/%s' % asset)
                command = localAvatar.guiMgr.showSkillPage
            elif category == 'card':
                suit = PlayingCardGlobals.getSuit(detail)
                rank = PlayingCardGlobals.getRank(detail)
                image = PlayingCardGlobals.getImage('standard', suit, rank)
                imageScale = 0.2
                command = localAvatar.guiMgr.showCollectionMain
            elif category == 'collect':
                name = CollectionMap.Assets[detail]
                image = StackMessage.TreasureGui.find('**/%s*' % name)
                imageScale = 0.35
                command = localAvatar.guiMgr.showCollectionMain
            elif category == 'quests':
                image = StackMessage.QuestTex
                imageScale = 0.18
                command = localAvatar.guiMgr.showQuestPanel
            elif category == 'crew':
                image = StackMessage.CrewTex
                imageScale = 0.1
                command = localAvatar.guiMgr.socialPanel.show
            elif category == 'friends':
                image = StackMessage.FriendTex
                imageScale = (0.06, 0, 0.07)
                command = localAvatar.guiMgr.socialPanel.show
            elif category == 'guild':
                image = StackMessage.GuildTex
                imageScale = 0.08
                command = localAvatar.guiMgr.socialPanel.show
            elif category == 'lookout':
                image = StackMessage.LookoutTex
                imageScale = 0.18
                command = localAvatar.guiMgr.showLookoutPanel
            elif category == 'weapon':
                image = StackMessage.WeaponTex
                imageScale = 0.12
                command = localAvatar.guiMgr.showWeaponPanel
            elif category == 'loot':
                if detail == ItemId.CARGO_CRATE:
                    image = StackMessage.CrateTex
                elif detail == ItemId.CARGO_CHEST:
                    image = StackMessage.ChestTex
                elif detail == ItemId.CARGO_SKCHEST:
                    image = StackMessage.RoyalChestTex
                elif detail == ItemId.GOLD:
                    StackMessage.CoinTex
                else:
                    StackMessage.CoinTex
                imageScale = 0.35
                command = localAvatar.guiMgr.showShipPanel
            elif category == 'admin':
                image = StackMessage.AdminTex
                imageScale = 0.3
                command = None
            elif category == 'hat':
                image = StackMessage.HatTex
                imageScale = 0.16
                imagePos = (0.1, 0, -0.12)
                command = localAvatar.guiMgr.showNonPayer
                extraArgs = ['Restricted_Message_Stack_Panel', 10]
            elif category == 'tattoo':
                image = StackMessage.TattooTex
                imageScale = 0.12
                imagePos = (0.1, 0, -0.1)
                command = localAvatar.guiMgr.showNonPayer
                extraArgs = [None, 10]
            elif category == 'pork':
                image = StackMessage.PorkChunkTex
                imageScale = 0.1
                imagePos = (0.1, 0, -0.08)
                command = localAvatar.guiMgr.showNonPayer
            elif category == 'ship':
                image = StackMessage.ShipTex
                imageScale = 0.18
                command = None
            elif category == 'jolly':
                image = StackMessage.JollyTex
                imageScale = 0.12
                command = None
            self.circle = DirectButton(parent=self, relief=None, image=StackMessage.CircleTex, image_scale=0.5, pos=imagePos, command=command, extraArgs=extraArgs)
            if category == 'friends':
                self.icon = OnscreenImage(parent=self.circle, image=image, scale=imageScale, pos=(0.028,
                                                                                                  0,
                                                                                                  0))
                self.icon2 = OnscreenImage(parent=self.circle, image=image, scale=imageScale, pos=(-0.028, 0, 0))
            else:
                self.icon = OnscreenImage(parent=self.circle, image=image, scale=imageScale)
        return

    def getIval(self):
        return self.ival

    def createIval(self, fadeTime, doneFunc=None):
        if not self.ival:
            baseColor = Vec4(1)
            baseTransp = VBase4(baseColor[0], baseColor[1], baseColor[2], 0)
            self.ival = Sequence(LerpColorScaleInterval(self, fadeTime, baseColor, startColorScale=baseTransp, blendType='easeIn'), Wait(max(0.0, self['time'] - 2 * fadeTime)), LerpColorScaleInterval(self, fadeTime, baseTransp))
            if doneFunc:
                self.ival.append(Func(doneFunc))
        return self.ival

    def getHeight(self):
        frameSize = self['frameSize']
        if not frameSize:
            frameSize = self.guiItem.getFrame()
        return frameSize[3] - frameSize[2]


class ModalStackMessage(StackMessage):

    def __init__(self, parent=None, **kwargs):
        StackMessage.__init__(self, parent, **kwargs)
        self.initialiseoptions(ModalStackMessage)
        self.doneFunc = None
        self.fadeTime = 0
        self.setupButtons()
        return

    def destroy(self, autoDestroy=1):
        self.doneFunc = None
        if self['buttonStyle'] == OTPDialog.YesNo:
            self.yesButton.destroy()
            self.noButton.destroy()
        elif self['buttonStyle'] == OTPDialog.CancelOnly:
            self.cancelButton.destroy()
        elif self['buttonStyle'] == OTPDialog.TwoChoice:
            self.boardButton.destroy()
            self.cancelButton.destroy()
        StackMessage.destroy(self, autoDestroy)
        return

    def setupButtons(self):
        if self['buttonStyle'] == OTPDialog.YesNo:
            self.yesButton = GuiButton(parent=self, image_scale=(0.22, 0.22, 0.15), pos=(0.275,
                                                                                         0,
                                                                                         -0.1), text=PLocalizer.DialogYes, command=self.handleYes)
            self.noButton = GuiButton(parent=self, image_scale=(0.22, 0.22, 0.15), pos=(0.55,
                                                                                        0,
                                                                                        -0.1), text=PLocalizer.DialogNo, command=self.handleNo)
            self.adjustFrameForButtons()
        elif self['buttonStyle'] == OTPDialog.CancelOnly:
            lookoutUI = loader.loadModel('models/gui/lookout_gui')
            self.cancelButton = DirectButton(parent=self, relief=None, image=(lookoutUI.find('**/lookout_close_window'), lookoutUI.find('**/lookout_close_window_down'), lookoutUI.find('**/lookout_close_window_over'), lookoutUI.find('**/lookout_close_window_disabled')), pos=(0.75,
                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                   -0.05), scale=0.12, command=self.handleCancel)
        elif self['buttonStyle'] == OTPDialog.TwoChoice:
            self.boardButton = GuiButton(parent=self, image_scale=(0.15, 0.22, 0.15), pos=(0.55,
                                                                                           0,
                                                                                           -0.1), text=PLocalizer.BoardShip, command=self.handleYes)
            lookoutUI = loader.loadModel('models/gui/lookout_gui')
            self.cancelButton = DirectButton(parent=self, relief=None, image=(lookoutUI.find('**/lookout_close_window'), lookoutUI.find('**/lookout_close_window_down'), lookoutUI.find('**/lookout_close_window_over'), lookoutUI.find('**/lookout_close_window_disabled')), pos=(0.75,
                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                   -0.05), scale=0.12, command=self.handleCancel)
            self['frameSize'] = (
             self['frameSize'][0], self['frameSize'][1], self['frameSize'][2] + 0.01, self['frameSize'][3])
            self.adjustFrameForButtons()
        return

    def adjustFrameForButtons(self):
        zOffset = self['frameSize'][2]
        self['frameSize'] = (self['frameSize'][0], self['frameSize'][1], zOffset - 0.06, self['frameSize'][3])
        if self['buttonStyle'] == OTPDialog.YesNo:
            self.yesButton.setZ(zOffset)
            self.noButton.setZ(zOffset)
        elif self['buttonStyle'] == OTPDialog.TwoChoice:
            self.boardButton.setZ(zOffset)

    def __removeIval(self):
        self.ival.pause()
        self.ival = None
        return

    def createIval(self, fadeTime, doneFunc=None):
        StackMessage.createIval(self, fadeTime, doneFunc)
        self.fadeTime = fadeTime
        self.doneFunc = doneFunc
        return self.ival

    def messageDone(self, quick=False):
        if self.ival:
            self.ival.pause()
        if quick:
            fadeTime = 0
        else:
            fadeTime = self.fadeTime
        baseColor = Vec4(1)
        baseTransp = VBase4(baseColor[0], baseColor[1], baseColor[2], 0)
        self.ival = Sequence(LerpColorScaleInterval(self, fadeTime, baseTransp))
        if self.doneFunc:
            self.ival.append(Func(self.doneFunc))

    def handleNo(self):
        if self['noCallback']:
            self['noCallback']()
        self.messageDone()

    def handleYes(self):
        if self['yesCallback']:
            self['yesCallback']()
        self.messageDone()

    def handleCancel(self):
        if self['cancelCallback']:
            self['cancelCallback']()
        self.messageDone()


class MessageStackPanel(DirectFrame):
    popupSfx = None

    def __init__(self, parent=None, **kwargs):
        optiondefs = (('relief', None, None), ('state', DGG.DISABLED, None), ('maxMessages', 3, self.setMaxMessages), ('messageBorder', 0.005, self.setMessageBorder), ('posLerpTime', 0.25, self.setPosLerpTime), ('fadeLerpTime', 0.25, self.setFadeLerpTime))
        self.defineoptions(kwargs, optiondefs, dynamicGroups=('posLerpTime', 'fadeLerpTime',
                                                              'messageBorder'))
        DirectFrame.__init__(self, parent, **kwargs)
        self.initialiseoptions(MessageStackPanel)
        if not MessageStackPanel.popupSfx:
            MessageStackPanel.popupSfx = loadSfx(SoundGlobals.SFX_GUI_STACK_POPUP)
        self.setTransparency(True)
        self.msgStack = []
        self.msgIvals = {}
        self.slideIval = None
        self.task = None
        self.lastMessage = None
        self.shipMessage = None
        self.startPos = self.getPos()
        self.setPos(self._getSlidePos())
        self.hide()
        return

    def destroy(self):
        self.clearMessages()
        DirectFrame.destroy(self)

    def clearMessages(self):
        for msg in self.msgStack[:]:
            self.removeMessage(msg)

        if self.slideIval:
            self.slideIval.pause()
            self.slideIval = None
        self._stopMessageTask()
        return

    def setMaxMessages(self):
        self.maxMessages = self['maxMessages']

    def setPosLerpTime(self):
        self.posLerpTime = self['posLerpTime']

    def getPosLerpTime(self):
        return self['posLerpTime']

    def setFadeLerpTime(self):
        self.fadeLerpTime = self['fadeLerpTime']

    def getFadeLerpTime(self):
        return self['fadeLerpTime']

    def setMessageBorder(self):
        self.messageBorder = self['messageBorder']

    def getMessageBorder(self):
        return self['messageBorder']

    def _getSlotPos(self, slot):
        pos = Point3(0, 0, -self['messageBorder'])
        for msg in self.msgStack[:slot]:
            z = pos[2] - msg.getHeight() - 2 * self['messageBorder']
            pos.setZ(z)

        if slot >= self['maxMessages']:
            z = pos[2] - 10
            pos.setZ(z)
        return pos

    def _getSlidePos(self):
        pos = Point3(self.startPos)
        pos.setZ(pos[2] + self['messageBorder'])
        for msg in self.msgStack[0:self.maxMessages]:
            z = pos[2] + msg.getHeight() + 2 * self['messageBorder']
            pos.setZ(z)

        return pos

    def _getMessageIndex(self, msg):
        for index, m in enumerate(self.msgStack):
            if msg is m:
                return index

        raise ValueError('%s not in list' % msg)

    def _startMessageTask(self):
        self._stopMessageTask()
        self.task = taskMgr.add(self._messageTask, self.uniqueName('MessageStack'))

    def _messageTask(self, task):
        for x, msg in enumerate(self.msgStack):
            ival = msg.getIval()
            if ival:
                if x < self.maxMessages:
                    if not ival.isPlaying():
                        ival.resume()
                else:
                    ival.pause()

        return task.cont

    def _stopMessageTask(self):
        if self.task:
            taskMgr.remove(self.task)

    def _startMsgSlideIval(self, msg, slot):
        self._removeMsgIval(msg)
        ival = Sequence(LerpPosInterval(msg, self['posLerpTime'], self._getSlotPos(slot)), Func(self._removeMsgIval, msg))
        self.msgIvals[msg] = ival
        ival.start()

    def _removeMsgIval(self, msg):
        ival = self.msgIvals.pop(msg, None)
        if ival:
            ival.pause()
        return

    def _adjustStack(self, fromIndex):
        unstable = self.msgStack[fromIndex:]
        for msg in unstable:
            index = self._getMessageIndex(msg)
            self._startMsgSlideIval(msg, index)

    def _startSlideIval(self):
        numMessages = len(self.msgStack)
        if self.slideIval:
            self.slideIval.pause()
        ival = Sequence()
        if numMessages:
            ival.append(Func(self._startMessageTask))
            ival.append(Func(self.show))
        ival.append(LerpPosInterval(self, self['posLerpTime'], self._getSlidePos()))
        if not numMessages:
            ival.append(Func(self._stopMessageTask))
            ival.append(Func(self.hide))
        self.slideIval = ival
        self.slideIval.start()

    def addMessage(self, message, autoDestroy=1):
        self.msgStack.append(message)
        self.msgStack.sort()
        index = self._getMessageIndex(message)
        message.setPos(self._getSlotPos(index))
        message.createIval(self['fadeLerpTime'], Functor(self.removeMessage, message, autoDestroy)).start()
        self._adjustStack(index + 1)
        self._startSlideIval()
        self.popupSfx.play()

    def removeMessage(self, message, autoDestroy=1):
        try:
            text = message['text']
            if self.lastMessage == text:
                self.lastMessage = None
            if self.shipMessage == message:
                self.shipMessage = None
            index = self._getMessageIndex(message)
            self.msgStack.pop(index)
            self._adjustStack(index)
            self._startSlideIval()
        except ValueError:
            pass

        message.destroy(autoDestroy)
        return

    def removeShipMessage(self):
        if self.shipMessage:
            self.removeMessage(self.shipMessage)
            self.shipMessage = None
        return

    def showLoot(self, plunder=[], gold=0, collect=0, card=0, cloth=0, color=0, jewel=None, tattoo=None, weapon=None, bounty=0):
        from pirates.piratesgui.LootPopupPanel import LootPopupPanel
        msg = LootPopupPanel()
        msg.reparentTo(self)
        msg.showLoot(plunder, gold, collect, card, cloth, color, jewel, tattoo, weapon, bounty)
        self.addMessage(msg)

    def addTextMessage(self, text, seconds=7, priority=0, color=(0, 0, 0, 1), icon=(), modelName='general_frame_b', name=None, avId=None, playerName=None):
        if name and playerName:
            t2 = text % (playerName, name)
        else:
            if name:
                t2 = text % name
            else:
                if playerName:
                    t2 = text % playerName
                else:
                    t2 = text
                if self.lastMessage == t2:
                    return
            msg = StackMessage(parent=self, text=t2, text_wordwrap=15.5, text_align=TextNode.ALeft, text_scale=0.035, text_fg=color, text_pos=(0.17, -0.072, 0), textMayChange=1, time=seconds, priority=priority, icon=icon, modelName=modelName)
            if name and playerName:
                buttonText = text % playerName
            else:
                buttonText = text
            if name or playerName:
                msg['text_fg'] = (0, 0, 0, 0)
                if name:
                    nameArray = (
                     '\x01CPOrangeHEAD\x01' + name + '\x02', '\x01CPOrangeHEAD\x01' + name + '\x02', '\x01CPOrangeOVER\x01' + name + '\x02', '\x01CPOrangeHEAD\x01' + name + '\x02')
                else:
                    nameArray = (
                     '\x01CPOrangeHEAD\x01' + playerName + '\x02', '\x01CPOrangeHEAD\x01' + playerName + '\x02', '\x01CPOrangeOVER\x01' + playerName + '\x02', '\x01CPOrangeHEAD\x01' + playerName + '\x02')
                if name:
                    nameButton = DirectButton(parent=NodePath(), relief=None, text=nameArray, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, command=self.handleAvatarTextPress, extraArgs=[avId, name])
                else:
                    nameButton = DirectButton(parent=NodePath(), relief=None, text=nameArray, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, command=self.handlePlayerTextPress, extraArgs=[avId, playerName])
                left, right, bottom, top = nameButton.getBounds()
                nameGFX = TextGraphic(nameButton, left, right, 0, 1)
                if name:
                    buttonName = '\x05' + name + '\x05'
                else:
                    buttonName = '\x05' + playerName + '\x05'
                buttonText = buttonText % buttonName
                tpMgr = TextPropertiesManager.getGlobalPtr()
                if name:
                    tpMgr.setGraphic(name, nameGFX)
                else:
                    tpMgr.setGraphic(playerName, nameGFX)
                del tpMgr
                textRender = TextNode('textRender')
                textRender.setFont(PiratesGlobals.getInterfaceFont())
                textRender.setTextColor(PiratesGuiGlobals.TextFG14)
                textRender.setShadowColor(PiratesGuiGlobals.TextShadow)
                textRender.setWordwrap(15.5)
                textRender.setTabWidth(1.0)
                textRender.setShadow(0.08, 0.08)
                textRender.setText(buttonText)
                x = msg.attachNewNode(textRender.generate())
                x.setScale(0.035)
                x.setPos(0.167, 0, -0.073)
        self.addMessage(msg)
        self.lastMessage = t2
        return msg

    def addModalTextMessage(self, text, buttonStyle=OTPDialog.CancelOnly, noCallback=None, yesCallback=None, cancelCallback=None, seconds=120, priority=0, color=(1, 1, 1, 1), icon=(), modelName='general_frame_f', name=None, avId=None):
        if name:
            t2 = text % name
        else:
            t2 = text
        if self.lastMessage == text:
            return
        msg = ModalStackMessage(parent=self, buttonStyle=buttonStyle, noCallback=noCallback, yesCallback=yesCallback, cancelCallback=cancelCallback, text=text, text_wordwrap=15.5, text_align=TextNode.ALeft, text_scale=0.035, text_fg=color, text_pos=(0.17, -0.072, 0), textMayChange=1, time=seconds, priority=priority, icon=icon, modelName=modelName)
        if name:
            msg['text_fg'] = (0, 0, 0, 0)
            nameArray = ('\x01CPOrangeHEAD\x01' + name + '\x02', '\x01CPOrangeHEAD\x01' + name + '\x02', '\x01CPOrangeOVER\x01' + name + '\x02', '\x01CPOrangeHEAD\x01' + name + '\x02')
            nameButton = DirectButton(parent=NodePath(), relief=None, text=nameArray, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, command=self.handleAvatarModalPress, extraArgs=[avId, name])
            left, right, bottom, top = nameButton.getBounds()
            nameGFX = TextGraphic(nameButton, left, right, 0, 1)
            buttonName = '\x05' + name + '\x05'
            buttonText = text % buttonName
            tpMgr = TextPropertiesManager.getGlobalPtr()
            tpMgr.setGraphic(name, nameGFX)
            del tpMgr
            textRender = TextNode('textRender')
            textRender.setFont(PiratesGlobals.getInterfaceFont())
            textRender.setTextColor(PiratesGuiGlobals.TextFG14)
            textRender.setShadowColor(PiratesGuiGlobals.TextShadow)
            textRender.setWordwrap(15.5)
            textRender.setTabWidth(1.0)
            textRender.setShadow(0.08, 0.08)
            textRender.setText(buttonText)
            x = msg.attachNewNode(textRender.generate())
            x.setScale(0.0345, 1.0, 0.035)
            x.setPos(0.167, 0, -0.073)
        self.addMessage(msg)
        self.lastMessage = text
        if icon and icon[0] == 'ship':
            self.shipMessage = msg
        return msg

    def handleAvatarTextPress(self, avId, avName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)

    def handlePlayerTextPress(self, pId, pName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handlePlayerDetails(pId, pName)

    def handleAvatarModalPress(self, avId, avName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)