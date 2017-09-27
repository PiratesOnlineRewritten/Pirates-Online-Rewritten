from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.otpgui import OTPDialog
from direct.task.Task import Task
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.ListFrame import ListFrame
from pirates.piratesgui.ButtonListItem import ButtonListItem
from pirates.piratesgui.LookoutListItem import LookoutListItem
from pirates.piratesgui.LookoutRequestLVL2 import LookoutRequestLVL2
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesbase import PiratesGlobals
from pirates.world import GameTypeGlobals
from pirates.ship import ShipGlobals
from pirates.uberdog import DistributedInventoryBase
from pirates.band import DistributedBandMember
from pirates.piratesgui.InventoryPage import InventoryPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.uberdog.InventoryRequestGameType import InventoryRequestGameType

class LookoutRequestLVL1(InventoryPage, InventoryRequestGameType):
    notify = directNotify.newCategory('LookoutRequestLVL1')
    ICON_2D_ROTATE = 0
    ICON_2D_FLASH = 1
    TIMER_AUTO_HIDE_MODE_OFF = 0
    TIMER_AUTO_HIDE_MODE_PAGECHANGE = 1
    TIMER_AUTO_HIDE_MODE_TIMEOUT = 2
    LOOKOUT_GUI_FILE = 'models/gui/lookout_gui'
    TOPLEVEL_GUI_FILE = 'models/gui/toplevel_gui'
    CHAR_GUI_FILE = 'models/gui/char_gui'
    MAIN_GUI_FILE = 'models/gui/gui_main'
    UI_VERSION = 1
    PANEL_AUTO_HIDE = 0

    def __init__(self, name, mm, guiMgr):
        self.width = PiratesGuiGlobals.LookoutRequestLVL1Width
        self.height = PiratesGuiGlobals.LookoutRequestLVL1Height
        lookoutUI = loader.loadModel(self.LOOKOUT_GUI_FILE)
        InventoryPage.__init__(self)
        self.initialiseoptions(LookoutRequestLVL1)
        InventoryRequestGameType.__init__(self)
        self.guiMgr = guiMgr
        self.titleText = None
        self.titleImage = None
        self.descText = None
        self.submitButton = None
        self.nextButton = None
        self.backButton = None
        self.activityList = None
        self.activityListItems = None
        self.name = name
        self.currMode = PiratesGuiGlobals.REQUEST_CAT_MODE
        self.selectedItem = None
        self.prevSelectedItem = None
        self.selectedValue = None
        self.prevSelectedValue = None
        self.typePanel = None
        self.joinTimeout = PiratesGlobals.LOOKOUT_JOIN_TIMEOUT
        self.mm = mm
        self.confirmMsg = None
        self.searchParams = {}
        self._createIface()
        self.deleteWhenClosed = False
        self.setSearchActive(False)
        self.searchIconImg = 0
        self.iconAnimType = self.ICON_2D_ROTATE
        self.inviteModes = [
         PiratesGlobals.LOOKOUT_INVITE_NONE]
        self.additionalAvs = []
        self.invited = None
        self.timerTask = None
        self.timerTaskEnd = None
        self.timerEndCallback = None
        self.timerAutoHide = self.TIMER_AUTO_HIDE_MODE_TIMEOUT
        self.invitesParams = None
        self.joinId = 0
        return

    def getUpdateActiveLookoutTaskName(self):
        return self.taskName('updateActiveLookout')

    def setInviteOptions(self, options, additionalAvs=[]):
        self.inviteModes = options
        self.additionalAvs = filter(lambda x: x, additionalAvs)

    def clearInviteOptions(self):
        self.inviteModes = [
         PiratesGlobals.LOOKOUT_INVITE_NONE]
        self.additionalAvs = []

    def setSearchActive(self, active, newMode=PiratesGuiGlobals.REQUEST_CAT_MODE):
        self.searchActive = active
        mode = newMode
        if active:
            pass
        else:
            self.invitedTimedOut()
        self.updateMode(mode)

    def updateMode(self, mode):
        if mode != self.currMode:
            self.stopTimer(self.TIMER_AUTO_HIDE_MODE_PAGECHANGE)
        if self.currMode == PiratesGuiGlobals.SEARCH_MODE or self.currMode == PiratesGuiGlobals.INVITE_MODE or self.currMode == PiratesGuiGlobals.CHALLENGE_MODE or self.currMode == PiratesGuiGlobals.INVITE_ACCEPTED_MODE:
            self.hideStatus()
        elif self.currMode == PiratesGuiGlobals.REQUEST_CAT_MODE:
            self.hideRequestCat()
        elif self.currMode == PiratesGuiGlobals.REQUEST_TYPE_MODE:
            self.hideRequestType()
        elif self.currMode == PiratesGuiGlobals.REQUEST_FOUND_MODE:
            self.hideRequestFound()
        elif self.currMode == PiratesGuiGlobals.REQUEST_JOIN_MODE:
            self.hideJoinMode()
        elif self.currMode == PiratesGuiGlobals.REQUEST_TYPE_DIRECT_MODE:
            self.disableSkipClick()
            self.hideRequestType()
        self.currMode = mode
        if mode == PiratesGuiGlobals.SEARCH_MODE or mode == PiratesGuiGlobals.INVITE_MODE or mode == PiratesGuiGlobals.INVITE_ACCEPTED_MODE or mode == PiratesGuiGlobals.CHALLENGE_MODE:
            self.showStatus()
        elif mode == PiratesGuiGlobals.REQUEST_CAT_MODE:
            self.showRequestCat()
        elif mode == PiratesGuiGlobals.REQUEST_TYPE_MODE:
            self.showRequestType()
        elif mode == PiratesGuiGlobals.REQUEST_FOUND_MODE:
            self.showRequestFound()
        elif mode == PiratesGuiGlobals.REQUEST_JOIN_MODE:
            self.showJoinMode()
        elif mode == PiratesGuiGlobals.REQUEST_TYPE_DIRECT_MODE:
            self.showRequestType()
            self.enableSkipClick()
        self.updateTitle(mode)

    def matchTeleport(self):
        self.updateMode(PiratesGuiGlobals.REQUEST_CAT_MODE)

    def showStatus(self):
        if self.foundType and self.searchParams.has_key('type'):
            self.foundType.show()
            self.foundType['text'] = PLocalizer.LookoutFoundStatusType % self.searchParams['type']
        if self.foundCat and self.searchParams.has_key('cat'):
            self.foundCat.show()
            self.foundCat['text'] = PLocalizer.LookoutFoundStatusCat % self.searchParams['cat']
        if self.SearchContButton:
            self.SearchContButton.show()
        if self.SearchCancelButton:
            self.SearchCancelButton.show()

    def hideStatus(self):
        if self.foundType:
            self.foundType.hide()
        if self.foundCat:
            self.foundCat.hide()
        if self.foundChance:
            self.foundChance.hide()
        if self.SearchContButton:
            self.SearchContButton.hide()
        if self.SearchCancelButton:
            self.SearchCancelButton.hide()

    def updateActiveLookout(self, task=None):
        imageTray = self.guiMgr.chestTray
        lookoutImage = imageTray.lookoutButtonImage
        if self.iconAnimType == self.ICON_2D_ROTATE:
            steps = 50
            halfSteps = 25
            self.searchIconImg = (self.searchIconImg + 1) % steps
            lookoutImage.setImage(imageTray.lookoutButtonNormal)
            lookoutImage.sourceImage = imageTray.lookoutButtonNormal
            increment = 90 / halfSteps
            if self.searchIconImg < halfSteps:
                incrementDir = 1
            else:
                incrementDir = -1
            currR = lookoutImage.getR()
            lookoutImage.setHpr(0, 0, currR + increment * incrementDir)
            lookoutImage.setScale(0.18, 0.18, 0.18)
        elif lookoutImage.sourceImage is imageTray.lookoutButtonNormal:
            lookoutImage.setImage(imageTray.lookoutButtonLight)
            lookoutImage.sourceImage = imageTray.lookoutButtonLight
            if task:
                task.delayTime = 0.5
        else:
            lookoutImage.setImage(imageTray.lookoutButtonNormal)
            lookoutImage.sourceImage = imageTray.lookoutButtonNormal
            if task:
                task.delayTime = 1.0
        return Task.again

    def clearActiveLookout(self):
        imageTray = self.guiMgr.chestTray
        lookoutImage = imageTray.lookoutButtonImage
        lookoutImage.setImage(imageTray.lookoutButtonLight)
        lookoutImage.sourceImage = imageTray.lookoutButtonLight
        if self.iconAnimType == self.ICON_2D_ROTATE:
            lookoutImage.setHpr(0, 0, 0)
            lookoutImage.setScale(0.09, 0.09, 0.09)

    def destroy(self):
        self.cleanup()
        self.mm = None
        self.selectedItem = None
        self.prevSelectedItem = None
        self.selectedValue = None
        self.prevSelectedValue = None
        self.parentPanel = None
        taskMgr.remove(self.getUpdateActiveLookoutTaskName())
        taskMgr.remove('joinedGameAbandon')
        if self.timerTask:
            taskMgr.remove(self.timerTask)
            self.timerTask = None
        DirectFrame.destroy(self)
        self.guiMgr = None
        self.cancelAllInventoryRequests()
        return

    def tryQuickStart(self, options):
        for option in options:
            if int(option[0]) == GameTypeGlobals.GAME_OPTION_SOLO_PLAY:
                if int(option[1]):
                    return True

        return False

    def submitRequest(self):
        options = []
        beingInvited = False
        gameCat = self.getSelectedValue()
        if gameCat is None:
            return
        gameType = PiratesGlobals.GAME_STYLE_ANY
        if self.typePanel:
            gameType = self.typePanel.selectedItem.value
            if self.typePanel:
                options = self.typePanel.getAllGameOptions(gameType, clear=True)
        quickStart = self.tryQuickStart(options)
        if gameCat == PiratesGlobals.GAME_TYPE_TM and gameType == PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL and quickStart:

            def beginTreasureMap(inventory):
                if inventory:
                    treasureMaps = inventory.getTreasureMapsList()
                    for tm in treasureMaps:
                        if tm.mapId == PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL:
                            tm.requestTreasureMapGo(quickStart)

            self.getInventory(localAvatar.inventoryId, beginTreasureMap)
            del beginTreasureMap
            return
        inviting = self.inviteModes != [PiratesGlobals.LOOKOUT_INVITE_NONE]
        if inviting == False and self.invited == None and DistributedBandMember.DistributedBandMember.getBandMember(localAvatar.doId):
            inviting = True
            self.setInviteOptions([PiratesGlobals.LOOKOUT_INVITE_CREW])
        if inviting:
            options.append([str(GameTypeGlobals.GAME_OPTION_VIP_PASS), str(localAvatar.doId)])
        elif self.invited:
            self.notify.debug('I was invited')
            beingInvited = True
            for currOption in self.invited[2]:
                if currOption[0] == str(GameTypeGlobals.GAME_OPTION_VIP_PASS) or currOption[0] == str(GameTypeGlobals.GAME_OPTION_DESIRED_PLAYERS):
                    options.append([currOption[0], currOption[1]])

            self.invitedTimedOut()

        def finishSubmitRequest(options, shipIds):
            self.searchParams = {'cat': GameTypeGlobals.getGameTypeString(gameCat, 'type'),'type': GameTypeGlobals.getGameTypeString(gameType, 'style', category=gameCat),'catId': gameCat,'typeId': gameType,'opts': options}
            selectedVal = gameCat
            if inviting:
                self.notify.debug('sending invites %s' % self.inviteModes)
                localAvatar.sendUpdate('requestInvites', [self.inviteModes, selectedVal, gameType, options, self.additionalAvs])
                self.invitesParams = [
                 gameType, selectedVal, options, shipIds]
            else:
                localAvatar.requestActivity(gameType, selectedVal, options, shipIds)
                self.invitesParams = None
            if self.PANEL_AUTO_HIDE:
                self.toggleVis()
            if beingInvited:
                guiMode = PiratesGuiGlobals.INVITE_ACCEPTED_MODE
            elif inviting:
                if gameCat == PiratesGlobals.GAME_TYPE_PVP:
                    guiMode = PiratesGuiGlobals.CHALLENGE_MODE
                else:
                    guiMode = PiratesGuiGlobals.INVITE_MODE
            else:
                guiMode = PiratesGuiGlobals.SEARCH_MODE
            self.setSearchActive(True, guiMode)
            self.clearInviteOptions()
            return

        self.addShipOptions(options, finishSubmitRequest)
        if self.confirmMsg:
            self.confirmMsg.messageDone()
            self.confirmMsg = None
        return

    def addShipOptions(self, options, callback):

        def receiveInventory(inventory):
            maxCrew = 0
            maxShip = []
            if inventory:
                shipIds = inventory.getShipDoIdList()
            else:
                shipIds = []
                self.notify.warning('could not find inventory in addShipOptions, avId = %s, inventoryId = %s' % (localAvatar.doId, localAvatar.inventoryId))
            for currShipId in shipIds:
                shipView = base.cr.getOwnerView(currShipId)
                if not shipView:
                    continue
                newMaxCrew = ShipGlobals.getShipConfig(shipView.shipClass)['maxCrew']
                if newMaxCrew > maxCrew:
                    maxCrew = newMaxCrew
                    maxShip = [currShipId]

            options.append([str(GameTypeGlobals.GAME_OPTION_MAX_CREW_SIZE), str(maxCrew)])
            callback(options, maxShip)

        self.getInventory(localAvatar.inventoryId, receiveInventory)

    def requestJoin(self):

        def teleportConfirmation(confirmed):
            if confirmed:
                self.submitJoin()
                if self.searchParams and self.searchParams.has_key('catId'):
                    if self.searchParams['catId'] == PiratesGlobals.GAME_TYPE_PVP:
                        base.localAvatar.d_setBandPvp(1)
                    elif self.searchParams['catId'] == PiratesGlobals.GAME_TYPE_PG:
                        base.localAvatar.d_setBandParlor(1)
                    elif self.searchParams['catId'] == PiratesGlobals.GAME_TYPE_TM:
                        if base.localAvatar.guiMgr.crewHUD.crew:
                            base.localAvatar.guiMgr.crewHUD.leaveCrew()
                if self.confirmMsg:
                    self.confirmMsg.messageDone()
                    self.confirmMsg = None
            return

        localAvatar.confirmTeleport(teleportConfirmation, feedback=True)

    def submitJoin(self):
        self.toggleVis()
        self.mm.requestJoin(self.joinId)
        description = PLocalizer.LookoutJoinMsg
        self.guiMgr.messageStack.addTextMessage(description, icon=('lookout', None))
        self.setSearchActive(False, newMode=PiratesGuiGlobals.REQUEST_JOIN_MODE)
        localAvatar.b_setTeleportFlag(PiratesGlobals.TFLookoutJoined)
        return None

    def _showJoinedAbandon(self):
        self.SearchCancelButtonText['text'] = PLocalizer.LookoutJoinCancel
        self.SearchCancelButton.show()

    def _hideJoinedAbandon(self):
        self.SearchCancelButtonText['text'] = PLocalizer.LookoutSearchCancel
        self.SearchCancelButton.hide()

    def cancelRequest(self):
        self.mm.cancelRequest(self.joinId)

    def getItemChangeMsg(self):
        return self.taskName('gameTypeChanged')

    def getItemList(self):
        allGameTypes = GameTypeGlobals.getGameTypes()
        itemList = []
        for currGameType in allGameTypes:
            if GameTypeGlobals.GameTypes[currGameType].get('hidden'):
                continue
            itemList.append({'Text': GameTypeGlobals.getGameTypeString(currGameType, 'type'),'Icon': GameTypeGlobals.getGameTypeString(currGameType, 'icon'),'Value': currGameType})

        return itemList

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        if self.UI_VERSION == 0:
            newItem = ButtonListItem(item, 0.08, 0.75, parent, parentList=self, txtColor=color, pressEffect=False, frameColor=(0,
                                                                                                                               0,
                                                                                                                               0,
                                                                                                                               0))
        else:
            if item['Value'] == PiratesGlobals.GAME_TYPE_PRIV:
                newItem = LookoutListItem(item, self.LOOKOUT_GUI_FILE, 0.16, 0.75, parent, parentList=self, txtColor=color, pressEffect=False, frameColor=(0,
                                                                                                                                                           0,
                                                                                                                                                           0,
                                                                                                                                                           0), wantFrame=True)
            else:
                newItem = LookoutListItem(item, self.TOPLEVEL_GUI_FILE, 0.16, 0.75, parent, parentList=self, txtColor=color, pressEffect=False, frameColor=(0,
                                                                                                                                                            0,
                                                                                                                                                            0,
                                                                                                                                                            0), wantFrame=True)
            newItem.setup()
            if item['Value'] == PiratesGlobals.GAME_TYPE_CREW:
                newItem.icon['scale'] = 0.225
                mainUI = loader.loadModel(self.MAIN_GUI_FILE)
                glowIcon = OnscreenImage(image=mainUI.find('**/icon_glow'), pos=(0.095,
                                                                                 0.0,
                                                                                 0.08), scale=(0.7,
                                                                                               0.7,
                                                                                               0.7), color=(0.18,
                                                                                                            0.404,
                                                                                                            0.396,
                                                                                                            5.0), parent=newItem, sort=-1)
                if self.guiMgr.crewHUD.crew or self.guiMgr.crewHUD.startACrewState or self.guiMgr.crewHUD.joinACrewStatusPVP:
                    if not DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() or base.localAvatar.getSiegeTeam():
                        newItem['state'] = DGG.DISABLED
                        newItem.title['text_fg'] = PiratesGuiGlobals.TextFG9
            elif item['Value'] == PiratesGlobals.GAME_TYPE_PRIV:
                newItem.icon['scale'] = 0.3
                if self.guiMgr.crewHUD.crew or self.guiMgr.crewHUD.startACrewState or self.guiMgr.crewHUD.joinACrewStatus:
                    if not DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() or not base.localAvatar.getSiegeTeam():
                        newItem['state'] = DGG.DISABLED
                        newItem.title['text_fg'] = PiratesGuiGlobals.TextFG9
            elif item['Value'] == PiratesGlobals.GAME_TYPE_CREW or item['Value'] == PiratesGlobals.GAME_TYPE_PRIV or item['Value'] == PiratesGlobals.GAME_TYPE_PVP:
                if hasattr(base, 'localAvatar') and base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_MET_JOLLY_ROGER and not base.localAvatar.guiMgr.forceLookout:
                    newItem['state'] = DGG.DISABLED
                    newItem.title['text_fg'] = PiratesGuiGlobals.TextFG9
        return newItem

    def determineLvl2ItemList(self, category, callback=None, gameType=None):

        def gotStylz(gameStylz):
            availItems = []
            if gameStylz:
                for currStyle in gameStylz:
                    styleName = (
                     GameTypeGlobals.getGameTypeString(currStyle, 'style', category),)
                    desc = (GameTypeGlobals.getGameTypeString(currStyle, 'descriptionStyle', category),)
                    availItems.append({'Text': styleName,'Desc': desc,'Icon': GameTypeGlobals.getGameTypeString(currStyle, 'iconStyle'),'Value': currStyle})

            callback(availItems)

        if gameType != None:
            gotStylz([gameType])
        else:
            self.getGameStyles(category, gotStylz)
        return

    def itemSelect(self, item, nextItemValue=None):
        if item.value == PiratesGlobals.GAME_TYPE_CREW:
            self.toggleAICrewLookout(item.value)
            return
        if item.value == PiratesGlobals.GAME_TYPE_PRIV:
            self.toggleAIPVPCrewLookout(item.value)
            return
        for currItem in self.activityListItems.items:
            currItem.setSelected(False)

        item.setSelected(True)
        self.prevSelectedItem = self.selectedItem
        self.selectedItem = item
        if self.nextButton:
            self.nextButton['state'] = DGG.NORMAL
            return False
        else:
            self.nextClick(nextItemValue)
            return True

    def itemSelectByValue(self, itemValue=None, nextItemValue=None):
        returnVal = False
        itemToSelect = None
        if itemValue == None:
            if len(self.activityListItems.items) > 0:
                itemToSelect = self.activityListItems.items[0]
        else:
            for currItem in self.activityListItems.items:
                if currItem.value == itemValue:
                    itemToSelect = currItem
                    break

            self.prevSelectedValue = self.selectedValue
            if itemToSelect:
                returnVal = self.itemSelect(itemToSelect, nextItemValue)
                self.selectedValue = None
            elif itemValue:
                self.prevSelectedItem = None
                self.selectedItem = None
                self.selectedValue = itemValue
        return returnVal

    def nextClick(self, gameType=None):
        if self.typePanel:
            self.typePanel.destroy()
            self.typePanel = None
        gameCat = self.getSelectedValue()

        def buildLvl2(itemList):
            if itemList and len(itemList) > 0:
                gameCatStr = GameTypeGlobals.getGameTypeString(gameCat, 'type')
                self.typePanel = LookoutRequestLVL2(gameCatStr, titleTextScale=0.05, itemList=itemList, parentPanel=self)
                self.typePanel.reparentTo(self)
                self.typePanel.setPos(0, 0, 0)
            elif self.submitButton:
                self.submitButton['state'] = DGG.NORMAL
            else:
                self.submitRequest()
                return
            self.updateMode(PiratesGuiGlobals.REQUEST_TYPE_MODE)
            messenger.send('lookoutChoseGame')

        self.determineLvl2ItemList(gameCat, buildLvl2, gameType)
        return

    def backClick(self):
        self.updateMode(PiratesGuiGlobals.REQUEST_CAT_MODE)

    def disableSkipClick(self):
        self.backButton.show()
        self.InviteCloseButton.hide()

    def enableSkipClick(self):
        self.backButton.hide()
        self.InviteCloseButton.show()

    def hideRequestCat(self):
        self.activityList.hide()
        if self.submitButton:
            self.submitButton.hide()
        if self.nextButton:
            self.nextButton.hide()

    def showRequestCat(self):
        self.prevSelectedItem = self.selectedItem
        self.selectedItem = None
        self.prevSelectedValue = self.selectedValue
        self.selectedValue = None
        self.activityList.show()
        if self.submitButton:
            self.submitButton.hide()
        if self.nextButton:
            self.nextButton.show()
        return

    def hideRequestType(self):
        if self.typePanel:
            self.typePanel.hide()
        if self.submitButton:
            self.submitButton.hide()
        if self.nextButton:
            self.nextButton.hide()
        if self.backButton:
            self.backButton.hide()

    def showRequestType(self):
        if self.typePanel:
            self.typePanel.show()
        if self.submitButton:
            self.submitButton.show()
        if self.nextButton:
            self.nextButton.hide()
        self.backButton.show()

    def hideRequestFound(self):
        if self.foundType:
            self.foundType.hide()
        if self.foundCat:
            self.foundCat.hide()
        if self.foundJoinButton:
            self.foundJoinButton.hide()
        if self.foundDontJoinButton:
            self.foundDontJoinButton.hide()
        if self.SearchCancelButton:
            self.SearchCancelButton.hide()
        if self.confirmMsg:
            self.confirmMsg.messageDone(quick=True)
            self.confirmMsg = None
        return

    def showRequestFound(self):
        if self.foundType:
            self.foundType.show()
            self.foundType['text'] = PLocalizer.LookoutFoundStatusType % self.searchParams['type']
        if self.foundCat:
            self.foundCat.show()
            self.foundCat['text'] = PLocalizer.LookoutFoundStatusCat % self.searchParams['cat']
        if self.foundJoinButton:
            self.foundJoinButton.show()
        if self.foundDontJoinButton:
            self.foundDontJoinButton.show()
        if self.SearchCancelButton:
            self.SearchCancelButton.show()
        self.startTimer(self.joinTimeout, autoHide=self.TIMER_AUTO_HIDE_MODE_PAGECHANGE)

    def hideJoinMode(self):
        if self.foundType:
            self.foundType.hide()
        if self.foundCat:
            self.foundCat.hide()
        self._hideJoinedAbandon()
        taskMgr.remove('joinedGameAbandon')

    def showJoinMode(self):
        if self.foundType:
            self.foundType.show()
            self.foundType['text'] = PLocalizer.LookoutFoundStatusType % self.searchParams['type']
        if self.foundCat:
            self.foundCat.show()
            self.foundCat['text'] = PLocalizer.LookoutFoundStatusCat % self.searchParams['cat']
        taskMgr.remove('joinedGameAbandon')
        if base.config.GetBool('disable-cancel-join-delay', False):
            numMinutes = 0
        else:
            numMinutes = 2
        taskMgr.doMethodLater(60 * numMinutes, self._showJoinedAbandon, 'joinedGameAbandon', extraArgs=[])

    def startTimer(self, time, callback=None, autoHide=TIMER_AUTO_HIDE_MODE_TIMEOUT):
        if self.timerTask:
            taskMgr.remove(self.timerTask)
        self.timerTask = taskMgr.add(self._updateTimer, 'lookoutTimer')
        self.timerTaskEnd = globalClock.getFrameTime() + time
        self.timerEndCallback = callback
        self.timerAutoHide = autoHide
        if self.TimerDisplay:
            self.TimerDisplay.show()
            self.TimerDisplay['text_fg'] = PiratesGuiGlobals.TextFG1

    def stopTimer(self, hideMode=TIMER_AUTO_HIDE_MODE_TIMEOUT):
        if self.timerAutoHide != hideMode:
            return
        if self.timerTask:
            taskMgr.remove(self.timerTask)
            self.timerTask = None
        if self.TimerDisplay:
            self.TimerDisplay.hide()
        return

    def endTimer(self):
        self.stopTimer()
        if self.timerEndCallback:
            self.timerEndCallback()
            self.timerEndCallback = None
        return

    def _updateTimer(self, task=None):
        timeLeft = self.timerTaskEnd - globalClock.getFrameTime()
        if self.TimerDisplay:
            self.TimerDisplay['text'] = PLocalizer.LookoutTimer % timeLeft
        if timeLeft < 1:
            self.endTimer()
            return Task.done
        return Task.cont

    def cleanup(self):
        self.cleanupRequest()
        self.cleanupSearch()
        self.cleanupFound()

    def cleanupRequest(self):
        if self.typePanel:
            self.typePanel.destroy()
            self.typePanel = None
        if self.activityListItems:
            self.activityListItems.destroy()
            self.activityListItems = None
        if self.submitButton:
            self.submitButton.destroy()
            self.submitButton = None
        if self.nextButton:
            self.nextButton.destroy()
            self.nextButton = None
        if self.backButton:
            self.backButton.destroy()
            self.backButton = None
        if self.activityList:
            self.activityList.destroy()
            self.activityList = None
        return

    def cleanupSearch(self):
        if self.SearchContButton:
            self.SearchContButton.destroy()
            self.SearchContButton = None
        if self.SearchCancelButton:
            self.SearchCancelButton.destroy()
            self.SearchCancelButton = None
        return

    def cleanupFound(self):
        if self.foundType:
            self.foundType.destroy()
            self.foundType = None
        if self.foundCat:
            self.foundCat.destroy()
            self.foundCat = None
        if self.foundJoinButton:
            self.foundJoinButton.destroy()
            self.foundJoinButton = None
        if self.foundDontJoinButton:
            self.foundDontJoinButton.destroy()
            self.foundDontJoinButton = None
        return

    def toggleVis(self, sendMsg=True):
        if not self.isHidden():
            if self.currMode == PiratesGuiGlobals.REQUEST_TYPE_DIRECT_MODE:
                self.invitedTimedOut()
            self.clearInviteOptions()
        else:
            self.activityListItems.redraw()
        if sendMsg:
            messenger.send('guiMgrToggleLookout')

    def clearClipPlaneHack(self, canvas):
        print 'setting clip plane off'

        def blahblah():
            canvas.setClipPlaneOff()
            print 'has clip plane off %s' % canvas.hasClipPlaneOff()

        DelayedCall(Functor(blahblah), delay=1)

    def _createIface(self):
        self.createFoundIface()
        self.createSearchIface()
        self.createRequestIface()

    def createButtonAndText(self, imageInfo=None, textInfo=None):
        if imageInfo == None:
            lookoutUI = loader.loadModel(self.LOOKOUT_GUI_FILE)
            images = (lookoutUI.find('**/lookout_submit'), lookoutUI.find('**/lookout_submit_down'), lookoutUI.find('**/lookout_submit_over'), lookoutUI.find('**/lookout_submit_disabled'))
            buttonPos = (0.83, 0, 0.15)
        else:
            uiTexture = imageInfo.get('textureCard')
            buttonImage = imageInfo.get('imageName')
            imagePostfixes = [
             '', '_down', '_over', '_disabled']
            images = []
            for currImagePostfix in imagePostfixes:
                imageFound = uiTexture.find('**/' + buttonImage + currImagePostfix)
                if imageFound and not imageFound.isEmpty():
                    images.append(imageFound)
                else:
                    images.append(None)

            buttonPos = imageInfo.get('buttonPos')
            buttonHpr = imageInfo.get('buttonHpr')
            buttonScale = imageInfo.get('buttonScale')
            command = imageInfo.get('clickCommand')
            buttonParent = imageInfo.get('parent', self)
        button = DirectButton(parent=buttonParent, relief=None, image=images, command=command, pos=buttonPos, scale=buttonScale, image_hpr=buttonHpr)
        text = None
        if textInfo:
            text = DirectLabel(parent=button, state=DGG.DISABLED, relief=None, text=textInfo, text_align=TextNode.ACenter, text_scale=0.18, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0, 0, -0.35))
        return [
         button, text]

    def createRequestIface(self):
        if self.UI_VERSION == 0:
            lookoutUI = loader.loadModel(self.LOOKOUT_GUI_FILE)
            self.submitButton, self.submitButtonText = self.createButtonAndText(imageInfo={'textureCard': lookoutUI,'imageName': 'lookout_submit','buttonPos': (0.88, 0, 0.15),'buttonScale': 0.3,'clickCommand': self.submitRequest}, textInfo=PLocalizer.LookoutSubmit)
            self.submitButton['state'] = DGG.DISABLED
            self.nextButton, self.nextButtonText = self.createButtonAndText(imageInfo={'textureCard': lookoutUI,'imageName': 'lookout_forward','buttonPos': (0.88, 0, 0.15),'buttonHpr': (0, 0, 180),'buttonScale': 0.3,'clickCommand': self.nextClick}, textInfo=PLocalizer.LookoutNext)
            self.nextButton['state'] = DGG.DISABLED
            self.backButton, self.backButtonText = self.createButtonAndText(imageInfo={'textureCard': lookoutUI,'imageName': 'lookout_forward','buttonPos': (0.69, 0, 0.15),'buttonScale': 0.3,'clickCommand': self.backClick}, textInfo=PLocalizer.LookoutBack)
        else:
            lookoutUI = loader.loadModel(self.LOOKOUT_GUI_FILE)
            self.updateTitle()
            self.backButton, self.backButtonText = self.createButtonAndText(imageInfo={'textureCard': lookoutUI,'imageName': 'lookout_forward','buttonPos': (0.69, 0, 0.15),'buttonScale': 0.3,'clickCommand': self.backClick}, textInfo=PLocalizer.LookoutBack)
        self.activityListItems = ListFrame(0.8, None, 'blah', self, frameColor=(0,
                                                                                0,
                                                                                0,
                                                                                0))
        self.activityListItems.setup()
        if self.UI_VERSION == 0:
            size = (0, 0.82, 0, 0.5)
            pos = (0.15, 0, 0.55)
        else:
            size = (0, 0.82, 0, 1.0)
            pos = (0.15, 0, 0.0)
        charUI = loader.loadModel(self.CHAR_GUI_FILE)
        charGui_slider = charUI.find('**/chargui_slider_large')
        charGui_slider_thumb = charUI.find('**/chargui_slider_node')
        self.activityList = DirectScrolledFrame(parent=self, frameSize=size, relief=DGG.GROOVE, state=DGG.NORMAL, frameColor=(0,
                                                                                                                              0,
                                                                                                                              0,
                                                                                                                              0), borderWidth=PiratesGuiGlobals.BorderWidth, canvasSize=(0, 0.7, 0, self.activityListItems['frameSize'][3]), verticalScroll_image=charGui_slider, verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, 0, self.height * 0.8), verticalScroll_thumb_image=charGui_slider_thumb, sortOrder=5, pos=pos)
        if self.UI_VERSION == 0:
            self.createListFrame(self.activityList, lookoutUI)
        self.activityListItems.reparentTo(self.activityList.getCanvas())
        if self.currMode != PiratesGuiGlobals.REQUEST_TYPE_MODE:
            self.hideRequestType()
        if self.currMode != PiratesGuiGlobals.REQUEST_FOUND_MODE:
            self.hideRequestFound()
        return

    def _determineTitle(self, mode):
        selectedVal = self.searchParams.get('catId')
        if selectedVal == None:
            selectedVal = self.getSelectedValue()
        if mode == PiratesGuiGlobals.SEARCH_MODE:
            iconName = GameTypeGlobals.GameTypeStrings['icon'][self.searchParams['catId']]
            return (
             PLocalizer.LookoutPanelStatus, PLocalizer.LookoutPanelStatusDesc, iconName)
        elif mode == PiratesGuiGlobals.INVITE_MODE:
            iconName = GameTypeGlobals.GameTypeStrings['icon'][self.searchParams['catId']]
            return (
             PLocalizer.LookoutPanelInvite, PLocalizer.LookoutPanelInviteDesc, iconName)
        elif mode == PiratesGuiGlobals.REQUEST_OPT_MODE:
            iconName = GameTypeGlobals.GameTypeStrings['icon'][selectedVal]
            return (
             PLocalizer.LookoutOptionsTitle, PLocalizer.LookoutOptionsDesc, iconName)
        elif mode == PiratesGuiGlobals.REQUEST_FOUND_MODE:
            iconName = GameTypeGlobals.GameTypeStrings['icon'][selectedVal]
            return (
             PLocalizer.LookoutPanelJoin, PLocalizer.LookoutPanelJoinDesc, iconName)
        elif mode == PiratesGuiGlobals.REQUEST_JOIN_MODE:
            iconName = GameTypeGlobals.GameTypeStrings['icon'][selectedVal]
            return (
             PLocalizer.LookoutPanelJoined, PLocalizer.LookoutPanelJoinedDesc, iconName)
        elif mode == PiratesGuiGlobals.REQUEST_TYPE_DIRECT_MODE:
            iconName = GameTypeGlobals.GameTypeStrings['icon'][selectedVal]
            return (
             PLocalizer.LookoutChallengeTitle, PLocalizer.LookoutChallengeDesc, iconName)
        elif mode == PiratesGuiGlobals.CHALLENGE_MODE:
            iconName = GameTypeGlobals.GameTypeStrings['icon'][selectedVal]
            return (
             PLocalizer.LookoutSkirmishTitle, PLocalizer.LookoutSkirmishDesc, iconName)
        elif mode == PiratesGuiGlobals.INVITE_ACCEPTED_MODE:
            iconName = GameTypeGlobals.GameTypeStrings['icon'][selectedVal]
            return (
             PLocalizer.LookoutPanelJoined, PLocalizer.LookoutJoinStatus, iconName)
        else:
            if self.selectedItem:
                iconName = GameTypeGlobals.GameTypeStrings['icon'][self.selectedItem.value]
            else:
                iconName = 'lookout_win_logo'
            title = PLocalizer.LookoutPanelTitle
            titleDesc = PLocalizer.LookoutPanelTitleDesc
            if mode == PiratesGuiGlobals.REQUEST_TYPE_MODE:
                gameTitle = GameTypeGlobals.getGameTypeString(selectedVal, 'type')
                titleDesc = PLocalizer.LookoutPanelTitleDescGame
                title = gameTitle
            return (title, titleDesc, iconName)
        return

    def updateTitle(self, mode=PiratesGuiGlobals.REQUEST_CAT_MODE):
        titleText, titleDesc, iconName = self._determineTitle(mode)
        if self.titleText:
            self.titleText.removeNode()
        self.titleText = DirectLabel(parent=self, relief=None, text=titleText, text_align=TextNode.ALeft, text_scale=0.09, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.36,
                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                              1.17))
        toplevelUI = loader.loadModel(self.TOPLEVEL_GUI_FILE)
        if self.titleImage:
            self.titleImage.removeNode()
        self.titleImage = OnscreenImage(image=toplevelUI.find('**/' + iconName), pos=(0.25,
                                                                                      0,
                                                                                      1.2), scale=(0.6,
                                                                                                   0.6,
                                                                                                   0.6), parent=self)
        if self.descText:
            self.descText.removeNode()
        self.descText = DirectLabel(parent=self, relief=None, text=titleDesc, text_align=TextNode.ALeft, text_scale=0.045, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=15, textMayChange=1, pos=(0.235,
                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                1.06))
        return

    def createListFrame(self, list, lookoutUI=None):
        self.activityListBorderFrame = BorderFrame(parent=list, pos=(0.4, 0, 0.265), scale=(0.8,
                                                                                            1,
                                                                                            0.6))
        self.activityListBorderFrame.setBackgroundVisible(False)

    def createSearchIface(self):
        lookoutUI = loader.loadModel(self.LOOKOUT_GUI_FILE)
        self.SearchContButton, self.SearchContButtonText = self.createButtonAndText(imageInfo={'textureCard': lookoutUI,'imageName': 'lookout_submit','buttonPos': (0.8, 0, 0.15),'buttonScale': 0.3,'clickCommand': self.continueSearch}, textInfo=PLocalizer.LookoutSearchContinue)
        self.SearchCancelButton, self.SearchCancelButtonText = self.createButtonAndText(imageInfo={'textureCard': lookoutUI,'imageName': 'lookout_stop_looking','buttonPos': (0.25, 0, 0.15),'buttonScale': 0.3,'clickCommand': self.cancelSearch}, textInfo=PLocalizer.LookoutSearchCancel)
        self.InviteCloseButton, self.InviteCloseButtonText = self.createButtonAndText(imageInfo={'textureCard': lookoutUI,'imageName': 'lookout_skip','buttonPos': (0.25, 0, 0.15),'buttonScale': 0.3,'clickCommand': self.close}, textInfo=PLocalizer.LookoutInviteSkip)
        self.InviteCloseButton.hide()
        if self.currMode != PiratesGuiGlobals.SEARCH_MODE and self.currMode != PiratesGuiGlobals.INVITE_MODE and self.currMode != PiratesGuiGlobals.CHALLENGE_MODE and self.currMode != PiratesGuiGlobals.INVITE_ACCEPTED_MODE:
            self.hideStatus()

    def createFoundIface(self):
        self.foundCat = DirectLabel(parent=self, relief=None, text=PLocalizer.LookoutFoundStatusCat, text_align=TextNode.ACenter, text_scale=0.055, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.52,
                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                       0.9))
        self.foundType = DirectLabel(parent=self, relief=None, text=PLocalizer.LookoutFoundStatusType, text_align=TextNode.ACenter, text_scale=0.05, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.52,
                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                        0.82))
        self.foundChance = DirectLabel(parent=self, relief=None, text=PLocalizer.LookoutFoundStatusChance, text_align=TextNode.ACenter, text_scale=0.045, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.52,
                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                             0.4))
        lookoutUI = loader.loadModel(self.LOOKOUT_GUI_FILE)
        self.foundJoinButton, self.foundJoinButtonText = self.createButtonAndText(imageInfo={'textureCard': lookoutUI,'imageName': 'lookout_join_game','buttonPos': (0.88, 0, 0.15),'buttonScale': 0.3,'clickCommand': self.requestJoin}, textInfo=PLocalizer.LookoutFoundJoin)
        self.foundDontJoinButton, self.foundDontJoinButtonText = self.createButtonAndText(imageInfo={'textureCard': lookoutUI,'imageName': 'lookout_skip','buttonPos': (0.5, 0, 0.15),'buttonScale': 0.3,'clickCommand': self.skipGame}, textInfo=PLocalizer.LookoutFoundSkip)
        self.TimerDisplay = DirectLabel(parent=self, relief=None, text=PLocalizer.LookoutTimer % self.joinTimeout, text_align=TextNode.ACenter, text_scale=0.055, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.57,
                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                     0.4))
        self.TimerDisplay.hide()
        return

    def continueSearch(self):
        self.toggleVis()

    def skipGame(self, restartRequest=True):
        if restartRequest:
            self.toggleVis()
            self.updateMode(PiratesGuiGlobals.SEARCH_MODE)
            self.mm.skipJoin(self.joinId, False)
        else:
            self.updateMode(PiratesGuiGlobals.REQUEST_CAT_MODE)
            self.mm.skipJoin(self.joinId, True)
        self.invitedTimedOut()

    def cancelSearch(self, local=False):
        if local == False:
            self.mm.cancelRequest(self.joinId)
        self.setSearchActive(False)
        if self.PANEL_AUTO_HIDE:
            self.toggleVis()
        if local == False:
            description = PLocalizer.LookoutCancelMsg
            self.guiMgr.messageStack.addTextMessage(description, icon=('lookout', None))
        localAvatar.b_clearTeleportFlag(PiratesGlobals.TFLookoutJoined)
        return None

    def close(self):
        self.setSearchActive(False)
        self.toggleVis()
        if self.confirmMsg:
            self.confirmMsg.messageDone(quick=True)
            self.confirmMsg = None
        return

    def _destroyIface(self):
        self.cleanup()

    def msgClick(self, task=None):
        self.toggleVis()

    def requestActivityAccepted(self):
        description = PLocalizer.LookoutStartMsg
        self.guiMgr.messageStack.addTextMessage(description, icon=('lookout', None))
        return None

    def matchFound(self, matchId, timeToJoin=PiratesGlobals.LOOKOUT_JOIN_TIMEOUT):
        if self.currMode == PiratesGuiGlobals.SEARCH_MODE or self.currMode == PiratesGuiGlobals.INVITE_MODE or self.currMode == PiratesGuiGlobals.CHALLENGE_MODE or self.currMode == PiratesGuiGlobals.INVITE_ACCEPTED_MODE:
            inviting = self.currMode == PiratesGuiGlobals.INVITE_MODE or self.currMode == PiratesGuiGlobals.CHALLENGE_MODE or self.currMode == PiratesGuiGlobals.INVITE_ACCEPTED_MODE
            if inviting == False and self.guiMgr.isSeaChestAllowed():
                if self.searchParams and self.searchParams.has_key('cat') and self.searchParams['cat'] == PLocalizer.TMGame and self.guiMgr.crewHUD.crew:
                    description = PLocalizer.LookoutFoundCrewMsg
                else:
                    description = PLocalizer.LookoutFoundMsg
                if self.confirmMsg:
                    self.confirmMsg.messageDone()
                    self.confirmMsg = None
                self.confirmMsg = self.guiMgr.messageStack.addModalTextMessage(description, buttonStyle=OTPDialog.YesNo, yesCallback=lambda param1=True, param2=self.searchParams['type']: self.quickConfirm(param1, param2), noCallback=lambda param1=False: self.quickConfirm(param1), icon=('lookout',
                                                                                                                                                                                                                                                                                               None))
            self.joinTimeout = timeToJoin
            self.joinId = matchId
            self.updateMode(PiratesGuiGlobals.REQUEST_FOUND_MODE)
            if inviting:
                self.requestJoin()
        return

    def matchFailed(self, restartRequest):
        if self.currMode == PiratesGuiGlobals.REQUEST_FOUND_MODE or self.currMode == PiratesGuiGlobals.REQUEST_JOIN_MODE or self.currMode == PiratesGuiGlobals.SEARCH_MODE or self.currMode == PiratesGuiGlobals.REQUEST_TYPE_DIRECT_MODE:
            if restartRequest and self.searchParams:
                self.updateMode(PiratesGuiGlobals.SEARCH_MODE)
                description = PLocalizer.LookoutFailedMsg
            else:
                self.updateMode(PiratesGuiGlobals.REQUEST_CAT_MODE)
                description = PLocalizer.LookoutAbortedMsg
            self.guiMgr.messageStack.addTextMessage(description, icon=('lookout', None))
            localAvatar.b_clearTeleportFlag(PiratesGlobals.TFLookoutJoined)
            if self.confirmMsg:
                self.confirmMsg.messageDone()
                self.confirmMsg = None
            self.invitedTimedOut()
        return

    def matchChance(self, matchChance):
        if self.foundChance:
            self.foundChance.show()
            if matchChance <= GameTypeGlobals.MATCH_CHANCE_LOW:
                matchChanceText = PLocalizer.LookoutFoundStatusChanceLow
            elif matchChance <= GameTypeGlobals.MATCH_CHANCE_MODERATE:
                matchChanceText = PLocalizer.LookoutFoundStatusChanceModerate
            else:
                matchChanceText = PLocalizer.LookoutFoundStatusChanceHigh
            self.foundChance['text'] = PLocalizer.LookoutFoundStatusChance % matchChanceText

    def requestInvite(self, inviterName, activityCategory, activityType, options):
        gameCatDesc = GameTypeGlobals.getGameTypeString(activityCategory, 'typeBrief')
        if inviterName == '':
            if activityCategory == PiratesGlobals.GAME_TYPE_TM and self.guiMgr.crewHUD.crew:
                description = PLocalizer.LookoutInviteCrewMsg % gameCatDesc
            else:
                description = PLocalizer.LookoutInviteMsg % gameCatDesc
        else:
            if activityCategory == PiratesGlobals.GAME_TYPE_TM and self.guiMgr.crewHUD.crew:
                description = PLocalizer.LookoutInviteFromCrewMsg % (inviterName, gameCatDesc)
            else:
                description = PLocalizer.LookoutInviteFromMsg % (inviterName, gameCatDesc)
            if self.guiMgr.isSeaChestAllowed():
                if self.confirmMsg:
                    self.confirmMsg.messageDone()
                    self.confirmMsg = None
                self.confirmMsg = self.guiMgr.messageStack.addModalTextMessage(description, buttonStyle=OTPDialog.YesNo, yesCallback=lambda param1=True, param2=activityType: self.quickConfirm(param1, param2), noCallback=lambda param1=False: self.quickConfirm(param1), icon=('lookout',
                                                                                                                                                                                                                                                                                  None))
        self.invited = [
         activityCategory, activityType, options]
        self.displayLookout(gameType=self.invited[0], gameStyle=self.invited[1])
        self.startTimer(PiratesGlobals.LOOKOUT_JOIN_TIMEOUT_INVITE, lambda param1=False: self.invitedTimedOut(param1), self.TIMER_AUTO_HIDE_MODE_PAGECHANGE)
        return

    def unlimitedInviteNotice(self, activityCategory):
        gameCatDesc = GameTypeGlobals.getGameTypeString(activityCategory, 'typeBrief')
        if activityCategory == PiratesGlobals.GAME_TYPE_TM and self.guiMgr.crewHUD.crew:
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.LookoutInviteNeedUnlimited % gameCatDesc, icon=('lookout',
                                                                                                                      None))
        return None

    def quickConfirm(self, yes, activityType=None):
        if yes:
            if self.currMode == PiratesGuiGlobals.REQUEST_FOUND_MODE:
                self.requestJoin()
            else:
                self.typePanel.itemSelectByValue(activityType)
        elif self.currMode == PiratesGuiGlobals.REQUEST_FOUND_MODE:
            self.skipGame()
        else:
            self.skipGame(restartRequest=False)

    def invitedTimedOut(self, clearInvitedInfo=True):
        if clearInvitedInfo:
            self.invited = None
        self.TimerDisplay['text_fg'] = PiratesGuiGlobals.TextFG6
        return

    def displayLookout(self, gameType=PiratesGlobals.GAME_TYPE_TM, gameStyle=PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL, inviteOptions=[PiratesGlobals.LOOKOUT_INVITE_NONE], additionalAvs=[], additionalOptions=[]):
        printStack()
        nextDone = self.itemSelectByValue(gameType, gameStyle)
        if nextDone == False:
            forcedGameType = None
            if inviteOptions == [PiratesGlobals.LOOKOUT_INVITE_NONE]:
                forcedGameType = gameStyle
            self.nextClick(forcedGameType)
        self.updateMode(PiratesGuiGlobals.REQUEST_TYPE_DIRECT_MODE)
        self.setInviteOptions(inviteOptions, additionalAvs)
        self.typePanel.addCustomOptions(gameStyle, additionalOptions)
        if PiratesGlobals.LOOKOUT_INVITE_CREW in inviteOptions:
            self.typePanel.itemSelectByValue(gameStyle)
        return

    def getSelectedValue(self):
        if self.selectedItem:
            return self.selectedItem.value
        else:
            return self.selectedValue

    def requestInvitesResponse(self, invitees):
        if self.invitesParams:
            options = self.invitesParams[2]
            if invitees != []:
                inviteesStr = str(localAvatar.doId)
                for currInvitee in invitees:
                    if currInvitee != localAvatar.doId:
                        inviteesStr = inviteesStr + ',' + str(currInvitee)

                options.append([str(GameTypeGlobals.GAME_OPTION_DESIRED_PLAYERS), inviteesStr])
            else:
                for currOption in options:
                    if currOption[0] == str(GameTypeGlobals.GAME_OPTION_VIP_PASS):
                        options.remove(currOption)
                        break

            localAvatar.requestActivity(*self.invitesParams)
            self.invitesParams = None
        return

    def currentInviteRequiresInvitees(self):
        if self.invitesParams:
            if self.invitesParams[1] == PiratesGlobals.GAME_TYPE_TM:
                return True
        return False

    def restoreOrCancelSearch(self):
        self.cancelSearch()

    def handleChildChange(self):
        newHeight = self.activityListItems['frameSize'][3]
        currCanvasSize = self.activityList['canvasSize']
        self.activityList['canvasSize'] = (currCanvasSize[0], currCanvasSize[1], currCanvasSize[2], newHeight)

    def toggleAICrewLookout(self, itemType):
        if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand():
            localAvatar.guiMgr.crewHUD.toggleCrewLookout()
        else:
            localAvatar.guiMgr.crewHUD.toggleAvatarLookout()
        localAvatar.guiMgr.lookoutPage.close()

    def toggleAIPVPCrewLookout(self, itemType):
        if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand():
            localAvatar.guiMgr.crewHUD.toggleCrewLookout()
        else:
            localAvatar.guiMgr.crewHUD.toggleAvatarLookoutPVP()
        localAvatar.guiMgr.lookoutPage.close()