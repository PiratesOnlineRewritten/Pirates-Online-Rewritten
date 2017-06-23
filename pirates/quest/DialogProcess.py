from direct.showbase.PythonUtil import POD, makeTuple
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiButton
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.quest import QuestOffer
from pirates.quest.QuestPrereq import *
from pirates.effects import CombatEffect
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class DialogProcess(POD, DirectObject):
    DataSet = {'prereq': [],'dialogId': None,'delayCleanup': False}

    def avCanParticipate(self, av):
        for prereq in self.prereq:
            if not prereq.avIsReady(av):
                return False

        return True

    def avCanParticipateAI(self, av):
        for prereq in self.prereq:
            if not prereq.avIsReadyAI(av):
                return False

        return True

    def handleEscapeKey(self):
        pass

    def begin(self, npc, dialogId):
        self.accept('escape', self.handleEscapeKey)
        self.dialogId = dialogId
        self.npc = npc

    def end(self):
        self.ignore('escape')
        messenger.send('DialogProcessEnded')

    def cleanup(self):
        pass


class Prereq(DialogProcess):

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        self.end()


class NPCDialog(DialogProcess):
    DataSet = {'textId': None}

    def __getDialogText(self):
        return PLocalizer.DialogStringDict.get(self.dialogId).get(self.textId).get('dialog')

    def __getDialogEmotes(self):
        return PLocalizer.DialogStringDict.get(self.dialogId).get(self.textId).get('emotes')

    def __handleNextChatPage(self, pageNumber, elapsed):
        if pageNumber == base.localAvatar.guiMgr.dialogSubtitler.getNumChatPages() - 1:
            localAvatar.guiMgr.dialogSubtitler.confirmButton.hide()
            self.ignore('nextChatPage')
            self.end()
        else:
            self.__playAnimation(pageNumber)

    def __playAnimation(self, index):
        if self.animationIval:
            self.animationIval.finish()
            self.animationIval = None
        if self.dialogAnimSet:
            if len(self.dialogAnimSet) > index and self.dialogAnimSet[index]:
                self.npc.gameFSM.request('Emote')
                self.npc.playEmote(self.dialogAnimSet[index])
        return

    def cleanup(self):
        self.ignore('nextChatPage')
        self.ignore('doneChatPage')
        if self.dialogBox:
            self.dialogBox.removeNode()
        if self.nametagLabel:
            self.nametagLabel.destroy()

    def handleEscapeKey(self):
        localAvatar.guiMgr.dialogSubtitler.advancePageNumber()

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        self.animationIval = None
        self.dialogAnimSet = []
        self.defaultAnim = None
        self.dialogBox = loader.loadModel('models/gui/pir_m_gui_frm_questChat')
        self.dialogBox.reparentTo(aspect2d)
        self.dialogBox.setScale(25.5)
        self.dialogBox.setPos(-0.48, 0, -0.58)
        self.dialogBox.find('**/pointer_left').hide()
        self.dialogBox.find('**/pointer_none').hide()
        self.dialogBox.setBin('gui-fixed', 0)
        self.nametagLabel = DirectLabel(parent=aspect2d, relief=None, text=self.npc.getName(), text_font=PiratesGlobals.getPirateFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ARight, text_fg=PiratesGuiGlobals.TextFG8, text_scale=0.055, pos=(0.3, 0, -0.44))
        self.nametagLabel.setBin('gui-fixed', 1)
        dialogStr = self.__getDialogText() + '\x07'
        self.dialogAnimSet = self.__getDialogEmotes()
        localAvatar.guiMgr.dialogSubtitler.setPageChat(dialogStr)
        self.__playAnimation(0)
        if localAvatar.guiMgr.dialogSubtitler.getNumChatPages() == 1:
            self.__handleNextChatPage(0, 0)
        else:
            self.accept('nextChatPage', self.__handleNextChatPage)
            self.accept('doneChatPage', self.end)
        return

    def end(self):
        if self.animationIval:
            self.animationIval.finish()
            self.animationIval = None
        DialogProcess.end(self)
        return


