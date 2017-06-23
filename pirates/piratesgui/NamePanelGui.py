from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.namepanel import NameCheck
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemList
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiPanel
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiButton
from pirates.piratesgui import DialogButton
from pirates.uberdog.UberDogGlobals import *
from pirates.economy import EconomyGlobals
from pirates.piratesgui import PNameTumbler
MAX_NAME_WIDTH = 14
PICK_A_NAME_ENABLED = 0

class NamePanelGui(GuiPanel.GuiPanel):
    notify = directNotify.newCategory('NamePanelGui')
    width = PiratesGuiGlobals.NamePanelWidth
    height = PiratesGuiGlobals.NamePanelHeight

    def __init__(self, title, nameLists, showClose=False, allowEscape=True):
        GuiPanel.GuiPanel.__init__(self, title, self.width, self.height, showClose)
        self.initialiseoptions(NamePanelGui)
        self.nameLists = nameLists
        self.tumblerList = []
        self.name = ''
        self.nameIndices = [0, 0]
        self.isTypedName = 0
        charGui = loader.loadModel('models/gui/char_gui')
        if PICK_A_NAME_ENABLED:
            self.nameModeButton = GuiButton.GuiButton(helpText=PLocalizer.TypeANameHelp, command=self.toggleNameMode, borderWidth=PiratesGuiGlobals.BorderWidth, text=PLocalizer.TypeAName, frameColor=PiratesGuiGlobals.ButtonColor1, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0, -0.01), frameSize=(-0.09, 0.09, -0.015, 0.065), text_scale=PiratesGuiGlobals.TextScaleLarge, pad=(0.01,
                                                                                                                                                                                                                                                                                                                                                                                         0.01), parent=self, pos=(0.12,
                                                                                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                                                                                  0.06))
        self.commitButton = DialogButton.DialogButton(command=self.handleCommit, text=PLocalizer.Submit, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0, -0.01), frameSize=(-0.09, 0.09, -0.015, 0.065), text_scale=PiratesGuiGlobals.TextScaleLarge, parent=self, pos=(self.width - 0.15, 0, 0.07))
        if showClose:
            self.cancelButton = DialogButton.DialogButton(command=self.closePanel, text=PLocalizer.lClose, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0, -0.01), frameSize=(-0.09, 0.09, -0.015, 0.065), text_scale=PiratesGuiGlobals.TextScaleLarge, parent=self, pos=(0.15,
                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                          0.07))
        if allowEscape:
            self.acceptOnce('escape', self.closePanel)
        self.accept('updateNameResult', self.__updateNameResult)
        self.pickAName = DirectFrame(parent=self, relief=None)
        self.nameResult = DirectFrame(parent=self.pickAName, relief=DGG.FLAT, text='', text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleTitleMed, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, frameColor=(0,
                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                             0.5), text_pos=(0,
                                                                                                                                                                                                                                                                             0.007), frameSize=(-0.3, 0.3, -0.015, 0.065), text_font=PiratesGlobals.getPirateOutlineFont(), textMayChange=1)
        self.nameResult.setPos(self.width / 2, 0, self.height - 0.14)
        for i in range(len(self.nameLists)):
            tPos = (i + 1) * (self.width / (len(self.nameLists) + 1))
            tumbler = PNameTumbler.PNameTumbler(self.nameLists[i], '')
            tumbler.reparentTo(self.pickAName)
            tumbler.setPos(tPos, 0, self.height * 0.55)
            tumbler.setScale(0.7)
            self.tumblerList.append(tumbler)

        self.randomButton = GuiButton.GuiButton(command=self.randomName, text=PLocalizer.Random, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0, -0.01), frameSize=(-0.09, 0.09, -0.015, 0.065), text_scale=PiratesGuiGlobals.TextScaleLarge, parent=self.pickAName, pos=(self.width / 2.0, 0, 0.12))
        self.randomName()
        self.typeAName = DirectFrame(parent=self, relief=None)
        self.typeAName.hide()
        self.nameEntry = DirectEntry(parent=self.typeAName, relief=DGG.FLAT, text='', entryFont=PiratesGlobals.getPirateOutlineFont(), text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, text_fg=PiratesGuiGlobals.TextFG1, width=MAX_NAME_WIDTH, frameColor=(0,
                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                   0.5), text_pos=(0,
                                                                                                                                                                                                                                                                                                                   0.007), frameSize=(-0.3, 0.3, -0.015, 0.065), numLines=1, focus=1, cursorKeys=1, text_align=TextNode.ACenter, command=self.handleCommit)
        self.nameEntry.setPos(self.width / 2, 0, self.height - 0.25)
        self.instructions = DirectFrame(parent=self.typeAName, relief=None, text=PLocalizer.TypeANameInstructions, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, frameColor=(0,
                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                      0.5), text_pos=(0,
                                                                                                                                                                                                                                                                                                      0.007), frameSize=(-0.3, 0.3, -0.015, 0.065), textMayChange=1, text_wordwrap=15)
        self.instructions.setPos(self.width / 2, 0, self.height - 0.35)
        charGui.removeNode()
        return

    def toggleNameMode(self):
        if self.isTypedName:
            self.nameModeButton['text'] = PLocalizer.TypeAName
            if self.nameModeButton.helpBox:
                self.nameModeButton.helpBox['text'] = PLocalizer.TypeANameHelp
            self.pickAName.show()
            self.typeAName.hide()
            self.isTypedName = 0
        else:
            self.nameModeButton['text'] = PLocalizer.PickAName
            if self.nameModeButton.helpBox:
                self.nameModeButton.helpBox['text'] = PLocalizer.PickANameHelp
            self.instructions['text'] = PLocalizer.TypeANameInstructions
            self.instructions['text_fg'] = PiratesGuiGlobals.TextFG2
            self.pickAName.hide()
            self.typeAName.show()
            self.isTypedName = 1

    def closePanel(self):
        messenger.send('returnStore')
        self.ignoreAll()
        self.destroy()

    def handleCommit(self, extraArgs=None):
        if self.isTypedName:
            name = self.nameEntry.get()
            name = TextEncoder().decodeText(name)
            name = name.strip()
            name = TextEncoder().encodeWtext(name)
            self.nameEntry['text'] = name
            problem = self.nameIsValid(name)
            if problem:
                self.rejectName(problem)
                return
            else:
                messenger.send('nameChosen', [(name, [])])
        else:
            self.refreshNameIndices()
            messenger.send('nameChosen', [(self.name, self.nameIndices)])
        self.destroy()

    def nameIsValid(self, name):
        self.notify.debug('nameIsValid')
        inventory = base.localAvatar.getInventory()
        if not inventory:
            return None
        usedNames = []
        shipList = inventory.getShipDoIdList()
        for shipId in shipList:
            shipOwnview = base.cr.getOwnerView(shipId)
            usedNames.append(shipOwnview.name)

        if name in usedNames:
            return PLocalizer.ShipNameAlreadyExists % name
        problem = NameCheck.checkName(name, font=self.nameEntry.getFont())
        if problem:
            return problem
        return None

    def rejectName(self, errorStr):
        self.notify.debug('rejectName')
        self.instructions['text'] = errorStr
        self.instructions['text_fg'] = PiratesGuiGlobals.TextFG6
        self.name = ''

    def randomName(self):
        for i in range(len(self.tumblerList)):
            self.tumblerList[i].getRandomResult()

        self.__updateNameResult()

    def __updateNameResult(self):
        self.nameResult['text'] = ''
        for i in range(len(self.tumblerList)):
            self.nameResult['text'] += self.tumblerList[i].getName()
            if i <= len(self.tumblerList) - 1:
                self.nameResult['text'] += ' '

        self.name = self.nameResult['text']

    def refreshNameIndices(self):
        index0 = PLocalizer.PirateShipPrefix.get(self.tumblerList[0].getName())
        index1 = PLocalizer.PirateShipSuffix.get(self.tumblerList[1].getName())
        self.nameIndices = [index0, index1]