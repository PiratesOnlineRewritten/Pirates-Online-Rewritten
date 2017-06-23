import random
import types
import string
from direct.fsm import StateData
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.task import Task
from pandac.PandaModules import *
from pandac.PandaModules import TextEncoder
from otp.namepanel import NameCheck
from otp.otpbase import OTPLocalizer as OL
from pirates.piratesbase import PLocalizer as PL
from pirates.pirate import HumanDNA
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.leveleditor import NPCList
from pirates.makeapirate.PCPickANamePattern import PCPickANamePattern
from direct.distributed.MsgTypes import *
from direct.distributed import PyDatagram
MAX_NAME_WIDTH = 9

class NameGUI(DirectFrame, StateData.StateData):
    NICKNAME = 'Nickname'
    FIRST = 'First'
    PREFIX = 'Prefix'
    SUFFIX = 'Suffix'
    __MODE_INIT = 0
    __MODE_TYPEANAME = 1
    __MODE_PICKANAME = 2
    POSSIBLE_NAME_COMBOS = {'first-last': [0, 1, 1]}
    text = TextNode('text')
    text.setFont(PiratesGlobals.getInterfaceFont())

    def __init__(self, main=None, independent=False):
        DirectFrame.__init__(self)
        DirectFrame.initialiseoptions(self, NameGUI)
        self.charGui = loader.loadModel('models/gui/char_gui')
        self.triangleGui = loader.loadModel('models/gui/triangle')
        if hasattr(base, 'cr') and not hasattr(base.cr, 'isFake'):
            self.cr = base.cr
        else:
            self.cr = None
        self.main = main
        self.independent = independent
        if self.independent:
            np = NodePath(PlaneNode('p', Plane(Vec4(1, 0, 0, 0))))
            self.mainFrame = DirectFrame(parent=base.a2dBottomRight, relief=None)
            self.bookModel = DirectFrame(parent=self.mainFrame, image=self.charGui.find('**/chargui_base'), image_pos=(-0.13, 0, 0), relief=None)
            self.bookModel.setClipPlane(np)
            np.setX(-1.13)
            np.reparentTo(self.bookModel)
            self.mainFrame.setScale(0.42)
            self.mainFrame.setX(-0.76)
            self.mainFrame.setZ(1.2)
            self.parent = self.bookModel
            self.avatar = main
        else:
            self.parent = main.bookModel
            self.avatar = main.avatar
        self.mode = self.__MODE_INIT
        self.wantTypeAName = True
        self.names = [
         '', '', '', '']
        self.savedGender = None
        self.savedMaleName = None
        self.savedMaleActiveStates = None
        self.savedFemaleName = None
        self.savedFemaleActiveStates = None
        self.customName = False
        self.nicknameIndex = 2
        self.firstIndex = 2
        self.prefixIndex = 2
        self.suffixIndex = 2
        self.listsCreated = 0
        self.nicknameActive = 0
        self.firstActive = 1
        self.lastActive = 1
        self.nameEntry = None
        self.pickANameGui = []
        self.typeANameGui = []
        self.fsm = ClassicFSM.ClassicFSM('NameShop', [
         State.State('Init', self.enterInit, self.exitInit, [
          'Pay']),
         State.State('Pay', self.enterPay, self.exitPay, [
          'PickAName', 'TypeAName']),
         State.State('PickAName', self.enterPickAName, self.exitPickAName, [
          'TypeAName', 'Done']),
         State.State('TypeAName', self.enterTypeAName, self.exitTypeAName, [
          'PickAName', 'Approved', 'Accepted', 'Rejected', 'Done']),
         State.State('Approved', self.enterApproved, self.exitApproved, [
          'PickAName', 'Done']),
         State.State('Accepted', self.enterAccepted, self.exitAccepted, [
          'Done']),
         State.State('Rejected', self.enterRejected, self.exitRejected, [
          'TypeAName']),
         State.State('Done', self.enterDone, self.exitDone, [
          'Init', 'Pay'])], 'Init', 'Done')
        self.fsm.enterInitialState()
        self.initNameLists()
        if self.independent or not self.main.wantNPCViewer:
            self.makeRandomName()
        return

    def initNameLists(self):
        buf = [
         '        ', '        ']
        self.nicknamesMale = PL.PirateNames_NickNamesGeneric + PL.PirateNames_NickNamesMale
        self.nicknamesFemale = PL.PirateNames_NickNamesGeneric + PL.PirateNames_NickNamesFemale
        self.firstNamesMale = PL.PirateNames_FirstNamesGeneric + PL.PirateNames_FirstNamesMale
        self.firstNamesFemale = PL.PirateNames_FirstNamesGeneric + PL.PirateNames_FirstNamesFemale
        self.lastPrefixesMale = PL.PirateNames_LastNamePrefixesGeneric + PL.PirateNames_LastNamePrefixesCapped + PL.PirateNames_LastNamePrefixesMale
        self.lastPrefixesFemale = PL.PirateNames_LastNamePrefixesGeneric + PL.PirateNames_LastNamePrefixesCapped + PL.PirateNames_LastNamePrefixesFemale
        self.lastSuffixesMale = PL.PirateNames_LastNameSuffixesGeneric + PL.PirateNames_LastNameSuffixesMale
        self.lastSuffixesFemale = PL.PirateNames_LastNameSuffixesGeneric + PL.PirateNames_LastNameSuffixesFemale
        self.nicknamesMale.sort()
        self.nicknamesFemale.sort()
        self.firstNamesMale.sort()
        self.firstNamesFemale.sort()
        self.lastPrefixesMale.sort()
        self.lastPrefixesFemale.sort()
        self.lastSuffixesMale.sort()
        self.lastSuffixesFemale.sort()
        self.nicknamesMale = buf + self.nicknamesMale + buf
        self.nicknamesFemale = buf + self.nicknamesFemale + buf
        self.firstNamesMale = buf + self.firstNamesMale + buf
        self.firstNamesFemale = buf + self.firstNamesFemale + buf
        self.lastPrefixesMale = buf + self.lastPrefixesMale + buf
        self.lastPrefixesFemale = buf + self.lastPrefixesFemale + buf
        self.lastSuffixesMale = buf + self.lastSuffixesMale + buf
        self.lastSuffixesFemale = buf + self.lastSuffixesFemale + buf
        self.makeRandomName()

    def enter(self):
        if self.mode == self.__MODE_INIT:
            self.loadPickAName()
            self.loadTypeAName()
            self.listsCreated = 1
            name = self.getDNA().getDNAName()
            if name:
                if not self.independent and self.main.isNPCEditor:
                    self.__assignNameToTyped(name)
                    return
                self.decipherName(name)
                if self.mode == self.__MODE_TYPEANAME:
                    return
            else:
                self.makeRandomName()
        else:
            if self.mode == self.__MODE_PICKANAME:
                self.enterPickAName()
            elif self.mode == self.__MODE_TYPEANAME:
                self.enterTypeAName()
            if self.savedGender:
                if self.savedGender != self.getDNA().gender:
                    self.listsCreated = 0
                    self.reset()
                    if self.getDNA().getGender() == 'f':
                        self.nicknameList['items'] = self.nicknamesFemale[:]
                        self.firstList['items'] = self.firstNamesFemale[:]
                        self.prefixList['items'] = self.lastPrefixesFemale[:]
                        self.suffixList['items'] = self.lastSuffixesFemale[:]
                    else:
                        self.nicknameList['items'] = self.nicknamesMale[:]
                        self.firstList['items'] = self.firstNamesMale[:]
                        self.prefixList['items'] = self.lastPrefixesMale[:]
                        self.suffixList['items'] = self.lastSuffixesMale[:]
                    self.listsCreated = 1
                    if self.getDNA().gender == 'm' and self.savedMaleName:
                        self.nicknameIndex, self.firstIndex, self.prefixIndex, self.suffixIndex = self.savedMaleName
                        self.nicknameActive, self.firstActive, self.lastActive = self.savedMaleActiveStates
                    elif self.getDNA().gender == 'f' and self.savedFemaleName:
                        self.nicknameIndex, self.firstIndex, self.prefixIndex, self.suffixIndex = self.savedFemaleName
                        self.nicknameActive, self.firstActive, self.lastActive = self.savedFemaleActiveStates
                    else:
                        self.makeRandomName()
                    self._updateLists()
                    self._updateCheckBoxes()
        self.fsm.request('Pay')

    def exit(self):
        self.hide()
        if self.cr:
            self.ignore(self.cr.getWishNameResultMsg())
        if hasattr(self, 'self._nameCheckCallback'):
            del self._nameCheckCallback
        if self.independent:
            pass
        else:
            self.main.enableRandom()
        self.fsm.request('Done')

    def assignAvatar(self, avatar):
        self.avatar = avatar

    def _checkNpcNames(self, name):

        def match(npcName, name=name):
            name = TextEncoder().encodeWtext(name)
            name = string.strip(name)
            return TextEncoder.upper(npcName) == TextEncoder.upper(name)

        for npcId in NPCList.NPC_LIST.keys():
            data = NPCList.NPC_LIST[npcId]
            if type(data) is types.DictType and HumanDNA.HumanDNA.setName in data:
                npcName = data[HumanDNA.HumanDNA.setName]
                if (self.independent or not self.main.isNPCEditor) and match(npcName):
                    self.notify.info('name matches NPC name "%s"' % npcName)
                    return OL.NCGeneric

    def getTypeANameProblem(self, callback):
        if not self.customName:
            callback(None)
        else:
            problem = None
            name = self.nameEntry.get()
            name = TextEncoder().decodeText(name)
            name = name.strip()
            name = TextEncoder().encodeWtext(name)
            self.nameEntry.enterText(name)
            problem = NameCheck.checkName(self.nameEntry.get(), [self._checkNpcNames], font=self.nameEntry.getFont())
            if problem:
                callback(problem)
            elif self.cr:
                self.ignore(self.cr.getWishNameResultMsg())
                self.acceptOnce(self.cr.getWishNameResultMsg(), self._handleSetWishnameResult)
                self._nameCheckCallback = callback
                self._sendSetWishname(justCheck=True)
                return
        return

    def _checkTypeANameAsPickAName(self):
        if self.customName:
            pnp = PCPickANamePattern(self.nameEntry.get(), self.getDNA().gender)
            if pnp.hasNamePattern():
                self.fsm.request('PickAName')
                pattern = pnp.getNamePattern()
                actives = [0, choice(pattern[1] != -1, 1, 0), choice(pattern[2] != -1, 1, 0)]
                indices = pattern
                self._updateGuiToPickAName(actives, indices)

    def _sendSetWishname(self, justCheck=False):
        name = self.nameEntry.get()
        if justCheck:
            self.cr.sendWishNameAnonymous(name)
        else:
            self.cr.sendWishName(self.main.id, name)

    def _handleSetWishnameResult(self, result, avId, name):
        callback = self._nameCheckCallback
        del self._nameCheckCallback
        problem = OL.NCGeneric
        if result in (self.cr.WishNameResult.PendingApproval, self.cr.WishNameResult.Approved):
            problem = None
        callback(problem)
        return

    def save(self):
        if self.independent:
            if self.customName:
                self._sendSetWishname()
            else:
                name = self.getNumericName()
                self.cr.avatarManager.sendRequestPatternName(self.main.id, name[0], name[1], name[2], name[3])
        else:
            self.avatar.dna.setName(self._getName())

    def loadPickAName(self):
        self.nameFrameTitle = DirectFrame(parent=self.parent, relief=None, frameColor=(0.5,
                                                                                       0.5,
                                                                                       0.5,
                                                                                       0.3), text=PL.NameFrameTitle, text_fg=(1,
                                                                                                                              1,
                                                                                                                              1,
                                                                                                                              1), text_scale=0.18, text_pos=(0,
                                                                                                                                                             0), pos=(0,
                                                                                                                                                                      0,
                                                                                                                                                                      0.3), scale=0.7)
        self.pirateName = DirectLabel(parent=self.parent, relief=None, image=self.charGui.find('**/chargui_frame02'), image_scale=(15,
                                                                                                                                   10,
                                                                                                                                   10), text=PL.NameGUI_EmptyNameText, text_align=TextNode.ACenter, text_fg=(1,
                                                                                                                                                                                                             1,
                                                                                                                                                                                                             0.5,
                                                                                                                                                                                                             1), text_pos=(0,
                                                                                                                                                                                                                           0.25), text_wordwrap=MAX_NAME_WIDTH, scale=0.15, pos=(0,
                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                 -1.1))
        if self.getDNA().getGender() == 'f':
            lists = (
             self.nicknamesFemale, self.firstNamesFemale, self.lastPrefixesFemale, self.lastSuffixesFemale)
        else:
            lists = (
             self.nicknamesMale, self.firstNamesMale, self.lastPrefixesMale, self.lastSuffixesMale)
        self.nicknameList = self._makeScrolledList(items=lists[0], pos=(-0.81, 0, -0.2), makeExtraArgs=[self.NICKNAME], extraArgs=[0])
        self.nicknameList.stash()
        self.firstList = self._makeScrolledList(items=lists[1], pos=(-0.65, 0, -0.2), makeExtraArgs=[self.FIRST], extraArgs=[1])
        self.prefixList = self._makeScrolledList(items=lists[2], pos=(-0.1, 0, -0.2), makeExtraArgs=[self.PREFIX], extraArgs=[2])
        self.suffixList = self._makeScrolledList(items=lists[3], pos=(0.45, 0, -0.2), makeExtraArgs=[self.SUFFIX], extraArgs=[3])
        self.nicknameCheck = self._makeCheckbox(text=PL.NameGUI_CheckboxText[0], command=self.nicknameToggle, pos=(-0.81, 0, 0.1))
        self.nicknameCheck.stash()
        self.firstCheck = self._makeCheckbox(text=PL.NameGUI_CheckboxText[0], command=self.firstToggle, pos=(-0.65, 0, 0.1))
        self.lastCheck = self._makeCheckbox(text=PL.NameGUI_CheckboxText[0], command=self.lastToggle, pos=(-0.1, 0, 0.1))
        self.nicknameHigh = self._makeHighlight((-0.81, 0, -0.2))
        self.nicknameHigh.hide()
        self.firstHigh = self._makeHighlight((-0.65, 0, -0.2))
        self.prefixHigh = self._makeHighlight((-0.1, 0, -0.2))
        self.suffixHigh = self._makeHighlight((0.45, 0, -0.2))
        self.randomNameButton = self._makeButton(text=PL.NameGUI_RandomButtonText, command=self.makeRandomName, pos=(-0.5,
                                                                                                                     0,
                                                                                                                     -1.4))
        self.randomNameButton.hide()
        func = lambda param=self: param.fsm.request('TypeAName')
        self.typeANameButton = self._makeButton(text=PL.NameGUI_TypeANameButtonText, command=func, pos=(0,
                                                                                                        0,
                                                                                                        -1.7))
        self.typeANameButton.hide()
        self.pickANameGui.append(self.nicknameHigh)
        self.pickANameGui.append(self.firstHigh)
        self.pickANameGui.append(self.prefixHigh)
        self.pickANameGui.append(self.suffixHigh)
        self.pickANameGui.append(self.nicknameList)
        self.pickANameGui.append(self.firstList)
        self.pickANameGui.append(self.prefixList)
        self.pickANameGui.append(self.suffixList)
        self.pickANameGui.append(self.pirateName)
        self.pickANameGui.append(self.typeANameButton)
        self.pickANameGui.append(self.nicknameCheck)
        self.pickANameGui.append(self.firstCheck)
        self.pickANameGui.append(self.lastCheck)
        self.hide()
        return

    def loadTypeAName(self):
        self.nameEntry = DirectEntry(parent=self.parent, relief=DGG.FLAT, scale=0.16, width=MAX_NAME_WIDTH, numLines=2, focus=0, cursorKeys=1, autoCapitalize=1, frameColor=(0.0,
                                                                                                                                                                             0.0,
                                                                                                                                                                             0.0,
                                                                                                                                                                             0.0), text=PL.NameGUI_EmptyNameText, text_fg=(1.0,
                                                                                                                                                                                                                           1.0,
                                                                                                                                                                                                                           0.5,
                                                                                                                                                                                                                           1.0), pos=(-0.65, 0.0, -0.05), suppressKeys=1, suppressMouse=1, image=self.charGui.find('**/chargui_frame02'), image_scale=(15,
                                                                                                                                                                                                                                                                                                                                                       0.0,
                                                                                                                                                                                                                                                                                                                                                       8.5), image_pos=(4.39, 0.0, -0.2))
        self.nameEntryGuidelines = DirectLabel(parent=self.parent, relief=None, text=PL.NameGUI_Guidelines, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG3, text_pos=(0,
                                                                                                                                                                                    0.25), text_wordwrap=18, scale=0.1, pos=(-0.7,
                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                             -0.5))
        if self.cr:
            self.nameEntryGuidelinesURL = DirectButton(parent=self.parent, relief=None, pos=(0,
                                                                                             0,
                                                                                             -0.55), command=base.popupBrowser, extraArgs=[launcher.getValue('GAME_INGAME_NAMING')], text=PL.NameGUI_URLText, text0_fg=PiratesGuiGlobals.TextFG2, text1_fg=PiratesGuiGlobals.TextFG2, text2_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getInterfaceFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_scale=0.09, text_pos=(0, -0.635))
        func = lambda param=self: param.fsm.request('PickAName')
        self.pickANameButton = self._makeButton(text=PL.NameGUI_PickANameButtonText, command=func, pos=(0,
                                                                                                        0,
                                                                                                        -1.7))
        if not self.independent:
            if not self.main.isNPCEditor:
                self.submitButton = self._makeButton(text=PL.NameGUI_SubmitButtonText, command=self._typedAName, pos=(0,
                                                                                                                      0,
                                                                                                                      1.7))
                self.submitButton.hide()
        else:
            self.cancelButton = GuiButton.GuiButton(parent=self.bookModel, text=PL.MakeAPirateCancel, text_fg=(1,
                                                                                                               1,
                                                                                                               1,
                                                                                                               1), text_scale=0.08, text_pos=(0, -0.25 * 0.1, 0), scale=1.8, image_scale=0.4, command=self.cancel, pos=(-0.68,
                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                        -2.43))
            self.randomButton = GuiButton.GuiButton(parent=self.bookModel, text=PL.RandomButton, text_fg=(1,
                                                                                                          1,
                                                                                                          1,
                                                                                                          1), text_scale=0.08, text_pos=(0, -0.25 * 0.1, 0), scale=1.8, image_scale=0.4, command=self.makeRandomName, pos=(0.05,
                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                           -2.43))
            self.randomButton.hide()
            self.randomButton
            self.submitButton = GuiButton.GuiButton(parent=self.bookModel, text=PL.NameGUI_SubmitButtonText, text_fg=(1,
                                                                                                                      1,
                                                                                                                      1,
                                                                                                                      1), text_scale=0.08, text_pos=(0, -0.25 * 0.1, 0), scale=1.8, image_scale=0.4, command=self.complete, pos=(0.78,
                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                 -2.43))
        self.typeANameGui.append(self.pickANameButton)
        self.typeANameGui.append(self.nameEntry)
        self.typeANameGui.append(self.nameEntryGuidelines)
        if self.cr:
            self.typeANameGui.append(self.nameEntryGuidelinesURL)
        self.hide()
        return

    def _makeScrolledList(self, items, pos, makeExtraArgs, extraArgs):
        lst = items[:]
        dsl = DirectScrolledList(parent=self.parent, relief=None, items=lst, itemMakeFunction=self._makeItemLabel, itemMakeExtraArgs=makeExtraArgs, extraArgs=extraArgs, command=self._listsChanged, pos=pos, scale=0.08, incButton_pos=(1.5,
                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                         -6), incButton_relief=None, incButton_image=(self.triangleGui.find('**/triangle'), self.triangleGui.find('**/triangle_down'), self.triangleGui.find('**/triangle_over')), incButton_image_scale=1.8, incButton_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   90), incButton_image_pos=(0, 0, -0.5), decButton_pos=(1.5,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         2), decButton_relief=None, decButton_image=(self.triangleGui.find('**/triangle'), self.triangleGui.find('**/triangle_down'), self.triangleGui.find('**/triangle_over')), decButton_image_scale=1.8, decButton_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  270), decButton_image_pos=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             0.5), itemFrame_relief=None, itemFrame_pos=(-0.75, 0, 0), itemFrame_scale=1.0, itemFrame_image=self.charGui.find('**/chargui_frame04'), itemFrame_image_scale=(14,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            10,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            10), itemFrame_image_pos=(2.4,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      -2), itemFrame_text_fg=(1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              1), forceHeight=1.1, numItemsVisible=5)
        return dsl

    def _makeHighlight(self, pos):
        return DirectFrame(parent=self.parent, relief=DGG.FLAT, frameColor=(1, 1, 1,
                                                                            0.4), frameSize=(-1.1,
                                                                                             4,
                                                                                             -2.2,
                                                                                             -1.1), borderWidth=(1,
                                                                                                                 0.5), pos=pos, scale=0.09)

    def _makeItemLabel(self, text, index, args=[]):
        f = DirectFrame(state='normal', relief=None, text=text, text_scale=1.0, text_pos=(-0.3, 0.14, 0), text_align=TextNode.ALeft, text_fg=(1,
                                                                                                                                              1,
                                                                                                                                              1,
                                                                                                                                              1), textMayChange=0)
        if len(args) > 0:
            listType = args[0]
            f.bind(DGG.B1PRESS, lambda x, f=f: self._nameClickedOn(listType, index))
        return f

    def _makeButton(self, text, command, pos):
        b = DirectButton(parent=self.parent, relief=None, image=(self.charGui.find('**/chargui_frame02'), self.charGui.find('**/chargui_frame02_down'), self.charGui.find('**/chargui_frame02_over')), text=text, text_fg=(1,
                                                                                                                                                                                                                           1,
                                                                                                                                                                                                                           1,
                                                                                                                                                                                                                           1), text_align=TextNode.ACenter, text_scale=0.1, command=command, pos=pos)
        return b

    def _makeCheckbox(self, text, command, pos):
        c = DirectCheckButton(parent=self.parent, relief=None, scale=0.1, boxBorder=0.08, boxRelief=None, pos=pos, text=text, text_fg=(1,
                                                                                                                                       1,
                                                                                                                                       1,
                                                                                                                                       1), text_scale=0.8, text_pos=(0.4,
                                                                                                                                                                     0), indicator_pos=(0,
                                                                                                                                                                                        0,
                                                                                                                                                                                        0), indicator_text_fg=(1,
                                                                                                                                                                                                               1,
                                                                                                                                                                                                               1,
                                                                                                                                                                                                               1), command=command, text_align=TextNode.ALeft)
        return c

    def _nameClickedOn(self, listType, index):
        if listType == self.NICKNAME:
            self.nicknameIndex = index
        elif listType == self.FIRST:
            self.firstIndex = index
        elif listType == self.PREFIX:
            self.prefixIndex = index
        else:
            self.suffixIndex = index
        self._updateLists()

    def _listsChanged(self, extraArgs):
        if self.listsCreated:
            if extraArgs == 0:
                if self.nicknameActive:
                    self.enableList(self.nicknameList)
                    self.names[0] = self.nicknameList['items'][self.nicknameList.index + 2]['text']
                    self.nicknameHigh.show()
                else:
                    self.disableList(self.nicknameList)
                    self.names[0] = ''
                    self.nicknameHigh.hide()
                self.nicknameIndex = self.nicknameList.index + 2
            elif extraArgs == 1:
                if self.firstActive:
                    self.enableList(self.firstList)
                    self.names[1] = self.firstList['items'][self.firstList.index + 2]['text']
                    self.firstHigh.show()
                else:
                    self.disableList(self.firstList)
                    self.names[1] = ''
                    self.firstHigh.hide()
                self.firstIndex = self.firstList.index + 2
            elif extraArgs == 2:
                if self.lastActive:
                    self.enableList(self.prefixList)
                    self.names[2] = self.prefixList['items'][self.prefixList.index + 2]['text']
                    self.prefixHigh.show()
                else:
                    self.disableList(self.prefixList)
                    self.names[2] = ''
                    self.prefixHigh.hide()
                self.prefixIndex = self.prefixList.index + 2
            elif extraArgs == 3:
                if self.lastActive:
                    self.enableList(self.suffixList)
                    self.names[3] = self.suffixList['items'][self.suffixList.index + 2]['text']
                    self.suffixHigh.show()
                else:
                    self.disableList(self.suffixList)
                    self.names[3] = ''
                    self.suffixHigh.hide()
                self.suffixIndex = self.suffixList.index + 2
            if len(self.names[0] + self.names[1] + self.names[2] + self.names[3]) > 0:
                self.updateName()

    def _updateLists(self):
        oldIndices = [
         self.nicknameIndex, self.firstIndex, self.prefixIndex, self.suffixIndex]
        self.firstList.scrollTo(self.firstIndex - 2)
        self._restoreIndices(oldIndices)
        self.prefixList.scrollTo(self.prefixIndex - 2)
        self._restoreIndices(oldIndices)
        self.suffixList.scrollTo(self.suffixIndex - 2)
        self._restoreIndices(oldIndices)

    def _getName(self):
        newName = ''
        if self.mode == self.__MODE_TYPEANAME:
            newName = self.nameEntry.get()
            newName = TextEncoder().decodeText(newName)
            newName = newName.strip()
            newName = TextEncoder().encodeWtext(newName)
        else:
            newName += self.names[0]
            if len(newName) > 0 and len(self.names[1]) > 0:
                newName += ' '
            newName += self.names[1]
            if len(newName) > 0 and len(self.names[2]) > 0:
                newName += ' '
            newName += self.names[2]
            if self.names[2] in PL.PirateNames_LastNamePrefixesCapped:
                newName += self.names[3].capitalize()
            else:
                newName += self.names[3]
        return newName

    def updateName(self):
        self.pirateName['text'] = self._getName()

    def _restoreIndices(self, indices):
        self.nicknameIndex = indices[0]
        self.firstIndex = indices[1]
        self.prefixIndex = indices[2]
        self.suffixIndex = indices[3]

    def enableList(self, listToEnable):
        listToEnable.show()
        listToEnable.decButton['state'] = 'normal'
        listToEnable.incButton['state'] = 'normal'

    def disableList(self, listToDisable):
        listToDisable.decButton['state'] = 'disabled'
        listToDisable.incButton['state'] = 'disabled'
        for item in listToDisable['items']:
            if item.__class__.__name__ != 'str':
                item.hide()

    def unload(self):
        self.nicknameCheck.destroy()
        self.nicknameList.destroy()
        if self.independent:
            self.mainFrame.destroy()
        elif self.nameEntry:
            self.nameEntry.destroy()
            self.nameEntryGuidelines.destroy()
            if self.cr:
                self.nameEntryGuidelinesURL.destroy()
        del self.main
        del self.parent
        del self.avatar
        del self.fsm

    def reset(self):
        for item in self.nicknameList['items'] + self.firstList['items'] + self.prefixList['items'] + self.suffixList['items']:
            if item.__class__.__name__ != 'str':
                item.destroy()

        self.nicknameIndex = 2
        self.firstIndex = 2
        self.prefixIndex = 2
        self.suffixIndex = 2
        self.nicknameList.index = 0
        self.firstList.index = 0
        self.prefixList.index = 0
        self.suffixList.index = 0

    def showPickAName(self):
        self.nameFrameTitle.show()
        for elt in self.pickANameGui:
            if elt != self.nicknameHigh and elt != self.firstHigh and elt != self.prefixHigh and elt != self.suffixHigh:
                elt.show()

    def hasCustomName(self):
        return self.customName

    def showTypeAName(self):
        self.customName = True
        self.nameFrameTitle.show()
        for elt in self.typeANameGui:
            elt.show()

    def hide(self):
        self.nameFrameTitle.hide()
        for elt in self.pickANameGui:
            elt.hide()

        for elt in self.typeANameGui:
            elt.hide()

    def makeRandomName(self):
        if self.customName and not self.independent:
            return
        if self.getDNA().getGender() == 'f':
            self.nicknameIndex = ''
            self.firstIndex = random.choice(range(len(self.firstNamesFemale) - 4)) + 2
            self.prefixIndex = random.choice(range(len(self.lastPrefixesFemale) - 4)) + 2
            self.suffixIndex = random.choice(range(len(self.lastSuffixesFemale) - 4)) + 2
        else:
            self.nicknameIndex = ''
            self.firstIndex = random.choice(range(len(self.firstNamesMale) - 4)) + 2
            self.prefixIndex = random.choice(range(len(self.lastPrefixesMale) - 4)) + 2
            self.suffixIndex = random.choice(range(len(self.lastSuffixesMale) - 4)) + 2
        nameCombo = random.choice(self.POSSIBLE_NAME_COMBOS.keys())
        self.nicknameActive, self.firstActive, self.lastActive = self.POSSIBLE_NAME_COMBOS[nameCombo]
        self._updateGuiToPickAName([self.nicknameActive, self.firstActive, self.lastActive], [
         0, self.firstIndex, self.prefixIndex, self.suffixIndex])

    def _updateGuiToPickAName(self, actives, indices):
        self.nicknameActive, self.firstActive, self.lastActive = actives
        nickname, self.firstIndex, self.prefixIndex, self.suffixIndex = indices
        if self.listsCreated:
            self._updateLists()
            self._updateCheckBoxes()
        else:
            if self.getDNA().getGender() == 'f':
                self.names[0] = ''
                self.names[1] = self.firstNamesFemale[self.firstIndex]
                self.names[2] = self.lastPrefixesFemale[self.prefixIndex]
                self.names[3] = self.lastSuffixesFemale[self.suffixIndex]
            else:
                self.names[0] = ''
                self.names[1] = self.firstNamesMale[self.firstIndex]
                self.names[2] = self.lastPrefixesMale[self.prefixIndex]
                self.names[3] = self.lastSuffixesMale[self.suffixIndex]
            self.notify.debug('random name blindly generated:%s' % self._getName())

    def decipherName(self, name):
        nameParts = name.split()
        if len(nameParts) == 1:
            self.nicknameEnabled = 0
            nameInFirst = self.__checkForNameInFirstList(nameParts[0])
            nameInLast = self.__checkForNameInLastList(nameParts[0])
            if not (nameInFirst or nameInLast):
                self.__assignNameToTyped(name)
                return
        elif len(nameParts) == 2:
            if self.__checkForNameInNicknameList(nameParts[0]):
                nameInFirst = self.__checkForNameInFirstList(nameParts[1])
                nameInLast = self.__checkForNameInLastList(nameParts[1])
                if not (nameInFirst or nameInLast):
                    self.__assignNameToTyped(name)
                    return
            else:
                nameInFirst = self.__checkForNameInFirstList(nameParts[0])
                nameInLast = self.__checkForNameInLastList(nameParts[1])
                if not (nameInFirst and nameInLast):
                    self.__assignNameToTyped(name)
                    return
        elif len(nameParts) == 3:
            nameInNick = self.__checkForNameInNicknameList(nameParts[0])
            nameInFirst = self.__checkForNameInFirstList(nameParts[1])
            nameInLast = self.__checkForNameInLastList(nameParts[2])
            if not (nameInNick and nameInFirst and nameInLast):
                self.__assignNameToTyped(name)
                return
        else:
            self.__assignNameToTyped(name)
            return
        self.mode = self.__MODE_PICKANAME
        self._updateLists()
        self._updateCheckBoxes()

    def __checkForNameInNicknameList(self, name):
        if self.getDNA().getGender() == 'f':
            nicknameTextList = self.nicknamesFemale
        else:
            nicknameTextList = self.nicknamesMale
        if nicknameTextList.__contains__(name):
            self.nicknameEnabled = 1
            self.nicknameIndex = nicknameTextList.index(name)
            return True
        else:
            self.nicknameEnabled = 0
            return False

    def __checkForNameInFirstList(self, name):
        if self.getDNA().getGender() == 'f':
            firstTextList = self.firstNamesFemale
        else:
            firstTextList = self.firstNamesMale
        if firstTextList.__contains__(name):
            self.firstEnabled = 1
            self.firstIndex = firstTextList.index(name)
            return True
        else:
            self.firstEnabled = 0
            return False

    def __checkForNameInLastList(self, name):
        if self.getDNA().getGender() == 'f':
            prefixTextList = self.lastPrefixesFemale
            suffixTextList = self.lastSuffixesFemale
        else:
            prefixTextList = self.lastPrefixesMale
            suffixTextList = self.lastSuffixesMale
        for prefix in prefixTextList:
            if prefix.strip() != '' and name.startswith(prefix) and suffixTextList.__contains__(name[len(prefix):]):
                self.lastEnabled = 1
                self.prefixIndex = prefixTextList.index(prefix)
                self.suffixIndex = suffixTextList.index(name[len(prefix):])
                return True

        self.lastEnabled = 0
        return False

    def __assignNameToTyped(self, name):
        self.nameEntry.enterText(name)
        self.mode = self.__MODE_TYPEANAME
        self.fsm.request('Pay')

    def nicknameToggle(self, value):
        self.nicknameActive = self.nicknameCheck['indicatorValue']
        self._listsChanged(0)
        if self.nicknameActive:
            self.nicknameList.refresh()
        self._updateCheckBoxes()

    def firstToggle(self, value):
        self.firstActive = self.firstCheck['indicatorValue']
        if not (self.firstActive or self.lastActive):
            self.firstActive = 1
            self.notify.debug(random.choice(PL.NameGUI_NoNameWarnings))
        self._listsChanged(1)
        if self.firstActive:
            self.firstList.refresh()
        self._updateCheckBoxes()

    def lastToggle(self, value):
        self.lastActive = self.lastCheck['indicatorValue']
        if not (self.firstActive or self.lastActive):
            self.lastActive = 1
            self.notify.debug(random.choice(PL.NameGUI_NoNameWarnings))
        self._listsChanged(2)
        self._listsChanged(3)
        if self.lastActive:
            self.prefixList.refresh()
            self.suffixList.refresh()
        self._updateCheckBoxes()

    def _updateCheckBoxes(self):
        self.nicknameCheck['indicatorValue'] = self.nicknameActive
        self.nicknameCheck['text'] = PL.NameGUI_CheckboxText[int(self.nicknameActive)]
        self.nicknameCheck.setIndicatorValue()
        self.firstCheck['indicatorValue'] = self.firstActive
        self.firstCheck['text'] = PL.NameGUI_CheckboxText[int(self.firstActive)]
        self.firstCheck.setIndicatorValue()
        self.lastCheck['indicatorValue'] = self.lastActive
        self.lastCheck['text'] = PL.NameGUI_CheckboxText[int(self.lastActive)]
        self.lastCheck.setIndicatorValue()

    def enterInit(self):
        pass

    def exitInit(self):
        pass

    def enterPay(self):
        if self.mode == self.__MODE_TYPEANAME:
            self.fsm.request('TypeAName')
        else:
            self.fsm.request('PickAName')

    def exitPay(self):
        pass

    def enterPickAName(self):
        if self.independent:
            self.randomButton.show()
        else:
            self.main.enableRandom()
        self.mode = self.__MODE_PICKANAME
        self.customName = False
        self.showPickAName()
        self._updateLists()
        self._updateCheckBoxes()

    def exitPickAName(self):
        if self.independent:
            self.randomButton.hide()
        self.hide()

    def enterTypeAName(self):
        self.mode = self.__MODE_TYPEANAME
        if not self.independent:
            self.main.disableRandom()
        self.typeANameButton.hide()
        self.showTypeAName()
        self.nameEntry['focus'] = 1

    def _typedAName(self, *args):
        self.nameEntry['focus'] = 0
        name = self.nameEntry.get()
        name = TextEncoder().decodeText(name)
        name = name.strip()
        name = TextEncoder().encodeWtext(name)
        self.nameEntry.enterText(name)
        self.notify.debug('Chosen name: %s' % self.nameEntry.get())
        problem = NameCheck.checkName(name, [self._checkNpcNames], font=self.nameEntry.getFont())
        if problem:
            print problem
            self.nameEntry.enterText('')
        else:
            self.fsm.request('Approved')

    def exitTypeAName(self):
        self.typeANameButton.show()
        self.hide()

    def enterApproved(self):
        self.fsm.request('Accepted')

    def exitApproved(self):
        pass

    def enterRejected(self):
        pass

    def exitRejected(self):
        pass

    def enterAccepted(self):
        pass

    def exitAccepted(self):
        pass

    def enterDone(self):
        self.notify.debug('Entering done state')
        if self.independent:
            self.save()
            messenger.send('NameGUIFinished', [1])
            return
        if self.getDNA().gender == 'm':
            self.savedMaleActiveStates = (
             self.nicknameActive, self.firstActive, self.lastActive)
            self.savedMaleName = [self.nicknameIndex, self.firstIndex, self.prefixIndex, self.suffixIndex]
            self.savedGender = 'm'
        elif self.getDNA().gender == 'f':
            self.savedFemaleName = [
             self.nicknameIndex, self.firstIndex, self.prefixIndex, self.suffixIndex]
            self.savedFemaleActiveStates = (self.nicknameActive, self.firstActive, self.lastActive)
            self.savedGender = 'f'

    def exitDone(self):
        pass

    def complete(self):
        self.nameEntry['focus'] = 0
        name = self.nameEntry.get()
        name = TextEncoder().decodeText(name)
        name = name.strip()
        name = TextEncoder().encodeWtext(name)
        self.nameEntry.enterText(name)
        self.notify.debug('Chosen name: %s' % name)
        if self.customName:
            problem = NameCheck.checkName(name, [self._checkNpcNames], font=self.nameEntry.getFont())
            if problem:
                print problem
                self.nameEntry.enterText('')
            else:
                self.fsm.request('Done')
        else:
            self.fsm.request('Done')

    def cancel(self):
        messenger.send('NameGUIFinished', [0])

    def getNumericName(self):
        nick = 0
        first = 0
        pre = 0
        suff = 0
        if self.firstActive:
            first = self.firstIndex
        if self.lastActive:
            pre = self.prefixIndex
            suff = self.suffixIndex
        return (
         nick, first, pre, suff)

    def findWidestInList(self, nameList):
        maxWidth = 0
        maxName = ''
        for name in nameList:
            width = self.text.calcWidth(name)
            if width > maxWidth:
                maxWidth = self.text.calcWidth(name)
                maxName = name

        print maxName + ' ' + str(maxWidth)
        return maxName

    def findWidestName(self):
        longestBoyTitle = self.findWidestInList(self.nicknamesMale[:])
        longestGirlTitle = self.findWidestInList(self.nicknamesFemale[:])
        longestBoyFirst = self.findWidestInList(self.firstNamesMale[:])
        longestGirlFirst = self.findWidestInList(self.firstNamesFemale[:])
        longestLastPrefix = self.findWidestInList(self.lastPrefixesFemale[:] + self.lastPrefixesMale[:])
        longestLastSuffix = self.findWidestInList(self.lastSuffixesFemale[:] + self.lastSuffixesMale[:])
        longestBoyName = longestBoyTitle + ' ' + longestBoyFirst + ' ' + longestLastPrefix + longestLastSuffix
        longestGirlName = longestGirlTitle + ' ' + longestGirlFirst + ' ' + longestLastPrefix + longestLastSuffix
        longestName = self.findWidestInList([longestBoyName, longestGirlName])
        return longestName

    def getDNA(self):
        if self.independent:
            return self.main.dna
        else:
            return self.main.pirate.style