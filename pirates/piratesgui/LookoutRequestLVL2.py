from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.ListFrame import ListFrame
from pirates.piratesgui.ButtonListItem import ButtonListItem
from pirates.piratesgui.LookoutListItem import LookoutListItem
from pirates.piratesgui.LookoutRequestLVL3 import LookoutRequestLVL3
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.world import GameTypeGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.band import DistributedBandMember
from pirates.uberdog.InventoryRequestGameType import InventoryRequestGameType

class LookoutRequestLVL2(DirectFrame, InventoryRequestGameType):

    def __init__(self, name, titleTextScale=None, itemList=None, parentPanel=None):
        self.width = PiratesGuiGlobals.LookoutRequestLVL2Width
        self.height = PiratesGuiGlobals.LookoutRequestLVL2Height
        DirectFrame.__init__(self, relief=None, state=DGG.DISABLED, frameColor=PiratesGuiGlobals.FrameColor, borderWidth=PiratesGuiGlobals.BorderWidth, frameSize=(0, self.width, 0, self.height))
        self.initialiseoptions(LookoutRequestLVL2)
        InventoryRequestGameType.__init__(self)
        self.parentPanel = parentPanel
        self.name = name
        if itemList:
            self.itemList = itemList
        else:
            self.notify.warning('no itemList provied, displaying default parlor game types')
            self.itemList = [{'Text': GameTypeGlobals.getGameTypeString(PiratesGlobals.GAME_STYLE_BLACKJACK, 'style'),'Value': PiratesGlobals.GAME_STYLE_BLACKJACK}, {'Text': GameTypeGlobals.getGameTypeString(PiratesGlobals.GAME_STYLE_POKER, 'style'),'Value': PiratesGlobals.GAME_STYLE_POKER}]
        self.activityListItems = ListFrame(0.8, None, 'blah', self, frameColor=(0,
                                                                                0,
                                                                                0,
                                                                                0))
        self.activityListItems.setup()
        if self.parentPanel.UI_VERSION == 0:
            size = (0, 0.82, 0, 0.45)
            pos = (0.15, 0, 0.55)
        else:
            size = (0, 0.82, 0, 0.75)
            pos = (0.15, 0, 0.2)
        self.activityList = DirectScrolledFrame(parent=self, frameSize=size, relief=DGG.GROOVE, state=DGG.NORMAL, frameColor=(0,
                                                                                                                              0,
                                                                                                                              0,
                                                                                                                              0), borderWidth=PiratesGuiGlobals.BorderWidth, canvasSize=(0, 0.7, 0, self.activityListItems['frameSize'][3]), verticalScroll_frameColor=PiratesGuiGlobals.ScrollbarColor, verticalScroll_borderWidth=(0.0075,
                                                                                                                                                                                                                                                                                                                                     0.0075), verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, 0, self.height), verticalScroll_thumb_frameColor=PiratesGuiGlobals.ButtonColor2, verticalScroll_incButton_frameColor=PiratesGuiGlobals.ButtonColor2, verticalScroll_decButton_frameColor=PiratesGuiGlobals.ButtonColor2, sortOrder=5, pos=pos)
        if self.parentPanel.UI_VERSION == 0:
            self.createListFrame(self.activityList)
        self.activityListItems.reparentTo(self.activityList.getCanvas())
        self.selectedItem = None
        self.optionsPanel = None
        self.optionsButton = None
        self.rankingDisplay = DirectLabel(parent=self.getParent(), relief=None, text='Ranking', text_align=TextNode.ALeft, text_scale=0.05, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.29, 0, -0.55))
        self.rankingDisplay.hide()
        self.setParentPanel(parentPanel)
        self.storedOptions = {}
        self.customOptions = {}
        return

    def createListFrame(self, list, lookoutUI=None):
        self.activityListBorderFrame = BorderFrame(parent=list, pos=(0.4, 0, 0.25), scale=(0.8,
                                                                                           1,
                                                                                           0.45))
        self.activityListBorderFrame.setBackgroundVisible(False)

    def createOptionsButton(self, lookoutUI=None, parentInfo=None):
        if lookoutUI == None:
            lookoutUI = loader.loadModel('models/gui/lookout_gui')
        if parentInfo == None:
            parent = self.parentPanel
            buttonPos = (0.43, 0, 0.15)
            buttonScale = 0.3
        else:
            parent = parentInfo.get('parent')
            buttonPos = parentInfo.get('pos', (0.43, 0, 0.15))
            buttonScale = parentInfo.get('scale', 0.3)
        optionsButton, optionsButtonText = self.parentPanel.createButtonAndText(imageInfo={'parent': parent,'textureCard': lookoutUI,'imageName': 'lookout_option','buttonPos': buttonPos,'buttonScale': buttonScale,'clickCommand': lambda param=parent: self.optionsClick(param)
           }, textInfo=PLocalizer.Options)
        if parentInfo == None:
            buttonParent = self
        else:
            buttonParent = parent
        buttonParent.optionsButton = optionsButton
        buttonParent.optionsButtonText = optionsButtonText
        if self.parentPanel.submitButton:
            self.parentPanel.submitButton['state'] = DGG.DISABLED
        return

    def setParentPanel(self, parentPanel):
        self.parentPanel = parentPanel

    def hide(self):
        self.activityList.hide()
        if self.optionsButton:
            self.optionsButton.hide()
        if self.rankingDisplay:
            self.rankingDisplay.hide()

    def show(self):
        self.activityList.show()

        def gotOptions(itemList):
            if itemList and len(itemList) > 0 and self.optionsButton:
                self.optionsButton.hide()

        itemList = self.determineLvl3ItemList(self.selectedItem, gotOptions)

    def destroy(self):
        self.selectedItem = None
        self.parentPanel = None
        if self.activityList:
            self.activityList.destroy()
            self.activityList = None
        if self.activityListItems:
            self.activityListItems.destroy()
            self.activityListItems = None
        if self.optionsButton:
            self.optionsButton.destroy()
            self.optionsButton = None
        if self.optionsPanel:
            self.optionsPanel.destroy()
            self.optionsPanel = None
        if self.rankingDisplay:
            self.rankingDisplay.destroy()
        DirectFrame.destroy(self)
        self.cancelAllInventoryRequests()
        return

    def getItemChangeMsg(self):
        return self.taskName('gameTypeChanged')

    def getItemList(self):
        return self.itemList

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        if self.parentPanel.UI_VERSION == 0:
            newItem = ButtonListItem(item, 0.08, 0.75, parent, parentList=self, txtColor=color, pressEffect=False, frameColor=(0,
                                                                                                                               0,
                                                                                                                               0,
                                                                                                                               0))
        else:
            newItem = LookoutListItem(item, self.parentPanel.TOPLEVEL_GUI_FILE, 0.16, 0.75, parent, parentList=self, txtColor=color, pressEffect=False, frameColor=(0,
                                                                                                                                                                    0,
                                                                                                                                                                    0,
                                                                                                                                                                    0), wantFrame=True)
            if self.parentPanel.invited == None:

                def gotOptions(itemList):
                    if itemList and len(itemList) > 0:
                        parentInfo = {'parent': newItem,'pos': (0.675, 0, 0.105),'scale': 0.18}
                        self.createOptionsButton(parentInfo=parentInfo)

                self.determineLvl3ItemList(newItem, gotOptions)
        newItem.setup()
        if item['Value'] == PiratesGlobals.CREW_STYLE_FIND_A_CREW:
            if localAvatar.guiMgr.crewHUD.crew or localAvatar.guiMgr.crewHUD.startACrewState or localAvatar.guiMgr.crewHUD.joinACrewStatusPVP:
                newItem['state'] = DGG.DISABLED
                newItem.title['text_fg'] = PiratesGuiGlobals.TextFG9
                newItem.desc['text_fg'] = PiratesGuiGlobals.TextFG9
        if item['Value'] == PiratesGlobals.CREW_STYLE_RECRUIT_MEMBERS:
            if not localAvatar.guiMgr.crewHUD.crew or DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() == 0:
                newItem['state'] = DGG.DISABLED
                newItem.title['text_fg'] = PiratesGuiGlobals.TextFG9
                newItem.desc['text_fg'] = PiratesGuiGlobals.TextFG9
            if localAvatar.guiMgr.crewHUD.startACrewState:
                newItem['state'] = DGG.NORMAL
                newItem.title['text_fg'] = PiratesGuiGlobals.TextFG1
                newItem.desc['text_fg'] = PiratesGuiGlobals.TextFG1
        if item['Value'] == PiratesGlobals.CREW_STYLE_FIND_A_PVP_CREW:
            if localAvatar.guiMgr.crewHUD.crew or localAvatar.guiMgr.crewHUD.startACrewState or localAvatar.guiMgr.crewHUD.joinACrewStatus:
                newItem['state'] = DGG.DISABLED
                newItem.title['text_fg'] = PiratesGuiGlobals.TextFG9
                newItem.desc['text_fg'] = PiratesGuiGlobals.TextFG9
        if item['Value'] == PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL:
            newItem.title['text_scale'] = PiratesGuiGlobals.TextScaleTitleSmall
        return newItem

    def determineLvl3ItemList(self, item, callback=None):
        availItems = []
        if item == None:
            return availItems
        gameType = self.parentPanel.getSelectedValue()

        def optionsReceived(options):
            if options:
                optionKeys = options.keys()
                for currOption in optionKeys:
                    if options[currOption][0] == PiratesGuiGlobals.UIItemType_Hidden or options.get('execute'):
                        continue
                    availItems.append({'Text': GameTypeGlobals.getGameTypeString(currOption, 'option'),'Option': currOption,'Values': options[currOption][1],'Value': options[currOption][1][0],'ValueType': options[currOption][0]})

            if callback:
                callback(availItems)

        self.getGameOptions(gameType, item.value, optionsReceived)
        return availItems

    def itemSelect(self, item):
        if item.value == PiratesGlobals.CREW_STYLE_FIND_A_CREW or item.value == PiratesGlobals.CREW_STYLE_RECRUIT_MEMBERS or item.value == PiratesGlobals.CREW_STYLE_FIND_A_PVP_CREW:
            self.toggleAICrewLookout(item.value)
            return
        for currItem in self.activityListItems.items:
            currItem.setSelected(False)

        item.setSelected(True)
        self.selectedItem = item
        categoryName = GameTypeGlobals.getGameTypeString(self.selectedItem.value, 'style')
        invCat = GameTypeGlobals.getGameTypeRanking(self.selectedItem.value)
        inv = base.localAvatar.getInventory()
        if inv:
            playerRank = inv.getStackQuantity(invCat)
            self.rankingDisplay['text'] = '%s : %d' % (categoryName, playerRank)
            self.rankingDisplay.show()
        if self.parentPanel.submitButton == None:
            self.parentPanel.submitRequest()
        return

    def optionsClick(self, selectedItem):
        if self.optionsPanel:
            self.optionsPanel.destroy()
            self.optionsPanel = None

        def gotOptions(itemList):
            if itemList and len(itemList) > 0:
                self.optionsPanel = LookoutRequestLVL3(PLocalizer.LookoutOptionsTitle, titleTextScale=0.05, itemList=itemList, optionsFor=selectedItem.value)
                self.optionsPanel.reparentTo(self.parentPanel)
                self.optionsPanel.setPos(0, 0, 0)
                self.optionsPanel.setParentPanel(self)
                gameTypeStr = GameTypeGlobals.getGameTypeString(selectedItem.value, 'style')
                self.optionsPanel.show(gameTypeStr, selectedItem)
                if self.optionsButton:
                    self.optionsButton.hide()
                self.parentPanel.updateMode(PiratesGuiGlobals.REQUEST_OPT_MODE)

        self.determineLvl3ItemList(selectedItem, gotOptions)
        return

    def optionsClose(self):
        self.parentPanel.updateMode(PiratesGuiGlobals.REQUEST_TYPE_MODE)
        if self.parentPanel.deleteWhenClosed:
            self.optionsPanel.destroy()
            self.optionsPanel.removeNode()
            self.optionsPanel = None
        else:
            self.optionsPanel.hide()
        self.rankingDisplay.hide()
        if self.optionsButton:
            self.optionsButton.show()
        return

    def itemSelectByValue(self, itemValue=None):
        itemToSelect = None
        if itemValue == None:
            if len(self.activityListItems.items) > 0:
                itemToSelect = self.activityListItems.items[0]
        else:
            for currItem in self.activityListItems.items:
                print 'checking item with value %s' % currItem.value
                if currItem.value == itemValue:
                    itemToSelect = currItem
                    break

            if itemToSelect:
                self.itemSelect(itemToSelect)
        return

    def addCustomOptions(self, gameType, optionPairs):
        currOptions = self.customOptions.get(gameType)
        if currOptions == None:
            self.customOptions[gameType] = optionPairs
            return
        for currOptionPair in optionPairs:
            for currOption in currOptions:
                if currOption[0] == currOptionPair[0]:
                    currOption[1] = currOptionPair[1]
                    continue

            currOptions.append(currOptionPair)

        return

    def getCustomOptions(self, gameType, clear=False):
        options = self.customOptions.get(gameType, [])
        if clear and len(options) > 0:
            del self.customOptions[gameType]
        return options

    def getAllGameOptions(self, gameType, clear=False):
        if self.optionsPanel:
            options = self.optionsPanel.getGameOptions(gameType, clear)
        else:
            options = []
        customOptions = self.getCustomOptions(gameType, clear)
        return options + customOptions

    def toggleAICrewLookout(self, itemType):
        if itemType == PiratesGlobals.CREW_STYLE_FIND_A_CREW:
            localAvatar.guiMgr.crewHUD.toggleAvatarLookout()
        if itemType == PiratesGlobals.CREW_STYLE_RECRUIT_MEMBERS:
            localAvatar.guiMgr.crewHUD.toggleCrewLookout()
        if itemType == PiratesGlobals.CREW_STYLE_FIND_A_PVP_CREW:
            localAvatar.guiMgr.crewHUD.toggleAvatarLookoutPVP()
        localAvatar.guiMgr.lookoutPage.close()