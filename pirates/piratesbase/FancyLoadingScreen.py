from panda3d.core import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.reputation import ReputationGlobals
from direct.showbase import DirectObject
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.gui import DirectGuiGlobals as DGG
from direct.task import Task
from direct.gui.DirectGui import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.world.LocationConstants import *
from otp.otpbase import OTPGlobals
import random

IDEALX = 1280
IDEALY = 1024
tutorialShots = [
 'models/gui/loadingScreen_12', 'models/gui/loadingScreen_16', 'models/gui/loadingScreen_33', 'models/gui/loadingScreen_34', 'models/gui/loadingScreen_35', 'models/gui/loadingScreen_36', 'models/gui/loadingScreen_37']
tutorialShots_MoveAim = [
 'models/gui/loadingScreen_33', 'models/gui/loadingScreen_36']
screenShots = [
 'models/gui/loadingScreen_01', 'models/gui/loadingScreen_02', 'models/gui/loadingScreen_05', 'models/gui/loadingScreen_06', 'models/gui/loadingScreen_07', 'models/gui/loadingScreen_08', 'models/gui/loadingScreen_09', 'models/gui/loadingScreen_10', 'models/gui/loadingScreen_11', 'models/gui/loadingScreen_12', 'models/gui/loadingScreen_13', 'models/gui/loadingScreen_14', 'models/gui/loadingScreen_15', 'models/gui/loadingScreen_16', 'models/gui/loadingScreen_17', 'models/gui/loadingScreen_18', 'models/gui/loadingScreen_19', 'models/gui/loadingScreen_20', 'models/gui/loadingScreen_21', 'models/gui/loadingScreen_22', 'models/gui/loadingScreen_24', 'models/gui/loadingScreen_25', 'models/gui/loadingScreen_26', 'models/gui/loadingScreen_27', 'models/gui/loadingScreen_28', 'models/gui/loadingScreen_29', 'models/gui/loadingScreen_30', 'models/gui/loadingScreen_31', 'models/gui/loadingScreen_32', 'models/gui/loadingScreen_34', 'models/gui/loadingScreen_46']
screenShots_Jungles = [
 'models/gui/loadingScreen_13']
screenShots_Swamps = [
 'models/gui/loadingScreen_18']
screenShots_Caves = [
 'models/gui/loadingScreen_32', 'models/gui/loadingScreen_30', 'models/gui/loadingScreen_31', 'models/gui/loadingScreen_26', 'models/gui/loadingScreen_27', 'models/gui/loadingScreen_29', 'models/gui/loadingScreen_28', 'models/gui/loadingScreen_22']
screenShots_WinterHoliday = [
 'models/gui/loadingScreen_38', 'models/gui/loadingScreen_39', 'models/gui/loadingScreen_40']