class PlayerDialog(DialogProcess):
    DataSet = {'textId': 0}

    def __getDialogText(self):
        return PLocalizer.DialogStringDict.get(self.dialogId).get(self.textId).get('dialog')

    def __getDialogEmotes(self):
        return PLocalizer.DialogStringDict.get(self.dialogId).get(self.textId).get('emotes')

    def __handleNextChatPage(self, pageNumber, elapsed):
        if pageNumber == base.localAvatar.guiMgr.dialogSubtitler.getNumChatPages() - 1:
            localAvatar.guiMgr.dialogSubtitler.confirmButton.hide()
            self.ignore('nextChatPage')
            self.end()
        else:
            self.__playAnimation(pageNumber)

    def __playAnimation(self, index):
        if self.animationIval:
            self.animationIval.finish()
            self.animationIval = None
        if self.dialogAnimSet:
            if not self.defaultAnim:
                self.defaultAnim = self.npc.getCurrentAnim()
            if len(self.dialogAnimSet) > index and self.dialogAnimSet[index]:
                localAvatar.playEmote(self.dialogAnimSet[index])
        return

    def cleanup(self):
        self.ignore('nextChatPage')
        self.ignore('doneChatPage')
        localAvatar.guiMgr.dialogSubtitler.clearText()
        if self.dialogBox:
            self.dialogBox.removeNode()
        if self.nametagLabel:
            self.nametagLabel.destroy()

    def handleEscapeKey(self):
        localAvatar.guiMgr.dialogSubtitler.advancePageNumber()

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        self.animationIval = None
        self.dialogAnimSet = []
        self.defaultAnim = None
        self.dialogBox = loader.loadModel('models/gui/pir_m_gui_frm_questChat')
        self.dialogBox.reparentTo(aspect2d)
        self.dialogBox.setScale(25.5)
        self.dialogBox.setPos(-0.48, 0, -0.58)
        self.dialogBox.find('**/pointer_right').hide()
        self.dialogBox.find('**/pointer_none').hide()
        self.dialogBox.setBin('gui-fixed', 0)
        self.nametagLabel = DirectLabel(parent=aspect2d, relief=None, text=localAvatar.getName(), text_font=PiratesGlobals.getPirateFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG8, text_scale=0.055, pos=(-0.6, 0, -0.44))
        self.nametagLabel.setBin('gui-fixed', 1)
        dialogStr = self.__getDialogText() + '\x07'
        self.dialogAnimSet = self.__getDialogEmotes()
        localAvatar.guiMgr.dialogSubtitler.setPageChat(dialogStr)
        self.__playAnimation(0)
        if localAvatar.guiMgr.dialogSubtitler.getNumChatPages() == 1:
            self.__handleNextChatPage(0, 0)
        else:
            self.accept('nextChatPage', self.__handleNextChatPage)
            self.accept('doneChatPage', self.end)
        return


