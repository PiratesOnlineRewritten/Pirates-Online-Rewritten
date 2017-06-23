import time
import random
from pandac.PandaModules import *
from direct.showbase import DirectObject
from pirates.piratesbase import PiratesGlobals
from pirates.tutorial import TutorialGlobals
from pirates.piratesgui import NewTutorialPanel

class ChatTutorialAlt(DirectObject.DirectObject):
    notify = directNotify.newCategory('ChatTutorialAlt')

    def __init__(self):
        self.stage = 0
        self.panel1 = None
        self.panel2 = None
        self.panel3 = None
        self.panel4 = None
        self.panel5 = None
        self.panel6 = None
        self.contentPart1 = 'chat_tut_alt1'
        self.contentPart2 = 'chat_tut_alt2'
        self.contentPart3 = 'chat_tut_alt3'
        self.contentPart4 = 'chat_tut_alt4'
        self.contentPart5 = 'chat_tut_alt5'
        self.contentPart6 = 'chat_tut_alt6'
        self.showPart1()
        return

    def __handleOKButton(self):
        messenger.send('closeTutorialWindow')
        self.showPart2()

    def __handleOpenSpeedChatWindow(self):
        messenger.send('closeTutorialWindow')
        self.showPart3()

    def __handleSentSpeedChat(self):
        messenger.send('closeTutorialWindow')
        self.showPart4()

    def __handleOKButton1(self):
        messenger.send('closeTutorialWindow')
        self.showPart5()

    def __handleOKButton2(self):
        messenger.send('closeTutorialWindow')
        self.showPart6()

    def __handleOKButton3(self):
        base.localAvatar.guiMgr.profilePage.hide()
        self.updateTutorialState()
        self.panelCleanup()
        self.ignoreAll()
        self.destroy()

    def showPart1(self):
        self.panel1 = NewTutorialPanel.NewTutorialPanel([self.contentPart1, 'test1'])
        self.panel1.activate()
        self.panel1.setYesCommand(self.__handleOKButton)
        self.stage = 1

    def showPart2(self):
        if self.stage != 1:
            return
        self.panel2 = NewTutorialPanel.NewTutorialPanel([self.contentPart2])
        self.panel2.activate()
        self.acceptOnce('openedSpeedChat', self.__handleOpenSpeedChatWindow)
        self.stage = 2

    def showPart3(self):
        if self.stage != 2:
            return
        self.panel3 = NewTutorialPanel.NewTutorialPanel([self.contentPart3])
        self.panel3.activate()
        self.acceptOnce('sentSpeedChat', self.__handleSentSpeedChat)
        self.stage = 3

    def showPart4(self):
        if self.stage != 3:
            return
        self.panel4 = NewTutorialPanel.NewTutorialPanel([self.contentPart4, 'test2'])
        self.panel4.activate()
        self.panel4.setYesCommand(self.__handleOKButton1)
        self.stage = 4

    def showPart5(self):
        if self.stage != 4:
            return
        base.localAvatar.guiMgr.profilePage.showProfile(base.localAvatar.getDoId(), example=True)
        self.panel5 = NewTutorialPanel.NewTutorialPanel([self.contentPart5, 'test3'])
        self.panel5.activate()
        self.panel5.setYesCommand(self.__handleOKButton2)
        self.stage = 5

    def showPart6(self):
        if self.stage != 5:
            return
        self.panel6 = NewTutorialPanel.NewTutorialPanel([self.contentPart6, 'test4'])
        self.panel6.activate()
        self.panel6.setYesCommand(self.__handleOKButton3)
        self.stage = 6

    def updateTutorialState(self):
        base.localAvatar.b_setTutorial(PiratesGlobals.TUT_INTRODUCTION_TO_FRIENDS)

    def panelCleanup(self):
        messenger.send('closeTutorialWindowAll')

    def destroy(self):
        del self.stage
        del self.panel1
        del self.panel2
        del self.panel3
        del self.panel4
        del self.panel5
        del self.panel6
        del self.contentPart1
        del self.contentPart2
        del self.contentPart3
        del self.contentPart4
        del self.contentPart5
        del self.contentPart6

    def doNothing(self):
        pass