from panda3d.core import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.reputation import ReputationGlobals
from direct.showbase import DirectObject
from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.gui.DirectGui import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.world.LocationConstants import *
from otp.otpbase import OTPGlobals
import random
from pandac.PandaModules import HTTPClient
from pandac.PandaModules import HTTPCookie
from pandac.PandaModules import URLSpec
from pandac.PandaModules import Ramfile
from pandac.PandaModules import Ostream
from pandac.PandaModules import HTTPDate
from pandac.PandaModules import DocumentSpec
tutorialShots = [
 'models/gui/loadingScreen_12', 'models/gui/loadingScreen_16', 'models/gui/loadingScreen_33', 'models/gui/loadingScreen_34', 'models/gui/loadingScreen_35', 'models/gui/loadingScreen_36', 'models/gui/loadingScreen_37']
tutorialShots_MoveAim = [
 'models/gui/loadingScreen_33', 'models/gui/loadingScreen_36']
screenShots = [
 'models/gui/loadingScreen_01', 'models/gui/loadingScreen_02', 'models/gui/loadingScreen_05', 'models/gui/loadingScreen_06', 'models/gui/loadingScreen_07', 'models/gui/loadingScreen_08', 'models/gui/loadingScreen_09', 'models/gui/loadingScreen_10', 'models/gui/loadingScreen_11', 'models/gui/loadingScreen_12', 'models/gui/loadingScreen_13', 'models/gui/loadingScreen_14', 'models/gui/loadingScreen_15', 'models/gui/loadingScreen_16', 'models/gui/loadingScreen_17', 'models/gui/loadingScreen_18', 'models/gui/loadingScreen_19', 'models/gui/loadingScreen_20', 'models/gui/loadingScreen_21', 'models/gui/loadingScreen_22', 'models/gui/loadingScreen_24', 'models/gui/loadingScreen_25', 'models/gui/loadingScreen_26', 'models/gui/loadingScreen_27', 'models/gui/loadingScreen_28', 'models/gui/loadingScreen_29', 'models/gui/loadingScreen_30', 'models/gui/loadingScreen_31', 'models/gui/loadingScreen_32', 'models/gui/loadingScreen_34']
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
screenShots_Locations = {LocationIds.ANVIL_ISLAND: ['models/gui/loadingScreen_01'],LocationIds.ISLA_CANGREJOS: ['models/gui/loadingScreen_02', 'models/gui/loadingScreen_10'],LocationIds.CUBA_ISLAND: ['models/gui/loadingScreen_05'],LocationIds.CUTTHROAT_ISLAND: ['models/gui/loadingScreen_06'],LocationIds.DEL_FUEGO_ISLAND: ['models/gui/loadingScreen_07'],LocationIds.DRIFTWOOD_ISLAND: ['models/gui/loadingScreen_09'],LocationIds.ISLA_PERDIDA: ['models/gui/loadingScreen_11'],LocationIds.KINGSHEAD_ISLAND: ['models/gui/loadingScreen_14'],LocationIds.OUTCAST_ISLE: ['models/gui/loadingScreen_19'],LocationIds.PORT_ROYAL_ISLAND: ['models/gui/loadingScreen_16'],LocationIds.RUMRUNNER_ISLE: ['models/gui/loadingScreen_17'],LocationIds.ISLA_TORMENTA: ['models/gui/loadingScreen_15'],LocationIds.TORTUGA_ISLAND: ['models/gui/loadingScreen_20'],LocationIds.ANVIL_CAVE_BARBOSA: ['models/gui/loadingScreen_22'],LocationIds.ISLA_AVARICIA: ['models/gui/loadingScreen_24'],LocationIds.ISLA_DE_PORC: ['models/gui/loadingScreen_25'],LocationIds.PORT_ROYAL_CAVE_A: ['models/gui/loadingScreen_32'],LocationIds.PORT_ROYAL_CAVE_B: ['models/gui/loadingScreen_30'],LocationIds.TORTUGA_CAVE: ['models/gui/loadingScreen_31'],LocationIds.DEL_FUEGO_CAVE_C: ['models/gui/loadingScreen_29'],LocationIds.DEL_FUEGO_CAVE_D: ['models/gui/loadingScreen_26'],LocationIds.DEL_FUEGO_CAVE_E: ['models/gui/loadingScreen_27'],LocationIds.TORMENTA_CAVE_B: ['models/gui/loadingScreen_28']}
screenShots_WinterHolidayLocations = {LocationIds.DEL_FUEGO_ISLAND: ['models/gui/loadingScreen_38'],LocationIds.PORT_ROYAL_ISLAND: ['models/gui/loadingScreen_39'],LocationIds.TORTUGA_ISLAND: ['models/gui/loadingScreen_40']}
screenShot_Potions = 'models/gui/loadingScreen_41'
screenShot_BenchRepair = 'models/gui/loadingScreen_42'
screenShot_ShipRepair = 'models/gui/loadingScreen_43'
screenShot_CannonDefense = 'models/gui/loadingScreen_44'

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