areaType_Jungles = {'1161798288.34sdnaik': 0,'1164141722.61sdnaik': 1,'1169592956.59sdnaik': 2,'1165004570.58sdnaik': 3,'1165009873.53sdnaik': 4,'1165009856.72sdnaik': 5,'1167857698.16sdnaik': 6,'1172209955.25sdnaik': 7}
areaType_Swamps = {'1169179552.88sdnaik': 0,'1161732578.06sdnaik': 1}
areaType_Caves = {'1164952144.06sdnaik': 0,'1165001772.05sdnaik': 1,'1158121765.09sdnaik': 2,'1167862588.52sdnaik': 3,'1168057131.73sdnaik': 4,'1164929110.98sdnaik': 5,'1172208344.92sdnaik': 6,'1245949184.0akelts': 7,'1235605888.0akelts': 8,'1228348366.44akelts': 9,'1245948731.45akelts': 10,'1245948708.12akelts': 11,'1245946851.97akelts': 12,'1245946794.3akelts': 13}
screenShot_Dinghy = 'models/gui/loadingScreen_08'
screenShot_Jail = 'models/gui/loadingScreen_12'
screenShot_Weapon = 'models/gui/loadingScreen_35'
screenShot_Cutlass = 'models/gui/loadingScreen_37'
screenShot_EnterGame = 'models/gui/loadingScreen_enter'
screenShot_ExitGame = 'models/gui/loadingScreen_exit'
screenShots_Locations = {
    LocationIds.ANVIL_ISLAND: ['models/gui/loadingScreen_01'],
    LocationIds.ISLA_CANGREJOS: ['models/gui/loadingScreen_02', 'models/gui/loadingScreen_10'],
    LocationIds.CUBA_ISLAND: ['models/gui/loadingScreen_05'],
    LocationIds.CUTTHROAT_ISLAND: ['models/gui/loadingScreen_06'],
    LocationIds.DEL_FUEGO_ISLAND: ['models/gui/loadingScreen_07'],
    LocationIds.DRIFTWOOD_ISLAND: ['models/gui/loadingScreen_09'],
    LocationIds.ISLA_PERDIDA: ['models/gui/loadingScreen_11'],
    LocationIds.KINGSHEAD_ISLAND: ['models/gui/loadingScreen_14'],
    LocationIds.OUTCAST_ISLE: ['models/gui/loadingScreen_19'],
    LocationIds.PORT_ROYAL_ISLAND: ['models/gui/loadingScreen_16'],
    LocationIds.RUMRUNNER_ISLE: ['models/gui/loadingScreen_17'],
    LocationIds.ISLA_TORMENTA: ['models/gui/loadingScreen_15'],
    LocationIds.TORTUGA_ISLAND: ['models/gui/loadingScreen_20'],
    LocationIds.ANVIL_CAVE_BARBOSA: ['models/gui/loadingScreen_22'],
    LocationIds.ISLA_AVARICIA: ['models/gui/loadingScreen_24'],
    LocationIds.ISLA_DE_PORC: ['models/gui/loadingScreen_25'],
    LocationIds.PORT_ROYAL_CAVE_A: ['models/gui/loadingScreen_32'],
    LocationIds.PORT_ROYAL_CAVE_B: ['models/gui/loadingScreen_30'],
    LocationIds.TORTUGA_CAVE: ['models/gui/loadingScreen_31'],
    LocationIds.DEL_FUEGO_CAVE_C: ['models/gui/loadingScreen_29'],
    LocationIds.DEL_FUEGO_CAVE_D: ['models/gui/loadingScreen_26'],
    LocationIds.DEL_FUEGO_CAVE_E: ['models/gui/loadingScreen_27'],
    LocationIds.TORMENTA_CAVE_B: ['models/gui/loadingScreen_28'],
    LocationIds.NASSAU_ISLAND: ['models/gui/loadingScreen_47'],
    LocationIds.ANTIGUA_ISLAND: ['models/gui/loadingScreen_48'],
    LocationIds.MADRE_DEL_FUEGO_ISLAND: ['models/gui/loacingScreen_49']
}
screenShots_WinterHolidayLocations = {LocationIds.DEL_FUEGO_ISLAND: ['models/gui/loadingScreen_38'],LocationIds.PORT_ROYAL_ISLAND: ['models/gui/loadingScreen_39'],LocationIds.TORTUGA_ISLAND: ['models/gui/loadingScreen_40']}
screenShot_Potions = 'models/gui/loadingScreen_41'
screenShot_BenchRepair = 'models/gui/loadingScreen_42'
screenShot_ShipRepair = 'models/gui/loadingScreen_43'
screenShot_CannonDefense = 'models/gui/loadingScreen_44'
screenShot_Fishing = 'models/gui/loadingScreen_45'

def getOceanHint():
    oceans = [
     'Windward_Passage', 'Brigand_Bay', 'Bloody_Bayou', 'Scurvy_Shallows', 'Blackheart_Strait', 'Salty_Flats', 'Mar_de_Plata', 'Smugglers_Run', 'The_Hinterseas', 'Dead_Mans_Trough', 'Leeward_Passage', 'Boiling_Bay', 'Mariners_Reef']
    ocean = random.choice(oceans)
    hints = PLocalizer.HintMap_Locations.get(ocean)
    if hints:
        hint = random.choice(hints)
    else:
        hint = random.choice(PLocalizer.Hints_General)
    return '%s:  %s' % (PLocalizer.LoadingScreen_Hint, hint)


def getGeneralHint():
    type = random.choice([0, 1])
    if base.cr.isPaid() == OTPGlobals.AccessVelvetRope and type == 1:
        hint = random.choice(PLocalizer.Hints_VelvetRope)
    else:
        hint = random.choice(PLocalizer.Hints_General)
    return hint


def getPrivateeringHint():
    hint = random.choice(PLocalizer.Hints_Privateering)
    return '%s:  %s' % (PLocalizer.LoadingScreen_Hint, hint)


