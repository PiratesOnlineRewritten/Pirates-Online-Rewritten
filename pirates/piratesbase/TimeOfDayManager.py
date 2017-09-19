from panda3d.core import *
from direct.fsm import FSM
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *
from pirates.ai import HolidayGlobals
from pirates.piratesbase import AvatarShadowCaster
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TODGlobals
from pirates.piratesbase import TODDefs
from pirates.piratesbase import SkyGroup
import time
from pirates.piratesbase import TimeOfDayManagerBase
import random


class TimeOfDayManager(FSM.FSM, TimeOfDayManagerBase.TimeOfDayManagerBase):
    notify = directNotify.newCategory('TimeOfDayManager')

    def __init__(self):
        FSM.FSM.__init__(self, 'TimeOfDayManager')
        TimeOfDayManagerBase.TimeOfDayManagerBase.__init__(self)
        self.lightSwitch = [
            0,
            0,
            0]
        self.cycleType = TODGlobals.TOD_REGULAR_CYCLE
        self.cycleDuration = 0
        self.currentState = -1
        self.prevState = -1
        self.lastState = 0
        self.envEffect = None
        self.lastEffective = (0, 0)
        self.inTransition = 0
        self.needCheckSub = 0
        self.ambientSFXList = []
        self.lastServerTimeArrived = 0
        self.cycleSpeed = 1
        self.timeOffset = 0
        tempTime = globalClockDelta.getFrameNetworkTime(bits=32)
        self.startingServerTime = globalClockDelta.networkToLocalTime(tempTime)
        self.startTodTime = globalClockDelta.networkToLocalTime(
            globalClockDelta.getFrameNetworkTime(bits=32))
        self.lastWaterColor = Vec4(0, 0, 0, 0)
        self.lastWaterColorFactor = Vec4(0, 0, 0, 0)
        self.frontLightColor = Vec4(0, 0, 0, 0)
        self.backLightColor = Vec4(0, 0, 0, 0)
        self.clearColor = Vec4(0, 0, 0, 0)
        self.frontLightFlutter = None
        self.backLightFlutter = None
        self.flutterFront = 0
        self.flutterBack = 0
        self.waterColorFactor = None
        self.environment = TODGlobals.ENV_DEFAULT
        self.envSubstitutionDict = {}
        self.waitTaskName = 'waitForNextTODState-' + str(hash(self))
        self.nextDoLater = None
        self.startingTime = 0
        self.startingState = -1
        self.transitionIval = None
        self.sunMoveIval = None
        self.moonPhaseIval = None
        self.targetMoonPhase = None
        self.moonJolly = 0
        self.moonJollyIval = None
        self.softTOD = 1
        if base.config.GetBool('want-soft-tod-changes', 0):
            self.softTOD = 1

        if base.config.GetBool('advanced-weather', 1):
            pass

        self.skyGroup = SkyGroup.SkyGroup()
        self.skyGroup.reparentTo(camera)
        self.fixedSky = False
        self.skyEnabled = True
        self.seapatch = None
        self.sunLight = self.skyGroup.dirLightSun
        self.dlight = self.skyGroup.dirLightSun
        self.grassLight = self.skyGroup.grassLight
        self.alight = self.skyGroup.ambLight
        self.shadowLight = self.skyGroup.dirLightShadowSun
        self.fog = Fog('TimeOfDayFog')
        self.setFogExpDensity(TODGlobals.FOG_DEFAULT_EXP)
        self.fogExpDensity = 0.0
        self.linearFog = Fog('LinearTimeOfDayFog')
        self.currFogOnset = 0.0
        self.currFogPeak = 100.0
        self.lerpFogIval = None
        self.fogMask = 0
        self.fogType = None
        self.fogColor = Vec4(0.0, 0.0, 0.0, 0.0)
        self.setFogType(TODGlobals.FOG_OFF)
        self.showSky = 0
        self.avatarShadowCaster = None
        if base.config.GetBool('want-avatar-shadows', 1):
            self.enableAvatarShadows()

        self.isPaused = 0
        if base.config.GetBool('want-shaders',
                               1) and base.win and base.win.getGsg():
            pass
        self.use_shader = base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20
        self.accept('HolidayStarted', self.handleHolidayStarted)
        self.accept('HolidayEnded', self.handleHolidayEnded)
        self.forcedStateEnabled = False
        self.currentStateDuration = None
        self.debugTOD = False
        self.alteratedSettingsList = []

    def toggleDebugMode(self):
        if self.debugTOD:
            self.debugTOD = False
            base.talkAssistant.receiveGameMessage('Turning off TOD info')
        else:
            self.debugTOD = True
            base.talkAssistant.receiveGameMessage('Turning on TOD info')
            base.talkAssistant.receiveGameMessage('Time is %s %s %s' % (str(self.getCurrentIngameTime())[
                                                  :5], TODGlobals.StateDict[self.currentState], TODGlobals.ENV_DEBUG_NAMES[self.environment]))

    def enableAvatarShadows(self):
        if not self.avatarShadowCaster:
            self.avatarShadowCaster = AvatarShadowCaster.AvatarShadowCaster(
                self.sunLight)

        self.avatarShadowCaster.enable()
        self.skyGroup.shadowCaster = self.avatarShadowCaster
        self.skyGroup.applySunAngle()

    def disableAvatarShadows(self):
        if self.avatarShadowCaster:
            self.avatarShadowCaster.disable()

        self.skyGroup.shadowCaster = None

    def setRelativeRotation(self, h=0):
        if hasattr(base.localAvatar, 'gridParent'):
            if base.localAvatar.gridParent and base.localAvatar.gridParent.grid:
                self.skyGroup.setRelativeCompassH(
                    base.localAvatar.gridParent.grid.getH())
            else:
                self.skyGroup.setRelativeCompassH(0.0)

    def disable(self):
        if self.envEffect is not None:
            self.stopEnvEffect(self.envEffect)

        self.ignore('gotTimeSync')
        self.ignore('HolidayStarted')
        self.ignore('HolidayEnded')
        taskMgr.remove('pauseTimeOfDayManagerTask')
        self.request('Off')
        if self.transitionIval:
            self.transitionIval.pause()
            self.transitionIval = None

        if self.sunMoveIval:
            self.sunMoveIval.pause()

        del self.sunMoveIval
        if self.moonPhaseIval:
            self.moonPhaseIval.pause()

        del self.moonPhaseIval
        if self.moonJollyIval:
            self.moonJollyIval.pause()

        del self.moonJollyIval

    def delete(self):
        render.clearLight(self.alight)
        render.clearLight(self.sunLight)
        render.clearLight(self.shadowLight)
        self.alight = None
        self.dlight = None
        self.shadowLight = None
        self.grassLight = None
        self.sunLight = None
        if self.lerpFogIval:
            self.lerpFogIval.pause()
            self.lerpFogIval = None

        if self.avatarShadowCaster:
            self.avatarShadowCaster.disable()
            self.avatarShadowCaster = None

        if self.transitionIval:
            self.transitionIval.pause()
            self.transitionIval = None

        self.fog = None
        self.ignoreAll()
        self.skyGroup.stopCloudIval()
        self.skyGroup.removeNode()
        del self.skyGroup

    def enterInitState(self):
        if self.forcedStateEnabled:
            return None

        if self.isPaused:
            stateName = TODGlobals.getStateName(self.startingState)
            self.request(stateName)
            taskMgr.doMethodLater(10.0, self.pause, 'pauseTimeOfDayManagerTask')
        else:
            self.syncTimeOfDay(0)

    def syncTimeOfDay(self, soft=1):
        if self.environment == TODGlobals.ENV_SAILING:
            pass

        if self.forcedStateEnabled:
            return None

        self.notify.debug('Syncing time of day...')
        (stateId, stateTime) = self._computeCurrentState()
        stateName = TODGlobals.getStateName(stateId)
        if hasattr(base, 'pe'):
            self.request('EnvironmentTOD')
        else:
            self.request('EnvironmentTOD')
        if self.debugTOD:
            base.talkAssistant.receiveGameMessage('syncTimeOfDay')

    def _computeCurrentState(self):
        if self.cycleDuration == 0:
            return (self.startingState, 0.0)

        elapsedTime = globalClockDelta.localElapsedTime(
            self.startingTime, bits=32)
        remTime = elapsedTime % self.cycleDuration
        stateId = self.startingState
        while None:
            stateDuration = self.cycleDuration * \
                TODGlobals.getStateDuration(self.cycleType, stateId)
            if remTime < stateDuration:
                return (stateId, remTime)
                continue
            remTime -= stateDuration
            stateId = TODGlobals.getNextStateId(self.cycleType, stateId)

    def _waitForNextStateRequest(self, stateId, elapsedTime):
        taskMgr.remove(self.waitTaskName)
        if self.cycleDuration == 0:
            self.notify.debug('stopping in state: %s' % stateId)
            return 0

        nextStateId = TODGlobals.getNextStateId(self.cycleType, stateId)
        nextStateName = TODGlobals.getStateName(nextStateId)
        stateDuration = self.cycleDuration * \
            TODGlobals.getStateDuration(self.cycleType, stateId)
        delayTime = stateDuration - elapsedTime
        self.nextDoLater = taskMgr.doMethodLater(
            delayTime, self._doLaterRequest, self.waitTaskName, extraArgs=[])
        return stateDuration

    def _getStateDuration(self, stateId):
        stateDuration = self.cycleDuration * \
            TODGlobals.getStateDuration(self.cycleType, stateId)
        return stateDuration

    def _doLaterRequest(self):
        (stateId, elapsedTime) = self._computeCurrentState()
        nextStateName = TODGlobals.getStateName(stateId)
        self.request('EnvironmentTOD')
        return Task.done

    def getStateName(self, stateId):
        return TODGlobals.getStateName(stateId)

    def pause(self, task=None):
        if self.transitionIval:
            self.transitionIval.pause()

        taskMgr.remove(self.waitTaskName)

    def setFrontLightColor(self, newColor):
        frontLight = self.skyGroup.dirLightSun
        ambientColor = self.alight.node().getColor()
        self.frontLightColor = newColor
        if not self.flutterFront:
            lightValueForColor = TODGlobals.computeLightColor(
                self.frontLightColor, ambientColor, self.lightSwitch)
            frontLight.node().setColor(lightValueForColor)

    def getFrontLightColor(self):
        return self.frontLightColor

    def setBackLightColor(self, newColor):
        backLight = self.skyGroup.dirLightShadowSun
        ambientColor = self.alight.node().getColor()
        self.backLightColor = newColor
        if not self.flutterBack:
            lightValueForColor = TODGlobals.computeLightColor(
                self.backLightColor, ambientColor, self.lightSwitch)
            backLight.node().setColor(lightValueForColor)

    def getBackLightColor(self):
        return self.backLightColor

    def setFillLightColor(self, newColor):
        self.alight.node().setColor(newColor)

    def getFillLightColor(self):
        return self.alight.node().getColor()

    def startFlutter(self):
        self.flutterFront = 1
        self.flutterBack = 1
        self.frontLightFlutter = self.frontLightColor
        self.backLightFlutter = self.backLightColor
        self.lastFrontRandom = 1.0
        self.lastBackRandom = 1.0
        taskMgr.add(
            self._TimeOfDayManager__flutterLights,
            'todManager-flutterLights')

    def endFlutter(self):
        taskMgr.remove('todManager-flutterLights')
        self.flutterFront = 0
        self.flutterBack = 0

    def _TimeOfDayManager__flutterLights(self, task):
        frontLight = self.skyGroup.dirLightSun
        backLight = self.skyGroup.dirLightShadowSun
        ambientColor = self.alight.node().getColor()
        randFront = random.random()
        randBack = random.random()
        blendFront = (randFront + self.lastFrontRandom) * 0.5
        blendBack = (randBack + self.lastBackRandom) * 0.5
        self.lastFrontRandom = randFront
        self.lastBackRandom = randBack
        factorFront = self.frontLightColor * (0.75 + blendFront * 0.5)
        factorBack = self.backLightColor * (0.75 + blendBack * 0.5)
        self.frontLightFlutter = self.frontLightFlutter * \
            0.80000000000000004 + factorFront * 0.20000000000000001
        self.backLightFlutter = self.backLightFlutter * \
            0.80000000000000004 + factorBack * 0.20000000000000001
        lightValueForColor = TODGlobals.computeLightColor(
            self.frontLightFlutter, ambientColor, self.lightSwitch)
        frontLight.node().setColor(lightValueForColor)
        lightValueForColor = TODGlobals.computeLightColor(
            self.backLightFlutter, ambientColor, self.lightSwitch)
        backLight.node().setColor(lightValueForColor)
        return task.cont

    def storeAlteredSetting(self, env, tod, settingName):
        settingTuple = (env, tod, settingName)
        if settingTuple not in self.alteratedSettingsList:
            self.alteratedSettingsList.append(settingTuple)

        messenger.send('TOD_Setting_Change', [])

    def listAlteredTODs(self, env):
        alteredList = []
        for entry in self.alteratedSettingsList:
            if entry[0] == env:
                if entry[1] not in alteredList:
                    alteredList.append(entry[1])

            entry[1] not in alteredList

        return alteredList

    def revertTODChange(self, env, tod):
        entryToRemoveList = []
        for entry in self.alteratedSettingsList:
            if entry[0] == env and entry[1] == tod:
                settingName = entry[2]
                del TODGlobals.ENV_SETTINGS_DICT[env][tod][settingName]
                entryToRemoveList.append(entry)
                envDict = TODGlobals.BACKUP_ENV_SETTINGS_DICT.get(env)
                if envDict:
                    timeDict = envDict.get(tod)
                    if timeDict:
                        settingValue = timeDict.get(settingName)
                        if settingValue:
                            TODGlobals.ENV_SETTINGS_DICT[env][tod][settingName] = settingValue

                if TODGlobals.ENV_SETTINGS_DICT[env][tod] == {}:
                    del TODGlobals.ENV_SETTINGS_DICT[env][tod]

            TODGlobals.ENV_SETTINGS_DICT[env][tod] == {}

        for entry in entryToRemoveList:
            self.alteratedSettingsList.remove(entry)

    def insertTODSettings(self, environment, todState, ambientColor, frontColor,
                          backColor, fogColor, fogExp, fogRange, lightSwitch, sunDir):
        envGroup = TODGlobals.ENV_SETTINGS_DICT.get(environment)
        if envGroup:
            settingGroup = envGroup.get(self.currentState)
            if not settingGroup:
                envGroup[self.currentState] = {}

            TODGlobals.ENV_SETTINGS_DICT[environment][todState]['AmbientColor'] = ambientColor
            TODGlobals.ENV_SETTINGS_DICT[environment][todState]['FrontColor'] = frontColor
            TODGlobals.ENV_SETTINGS_DICT[environment][todState]['BackColor'] = backColor
            TODGlobals.ENV_SETTINGS_DICT[environment][todState]['FogColor'] = fogColor
            TODGlobals.ENV_SETTINGS_DICT[environment][todState]['FogExp'] = fogExp
            TODGlobals.ENV_SETTINGS_DICT[environment][todState]['FogLinearRange'] = (
                fogRange[0], fogRange[1])
            TODGlobals.ENV_SETTINGS_DICT[environment][todState]['LightSwitch'] = (
                lightSwitch[0], lightSwitch[1], lightSwitch[2])
            TODGlobals.ENV_SETTINGS_DICT[environment][todState]['Direction'] = Vec3(
                sunDir[0], sunDir[1], sunDir[2])
            self.storeAlteredSetting(environment, todState, 'AmbientColor')
            self.storeAlteredSetting(environment, todState, 'FrontColor')
            self.storeAlteredSetting(environment, todState, 'BackColor')
            self.storeAlteredSetting(environment, todState, 'FogColor')
            self.storeAlteredSetting(environment, todState, 'FogExp')
            self.storeAlteredSetting(environment, todState, 'FogLinearRange')
            self.storeAlteredSetting(environment, todState, 'LightSwitch')
            self.storeAlteredSetting(environment, todState, 'Direction')

        print 'Inserting env%s tod %s\nambient %s\nfront %s\nback %s\nfogColor %s\nfogExp %s\nfogRange %s\n' % (self.environment, self.currentState, ambientColor, frontColor, backColor, fogColor, fogExp, fogRange)

    def insertEnvDict(self, envIndex, envDict):
        for todName in envDict:
            todDict = envDict[todName]
            todIndex = TODGlobals.NAME_TO_ID_DICT[todName]
            if todDict and todDict != {}:
                self.insertTODSettingDict(envIndex, todIndex, todDict)
                continue

    def insertTODSettingDict(self, env, tod, settingDict):
        for settingName in settingDict:
            self.insertTODSetting(
                env, tod, settingName, settingDict[settingName])

    def insertTODSetting(self, env, todId, settingName, settingValue):
        print 'insertTODSetting %s %s %s %s' % (env, todId, settingName, settingValue)
        tod = TODGlobals.StateDict.get(todId, None)
        if tod is None:
            return None

        envGroup = TODGlobals.ENV_SETTINGS_DICT.get(env)
        if not envGroup:
            TODGlobals.ENV_SETTINGS_DICT[env] = {}

        settingGroup = envGroup.get(tod)
        if not settingGroup:
            TODGlobals.ENV_SETTINGS_DICT[env][tod] = {}

        if tod == 'BASE' and env == TODGlobals.ENV_DEFAULT:
            pass

        if TODGlobals.ENV_SETTINGS_DICT[env][tod].get(settingName):
            del TODGlobals.ENV_SETTINGS_DICT[env][tod][settingName]

        parentSettingValue = TODGlobals.getTodEnvSetting(tod, env, settingName)
        if parentSettingValue == settingValue:
            return None
        elif settingName == 'Direction':
            sameCount = 0
            for compIndex in xrange(3):
                if parentSettingValue[compIndex] % 360.0 == settingValue[compIndex] % 360.0:
                    sameCount += 1
                    continue

            if sameCount >= 3:
                return None

        if settingName == 'FogLinearRange':
            TODGlobals.ENV_SETTINGS_DICT[env][tod][settingName] = (
                settingValue[0], settingValue[1])
        else:
            TODGlobals.ENV_SETTINGS_DICT[env][tod][settingName] = settingValue
        self.storeAlteredSetting(env, tod, settingName)

    def setLightSwitch(self, switchList):
        frontOn = switchList[0]
        ambientOn = switchList[1]
        backOn = switchList[2]
        oldFront = self.getFrontLightColor()
        oldBack = self.getBackLightColor()
        if frontOn != self.lightSwitch[0]:
            if frontOn:
                render.setLight(self.sunLight)
            else:
                render.clearLight(self.sunLight)

        if ambientOn != self.lightSwitch[1]:
            if ambientOn:
                render.setLight(self.alight)
            else:
                render.clearLight(self.alight)

        if backOn != self.lightSwitch[2]:
            if backOn:
                render.setLight(self.shadowLight)
            else:
                render.clearLight(self.shadowLight)

        self.lightSwitch = switchList
        self.setFrontLightColor(oldFront)
        self.setBackLightColor(oldBack)

    def _transitionTimeOfDay(self, fromState, toState, t, startEnv=None, destEnv=None):
        if self.forcedStateEnabled:
            return Parallel()

        if destEnv is None:
            destEnv = self.environment

        if startEnv is None:
            startEnv = destEnv

        environment = self.environment
        timeLightSwitch = TODGlobals.getTodEnvSetting(
            toState, environment, 'LightSwitch')
        fromAmbient = TODGlobals.getTodEnvSetting(
            fromState, startEnv, 'AmbientColor')
        fromFogColor = TODGlobals.getTodEnvSetting(
            fromState, startEnv, 'FogColor')
        fromFogExp = TODGlobals.getTodEnvSetting(fromState, startEnv, 'FogExp')
        fromFogOnset = TODGlobals.getTodEnvSetting(
            fromState, startEnv, 'FogLinearRange')[0]
        fromFogPeak = TODGlobals.getTodEnvSetting(
            fromState, startEnv, 'FogLinearRange')[1]
        fromStarColor = TODGlobals.getTodEnvSetting(
            fromState, startEnv, 'StarColor')
        fromFrontLight = TODGlobals.getTodEnvSetting(
            fromState, startEnv, 'FrontColor')
        fromBackLight = TODGlobals.getTodEnvSetting(
            fromState, startEnv, 'BackColor')
        ival = Parallel(
            LerpFunctionInterval(
                self.alight.node().setColor,
                duration=t,
                toData=TODGlobals.getTodEnvSetting(
                    toState,
                    destEnv,
                    'AmbientColor'),
                fromData=fromAmbient,
                name='TOD_aLightColor-%d'),
            LerpFunctionInterval(
                self.grassLight.node().setColor,
                duration=t,
                toData=TODGlobals.getTodEnvSetting(
                    toState,
                    destEnv,
                    'AmbientColor'),
                fromData=fromAmbient,
                name='TOD_grassLightColor-%d'),
            LerpFunctionInterval(
                self.setFogColor,
                duration=t,
                toData=TODGlobals.getTodEnvSetting(
                    toState,
                    destEnv,
                    'FogColor'),
                fromData=fromFogColor,
                name='TOD_fogColor-%d'),
            LerpFunctionInterval(
                self.setFogExpDensity,
                duration=t,
                toData=TODGlobals.getTodEnvSetting(
                    toState,
                    destEnv,
                    'FogExp'),
                fromData=fromFogExp,
                name='TOD_fogExp-%d'),
            LerpFunctionInterval(
                self.setLinearFogOnset,
                duration=t,
                toData=TODGlobals.getTodEnvSetting(
                    toState,
                    destEnv,
                    'FogLinearRange')[0],
                fromData=fromFogOnset,
                name='TOD_fogExp-%d'),
            LerpFunctionInterval(
                self.setLinearFogPeak,
                duration=t,
                toData=TODGlobals.getTodEnvSetting(
                    toState,
                    destEnv,
                    'FogLinearRange')[1],
                fromData=fromFogPeak,
                name='TOD_fogExp-%d'),
            LerpFunctionInterval(
                self.skyGroup.stars.setColorScale,
                duration=t,
                toData=TODGlobals.getTodEnvSetting(
                    toState,
                    destEnv,
                    'StarColor'),
                fromData=fromStarColor,
                name='TOD_fogExp-%d'),
            name='TOD_transitionTimeOfDay')
        if not self.fixedSky:
            fromSkyType = TODGlobals.getTodEnvSetting(
                fromState, startEnv, 'SkyType')
            fromSkyColor = TODGlobals.SKY_CLEARCOLORS[fromSkyType]
            toSkyType = TODGlobals.getTodEnvSetting(
                toState, destEnv, 'SkyType')
            toSkyColor = TODGlobals.SKY_CLEARCOLORS[toSkyType]
            ival.append(
                LerpFunctionInterval(
                    self.setSkyClearColor,
                    duration=t,
                    fromData=fromSkyColor,
                    toData=toSkyColor))
            if hasattr(base, 'pe'):
                ival.append(
                    LerpFunctionInterval(
                        base.setBackgroundColor,
                        duration=t,
                        fromData=fromSkyColor,
                        toData=toSkyColor))

            toSkySettings = TODGlobals.getTodEnvSetting(
                toState, destEnv, 'SkyType')
            fromSkySettings = TODGlobals.getTodEnvSetting(
                fromState, startEnv, 'SkyType')
            if t > 0.0:
                ival.append(
                    self.skyGroup.transitionSky(
                        fromSkySettings,
                        toSkySettings,
                        duration=t))

        if base.cr.activeWorld and hasattr(
                base.cr.activeWorld, 'getWater') and base.cr.activeWorld.getWater():
            if self.use_shader:
                self.seapatch = base.cr.activeWorld.getWater()
            else:
                self.seapatch = base.cr.activeWorld.getWater().patchNP

        if base.cr.newsManager and base.cr.newsManager.getHoliday(
                HolidayGlobals.SAINTPATRICKSDAY):
            self.setSaintPatricksSea()
        elif self.use_shader:
            fromSeaColor = TODGlobals.getTodEnvSetting(
                fromState, startEnv, 'SeaColorShader')
            toSeaColor = TODGlobals.getTodEnvSetting(
                toState, destEnv, 'SeaColorShader')
            ival.append(
                LerpFunctionInterval(
                    self.modifyWaterColor,
                    duration=t,
                    fromData=fromSeaColor,
                    toData=toSeaColor))
            fromSeaColorFactor = TODGlobals.getTodEnvSetting(
                fromState, startEnv, 'SeaFactor')
            toSeaColorFactor = TODGlobals.getTodEnvSetting(
                toState, destEnv, 'SeaFactor')
            ival.append(
                LerpFunctionInterval(
                    self.modifyWaterColorFactor,
                    duration=t,
                    fromData=fromSeaColorFactor,
                    toData=toSeaColorFactor))
        else:
            fromSeaColor = TODGlobals.getTodEnvSetting(
                fromState, startEnv, 'SeaColor')
            toSeaColor = TODGlobals.getTodEnvSetting(
                toState, destEnv, 'SeaColor')
            ival.append(
                LerpFunctionInterval(
                    self.modifyWaterColor,
                    duration=t,
                    fromData=fromSeaColor,
                    toData=toSeaColor))
        self.currLight = self.skyGroup.getLight(fromState)
        self.dLight = self.skyGroup.getLight(toState)
        fromDirectionalColor = TODGlobals.computeLightColor(
            TODGlobals.getTodEnvSetting(
                fromState, startEnv, 'FrontColor'), TODGlobals.getTodEnvSetting(
                fromState, startEnv, 'AmbientColor'), timeLightSwitch)
        toDirectionalColor = TODGlobals.computeLightColor(
            TODGlobals.getTodEnvSetting(
                toState, destEnv, 'FrontColor'), TODGlobals.getTodEnvSetting(
                toState, destEnv, 'AmbientColor'), timeLightSwitch)
        ival.append(
            LerpFunctionInterval(
                self.setFrontLightColor,
                duration=t,
                toData=TODGlobals.getTodEnvSetting(
                    toState,
                    destEnv,
                    'FrontColor'),
                fromData=fromFrontLight,
                name='TOD_dLightColor-%d'))
        self.currShadowLight = self.skyGroup.getShadowLight(fromState)
        self.shadowLight = self.skyGroup.getShadowLight(toState)
        fromShadowLight = TODGlobals.computeLightColor(
            TODGlobals.getTodEnvSetting(
                fromState, startEnv, 'BackColor'), TODGlobals.getTodEnvSetting(
                fromState, startEnv, 'AmbientColor'), timeLightSwitch)
        toShadowLight = TODGlobals.computeLightColor(
            TODGlobals.getTodEnvSetting(
                toState, destEnv, 'BackColor'), TODGlobals.getTodEnvSetting(
                toState, destEnv, 'AmbientColor'), timeLightSwitch)
        ival.append(
            LerpFunctionInterval(
                self.setBackLightColor,
                duration=t,
                toData=TODGlobals.getTodEnvSetting(
                    toState,
                    destEnv,
                    'BackColor'),
                fromData=fromBackLight,
                name='TOD_dLightColor-%d'))
        fromMoonOverlay = TODGlobals.getTodEnvSetting(
            fromState, startEnv, 'MoonOverlay')
        fromMoonSize = TODGlobals.getTodEnvSetting(
            fromState, startEnv, 'MoonSize')
        fromMoonState = self.skyGroup.moonState
        toMoonOverlay = TODGlobals.getTodEnvSetting(
            toState, destEnv, 'MoonOverlay')
        toMoonSize = TODGlobals.getTodEnvSetting(toState, destEnv, 'MoonSize')
        toMoonState = TODGlobals.getTodEnvSetting(
            toState, destEnv, 'MoonPhase')
        if self.moonJolly:
            fromMoonOverlay = 0.5
            toMoonOverlay = 0.5

        if self.moonJollyIval and self.moonJollyIval.isPlaying():
            pass

        ival.append(
            LerpFunctionInterval(
                self.skyGroup.setMoonOverlayAlpha,
                duration=t,
                fromData=fromMoonOverlay,
                toData=toMoonOverlay,
                name='TOD-Trans-MoonJolly'))
        ival.append(
            LerpFunctionInterval(
                self.skyGroup.setMoonSize,
                duration=t,
                fromData=fromMoonSize,
                toData=toMoonSize,
                name='TOD-Trans-MoonSize'))
        if self.moonPhaseIval and self.moonPhaseIval.isPlaying():
            pass

        ival.append(
            LerpFunctionInterval(
                self.setMoonState,
                duration=t,
                fromData=fromMoonState,
                toData=toMoonState,
                name='TOD-Trans-MoonPhase'))

        return ival

    def setMoonState(self, moonPhase):
        if self.moonPhaseIval:
            return None

        self.skyGroup.setMoonState(moonPhase)

    def setMoonStateAnim(self, moonPhase):
        self.skyGroup.setMoonState(moonPhase)

    def animateMoon(self, fromCurrent, startPhase, phase, duration):
        if self.inTransition:
            pass

        if self.moonPhaseIval:
            self.moonPhaseIval.finish()

        if fromCurrent:
            startPhase = self.skyGroup.moonState

        self.moonPhaseIval = Sequence()
        self.moonPhaseIval.append(
            LerpFunctionInterval(
                self.setMoonStateAnim,
                duration=duration,
                fromData=startPhase,
                toData=phase,
                name='animateMoon-Trans-MoonPhase'))
        self.moonPhaseIval.start()

    def switchJollyMoon(self, jolly):
        if not self.moonJolly and jolly:
            self.moonJollyIval = Sequence()
            self.moonJollyIval.append(
                LerpFunctionInterval(
                    self.skyGroup.setMoonOverlayAlpha,
                    duration=3.0,
                    fromData=0.0,
                    toData=0.5,
                    name='Switch-MoonJolly'))
            self.moonJollyIval.start()
        elif self.moonJolly and not jolly:
            self.moonJollyIval = Sequence()
            self.moonJollyIval.append(
                LerpFunctionInterval(
                    self.skyGroup.setMoonOverlayAlpha,
                    duration=3.0,
                    fromData=0.5,
                    toData=0.0,
                    name='Switch-MoonJolly'))
            self.moonJollyIval.start()

        self.moonJolly = jolly

    def _prepareState(self, stateId, environment=None):
        self.notify.debug('_prepareState %s' % stateId)
        if self.forcedStateEnabled:
            return None

        if environment is None:
            environment = self.environment

        if TODGlobals.getTodEnvSetting(
                stateId, environment, 'SkyType') == TODGlobals.SKY_OFF:
            self.skyGroup.stash()
            self.showSky = 0
        else:
            self.skyGroup.unstash()
            self.showSky = 1
        if not self.fixedSky:
            skyType = TODGlobals.getTodEnvSetting(
                stateId, environment, 'SkyType')
            clearColor = TODGlobals.SKY_CLEARCOLORS[skyType]
            self.setSkyClearColor(clearColor)
            if hasattr(base, 'pe'):
                base.setBackgroundColor(
                    base.backgroundDrawable.getClearColor())

            skySettings = TODGlobals.getTodEnvSetting(
                stateId, environment, 'SkyType')
            self.setSkyType(skySettings)

        lastSunDir = TODGlobals.getTodEnvSetting(
            self.lastState, environment, 'Direction')
        self.skyGroup.setSunTrueAngle(lastSunDir)
        if base.cr.activeWorld and hasattr(
                base.cr.activeWorld, 'getWater') and base.cr.activeWorld.getWater():
            if self.use_shader:
                self.seapatch = base.cr.activeWorld.getWater()
            else:
                self.seapatch = base.cr.activeWorld.getWater().patchNP

        if self.use_shader:
            seaColor = TODGlobals.getTodEnvSetting(
                stateId, environment, 'SeaColorShader')
            waterColorFactor = TODGlobals.getTodEnvSetting(
                stateId, environment, 'SeaFactor')
            self.modifyWaterColor(seaColor)
            self.modifyWaterColorFactor(waterColorFactor)
        else:
            seaColor = TODGlobals.getTodEnvSetting(
                stateId, environment, 'SeaColor')
            self.modifyWaterColor(seaColor)
            self.modifyWaterColorFactor()
        fogType = TODGlobals.getTodEnvSetting(stateId, environment, 'FogType')
        self.setFogType(fogType)
        if render.getFog():
            fogColor = TODGlobals.getTodEnvSetting(
                stateId, environment, 'FogColor')
            self.fog.setColor(fogColor)
            fogExp = TODGlobals.getTodEnvSetting(
                stateId, environment, 'FogExp')
            self.setFogExpDensity(fogExp)
            linearFogRanges = TODGlobals.getTodEnvSetting(
                stateId, environment, 'FogLinearRange')
            self.currFogOnset = linearFogRanges[0]
            self.currFogPeak = linearFogRanges[1]
            self.linearFog.setLinearRange(self.currFogOnset, self.currFogPeak)

        lightSwitch = TODGlobals.getTodEnvSetting(
            stateId, environment, 'LightSwitch')
        self.setLightSwitch(lightSwitch)
        envEffect = TODGlobals.getTodEnvSetting(
            stateId, environment, 'EnvEffect')
        self.setEnvEffect(envEffect)
        ambientColor = TODGlobals.getTodEnvSetting(
            stateId, environment, 'AmbientColor')
        self.alight.node().setColor(ambientColor)
        self.grassLight.node().setColor(ambientColor)
        self.shadowLight = self.skyGroup.getShadowLight(stateId)
        self.dlight = self.skyGroup.getLight(stateId)
        if self.dlight:
            highLightColor = TODGlobals.computeLightColor(
                TODGlobals.getTodEnvSetting(
                    stateId, environment, 'FrontColor'), TODGlobals.getTodEnvSetting(
                    stateId, environment, 'AmbientColor'), lightSwitch=lightSwitch)
            self.setFrontLightColor(
                TODGlobals.getTodEnvSetting(
                    stateId, environment, 'FrontColor'))

        if self.shadowLight:
            shadowLightColor = TODGlobals.computeLightColor(
                TODGlobals.getTodEnvSetting(
                    stateId, environment, 'BackColor'), TODGlobals.getTodEnvSetting(
                    stateId, environment, 'AmbientColor'), lightSwitch=lightSwitch)
            self.setBackLightColor(
                TODGlobals.getTodEnvSetting(
                    stateId, environment, 'BackColor'))

        if self.avatarShadowCaster:
            self.avatarShadowCaster.setLightSrc(self.dlight)

    def setSkyType(self, skyType):
        if skyType == TODGlobals.SKY_OFF:
            self.showSky = 0
        else:
            self.showSky = 1
        self.skyGroup.setSky(skyType)
        clearColor = TODGlobals.SKY_CLEARCOLORS[skyType]
        self.setSkyClearColor(clearColor)

    def setSkyClearColor(self, clearColor, override=0):
        self.clearColor = clearColor
        if not self.showSky:
            base.backgroundDrawable.setClearColor(self.fogColor)
            return None

        if not (self.fixedSky) or override:
            base.backgroundDrawable.setClearColor(clearColor)

    def getCurrentIngameTime(self, time=None):
        cycleSpeed = self.cycleSpeed
        if cycleSpeed <= 0:
            cycleSpeed = 1

        if time is None:
            currentTime = globalClockDelta.networkToLocalTime(
                globalClockDelta.getFrameNetworkTime(bits=32))
        else:
            currentTime = time
        REALSECONDS_PER_GAMEDAY = PiratesGlobals.TOD_REALSECONDS_PER_GAMEDAY / cycleSpeed
        REALSECONDS_PER_GAMEHOUR = float(
            REALSECONDS_PER_GAMEDAY /
            PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY)
        cycleDuration = REALSECONDS_PER_GAMEHOUR * \
            PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY
        timeElapsed = currentTime - self.startingServerTime
        timeIntoCycle = (timeElapsed + self.timeOffset) % cycleDuration
        hoursIntoCycle = timeIntoCycle / REALSECONDS_PER_GAMEHOUR
        return hoursIntoCycle

    def getEnvAtTime(self, baseEnv, timeForEnv):
        print 'getEnvAtTime %s %s' % (baseEnv, timeForEnv)
        subEntry = self.envSubstitutionDict.get(baseEnv)
        if not subEntry:
            print ' base %s' % baseEnv
            return baseEnv
        else:
            timeStamp = globalClockDelta.networkToLocalTime(
                subEntry[3], bits=32)
            if timeForEnv > timeStamp:
                print ' sub2 %s' % subEntry[2]
                return subEntry[2]
            else:
                print ' sub1 %s' % subEntry[1]
                return subEntry[1]

    def addEnvSub(self, baseEnv, envReplacement, netTime=None):
        cycleSpeed = self.cycleSpeed
        if cycleSpeed <= 0:
            cycleSpeed = 1

        localNetTime = globalClockDelta.networkToLocalTime(
            globalClockDelta.getFrameNetworkTime(bits=32))
        REALSECONDS_PER_GAMEDAY = PiratesGlobals.TOD_REALSECONDS_PER_GAMEDAY / cycleSpeed
        REALSECONDS_PER_GAMEHOUR = float(
            REALSECONDS_PER_GAMEDAY /
            PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY)
        cycleDuration = REALSECONDS_PER_GAMEHOUR * \
            PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY
        (fieldStartTime, absoluteTODCycle) = self.getSubTimeList(
            self.cycleType, self.environment)
        (previousIndex, currentIndex, nextIndex, stateStartTime) = self.getTODStateDatatAtTime(
            fieldStartTime, absoluteTODCycle, globalClock.getFrameTime(), REALSECONDS_PER_GAMEHOUR)
        previousStateTransTime = absoluteTODCycle[previousIndex][2]
        lastEnv = baseEnv
        envEntry = self.envSubstitutionDict.get(baseEnv)
        if netTime is None:
            netTime = globalClockDelta.getFrameNetworkTime(bits=32)

        timeStamp = globalClockDelta.networkToLocalTime(netTime, bits=32)
        needStartRetro = 0
        if previousStateTransTime and timeStamp < previousStateTransTime and baseEnv == self.environment:
            needStartRetro = 1

        print 'Adding EnvSub for %s stamp %s current time %s netTime %s' % (baseEnv, timeStamp, globalClock.getFrameTime(), localNetTime)
        if envEntry:
            lastEnv = envEntry[2]
        else:
            currentEnvLook = baseEnv
        if lastEnv == envReplacement:
            pass

        newEnvEntry = (baseEnv, lastEnv, envReplacement, netTime)
        self.envSubstitutionDict[baseEnv] = newEnvEntry
        if baseEnv == self.environment:
            if self.inTransition:
                self.needCheckSub = 1
            else:
                self.doStartTimeOfDay()
                return None

        if needStartRetro:
            if self.debugTOD:
                base.talkAssistant.receiveGameMessage(
                    'Starting time of day for retroActive TimeStamp')

            if self.transitionIval:
                self.transitionIval.finish()
                self.transitionIval = None

            self.doStartTimeOfDay()

    def getEnvSub(self, environment, testTime):
        entry = self.envSubstitutionDict.get(environment)
        if not entry:
            return environment
        else:
            netTime = entry[3]
            timeStamp = globalClockDelta.networkToLocalTime(netTime, bits=32)
            if testTime > timeStamp:
                return entry[2]
            else:
                return entry[1]

    def getSubTimeList(self, cycleType, env):
        if self.notify.getDebug():
            print 'getSubTimeList'
        cycleSpeed = self.cycleSpeed
        if cycleSpeed <= 0:
            cycleSpeed = 1

        REALSECONDS_PER_GAMEDAY = PiratesGlobals.TOD_REALSECONDS_PER_GAMEDAY / cycleSpeed
        REALSECONDS_PER_GAMEHOUR = float(
            REALSECONDS_PER_GAMEDAY /
            PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY)
        cycleDuration = REALSECONDS_PER_GAMEHOUR * \
            PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY
        cycleList = TODGlobals.CycleStateTimeList.get(
            cycleType) + TODGlobals.CycleStateTimeList.get(cycleType) + TODGlobals.CycleStateTimeList.get(cycleType)
        modCycleList = []
        currentGameTime = self.getCurrentIngameTime()
        currentFrameTime = globalClock.getFrameTime()
        subCycleTimeStart = None
        subCycleTimeTransEnd = None
        sub = self.envSubstitutionDict.get(env)
        if self.notify.getDebug():
            print ' sub was %s for %s' % (sub, env)
        gameTimeToSeconds = currentGameTime * REALSECONDS_PER_GAMEHOUR
        cycleStartFrameTime = currentFrameTime - gameTimeToSeconds
        cycleEndFrameTime = currentFrameTime + \
            (cycleDuration - gameTimeToSeconds)
        fieldStartFrameTime = cycleStartFrameTime - REALSECONDS_PER_GAMEDAY
        fieldEndFrameTime = cycleEndFrameTime + REALSECONDS_PER_GAMEDAY
        subInField = 0
        subBeforeField = 0
        subAfterField = 0
        if sub:
            netTime = sub[3]
            timeStamp = globalClockDelta.networkToLocalTime(netTime, bits=32)
            if self.notify.getDebug():
                print 'Sub TimeStamp %s current Time %s' % (timeStamp, currentFrameTime)
            if timeStamp > fieldStartFrameTime and timeStamp < fieldEndFrameTime:
                if self.notify.getDebug():
                    print ' sub found in current cycle'
                start = timeStamp - cycleStartFrameTime
                subCycleTimeStart = float(start) / REALSECONDS_PER_GAMEHOUR
                subCycleTimeTransEnd = subCycleTimeStart + sub[3]
                subInField = 1
            elif timeStamp > fieldEndFrameTime:
                subAfterField = 1
            elif timeStamp < fieldStartFrameTime:
                subBeforeField = 1

        absoluteTimeList = self.getAbsoluteTimeList(
            cycleList, -(PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY))
        if not sub:
            newBaseCycleEntry = absoluteTimeList
        else:
            envPre = sub[1]
            envPost = sub[2]
            if subInField:
                subStart = subCycleTimeStart
                subLength = 1.0
                subEnd = subStart + subLength
                noSub = 0

            subListAbsolute = []
            index = 0
            for timeEntry in absoluteTimeList:
                vId = timeEntry[0]
                startTime = timeEntry[1]
                transEndTime = timeEntry[2]
                endTime = timeEntry[3]
                transLength = transEndTime - startTime
                subEntry = None
                if (subAfterField or subInField) and endTime < subStart:
                    regEntry = (vId, startTime, transEndTime, endTime, envPre)
                    subListAbsolute.append(regEntry)
                    index += 1
                    continue
                if (subBeforeField or subInField) and startTime > subEnd:
                    regEntry = (vId, startTime, transEndTime, endTime, envPost)
                    subListAbsolute.append(regEntry)
                    index += 1
                    continue
                if subEnd > endTime:
                    regEntry = (vId, startTime, transEndTime, endTime, envPre)
                    subListAbsolute.append(regEntry)
                    index += 1
                    continue
                if subStart < transEndTime:
                    regEntry = (
                        vId,
                        startTime,
                        transEndTime,
                        transEndTime,
                        envPre)
                    index += 1
                    subListAbsolute.append(regEntry)
                    subStart = transEndTime
                    subLength = 1.0
                    subEnd = subStart + subLength
                    subEntry = (vId, subStart, subEnd, endTime, envPost)
                    subListAbsolute.append(subEntry)
                    index += 1
                    continue
                regEntry = (vId, startTime, transEndTime, subStart, envPre)
                subListAbsolute.append(regEntry)
                index += 1
                subLength = 1.0
                subEntry = (vId, subStart, subEnd, endTime, envPost)
                index += 1
                subListAbsolute.append(subEntry)

            newBaseCycleEntry = subListAbsolute
        index = 0
        for timeEntry in newBaseCycleEntry:
            index += 1

        return (fieldStartFrameTime, newBaseCycleEntry)

    def getTODStateDatatAtTime(self, fieldStartTimeInSeconds,
                               absoluteCycleList, currentTimeSeconds, secondsPerHour):
        fieldStartHour = absoluteCycleList[0][1]
        timeInHours = fieldStartHour + \
            (currentTimeSeconds - fieldStartTimeInSeconds) / secondsPerHour
        currentIndex = 0
        nextIndex = None
        previousIndex = None
        stateStartTime = None
        for stateIndex in xrange(len(absoluteCycleList)):
            state = absoluteCycleList[stateIndex]
            tod = state[0]
            time = state[1]
            transTime = state[2]
            if time <= timeInHours:
                currentIndex = stateIndex
                stateStartTime = time
                continue

        nextIndex = (currentIndex + 1) % len(absoluteCycleList)
        previousIndex = currentIndex - 1
        if previousIndex < 0:
            previousIndex = len(absoluteCycleList) - 1

        return (previousIndex, currentIndex, nextIndex, stateStartTime)

    def getAbsoluteTimeList(self, cycleList, startTime=0):
        absoluteTimeList = []
        runningTimeTotal = startTime
        for timeEntry in cycleList:
            absoluteTimeList.append(
                (timeEntry[0],
                 runningTimeTotal,
                 runningTimeTotal +
                 timeEntry[2],
                    runningTimeTotal +
                    timeEntry[1],
                    None))
            runningTimeTotal += timeEntry[1]

        return absoluteTimeList

    def setInTransition(self, inTrans):
        self.inTransition = inTrans
        if self.needCheckSub and self.inTransition == 0:
            self.needCheckSub = 0
            self.doStartTimeOfDay()

    def setDesiredTime(self, desiredTime):
        cycleSpeed = self.cycleSpeed
        if cycleSpeed <= 0:
            cycleSpeed = 1

        REALSECONDS_PER_GAMEDAY = PiratesGlobals.TOD_REALSECONDS_PER_GAMEDAY / cycleSpeed
        REALSECONDS_PER_GAMEHOUR = float(
            REALSECONDS_PER_GAMEDAY /
            PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY)
        cycleDuration = REALSECONDS_PER_GAMEHOUR * \
            PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY
        currentTime = self.getCurrentIngameTime() - self.timeOffset / \
            REALSECONDS_PER_GAMEHOUR
        offsetInHours = (
            desiredTime - currentTime) % PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY
        offsetInSeconds = offsetInHours * REALSECONDS_PER_GAMEHOUR
        self.timeOffset = offsetInSeconds

    def doStartTimeOfDayTask(self, task=None):
        self.doStartTimeOfDay()
        return task.done

    def doStartTimeOfDay(self, initial=0):
        pauseTOD = 0
        cycleSpeed = self.cycleSpeed
        if cycleSpeed <= 0:
            cycleSpeed = 1
            pauseTOD = 1

        REALSECONDS_PER_GAMEDAY = PiratesGlobals.TOD_REALSECONDS_PER_GAMEDAY / cycleSpeed
        REALSECONDS_PER_GAMEHOUR = float(
            REALSECONDS_PER_GAMEDAY /
            PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY)
        cycleDuration = REALSECONDS_PER_GAMEHOUR * \
            PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY
        lastTime = self.startTodTime
        self.startTodTime = globalClockDelta.networkToLocalTime(
            globalClockDelta.getFrameNetworkTime(bits=32))
        lastTODlength = self.startTodTime - lastTime
        (fieldStartTime, absoluteTODCycle) = self.getSubTimeList(
            self.cycleType, self.environment)
        startServerTime = self.startingServerTime
        currentTimeSeconds = globalClock.getFrameTime()
        totalElapsedTime = (
            currentTimeSeconds - startServerTime) + self.timeOffset
        timeIntoCycle = totalElapsedTime % cycleDuration
        hoursIntoCycle = timeIntoCycle / REALSECONDS_PER_GAMEHOUR
        currentGameTimeInHours = hoursIntoCycle
        (previousIndex, currentIndex, nextIndex, stateStartTime) = self.getTODStateDatatAtTime(
            fieldStartTime, absoluteTODCycle, currentTimeSeconds + 0.5, REALSECONDS_PER_GAMEHOUR)
        previousStateStartTime = absoluteTODCycle[previousIndex][1]
        currentStateData = absoluteTODCycle[currentIndex]
        TOD = currentStateData[0]
        totalStateTimeHours = currentStateData[3] - currentStateData[1]
        totalTransTimeHours = currentStateData[2] - currentStateData[1]
        if totalTransTimeHours > totalStateTimeHours:
            totalTransTimeHours = totalStateTimeHours

        self.currentState = TOD
        secondsIntoCycle = float(
            currentGameTimeInHours - stateStartTime) * REALSECONDS_PER_GAMEHOUR
        secondsLeftInCycle = float(
            totalTransTimeHours) * REALSECONDS_PER_GAMEHOUR - secondsIntoCycle
        if secondsIntoCycle < 0 and 0:
            taskMgr.doMethodLater(
                1.0, self.doStartTimeOfDayTask, self.waitTaskName)
            return None

        self.lastState = absoluteTODCycle[previousIndex][0]
        self.currentStateDuration = float(
            totalStateTimeHours) * REALSECONDS_PER_GAMEHOUR
        stateDuration = self.currentStateDuration
        transitionTimeSeconds = float(
            totalTransTimeHours) * REALSECONDS_PER_GAMEHOUR
        stateStartTime = currentTimeSeconds - secondsIntoCycle
        previousStateStartTime = absoluteTODCycle[previousIndex][1]
        previoudStateEndTime = absoluteTODCycle[previousIndex][3]
        previousLength = (previoudStateEndTime -
                          previousStateStartTime) * REALSECONDS_PER_GAMEHOUR
        startEnv = absoluteTODCycle[previousIndex][4]
        destEnv = absoluteTODCycle[currentIndex][4]
        if startEnv is None:
            startEnv = self.environment

        if destEnv is None:
            destEnv = self.environment

        if (initial or self.lastState ==
                self.currentState) and startEnv == destEnv:
            self._prepareState(self.currentState, environment=destEnv)

        newEffective = (startEnv, destEnv)
        self.lastEffective = newEffective
        elapsedTime = secondsIntoCycle
        if self.debugTOD:
            base.talkAssistant.receiveGameMessage('TOD:%s T Sec:%s D Sec:%s In Sec:%s\nfrom %s-%s to %s-%s\nNext %s ' % (str(currentGameTimeInHours)[:5], str(transitionTimeSeconds)[:5], str(stateDuration)[:5], str(secondsIntoCycle)[
                                                  :6], TODGlobals.ENV_DEBUG_NAMES[startEnv], TODGlobals.StateDict[absoluteTODCycle[previousIndex][0]], TODGlobals.ENV_DEBUG_NAMES[destEnv], TODGlobals.StateDict[absoluteTODCycle[currentIndex][0]], TODGlobals.StateDict[absoluteTODCycle[nextIndex][0]]))

        if TODGlobals.SunRotationStates[self.lastState] != TODGlobals.SunRotationStates[self.currentState]:
            fade = 1
            transitionTime = min(
                transitionTimeSeconds,
                TODGlobals.NONGROUP_MAX_TRANSITION_TIME)
            sunMoveTime = transitionTime
        else:
            fade = 0
            sunMoveTime = stateDuration
        sunCorrection = elapsedTime
        if initial:
            sunDirLast = TODGlobals.getTodEnvSetting(
                self.lastState, destEnv, 'Direction')
            self.skyGroup.setSunTrueAngle(sunDirLast)
            sunCorrection = 0

        sunDir = TODGlobals.getTodEnvSetting(
            self.currentState, destEnv, 'Direction')
        if self.transitionIval:
            self.transitionIval.finish()
            self.transitionIval = None

        if self.sunMoveIval:
            self.sunMoveIval.pause()
            self.sunMoveIval = None

        masterIval = Parallel()
        transAndClearIval = Sequence()
        if self.lastState != self.currentState or startEnv != destEnv:
            self.setInTransition(1)
            timeofDayTrans = self._transitionTimeOfDay(
                self.lastState,
                self.currentState,
                transitionTimeSeconds,
                startEnv=startEnv,
                destEnv=destEnv)
            transClearIval = Sequence()
            transClearIval.append(Wait(transitionTimeSeconds))
            transClearIval.append(Func(self.setInTransition, 0))
            transAndClearIval.append(timeofDayTrans)
            transAndClearIval.append(Func(self.setInTransition, 0))
            masterIval.append(transAndClearIval)

        self.sunMoveIval = self.skyGroup.transitionSunAngle(
            sunDir, sunMoveTime - sunCorrection, fade, sunDirLast=None)
        self.transitionIval = masterIval
        self.transitionIval.start(elapsedTime)
        if initial:
            self.sunMoveIval.start(elapsedTime)
        else:
            self.sunMoveIval.start()
        taskMgr.remove(self.waitTaskName)
        if not pauseTOD:
            timeToNextState = self.currentStateDuration - elapsedTime
            taskMgr.doMethodLater(
                timeToNextState,
                self.doStartTimeOfDayTask,
                self.waitTaskName)
        else:
            self.transitionIval.finish()
            self.sunMoveIval.finish()
        self.accept('settingLocalShip', self.switchFogDensity)
        messenger.send('timeOfDayChange', [
            self.currentState,
            stateDuration,
            elapsedTime,
            transitionTimeSeconds])
        return (stateDuration, elapsedTime, transitionTimeSeconds)

    def doEndTimeOfDay(self):
        self.currentStateDuration = None
        self.notify.debug('exit: %s' % self.currentState)
        self.ignore('settingLocalShip')
        taskMgr.remove(self.waitTaskName)
        if self.transitionIval:
            self.transitionIval.pause()
            self.transitionIval = None

    def enterEnvironmentTOD(self):
        self.notify.debug('enterEnvironmentTOD')
        (stateDuration, elapsedTime, transitionTime) = self.doStartTimeOfDay(initial=1)

    def exitEnvironmentTOD(self):
        self.notify.debug('exitEnvironmentTOD')
        self.doEndTimeOfDay()

    def enterNoLighting(self):
        self.notify.debug('enter: NoLighting')
        taskMgr.remove(self.waitTaskName)
        if self.transitionIval:
            self.transitionIval.pause()
            self.transitionIval = None

        render.clearLight(self.alight)
        render.clearLight(self.shadowLight)
        render.clearLight(self.sunLight)
        render.setFogOff()
        messenger.send('nametagAmbientLightChanged', [None])
        if self.nextDoLater:
            self.nextDoLater.remove()
            self.nextDoLater = None

    def exitNoLighting(self):
        self.notify.debug('exit: NoLighting')
        render.setLight(self.alight)
        render.setLight(self.sunLight)
        render.setLight(self.shadowLight)
        messenger.send('nametagAmbientLightChanged', [
            self.alight])

    def enterIndoors(self, todSettings=None):
        self.notify.debug('enterIndoors')
        self.currentState = PiratesGlobals.TOD_CUSTOM
        self.fixedSky = True
        self._prepareState(self.currentState)
        sunDir = TODGlobals.getTodEnvSetting(
            self.currentState, self.environment, 'Direction')
        self.skyGroup.setSunTrueAngle(sunDir)
        if hasattr(base, 'pe'):
            self._prepareState(PiratesGlobals.TOD_CUSTOM)
            self.setSkyClearColor(Vec4(0, 0, 0, 0), 1)
            base.setBackgroundColor(base.backgroundDrawable.getClearColor())
            self.linearFog.setColor(
                TODGlobals.getTodEnvSetting(
                    PiratesGlobals.TOD_CUSTOM,
                    self.environment,
                    'FogColor'))

        if todSettings:
            if todSettings.get('AmbientColors') and todSettings['AmbientColors'].get(
                    self.currentState):
                self.setFillLightColor(
                    todSettings['AmbientColors'][self.currentState])

            if todSettings.get('DirectionalColors') and todSettings['DirectionalColors'].get(
                    self.currentState):
                self.setFrontLightColor(
                    todSettings['DirectionalColors'][self.currentState])

            if todSettings.get('BacklightColors') and todSettings['BacklightColors'].get(
                    self.currentState):
                self.setBackLightColor(
                    todSettings['BacklightColors'][self.currentState])

            if todSettings.get('LightSwitches') and todSettings['LightSwitches'].get(
                    self.currentState):
                self.setLightSwitch(
                    todSettings['LightSwitches'][self.currentState])

            if todSettings.get('SunDirections') and todSettings['SunDirections'].get(
                    self.currentState):
                self.skyGroup.setSunTrueAngle(
                    todSettings['SunDirections'][self.currentState])

            if todSettings.get('FogColors') and todSettings['FogColors'].get(
                    self.currentState):
                fogColor = todSettings['FogColors'][self.currentState]
                self.linearFog.setColor(fogColor)
                self.setSkyClearColor(fogColor, 1)

            if todSettings.get('LinearFogRanges') and todSettings['LinearFogRanges'].get(
                    self.currentState):
                fogRanges = todSettings['LinearFogRanges'][self.currentState]
                self.currFogOnset = fogRanges[0]
                self.currFogPeak = fogRanges[1]
                self.defaultFogOnset = self.currFogOnset
                self.defaultFogPeak = self.currFogPeak
                base.farCull.setPos(0, self.currFogPeak + 5, 0)
                self.linearFog.setLinearRange(
                    self.currFogOnset, self.currFogPeak)

            if todSettings.get('FogRanges') and todSettings['FogRanges'].get(
                    self.currentState):
                fogDensity = todSettings['FogRanges'][self.currentState]
                self.setFogExpDensity(fogDensity)

            if todSettings.get('FogTypes') and todSettings['FogTypes'].get(
                    self.currentState):
                fogType = todSettings['FogTypes'][self.currentState]
                self.setFogType(fogType)

        messenger.send('timeOfDayChange', [
            self.currentState,
            0,
            0,
            0])

    def exitIndoors(self):
        self.notify.debug('exitIndoors')
        self.fixedSky = False
        base.positionFarCull()

    def enterOff(self):
        self.notify.debug('enter: Off')
        if self.transitionIval:
            self.transitionIval.pause()
            self.transitionIval = None

        self.disableAvatarShadows()
        taskMgr.remove(self.waitTaskName)
        render.clearLight(self.alight)
        render.clearLight(self.dlight)
        messenger.send('nametagAmbientLightChanged', [
            None])
        if self.nextDoLater:
            self.nextDoLater.remove()
            self.nextDoLater = None

    def exitOff(self):
        self.notify.debug('exit: Off')
        render.setLight(self.alight)
        render.setLight(self.dlight)
        if base.win and not base.win.isClosed():
            if base.config.GetBool('want-avatar-shadows', 1):
                self.enableAvatarShadows()

        messenger.send('nametagAmbientLightChanged', [
            self.alight])

    def getTimeUntil(self, stateId):
        if not TODGlobals.isStateIdValid(self.cycleType, stateId):
            return self.cycleDuration

        (currStateId, remTime) = self._computeCurrentState()
        if currStateId == stateId:
            return -remTime

        while currStateId != stateId:
            currStateId = TODGlobals.getNextStateId(
                self.cycleType, currStateId)
            stateDuration = TODGlobals.getStateDuration(
                self.cycleType, currStateId) * self.cycleDuration
            remTime += stateDuration
        return remTime - stateDuration

    def setEnvironment(self, envId, envData=None):
        print 'setEnvironment %s %s %s' % (TODGlobals.ENVIRONMENT_NAMES.get(envId, 'unnamed'), envId, envData)
        envName = TODGlobals.ENVIRONMENT_NAMES.get(envId, 'Unknown')
        self.notify.debug('setEnvironment: %s' % envId)
        if self.environment == envId and envData is None:
            return None

        self.environment = envId
        if envData is not None:
            TODGlobals.ENV_SETTINGS_DICT[TODGlobals.ENV_DATAFILE] = envData

        self.fixedSky = False
        self.disableForcedState()
        self.enterInitState()
        messenger.send('environmentChanged')

    def setEnvEffect(self, effectNumber):
        if effectNumber != self.envEffect:
            self.stopEnvEffect(self.envEffect)
            self.startEnvEffect(effectNumber)

        self.envEffect = effectNumber

    def stopEnvEffect(self, envNum):
        if envNum == 0:
            pass

        if envNum == 1:
            self.envSound.stop()
            del self.envSound
            self.endAmbientSFX()

    def startEnvEffect(self, envNum):
        if envNum == 0:
            pass

        if envNum == 1:
            self.envSound = loader.loadSfx('audio/sfx_ocean_wind.mp3')
            self.envSound.setLoop(True)
            self.envSound.setVolume(0.69999999999999996)
            self.envSound.setPlayRate(1.0)
            self.envSound.play()
            self.startAmbientSFX()

    def registerAmbientSFXNode(self, node):
        if node not in self.ambientSFXList:
            self.ambientSFXList.append(node)

    def removeAmbientSFXNode(self, node):
        if node in self.ambientSFXList:
            self.ambientSFXList.remove(node)

    def runAmbientSFXTask(self, task=None):
        if not self.inAmbTime or self.closestNode is None:
            self.ambSound.setVolume(0.0)
            if task:
                return task.cont
            else:
                return None

        minDistance = self.closestNode.getDistance(base.cam)
        cutoff = 500.0
        fullrange = 50.0
        fullCut = cutoff + fullrange
        if minDistance <= fullCut and self.timeVol:
            volume = min(1.0, 1.0 - float(minDistance / fullCut))
            self.ambSound.setVolume(volume * self.timeVol)
        else:
            volume = 0
            self.ambSound.setVolume(0.0)
        if task:
            return task.cont

    def recalcClosestAmbNode(self, task=None):
        taskMgr.remove('ambientNodeSFXTask')
        minDistance = None
        self.closestNode = None
        for node in self.ambientSFXList:
            distance = node.getDistance(base.cam)
            if minDistance is None or distance < minDistance:
                minDistance = distance
                self.closestNode = node
                continue

        taskMgr.doMethodLater(
            2.5,
            self.recalcClosestAmbNode,
            'ambientNodeSFXTask')
        timeStart = (5.5, 6.0)
        timeEnd = (20.0, 20.5)
        self.timeVol = 1.0
        timeCurrent = self.getCurrentIngameTime()
        if timeCurrent < timeStart[0] or timeCurrent > timeEnd[1]:
            self.timeVol = 0
            if self.inAmbTime:
                self.envSound.stop()
                self.ambSound.stop()

            self.inAmbTime = 0
        elif timeCurrent < timeStart[1]:
            timeDiff = timeStart[0] - timeStart[1]
            self.timeVol = 1.0 - (timeCurrent - timeStart[1]) / timeDiff
            if not self.inAmbTime:
                self.envSound.play()
                self.ambSound.play()

            self.inAmbTime = 1
        elif timeCurrent > timeEnd[0]:
            timeDiff = timeEnd[0] - timeEnd[1]
            self.timeVol = 1.0 - (timeEnd[0] - timeCurrent) / timeDiff
            if not self.inAmbTime:
                self.envSound.play()
                self.ambSound.play()

            self.inAmbTime = 1
        elif not self.inAmbTime:
            self.envSound.play()
            self.ambSound.play()

        self.inAmbTime = 1
        if self.environment == TODDefs.ENV_INTERIOR:
            self.timeVol = self.timeVol * 0.65000000000000002

        self.envSound.setVolume(0.69999999999999996 * self.timeVol)
        if task:
            return task.done

    def startAmbientSFX(self):
        self.ambSound = loader.loadSfx('audio/sfx_ocean_shore.mp3')
        self.ambSound.setLoop(True)
        self.ambSound.setVolume(0.0)
        self.ambSound.setPlayRate(1.0)
        self.ambSound.play()
        self.closestNode = None
        self.inAmbTime = 0
        self.recalcClosestAmbNode()
        taskMgr.add(self.runAmbientSFXTask, 'ambientRangeSFXTask')

    def endAmbientSFX(self):
        self.ambSound.stop()
        del self.ambSound
        del self.closestNode
        del self.inAmbTime
        taskMgr.remove('ambientRangeSFXTask')
        taskMgr.remove('ambientNodeSFXTask')

    def enableForcedState(self, state=None, gameArea=None):
        if state and gameArea:
            self.request(state, gameArea)
        elif state:
            self.request(state)

        self.forcedStateEnabled = True

    def disableForcedState(self):
        self.forcedStateEnabled = False

    def modifyWaterColor(self, color):
        self.lastWaterColor = color
        if not self.seapatch:
            return None

        if self.use_shader:
            v3Color = Vec3(color[0], color[1], color[2])
            if not self.seapatch.seamodel.isEmpty():
                self.seapatch.modify_water_color_add_np(v3Color)

        elif not self.seapatch.isEmpty():
            self.seapatch.setColorScale(color)

    def modifyWaterColorFactor(self, colorFactor=None):
        self.lastWaterColorFactor = colorFactor
        if not self.seapatch:
            return None

        if colorFactor is None:
            self.waterColorFactor = Vec3(1.0, 1.0, 1.0)
        else:
            self.waterColorFactor = Vec3(
                colorFactor[0], colorFactor[1], colorFactor[2])
        if self.use_shader:
            if not self.seapatch.seamodel.isEmpty():
                self.seapatch.modify_water_color_factor_np(
                    self.waterColorFactor)

    def setSaintPatricksSea(self):
        if self.use_shader:
            self.modifyWaterColor(
                VBase3(
                    0.22,
                    0.56000000000000005,
                    0.14999999999999999))
            self.modifyWaterColorFactor(
                VBase3(
                    0.40000000000000002,
                    1.0,
                    0.29999999999999999))
        else:
            self.modifyWaterColor(
                VBase4(
                    0.25,
                    0.90000000000000002,
                    0.20000000000000001,
                    1.0))
            self.modifyWaterColorFactor()

    def handleHolidayStarted(self, holidayName):
        pass

    def handleHolidayEnded(self, holidayName):
        pass

    def setFogColor(self, fogColor):
        self.fogColor = fogColor
        if self.linearFog:
            self.linearFog.setColor(fogColor)

        if self.fog:
            self.fog.setColor(fogColor)

    def getFogColor(self):
        return self.fogColor

    def setFogMask(self, fogMask):
        self.fogMask = fogMask
        self.setFogType(self.fogType, 1)

    def setFogType(self, fogType, override=0):
        if fogType != self.fogType or override:
            render.clearFog()
            self.fogType = fogType
            if not self.fogMask:
                if self.fogType == TODGlobals.FOG_EXP:
                    self.fog.setExpDensity(self.fogExpDensity)
                    self.fog.setColor(self.fogColor)
                    render.setFog(self.fog)
                elif self.fogType == TODGlobals.FOG_LINEAR:
                    self.linearFog.setColor(self.fogColor)
                    base.farCull.setPos(0, self.currFogPeak + 5, 0)
                    self.linearFog.setLinearRange(self.currFogOnset, self.currFogPeak)
                    render.setFog(self.linearFog)

    def setLinearFogOnset(self, onset):
        self.currFogOnset = onset
        self.linearFog.setLinearRange(self.currFogOnset, self.currFogPeak)

    def setLinearFogPeak(self, peak):
        self.currFogPeak = peak
        self.linearFog.setLinearRange(self.currFogOnset, self.currFogPeak)
        base.farCull.setPos(0, self.currFogPeak + 5, 0)

    def setFogExpDensity(self, newValue):
        self.fogExpDensity = newValue
        if self.fog:
            if hasattr(base, 'localAvatar') and base.localAvatar.ship:
                self.fog.setExpDensity(
                    self.fogExpDensity * TODGlobals.SHIP_FOG_MULT)
            else:
                self.fog.setExpDensity(self.fogExpDensity)

    def getFogExpDensity(self):
        return self.fogExpDensity

    def switchFogDensity(self, onShip):
        if onShip:
            self.fog.setExpDensity(
                self.fogExpDensity *
                TODGlobals.SHIP_FOG_MULT)
        else:
            self.fog.setExpDensity(self.fogExpDensity)

    def restoreLinearFog(self):
        return None
        if self.currFogOnset == self.defaultFogOnset and self.currFogPeak == self.defaultFogPeak:
            return None

        self.lerpLinearFog(self.defaultFogOnset, self.defaultFogPeak)

    def lerpLinearFog(self, targetOnset, targetPeak, lerpTime=1.0):
        if self.lerpFogIval:
            self.lerpFogIval.pause()

        baseOnset = self.currFogOnset
        basePeak = self.currFogPeak

        def setLinearFog(v):
            self.currFogOnset = baseOnset * (1 - v) + targetOnset * v
            self.currFogPeak = basePeak * (1 - v) + targetPeak * v
            base.farCull.setPos(0, self.currFogPeak + 10, 0)
            self.linearFog.setLinearRange(self.currFogOnset, self.currFogPeak)

        self.lerpFogIval = LerpFunctionInterval(
            setLinearFog,
            duration=lerpTime,
            fromData=0.0,
            toData=1.0,
            name='LerpFogIval')
        self.lerpFogIval.start()

    def getEnviroDictString(self, environment=None, tabs=0, heading='SettingsDict ='):
        if environment is None:
            environment = self.environment

        envDict = TODGlobals.ENV_SETTINGS_DICT[environment]
        tab = '    '
        outputString = ''
        outputString += tab * tabs
        outputString += '%s {' % heading
        outputString += '\n'
        for timeIndex in TODGlobals.INORDER_TOD_LIST:
            timeName = TODGlobals.StateDict.get(timeIndex)
            timeDict = envDict.get(timeName)
            if timeDict and timeDict != {}:
                outputString += tab * tabs
                outputString += '    "%s" : {' % timeName
                outputString += '\n'
                for timeSettingName in TODGlobals.TOD_ATTRIBUTES:
                    timeSetting = timeDict.get(timeSettingName)
                    if timeSetting is not None:
                        if timeSettingName == 'FogType':
                            timeSetting = TODGlobals.FOG_CODES[timeSetting]
                        elif timeSettingName == 'SkyType':
                            timeSetting = TODGlobals.SKY_CODES[timeSetting]

                        outputString += tab * tabs
                        outputString += '        "%s" : %s,' % (
                            timeSettingName, timeSetting)
                        outputString += '\n'
                        continue

                outputString += tab * tabs
                outputString += '        },'
                outputString += '\n'
                continue

        outputString += tab * tabs
        outputString += '}'
        return outputString