class StepChoice(DialogProcess):
    DataSet = {'choices': tuple()}

    def __getDialogChoiceText(self, stepId, index=0):
        from pirates.quest.DialogTree import DialogDict
        textId = DialogDict.get(self.npc.getUniqueId()).get(self.dialogId).get(stepId)[index].getTextId()
        if PLocalizer.DialogStringDict.get(self.dialogId).get(textId).has_key('choice'):
            return PLocalizer.DialogStringDict.get(self.dialogId).get(textId).get('choice')
        else:
            return PLocalizer.DialogStringDict.get(self.dialogId).get(textId).get('dialog')

    def highlightIcon(self, buttonIndex, event):
        self.choiceButtons[buttonIndex]['image_color'] = PiratesGuiGlobals.TextFG8

    def unhighlightIcon(self, buttonIndex, event):
        self.choiceButtons[buttonIndex]['image_color'] = PiratesGuiGlobals.TextFG2

    def buttonClicked(self, stepId):
        messenger.send('SwitchStep', [stepId])

    def handleEscapeKey(self):
        pass

    def displayStepChoices(self):
        from pirates.quest.DialogTree import DialogDict
        self.choiceLabels = []
        self.choiceButtons = []
        gui = loader.loadModel('models/gui/compass_main')
        choiceIcon = gui.find('**/icon_sphere')
        for i in range(len(self.choices)):
            index = 0
            process = DialogDict.get(self.npc.getUniqueId()).get(self.dialogId).get(self.choices[i])[index]
            while not isinstance(process, PlayerDialog):
                index += 1
                process = DialogDict.get(self.npc.getUniqueId()).get(self.dialogId).get(self.choices[i])[index]

            while not process.avCanParticipate(localAvatar):
                index += 1
                process = DialogDict.get(self.npc.getUniqueId()).get(self.dialogId).get(self.choices[i])[index]

            if process.avCanParticipate(localAvatar) and isinstance(process, PlayerDialog):
                choiceButton = GuiButton.GuiButton(parent=aspect2d, relief=None, text=self.__getDialogChoiceText(self.choices[i], index), text_font=PiratesGlobals.getPirateFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=None, text_align=TextNode.ALeft, text_scale=0.055, text0_fg=PiratesGuiGlobals.TextFG2, text1_fg=PiratesGuiGlobals.TextFG8, text2_fg=PiratesGuiGlobals.TextFG8, text3_fg=PiratesGuiGlobals.TextFG9, image=choiceIcon, image_scale=0.3, image_pos=(-0.05, 0, 0.007), geom=None, pos=(-1.15, 0, -0.48 - i * 0.075), command=self.buttonClicked, extraArgs=[self.choices[i]])
                choiceButton.setBin('gui-fixed', 1)
                choiceButton.bind(DGG.ENTER, self.highlightIcon, extraArgs=[i])
                choiceButton.bind(DGG.EXIT, self.unhighlightIcon, extraArgs=[i])
                self.choiceButtons.append(choiceButton)

        return

    def cleanUpStepChoices(self):
        for button in self.choiceButtons:
            button.destroy()

        self.choiceButtons = []

    def cleanup(self):
        self.cleanUpStepChoices()
        if self.dialogBox:
            self.dialogBox.removeNode()
            self.dialogBox = None
        return

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        self.dialogBox = loader.loadModel('models/gui/pir_m_gui_frm_questChat')
        self.dialogBox.reparentTo(aspect2d)
        self.dialogBox.setScale(25.5)
        self.dialogBox.setPos(-0.48, 0, -0.58)
        self.dialogBox.find('**/pointer_left').hide()
        self.dialogBox.find('**/pointer_right').hide()
        self.dialogBox.setBin('gui-fixed', 0)
        self.displayStepChoices()
        localAvatar.guiMgr.dialogSubtitler.confirmButton.hide()


class SwitchStep(DialogProcess):
    DataSet = {'stepId': 0}


class ExitDialog(DialogProcess):

    def begin(self, npc, dialogId):
        npc.requestExit()
        self.end()


class OfferQuest(DialogProcess):
    DataSet = {'questId': None}

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        self.acceptOnce('setDialogQuestOffer', self.__gotQuestOffer)
        npc.requestDialogQuestOffer(self.questId, dialogId)

    def __gotQuestOffer(self):

        def handleOption(option):
            if option == PLocalizer.Accept:
                self.npc.assignDialogQuestOffer()
            self.end()

        self.npc.showDialogQuestOffer()
        localAvatar.guiMgr.dialogSubtitler.setPageChat('', options=[PLocalizer.Decline, PLocalizer.Accept], callback=handleOption)

    def handleEscapeKey(self):
        pass


class AssignQuest(DialogProcess):
    DataSet = {'questId': None}

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        self.acceptOnce('setDialogQuestOffer', self.__gotQuestAssigned)
        npc.requestDialogQuestAssignment(self.questId, dialogId)

    def end(self):
        self.npc.cleanUpQuestDetails()
        DialogProcess.end(self)

    def __gotQuestAssigned(self):

        def handleOption(option):
            self.end()

        self.npc.showDialogQuestOffer()
        localAvatar.guiMgr.dialogSubtitler.setPageChat('', options=[PLocalizer.Accept], callback=handleOption)

    def handleEscapeKey(self):
        pass


