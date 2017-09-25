from direct.showbase.ShowBaseGlobal import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from otp.avatar import Avatar
from otp.chat import ChatManager
import string
from direct.showbase import PythonUtil
from otp.otpbase import OTPGlobals
from direct.distributed.ClockDelta import *
from otp.ai import MagicWordManager
from pirates.pirate import DistributedPlayerPirate
from pirates.npc import DistributedNPCTownfolk
from direct.distributed import DistributedCartesianGrid
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.RadarUtil import RadarUtil
from pirates.cutscene import Cutscene, CutsceneData
from pirates.effects.Fireflies import Fireflies
from pirates.effects.GroundFog import GroundFog
from pirates.effects.Bonfire import Bonfire
from pirates.effects.CeilingDust import CeilingDust
from pirates.effects.CeilingDebris import CeilingDebris
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.DarkWaterFog import DarkWaterFog
from pirates.ship import DistributedSimpleShip
from pirates.world import WorldGlobals
from pirates.effects.FireworkGlobals import *
from pirates.effects.FireworkShowManager import FireworkShowManager
from pirates.piratesbase import PLocalizer

class PiratesMagicWordManager(MagicWordManager.MagicWordManager):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesMagicWordManager')
    neverDisable = 1
    GameAvatarClass = DistributedPlayerPirate.DistributedPlayerPirate

    def __init__(self, cr):
        MagicWordManager.MagicWordManager.__init__(self, cr)
        self.pendingCameraReparent = None
        self.originalLocation = None
        self.groundFog = None
        self.fireflies = None
        self.rainDrops = None
        self.rainMist = None
        self.rainSplashes = None
        self.rainSplashes2 = None
        self.stormEye = None
        self.stormRing = None
        self.fishCamEnabled = False


    def generate(self):
        MagicWordManager.MagicWordManager.generate(self)
        self.accept('magicWord', self.b_setMagicWord)


    def doLoginMagicWords(self):
        MagicWordManager.MagicWordManager.doLoginMagicWords(self)
        if base.config.GetBool('want-chat', 0):
            self.d_setMagicWord('~chat', localAvatar.doId, 0)

        if base.config.GetBool('want-run', 0) or base.config.GetBool('want-pirates-run', 0):
            self.toggleRun()

        if base.config.GetBool('immortal-mode', 0):
            self.d_setMagicWord('~immortal', localAvatar.doId, 0)



    def disable(self):
        self.ignore('magicWord')
        MagicWordManager.MagicWordManager.disable(self)
        if self.pendingCameraReparent:
            base.cr.relatedObjectMgr.abortRequest(self.pendingCameraReparent)
            self.pendingCameraReparent = None



    def doMagicWord(self, word, avId, zoneId):

        def wordIs(w, word = word):
            if not word[:len(w) + 1] == '%s ' % w:
                pass
            return word == w

        if word == '~rio':
            self.doMagicWord('~run', avId, zoneId)

        if MagicWordManager.MagicWordManager.doMagicWord(self, word, avId, zoneId) == 1:
            pass
        
        if word == '~walk':
            localAvatar.b_setGameState('LandRoam')
            localAvatar.motionFSM.on()
        elif word == '~players':
            players = base.cr.doFindAll('DistributedPlayerPirate')
            for player in players:
                playerText = '%s %s' % (player.getName(), player.doId)
                base.talkAssistant.receiveGameMessage(playerText)

        elif word == '~rocketman':
            if localAvatar.rocketOn == 0:
                localAvatar.startRocketJumpMode()
                base.talkAssistant.receiveGameMessage('Zero hour nine a.m. (Bill Shattner Version)')
            else:
                localAvatar.endRocketJumpMode()
                base.talkAssistant.receiveGameMessage("And I think it's gonna be a long long time")
        elif word == '~shipUpgrade':
            localAvatar.guiMgr.toggleShipUpgrades()
        elif word == '~shipCam':
            if base.shipLookAhead:
                base.talkAssistant.receiveGameMessage('Ship Look ahead camera off!')
                base.setShipLookAhead(0)
            else:
                base.talkAssistant.receiveGameMessage('Ship Look ahead camera on!')
                base.setShipLookAhead(1)
        elif word == '~time':
            base.talkAssistant.receiveGameMessage('The time is %s' % base.cr.timeOfDayManager.getCurrentIngameTime())
        elif word == '~todDebug':
            base.cr.timeOfDayManager.toggleDebugMode()
        elif word == '~vismask':
            base.talkAssistant.receiveGameMessage('Vis Mask %s' % localAvatar.invisibleMask)
        elif word == '~target':
            localAvatar.setAvatarViewTarget()
        elif word == '~collisions_on':
            pass
        elif word == '~collisions_off':
            pass
        elif word == '~topten':
            base.cr.guildManager.requestLeaderboardTopTen()
        elif word == '~airender':
            pass
        elif __dev__ and wordIs('~shiphat'):
            args = word.split()
            if hasattr(localAvatar, 'shipHat'):
                localAvatar.shipHat.modelRoot.detachNode()
                localAvatar.shipHat = None

            if len(args) == 1:
                ship = base.shipFactory.getShip(23)
            else:
                shipClass = args[1]
                ship = base.shipFactory.getShip(int(shipClass))
            ship.startSailing()
            ship.modelRoot.reparentTo(localAvatar.headNode)
            ship.modelRoot.setR(90)
            ship.modelRoot.setP(-90)
            ship.modelRoot.setX(0.80000000000000004)
            ship.modelRoot.setScale(0.0040000000000000001)
            ship.modelRoot.setZ(-0.20000000000000001)
            ship.forceLOD(2)
            ship.modelCollisions.detachNode()
            localAvatar.shipHat = ship
        elif __dev__ and wordIs('~cr'):
            pass
        elif __dev__ and wordIs('~watch'):
            if taskMgr.hasTaskNamed('lookAtDude'):
                taskMgr.remove('lookAtDude')
                localAvatar.guiMgr.setIgnoreAllKeys(False)
                localAvatar.guiMgr.combatTray.initCombatTray()
                localAvatar.unstash()
            else:
                args = word.split()
                if len(args) >= 2:
                    tgtDoId = int(args[1])

                    def doHeadsUp(task = None):
                        targetObj = self.cr.doId2do.get(tgtDoId)
                        if targetObj:
                            localAvatar.lookAt(targetObj)

                        return Task.cont

                    taskMgr.add(doHeadsUp, 'lookAtDude')
                    localAvatar.guiMgr.setIgnoreAllKeys(True)
                    localAvatar.guiMgr.combatTray.skillMapping.clear()
                    localAvatar.stash()
                else:
                    print 'need a target object doId to watch'
        elif __dev__ and wordIs('~ccNPC') or wordIs('~ccShip'):
            pass
        elif wordIs('~bonfire'):
            bf = Bonfire()
            bf.reparentTo(render)
            bf.setPos(localAvatar, 0, 0, 0)
            bf.startLoop()
            print 'bonfire at %s, %s' % (localAvatar.getPos(), localAvatar.getHpr())
        elif __dev__ and wordIs('~mario'):
            localAvatar.toggleMario()
        elif wordIs('~islandShips'):
            args = word.split()

            try:
                if args[1] == '1':
                    localAvatar.getParentObj().setOceanVisEnabled(1)
                    localAvatar.getParentObj().setFlatShips(0)
                else:
                    localAvatar.getParentObj().setOceanVisEnabled(0)
            except:
                pass

        elif wordIs('~swamp'):
            if self.fireflies:
                self.fireflies.destroy()
                self.fireflies = None
                self.groundFog.destroy()
                self.groundFog = None
            else:
                self.fireflies = Fireflies()
                if self.fireflies:
                    self.fireflies.reparentTo(localAvatar)
                    self.fireflies.startLoop()

                self.groundFog = GroundFog()
                if self.groundFog:
                    self.groundFog.reparentTo(localAvatar)
                    self.groundFog.startLoop()

        elif wordIs('~darkfog'):
            if self.groundFog:
                self.groundFog.destroy()
                self.groundFog = None
            else:
                self.groundFog = DarkWaterFog()
                if self.groundFog:
                    self.groundFog.reparentTo(localAvatar)
                    self.groundFog.startLoop()

        elif wordIs('~dust'):
            effect = CeilingDust.getEffect()
            if effect:
                effect.reparentTo(localAvatar)
                effect.setPos(0, 0, 10)
                effect.play()

            effect = CeilingDebris.getEffect()
            if effect:
                effect.reparentTo(localAvatar)
                effect.setPos(0, 0, 20)
                effect.play()

            cameraShakerEffect = CameraShaker()
            cameraShakerEffect.reparentTo(localAvatar)
            cameraShakerEffect.setPos(0, 0, 0)
            cameraShakerEffect.shakeSpeed = 0.050000000000000003
            cameraShakerEffect.shakePower = 4.5
            cameraShakerEffect.numShakes = 2
            cameraShakerEffect.scalePower = 1
            cameraShakerEffect.play(80.0)
        elif wordIs('~rain'):
            if self.rainDrops:
                self.rainDrops.stopLoop()
                self.rainDrops = None
                if self.rainMist:
                    self.rainMist.stopLoop()
                    self.rainMist = None

                if self.rainSplashes:
                    self.rainSplashes.stopLoop()
                    self.rainSplashes = None

                if self.rainSplashes2:
                    self.rainSplashes2.stopLoop()
                    self.rainSplashes2 = None

            else:
                from pirates.effects.RainDrops import RainDrops
                self.rainDrops = RainDrops(base.camera)
                self.rainDrops.reparentTo(render)
                self.rainDrops.startLoop()
                from pirates.effects.RainMist import RainMist
                self.rainMist = RainMist(base.camera)
                self.rainMist.reparentTo(render)
                self.rainMist.startLoop()
                from pirates.effects.RainSplashes import RainSplashes
                self.rainSplashes = RainSplashes(base.camera)
                self.rainSplashes.reparentTo(render)
                self.rainSplashes.startLoop()
                from pirates.effects.RainSplashes2 import RainSplashes2
                self.rainSplashes2 = RainSplashes2(base.camera)
                self.rainSplashes2.reparentTo(render)
                self.rainSplashes2.startLoop()
        elif wordIs('~clouds'):
            args = word.split()
            if len(args) >= 2:
                level = int(args[1])
                base.cr.timeOfDayManager.skyGroup.transitionClouds(level).start()

        elif wordIs('~storm'):
            if self.stormEye:
                self.stormEye.stopLoop()
                self.stormEye = None
                if self.stormRing:
                    self.stormRing.stopLoop()
                    self.stormRing = None

            else:
                args = word.split()
                grid = 0
                if len(args) > 1:
                    grid = int(args[1])

                pos = Vec3(base.cr.doId2do[201100017].getZoneCellOrigin(grid)[0], base.cr.doId2do[201100017].getZoneCellOrigin(grid)[1], base.cr.doId2do[201100017].getZoneCellOrigin(grid)[2])
                StormEye = StormEye
                import pirates.effects.StormEye
                self.stormEye = StormEye()
                self.stormEye.reparentTo(render)
                self.stormEye.startLoop()
                StormRing = StormRing
                import pirates.effects.StormRing
                self.stormRing = StormRing()
                self.stormRing.reparentTo(render)
                self.stormRing.setZ(100)
                self.stormRing.startLoop()
        elif wordIs('~alight'):
            args = word.split()
            if len(args) > 3:
                color = Vec4(float(args[1]), float(args[2]), float(args[3]), 1)
                base.cr.timeOfDayManager.alight.node().setColor(color)

        elif wordIs('~dlight'):
            args = word.split()
            if len(args) > 3:
                color = Vec4(float(args[1]), float(args[2]), float(args[3]), 1)
                base.cr.timeOfDayManager.dlight.node().setColor(color)

        elif wordIs('~fog'):
            args = word.split()
            if len(args) > 3:
                color = Vec4(float(args[1]), float(args[2]), float(args[3]), 1)
                base.cr.timeOfDayManager.fog.setColor(color)

            if len(args) > 4:
                base.cr.timeOfDayManager.fog.setExpDensity(float(args[4]))

            if len(args) == 2:
                base.cr.timeOfDayManager.fog.setExpDensity(float(args[1]))

        elif __dev__ and wordIs('~turbo'):
            localAvatar.toggleTurbo()
        elif __dev__ and wordIs('~joincrew'):
            base.cr.crewManager.requestNewCrew()
        elif wordIs('~tm'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_TM, 'treasureMapCove')
        elif wordIs('~tml'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, WorldGlobals.PiratesWorldSceneFileBase)
        elif wordIs('~pg'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_PG, 'ParlorWorld')
        elif wordIs('~pgvip'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_PG, 'ParlorVIPWorld')
        elif wordIs('~pgl'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, WorldGlobals.PiratesWorldSceneFileBase)
        elif wordIs('~tutorial'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_TUTORIAL, 'RambleshackWorld', self.cr.playGame.handleTutorialGeneration)
        elif wordIs('~tutoriall'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, WorldGlobals.PiratesWorldSceneFileBase)
        elif wordIs('~pvp'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_PVP, 'pvp_mayhemWorld1')
        elif wordIs('~pirateer'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_PVP, 'pirateerMap')
        elif wordIs('~pvpl'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, WorldGlobals.PiratesWorldSceneFileBase)
        elif wordIs('~tortuga'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'TortugaWorld')
        elif wordIs('~portRoyal'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'PortRoyalWorld')
        elif wordIs('~delFuego'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'DelFuegoWorld')
        elif wordIs('~bilgewater'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'BilgewaterWorld')
        elif wordIs('~kingshead'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'KingsheadWorld')
        elif wordIs('~cuba'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CubaWorld')
        elif wordIs('~rumrunner'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'RumrunnerWorld')
        elif wordIs('~wildisland'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'WildIslandWorld')
        elif wordIs('~caveA'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CaveAWorld')
        elif wordIs('~caveB'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CaveBWorld')
        elif wordIs('~caveC'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CaveCWorld')
        elif wordIs('~caveD'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CaveDWorld')
        elif wordIs('~caveE'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'CaveEWorld')
        elif wordIs('~jungleA'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'JungleTestWorldA')
        elif wordIs('~jungleB'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'JungleTestWorld')
        elif wordIs('~jungleC'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'JungleTestWorldC')
        elif wordIs('~swampA'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'SwampTestWorld')
        elif wordIs('~mainWorld'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, WorldGlobals.PiratesWorldSceneFileBase)
        elif wordIs('~gameArea'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_GENERIC, 'GameAreaSandbox')
        elif wordIs('~blackpearl') or wordIs('~bp'):
            args = word.split()
            if len(args) == 1:
                self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_TM, 'BlackpearlWorld')

        elif wordIs('~scrimmage'):
            self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_SCRIMMAGE, 'ScrimmageTestWorld')
        elif wordIs('~fireworks') or wordIs('~fw'):
            args = word.split()
            if len(args) >= 2 and args[1] in [
                'show',
                's']:
                if len(args) >= 3:
                    showType = args[2]

                timestamp = 0.0
                if len(args) >= 4:
                    timestamp = args[3]

                if base.cr.activeWorld:
                    localAvatar.getParentObj().fireworkShowType = int(showType)
                    localAvatar.getParentObj().beginFireworkShow(timeStamp = timestamp)

            elif len(args) >= 2 and args[1] in [
                'type',
                't']:
                fireworkType = 0
                if len(args) >= 3:
                    fireworkType = int(args[2])

                Firework = Firework
                import pirates.effects.Firework
                firework = Firework(fireworkType)
                firework.reparentTo(render)
                firework.setPos(Point3(10525, 19000, 245))
                firework.play()
            elif len(args) >= 2 and args[1] in [
                'effect',
                'e']:
                trailType = 0
                burstType = 0
                if len(args) >= 3:
                    burstType = int(args[2])

                if len(args) >= 4:
                    trailType = int(args[3])

                FireworkEffect = FireworkEffect
                import pirates.effects.FireworkEffect
                firework = FireworkEffect(burstType, trailType)
                firework.reparentTo(render)
                firework.setPos(Point3(10525, 19000, 245))
                firework.play()

        elif wordIs('~te'):
            if localAvatar.gameFSM.getCurrentOrNextState() == 'LandRoam':
                localAvatar.b_setGameState('TeleportOut')
            elif localAvatar.gameFSM.getCurrentOrNextState() == 'TeleportOut':
                localAvatar.b_setGameState('LandRoam')

        elif wordIs('~lfa'):
            args = word.split()
            activityName = None
            if len(args) >= 2:
                activityName = args[1]

            if activityName == 'blackjack':
                localAvatar.requestActivity(PiratesGlobals.GAME_STYLE_BLACKJACK)
            elif activityName == 'poker':
                localAvatar.requestActivity(PiratesGlobals.GAME_STYLE_POKER)
            elif activityName == 'pvp':
                localAvatar.requestActivity(PiratesGlobals.GAME_TYPE_PVP)
            elif activityName == 'tm':
                localAvatar.requestActivity(PiratesGlobals.GAME_TYPE_TM)
            elif activityName == 'hsa':
                localAvatar.requestActivity(PiratesGlobals.GAME_TYPE_HSA)
            elif activityName == 'mmp':
                self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, WorldGlobals.PiratesWorldSceneFileBase)

        elif wordIs('~term') or wordIs('terminator'):
            localAvatar.setEquippedWeapons([
                10103,
                10106,
                10115])
            localAvatar.d_requestEquipWeapons([
                10103,
                10106,
                10115])
        elif wordIs('~battleRandom'):
            args = word.split()
            if len(args) >= 2:
                command = args[1]
                if command == 'resync':
                    localAvatar.battleRandom.resync()
                    self.notify.info('Client Battle random resynced, counter=0')

            else:
                response = 'Client Battle random attack counter=%s  main counter=%s' % (localAvatar.battleRandom.attackCounter, localAvatar.battleRandom.mainCounter)
                self.setMagicWordResponse(response)
        elif wordIs('~cutscene'):
            args = word.split()
            name = None
            if len(args) >= 2:
                csId = args[1]
            else:
                csId = base.config.GetString('default-cutscene', '0')
            if int(csId) >= len(CutsceneData.CutsceneNames):
                return None

            name = CutsceneData.CutsceneNames[int(csId)]
            cs = PythonUtil.ScratchPad()

            def destroyCutscene(cs = cs):
                cs.cutscene.destroy()

            c = Cutscene.Cutscene(self.cr, name, PythonUtil.DelayedFunctor(destroyCutscene, '~cutscene-destroy'))
            cs.cutscene = c
            c.play()
            destroyCutscene = None
        elif wordIs('~forceLod'):
            for n in render.findAllMatches('**/+LODNode'):
                n.node().forceSwitch(n.node().getHighestSwitch())

        elif wordIs('~wave'):
            args = word.split()
            patch = base.cr.doFind('OceanGrid').water.patch
            if len(args) < 4:
                response = '~wave num amplitude wavelength speed'
                numWaves = patch.getNumWaves()
                num = 0
                while numWaves > 0:
                    if patch.isWaveEnabled(num):
                        numWaves -= 1
                        if patch.getWaveTarget(num) != SeaPatchRoot.WTZ or patch.getWaveFunc(num) != SeaPatchRoot.WFSin:
                            response = '%s\n%s NON-SINE-WAVE' % (response, num)
                        else:
                            response = '%s\n%s amp=%s len=%s spd=%s' % (response, num, patch.getWaveAmplitude(num), patch.getWaveLength(num), patch.getWaveSpeed(num))

                    num += 1
            else:
                num = int(args[1])
                amplitude = float(args[2])
                wavelength = float(args[3])
                speed = float(args[4])
                patch.enableWave(num)
                patch.setWaveTarget(num, SeaPatchRoot.WTZ)
                patch.setWaveFunc(num, SeaPatchRoot.WFSin)
                patch.setChoppyK(num, 0)
                patch.setWaveAmplitude(num, amplitude)
                patch.setWaveLength(num, wavelength)
                patch.setWaveSpeed(num, speed)
                response = 'wave %s modified' % num
            self.setMagicWordResponse(response)
        elif wordIs('~roll'):
            args = word.split()
            if len(args) < 2:
                response = '~roll angle [fakeMass]'
            elif localAvatar.ship is None:
                response = 'not on a ship'
            elif len(args) > 2:
                localAvatar.ship._rocker.setFakeMass(float(args[2]))

            localAvatar.ship.addRoll(float(args[1]))
            response = 'rolling!'
            self.setMagicWordResponse(response)
        elif wordIs('~ru'):
            if hasattr(self, 'radarUtil') and self.radarUtil and not self.radarUtil.isDestroyed():
                self.radarUtil.destroy()
            else:
                self.radarUtil = RadarUtil()
        elif __dev__ and wordIs('~todpanel'):
            tod = base.cr.timeOfDayManager
            TimeOfDayPanel = TimeOfDayPanel
            import pirates.leveleditor
            p = TimeOfDayPanel.TimeOfDayPanel(tod)
        elif __dev__ and wordIs('~kraken'):
            args = word.split()[1:]
            if args and args[0]:
                if not hasattr(base, 'oobeMode') or not (base.oobeMode):
                    base.oobe()
                    base.oobeCamera.wrtReparentTo(render)


        elif wordIs('~pvpmoney') or wordIs('~pvpinfamy'):
            if localAvatar.ship and localAvatar.ship.renownDisplay:
                taskMgr.doMethodLater(2.0, localAvatar.ship.renownDisplay.loadRank, 'pvp-infamy-display', [])

            if localAvatar.guiMgr and localAvatar.guiMgr.pvpPanel and hasattr(localAvatar.guiMgr.pvpPanel, 'renownDisplay') and localAvatar.guiMgr.pvpPanel.renownDisplay:
                taskMgr.doMethodLater(2.0, localAvatar.guiMgr.pvpPanel.renownDisplay.loadRank, 'pvp-infamy-display', [])

            if localAvatar.guiMgr and localAvatar.guiMgr.titlesPage:
                taskMgr.doMethodLater(2.0, localAvatar.guiMgr.titlesPage.refresh, 'titles-refresh', [])

        elif wordIs('~profileCard'):
            args = word.split()
            if len(args) >= 2:
                profileId = int(args[1])
            else:
                profileId = localAvatar.getDoId()
            localAvatar.guiMgr.handleAvatarDetails(profileId)
        elif wordIs('~gmNameTag'):
            args = word.split()
            if len(args) < 2 and localAvatar.isGM():
                response = PLocalizer.MAGICWORD_GMNAMETAG
                self.setMagicWordResponse(response)

            if len(args) >= 2 and localAvatar.isGM():
                if args[1] == 'enable':
                    localAvatar.setGMNameTagState(1)
                elif args[1] == 'disable':
                    localAvatar.setGMNameTagState(0)
                elif args[1] == 'setString':
                    xCount = 0
                    stringToSet = ''
                    for i in args:
                        if xCount < 2:
                            pass
                        1
                        stringToSet = '%s %s' % (stringToSet, args[xCount])
                        xCount += 1

                    localAvatar.setGMNameTagString(stringToSet)
                elif args[1] == 'setColor':
                    localAvatar.setGMNameTagColor(args[2])


        elif wordIs('~liveCam'):
            LiveCamTransforms = {
                '1': [
                    Vec3(-385.77600000000001, -2369.6399999999999, 52.464399999999998),
                    Vec3(-18.0412, -3.2476600000000002, 0),
                    39.307600000000001,
                    0],
                '2': [
                    Vec3(79.119500000000002, -2521.2600000000002, 52.464399999999998),
                    Vec3(-18.0412, -3.2476600000000002, 0),
                    39.307600000000001,
                    0],
                '3': [
                    Vec3(2858.3499999999999, 931.11099999999999, 37.956400000000002),
                    Vec3(-29.8904, -7.1252500000000003, 0),
                    39.307600000000001,
                    1],
                '4': [
                    Vec3(3551.9299999999998, 532.43700000000001, 37.956400000000002),
                    Vec3(-29.8904, -7.1252500000000003, 0),
                    39.307600000000001,
                    1],
                '5': [
                    Vec3(4245.5200000000004, 133.76300000000001, 37.956400000000002),
                    Vec3(-29.8904, -7.1252500000000003, 0),
                    39.307600000000001,
                    1],
                '6': [
                    Vec3(4939.1000000000004, -264.911, 37.956400000000002),
                    Vec3(-29.8904, -7.1252500000000003, 0),
                    39.307600000000001,
                    1] }
            lodNodes = render.findAllMatches('**/+LODNode')
            for i in xrange(0, lodNodes.getNumPaths()):
                lodNodes[i].node().forceSwitch(lodNodes[i].node().getHighestSwitch())

            localAvatar.clearInterestNamed(None, [
                'liveCam'])
            localAvatar.getParentObj().setOceanVisEnabled(0)
            args = word.split()
            if len(args) > 1:
                camNum = args[1]
                camData = LiveCamTransforms[camNum]
                localAvatar.cameraFSM.request('Control')
                if camData[3]:
                    camParent = render
                else:
                    camParent = localAvatar.getParentObj()
                base.cam.reparentTo(camParent)
                base.cam.setPos(camData[0])
                base.cam.setHpr(camData[1])
                base.camLens.setFov(camData[2])
                if camData[3] == 0:
                    localAvatar.setInterest(localAvatar.getParentObj().doId, [
                        11622,
                        11621,
                        11443,
                        11442,
                        11620,
                        11619,
                        11441,
                        11086,
                        11085,
                        11263,
                        11264,
                        11265,
                        11444,
                        11266,
                        11267,
                        11445,
                        11446,
                        11268,
                        11269,
                        11447,
                        11449,
                        11270,
                        11448,
                        11271,
                        11272,
                        11450,
                        11451,
                        11273,
                        11095,
                        11093,
                        11094,
                        11092,
                        11091,
                        11090,
                        11089,
                        11088,
                        11087,
                        11623,
                        11624,
                        11625,
                        11626,
                        11627,
                        11628,
                        11629,
                        11807,
                        11630,
                        11452,
                        11274,
                        11096,
                        11275,
                        11277,
                        11276,
                        11099,
                        11098,
                        11097,
                        11455,
                        11454,
                        11453,
                        11631,
                        11632,
                        11633,
                        11100,
                        11278,
                        11456,
                        11634,
                        11990,
                        11812,
                        11811,
                        11989,
                        11988,
                        11987,
                        11809,
                        11810,
                        11808,
                        11986,
                        11985,
                        12164,
                        12163,
                        12162,
                        11984,
                        11806,
                        11805,
                        11983,
                        12161,
                        12160,
                        11982,
                        11804,
                        11803,
                        11981,
                        11980,
                        12159,
                        11802,
                        11801,
                        11979,
                        12158,
                        12157,
                        12156,
                        11978,
                        11799,
                        11800,
                        11977,
                        11798,
                        11976,
                        11975,
                        11797,
                        11796,
                        11974,
                        11084,
                        11262,
                        11440,
                        11618,
                        11795,
                        11617,
                        11439,
                        11261,
                        11083,
                        11082,
                        11260,
                        11438,
                        11616,
                        11794,
                        11793,
                        11615,
                        11437,
                        11081,
                        11259,
                        11080,
                        11258,
                        11436,
                        11614,
                        11435,
                        11257,
                        11079,
                        11973,
                        11972,
                        12155,
                        12154,
                        12153], [
                        'liveCam'])
                else:
                    localAvatar.getParentObj().setOceanVisEnabled(1)
                    localAvatar.getParentObj().setFlatShips(0)
            else:
                localAvatar.cameraFSM.request('FPS')
                base.cam.reparentTo(camera)
                base.cam.setPos(0, 0, 0)
                base.cam.setHpr(0, 0, 0)
                base.camLens.setFov(63.741999999999997)
        elif wordIs('~showCams'):
            render.findAllMatches('**/liveCamParent*').detach()
            LiveCamTransforms = {
                '1': [
                    Vec3(-385.77600000000001, -2369.6399999999999, 52.464399999999998),
                    Vec3(-18.0412, -3.2476600000000002, 0),
                    39.307600000000001,
                    0],
                '2': [
                    Vec3(79.119500000000002, -2521.2600000000002, 52.464399999999998),
                    Vec3(-18.0412, -3.2476600000000002, 0),
                    39.307600000000001,
                    0],
                '3': [
                    Vec3(2858.3499999999999, 931.11099999999999, 37.956400000000002),
                    Vec3(-29.8904, -7.1252500000000003, 0),
                    39.307600000000001,
                    1],
                '4': [
                    Vec3(3551.9299999999998, 532.43700000000001, 37.956400000000002),
                    Vec3(-29.8904, -7.1252500000000003, 0),
                    39.307600000000001,
                    1],
                '5': [
                    Vec3(4245.5200000000004, 133.76300000000001, 37.956400000000002),
                    Vec3(-29.8904, -7.1252500000000003, 0),
                    39.307600000000001,
                    1],
                '6': [
                    Vec3(4939.1000000000004, -264.911, 37.956400000000002),
                    Vec3(-29.8904, -7.1252500000000003, 0),
                    39.307600000000001,
                    1] }
            camModel = NodePath('camera')
            lens = PerspectiveLens()
            lens.setFov(base.camLens.getFov())
            lens.setFov(39.307600000000001)
            g = lens.makeGeometry()
            gn = GeomNode('frustum')
            gn.addGeom(g)
            gnp = camModel.attachNewNode(gn)
            if not localAvatar.getShip():
                for camNum in range(1, 3):
                    camData = LiveCamTransforms[str(camNum)]
                    camParent = localAvatar.getParentObj().attachNewNode('liveCamParent-%s' % camNum)
                    camParent.setPos(camData[0])
                    camParent.setHpr(camData[1])
                    camParent.setScale(10)
                    camModel.instanceTo(camParent)

            else:
                for camNum in range(3, 7):
                    camData = LiveCamTransforms[str(camNum)]
                    camParent = render.attachNewNode('liveCamParent-%s' % camNum)
                    camParent.setPos(camData[0])
                    camParent.setHpr(camData[1])
                    camParent.setScale(10)
                    camModel.instanceTo(camParent)

        elif wordIs('~hideCams'):
            render.findAllMatches('**/liveCamParent*').detach()
        elif wordIs('~dropBlockers'):
            ga = localAvatar.getParentObj()
            blockers = ga.findAllMatches('**/blocker_*')
            blockers.stash()
        elif __dev__ and wordIs('~effects'):
            args = word.split()
            self.configEffects(args)
        elif __dev__ and wordIs('~shipsRock'):
            configIs = 'ships-rock'
            args = word.split()
            self.configShipsRock(configIs, args)
        elif __dev__ and wordIs('~shipsRockWithoutWaves'):
            configIs = 'ships-rock-without-waves'
            args = word.split()
            self.configShipsRock(configIs, args)
        elif __dev__ and wordIs('~wantCompassTask'):
            self.configToggleBool('want-compass-task')
        elif __dev__ and wordIs('~wantPatchie'):

            def turnOffSeapatch():
                if hasattr(base.cr.activeWorld.worldGrid, 'cleanupWater'):
                    base.cr.activeWorld.worldGrid.cleanupWater()



            def turnOnSeapatch():
                if hasattr(base.cr.activeWorld.worldGrid, 'setupWater'):
                    base.cr.activeWorld.worldGrid.setupWater()


            self.configToggleBool('want-compass-task', offCode = turnOffSeapatch, onCode = turnOnSeapatch)
        elif __dev__ and wordIs('~wantShipColl'):
            if localAvatar.ship and localAvatar.ship.controlManager.controls.has_key('ship'):
                if localAvatar.ship.controlManager.controls['ship'].collisionsActive:
                    localAvatar.ship.controlManager.controls['ship'].setCollisionsActive(0)
                    self.setMagicWordResponse('ship collisions OFF')
                else:
                    localAvatar.ship.controlManager.controls['ship'].setCollisionsActive()
                    self.setMagicWordResponse('ship collisions ON')
            else:
                self.setMagicWordResponse('get on a ship!')
        elif __dev__ and wordIs('~wantCannonColl'):
            if localAvatar.ship:
                args = word.split()
                if len(args) > 1:
                    type = int(args[1])
                    base.cr.cannonballCollisionDebug = type
                elif base.cr.cannonballCollisionDebug == 0:
                    base.cr.cannonballCollisionDebug = 1
                else:
                    base.cr.cannonballCollisionDebug = 0
                if base.cr.cannonballCollisionDebug == 0:
                    self.setMagicWordResponse('cannonball collisions set to ALL OFF')
                elif base.cr.cannonballCollisionDebug == 1:
                    self.setMagicWordResponse('cannonball collisions set to ALL ON')
                elif base.cr.cannonballCollisionDebug == 2:
                    self.setMagicWordResponse('cannonball collisions set to Broadside ONLY ON')
                elif base.cr.cannonballCollisionDebug == 3:
                    self.setMagicWordResponse('cannonball collisions set to Deck ONLY ON')

            else:
                self.setMagicWordResponse('get on a ship!')
        elif __dev__ and wordIs('~wantEventCollider'):
            self.configWantEventCollider()
        elif __dev__ and wordIs('~wantFloorEventRay'):
            self.configWantFloorEventRay()
        elif __dev__ and wordIs('~optimized1'):
            if not (localAvatar.ship):
                self.setMagicWordResponse('get on a ship FIRST')

            self.configWantFloorEventRay()
            self.configWantEventCollider()
            self.configWantWaterRippleRay()
            self.configToggleBool('want-compass-task')
            configIs = 'ships-rock'
            args = word.split()
            self.configShipsRock(configIs, args)
            self.configEffects(args)
        elif __dev__ and wordIs('~optimized2'):
            if not (localAvatar.ship):
                self.setMagicWordResponse('get on a ship FIRST')

            self.configWantFloorEventRay()
            self.configWantEventCollider()
            self.configWantWaterRippleRay()
        elif wordIs('~setCannonFireVis'):
            args = word.split()
            type = 'all'
            if len(args) > 2:
                if args[2] == 'broadside':
                    type = 'broadside'
                elif args[2] == 'deck':
                    type = 'deck'


            if len(args) > 1:
                dist = int(args[1])
            elif type == 'broadside':
                dist = config.GetInt('cannon-fire-broadside-dist', 3500)
            else:
                dist = config.GetInt('cannon-fire-dist', 3500)
            if type == 'all' or type == 'deck':
                DistributedSimpleShip.DistributedSimpleShip.CannonFireDist = dist
                self.setMagicWordResponse('setting deck cannon visibility distance to %s' % dist)

            if type == 'all' or type == 'broadside':
                DistributedSimpleShip.DistributedSimpleShip.CannonFireBroadsideDist = dist
                self.setMagicWordResponse('setting broadside cannon visibility distance to %s' % dist)

        elif wordIs('~setWakeVis'):
            args = word.split()
            dist = config.GetInt('ship-wake-dist', 3800)
            if len(args) > 1:
                dist = int(args[1])

            DistributedSimpleShip.DistributedSimpleShip.ShipWakeDist = dist
            self.setMagicWordResponse('setting wake visibility distance to %s' % dist)
        elif wordIs('~setRockVis'):
            args = word.split()
            dist = config.GetInt('ship-rock-dist', 1000)
            if len(args) > 1:
                dist = int(args[1])

            DistributedSimpleShip.DistributedSimpleShip.ShipRockDist = dist
            self.setMagicWordResponse('setting rocking visibility distance to %s' % dist)
        elif __dev__ and wordIs('~wantReducedShipColl'):
            shipPilot = localAvatar.ship.controlManager.controls.get('ship')
            shipCollNode = shipPilot.cNodePath.node()
            if shipCollNode.getNumSolids() > 1:
                shipCollNode.removeSolid(2)
                shipCollNode.removeSolid(1)
                self.setMagicWordResponse('removing mid and stern spheres')
            else:
                shipCollNode.addSolid(shipPilot.cMidSphere)
                shipCollNode.addSolid(shipPilot.cSternSphere)
                self.setMagicWordResponse('adding mid and stern spheres')
        elif __dev__ and wordIs('~wantCollideMasks'):
            args = word.split()
            force = None
            if len(args) > 1:
                force = int(args[1])

            clientShips = [x for x in base.cr.doId2do.values() if isinstance(x, DistributedSimpleShip.DistributedSimpleShip)]
            cleared = False
            for currShip in clientShips:
                shipCollWall = currShip.hull[0].collisions.find('**/collision_hull')
                if not shipCollWall.isEmpty():
                    if shipCollWall.getCollideMask() & PiratesGlobals.ShipCollideBitmask == BitMask32.allOff():
                        shipCollWall.setCollideMask(shipCollWall.getCollideMask() | PiratesGlobals.ShipCollideBitmask)
                    else:
                        shipCollWall.setCollideMask(shipCollWall.getCollideMask() ^ PiratesGlobals.ShipCollideBitmask)
                        cleared = True


            if cleared:
                self.setMagicWordResponse('cleared ship collide bitmasks')
            else:
                self.setMagicWordResponse('set ship collide bitmasks')
        elif __dev__ and wordIs('~saveCamera'):
            camera = base.cr.doFind('DistributedCamera')
            cameraOV = camera.getOV()
            args = word.split()[1:]
            if args:
                id = cameraOV.saveFixture(int(args[0]))
            else:
                id = cameraOV.saveFixture()
            self.setMagicWordResponse('camera saved: %d' % id)
        elif __dev__ and wordIs('~removeCamera'):
            camera = base.cr.doFind('DistributedCamera')
            cameraOV = camera.getOV()
            args = word.split()[1:]
            if args:
                cameraOV.removeFixture(int(args[0]))
            else:
                self.setMagicWordResponse('need camera id to remove')
        elif __dev__ and wordIs('~standbyCamera'):
            camera = base.cr.doFind('DistributedCamera')
            cameraOV = camera.getOV()
            args = word.split()[1:]
            if args:
                cameraOV.standbyFixture(int(args[0]))
            else:
                self.setMagicWordResponse('need camera id to standby')
        elif __dev__ and wordIs('~blinkCamera'):
            camera = base.cr.doFind('DistributedCamera')
            cameraOV = camera.getOV()
            args = word.split()[1:]
            if args:
                cameraOV.blinkFixture(int(args[0]))
            else:
                self.setMagicWordResponse('need camera id to blink')
        elif __dev__ and wordIs('~testCamera'):
            camera = base.cr.doFind('DistributedCamera')
            cameraOV = camera.getOV()
            args = word.split()[1:]
            if args:
                cameraOV.testFixture(int(args[0]))
            else:
                self.setMagicWordResponse('need camera id to test')
        elif __dev__ and wordIs('~storeCameras'):
            camera = base.cr.doFind('DistributedCamera')
            cameraOV = camera.getOV()
            args = word.split()[1:]
            if args:
                cameraOV.storeToFile(args[0])
            else:
                self.setMagicWordResponse('need name to store')
        elif __dev__ and wordIs('~loadCameras'):
            camera = base.cr.doFind('DistributedCamera')
            cameraOV = camera.getOV()
            args = word.split()[1:]
            if args:
                cameraOV.loadFromFile(args[0])
            else:
                self.setMagicWordResponse('need name to load')
        elif __dev__ and wordIs('~startRecording'):
            camera = base.cr.doFind('DistributedCamera')
            cameraOV = camera.getOV()
            cameraOV.startRecording()
        elif __dev__ and wordIs('~stopRecording'):
            camera = base.cr.doFind('DistributedCamera')
            cameraOV = camera.getOV()
            cameraOV.stopRecording()
        elif __dev__ and base.config.GetBool('want-fishing-game', 0) and wordIs('~fishcam'):
            self.toggleFishCam()
            self.setMagicWordResponse('toggling fish cam')
            cameraOV.stopRecording()
        elif wordIs('~fishR'):
            self.doRequestFish(word, localAvatar, zoneId, localAvatar.doId)
        elif wordIs('~leg'):
            args = word.split()[1:]
            if args:
                base.fishingGame.wantLeg = arg[0]
            else:
                base.fishingGame.wantLeg = 1
        elif wordIs('~legWin'):
            if hasattr(base, 'fishingGame'):
                if base.fishingGame.fsm.getCurrentOrNextState() == 'LegendaryFish':
                    base.fishingGame.lfgFsm.request('Win')
                else:
                    self.setMagicWordResponse('Not battling legendary fish! (use ~leg)')
            else:
                self.setMagicWordResponse('Fishing Game not started.')
        elif wordIs('~cdunlockall'):
            messenger.send('cdUnlockAll')
        elif wordIs('~camSpin'):
            args = word.split()
            dist = 40
            if len(args) > 1:
                dist = float(args[1])


            def spin(task = None):
                localAvatar.cameraFSM.getCurrentCamera().setH(localAvatar.cameraFSM.getCurrentCamera().getH() + 1)
                return Task.cont

            if taskMgr.hasTaskNamed('camSpin'):
                localAvatar.cameraFSM.getCurrentCamera().setH(0)
                localAvatar.cameraFSM.getCurrentCamera()._setCamDistance(14)
                localAvatar.cameraFSM.getCurrentCamera().forceMaxDistance = True
                localAvatar.cameraFSM.getCurrentCamera()._startCollisionCheck()
                taskMgr.remove('camSpin')
            else:
                localAvatar.cameraFSM.getCurrentCamera()._stopCollisionCheck()
                localAvatar.cameraFSM.getCurrentCamera().forceMaxDistance = False
                localAvatar.cameraFSM.getCurrentCamera()._setCamDistance(dist)
                taskMgr.add(spin, 'camSpin')
        elif wordIs('~hostilizeNear'):
            interactivesNear = base.cr.interactionMgr.sortInteractives()
            for currInteractive in interactivesNear:
                if isinstance(currInteractive, DistributedNPCTownfolk.DistributedNPCTownfolk):
                    self.b_setMagicWord('~hostilize ' + str(currInteractive.doId))





    def configEffects(self, args):
        effectCats = args[1:]

        def toggleEffects(on = None):
            if effectCats:
                for currEffectCat in effectCats:
                    if currEffectCat == 'clearCustom':
                        base.cr.effectToggles = { }
                        continue

                    if currEffectCat == 'listEffectCats':
                        response = 'known effect types are: \n%s' % base.cr.effectTypes.keys()
                        self.setMagicWordResponse(response)
                        continue

                    effectTypes = base.cr.effectTypes.get(currEffectCat, [
                        currEffectCat])
                    for currEffectType in effectTypes:
                        newStatus = not base.cr.effectToggles.get(currEffectType, base.config.GetBool('want-special-effects', 1))
                        base.cr.effectToggles[currEffectType] = newStatus
                        response = 'effect %s set to %s' % (currEffectType, choice(newStatus, 'ON', 'OFF'))
                        self.setMagicWordResponse(response)



            base.cr.wantSpecialEffects = base.config.GetBool('want-special-effects', 1)
            clientShips = [x for x in base.cr.doId2do.values() if isinstance(x, DistributedSimpleShip.DistributedSimpleShip)]
            if base.cr.queryShowEffect('BlackSmoke') or base.cr.queryShowEffect('Fire'):
                for ship in clientShips:
                    if base.cr.queryShowEffect('BlackSmoke'):
                        ship.startSmoke()

                    if base.cr.queryShowEffect('Fire'):
                        ship.startFire()
                        continue

            elif not base.cr.queryShowEffect('BlackSmoke') or not base.cr.queryShowEffect('Fire'):
                for ship in clientShips:
                    if not base.cr.queryShowEffect('BlackSmoke'):
                        ship.stopSmoke()

                    if not base.cr.queryShowEffect('Fire'):
                        ship.stopFire()
                        continue



        if effectCats:
            toggleEffects()
        else:
            self.configToggleBool('want-special-effects', offCode = (lambda p1 = False: toggleEffects(p1)), onCode = (lambda p1 = True: toggleEffects(p1)))


    def configWantEventCollider(self):
        currControls = localAvatar.controlManager.currentControls
        if currControls == None:
            return None

        if not base.shadowTrav.hasCollider(currControls.cEventSphereNodePath):
            pass
        colliderExists = currControls.cTrav.hasCollider(currControls.cEventSphereNodePath)
        if colliderExists:
            currControls.cTrav.removeCollider(currControls.cEventSphereNodePath)
            base.shadowTrav.removeCollider(currControls.cEventSphereNodePath)
            currControls.pusher.addInPattern('enter%in')
            currControls.pusher.addOutPattern('exit%in')
            self.setMagicWordResponse('event sphere OFF')
        else:
            currControls.pusher.clearInPatterns()
            currControls.pusher.clearOutPatterns()
            avatarRadius = 1.3999999999999999
            base.shadowTrav.addCollider(currControls.cEventSphereNodePath, currControls.event)
            self.setMagicWordResponse('event sphere ON')


    def configWantFloorEventRay(self):
        if localAvatar.cTrav.hasCollider(localAvatar.cFloorNodePath):
            localAvatar.cTrav.removeCollider(localAvatar.cFloorNodePath)
            self.setMagicWordResponse('floor event ray OFF')
        else:
            localAvatar.cTrav.addCollider(localAvatar.cFloorNodePath, localAvatar.floorEventHandler)
            self.setMagicWordResponse('floor event ray ON')


    def configWantWaterRippleRay(self):
        if localAvatar.cTrav.hasCollider(localAvatar.cWaterNodePath):
            localAvatar.cTrav.removeCollider(localAvatar.cWaterNodePath)
            self.setMagicWordResponse('water ripple ray OFF')
        else:
            localAvatar.cTrav.addCollider(localAvatar.cWaterNodePath, localAvatar.waterEventHandler)
            self.setMagicWordResponse('water ripple ray ON')


    def configWantShadowPlacer(self):
        if localAvatar.shadowPlacer.cTrav.hasCollider(localAvatar.shadowPlacer.cRayNodePath):
            localAvatar.shadowPlacer.cTrav.removeCollider(localAvatar.shadowPlacer.cRayNodePath)
            self.setMagicWordResponse('shadow placer ray OFF')
        else:
            localAvatar.shadowPlacer.cTrav.addCollider(localAvatar.shadowPlacer.cRayNodePath, localAvatar.shadowPlacer.lifter)
            self.setMagicWordResponse('shadow placer ray ON')


    def configShipsRock(self, configIs, args):
        onlyPlayerRocks = False
        if len(args) > 1 and args[1] == 'playerOnly':
            onlyPlayerRocks = True

        if config.GetInt(configIs, 1) == 1 or config.GetInt(configIs, 1) == 2:
            ConfigVariableInt(configIs).setValue(0)
            self.setMagicWordResponse('%s OFF (all ships)' % configIs)
        elif onlyPlayerRocks:
            ConfigVariableInt(configIs).setValue(2)
            self.setMagicWordResponse('%s ON (local player ship only)' % configIs)
        else:
            ConfigVariableInt(configIs).setValue(1)
            self.setMagicWordResponse('%s ON (all ships)' % configIs)


    def configToggleBool(self, configName, defaultVal = 1, offCode = None, onCode = None):
        currVal = not config.GetBool(configName, defaultVal)
        loadPrcFileData('', '%s %s' % (configName, currVal))
        self.setMagicWordResponse('%s %s' % (configName, choice(currVal, 'ON', 'OFF')))
        if currVal and onCode:
            onCode()
        elif not currVal and offCode:
            offCode()



    def cameraFollowTgt(self, target, parentId):
        localAvatar.cTrav.removeCollider(localAvatar.cFloorNodePath)
        localAvatar.controlManager.use('observer', localAvatar)
        localAvatar.controlManager.currentControls.disableAvatarControls()
        localAvatar.guiMgr.setIgnoreAllKeys(True)
        localAvatar.guiMgr.combatTray.skillMapping.clear()
        localAvatar.reparentTo(target)
        localAvatar.setScale(1)
        parentObj = base.cr.doId2do[parentId]
        localAvatar.setPos(0, 0, 0)
        localAvatar.setHpr(render, target.getHpr(render))
        localAvatar.stash()
        if self.pendingCameraReparent:
            base.cr.relatedObjectMgr.abortRequest(self.pendingCameraReparent)
            self.pendingCameraReparent = None



    def cameraUnfollowTgt(self, target):
        localAvatar.cTrav.addCollider(localAvatar.cFloorNodePath, localAvatar.floorEventHandler)
        localAvatar.controlManager.currentControls.enableAvatarControls()
        localAvatar.controlManager.use('walk', localAvatar)
        localAvatar.guiMgr.setIgnoreAllKeys(False)
        localAvatar.guiMgr.combatTray.initCombatTray()
        localAvatar.unstash()
        if hasattr(localAvatar, 'followTgt'):
            del localAvatar.followTgt



    def cameraReparent(self, targetId, targetParentId, zoneId):
        targetObj = base.cr.doId2do.get(targetParentId)
        if targetObj and not isinstance(targetObj, NodePath):
            return None

        currParentObj = localAvatar.getParentObj()
        if self.originalLocation == None:
            self.originalLocation = [
                localAvatar.getLocation(),
                localAvatar.getPos(currParentObj)]

        prevPos = None
        if targetId == 0 and targetParentId == 0 and zoneId == 0 and self.originalLocation:
            targetParentId = self.originalLocation[0][0]
            zoneId = self.originalLocation[0][1]
            prevPos = self.originalLocation[1]
            self.originalLocation = None

        targetObj = base.cr.doId2do.get(targetParentId)
        if targetObj == None or not isinstance(targetObj, NodePath):
            self.notify.debug('Parent of target object to reparent avatar/camera to does not yet exist, skipping reparent request')
            return None

        if prevPos:
            newPos = prevPos
        else:
            newPos = Point3(*targetObj.getZoneCellOriginCenter(zoneId))
        localAvatar.reparentTo(targetObj)
        localAvatar.setPos(newPos)
        localAvatar.isGhosting = True
        if base.cr.doId2do.has_key(targetId):
            self.cameraFollowTgt(base.cr.doId2do[targetId], targetParentId)
        elif targetId:
            self.pendingCameraReparent = base.cr.relatedObjectMgr.requestObjects([
                targetId], eachCallback = (lambda param = None, param2 = targetParentId: self.cameraFollowTgt(param, param2)))
        elif self.pendingCameraReparent:
            base.cr.relatedObjectMgr.abortRequest(self.pendingCameraReparent)
            self.pendingCameraReparent = None

        self.cameraUnfollowTgt(targetObj)
        localAvatar.isGhosting = False


    def shipCreated(self, shipId):
        return None
        print 'shipCreated(%s)' % shipId
        ship = base.cr.doId2do.get(shipId)
        if ship:
            print 'ship created: %s' % ship
            ship.localAvatarInstantBoard()
            ship.enableOnDeckInteractions()



    def toggleFishCam(self):
        self.fishCamEnabled = not (self.fishCamEnabled)
        if self.fishCamEnabled:
            base.oobe()
            base.oobeCamera.setPos(-13.0, 4.0, -6.0)
            base.oobeCamera.setHpr(90.0, 0.0, 0.0)
            CardMaker = CardMaker
            import pandac.PandaModules
            PosInterval = PosInterval
            ProjectileInterval = ProjectileInterval
            Sequence = Sequence
            Wait = Wait
            import direct.interval.IntervalGlobal
            cm = CardMaker('fishBackdrop')
            self.fishBackdrop = render.attachNewNode(cm.generate())
            tex = loader.loadTexture('maps/underseaBackdrop.jpg')
            self.fishBackdrop.setTexture(tex)
            self.fishBackdrop.reparentTo(localAvatar)
            self.fishBackdrop.setHpr(90, 0, 0)
            self.fishBackdrop.setPos(0, -100, -108.7)
            self.fishBackdrop.setScale(400, 1, 100)
            self.fishBackdrop.setBin('ground', 20)
            self.fishBackdrop.setDepthWrite(0)
            self.fishCamProjectileInterval = Sequence(Wait(4), ProjectileInterval(base.oobeCamera, startPos = Point3(-13.0, 4.0, -6.0), endPos = Point3(-13.0, 164.0, -36.0), duration = 3), ProjectileInterval(base.oobeCamera, startPos = Point3(-13.0, 164.0, -36.0), endPos = Point3(-13.0, 4.0, -24.0), gravityMult = -0.5, duration = 5), base.oobeCamera.posInterval(5, Point3(-13.0, 4.0, -6.0)))
            self.fishCamProjectileInterval.start()
        else:
            self.fishCamProjectileInterval.finish()
            del self.fishCamProjectileInterval
            self.fishBackdrop.reparentTo(hidden)
            del self.fishBackdrop
            base.oobe()


    def doRequestFish(self, word, av, zoneId, senderId):
        args = word.split()
        doid = args[1]
        spot = self.cr.doId2do[int(doid)]
        spot.requestInteraction(localAvatar.doId)
