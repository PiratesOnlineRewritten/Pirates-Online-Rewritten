from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryPage
from pirates.piratesgui import InventoryItemGui
from pirates.piratesgui import InventoryItemList
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import CollectionMap
from pirates.piratesbase import Freebooter
from pirates.minigame import FishingGlobals

class CollectionPage(InventoryPage.InventoryPage):

    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(CollectionPage)
        self.card = loader.loadModel('models/gui/treasure_gui')
        butcard = loader.loadModel('models/gui/lookout_gui')
        gui = loader.loadModel('models/gui/toplevel_gui')
        ornament = loader.loadModel('models/gui/gui_treasure_window_b')
        ornament.setPos(0.53, 0, 0.72)
        ornament.setScale(0.315)
        ornament.reparentTo(self)
        ornament.flattenStrong()
        self.setLabel = DirectFrame(parent=self, relief=None, pos=(0.42, 0, 1.04), text='', text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=0.05)
        butImg = butcard.find('**/lookout_forward')
        self.backButton = DirectButton(parent=self, relief=None, image_scale=0.18, image=butImg, pos=(0.35,
                                                                                                      0,
                                                                                                      1.055), command=self.goMainPage, extraArgs=[])
        gui.removeNode()
        self.setPics = {}
        self.setFrames = {}
        self.setNum = {}
        self.setHowMany = {}
        self.currentDisplay = 0
        return

    def goMainPage(self):
        base.localAvatar.guiMgr.showCollectionMain()

    def show(self):
        self.refreshList()
        InventoryPage.InventoryPage.show(self)

    def hide(self):
        InventoryPage.InventoryPage.hide(self)

    def clearList(self):
        for item in self.setFrames:
            self.setFrames[item].destroy()

        for item in self.setPics:
            self.setPics[item].destroy()

        for item in self.setNum:
            self.setNum[item].destroy()

        self.setLabel.destroy()
        self.setPics = {}
        self.setFrames = {}
        self.setNum = {}

    def refreshList(self, setKey=0):
        if setKey == 0 or setKey == None:
            return
        if self.currentDisplay != 0:
            oldSize = CollectionMap.Collection_Set_Sizes.get(self.currentDisplay)
            for loopItr in range(oldSize):
                curNum = self.currentDisplay + loopItr + 1
                if curNum in self.setPics:
                    self.setPics[curNum].hide()
                self.setFrames[curNum].hide()

        self.currentDisplay = setKey
        self.setLabel['text'] = PLocalizer.Collections[setKey]
        inv = localAvatar.getInventory()
        if not inv:
            return
        setCount = 0
        heightOffset = 0
        setSize = CollectionMap.Collection_Set_Sizes.get(setKey)
        gui = loader.loadModel('models/gui/toplevel_gui')
        for loopItr in range(setSize):
            setItem = setKey + 1 + loopItr
            rowSpot = loopItr % 4
            colSpot = loopItr / 4
            localHeight = PiratesGuiGlobals.InventoryPanelHeight - 0.2
            howMany = inv.getStackQuantity(setItem)
            if setItem in CollectionMap.Collection_Set_Locked:
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    isLocked = True
                else:
                    isLocked = False
            else:
                isLocked = False
            if isLocked or howMany > 0:
                if setItem in self.setPics:
                    self.setPics[setItem].show()
                    self.setFrames[setItem].show()
                else:
                    frameImg = gui.find('**/treasure_w_b_slot_full')
                    self.setFrames[setItem] = DirectFrame(parent=self, relief=None, image=frameImg, image_scale=0.4, image_pos=(0,
                                                                                                                                0,
                                                                                                                                0), pos=(0.28 + 0.18 * rowSpot, 0, localHeight - 0.36 - 0.18 * colSpot))
                    pic_name = CollectionMap.Assets[setItem]
                    if isLocked:
                        tex = gui.find('**/pir_t_gui_gen_key_subscriber')
                        use_scale = 0.25
                        self.setPics[setItem] = DirectButton(parent=self, relief=None, image=tex, image_scale=use_scale, image_pos=(0,
                                                                                                                                    0,
                                                                                                                                    0), pos=(0.28 + 0.18 * rowSpot, 0, localHeight - 0.36 - 0.18 * colSpot), text=PLocalizer.Collections[setItem], text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ACenter, text_wordwrap=6, text_scale=0.025, text_pos=(0, -0.085, 0), command=base.localAvatar.guiMgr.showNonPayer, extraArgs=['Restricted_Treasure_Selection', 7])
                    else:
                        tex = self.card.find('**/%s*' % pic_name)
                        use_scale = 0.39
                        self.setPics[setItem] = DirectButton(parent=self, relief=None, image=tex, image_scale=use_scale, image_pos=(0,
                                                                                                                                    0,
                                                                                                                                    0), pos=(0.28 + 0.18 * rowSpot, 0, localHeight - 0.36 - 0.18 * colSpot), command=self.clickedTreasure, extraArgs=[setItem], text=PLocalizer.Collections[setItem], text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ACenter, text_wordwrap=6, text_scale=0.025, text_pos=(0, -0.085, 0))
                    self.setPics[setItem].setTransparency(1)
                if setItem in CollectionMap.Collection_Needed:
                    howManyINeed = CollectionMap.Collection_Needed[setItem]
                else:
                    howManyINeed = 1
                if setItem in CollectionMap.Collection_SingleNumeric:
                    if howMany > 0:
                        if howMany == 1:
                            weightTxt = 'Lb'
                        else:
                            weightTxt = 'Lbs'
                        if setItem in self.setHowMany:
                            self.setHowMany[setItem]['text'] = '%d %s' % (howMany, weightTxt)
                        else:
                            self.setHowMany[setItem] = DirectLabel(parent=self.setPics[setItem], relief=None, text='%d %s' % (howMany, weightTxt), text_align=TextNode.ARight, text_scale=0.04, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.08, 0, -0.05), text_font=PiratesGlobals.getInterfaceOutlineFont())
                elif setItem in self.setHowMany:
                    if howManyINeed < 2:
                        self.setHowMany[setItem].hide()
                    else:
                        self.setHowMany[setItem]['text'] = '%d/%d' % (howMany, howManyINeed)
                        self.setHowMany[setItem].show()
                elif howMany > 1:
                    self.setHowMany[setItem] = DirectLabel(parent=self.setPics[setItem], relief=None, text='%d/%d' % (howMany, howManyINeed), text_align=TextNode.ARight, text_scale=0.04, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.08, 0, -0.05), text_font=PiratesGlobals.getInterfaceOutlineFont())
                if isLocked:
                    if setItem in self.setHowMany:
                        self.setHowMany[setItem].hide()
            elif setItem in self.setFrames:
                self.setFrames[setItem].show()
            else:
                frameImg = gui.find('**/treasure_w_b_slot_empty')
                self.setFrames[setItem] = DirectFrame(parent=self, relief=None, image=frameImg, image_scale=0.4, image_pos=(0,
                                                                                                                            0,
                                                                                                                            0), pos=(0.28 + 0.18 * rowSpot, 0, localHeight - 0.36 - 0.18 * colSpot))

        gui.removeNode()
        return

    def destroy(self):
        self.clearList()
        DirectFrame.destroy(self)

    def clickedTreasure(self, value):
        if FishingGlobals.inFishingCollection(value):
            model = FishingGlobals.getModelFromCollection(value)
            inv = localAvatar.getInventory()
            fishWeight = inv.getStackQuantity(value)
            if fishWeight:
                localAvatar.d_requestShowOffFish(value)