class AdvanceQuest(DialogProcess):
    DataSet = {'questId': None}

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        npc.requestDialogQuestAdvancement(self.questId, dialogId)
        self.end()


class ShowGivenQuest(DialogProcess):

    def begin(self, npc, dialogId):
        npc.displayNewQuests()

    def handleEscapeKey(self):
        pass


class ShowRewards(DialogProcess):

    def begin(self, npc, dialogId):
        npc.showQuestRewards()
        self.end()


class HideRewards(DialogProcess):

    def begin(self, npc, dialogId):
        npc.hideQuestRewards()
        self.end()


class MakeNPCHostile(DialogProcess):
    DataSet = {'npcId': None}

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        npc.requestNPCHostile(self.npcId, dialogId)
        self.end()


class PlayCombatEffectOnNPC(DialogProcess):
    DataSet = {'effectId': None}

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        combatEffect = CombatEffect.CombatEffect(self.effectId, attacker=localAvatar)
        combatEffect.reparentTo(render)
        combatEffect.setPos(npc.getPos(render) + Point3(0, 0, 2.5))
        combatEffect.play()
        self.end()


class FadeOutGhost(DialogProcess):

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        npc.fadeOutGhost()
        self.end()


class Delay(DialogProcess):
    DataSet = {'duration': 0}

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        taskMgr.doMethodLater(self.duration, self.endWaitTask, 'endDialogProcess')

    def endWaitTask(self, task):
        self.end()

    def cleanup(self):
        taskMgr.remove('endDialogProcess')


class SwitchVisualModeNPC(DialogProcess):
    DataSet = {'mode': None,'skipHide': False}

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        npc.switchVisualMode(self.mode, self.skipHide)
        self.end()


class PlayNPCEmote(DialogProcess):
    DataSet = {'emoteId': None,'npcId': None}

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        if self.npcId:
            npcDoId = base.cr.uidMgr.getDoId(self.npcId)
            self.npc = base.cr.doId2do.get(npcDoId)
        self.npc.gameFSM.request('Emote')
        self.npc.playEmote(self.emoteId)
        self.end()


class PlayPlayerEmote(DialogProcess):
    DataSet = {'emoteId': None}

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        localAvatar.playEmote(self.emoteId)
        self.end()


class PlayerDrawPistolAndAim(DialogProcess):

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        weaponId = 2001
        from pirates.battle import Pistol
        localAvatar.dialogProp = Pistol.Pistol(weaponId)
        self.animIval = Sequence(localAvatar.dialogProp.getDrawIval(localAvatar), Func(localAvatar.loop, 'gun_aim_idle'), Func(self.end)).start()

    def end(self):
        if self.animIval:
            self.animIval.pause()
            self.animIval = None
        DialogProcess.end(self)
        return

    def cleanup(self):
        if localAvatar.dialogProp:
            localAvatar.dialogProp.detachNode()


class PlayerHidePistol(DialogProcess):

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        self.animIval = None
        if localAvatar.dialogProp:
            self.animIval = Sequence(localAvatar.dialogProp.getReturnIval(localAvatar), Func(localAvatar.loop, 'idle'), Func(self.end)).start()
        else:
            self.end()
        return

    def end(self):
        if self.animIval:
            self.animIval.pause()
            self.animIval = None
        localAvatar.dialogProp = None
        DialogProcess.end(self)
        return


class PlayChickenFly(DialogProcess):

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        self.npc.play('fly', startFrame=20)
        self.end()


class PlaySfx(DialogProcess):
    DataSet = {'sfxId': None}
    sfxList = {SoundGlobals.SFX_SKILL_CLEANSE: loadSfx(SoundGlobals.SFX_SKILL_CLEANSE)}

    def begin(self, npc, dialogId):
        DialogProcess.begin(self, npc, dialogId)
        sfx = self.sfxList.get(self.sfxId)
        base.playSfx(sfx, volume=0.75)
        self.end()