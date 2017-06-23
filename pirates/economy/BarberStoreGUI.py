from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import GuiButton, DialogButton
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiButton
from pirates.pirate import DynamicHuman
from pirates.piratesgui.TabBar import LeftTab, TabBar
from direct.interval.IntervalGlobal import *
from pirates.makeapirate import BarberGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.pirate.HumanDNA import hairColors, availableHairColors
from pirates.piratesgui import PiratesConfirm
from pirates.ai import HolidayGlobals
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from direct.task import Task
import random
from pirates.piratesbase import Freebooter
FACE_CAMERA = 0

class BarberStoreTab(LeftTab):

    def __init__(self, tabBar, name, **kw):
        optiondefs = (
         ('modelName', 'general_frame_d', None), ('borderScale', 0.38, None), ('bgBuffer', 0.15, None))
        self.defineoptions(kw, optiondefs)
        LeftTab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(BarberStoreTab)
        return None


class BarberStoreTabBar(TabBar):

    def refreshTabs(self):
        for x, name in enumerate(self.tabOrder):
            tab = self.tabs[name]
            tab.reparentTo(self.bParent)
            tab.setPos(-0.07, 0, 1.1 - 0.1 * (x + self.offset))
            (tab.setScale(0.2, 1, 0.2),)

        self.activeIndex = max(0, min(self.activeIndex, len(self.tabOrder) - 1))
        if len(self.tabOrder):
            name = self.tabOrder[self.activeIndex]
            tab = self.tabs[name]
            tab.reparentTo(self.fParent)
            tab.setX(-0.08)
            tab.setScale(0.2, 1, 0.22)

    def makeTab(self, name, **kw):
        return BarberStoreTab(self, name, **kw)


