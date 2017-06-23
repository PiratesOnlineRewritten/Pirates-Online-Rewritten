import sys
import os
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton
from pirates.piratesgui.CheckBox import CheckBox
from direct.gui.DirectCheckBox import DirectCheckBox
from pirates.piratesgui import PNameTumbler
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.distributed import InteractGlobals
try:
    import embedded
    hasEmbedded = 1
except ImportError:
    hasEmbedded = 0

class FeedbackConfirmButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(FeedbackConfirmButton)


class FeedbackCancelButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(FeedbackCancelButton)


class FeedbackAccountButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command, 1.85)
        self.initialiseoptions(FeedbackAccountButton)


class FeedbackInput(GuiPanel.GuiPanel):

    def __init__(self, commandToExe):
        currentInteraction = base.cr.interactionMgr.getCurrent()
        if not hasattr(currentInteraction, 'storeType'):
            GuiPanel.GuiPanel.__init__(self, '', 0.735, 0.47, 0, '', pos=(0.43, 0, -0.72))
        elif currentInteraction.storeType in [InteractGlobals.ACCESSORIES_STORE, InteractGlobals.CATALOG_STORE, InteractGlobals.TATTOO_STORE, InteractGlobals.JEWELRY_STORE, InteractGlobals.BARBER_STORE]:
            GuiPanel.GuiPanel.__init__(self, '', 0.735, 0.47, 0, '', pos=(-1.22, 0, -0.72))
        else:
            GuiPanel.GuiPanel.__init__(self, '', 0.735, 0.47, 0, '', pos=(0.43, 0, -0.72))
        self.commandToExe = commandToExe
        self.accept('clientLogout', self.destroy)
        self.accept('destroyFeedbackPanel', self.destroy)

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    def generateFeedbackPanel(self, commandToExe):
        self.feedbackInput = DirectEntry(parent=self, relief=DGG.GROOVE, scale=0.051, pos=(0.007,
                                                                                           0,
                                                                                           0.42), borderWidth=PiratesGuiGlobals.BorderWidth, frameColor=(0,
                                                                                                                                                         0.0,
                                                                                                                                                         0.0,
                                                                                                                                                         0.5), text_align=TextNode.ALeft, width=14, numLines=9, focus=1, cursorKeys=1, text_fg=(1,
                                                                                                                                                                                                                                                1,
                                                                                                                                                                                                                                                1,
                                                                                                                                                                                                                                                1), command=self.commandToExe, suppressKeys=1, suppressMouse=1, autoCapitalize=0)
        return self.feedbackInput


class FeedbackPanel(GuiPanel.GuiPanel):
    notify = DirectNotifyGlobal.directNotify.newCategory('FeedbackPanel')

    def __init__(self):
        if hasattr(base, 'localAvatar'):
            if base.localAvatar.guiMgr.feedbackFormActive:
                return
            else:
                base.localAvatar.guiMgr.feedbackFormActive = True
        title = PLocalizer.FeedbackFormTitle
        self.hasEmbedded = hasEmbedded
        currentInteraction = base.cr.interactionMgr.getCurrent()
        if not hasattr(currentInteraction, 'storeType'):
            GuiPanel.GuiPanel.__init__(self, title, 0.79, 1.15, 0, 1.5, pos=(0.4, 0, -0.83))
        elif currentInteraction.storeType in [InteractGlobals.ACCESSORIES_STORE, InteractGlobals.CATALOG_STORE, InteractGlobals.TATTOO_STORE, InteractGlobals.JEWELRY_STORE, InteractGlobals.BARBER_STORE]:
            GuiPanel.GuiPanel.__init__(self, title, 0.79, 1.15, 0, 1.5, pos=(-1.25, 0, -0.83))
        else:
            GuiPanel.GuiPanel.__init__(self, title, 0.79, 1.15, 0, 1.5, pos=(0.4, 0, -0.83))
        self.initialiseoptions(FeedbackPanel)
        self.charGui = loader.loadModel('models/gui/char_gui')
        message = PLocalizer.FeedbackFormMessage
        self.message = DirectLabel(parent=self, relief=None, text=message, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=10, pos=(0.2225,
                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                         0.93), textMayChange=1)
        self.categoryItems = PLocalizer.FeedbackFormCatItems
        self.categoryItems.sort()
        self.tumbler = PNameTumbler.PNameTumbler(self.categoryItems, '')
        self.tumbler.reparentTo(self)
        self.tumbler.setPos(0.578, 0, 0.9)
        self.tumbler.setScale(0.75)
        self.feedbackObj = FeedbackInput(self._typedAComment)
        self.feedbackInput = self.feedbackObj.generateFeedbackPanel(self._typedAComment)
        self.feedbackInput.reparentTo(self.feedbackObj)
        self.feedbackObj.setBin('gui-popup', 0)
        self.bOk = FeedbackConfirmButton(text=PLocalizer.FeedbackFormSend, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.075, 0, 0.025)
        self.bCancel = FeedbackCancelButton(text=PLocalizer.GenericConfirmCancel, command=self.__handleCancel)
        self.bCancel.reparentTo(self)
        self.bCancel.setPos(0.268, 0, 0.025)
        self.bManageAccount = FeedbackAccountButton(text=PLocalizer.FeedbackManageButton, command=self.__handleAccountWeb)
        self.bManageAccount.reparentTo(self)
        self.bManageAccount.setPos(0.54, 0, 0.025)
        self.accept('clientLogout', self.destroy)
        self.accept('destroyFeedbackPanel', self.destroy)
        return

    def destroy(self):
        if hasattr(base, 'localAvatar'):
            base.localAvatar.guiMgr.feedbackFormActive = False
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOk(self):
        base.cr.centralLogger.writeClientEvent('GUEST_FEEDBACK|%s|%s' % (self.tumbler.getName(), self.feedbackInput.get()))
        self.destroy()
        self.feedbackObj.destroy()

    def __handleCancel(self):
        self.feedbackObj.destroy()
        self.destroy()

    def __handleCancelFromAbove(self):
        self.feedbackObj.destroy()
        self.destroy()

    def __handleAccountWeb(self):
        base.popupBrowser(launcher.getValue('GAME_INGAME_MANAGE_ACCT'))
        self.feedbackObj.destroy()
        self.destroy()

    def _typedAComment(self, *args):
        self.feedbackInput['focus'] = 0
        name = self.feedbackInput.get()
        name = TextEncoder().decodeText(name)
        name = name.strip()
        name = TextEncoder().encodeWtext(name)
        self.feedbackInput.enterText(name)

    def _catSelect(self, item):
        print 'Item Selected is %s' % item