class LoadingScreen(DirectObject.DirectObject):

    def __init__(self, parent):
        DirectObject.DirectObject.__init__(self)
        self.parent = parent
        self.state = False
        self.model = None
        self.wheel = None
        self.snapshot = None
        self.snapshotFrame = None
        self.snapshotFrameBasic = None
        self.currentTime = 0
        self.lastUpdateTime = globalClock.getRealTime()
        self.locationLabel = None
        self.locationText = None
        self.hintLabel = None
        self.hintText = None
        self.adImage = None
        self.allowLiveFlatten = ConfigVariableBool('allow-live-flatten')
        self.title_art = []
        self.tempVolume = []

    def startLoading(self):
        pass

    def beginStep(self, stageName, amt=0, percent=0):
        self.update()

    def endStep(self, stageName):
        self.update()

    def tick(self):
        self.update()

    def destroy(self):
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
        taskMgr.remove('updateLoadingScreen')
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
        if self.state or base.config.GetBool('no-loading-screen', 0):
            return
        self.startLoading()
        render.hide()
        self.state = True
        gsg = base.win.getGsg()
        if gsg:
            gsg.setIncompleteRender(False)
        base.setTaskChainNetNonthreaded()
        self.allowLiveFlatten.setValue(1)
        if base.config.GetBool('loading-screen-interstitial', 0):
            self.model = loader.loadModel('models/gui/loading_screen_interstitial')
            if self.model is not None:
                loadimage = self.model.find('**/loadimage')
                if loadimage is not None:
                    loadimage.hide()
        else:
            self.model = loader.loadModel('models/gui/loading_screen')

        self.locationLabel = DirectLabel(parent=aspect2dp, relief=None, text='', text_font=PiratesGlobals.getPirateOutlineFont(), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_scale=PiratesGuiGlobals.TextScaleTitleJumbo * 0.7, text_align=TextNode.ACenter, pos=(0.0, 0.0, -0.52), textMayChange=1)
        self.hintLabel = DirectLabel(parent=aspect2dp, relief=None, text='', text_font=PiratesGlobals.getPirateOutlineFont(), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_scale=PiratesGuiGlobals.TextScaleTitleJumbo * 0.5, text_align=TextNode.ACenter, pos=(0.0, 0.0, -0.8), text_wordwrap=30, textMayChange=1)
        self.wheel = self.model.find('**/red_wheel')
        title_bg = self.model.find('**/title_bg')
        title_frame = self.model.find('**/title_frame')
        if base.config.GetBool('loading-screen-interstitial', 0):
            self.hintLabel.setPos(0.69, 0, -0.63)
            self.hintLabel['text_wordwrap'] = 12
            self.locationLabel.setPos(-0.11, 0.0, -0.65)
            root = self.model.find('**/loading_screen_top')
            timer = self.model.find('**/timer')
            gear = self.model.find('**/gear')
            shell = self.model.find('**/shell')
            frame_little = self.model.find('**/frame_little')
            self.wheel.reparentTo(timer, 0)
            gear.reparentTo(timer, 1)
            shell.reparentTo(timer, 2)
            title_bg.reparentTo(root)
            title_frame.reparentTo(root)
            self.snapshotFrameBasic = DirectFrame(parent=aspect2dp, relief=DGG.FLAT, frameColor=(0.0,
                                                                                                 0.0,
                                                                                                 0.0,
                                                                                                 1.0), frameSize=(-4.95,
                                                                                                                  -2.5,
                                                                                                                  -1.1,
                                                                                                                  -2.6))
            self.snapshotFrameBasic.reparentTo(root)
            frame_little.reparentTo(root)
            self.title_art.append(title_bg)
            self.title_art.append(title_frame)
            self.hideTitleFrame()
            if waitForLocation or self.snapshot is None:
                screenshot = random.choice(tutorialShots_MoveAim)
                self.__setLoadingArt(screenshot)
            if self.snapshot:
                self.snapshot.show()
        elif self.snapshot:
            self.snapshot.show()
        if self.snapshot and base.config.GetBool('loading-screen-interstitial', 0):
            root = self.model.find('**/loading_screen_top')
            frame_little = self.model.find('**/frame_little')
            self.snapshot.reparentTo(root, 0)
            frame_little.reparentTo(root, 1)
        self.snapshotFrame = DirectFrame(parent=aspect2dp, relief=DGG.FLAT, frameColor=(0.0,
                                                                                        0.0,
                                                                                        0.0,
                                                                                        1.0), frameSize=(-2.0,
                                                                                                         2.0,
                                                                                                         2.0,
                                                                                                         -2.0))
        self.snapshotFrame.setBin('fixed', 0)
        self.model.reparentTo(aspect2dp, DGG.NO_FADE_SORT_INDEX)
        self.locationLabel.reparentTo(aspect2dp, DGG.NO_FADE_SORT_INDEX)
        self.hintLabel.reparentTo(aspect2dp, DGG.NO_FADE_SORT_INDEX)
        if base.config.GetBool('loading-screen-interstitial', 0):
            self.model.setScale(0.22, 0.22, 0.22)
            self.model.setPos(0.0, 0.0, -0.3)
        else:
            self.model.setScale(0.25, 0.25, 0.25)
            self.model.setPos(0.0, 0.0, -0.15)
        if self.locationText and len(self.locationText):
            self.__setLocationText(self.locationText)
        if self.hintText is not None:
            if len(self.hintText):
                self.__setHintText(self.hintText)
        if base.config.GetBool('want-ad-reporting', 0) and base.config.GetBool('loading-screen-interstitial', 0):
            self.__setAdArt()
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
        return

    def showHint(self, destId=None, ocean=False):
        if base.config.GetBool('no-loading-screen', 0):
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
        if base.localAvatar.style.getTutorial() == PiratesGlobals.TUT_MET_JOLLY_ROGER:
            hint = '%s:  %s' % (PLocalizer.LoadingScreen_Hint, PLocalizer.GeneralTip7)
        self.__setHintText(hint)

    def update(self, task=None):
        if not self.state:
            return Task.cont
        realTime = globalClock.getRealTime()
        if realTime - self.lastUpdateTime < 0.1:
            return Task.cont
        self.currentTime += min(10, (realTime - self.lastUpdateTime) * 250)
        self.lastUpdateTime = realTime
        self.wheel.setR(-self.currentTime)
        base.graphicsEngine.renderFrame()
        return Task.cont

    def hide(self):
        if not self.state:
            return
        render.show()
        base.graphicsEngine.renderFrame()
        self.state = False
        self.currentTime = 0
        self.locationText = None
        self.hintText = None
        gsg = base.win.getGsg()
        if gsg:
            gsg.setIncompleteRender(True)
            render.prepareScene(gsg)
            render2d.prepareScene(gsg)
        for part in (self.model, self.snapshot):
            if part:
                tex = part.findTexture('*')
                if tex:
                    tex.releaseAll()
                part.removeNode()

        self.model = None
        self.snapshot = None
        if self.adImage:
            self.adImage = None
        if self.snapshotFrame:
            self.snapshotFrame.destroy()
        if self.locationLabel:
            self.locationLabel.destroy()
        if self.hintLabel:
            self.hintLabel.destroy()
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
        else:
            if exit:
                screenshot = screenShot_ExitGame
            else:
                if ocean:
                    screenshot = screenShot_Dinghy
                elif jail:
                    screenshot = screenShot_Jail
                elif potionCrafting:
                    screenshot = screenShot_Potions
                elif benchRepair:
                    screenshot = screenShot_BenchRepair
                else:
                    if shipRepair:
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
                    elif len(screenshot) > 1:
                        screenshot = random.choice(screenshot)
                    else:
                        screenshot = screenshot[0]
                    self.__setLoadingArt(screenshot)
                    if pickapirate:
                        targetName = PLocalizer.LoadingScreen_PickAPirate
                    if exit:
                        targetName = None
                    if ocean:
                        targetName = PLocalizer.LoadingScreen_Ocean
                    if jail:
                        targetName = PLocalizer.LoadingScreen_Jail
                    targetName = PLocalizer.LocationNames.get(targetId)
                base.setLocationCode('Loading: %s' % targetName)
                if targetName is None:
                    return
            if len(targetName):
                self.__setLocationText(targetName)
        return

    def __setLoadingArt(self, screenshot):
        if self.snapshot:
            return

        if hasattr(base, 'localAvatar') and base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_MET_JOLLY_ROGER and screenshot not in tutorialShots:
            screenshot = random.choice(tutorialShots)

        self.snapshot = loader.loadModel(screenshot)
        if self.snapshot:
            if base.config.GetBool('loading-screen-interstitial', 0):
                self.snapshot.setScale(2.35, 1.0, 1.3)
                self.snapshot.setPos(-3.74, 0, -1.83)
                if self.model is not None:
                    root = self.model.find('**/loading_screen_top')
                    frame_little = self.model.find('**/frame_little')
                    self.snapshot.reparentTo(root, 0)
                    frame_little.reparentTo(root, 1)
            else:
                self.snapshot.reparentTo(aspect2dp, DGG.NO_FADE_SORT_INDEX)
                self.snapshot.setScale(2.15, 1, 1.2)
                self.snapshot.setPos(0.0, 0.0, 0.09)
                self.snapshot.setBin('fixed', 1)
            self.__isVisible() or self.snapshot.hide()

    def __setLocationText(self, locationText):
        self.locationText = locationText
        if self.__isVisible():
            self.locationLabel['text'] = locationText
            self.locationLabel.show()
            self.showTitleFrame()
        launcher.setValue('gameLocation', self.locationText)

    def __setHintText(self, hintText):
        self.hintText = hintText
        if self.__isVisible():
            self.hintLabel['text'] = hintText
            self.hintLabel.show()

    def __isVisible(self):
        return self.state

    def scheduleHide(self, function):
        base.cr.queueAllInterestsCompleteEvent()
        self.acceptOnce(function, self.hide)

    def __setAdArt(self):
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