class BarberStoreGUI(DirectFrame):
    notify = directNotify.newCategory('BarberStoreGUI')
    width = (PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.06) * 2
    height = 1.5
    columnWidth = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.05
    holidayIdList = []

    def __init__(self, npc, shopId, **kw):
        optiondefs = (
         ('relief', None, None), ('framSize', (0, self.width, 0, self.height), None), ('sortOrder', 20, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, None, **kw)
        self.initialiseoptions(BarberStoreGUI)
        self.pirate = None
        self.camIval = None
        self.buttons = []
        self.buttonIndex = 0
        self.itemAmount = 0
        self.currentPage = None
        self.confirmBox = None
        self.buttonsPerPage = 3
        self.displayRegionStates = {}
        self.numPages = 0
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.CoinImage = gui.find('**/treasure_w_coin*')
        self.ParchmentIcon = gui.find('**/main_gui_quest_scroll')
        self.barberIconsA = loader.loadModel('models/gui/char_gui')
        self.barberIconsB = loader.loadModel('models/textureCards/shopIcons')
        self.ShirtIcon = loader.loadModel('models/gui/char_gui').find('**/chargui_cloth')
        self.LockIcon = gui.find('**/pir_t_gui_gen_key_subscriber')
        self.backTabParent = self.attachNewNode('backTabs', sort=0)
        self.panel = GuiPanel.GuiPanel(None, self.width, self.height, parent=self, showClose=False)
        self.setPos(0.0, 0, -0.75)
        self.balance = 0
        self.npc = npc
        self.rootTitle = PLocalizer.ShopBarber
        self.paid = Freebooter.getPaidStatus(localAvatar.getDoId())
        self.shopId = shopId
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()
        self.initialCamPos = camera.getPos()
        self.initialCamHpr = camera.getHpr()
        self.initialPirateH = 0
        self.cartWidth = self.columnWidth - 0.1
        self.cartHeight = self.height - 0.25
        self.cartFrame = DirectFrame(parent=self.panel, relief=None, frameSize=(0, self.cartWidth, 0, self.cartHeight))
        self.cartFrame.setPos(self.columnWidth + 0.025, 0, 0.08)
        self.categoryText = [
         [
          PLocalizer.Hat, PLocalizer.Hats], [PLocalizer.Shirt, PLocalizer.Shirts], [PLocalizer.Vest, PLocalizer.Vests], [PLocalizer.Coat, PLocalizer.Coats], [PLocalizer.Pants, PLocalizer.Pants], [PLocalizer.Belt, PLocalizer.Belts], [None, None], [PLocalizer.Shoe, PLocalizer.Shoes]]
        self.frontTabParent = self.panel.attachNewNode('frontTab', sort=2)
        self.myGoldTitle = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.YourMoney, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, pos=(-0.375, 0, 0.175))
        self.myGold = DirectFrame(parent=self.cartFrame, relief=None, text=str(localAvatar.getMoney()), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, image=self.CoinImage, image_scale=0.15, image_pos=(0.03,
                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                  0.015), pos=(-0.06, 0, 0.175))
        self.closeButton = DialogButton.DialogButton(command=self.closePanel, parent=self.cartFrame, text=PLocalizer.lClose, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.02, -PiratesGuiGlobals.TextScaleLarge * 0.25), text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, buttonStyle=DialogButton.DialogButton.NO)
        self.closeButton.setPos(0, 0, 0.005)
        tGui = loader.loadModel('models/gui/triangle')
        triangle = (tGui.find('**/triangle'), tGui.find('**/triangle_down'), tGui.find('**/triangle_over'))
        self.nextPageButton = DirectButton(parent=self.cartFrame, relief=None, state=DGG.DISABLED, image=triangle, image_scale=0.065, pos=(0.18,
                                                                                                                                           0.0,
                                                                                                                                           0.1), rolloverSound=None, command=self.nextPage)
        self.prevPageButton = DirectButton(parent=self.cartFrame, relief=None, state=DGG.DISABLED, image=triangle, image_scale=-0.065, pos=(-0.18, 0.0, 0.1), rolloverSound=None, command=self.previousPage)
        self.pageNumber = DirectFrame(parent=self.cartFrame, relief=None, text='', text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                          0.0), text_shadow=PiratesGuiGlobals.TextShadow, pos=(0,
                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                               0.09))
        self.titleLabel = DirectLabel(parent=self, relief=None, text='', text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge * 1.3, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.62,
                                                                                                                                                                                                                                           0.0,
                                                                                                                                                                                                                                           1.33))
        self.titleLabel.setBin('gui-fixed', 1)
        self.createPirate()
        charGui = loader.loadModel('models/gui/char_gui')
        self.rotateSlider = DirectSlider(parent=base.a2dBottomLeft, relief=None, command=self.rotatePirate, image=charGui.find('**/chargui_slider_small'), image_scale=(2.15,
                                                                                                                                                                        2.15,
                                                                                                                                                                        1.5), thumb_relief=None, thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), pos=(0.8,
                                                                                                                                                                                                                                                                                                                                                      0.0,
                                                                                                                                                                                                                                                                                                                                                      0.09), text_align=TextNode.ACenter, text_scale=(0.1,
                                                                                                                                                                                                                                                                                                                                                                                                      0.1), text_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                      0.1), text_fg=PiratesGuiGlobals.TextFG1, scale=0.43, text=PLocalizer.RotateSlider, value=0.5, sortOrder=-1)
        self.rotateSlider['extraArgs'] = [
         self.rotateSlider]
        self.rotateSliderOrigin = 0.5
        self.accept('mouse1', self._startMouseReadTask)
        self.accept('mouse1-up', self._stopMouseReadTask)
        self.clothWindows = []
        self.clothRenders = []
        self.clothHumans = []
        self.clothCameraNPs = []
        self.clothCameras = []
        self.createDisplayRegions()
        self.alertDialog = None
        self.accept('aspectRatioChanged', self.aspectRatioChange)
        self.accept('NonPayerPanelShown', self.hideDisplayRegions)
        self.accept('NonPayerPanelHidden', self.showDisplayRegions)
        self.accept('MainMenuShown', self.hideDisplayRegions)
        self.accept('MainMenuHidden', self.showDisplayRegions)
        self.accept('GUIShown', self.showDisplayRegions)
        self.accept('GUIHidden', self.hideDisplayRegions)
        localAvatar.guiMgr.chatPanel.show()
        localAvatar.guiMgr.chatPanel.startFadeTextIval()
        self.model = loader.loadModel('models/gui/gui_shop_tailor')
        self.model.reparentTo(self.panel)
        self.model.setBin('gui-fixed', 0)
        self.model.setPos(0.625, 0.0, 1.05)
        self.model.setScale(0.337, 0.0, 0.327)
        localAvatar.guiMgr.hideTrackedQuestInfo()
        self.initTabs()
        self.updateBalance()
        self.focusCamera()
        return

    def hideDisplayRegions(self):
        for id in range(len(self.clothRenders)):
            if self.clothRenders[id].isHidden():
                self.displayRegionStates[id] = False
            else:
                self.displayRegionStates[id] = True
            self.clothRenders[id].hide()

    def showDisplayRegions(self):
        for id in range(len(self.clothRenders)):
            if self.displayRegionStates[id]:
                self.clothRenders[id].show()

    def aspectRatioChange(self):
        properties = base.win.getProperties()
        x = properties.getXSize()
        y = properties.getYSize()
        ar = float(x) / float(y)
        width = 0.125 * aspect2d.getScale()[0]
        height = 0.1 * aspect2d.getScale()[2]
        offsetX = 0.2 * aspect2d.getScale()[0]
        offsetY = -0.015 * aspect2d.getScale()[2]
        for id in range(len(self.buttons)):
            button = self.buttons[id]
            displayRegion = self.clothWindows[id]
            p = button.getPos(render2d) - Point3(width + offsetX, 0, height + offsetY)
            pv = Point3((p[0] + 1) / 2.0, 0.0, (p[2] + 1) / 2.0)
            displayRegion.setDimensions(pv[0], pv[0] + width, pv[2], pv[2] + height)

    def rotatePirate(self, slider):
        if self.pirate and slider:
            value = slider.getValue()
            if value != self.rotateSliderOrigin:
                diff = value - self.rotateSliderOrigin
                h = diff * 360.0 + self.pirate.getH()
                self.pirate.setH(h)
                self.rotateSliderOrigin = value

    def destroy(self):
        DirectFrame.destroy(self)
        self._stopMouseReadTask()
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
            camera.setHpr(0, 0, 0)
        self.rotateSlider.destroy()
        self.cleanupRegions()
        self.unloadPirate()
        if self.confirmBox:
            self.confirmBox.destroy()
            self.confirmBox = None
        if self.model:
            self.model.removeNode()
            self.model = None
        if self.CoinImage:
            self.CoinImage.removeNode()
            self.CoinImage = None
        if self.ParchmentIcon:
            self.ParchmentIcon.removeNode()
            self.ParchmentIcon = None
        if self.barberIconsA:
            self.barberIconsA.removeNode()
            self.barberIconsA = None
        if self.barberIconsB:
            self.barberIconsB.removeNode()
            self.barberIconsB = None
        if self.ShirtIcon:
            self.ShirtIcon.removeNode()
            self.ShirtIcon = None
        if self.alertDialog:
            self.alertDialog.destroy()
        if len(localAvatar.guiMgr.trackedQuestLabel['text']):
            localAvatar.guiMgr.showTrackedQuestInfo()
        localAvatar.guiMgr.chatPanel.hide()
        return

    def createPirate(self):
        self.pirate = DynamicHuman.DynamicHuman()
        self.pirate.setDNAString(localAvatar.style)
        self.pirate.generateHuman(localAvatar.style.gender)
        self.pirate.model.setupSelectionChoices('DEFAULT')
        self.pirate.mixingEnabled = False
        self.pirate.enableBlend()
        self.pirate.loop('idle_centered')
        self.pirate.loop('idle')
        self.pirate.setControlEffect('idle_centered', 0)
        self.pirate.setControlEffect('idle', 1)
        self.pirate.useLOD(2000)
        dummy = self.npc.attachNewNode('dummy')
        dummy.setPos(self.npc.getPos() - Vec3(0, 7, 0))
        parent = self.npc.getParent()
        self.pirate.reparentTo(parent)
        pos = dummy.getPos()
        hpr = dummy.getHpr()
        self.pirate.setPos(pos)
        self.pirate.setHpr(hpr)
        self.pirate.lookAt(self.npc)
        dummy.detachNode()
        self.initialPirateH = self.pirate.getH()
        self.pirate.show()
        localAvatar.stash()

    def focusCamera(self, cameraId=FACE_CAMERA):
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
        self.pirate.setH(self.initialPirateH)
        self.rotateSlider['value'] = self.rotateSliderOrigin = 0.5
        dummy = self.pirate.attachNewNode('dummy')
        if cameraId == FACE_CAMERA:
            dummy.setPos(dummy, 0, 3, self.pirate.headNode.getZ(self.pirate) * 1.1)
        else:
            dummy.setPos(dummy, 0, 0, 0)
        dummy.wrtReparentTo(render)
        if cameraId == FACE_CAMERA:
            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
        else:
            dummy.lookAt(0, 0, 0, 0)
        dummy.setH(dummy, -17)
        dummy.setP(dummy, -12)
        camPos = dummy.getPos()
        camHpr = Point3(dummy.getH(), dummy.getP(), 0)
        dummy.detachNode()
        camera.wrtReparentTo(render)
        camH = camera.getH() % 360
        h = camHpr[0] % 360
        if camH > h:
            h += 360
        if h - camH > 180:
            h -= 360
        camHpr.setX(h)
        camera.setH(camH)
        t = 1.5
        self.camIval = camera.posHprInterval(t, pos=camPos, hpr=camHpr, blendType='easeOut')
        localAvatar.cameraFSM.request('Control')
        self.camIval.start()
        return

    def buyItem(self, uid, button, confirmed=False):
        if confirmed:
            color = button.color
            self.npc.sendRequestBarber(uid, color)
            if self.confirmBox:
                self.confirmBox.destroy()
                self.confirmBox = None
        else:
            if self.confirmBox:
                self.confirmBox.destroy()
                self.confirmBox = None
            item = BarberGlobals.barber_id.get(uid)
            if not item:
                return
            itemColor = button.color
            itemId = item[0]
            type = item[1]
            currentColor = localAvatar.style.getHairColor()
            if type == BarberGlobals.HAIR:
                current = [
                 localAvatar.style.getHairHair(), itemColor]
            else:
                if type == BarberGlobals.BEARD:
                    current = [
                     localAvatar.style.getHairBeard(), itemColor]
                elif type == BarberGlobals.MUSTACHE:
                    current = [
                     localAvatar.style.getHairMustache(), itemColor]
                else:
                    current = 0
                if current == [itemId, currentColor]:
                    self.showCurrentlyOwnedAlert()
                text = PLocalizer.BarberConfirm % (str(item[3]), str(item[4]))
                self.confirmBox = PiratesConfirm.PiratesConfirm(PLocalizer.BarberPurchase, text, self.buyItem, barber=[uid, button, True])
                self.confirmBox.setPos(-self.confirmBox.getWidth() / 2, 0, -self.confirmBox.getHeight() / 2)
                self.confirmBox.setBin('gui-fixed', 1)
        return

    def applyItem(self, pirate, type, uid, button=None):
        if not hasattr(pirate, 'style'):
            return
        if type == BarberGlobals.HAIR:
            pirate.style.setHairHair(uid)
        else:
            if type == BarberGlobals.BEARD:
                pirate.style.setHairBeard(uid)
            elif type == BarberGlobals.MUSTACHE:
                pirate.style.setHairMustache(uid)
            if button:
                pirate.style.setHairColor(button.color)
        pirate.model.handleHeadHiding()

    def purchaseConfirmation(self):
        pass

    def barberPurchase(self, uid, color):
        localAvatar.generateHuman(localAvatar.gender, base.cr.humanHigh)
        localAvatar.motionFSM.off()
        localAvatar.motionFSM.on()
        item = BarberGlobals.barber_id.get(uid)
        id = item[0]
        if item:
            self.applyItem(self.pirate, item[1], id)

    def unloadPirate(self):
        if self.pirate:
            self.pirate.detachNode()
            self.pirate.cleanupHuman()
            self.pirate.delete()
            self.pirate = None
        localAvatar.unstash()
        return

    def closePanel(self):
        messenger.send('exitStore')
        self.ignoreAll()
        localAvatar.cameraFSM.request('Control')
        camera.setPos(self.initialCamPos)
        camera.setHpr(self.initialCamHpr)
        self.unloadPirate()

    def updateBalance(self, extraArgs=None):
        self.myGold['text'] = str(localAvatar.getMoney())
        self.setPage(self.currentPage, self.buttonIndex)

    def initTabs(self):
        self.tabBar = BarberStoreTabBar(parent=self, backParent=self.backTabParent, frontParent=self.frontTabParent, offset=0)
        self.pageNames = []
        self.createTabs()
        if len(self.pageNames) > 0:
            self.setPage(self.pageNames[0])

    def createTabs(self):
        gender = localAvatar.style.getGender()
        for id in BarberGlobals.barberTypes:
            if gender == 'f':
                if id in [BarberGlobals.BEARD, BarberGlobals.MUSTACHE]:
                    continue
                self.isPageAdded(id) or self.addTab(id)

    def addTab(self, id):
        newTab = self.tabBar.addTab(id, command=self.setPage, extraArgs=[id])
        if id == BarberGlobals.HAIR:
            tabIcon = self.barberIconsA.find('**/chargui_hair')
            tabScale = 1.75
        elif id == BarberGlobals.BEARD:
            tabIcon = self.barberIconsB.find('**/icon_shop_tailor_beard')
            tabScale = 0.5
        elif id == BarberGlobals.MUSTACHE:
            tabIcon = self.barberIconsB.find('**/icon_shop_tailor_mustache')
            tabScale = 0.55
        else:
            tabIcon = None
            tabScale = 0.0
        tabText = PLocalizer.barberNames.get(id)
        newTab.nameTag = DirectLabel(parent=newTab, relief=None, state=DGG.DISABLED, pos=(0.06, 0, -0.035), text_fg=PiratesGuiGlobals.TextFG1, text_scale=0.2, image=tabIcon, image_scale=tabScale)
        self.pageNames.append(id)
        return

    def isPageAdded(self, pageName):
        return self.pageNames.count(pageName) > 0

    def nextPage(self):
        if self.itemAmount - (self.buttonIndex + self.buttonsPerPage) > 0:
            startIndex = self.buttonIndex + self.buttonsPerPage
            self.setPage(self.currentPage, startIndex)
        else:
            self.setPage(self.currentPage, 0)

    def previousPage(self):
        if self.buttonIndex > 0:
            startIndex = self.buttonIndex - self.buttonsPerPage
            self.setPage(self.currentPage, startIndex)
        else:
            remainder = self.itemAmount % self.buttonsPerPage
            if remainder:
                startIndex = self.itemAmount - remainder
            else:
                startIndex = self.itemAmount - self.buttonsPerPage
            self.setPage(self.currentPage, startIndex)

    def reloadPirateDNA(self, pirate):
        if pirate is None:
            return
        pirate.style.setHairHair(localAvatar.style.getHairHair())
        pirate.style.setHairBeard(localAvatar.style.getHairBeard())
        pirate.style.setHairMustache(localAvatar.style.getHairMustache())
        pirate.style.setClothesHat(0, 0)
        pirate.style.setHairColor(localAvatar.style.getHairColor())
        pirate.model.handleHeadHiding()
        return

    def sortItems(self, item1, item2):
        if item1[3] is not None:
            return -1
        elif item2[3] is not None:
            return 1
        elif item1[1] == True:
            return -1
        elif item2[1] == True:
            return 1
        elif item1[2] > item2[2]:
            return 1
        elif item1[2] < item2[2]:
            return -1
        else:
            return 0
        return

    def setPage(self, pageName, startIndex=0):
        self.tabBar.unstash()
        self.titleLabel['text'] = '\x01smallCaps\x01' + self.rootTitle + ' - ' + PLocalizer.barberNames.get(pageName) + '\x02'
        if localAvatar.style.getGender() == 'm':
            GENDER = 'MALE'
        else:
            GENDER = 'FEMALE'
        self.currentPage = pageName
        startPos = Vec3(0.63, 0.0, 1.1)
        buttonScale = Vec3(0.8, 0.8, 0.8)
        for item in self.buttons:
            item.destroy()

        self.buttons = []
        choices = []
        regionData = []
        self.buttonIndex = startIndex
        self.itemAmount = 0
        self.reloadPirateDNA(self.pirate)
        startRange = 0
        if GENDER == 'MALE':
            if pageName == BarberGlobals.HAIR:
                startRange = BarberGlobals.MALE_HAIR
            elif pageName == BarberGlobals.BEARD:
                startRange = BarberGlobals.MALE_BEARD
            elif pageName == BarberGlobals.MUSTACHE:
                startRange = BarberGlobals.MALE_MUSTACHE
        elif GENDER == 'FEMALE':
            if pageName == BarberGlobals.HAIR:
                startRange = BarberGlobals.FEMALE_HAIR
            elif pageName == BarberGlobals.BEARD:
                startRange = BarberGlobals.FEMALE_BEARD
            elif pageName == BarberGlobals.MUSTACHE:
                startRange = BarberGlobals.FEMALE_MUSTACHE
        currentHair = localAvatar.style.getHairHair()
        currentBeard = localAvatar.style.getHairBeard()
        currentMustache = localAvatar.style.getHairMustache()
        currentHairColor = localAvatar.style.getHairColor()
        store = self.shopId
        set = BarberGlobals.stores.get(store)
        if set is None:
            return
        for index in range(startRange, startRange + 9999):
            if index in set:
                item = BarberGlobals.barber_id.get(index)
                if item:
                    type = item[1]
                    cost = item[4]
                    itemId = item[0]
                    owned = False
                    holiday = item[5]
                    if type == BarberGlobals.HAIR:
                        if itemId == currentHair:
                            owned = True
                    elif type == BarberGlobals.BEARD:
                        if itemId == currentBeard:
                            owned = True
                    elif type == BarberGlobals.MUSTACHE:
                        if itemId == currentMustache:
                            owned = True
                    if holiday is not None:
                        if holiday in AccessoriesStoreGUI.holidayIdList:
                            choices.append([index, owned, cost, holiday])
                    else:
                        choices.append([index, owned, cost, holiday])

        choices.sort(self.sortItems)
        for choice in choices:
            uid = choice[0]
            item = BarberGlobals.barber_id.get(uid)
            itemId = item[0]
            cost = item[4]
            owned = choice[1]
            text = item[2]
            type = item[1]
            shortDesc = item[2]
            longDesc = item[3]
            helpText = longDesc
            if type == BarberGlobals.MUSTACHE:
                if currentBeard in [1, 2, 3]:
                    itemButton = GuiButton.GuiButton(parent=self.panel, state=DGG.DISABLED, text=PLocalizer.BarberNoMustache, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0,
                                                                                                                                                                           0.05), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, pos=startPos, image_scale=buttonScale)
                    self.buttons.append(itemButton)
                    self.pageNumber['text'] = '%s %s / %s' % (PLocalizer.TailorPage, 1, 1)
                    self.numPages = 1
                    for item in self.clothRenders:
                        item.hide()

                    return
            if self.itemAmount - startIndex < self.buttonsPerPage and self.itemAmount >= startIndex:
                itemButton = GuiButton.GuiButton(command=self.applyItem, parent=self.panel, state=DGG.NORMAL, text=text, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(-0.04, 0.07), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, pos=startPos, image_scale=buttonScale, helpText=helpText, helpDelay=0, helpPos=(0.0, 0.0, -0.12), helpLeftAlign=True, sortOrder=1)
                itemButton['extraArgs'] = [
                 self.pirate, type, itemId, itemButton]
                itemButton.cost = DirectFrame(parent=itemButton, relief=None, text='%s%s' % (PLocalizer.Cost, str(cost)), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), text_shadow=PiratesGuiGlobals.TextShadow, image=self.CoinImage, image_scale=0.15, image_pos=(-0.025,
                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                           0.015), pos=(0.3, 0, -0.08))
                itemButton.previewText = DirectFrame(parent=itemButton, relief=None, text=PLocalizer.TailorPreview, text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleSmall, text_shadow=PiratesGuiGlobals.TextShadow, pos=(-0.09, 0, -0.115))
                itemButton.buy = GuiButton.GuiButton(command=self.buyItem, parent=itemButton, text=PLocalizer.PurchaseCommit, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.25,
                                                                                                                                                                                                                                                                                                                 0.0,
                                                                                                                                                                                                                                                                                                                 0.09), extraArgs=[uid, itemButton])
                startPos -= Vec3(0.0, 0.0, itemButton.getHeight() - 0.03)
                itemButton.helpWatcher.setPos(itemButton.getPos())
                self.buttons.append(itemButton)
                regionData.append([type, uid])
                if cost > localAvatar.getMoney():
                    itemButton.buy['state'] = DGG.DISABLED
                    itemButton.cost['text_fg'] = PiratesGuiGlobals.TextFG6
                if owned:
                    if itemId == 0:
                        itemButton.buy['state'] = DGG.DISABLED
                        itemButton['state'] = DGG.DISABLED
                    itemButton.previewText['text'] = PLocalizer.TattooShopOwned
                if itemId != 0 or GENDER == 'FEMALE':
                    xOffset = -0.05
                    yOffset = 0.0
                    choices = list(availableHairColors)
                    holiday = HolidayGlobals.SAINTPATRICKSDAY
                    if holiday in BarberStoreGUI.holidayIdList:
                        choices.insert(0, 8)
                    for i in choices:
                        hairColor = hairColors[i]
                        hairTone = (hairColor[0], hairColor[1], hairColor[2], 1.0)
                        button = DirectButton(parent=itemButton, relief=DGG.RAISED, pos=(xOffset, 0, yOffset), frameSize=(-0.024, 0.024, -0.025, 0.025), borderWidth=(0.004,
                                                                                                                                                                      0.004), frameColor=hairTone, command=self.handleSetBaseColor, extraArgs=[self.itemAmount, type, i, itemButton], sortOrder=2)
                        xOffset += 0.048

                if not self.paid:
                    itemButton.buy['geom'] = self.LockIcon
                    itemButton.buy['geom_scale'] = 0.2
                    itemButton.buy['geom_pos'] = Vec3(-0.1, 0.0, 0.0)
                    itemButton.buy['command'] = localAvatar.guiMgr.showNonPayer
                    itemButton.buy['extraArgs'] = ['BARBER_CANNOT_BUY', 10]
                itemButton.color = currentHairColor
                itemButton.uid = uid
                itemButton.type = type
                itemButton.itemId = itemId
            self.itemAmount += 1

        if self.itemAmount > self.buttonsPerPage:
            numPages = float(self.itemAmount) / float(self.buttonsPerPage)
            remainder = numPages - int(numPages)
            if remainder > 0:
                numPages += 1.0 - remainder
            page = startIndex / self.buttonsPerPage + 1
        else:
            numPages = 1
            page = 1
        if len(choices):
            self.setupDisplayRegions(regionData, pageName)
        else:
            for item in self.clothRenders:
                item.hide()

            if self.itemAmount <= self.buttonsPerPage:
                self.nextPageButton['state'] = DGG.DISABLED
                self.prevPageButton['state'] = DGG.DISABLED
            if startIndex:
                self.prevPageButton['state'] = DGG.NORMAL
            if startIndex + self.buttonsPerPage < self.itemAmount:
                self.nextPageButton['state'] = DGG.NORMAL
                self.prevPageButton['state'] = DGG.NORMAL
        self.pageNumber['text'] = '%s %s / %s' % (PLocalizer.TailorPage, page, int(numPages))
        self.numPages = numPages
        return

    def handleSetBaseColor(self, humanId, type, color, button):
        self.clothHumans[humanId % self.buttonsPerPage].style.setHairColor(color)
        self.clothHumans[humanId % self.buttonsPerPage].model.handleHeadHiding()
        button.color = color
        self.applyItem(self.pirate, button.type, button.itemId, button)

    def _stopMouseReadTask(self):
        taskMgr.remove('BarberStore-MouseRead')

    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        taskMgr.add(self._mouseReadTask, 'BarberStore-MouseRead')

    def _mouseReadTask(self, task):
        if not base.mouseWatcherNode.hasMouse():
            pass
        else:
            winSize = (
             base.win.getXSize(), base.win.getYSize())
            mouseData = base.win.getPointer(0)
            if mouseData.getX() > winSize[0] or mouseData.getY() > winSize[1]:
                pass
            else:
                dx = mouseData.getX() - self.lastMousePos[0]
                mouseData = base.win.getPointer(0)
                self.lastMousePos = (mouseData.getX(), mouseData.getY())
                value = self.rotateSlider['value']
                value = max(-1, min(1, value + dx * 0.004))
                self.rotateSlider['value'] = value
        return Task.cont

    def cleanupRegions(self):
        for item in self.clothWindows:
            base.win.removeDisplayRegion(item)
            item = None

        self.clothWindows = []
        for item in self.clothCameras:
            del item

        self.clothCameras = []
        for item in self.clothRenders:
            item.remove()
            item.removeNode()

        self.clothRenders = []
        for item in self.clothHumans:
            item.delete()
            item.remove()
            item.removeNode()

        self.clothHumans = []
        for item in self.clothCameraNPs:
            item.remove()
            item.removeNode()

        self.clothCameraNPs = []
        return

    def createDisplayRegions(self):
        startRegion = Vec4(0.526, 0.596, 0.62, 0.69)
        for x in range(self.buttonsPerPage):
            clothWindow = base.win.makeDisplayRegion(startRegion[0], startRegion[1], startRegion[2], startRegion[3])
            clothWindow.setSort(10)
            clothCamera = Camera('clothCamera' + str(x))
            clothRender = NodePath('clothRender' + str(x))
            clothHuman = DynamicHuman.DynamicHuman()
            clothHuman.setDNAString(localAvatar.style)
            clothHuman.generateHuman(localAvatar.style.gender)
            clothCameraNP = NodePath(clothCamera)
            clothCameraNP.reparentTo(clothRender)
            clothHuman.reparentTo(clothRender)
            clothWindow.setCamera(clothCameraNP)
            clothHuman.pose('idle', 1)
            clothHuman.dropShadow.hide()
            clothCamera.getLens().setAspectRatio(base.camLens.getAspectRatio())
            clothCamera.getLens().setNear(0.1)
            self.clothCameras.append(clothCamera)
            self.clothHumans.append(clothHuman)
            self.clothWindows.append(clothWindow)
            self.clothCameraNPs.append(clothCameraNP)
            self.clothRenders.append(clothRender)
            startRegion -= Vec4(0.0, 0.0, 0.12, 0.12)
            self.displayRegionStates[x] = True

    def setupDisplayRegions(self, regionData, pageName):
        bodyShape = localAvatar.style.getBodyShape()
        bodyOffset = 0.0
        if bodyShape == 0:
            bodyOffset = 1
        else:
            if bodyShape == 1:
                bodyOffset = 0
            else:
                if bodyShape == 2:
                    bodyOffset = 0.5
                elif bodyShape == 3:
                    bodyOffset = 1
                elif bodyShape == 4:
                    bodyOffset = 0.5
                x = 0
                m = Mat4(Mat4.identMat())
                headPos = None
                source = localAvatar
                gender = source.style.gender
                source.pose('idle', 1)
                source.update()
                offsetY = 2.0
                offsetH = 200
                x = 0
                for x in range(len(regionData)):
                    if headPos is None:
                        source.getLOD('2000').getChild(0).node().findJoint('def_head01').getNetTransform(m)
                        headPos = TransformState.makeMat(m).getPos().getZ()
                    if pageName == BarberGlobals.HAIR:
                        if gender == 'f':
                            offsetZ = -headPos * 1.04
                        else:
                            offsetZ = -headPos * 1.07
                    elif pageName == BarberGlobals.BEARD:
                        offsetZ = -headPos * 1.0
                    elif pageName == BarberGlobals.MUSTACHE:
                        offsetZ = -headPos * 1.03
                        offsetY = 1.5
                    self.clothHumans[x].setY(offsetY)
                    self.clothHumans[x].setZ(offsetZ)
                    self.clothHumans[x].setH(offsetH)
                    self.reloadPirateDNA(self.clothHumans[x])
                    type = regionData[x][0]
                    uid = regionData[x][1]
                    item = BarberGlobals.barber_id.get(uid)
                    itemId = item[0]
                    self.applyItem(self.clothHumans[x], type, itemId)
                    self.clothRenders[x].show()

            x = len(regionData)
            if x < self.buttonsPerPage:
                for y in range(self.buttonsPerPage - x):
                    self.clothRenders[self.buttonsPerPage - 1 - y].hide()

        self.aspectRatioChange()
        return

    def showCurrentlyOwnedAlert(self):
        self.removeAlertDialog()
        text = PLocalizer.ShopOwnedBarber
        self.alertDialog = PDialog.PDialog(text=text, text_align=TextNode.ACenter, style=OTPDialog.Acknowledge, pos=(-0.65, 0.0, 0.0), command=self.removeAlertDialog)
        self.alertDialog.setBin('gui-fixed', 3, 3)

    def removeAlertDialog(self, value=None):
        if self.alertDialog:
            self.alertDialog.destroy()
            self.alertDialog = None
        return