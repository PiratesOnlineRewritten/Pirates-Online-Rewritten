import math
from direct.gui.DirectGui import DirectFrame, DGG
from direct.task import Task
from pirates.piratesgui import GUIFactory
from RepairGameButton import RepairGameButton

class RepairGamePickerGUI(DirectFrame):

    def __init__(self, parent, repairGame, model):
        DirectFrame.__init__(self, parent=parent, relief=None, sortOrder=40)
        self.repairGame = repairGame
        self.model = model
        self.gameIndicesToNames = {}
        self.staticElements = GUIFactory.generateStaticElements(self.model, self)
        self.buttons = GUIFactory.generateButtons(self.model, self, buttonClass=RepairGameButton, passNodePathToButton=True)
        self.staticElements['tab'].setBin('fixed', 31)
        self.staticElements['border1'].setBin('fixed', 33)
        self.staticElements['border2'].setBin('fixed', 33)
        self.staticElements['border3'].setBin('fixed', 33)
        self.staticElements['border4'].setBin('fixed', 33)
        self.staticElements['border5'].setBin('fixed', 33)
        self.stashTab()
        self.enabled = True
        return

    def onGameButtonSelected(self, button, index):
        if not self.repairGame.gameFSM or self.repairGame.gameFSM.state in ('Off',
                                                                            'Init',
                                                                            'CycleComplete',
                                                                            'Final',
                                                                            'Outro'):
            return
        for key, b in self.buttons.items():
            b.downStateNode.reparentTo(b.stateNodePath[1])
            b.disabledStateNode.reparentTo(b.stateNodePath[3])
            b.hideGlow()

        button.downStateNode.reparentTo(button.stateNodePath[3])
        button.disabledStateNode.detachNode()
        self.unstashTab()
        self.staticElements['tab'].setPos(button.getX(), 0.0, 0.0)
        self.repairGame.d_requestMincroGame(index)

    def stashTab(self):
        self.staticElements['tab'].stash()

    def unstashTab(self):
        self.staticElements['tab'].unstash()

    def setGames(self, gameList):
        gameNamesToIndices = {}
        for i in range(len(gameList)):
            gameName = self.repairGame.games[i].name
            self.gameIndicesToNames[i] = gameName.lower()
            gameNamesToIndices[gameName.lower()] = i

        keysToRemove = []
        for key, button in self.buttons.items():
            if key.lower() not in gameNamesToIndices:
                keysToRemove.append(key)
            else:
                button['extraArgs'] = [
                 button, gameNamesToIndices[key.lower()]]
                button['command'] = self.onGameButtonSelected

        for key in keysToRemove:
            self.buttons[key].destroy()
            self.buttons[key].removeNode()
            del self.buttons[key]

    def setEnabled(self, enabled):
        self.enabled = enabled
        if enabled:
            self.unstash()
            for key, button in self.buttons.items():
                button.showGlow()
                button.skillGlow.setColorScale(1.0, 1.0, 1.0, 0.0)

            self.totalTime = 0.0
            for i in range(len(self.repairGame.gameProgress)):
                self.setProgress(i, self.repairGame.gameProgress[i])

            self.totalTime = 0.0
            taskMgr.add(self.updateGui, 'RepairGameGUIUpdate')
        else:
            for key, button in self.buttons.items():
                button['state'] = DGG.DISABLED
                button.hideGlow()

            taskMgr.remove('RepairGameGUIUpdate')

    def updateGui(self, task):
        dt = globalClock.getDt()
        self.totalTime += dt * 1.25
        for i in range(self.repairGame.getGameCount()):
            offset = 0
            alphaVal = self.totalTime - offset - math.floor(self.totalTime - offset)
            if math.floor(self.totalTime - offset) % 2 == 1:
                alphaVal = 1.0 - alphaVal
            alphaVal = alphaVal * alphaVal
            self.buttons[self.gameIndicesToNames[i]].skillGlow.setColorScale(1.0, 1.0, 1.0, alphaVal)

        return Task.cont

    def setProgress(self, gameIndex, percent):
        self.buttons[self.gameIndicesToNames[gameIndex]].setProgress(percent)
        if percent >= 100:
            self.totalTime = 0.0
            for key, b in self.buttons.items():
                b.showGlow()
                b.skillGlow.setColorScale(1.0, 1.0, 1.0, 0.0)

        if percent != -1:
            self.buttons[self.gameIndicesToNames[gameIndex]]['state'] = DGG.DISABLED
        elif percent >= 1.0:
            self.buttons[self.gameIndicesToNames[gameIndex]].overStateNode.reparentTo(self.buttons[self.gameIndicesToNames[gameIndex]].stateNodePath[3])
            self.buttons[self.gameIndicesToNames[gameIndex]]['state'] = DGG.NORMAL
        else:
            self.buttons[self.gameIndicesToNames[gameIndex]]['state'] = DGG.NORMAL

    def updatePirateNamesPerMincrogame(self, avIds2CurrentGameIndex):
        for i in range(self.repairGame.getGameCount()):
            self.buttons[self.gameIndicesToNames[i]].updatePirateNameBox('')

        for k, v in avIds2CurrentGameIndex.iteritems():
            if k != localAvatar.doId:
                pirateName = ''
                handle = base.cr.identifyAvatar(k)
                if handle:
                    pirateName = handle.getName()
                self.buttons[self.gameIndicesToNames[v]].updatePirateNameBox(pirateName)

    def destroy(self):
        taskMgr.remove('RepairGameGUIUpdate')
        DirectFrame.destroy(self)
        for b in self.buttons:
            self.buttons[b].destroy()

        del self.buttons
        del self.repairGame