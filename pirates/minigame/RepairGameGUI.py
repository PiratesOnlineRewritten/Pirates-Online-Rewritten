import random
from pandac.PandaModules import NodePath, TextNode
from direct.gui.DirectGui import DirectFrame, DirectLabel
from direct.interval.IntervalGlobal import Sequence, Func, Parallel, LerpPosInterval, Wait, LerpColorScaleInterval
from pandac.PandaModules import TextPropertiesManager, TextProperties
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GUIFactory
from pirates.minigame.DistributedRepairGameBase import AT_SEA, ON_LAND
from pirates.piratesbase import PiratesGlobals
from RepairGamePickerGUI import RepairGamePickerGUI
import RepairGlobals

class RepairGameGUI(DirectFrame):
    completeSound = None
    guiDownSound = None
    guiUpSound = None
    shipRepairMusic = None

    def __init__(self, repairGame):
        DirectFrame.__init__(self, parent=base.a2dBackground, relief=None)
        self.repairGame = repairGame
        base.loadingScreen.beginStep('Sound', 1, 10)
        self._initSound()
        base.loadingScreen.endStep('Sound')
        base.loadingScreen.beginStep('GUI', 1, 43)
        self._initGUI()
        base.loadingScreen.endStep('GUI')
        self.accept('clientLogout', self.handleExitGame)
        if base.localAvatar.guiMgr.seaChestActive:
            base.localAvatar.guiMgr.hideSeaChest()
        if base.localAvatar.guiMgr.minimap:
            base.localAvatar.guiMgr.hideMinimap()
        self.accept('seachestOpened', self.handleExitGame)
        self.accept('avatarDetailsOpened', self.handleExitGame)
        self.accept('minimapOpened', self.handleExitGame)
        self.setBin('fixed', 30)
        self.setZ(-0.2)
        base.loadingScreen.beginStep('Intervals')
        self._initIntervals()
        base.loadingScreen.endStep('Intervals')
        return

    def _initSound(self):
        if not self.completeSound:
            RepairGameGUI.completeSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_GENERAL_CYCLECOMPLETE)
            RepairGameGUI.guiDownSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_GENERAL_GUIDOWN)
            RepairGameGUI.guiUpSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_GENERAL_GUIUP)
            RepairGameGUI.guiDownSound.setVolume(0.5)
            RepairGameGUI.guiUpSound.setVolume(0.5)
            RepairGameGUI.shipRepairMusic = [
             SoundGlobals.MUSIC_PERFORMERS_02, SoundGlobals.MUSIC_PERFORMERS_07, SoundGlobals.MUSIC_PERFORMERS_09]
        base.musicMgr.request(random.choice(self.shipRepairMusic), priority=1, volume=0.5)

    def _initGUI(self):
        self.model = loader.loadModel('models/gui/pir_m_gui_srp_main')
        self.repairGamePicker = RepairGamePickerGUI(self, self.repairGame, self.model.find('**/group_picker'))
        self.staticElements = GUIFactory.generateStaticElements(self.model.getChild(0), self)
        self.textElements = {}
        self.textElements['title'] = DirectLabel(text='', text_fg=(1.0, 1.0, 1.0, 1.0), text_shadow=(0.0, 0.0, 0.0, 1.0), scale=(0.0875, 0.0875, .0875), pos=(0.0, 0.0, 0.91), relief=None, textMayChange=1, text_font=PiratesGlobals.getPirateFont(), parent=self.staticElements['bg'])
        self.textElements['tutorial'] = DirectLabel(text='', text_fg=(1.0, 1.0, 1.0, 1.0), text_shadow=(0.0, 0.0, 0.0, 1.0), text_wordwrap=14, scale=(0.045, 0.045, 0.045), pos=(0.0, 0.0, 0.795), relief=None, textMayChange=1, text_font=PiratesGlobals.getPirateFont(), parent=self.staticElements['bg'])
        self.textElements['level'] = DirectLabel(text='', text_fg=(1.0, 1.0, 1.0, 1.0), scale=(0.0525, 0.0525, 0.0525), pos=(0.315, 0.0, 0.7), relief=None, textMayChange=1, text_align=TextNode.ARight, text_font=PiratesGlobals.getPirateFont(), parent=self.staticElements['bg'])
        self.textElements['level'].stash()
        self.textElements['idleMessage'] = DirectLabel(text='', text_fg=(1.0, 1.0, 1.0, 1.0), text_shadow=(0.0, 0.0, 0.0, 1.0), text_wordwrap=15, scale=(0.0875, 0.0875, 0.0875), pos=(0.0, 0.0, 0.0), relief=None, textMayChange=1, text_font=PiratesGlobals.getPirateFont(), parent=self.staticElements['bg'])
        self.textElements['cycleCompleteMessage'] = DirectLabel(text='', text_fg=(1.0,1.0, 1.0, 1.0), text_shadow=(0.0, 0.0, 0.0,1.0), text_wordwrap=20, scale=(0.0875,   0.0875,   0.0875), pos=(0.0, 0.0, 0.0), relief=None, textMayChange=1, text_font=PiratesGlobals.getPirateFont(), parent=self.staticElements['bg'])
        self.closeButton = GuiButton(image=(self.model.find('**/esc_button/idle'), self.model.find('**/esc_button/over'), self.model.find('**/esc_button/over'), self.model.find('**/esc_button/idle')), image_scale=(0.75, 0.75, 0.75), image_pos=(0.075, 0, 0.08), hotkeys=['Escape'], hotkeyLabel=PLocalizer.Minigame_Repair_Leave_Game_Text, pos=(-0.4, 0.0, 0.01), parent=base.a2dBottomRight, command=self.handleExitGame)
        self.closeButton.setBin('background', -90)
        self.model.removeNode()
        del self.model
        return

    def setPickerOutroStartPos(self):
        self.pickerOutroLerp.setStartPos(self.repairGamePicker.getPos())

    def setBGOutroStartPos(self):
        self.bgOutroLerp.setStartPos(self.staticElements['bg'].getPos())

    def _initIntervals(self):
        self.bgIntroLerp = LerpPosInterval(self.staticElements['bg'], duration=1.0, pos=self.staticElements['bg'].getPos(), startPos=(0.0, 0.0, 2.0))
        self.pickerIntroLerp = LerpPosInterval(self.repairGamePicker, duration=1.0, pos=self.repairGamePicker.getPos(), startPos=(0.0, 0.0, -1.0))
        self.introSequence = Sequence(Func(self.repairGamePicker.setEnabled, False), Parallel(Sequence(Wait(0.25), Func(self.guiDownSound.play)), self.bgIntroLerp, self.pickerIntroLerp), Func(self.repairGamePicker.setEnabled, True), Func(self.repairGame.gameFSM.request, 'Idle'), name='RepairGame.introSequence')
        self.pickerOutroLerp = LerpPosInterval(self.repairGamePicker, duration=1.0, startPos=self.repairGamePicker.getPos(), pos=(0.0, 0.0, -1.0))
        self.bgOutroLerp = LerpPosInterval(self.staticElements['bg'], duration=1.0, startPos=self.repairGamePicker.getPos(), pos=(0.0, 0.0, 2.0))
        self.outroSequence = Sequence(Func(self.repairGamePicker.stashTab), Func(self.closeButton.stash), Parallel(Func(self.guiUpSound.play), Func(self.setPickerOutroStartPos), Func(self.setBGOutroStartPos), self.pickerOutroLerp, self.bgOutroLerp), Func(self.repairGame.cleanup), name='RepairGame.outroSequence')
        self.cycleCompleteSequence = Sequence(Func(self.showCycleCompleteMessage), Func(self.repairGamePicker.stashTab), Wait(self.getCycleCompleteWaitTime()), Func(self.completeSound.play), Func(self.hideCycleCompleteMessage), LerpPosInterval(self.repairGamePicker, duration=0.5, pos=self.repairGamePicker.getPos() - (0, 0, 1.0)), Func(self.repairGame.resetMincroGameProgress), LerpPosInterval(self.repairGamePicker, duration=0.5, pos=self.repairGamePicker.getPos()), Func(self.repairGame.gameFSM.request, 'Idle'), name='RepairGame.cycleCompleteSequence')
        self.shakeSequence = Sequence(name='RepairGameGUI.shakeSequence')

    def handleExitGame(self):
        messenger.send('escape')

    def getCycleCompleteWaitTime(self):
        if self.repairGame.location == ON_LAND:
            return 5.5
        else:
            return 1.5

    def showCycleCompleteMessage(self):
        if self.repairGame.location == ON_LAND:
            tpMgr = TextPropertiesManager.getGlobalPtr()
            tpGold = TextProperties()
            tpGold.setTextColor(0.98, 0.76, 0, 1)
            tpMgr.setProperties('gold', tpGold)
            completionTime = self.repairGame.getCycleCompleteTime()
            seconds = completionTime % 60
            minutes = int(completionTime / 60.0)
            if minutes == 0:
                time = '\x01gold\x01%i %s\x02' % (seconds, PLocalizer.Minigame_Repair_Seconds)
            else:
                if seconds < 10:
                    time = '\x01gold\x01%i:0%i %s\x02' % (minutes, seconds, PLocalizer.Minigame_Repair_Minutes)
                else:
                    time = '\x01gold\x01%i:%i %s\x02' % (minutes, seconds, PLocalizer.Minigame_Repair_Minutes)
                goldAmount = self.repairGame.getReward(localAvatar.doId)
                goldBonus = self.repairGame.getGoldBonus()
                if goldBonus:
                    reward = PLocalizer.Minigame_Repair_GoldBonus % (str(goldAmount), str(goldBonus))
                reward = PLocalizer.Minigame_Repair_Gold % str(goldAmount)
            text = PLocalizer.Minigame_Repair_BenchOutro % (time, reward)
            self.textElements['cycleCompleteMessage'].setPos(0.0, 0.0, 0.35)
        else:
            text = PLocalizer.Minigame_Repair_ShipOutro
            self.textElements['cycleCompleteMessage'].setPos(0.0, 0.0, 0.15)
        self.textElements['cycleCompleteMessage']['text'] = text
        self.textElements['cycleCompleteMessage'].setText()

    def hideCycleCompleteMessage(self):
        self.textElements['cycleCompleteMessage']['text'] = ''
        self.textElements['cycleCompleteMessage'].setText()

    def showIdleMessage(self):
        if self.repairGame.location == ON_LAND:
            text = PLocalizer.Minigame_Repair_BenchIntro
            self.textElements['idleMessage'].setPos(0.0, 0.0, 0.35)
        else:
            text = PLocalizer.Minigame_Repair_ShipIntro
            self.textElements['idleMessage'].setPos(0.0, 0.0, 0.175)
        self.textElements['idleMessage']['text'] = text
        self.textElements['idleMessage'].setText()

    def hideIdleMessage(self):
        self.textElements['idleMessage']['text'] = ''
        self.textElements['idleMessage'].setText()

    def onShipDamaged(self, wasGrapeshot=False):
        if wasGrapeshot:
            shakeDelta = 0.05
            randomX = random.random() * 2 * shakeDelta - shakeDelta
            randomZ = random.random() * 2 * shakeDelta - shakeDelta
            if self.shakeSequence.isPlaying():
                self.shakeSequence.finish()
            self.shakeSequence = Parallel(Sequence(
              LerpColorScaleInterval(self, duration=0.5, colorScale=(1.0,0.2, 0.2, 1.0)), 
              LerpColorScaleInterval(self, duration=RepairGlobals.Common.guiShakeCooldownTime / 2.0, colorScale=(1.0, 1.0, 1.0, 1.0))), 
            Sequence(LerpPosInterval(self, duration=0.1, pos=self.getPos() - (randomX, 0.0, randomZ)), 
              LerpPosInterval(self, duration=0.2, pos=self.getPos() + (randomX, 0.0, randomZ)), 
              LerpPosInterval(self, duration=0.1, pos=self.getPos()), 
              Wait(RepairGlobals.Common.guiShakeCooldownTime)), name='RepairGameGUI.shakeSequence')
            self.shakeSequence.start()
        else:
            shakeDelta = 0.025
            randomX = random.random() * 2 * shakeDelta - shakeDelta
            randomZ = random.random() * 2 * shakeDelta - shakeDelta
            if not self.shakeSequence.isPlaying():
                self.shakeSequence = Sequence(
                  LerpPosInterval(self, duration=0.1, pos=self.getPos() - (randomX, 0.0, randomZ)), 
                  LerpPosInterval(self, duration=0.2, pos=self.getPos() + (randomX, 0.0, randomZ)), 
                  LerpPosInterval(self, duration=0.1, pos=self.getPos()), 
                  Wait(RepairGlobals.Common.guiShakeCooldownTime), name='RepairGameGUI.shakeSequence')
                self.shakeSequence.start()

    def setTutorial(self, game, index=None):
        text = PLocalizer.Minigame_Tutorials[game]
        if index is not None:
            text = text[index]
        self.textElements['tutorial']['text'] = text
        self.textElements['tutorial'].setText()
        return

    def clearTutorial(self):
        self.textElements['tutorial']['text'] = ''
        self.textElements['tutorial'].setText()

    def setRepairTitle(self):
        self.setTitle('repair')

    def setTitle(self, game):
        text = (
         PLocalizer.Minigame_Repair_Names[game],)
        self.textElements['title']['text'] = text
        self.textElements['title'].setText()

    def clearTitle(self):
        self.textElements['title']['text'] = ''
        self.textElements['title'].setText()

    def setDifficulty(self, difficulty):
        self.textElements['level']['text'] = PLocalizer.Minigame_Repair_Level % str(difficulty + 1)
        self.textElements['level'].setText()

    def setReward(self, reward):
        self.currentReward = reward

    def setGames(self, gameList):
        self.repairGamePicker.setGames(gameList)

    def resetGames(self):
        self.repairGamePicker.setEnabled(True)

    def setProgress(self, gameIndex, percent):
        self.repairGamePicker.setProgress(gameIndex, percent)

    def updatePirateNamesPerMincrogame(self, avIds2CurrentGameIndex):
        self.repairGamePicker.updatePirateNamesPerMincrogame(avIds2CurrentGameIndex)

    def destroy(self):
        self.ignore('clientLogout')
        self.ignore('seachestOpened')
        self.ignore('avatarDetailsOpened')
        self.ignore('minimapOpened')
        self.introSequence.clearToInitial()
        self.outroSequence.clearToInitial()
        self.cycleCompleteSequence.clearToInitial()
        self.shakeSequence.clearToInitial()
        del self.introSequence
        del self.outroSequence
        del self.cycleCompleteSequence
        del self.shakeSequence
        self.closeButton.destroy()
        self.closeButton.removeNode()
        del self.closeButton
        GUIFactory.destroyDirectGUIDict(self.staticElements)
        del self.staticElements
        self.repairGamePicker.destroy()
        del self.repairGamePicker
        self.removeNode()