def getHint(destId=None, level=None):
    if destId and level:
        type = random.choice([0, 1, 2])
        if type == 0:
            hints = PLocalizer.HintMap_Locations.get(destId)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        elif type == 1:
            hints = PLocalizer.HintMap_Levels.get(level)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        else:
            hint = getGeneralHint()
    elif destId and not level:
        type = random.choice([0, 1])
        if type == 0:
            hints = PLocalizer.HintMap_Locations.get(destId)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        else:
            hint = getGeneralHint()
    elif level and not destId:
        type = random.choice([0, 1])
        if type == 0:
            hints = PLocalizer.HintMap_Levels.get(level)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        else:
            hint = getGeneralHint()
    else:
        hint = getGeneralHint()
    return '%s:  %s' % (PLocalizer.LoadingScreen_Hint, hint)


class FancyLoadingScreen(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('LoadingScreen')

    def __init__(self, parent):
        DirectObject.DirectObject.__init__(self)
        self.debugMode = config.GetInt('loading-screen') == 2
        self.parent = parent
        self.state = False
        self.currScreenshot = None
        self.snapshot = None
        self.snapshotFrame = None
        self.snapshotFrameBasic = None
        self.currentTime = 0
        self.analyzeMode = False
        self.loadScale = 1.0
        self.unmappedTicks = []
        self.stepInfo = {}
        self.accept(base.win.getWindowEvent(), self.adjustSize)
        self.accept('tick', self.tick)
        self.currStage = 'unmapped'
        self.stagePercent = 0
        self.numObjects = 0
        self.currPercent = 0.0
        self.line = LineSegs()
        self.line.setColor((0, 0, 0, 1))
        self.line.setThickness(1)
        self.stageLabel = None
        self.currNum = 0
        self.overallPercent = 0
        self.lastPercent = 0
        self.topLock = aspect2dp.attachNewNode('topShift')
        self.root = self.topLock.attachNewNode('loadingScreenRoot')
        self.root.setZ(-1)
        self.root.stash()
        self.model = loader.loadModel('models/gui/pir_m_gui_gen_loadScreen.bam')
        self.model.setP(90)
        self.model.reparentTo(self.root)
        cm = CardMaker('backdrop')
        cm.setFrame(-10, 10, -10, 10)
        if self.debugMode:
            self.backdrop = self.root.attachNewNode(cm.generate())
            self.backdrop.setX(-1.5)
            self.backdrop.setZ(-1)
            self.backdrop.setScale(4)
            self.backdrop.setColor(0.5, 0.5, 0.5, 1)
            cm = CardMaker('loadingBarBase')
            cm.setFrame(-0.9, 0.9, 0.1, 0.5)
            self.loadingBarBacking = self.root.attachNewNode(cm.generate())
            self.loadingBarRoot = self.root.attachNewNode('loadingBarRoot')
            cm.setName('analysisBarBase')
            cm.setFrame(-0.9, 0.9, -0.5, -0.1)
            self.analysisBar = self.root.attachNewNode(cm.generate())
            self.analysisBarRoot = self.root.attachNewNode('analysisBarRoot')
            self.analysisBar.hide()
            self.analysisButtons = []
            self.enterToContinue = DirectLabel(parent=self.root, text='Press Shift To Continue', relief=None, text_scale=0.1, pos=(0,
                                                                                                                                   0,
                                                                                                                                   -0.9), text_align=TextNode.ACenter)
            self.enterToContinue.hide()
            self.stageLabel = DirectLabel(parent=self.root, text='', relief=None, text_scale=0.1, pos=(-1.25,
                                                                                                       0,
                                                                                                       0.75), text_align=TextNode.ALeft, textMayChange=1)
            self.tickLabel = DirectLabel(parent=self.root, text='', relief=None, text_scale=0.1, pos=(0.75,
                                                                                                      0,
                                                                                                      0.75), textMayChange=1)
            self.overallLabel = DirectLabel(parent=self.root, text='', relief=None, text_scale=0.1, pos=(0,
                                                                                                         0,
                                                                                                         -0.75), textMayChange=1)
        else:
            self.backdrop = loader.loadModel('models/gui/pir_m_gui_gen_loadScreen')
            self.backdrop.reparentTo(self.root)
            bg = self.backdrop.find('**/expandable_bg')
            bg.setScale(1000, 1, 1000)
            bg.flattenStrong()
            self.backdrop.find('**/loadbar_grey').setColorScale(0.15, 0.15, 0.15, 0.1)
            self.loadingBar = self.backdrop.find('**/loadbar')
            self.loadingBar.setColorScale(0.2, 0.6, 0.5, 1)
            self.loadingPlank = NodePathCollection()
            self.loadingPlank.addPath(self.backdrop.find('**/plank_loading_bar'))
            self.loadingPlank.addPath(self.backdrop.find('**/loadbar'))
            self.loadingPlank.addPath(self.backdrop.find('**/loadbar_frame'))
            self.loadingPlank.addPath(self.backdrop.find('**/loadbar_grey'))
            self.titlePlank = self.backdrop.find('**/plank_title')
            self.percentLabel = DirectLabel(text='0%', parent=self.root, relief=None, text_font=PiratesGlobals.getPirateFont(), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_scale=0.031, pos=(0,
                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                    -0.4445), textMayChange=1)
            self.loadingPlank.addPath(self.percentLabel)
            self.screenshot = self.backdrop.find('**/screenshot')
            copyGeom = self.loadingBar.find('**/+GeomNode').node().getGeom(0)
            format = copyGeom.getVertexData().getFormat()
            primitive = copyGeom.getPrimitive(0)
            data = GeomVertexData(self.screenshot.node().getGeom(0).getVertexData())
            data.setFormat(format)
            writer = GeomVertexWriter(data, 'texcoord')
            writer.setData2f(0, 0)
            writer.setData2f(1, 0)
            writer.setData2f(1, 1)
            writer.setData2f(0, 1)
            geom = Geom(data)
            geom.addPrimitive(primitive)
            self.screenshot.node().removeGeom(0)
            self.screenshot.node().addGeom(geom)
            self.titlePlankMiddle = self.backdrop.find('**/plank_title_middle_box')
            self.titlePlankLeft = self.backdrop.find('**/plank_title_left')
            self.titlePlankRight = self.backdrop.find('**/plank_title_right')
        self.loadingBarColors = [ ((i % 10 / 10.0 + 0.5) / 2.0, (i % 100 / 10 / 10.0 + 0.5) / 2.0, (i / 100 / 10.0 + 0.5) / 2.0, 1) for i in range(1000) ]
        random.shuffle(self.loadingBarColors)
        self.lastUpdateTime = globalClock.getRealTime()
        self.locationLabel = DirectLabel(parent=self.root, relief=None, text='', text_font=PiratesGlobals.getPirateOutlineFont(), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_scale=PiratesGuiGlobals.TextScaleTitleJumbo * 0.7, text_align=TextNode.ACenter, pos=(0.0,
                                                                                                                                                                                                                                                                                                         0.0,
                                                                                                                                                                                                                                                                                                         0.515), textMayChange=1)
        self.locationText = None
        self.hintLabel = DirectLabel(parent=self.root, relief=None, text='', text_font=PiratesGlobals.getPirateOutlineFont(), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_scale=PiratesGuiGlobals.TextScaleTitleJumbo * 0.5, text_align=TextNode.ACenter, pos=(0.0, 0.0, -0.62), text_wordwrap=30, textMayChange=1)
        self.hintText = None
        self.adImage = None
        self.allowLiveFlatten = ConfigVariableBool('allow-live-flatten')
        self.title_art = []
        self.tempVolume = []
        self.adjustSize(base.win)
        gsg = base.win.getGsg()
        if gsg:
            self.root.prepareScene(gsg)
        return

    def startLoading(self, expectedLoadScale):
        if not self.debugMode:
            self.loadingBar.setSx(0)
        self.loadScale = float(expectedLoadScale)
        self.currStage = 'unmapped'
        self.stagePercent = 0
        self.numObjects = 0
        self.currPercent = 0.0
        self.loadingStart = globalClock.getRealTime()
        self.currNum = 0
        self.overallPercent = 0
        self.lastPercent = 0
        self.stepNum = 0
        if self.debugMode:
            self.overallLabel['text'] = '0.0'
            self.stageLabel['text'] = self.currStage
        self.update()

    def beginStep(self, stageName, amt=0, percent=0.001):
        if not self.state:
            return
        if self.currStage != 'unmapped' and stageName != self.currStage:
            if __dev__ and self.debugMode:
                self.notify.error('step %s not finished when step %s was started!' % (self.currStage, stageName))
            else:
                self.notify.warning('step %s not finished when step %s was started!' % (self.currStage, stageName))
                return
        self.stepNum += 1
        if self.debugMode:
            stageColor = self.loadingBarColors[self.stepNum]
            self.stepInfo[stageName] = [
             globalClock.getRealTime() - self.loadingStart, 0.0, stageColor, [], self.lastPercent + self.stagePercent, percent, amt]
            self.stepCard = CardMaker('step-%s' % stageName)
            self.stepCard.setColor(stageColor)
            self.currPoly = NodePath('empty')
            self.stageLabel['text'] = stageName
            self.tickLabel['text'] = '0.0'
        self.currPercent = 0.0
        self.overallPercent = min(100.0 * self.loadScale, self.lastPercent + self.stagePercent)
        self.lastPercent = self.overallPercent
        self.currStage = stageName
        self.stagePercent = percent
        self.numObjects = amt
        self.currNum = 0
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

    def endStep(self, stageName):
        if self.currStage == 'unmapped':
            self.notify.warning('step %s was started before loading screen was enabled' % stageName)
            return
        if stageName != self.currStage:
            if __dev__ and self.debugMode:
                self.notify.error('step %s was active while step %s was trying to end!' % (self.currStage, stageName))
            else:
                return
        self.tick()
        if self.debugMode:
            stageInfo = self.stepInfo[self.currStage]
            stageInfo[1] = globalClock.getRealTime() - self.loadingStart - stageInfo[0]
            self.currPoly.detachNode()
            self.stepCard.setFrame(self.lastPercent / self.loadScale * 0.018 - 0.9, (self.lastPercent + self.stagePercent) / self.loadScale * 0.018 - 0.9, 0.1, 0.5)
            self.loadingBarRoot.attachNewNode(self.stepCard.generate())
            self.stageLabel['text'] = 'unmapped'
        self.currStage = 'unmapped'
        self.currPercent = 0.0

    def tick(self):
        if self.state == False or self.analyzeMode:
            return
        if self.debugMode:
            if self.currStage == 'unmapped':
                self.unmappedTicks.append(globalClock.getRealTime() - self.loadingStart)
            else:
                self.stepInfo[self.currStage][3].append(globalClock.getRealTime() - self.loadingStart)
        self.currNum += 1
        self.currPercent = min(1.0, self.currNum / float(self.numObjects + 1))
        self.overallPercent = min(100.0 * self.loadScale, self.lastPercent + self.currPercent * self.stagePercent)
        self.update()

    def destroy(self):
        taskMgr.remove('updateLoadingScreen')
        for part in (self.model, self.snapshot):
            if part is not None:
                tex = part.findTexture('*')
                if tex:
                    tex.releaseAll()
                part.removeNode()

        self.model = None
        self.snapshot = None
        if self.snapshotFrame:
            self.snapshotFrame.destroy()
        if self.snapshotFrameBasic:
            self.snapshotFrameBasic.destroy()
        if self.locationLabel:
            self.locationLabel.destroy()
        if self.hintLabel:
            self.hintLabel.destroy()
        if self.debugMode:
            self.stageLabel.destroy()
            self.tickLabel.destroy()
            self.overallLabel.destroy()
            self.enterToContinue.destroy()
            self.stageLabel = None
            self.tickLabel = None
            self.overallLabel = None
            self.enterToContinue = None
        self.ignoreAll()
        return

    def showTitleFrame(self):
        if base.config.GetBool('no-loading-screen', 0):
            return
        for part in self.title_art:
            part.show()

    def hideTitleFrame(self):
        for part in self.title_art:
            part.hide()

    def show(self, waitForLocation=False, disableSfx=True, expectedLoadScale=1.0):
        if self.state or base.config.GetBool('no-loading-screen', 0) or not self.locationLabel:
            return
        render.hide()
        render2d.hide()
        render2dp.hide()
        if not self.debugMode:
            self.loadingPlank.hide()
        self.root.unstash()
        self.root.showThrough()
        self.state = True
        gsg = base.win.getGsg()
        if gsg:
            gsg.setIncompleteRender(False)
        base.setTaskChainNetNonthreaded()
        self.allowLiveFlatten.setValue(1)
        self.startLoading(expectedLoadScale)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        base.refreshAds()
        taskMgr.add(self.update, 'updateLoadingScreen', priority=-100)
        if base.sfxManagerList and disableSfx:
            index = 0
            while index < len(base.sfxManagerList):
                sfx_manager = base.sfxManagerList[index]
                sfx_manager.setVolume(0.0)
                index += 1

        if base.appRunner:
            base.appRunner.notifyRequest('onLoadingMessagesStart')
        self.__setLocationText(self.locationText)
        self.__setHintText(self.hintText)
        if not waitForLocation:
            screenshot = random.choice(tutorialShots_MoveAim)
            self.__setLoadingArt(screenshot)

    def showHint(self, destId=None, ocean=False):
        if base.config.GetBool('no-loading-screen', 0) or not self.locationLabel:
            return
        if ocean:
            hint = getOceanHint()
        else:
            if hasattr(base, 'localAvatar'):
                totalReputation = 0
                level = base.localAvatar.getLevel()
                if totalReputation:
                    hint = getHint(destId, level)
                else:
                    hint = getHint(destId)
            else:
                hint = getHint()
            shipPVPIslands = [
             '1196970035.53sdnaik', '1196970080.56sdnaik']
            if destId in shipPVPIslands or ocean and base.localAvatar.getCurrentIsland() in shipPVPIslands:
                hint = getPrivateeringHint()
        if self.parent and base.localAvatar.style.getTutorial() == PiratesGlobals.TUT_MET_JOLLY_ROGER:
            hint = '%s:  %s' % (PLocalizer.LoadingScreen_Hint, PLocalizer.GeneralTip7)
        self.__setHintText(hint)

    def update(self, task=None):
        if not self.state or self.analyzeMode:
            return Task.cont
        realTime = globalClock.getRealTime()
        if realTime - self.lastUpdateTime < 0.1:
            return Task.cont
        self.currentTime += min(10, (realTime - self.lastUpdateTime) * 250)
        self.lastUpdateTime = realTime
        if self.debugMode:
            self.overallLabel['text'] = '%3.1f' % (self.overallPercent / self.loadScale)
            self.tickLabel['text'] = '%3.1f' % (self.currPercent * 100.0)
        else:
            self.percentLabel['text'] = '%d%%' % (self.overallPercent / self.loadScale)
        if self.currStage != 'unmapped':
            if self.debugMode:
                self.currPoly.detachNode()
                self.stepCard.setFrame(self.lastPercent / self.loadScale * 0.018 - 0.9, self.overallPercent / self.loadScale * 0.018 - 0.9, 0.2, 0.4)
                self.currPoly = self.loadingBarRoot.attachNewNode(self.stepCard.generate())
        if not self.debugMode:
            self.loadingBar.setSx(self.overallPercent / self.loadScale * 3.4)
            if self.overallPercent > 0:
                self.loadingPlank.show()
        base.eventMgr.doEvents()
        base.graphicsEngine.renderFrame()
        return Task.cont

    def hide(self, reallyHide=not config.GetInt('loading-screen', 0) == 2):
        if not self.state:
            return
        if not reallyHide:
            if not self.analyzeMode:
                self.loadingEnd = globalClock.getRealTime()
                self.accept('shift', self.hide, extraArgs=[1])
                self.enterToContinue.show()
                self.generateAnalysis()
            return
        self.cleanupLoadingScreen()
        if self.debugMode:
            self.enterToContinue.hide()
            self.ignore('shift')
        self.root.hide()
        self.root.stash()
        render2d.show()
        render2dp.show()
        render.show()
        base.graphicsEngine.renderFrame()
        self.state = False
        self.currentTime = 0
        self.locationText = None
        self.hintText = None
        self.currScreenshot = None
        gsg = base.win.getGsg()
        if gsg:
            gsg.setIncompleteRender(True)
            render.prepareScene(gsg)
            render2d.prepareScene(gsg)
        taskMgr.remove('updateLoadingScreen')
        self.allowLiveFlatten.clearValue()
        base.setTaskChainNetThreaded()
        if base.sfxManagerList:
            index = 0
            while index < len(base.sfxManagerList):
                sfx_manager = base.sfxManagerList[index]
                sfx_manager.setVolume(base.options.sound_volume)
                index += 1

        messenger.send('texture_state_changed')
        if base.appRunner:
            base.appRunner.notifyRequest('onLoadingMessagesStop')
        return

    def showTarget(self, targetId=None, ocean=False, jail=False, pickapirate=False, exit=False, potionCrafting=False, benchRepair=False, shipRepair=False, cannonDefense=False):
        if base.config.GetBool('no-loading-screen', 0):
            return
        if pickapirate:
            screenshot = screenShot_EnterGame
        elif exit:
            screenshot = screenShot_ExitGame
        elif ocean:
            screenshot = screenShot_Dinghy
        elif jail:
            screenshot = screenShot_Jail
        elif potionCrafting:
            screenshot = screenShot_Potions
        elif benchRepair:
            screenshot = screenShot_BenchRepair
        elif shipRepair:
            screenshot = screenShot_ShipRepair
        elif cannonDefense:
            screenshot = screenShot_CannonDefense
        elif base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_CUTLASS:
            screenshot = screenShot_Weapon
        elif base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_MET_JOLLY_ROGER:
            screenshot = screenShot_Cutlass
        elif base.cr.newsManager:
            if base.cr.newsManager.getHoliday(21):
                screenshot = screenShots_WinterHolidayLocations.get(targetId)
                if not screenshot:
                    screenshot = screenShots_Locations.get(targetId)
        else:
            screenshot = screenShots_Locations.get(targetId)

        if screenshot or areaType_Jungles.has_key(targetId):
            screenshot = random.choice(screenShots_Jungles)
        elif areaType_Swamps.has_key(targetId):
            screenshot = random.choice(screenShots_Swamps)
        elif areaType_Caves.has_key(targetId):
            screenshot = random.choice(screenShots_Caves)
        else:
            island = getParentIsland(targetId)
            screenshot = screenShots_Locations.get(island, [random.choice(screenShots)])[0]
        if len(screenshot) > 1 and not isinstance(screenshot, str):
            screenshot = random.choice(screenshot)
        self.__setLoadingArt(screenshot)
        if pickapirate:
            targetName = PLocalizer.LoadingScreen_PickAPirate
        elif exit:
            targetName = None
        elif ocean:
            targetName = PLocalizer.LoadingScreen_Ocean
        elif jail:
            targetName = PLocalizer.LoadingScreen_Jail
        else:
            targetName = PLocalizer.LocationNames.get(targetId)
        base.setLocationCode('Loading: %s' % targetName)
        if targetName is None:
            return
        if len(targetName):
            self.__setLocationText(targetName)

    def __setLoadingArt(self, screenshot):
        if self.currScreenshot:
            return
        if self.parent and hasattr(base, 'localAvatar') and base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_MET_JOLLY_ROGER and screenshot not in tutorialShots:
            screenshot = random.choice(tutorialShots)
        self.currScreenshot = loader.loadModel(screenshot).findAllTextures()[0]
        if not self.debugMode:
            self.screenshot.setTexture(self.currScreenshot)

    def __setLocationText(self, locationText):
        if self.debugMode:
            return
        self.locationText = locationText
        if not self.locationText:
            self.locationText = ''
            self.titlePlank.hide()
        if len(self.locationText) > 12:
            scaleFactor = len(self.locationText) / 12.0
            self.titlePlankMiddle.setSx(scaleFactor)
            self.titlePlankRight.setX(0.215 * scaleFactor - 0.215)
            self.titlePlankLeft.setX(-1 * (0.215 * scaleFactor - 0.215))
        else:
            self.titlePlankMiddle.setSx(1)
            self.titlePlankRight.setX(0)
            self.titlePlankLeft.setX(0)
        self.locationLabel['text'] = self.locationText
        if self.__isVisible() and len(self.locationText):
            self.locationLabel.show()
            self.titlePlank.show()
        else:
            self.locationLabel.hide()
            self.titlePlank.hide()
        launcher.setValue('gameLocation', self.locationText)

    def __setHintText(self, hintText):
        self.hintText = hintText
        if not self.hintText:
            self.hintText = ''
        self.hintLabel['text'] = self.hintText
        if self.__isVisible():
            self.hintLabel.show()

    def __isVisible(self):
        return self.state

    def scheduleHide(self, function):
        base.cr.queueAllInterestsCompleteEvent()
        self.acceptOnce(function, self.interestComplete)

    def interestComplete(self):
        self.endStep('scheduleHide')
        self.hide()

    def __setAdArt(self):
        return
        imageFrame = self.model.find('**/frame')
        randomImageNumber = random.randint(0, len(screenShots) - 1)
        imageFileName = screenShots[randomImageNumber]
        self.adImage = loader.loadModel(imageFileName)
        self.adImage.reparentTo(imageFrame)
        self.adImage.setScale(2.15 * 5, 1, 1.2 * 5)
        self.adImage.setPos(0, 0, 2.3)
        self.adImage.setBin('fixed', 1)
        if randomImageNumber == 0:
            urlToGet = 'http://log.go.com/log?srvc=dis&guid=951C36F8-3ACD-4EB2-9F02-8E8A0A217AF5&drop=0&addata=3232:64675:408091:64675&a=0'
            self.httpSession = HTTPClient()
            self.nonBlockHTTP = self.httpSession.makeChannel(False)
            self.nonBlockHTTP.beginGetDocument(DocumentSpec(urlToGet))
            instanceMarker = 'FunnelLoggingRequest-%s' % str(random.randint(1, 1000))
            self.startCheckingAsyncRequest(instanceMarker)

    def startCheckingAsyncRequest(self, name):
        taskMgr.remove(name)
        taskMgr.doMethodLater(0.5, self.pollAdTask, name)

    def pollAdTask(self, task):
        result = self.nonBlockHTTP.run()
        if result == 0:
            self.stopCheckingAdTask(task)
        else:
            return Task.again

    def stopCheckingAdTask(self, name):
        taskMgr.remove(name)

    def cleanupLoadingScreen(self):
        if self.debugMode:
            self.loadingBarRoot.get_children().detach()
            self.cleanupAnalysis()
            self.stepInfo = {}
            self.unmappedTicks = []

    def showInfo(self, stepName, pos):
        self.stageLabel['text'] = stepName
        info = self.stepInfo[stepName]
        self.tickLabel['text'] = '%s ticks(%s)' % (len(info[3]), info[6])
        self.overallLabel['text'] = '%3.2f seconds (%d%%)' % (info[1], 100 * info[1] / (self.loadingEnd - self.loadingStart))

    def generateAnalysis(self):
        if self.analyzeMode:
            self.cleanupAnalysis()
        self.analyzeMode = True
        cm = CardMaker('cm')
        self.analysisBar.show()
        loadingTime = self.loadingEnd - self.loadingStart
        for stepName in self.stepInfo:
            startTime, duration, color, ticks, startPercent, percent, expectedTicks = self.stepInfo[stepName]
            cm.setName(stepName)
            cm.setColor(color)
            cm.setFrame(startTime / loadingTime * 1.8 - 0.9, (startTime + duration) / loadingTime * 1.8 - 0.9, -0.5, -0.1)
            self.analysisBarRoot.attachNewNode(cm.generate())
            button = DirectFrame(parent=self.analysisBarRoot, geom=NodePath('empty'), image=NodePath('empty'), state=DGG.NORMAL, relief=None, frameSize=(startTime / loadingTime * 1.8 - 0.9, (startTime + duration) / loadingTime * 1.8 - 0.9, -0.5, -0.1))
            button.bind(DGG.ENTER, self.showInfo, extraArgs=[stepName])
            self.analysisButtons.append(button)
            button = DirectFrame(parent=self.analysisBarRoot, geom=NodePath('empty'), image=NodePath('empty'), state=DGG.NORMAL, relief=None, frameSize=(startPercent / self.loadScale / 100.0 * 1.8 - 0.9, (startPercent + percent) / self.loadScale / 100.0 * 1.8 - 0.9, 0.1, 0.5))
            button.bind(DGG.ENTER, self.showInfo, extraArgs=[stepName])
            self.analysisButtons.append(button)
            for tick in ticks:
                self.line.moveTo(VBase3(tick / loadingTime * 1.8 - 0.9, 0, -0.5))
                self.line.drawTo(VBase3(tick / loadingTime * 1.8 - 0.9, 0, -0.55))

        for tick in self.unmappedTicks:
            self.line.moveTo(VBase3(tick / loadingTime * 1.8 - 0.9, 0, -0.5))
            self.line.drawTo(VBase3(tick / loadingTime * 1.8 - 0.9, 0, -0.55))

        self.analysisSegs = self.analysisBarRoot.attachNewNode(self.line.create())
        return

    def cleanupAnalysis(self):
        for button in self.analysisButtons:
            button.destroy()

        self.analysisButtons = []
        self.analysisBarRoot.get_children().detach()
        self.analysisBar.hide()
        self.analyzeMode = False
        self.analysisSegs = None
        return

    def adjustSize(self, window):
        x = max(1, window.getXSize())
        y = max(1, window.getYSize())
        minSz = min(x, y)
        aspect = float(x) / y
        if x > y:
            self.topLock.setZ(1)
        else:
            self.topLock.setZ(float(y) / x)
        if minSz > IDEALX:
            self.topLock.setScale(IDEALX / float(x))
        elif minSz > IDEALY:
            self.topLock.setScale(IDEALY / float(y))
        else:
            self.topLock.setScale(1.0)
