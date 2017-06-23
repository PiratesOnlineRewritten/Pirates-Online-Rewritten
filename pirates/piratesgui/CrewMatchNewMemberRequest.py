from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class CrewMatchNewMemberRequestButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewMatchNewMemberRequestButton)


class CrewMatchNewMemberRequest(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewMatchNewMemberRequest')

    def __init__(self, avId, avName, crewType, openCrew):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief=None, pos=(-0.6, 0, 0.47), image=guiMain.find('**/general_frame_e'), image_pos=(0.25,
                                                                                                                          0,
                                                                                                                          0.275), image_scale=0.25)
        self.initialiseoptions(CrewMatchNewMemberRequest)
        self.avId = avId
        self.avName = avName
        self.crewType = crewType
        self.openCrew = openCrew
        self.title = DirectLabel(parent=self, relief=None, text=PLocalizer.CrewMatchNewMemberRequestTitle, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), pos=(0.25,
                                                                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                                                                             0.42))
        nameArray = (
         '\x01CPOrangeHEAD\x01' + self.avName + '\x02', '\x01CPOrangeHEAD\x01' + self.avName + '\x02', '\x01CPOrangeOVER\x01' + self.avName + '\x02', '\x01CPOrangeHEAD\x01' + self.avName + '\x02')
        nameButton = DirectButton(parent=NodePath(), relief=None, text=nameArray, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, command=self.handleAvatarPress, extraArgs=[avId, avName])
        left, right, bottom, top = nameButton.getBounds()
        nameGFX = TextGraphic(nameButton, left, right, 0, 1)
        buttonName = '\x05' + self.avName + '\x05'
        buttonText = PLocalizer.CrewMatchNewMemberRequestMessage % buttonName
        tpMgr = TextPropertiesManager.getGlobalPtr()
        tpMgr.setGraphic(self.avName, nameGFX)
        del tpMgr
        textRender = TextNode('textRender')
        textRender.setFont(PiratesGlobals.getInterfaceFont())
        textRender.setTextColor(PiratesGuiGlobals.TextFG2)
        textRender.setAlign(TextNode.ACenter)
        textRender.setShadowColor(PiratesGuiGlobals.TextShadow)
        textRender.setWordwrap(11)
        textRender.setTabWidth(1.0)
        textRender.setShadow(0.08, 0.08)
        textRender.setText(buttonText)
        textNode = self.attachNewNode(textRender.generate())
        textNode.setScale(PiratesGuiGlobals.TextScaleLarge)
        textNode.setPos(0.25, 0, 0.325)
        self.bOk = CrewMatchNewMemberRequestButton(text=PLocalizer.CrewMatchNewMemberRequestYes, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = CrewMatchNewMemberRequestButton(text=PLocalizer.CrewMatchNewMemberRequestNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.accept('clientLogout', self.destroy)
        self.accept('destroyCrewMatchInvite', self.destroy)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('Esc')
        DirectFrame.destroy(self)

    def __handleOk(self):
        base.cr.crewMatchManager.requestNewMember(self.avId, self.avName, 1, self.crewType, self.openCrew)
        self.destroy()

    def __handleNo(self):
        base.cr.crewMatchManager.requestNewMember(self.avId, self.avName, 0, self.crewType, self.openCrew)
        self.destroy()

    def handleAvatarPress(self, avId, avName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)