import sys
import time
import os
from pandac.PandaModules import *
from otp.nametag import NametagGlobals
from otp.nametag.ChatBalloon import ChatBalloon
from otp.nametag.MarginManager import MarginManager
from direct.showbase.DirectObject import *
from direct.showbase.PythonUtil import *
from direct.showbase.Transitions import Transitions
from direct.directnotify import DirectNotifyGlobal
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.task import Task
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
from otp.otpbase.OTPBase import OTPBase
from pirates.audio import MusicManager
from pirates.audio import PiratesAmbientManager
from pirates.launcher import PiratesDownloadWatcher
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.GameOptions import Options
from pirates.piratesgui import PiratesGuiGlobals
from pirates.ship import ShipFactory
from pirates.piratesgui import ScreenshotViewer
from pirates.piratesbase import FancyLoadingScreen
from pirates.piratesbase import LoadingScreen
from otp.otpgui import OTPDialog
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from pirates.piratesgui import PDialog
from pirates.chat.PWhiteList import PWhiteList
import PiratesGlobals
import __builtin__
try:
    import embedded
    hasEmbedded = 1
except ImportError:
    hasEmbedded = 0

from pirates.piratesbase import UserFunnel

class PiratesBase(OTPBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesBase')
    lowMemoryStreamAudio = ConfigVariableBool('low-memory-stream-audio', 1)
    resolution_table = [(800, 600), (1024, 768), (1280, 1024), (1600, 1200)]
    widescreen_resolution_table = [(1280, 720), (1920, 1080)]
    MinimumHorizontalResolution = 800
    MinimumVerticalResolution = 600
    apiNames = ['pandagl', 'pandadx8', 'pandadx9', 'tinydisplay']

    def __init__(self):
        OTPBase.__init__(self, windowType='none')
        print cpMgr
        self.hasEmbedded = hasEmbedded
        self.shipFactory = None
        self.firstMateVoiceOn = 1
        self.shipLookAhead = 0
        if __dev__:
            launcher.setValue('GAME_SHOW_ADDS', 'NO')
        if base.appRunner:
            launcher.setValue('GAME_SHOW_ADDS', 'NO')
        self.fourthOfJuly = self.config.GetBool('test-fourth-of-july', 0)
        if self.hasEmbedded:
            self.inAdFrame = embedded.isMainWindowVisible()
        else:
            self.inAdFrame = False
        self.bamCache = BamCache.getGlobalPtr()
        if self.config.GetBool('want-dev', 0):
            flavor = self.config.GetString('dev-branch-flavor', '')
            if flavor:
                cachePath = '/c/cache_%s' % (flavor,)
            else:
                cachePath = '/c/cache'
            self.bamCache.setRoot(Filename(cachePath))
        else:
            self.bamCache.setRoot(Filename('./cache'))
        self.bamCache.setActive(False)
        self.bamCache.setActive(True)
        self.bamCache.setCacheModels(False)
        self.bamCache.setCacheTextures(True)
        self.bamCache.setCacheCompressedTextures(True)
        CullBinManager.getGlobalPtr().addBin('ground', CullBinEnums.BTFixed, 14)
        CullBinManager.getGlobalPtr().addBin('shadow', CullBinEnums.BTFixed, 15)
        CullBinManager.getGlobalPtr().addBin('water', CullBinEnums.BTFixed, 28)
        CullBinManager.getGlobalPtr().addBin('gui-fixed', CullBinEnums.BTFixed, 55)
        CullBinManager.getGlobalPtr().addBin('gui-popup', CullBinEnums.BTUnsorted, 60)
        base.effectsRoot = render.attachNewNode('Effects Root')
        self.musicMgr = None
        use_recommended_options = False
        options = Options()
        options_loaded = options.load(Options.DEFAULT_FILE_PATH)
        self.notify.info('Requested graphics API = %s' % options.api)
        if options.api == 'default' and self.config.GetBool('use-graphics-api-auto-select', True):
            base.makeDefaultPipe()
            options.automaticGraphicsApiSelection(base.pipe)
            self.notify.info('Auto-selected graphics API = %s' % options.api)
        if options.api in self.apiNames:
            selection = GraphicsPipeSelection.getGlobalPtr()
            pipe = selection.makeModulePipe(options.api)
            if pipe:
                base.pipe = pipe
                self.notify.info('Loaded requested graphics %s' % base.pipe.getType().getName())
        if not base.pipe:
            base.makeDefaultPipe()
            if not base.pipe:
                self.notify.error('Could not find any graphics API.')
            self.notify.info('Loaded default graphics %s' % base.pipe.getType().getName())
        bits_per_pixel = 32
        if self.inAdFrame:
            self.getVelvetDisplayResolutions(bits_per_pixel, base.pipe)
        else:
            self.getDisplayResolutions(bits_per_pixel, base.pipe)
        if options_loaded:
            print 'state = %s' % options.state
            if __dev__:
                options.save(Options.DEFAULT_FILE_PATH, Options.WORKING_STATE)
            elif options.state == Options.DEFAULT_STATE or options.state == Options.NEW_STATE:
                options.save(Options.DEFAULT_FILE_PATH, Options.ATTEMPT_STATE)
            elif options.state == Options.ATTEMPT_STATE:
                working_options = Options()
                if working_options.load(Options.WORKING_FILE_PATH):
                    options = working_options
                    working_options.save(Options.DEFAULT_FILE_PATH, Options.ATTEMPT_WORKING_STATE)
                else:
                    options.config_to_options()
                    use_recommended_options = True
            elif options.state == Options.WORKING_STATE:
                options.save(Options.DEFAULT_FILE_PATH, Options.ATTEMPT_STATE)
            elif options.state == Options.ATTEMPT_WORKING_STATE:
                options.config_to_options()
                use_recommended_options = True
            else:
                options.save(Options.DEFAULT_FILE_PATH, Options.ATTEMPT_STATE)
            options.log('Loaded Game Options')
        else:
            options.config_to_options()
            if self.config.GetBool('want-dev', False):
                pass
            else:
                use_recommended_options = True
            if use_recommended_options:
                options.recommendedOptions(base.pipe, False)
                options.log('Recommended Game Options')

        overwrite_options = config.GetBool('allow-options-override', False)
        options.verifyOptions(base.pipe, overwrite_options)
        string = options.optionsToPrcData()
        loadPrcFileData('game_options', string)
        self.options = options
        self.shipsVisibleFromIsland = self.options.ocean_visibility
        self.overrideShipVisibility = False
        base.windowType = 'onscreen'
        self.detachedWP = WindowProperties()
        self.embeddedWP = WindowProperties()
        if self.hasEmbedded:
            if embedded.isMainWindowVisible():
                self.showEmbeddedFrame()
            else:
                self.hideEmbeddedFrame()
        else:
            if self.appRunner:
                self.openDefaultWindow()
            else:
                wp = WindowProperties()
                wp.setSize(options.getWidth(), options.getHeight())
                wp.setFullscreen(options.getFullscreen())
                self.openDefaultWindow(props=wp)

        self.eventMgr.doEvents()
        options.options_to_config()
        options.setRuntimeOptions()
        if not options.fancy_loading_screen:
            self.loadingScreen = LoadingScreen.LoadingScreen(None)
        else:
            self.loadingScreen = FancyLoadingScreen.FancyLoadingScreen(None)
        self.loadingScreen.showTarget(pickapirate=True)
        self.loadingScreen.show()
        self.loadingScreen.beginStep('PiratesBase', 34, 25)
        self.loadingScreen.tick()
        if base.wantEnviroDR:
            base.cam.node().setCameraMask(OTPRender.MainCameraBitmask)
            self.setupEnviroCamera()
            self.setupAutoPixelZoom()
        else:
            base.cam.node().setCameraMask(OTPRender.MainCameraBitmask | OTPRender.EnviroCameraBitmask)
        self.loadingScreen.tick()
        self.__alreadyExiting = False
        self.exitFunc = self.userExit
        TextureStage.getDefault().setPriority(10)
        self.useDrive()
        self.disableMouse()
        if not self.config.GetBool('location-kiosk', 0):
            for key in PiratesGlobals.ScreenshotHotkeyList:
                self.accept(key, self.takeScreenShot)

        self.screenshotViewer = None
        if self.config.GetBool('want-screenshot-viewer', 0):
            self.accept(PiratesGlobals.ScreenshotViewerHotkey, self.showScreenshots)
        self.wantMarketingViewer = self.config.GetBool('want-marketing-viewer', 0)
        self.marketingViewerOn = False
        if self.wantMarketingViewer:
            for key in PiratesGlobals.MarketingHotkeyList:
                self.accept(key, self.toggleMarketingViewer)

        self.accept('panda3d-render-error', self.panda3dRenderError)
        camera.setPosHpr(0, 0, 0, 0, 0, 0)
        self.camLens.setMinFov(PiratesGlobals.DefaultCameraFov)
        self.camLens.setNearFar(PiratesGlobals.DefaultCameraNear, PiratesGlobals.DefaultCameraFar)
        farCullNode = PlaneNode('farCull')
        farCullNode.setPlane(Plane(Vec3(0, -1, 0), Point3(0, 0, 0)))
        farCullNode.setClipEffect(0)
        self.farCull = camera.attachNewNode(farCullNode)
        self.positionFarCull()
        globalClockMaxDt = self.config.GetFloat('pirates-max-dt', 0.2)
        globalClock.setMaxDt(globalClockMaxDt)
        self.loadingScreen.tick()
        if self.config.GetBool('want-particles', 1):
            self.notify.debug('Enabling particles')
            self.enableParticles()
        self.loadingScreen.tick()
        self.notify.debug('Enabling new ship controls')
        self.avatarPhysicsMgr = PhysicsManager()
        integrator = LinearEulerIntegrator()
        self.avatarPhysicsMgr.attachLinearIntegrator(integrator)
        integrator = AngularEulerIntegrator()
        self.avatarPhysicsMgr.attachAngularIntegrator(integrator)
        self.taskMgr.add(self.doAvatarPhysics, 'physics-avatar')
        fn = ForceNode('ship viscosity')
        fnp = NodePath(fn)
        fnp.reparentTo(render)
        viscosity = LinearFrictionForce(0.0, 1.0, 0)
        viscosity.setCoef(0.5)
        viscosity.setAmplitude(2)
        fn.addForce(viscosity)
        self.avatarPhysicsMgr.addLinearForce(viscosity)
        self.loadingScreen.tick()
        fn = ForceNode('avatarControls')
        fnp = NodePath(fn)
        fnp.reparentTo(render)
        controlForce = LinearControlForce()
        self.controlForce = controlForce
        controlForce.setAmplitude(5)
        fn.addForce(controlForce)
        self.avatarPhysicsMgr.addLinearForce(controlForce)
        self.loadingScreen.tick()
        self.accept('PandaPaused', self.disableAudio)
        self.accept('PandaRestarted', self.enableAllAudio)
        self.emoteGender = None
        shadow = loader.loadModel('models/misc/drop_shadow.bam')
        shadow.findTexture('*').setQualityLevel(Texture.QLBest)
        self.loadingScreen.tick()
        taskMgr.setupTaskChain('phasePost', numThreads=0, threadPriority=TPHigh)
        launcher.addPhasePostProcess(3, self.phase3Post, taskChain='phasePost')
        launcher.addPhasePostProcess(4, self.phase4Post, taskChain='phasePost')
        launcher.addPhasePostProcess(5, self.phase5Post, taskChain='phasePost')
        self.whiteList = PWhiteList()
        tpMgr = TextPropertiesManager.getGlobalPtr()
        WLDisplay = TextProperties()
        WLDisplay.setSlant(0.3)
        WLEnter = TextProperties()
        WLEnter.setTextColor(1.0, 0.0, 0.0, 1)
        tpMgr.setProperties('WLDisplay', WLDisplay)
        tpMgr.setProperties('WLEnter', WLEnter)
        del tpMgr
        CullBinManager.getGlobalPtr().addBin('ShipRigging', CullBinEnums.BTBackToFront, 52)
        CullBinManager.getGlobalPtr().addBin('pre-additive', CullBinEnums.BTFixed, 53)
        CullBinManager.getGlobalPtr().addBin('additive', CullBinEnums.BTBackToFront, 54)
        self.showShipFlats = False
        self.hideShipNametags = False
        self.showGui = True
        self.memoryMonitorMinimumPercentage = 90
        self.cpuSpeedDialog = None
        self.peakProcessMemory = 0
        self.peakMemoryLoad = 0
        self.maximumCpuFrequency = 0
        self.currentCpuFrequency = 0
        self.displayCpuFrequencyDialog = False
        self.taskMgr.doMethodLater(120.0, self.memoryMonitorTask, 'memory-monitor-task')
        self.useStencils = self.win.getGsg().getSupportsStencil()
        self.supportAlphaFb = self.win.getFbProperties().getAlphaBits()
        taskMgr.setupTaskChain('background', frameBudget=0.001, threadPriority=TPLow)
        gsg = base.win.getGsg()
        if gsg.getShaderModel() < gsg.SM20:
            base.options.shader_runtime = 0

        self.noticeSystemOn = 1
        self.lodTrav = CollisionTraverser('base.lodTrav')
        self.zoneLODEventHandler = CollisionHandlerEvent()
        self.zoneLODEventHandler.addInPattern('enter%in')
        self.zoneLODEventHandler.addOutPattern('exit%in')
        self.zoneLODTarget = None
        self.transitions.loadLetterbox()
        self.transitions.letterbox.setColorScale(0, 0, 0, 1)
        self.loadingScreen.endStep('PiratesBase')

        self.accept('f4', lambda: self.oobe())
        self.accept('f5', lambda: self.localAvatar.setZ(self.localAvatar.getZ() + 15))

    def disableAudio(self):
        if not self.options.background_audio:
            self.disableAllAudio()

    def setNoticeSystem(self, on):
        if self.noticeSystemOn == on:
            return

        self.noticeSystemOn = on
        messenger.send('noticeStateChanged')

    def enableFirstMate(self, bEnableFirstMate):
        self.firstMateVoiceOn = bEnableFirstMate

    def setShipLookAhead(self, value):
        self.shipLookAhead = value

    def deleteDialogs(self):
        if self.cpuSpeedDialog:
            self.cpuSpeedDialog.destroy()
            del self.cpuSpeedDialog
            self.cpuSpeedDialog = None

    def cpuSpeedDialogCommand(self, value):
        if value == DGG.DIALOG_OK:
            pass
        elif value == DGG.DIALOG_CANCEL:
            base.options.cpu_frequency_warning = 0
            base.options.save(Options.DEFAULT_FILE_PATH, Options.NEW_STATE)
            base.options.log('Options Saved: Cpu Frequency Warning Disable')

        self.deleteDialogs()

    def displayCpuSpeedDialog(self, message):
        self.deleteDialogs()
        if base.options.cpu_frequency_warning:
            buttonText = [
             OTPLocalizer.DialogOK, OTPLocalizer.DialogDoNotShowAgain]
            self.cpuSpeedDialog = PDialog.PDialog(text=message, style=OTPDialog.TwoChoiceCustom, giveMouse=False, command=self.cpuSpeedDialogCommand, buttonText=buttonText)
            if self.cpuSpeedDialog:
                self.cpuSpeedDialog.setBin('gui-fixed', 20, 20)

    def memoryMonitorTask(self, task):
        if base.pipe:
            display = False
            di = base.pipe.getDisplayInformation()
            if di:
                di.updateMemoryInformation()
                if di.getPeakProcessMemory() > self.peakProcessMemory:
                    self.peakProcessMemory = di.getPeakProcessMemory()
                    display = True
                if di.getMemoryLoad() >= self.memoryMonitorMinimumPercentage and di.getMemoryLoad() > self.peakMemoryLoad:
                    self.peakMemoryLoad = di.getMemoryLoad()
                    display = True
                if display:
                    oomb = 1.0 / (1024.0 * 1024.0)
                    string = 'memory_usage:    %d%%' % di.getMemoryLoad()
                    self.notify.info(string)
                    string = 'physical_memory: %.2f / %.2f MB' % (di.getAvailablePhysicalMemory() * oomb, di.getPhysicalMemory() * oomb)
                    self.notify.info(string)
                    string = 'page_file_size:  %.2f / %.2f MB' % (di.getAvailablePageFileSize() * oomb, di.getPageFileSize() * oomb)
                    self.notify.info(string)
                    string = 'virtual_memory:  %.2f / %.2f MB' % (di.getAvailableProcessVirtualMemory() * oomb, di.getProcessVirtualMemory() * oomb)
                    self.notify.info(string)
                    string = 'process_memory:  %.2f / %.2f MB' % (di.getProcessMemory() * oomb, di.getPeakProcessMemory() * oomb)
                    self.notify.info(string)
                    string = 'page_file_usage: %.2f / %.2f MB' % (di.getPageFileUsage() * oomb, di.getPeakPageFileUsage() * oomb)
                    self.notify.info(string)
                    string = 'page_faults:     %d' % di.getPageFaultCount()
                    self.notify.info(string)
                if self.config.GetBool('want-cpu-frequency-warning', 0):
                    processor_number = 0
                    di.updateCpuFrequency(processor_number)
                    maximum = di.getMaximumCpuFrequency()
                    if maximum > 0:
                        current = di.getCurrentCpuFrequency()
                        if current > 0:
                            if self.config.GetInt('test-cpu-frequency-warning', 0):
                                current = maximum - 1000000
                            change = False
                            if current != self.currentCpuFrequency:
                                if self.currentCpuFrequency:
                                    change = True
                                self.currentCpuFrequency = current
                            if maximum != self.maximumCpuFrequency:
                                self.maximumCpuFrequency = maximum
                            if current < maximum:
                                if self.displayCpuFrequencyDialog == False:
                                    self.displayCpuFrequencyDialog = True
                                    oob = 1.0 / 1000000000.0
                                    c = current * oob
                                    m = maximum * oob
                                    string = PLocalizer.CpuWarning % (c, m)
                                    self.displayCpuSpeedDialog(string)
                                    self.notify.info(string)
                            if current == maximum:
                                self.displayCpuFrequencyDialog = False
        return Task.again

    def phase3Post(self):
        from pirates.battle import Sword, Dagger
        Sword.Sword.setupAssets()
        Dagger.Dagger.setupAssets()
        self.buildShips()

    def phase4Post(self):
        self.buildPhase4Assets()
        self.buildPhase4Ships()

    def phase5Post(self):
        from pirates.creature import Raven
        Raven.Raven.setupAssets()
        self.buildPhase5Ships()

    def buildPhase4Assets(self):
        from pirates.battle import WeaponGlobals
        from pirates.battle import Pistol, Sword, Dagger, Doll, Wand, Grenade, Bayonet, Melee, DualCutlass, Foil, Gun, FishingRod, Torch, PowderKeg
        from pirates.creature import Alligator, Bat, Chicken, Crab, Dog, FlyTrap, Monkey, Pig, Rooster, Scorpion, Seagull, Stump, Wasp
        if config.GetBool('want-kraken', 0):
            from pirates.kraken import Holder
            Holder.Holder.setupAssets()
            self.loadingScreen.tick()
        if self.config.GetBool('want-seamonsters', 0):
            from pirates.creature import SeaSerpent
            SeaSerpent.SeaSerpent.setupAssets()
            self.loadingScreen.tick()
        PowderKeg.PowderKeg.setupAssets()
        self.loadingScreen.tick()
        Torch.Torch.setupAssets()
        self.loadingScreen.tick()
        FishingRod.FishingRod.setupAssets()
        self.loadingScreen.tick()
        Bayonet.Bayonet.setupAssets()
        self.loadingScreen.tick()
        Pistol.Pistol.setupAssets()
        self.loadingScreen.tick()
        Doll.Doll.setupAssets()
        self.loadingScreen.tick()
        Grenade.Grenade.setupAssets()
        self.loadingScreen.tick()
        Wand.Wand.setupAssets()
        self.loadingScreen.tick()
        Melee.Melee.setupSounds()
        self.loadingScreen.tick()
        DualCutlass.DualCutlass.setupAssets()
        self.loadingScreen.tick()
        Foil.Foil.setupAssets()
        self.loadingScreen.tick()
        Gun.Gun.setupAssets()
        self.loadingScreen.tick()
        Alligator.Alligator.setupAssets()
        self.loadingScreen.tick()
        Bat.Bat.setupAssets()
        self.loadingScreen.tick()
        Chicken.Chicken.setupAssets()
        self.loadingScreen.tick()
        Crab.Crab.setupAssets()
        self.loadingScreen.tick()
        Dog.Dog.setupAssets()
        self.loadingScreen.tick()
        FlyTrap.FlyTrap.setupAssets()
        self.loadingScreen.tick()
        Monkey.Monkey.setupAssets()
        self.loadingScreen.tick()
        Pig.Pig.setupAssets()
        self.loadingScreen.tick()
        Rooster.Rooster.setupAssets()
        self.loadingScreen.tick()
        Scorpion.Scorpion.setupAssets()
        self.loadingScreen.tick()
        Seagull.Seagull.setupAssets()
        self.loadingScreen.tick()
        Stump.Stump.setupAssets()
        self.loadingScreen.tick()
        Wasp.Wasp.setupAssets()
        self.loadingScreen.tick()

    def buildAssets(self):
        pass

    def buildShips(self):
        if not self.shipFactory:
            self.shipFactory = ShipFactory.ShipFactory(phasedLoading=True)
        self.loadingScreen.tick()

    def buildPhase4Ships(self):
        if not self.shipFactory:
            self.buildShips()
        self.shipFactory.handlePhase4()
        self.loadingScreen.tick()

    def buildPhase5Ships(self):
        if not self.shipFactory:
            self.buildShips()
        self.shipFactory.handlePhase5()
        self.loadingScreen.tick()

    def openMainWindow(self, *args, **kw):
        kw['stereo'] = bool(self.stereoEnabled)
        success = OTPBase.openMainWindow(self, *args, **kw)
        if self.win:
            self.win.setSort(500)
            self.win.setChildSort(10)
            self.postOpenWindow()
        return success

    def postOpenWindow(self):
        NametagGlobals.setCamera(base.cam)
        if base.wantEnviroDR:
            base.cam.node().setCameraMask(OTPRender.MainCameraBitmask)
        else:
            base.cam.node().setCameraMask(OTPRender.MainCameraBitmask | OTPRender.EnviroCameraBitmask)
        NametagGlobals.setMouseWatcher(base.mouseWatcherNode)
        if base.wantEnviroDR:
            base.setupEnviroCamera()
        if self.config.GetBool('show-tex-mem', False):
            if not self.texmem or self.texmem.cleanedUp:
                self.toggleTexMem()

    def showEmbeddedFrame(self):
        if not self.hasEmbedded:
            return False
        embedded.showMainWindow()
        self.inAdFrame = True
        self.options.fullscreen_runtime = 0
        wdef = embedded.getCurrentWindowModeDef()
        self.embeddedWP.setSize(wdef['want_size_x'], wdef['want_size_y'])
        self.embeddedWP.setOrigin(wdef['want_loc_x'], wdef['want_loc_y'])
        self.embeddedWP.setParentWindow(embedded.getMainWindowHandle())
        self.embeddedWP.setFullscreen(0)
        messenger.send('access-changed')
        return self.openDefaultWindow(props=self.embeddedWP, gsg=base.win, keepCamera=True)

    def hideEmbeddedFrame(self):
        if not self.hasEmbedded:
            return False
        embedded.hideMainWindow()
        self.detachedWP.setSize(self.options.getWidth(), self.options.getHeight())
        self.detachedWP.setFullscreen(self.options.fullscreen)
        messenger.send('access-changed')
        return self.openDefaultWindow(props=self.detachedWP, gsg=base.win, keepCamera=True)

    def setEmbeddedFrameMode(self, access):
        if not self.hasEmbedded:
            return False
        if access == OTPGlobals.AccessVelvetRope:
            if launcher.getValue('GAME_SHOW_ADDS') != 'NO':
                self.inAdFrame = True
                return embedded.isMainWindowVisible() or self.showEmbeddedFrame()
        else:
            self.inAdFrame = False
            if embedded.isMainWindowVisible():
                return self.hideEmbeddedFrame()

    def popupBrowser(self, url, demandFocus=False):
        import sys
        if sys.platform == 'darwin':
            import os
            os.system('/usr/bin/open %s' % url)
        elif sys.platform == 'linux2':
            import webbrowser
            webbrowser.open(url)
        else:
            try:
                import webbrowser
                webbrowser.open(url, new=2, autoraise=True)
            except WindowsError, e:
                if base.appRunner:
                    demandFocus = False
                    if demandFocus:
                        base.appRunner.dom.location = url
                    else:
                        base.appRunner.evalScript('window.open("%s")' % (url,), needsResponse=False)
                else:
                    import os
                    os.system('explorer "%s"' % url)

    def refreshAds(self):
        self.notify.debug('Refresh Ads')
        if not self.hasEmbedded:
            return False
        embedded.allowAddRefreshLeft()
        embedded.allowAddRefreshTop()

    def positionFarCull(self):
        gridDetail = self.config.GetString('grid-detail', 'high')
        self.gridDetail = gridDetail
        if gridDetail == 'high':
            self.farCull.setPos(0, 10000, 0)
        elif gridDetail == 'med':
            self.farCull.setPos(0, 5000, 0)
        elif gridDetail == 'low':
            self.farCull.setPos(0, 200, 0)
        else:
            raise StandardError, 'Invalid grid-detail: %s' % gridDetail

    def disableFarCull(self):
        self.farCull.setPos(0, 10000, 0)

    def setLowMemory(self, lowMemory):
        self.lowMemory = lowMemory
        if lowMemory:
            GeomVertexArrayData.getIndependentLru().setMaxSize(5242880)
            VertexDataPage.getGlobalLru(VertexDataPage.RCResident).setMaxSize(5242880)
            taskMgr.setupTaskChain('background', numThreads=0)
        else:
            GeomVertexArrayData.getIndependentLru().setMaxSize(4294967295L)
            VertexDataPage.getGlobalLru(VertexDataPage.RCResident).setMaxSize(4294967295L)
            taskMgr.setupTaskChain('background', numThreads=1)
        for filename in ['models/misc/male_face.bam', 'models/misc/female_face.bam']:
            self._setKeepRamImage(filename)

    def _setKeepRamImage(self, filename):
        model = loader.loadModel(filename)
        if self.lowMemory:
            for tex in model.findAllTextures():
                tex.setCompression(tex.CMDefault)
                tex.setKeepRamImage(False)
                tex.clearRamImage()

        else:
            for tex in model.findAllTextures():
                tex.setCompression(tex.CMOff)
                tex.setKeepRamImage(True)
                tex.reload()

    def setupRender2d(self):
        OTPBase.setupRender2d(self)
        self.a2dTopRight.reparentTo(self.aspect2d, sort=1)

    def setupMouse(self, win, fMultiWin=False):
        response = OTPBase.setupMouse(self, win, fMultiWin)
        mk = self.mouseWatcher.getParent()
        bt = mk.attachNewNode(ButtonThrower('uber'))
        bt.node().setPrefix('uber-')
        mods = ModifierButtons()
        mods.addButton(KeyboardButton.shift())
        mods.addButton(KeyboardButton.control())
        mods.addButton(KeyboardButton.alt())
        mods.addButton(KeyboardButton.meta())
        bt.node().setModifierButtons(mods)
        self.buttonThrowers.append(bt)
        return response

    def doAvatarPhysics(self, state):
        dt = ClockObject.getGlobalClock().getDt()
        freq = self.config.GetFloat('avatar-physics-freq', 0.0)
        maxSteps = self.config.GetInt('avatar-physics-maxsteps', 5)
        if not freq:
            self.avatarPhysicsMgr.doPhysics(dt)
        else:
            if not hasattr(state, 'dtRollover'):
                state.dtRollover = 0
            maxDt = 1.0 / freq
            dt += state.dtRollover
            steps = int(dt / maxDt)
            state.dtRollover = dt % maxDt
            for x in range(min(steps, maxSteps)):
                self.avatarPhysicsMgr.doPhysics(maxDt)

            finalStep = max(steps - maxSteps, 0)
            if finalStep:
                self.avatarPhysicsMgr.doPhysics(finalStep * maxDt)
        return Task.cont

    def takeScreenShot(self):
        self.notify.info('Beginning screenshot capture')
        dt = time.localtime()
        date_time = '%04d-%02d-%02d_%02d-%02d-%02d' % (dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
        uFilename = PLocalizer.ScreenshotDir + '/' + PLocalizer.Screenshot + '_' + date_time + '.' + base.screenshotExtension
        pandafile = Filename(str(ExecutionEnvironment.getCwd()) + '/' + str(uFilename))
        pandafile.makeDir()
        fn = base.screenshot(namePrefix=uFilename, defaultFilename=0)
        winfile = pandafile.toOsSpecific()
        self.notify.info('Screenshot captured: ' + winfile)
        screenShotNotice = DirectLabel(text=PLocalizer.ScreenshotCaptured + ':\n' + winfile, scale=0.05, pos=(0.0,
                                                                                                              0.0,
                                                                                                              0.3), text_bg=(1,
                                                                                                                             1,
                                                                                                                             1,
                                                                                                                             0), text_fg=(1,
                                                                                                                                          1,
                                                                                                                                          1,
                                                                                                                                          1), frameColor=(1,
                                                                                                                                                          1,
                                                                                                                                                          1,
                                                                                                                                                          0), text_font=PiratesGlobals.getInterfaceOutlineFont())
        screenShotNotice.reparentTo(base.a2dBottomCenter)
        screenShotNotice.setBin('gui-popup', 0)

        def clearScreenshotMsg(event):
            screenShotNotice.destroy()

        taskMgr.doMethodLater(3.0, clearScreenshotMsg, 'clearScreenshot')

    def showScreenshots(self):
        filenames = os.listdir(os.curdir + '/' + PLocalizer.ScreenshotDir)
        for f in filenames:
            if 'jpg' in f:
                if not self.screenshotViewer:
                    self.screenshotViewer = ScreenshotViewer.ScreenshotViewer()
                self.screenshotViewer.toggleShow()

    def cleanupDownloadWatcher(self):
        self.downloadWatcher.cleanup()
        if hasattr(self, 'localAvatar'):
            if self.localAvatar.guiMgr.trackedQuestLabel:
                self.localAvatar.guiMgr.trackedQuestLabel.setPos(-0.9, 0, -0.05)
        self.downloadWatcher = None
        return

    def startShow(self, cr):
        self.cr = cr
        from pirates.world import WorldCreator
        self.worldCreator = WorldCreator.WorldCreator(self.cr, None, None)

        def nullYield(comment=''):
            pass

        __builtin__.yieldThread = nullYield
        del nullYield
        base.graphicsEngine.renderFrame()
        self.downloadWatcher = PiratesDownloadWatcher.PiratesDownloadWatcher(PLocalizer.LauncherPhaseNames)
        if launcher.getPhaseComplete(5):
            self.cleanupDownloadWatcher()
        else:
            self.acceptOnce('launcherAllPhasesComplete', self.cleanupDownloadWatcher)

        gameServer = self.config.GetString('game-server', '')
        if gameServer:
            self.notify.info('Using game-server from Configrc: %s ' % gameServer)
        else:
            if launcher.getGameServer():
                gameServer = launcher.getGameServer()
                self.notify.info('Using gameServer from launcher: %s ' % gameServer)
            else:
                gameServer = 'localhost'
                self.notify.info('Using gameServer localhost')

        serverPort = self.config.GetInt('server-port', 7198)
        debugQuests = self.config.GetBool('debug-quests', True)
        self.wantTattoos = self.config.GetBool('want-tattoos', 0)
        self.wantSocks = self.config.GetBool('want-socks', 0)
        self.wantJewelry = self.config.GetBool('want-jewelry', 0)
        serverList = []
        for name in gameServer.split(';'):
            url = URLSpec(name, 1)
            if self.config.GetBool('want-ssl-scheme', False):
                url.setScheme('s')

            if not url.hasPort():
                url.setPort(serverPort)

            serverList.append(url)

        if len(serverList) == 1:
            failover = self.config.GetString('server-failover', '')
            serverURL = serverList[0]
            for arg in failover.split():
                try:
                    port = int(arg)
                    url = URLSpec(serverURL)
                    url.setPort(port)
                except:
                    url = URLSpec(arg, 1)

                if url != serverURL:
                    serverList.append(url)

        cr.loginFSM.request('connect', [serverList])
        self.musicMgr = MusicManager.MusicManager()
        self.ambientMgr = PiratesAmbientManager.PiratesAmbientManager()

        def toggleGUI():
            self.showGui = not self.showGui
            render2d.toggleVis()
            if self.config.GetBool('hidegui-hidenametags', 1):
                npc = render.findAllMatches('**/nametag3d')
                for i in range(npc.getNumPaths()):
                    np = npc.getPath(i)
                    np.toggleVis()

            if not self.showGui:
                messenger.send('GUIHidden')
            else:
                messenger.send('GUIShown')

        def toggleWorld():
            if base.cr.activeWorld.isHidden():
                base.cr.activeWorld.show()
                render.find('**/*sky*').show()
                render.find('**/*seapatch*').show()
                base.win.setClearColor(Vec4(0, 0, 0, 1.0))
            else:
                base.cr.activeWorld.hide()
                render.find('**/*sky*').hide()
                render.find('**/*seapatch*').hide()
                base.win.setClearColor(Vec4(0.5, 0.5, 0.5, 1.0))

        self.accept(PiratesGlobals.HideGuiHotkey, toggleGUI)
        return

    def panda3dRenderError(self):
        if launcher:
            launcher.setPandaErrorCode(14)
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(PiratesGlobals.DisconnectGraphicsError)
        self.cr.sendDisconnect()
        sys.exit()

    def userExit(self):
        if self.__alreadyExiting:
            return
        self.__alreadyExiting = True
        requestResult = False
        if hasattr(base, 'cr'):
            if self.cr.timeManager:
                self.cr.timeManager.setDisconnectReason(PiratesGlobals.DisconnectCloseWindow)
            if self.cr.loginFSM.getCurrentState().getName() == 'playingGame':
                requestResult = self.cr.gameFSM.request('closeShard', ['shutdown'])
            else:
                requestResult = self.cr.loginFSM.request('shutdown')
        self.loadingScreen.destroy()
        if not requestResult:
            self.notify.warning('Could not request shutdown; exiting anyway.')
            self.exitShow()

    def exitShow(self, errorCode=None):
        self.bamCache.flushIndex()
        self.ignore('f12')
        if hasattr(base, 'cr'):
            self.musicMgr.delete()
            self.ambientMgr.delete()
            self.cr.ignoreAll()
        self.notify.info('Exiting Pirates')
        if self.launcher and errorCode is not None:
            self.launcher.setPandaErrorCode(errorCode)
        sys.exit()
        return

    def initNametagGlobals(self):
        arrow = loader.loadModel('models/gui/arrow')
        card = NodePath('card')
        speech3d = ChatBalloon(loader.loadModel('models/gui/chatbox').node())
        thought3d = ChatBalloon(loader.loadModel('models/gui/chatbox_thought_cutout').node())
        speech2d = ChatBalloon(loader.loadModel('models/gui/chatbox_noarrow').node())
        chatButtonGui = loader.loadModel('models/gui/triangle')
        chatButtonGui.setScale(0.1)
        chatButtonGui.flattenStrong()
        lookoutButtonGui = loader.loadModel('models/gui/lookout_gui')
        lookoutButtonGui.setScale(0.4)
        lookoutButtonGui.flattenStrong()
        NametagGlobals.setCamera(self.cam)
        NametagGlobals.setArrowModel(arrow)
        NametagGlobals.setNametagCard(card, VBase4(-1, 1, -1, 1))
        if self.mouseWatcherNode:
            NametagGlobals.setMouseWatcher(self.mouseWatcherNode)
        NametagGlobals.setSpeechBalloon3d(speech3d)
        NametagGlobals.setThoughtBalloon3d(thought3d)
        NametagGlobals.setSpeechBalloon2d(speech2d)
        NametagGlobals.setThoughtBalloon2d(thought3d)
        NametagGlobals.setPageButton(PGButton.SReady, chatButtonGui.find('**/triangle'))
        NametagGlobals.setPageButton(PGButton.SDepressed, chatButtonGui.find('**/triangle_down'))
        NametagGlobals.setPageButton(PGButton.SRollover, chatButtonGui.find('**/triangle_over'))
        NametagGlobals.setQuitButton(PGButton.SReady, lookoutButtonGui.find('**/lookout_close_window'))
        NametagGlobals.setQuitButton(PGButton.SDepressed, lookoutButtonGui.find('**/lookout_close_window_down'))
        NametagGlobals.setQuitButton(PGButton.SRollover, lookoutButtonGui.find('**/lookout_close_window_over'))
        rolloverSound = PiratesGuiGlobals.getDefaultRolloverSound()
        clickSound = PiratesGuiGlobals.getDefaultClickSound()
        NametagGlobals.setRolloverSound(rolloverSound)
        NametagGlobals.setClickSound(clickSound)
        NametagGlobals.setToon(self.cam)
        self.marginManager = MarginManager()
        self.margins = self.aspect2d.attachNewNode(self.marginManager, DirectGuiGlobals.MIDGROUND_SORT_INDEX + 1)
        mm = self.marginManager
        self.leftCells = [mm.addGridCell(0, 1.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(0, 2.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(0, 3.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)]
        self.bottomCells = [
         mm.addGridCell(0.5, 0.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(1.5, 0.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(2.5, 0.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(3.5, 0.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(4.5, 0.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)]
        self.rightCells = [
         mm.addGridCell(5, 2.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop), mm.addGridCell(5, 1.5, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)]

    def getShardPopLimits(self):
        low = self.config.GetInt('shard-pop-limit-low', 100)
        mid = self.config.GetInt('shard-pop-limit-mid', 200)
        high = self.config.GetInt('shard-pop-limit-high', 300)
        return (
         low, mid, high)

    def toggleMarketingViewer(self):
        if not self.marketingViewerOn:
            if self.cr:
                if self.cr.tutorialObject and self.cr.tutorialObject.map:
                    self.cr.tutorialObject.map.marketingOn()
                elif self.cr.avCreate:
                    self.cr.avCreate.marketingOn()
            self.marketingViewerOn = True
        else:
            if self.cr:
                if self.cr.tutorialObject and self.cr.tutorialObject.map:
                    self.cr.tutorialObject.map.marketingOff()
                elif self.cr.avCreate:
                    self.cr.avCreate.marketingOff()
            self.marketingViewerOn = False

    def setOverrideShipVisibility(self, value):
        self.overrideShipVisibility = value
        if value:
            self.shipsVisibleFromIsland = 2
        elif localAvatar.guiMgr.mainMenu and localAvatar.guiMgr.mainMenu.gameOptions:
            localAvatar.guiMgr.mainMenu.gameOptions.updateShipVisibility()
        else:
            self.shipsVisibleFromIsland = self.options.ocean_visibility
            messenger.send('ship_vis_change', [self.options.ocean_visibility])

    def getVelvetDisplayResolutions(self, bits_per_pixel, pipe):
        self.getDisplayResolutions(bits_per_pixel, pipe)
        self.windowed_resolution_table = []
        total_modes = embedded.getCountWindowModes()
        for i in range(total_modes):
            m = embedded.getAtWindowModeDef(i)
            self.windowed_resolution_table = self.windowed_resolution_table + [(m['want_size_x'], m['want_size_y'])]

    def getDisplayResolutions(self, bits_per_pixel, pipe):
        di = pipe.getDisplayInformation()
        total_display_modes = di.getTotalDisplayModes()
        if di.getDisplayState() == DisplayInformation.DSSuccess and total_display_modes > 0:
            resolution_table = []
            index = 0
            while index < total_display_modes:
                if di.getDisplayModeBitsPerPixel(index) == bits_per_pixel:
                    if di.getDisplayModeFullscreenOnly(index) == False:
                        if di.getDisplayModeWidth(index) >= self.MinimumHorizontalResolution and di.getDisplayModeHeight(index) >= self.MinimumVerticalResolution:
                            resolution = (
                             di.getDisplayModeWidth(index), di.getDisplayModeHeight(index))
                            if resolution not in resolution_table:
                                if di.getDisplayModeWidth(index) <= di.getMaximumWindowWidth() and di.getDisplayModeHeight(index) <= di.getMaximumWindowHeight():
                                    resolution_table = resolution_table + [resolution]
                index += 1

            widescreen_resolution_table = [
             (1280, 720), (1920, 1080)]
            index = 0
            while index < len(widescreen_resolution_table):
                resolution = widescreen_resolution_table[index]
                if resolution not in resolution_table:
                    if resolution[0] <= di.getMaximumWindowWidth() and resolution[1] <= di.getMaximumWindowHeight():
                        resolution_table = resolution_table + [resolution]
                index += 1

            width = self.config.GetInt('custom-window-width', 0)
            height = self.config.GetInt('custom-window-height', 0)
            if width > 0 and height > 0:
                resolution = (
                 width, height)
                if resolution not in resolution_table:
                    if di.getDisplayModeWidth(index) <= di.getMaximumWindowWidth() and di.getDisplayModeHeight(index) <= di.getMaximumWindowHeight():
                        resolution_table = resolution_table + [resolution]
            self.windowed_resolution_table = resolution_table
            resolution_table = []
            index = 0
            while index < total_display_modes:
                if di.getDisplayModeBitsPerPixel(index) == bits_per_pixel:
                    if di.getDisplayModeWidth(index) >= self.MinimumHorizontalResolution and di.getDisplayModeHeight(index) >= self.MinimumVerticalResolution:
                        resolution = (
                         di.getDisplayModeWidth(index), di.getDisplayModeHeight(index))
                        if resolution not in resolution_table:
                            resolution_table = resolution_table + [resolution]
                index += 1

            if False:
                resolution = (2048, 1536)
                resolution_table = resolution_table + [resolution]
            self.fullscreen_resolution_table = resolution_table
        else:
            default_windowed_resolution_table = [(800, 600), (1024, 768), (1280, 1024), (1600, 1200), (1280, 720), (1920, 1080)]
            default_fullscreen_resolution_table = [(800, 600), (1024, 768), (1280, 1024), (1600, 1200)]
            self.windowed_resolution_table = default_windowed_resolution_table
            self.fullscreen_resolution_table = default_fullscreen_resolution_table

    def width_to_resolution_id(self, width):
        id = 1
        index = 0
        total_resolutions = len(self.resolution_table)
        while index < total_resolutions:
            if width == GameOptions.resolution_table[index][0]:
                id = index
                break
            index += 1

        return id

    def hideEffects(self):
        self.effectsRoot.hide()

    def showEffects(self):
        self.effectsRoot.show()

    def zoneLODCollLoop(self, task):
        if self.zoneLODTarget:
            self.lodTrav.traverse(self.zoneLODTarget)
        return Task.cont

    def enableZoneLODs(self, target):
        self.zoneLODTarget = target
        taskMgr.add(self.zoneLODCollLoop, 'zoneLODloop', priority=39)

    def disableZoneLODs(self):
        self.zoneLODTarget = None
        self.zoneLODEventHandler.clear()
        taskMgr.remove('zoneLODloop')
        return
