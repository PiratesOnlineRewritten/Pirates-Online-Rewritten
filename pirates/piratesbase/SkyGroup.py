from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPRender
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPRender
from direct.showbase import PythonUtil
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import TODGlobals

class SkyGroup(NodePath):

    def __init__(self):
        NodePath.__init__(self, 'SkyGroup')
        self.relativeCompass = self.attachNewNode('relativeCompass')
        self.skyHandle = self.relativeCompass.attachNewNode('relativeCompass')
        self.sunDepth = 2300
        self.overallScale = 10
        self.lightDepth = self.sunDepth * self.overallScale
        self.hide(OTPRender.MainCameraBitmask)
        self.showThrough(OTPRender.EnviroCameraBitmask)
        self.showThrough(OTPRender.SkyReflectionCameraBitmask)
        self.setEffect(CompassEffect.make(NodePath(), CompassEffect.PRot))
        self.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CRed | ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue))
        self.setTransparency(1)
        self.setColorScaleOff()
        self.setDepthWrite(0)
        self.setDepthTest(0)
        self.clearFog()
        self.setFogOff()
        self.setLightOff()
        self.setHpr(0.0, 0.0, 0.0)
        self.setScale(self.overallScale)
        self.setZ(-10)
        self.lockSunPos = 0
        self.lastSky = 0
        skydome = loader.loadModel('models/sky/PiratesSkyDome')
        geoms = skydome.findAllMatches('**/+GeomNode')
        for geom in geoms:
            self._clearTexAttrib(geom)

        self.sides = skydome.find('**/Sides')
        self.sides.setBin('background', 102)
        self.sides.reparentTo(self.skyHandle)
        self.top = skydome.find('**/Top')
        self.top.setBin('background', 104)
        self.top.reparentTo(self.skyHandle)
        self.horizon = skydome.find('**/Horizon')
        self.horizon.setBin('background', 125)
        self.horizon.hide(OTPRender.ReflectionCameraBitmask)
        self.horizon.reparentTo(self.skyHandle)
        self.clouds = skydome.find('**/CloudsTop')
        self.clouds.setBin('background', 125)
        self.clouds.reparentTo(self.skyHandle)
        self.stars = loader.loadModel('models/sky/pir_m_are_wor_stars')
        self.stars.setBin('background', 103)
        self.stars.setColorScale(1, 1, 1, 0.25)
        self.stars.reparentTo(self.skyHandle)
        self.skyHandle.setH(180)
        textures = loader.loadModel('models/sky/PiratesSkyDomeCards')
        self.texCloudsLight = textures.find('**/clouds_light').findAllTextures()[0]
        self.texCloudsMedium = textures.find('**/clouds_medium').findAllTextures()[0]
        self.texCloudsHeavy = textures.find('**/clouds_heavy').findAllTextures()[0]
        self.texOpaque = textures.find('**/opaque').findAllTextures()[0]
        self.texTransparent = textures.find('**/transparent').findAllTextures()[0]
        self.texGradient = textures.find('**/gradient').findAllTextures()[0]
        self.texStars = textures.find('**/stars').findAllTextures()[0]
        self.cloudSettings = {0: (self.texTransparent, ''),1: (self.texCloudsLight, ''),2: (self.texCloudsMedium, ''),3: (self.texCloudsHeavy, '')}
        self.skySettings = {TODGlobals.SKY_OFF: [(self.texTransparent, '', VBase4(0, 0, 0, 0), VBase4(0.0, 0.0, 0.0, 1)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0.0, 0.0, 0.0, 1)), VBase4(0.0, 0.0, 0.0, 1), VBase4(0.0, 0.0, 0.0, 1)],TODGlobals.SKY_DAWN: [(self.texTransparent, '', VBase4(0, 0, 0, 0), VBase4(0.8, 0.5, 0.2, 1)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0.4, 0.58, 0.6, 1)), VBase4(0.8, 0.8, 0.6, 1), VBase4(0.29, 0.32, 0.44, 1)],TODGlobals.SKY_DAY: [(self.texTransparent, '', VBase4(0, 0, 0, 0), VBase4(1, 1, 1, 0.7)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0.45, 0.55, 0.7, 0)), VBase4(1, 1, 1, 1), VBase4(0.6, 0.7, 0.9, 1)],TODGlobals.SKY_DUSK: [(self.texTransparent, '', VBase4(0, 0, 0, 0), VBase4(0.6, 0.365, 0.325, 1)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0.45, 0.4, 0.52, 1)), VBase4(0.75, 0.35, 0.22, 1), VBase4(0.46, 0.38, 0.43, 1)],TODGlobals.SKY_NIGHT: [(self.texStars, '', VBase4(0.1, 0.1, 0.1, 0.1), VBase4(0.36, 0.48, 0.74, 0.8)), (self.texStars, '', VBase4(0, 0, 0, 0), VBase4(0.36, 0.48, 0.74, 0.2)), VBase4(0.34, 0.45, 0.7, 0.8), VBase4(0.11, 0.18, 0.33, 1)],TODGlobals.SKY_STARS: [(self.texStars, '', VBase4(0.85, 0.8, 0.5, 0.5), VBase4(1, 1, 1, 1)), (self.texStars, '', VBase4(0, 0, 0, 0), VBase4(1, 1, 1, 1)), VBase4(0.45, 0.45, 0.7, 0.6), VBase4(0.09, 0.09, 0.24, 1)],TODGlobals.SKY_HALLOWEEN: [(self.texStars, '', VBase4(0, 0, 0, 0.2), VBase4(0.5, 0.6, 0.15, 1)), (self.texStars, '', VBase4(0, 0, 0, 0), VBase4(1, 1, 1, 0.4)), VBase4(0.5, 0.6, 0.15, 1), VBase4(0.1, 0.12, 0.03, 1)],TODGlobals.SKY_SWAMP: [(self.texTransparent, '', VBase4(0, 0, 0, 0), VBase4(0.35, 0.5, 0.6, 1)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0.35, 0.5, 0.6, 0)), VBase4(0.35, 0.5, 0.6, 1), VBase4(0.15, 0.2, 0.35, 1)],TODGlobals.SKY_INVASION: [(self.texStars, '', VBase4(0, 0, 0, 0.2), VBase4(0.15, 0.18, 0.06, 1)), (self.texStars, '', VBase4(0, 0, 0, 0), VBase4(1, 1, 1, 0.4)), VBase4(0.15, 0.18, 0.06, 1), VBase4(0.1, 0.12, 0.03, 1)],TODGlobals.SKY_OVERCAST: [(self.texTransparent, '', VBase4(0.0, 0.0, 0.0, 0), VBase4(0.34, 0.32, 0.25, 1)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0.42, 0.42, 0.38, 1)), VBase4(0.21, 0.2, 0.2, 1), VBase4(0.34, 0.32, 0.25, 1)],TODGlobals.SKY_OVERCASTNIGHT: [(self.texTransparent, '', VBase4(0, 0, 0, 0), VBase4(0.12, 0.22, 0.25, 1)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0, 0.0, 0.0, 0)), VBase4(0.12, 0.21, 0.25, 1), VBase4(0.12, 0.21, 0.25, 1)]}
        self.tsSides = []
        self.tsSides.append(self._setupTexStageA('tsSidesA'))
        self.tsSides.append(self._setupTexStageB('tsSidesB'))
        self.tsSides.append(self._setupTexStageC('tsSidesC'))
        self.tsSides.append(self._setupTexStageD('tsSidesD'))
        self.sides.setTexture(self.tsSides[3], self.texTransparent)
        self.tsTop = []
        self.tsTop.append(self._setupTexStageA('tsTopA'))
        self.tsTop.append(self._setupTexStageB('tsTopB'))
        self.tsTop.append(self._setupTexStageD('tsTopD'))
        self.top.setTexture(self.tsSides[3], self.texTransparent)
        self.clouds.setTexture(self.tsSides[3], self.texTransparent)
        self.cloudIval = None
        self.setCloudLevel(TODGlobals.LIGHTCLOUDS)
        self.sunTrack = self.relativeCompass.attachNewNode('sunTrack')
        self.sunTrack.setHpr(0, 0, 0)
        self.sunWheelHeading = self.sunTrack.attachNewNode('sunWheelHeading')
        self.sunWheelPitch = self.sunWheelHeading.attachNewNode('sunWheelPitch')
        self.sunWheelRoll = self.sunWheelPitch.attachNewNode('sunWheelRoll')
        self.sunLight = self.sunWheelRoll.attachNewNode('sunLight')
        self.sunLight.setPosHpr(self.sunDepth, 0, 0, 90, 0, 0)
        dl = DirectionalLight('directionalLightSun')
        self.dirLightSun = self.sunLight.attachNewNode(dl)
        self.shadowSunLight = self.sunWheelRoll.attachNewNode('shadowLight')
        self.shadowSunLight.setPosHpr(-self.sunDepth, 0, 0, -90, 0, 0)
        ds = DirectionalLight('directionalLightShadowSun')
        self.dirLightShadowSun = self.shadowSunLight.attachNewNode(ds)
        al = AmbientLight('grassLight')
        al.setColor(VBase4(1, 1, 1, 1))
        self.grassLight = self.sunLight.attachNewNode(al)
        al = AmbientLight('ambientLight')
        al.setColor(VBase4(1, 1, 1, 1))
        self.ambLight = self.sunLight.attachNewNode(al)
        self.sunModel = loader.loadModel('models/sky/sun')
        if base.config.GetBool('prepare-scene', 1):
            if base.win.getGsg():
                self.sunModel.prepareScene(base.win.getGsg())
        self.sunModel.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.sunModel.setBillboardPointEye()
        self.sunModel.setBin('background', 120)
        self.sunModel.setScale(2700)
        self.sunModel.reparentTo(self.sunLight)
        self.moonBaseScale = 350.0
        self.moonModel = loader.loadModel('models/sky/moon')
        self.moonModel.setBillboardAxis(0)
        self.moonModel.setBin('background', 110)
        self.moonModel.setScale(self.moonBaseScale)
        self.moonModel.reparentTo(self.dirLightShadowSun)
        self.moonGlow = loader.loadModel('models/sky/sun')
        self.moonGlow.reparentTo(self.moonModel)
        self.moonGlow.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.moonGlow.setBin('background', 109, 1)
        self.moonGlow.setPos(0, 0, -0.2)
        self.moonGlow.setColorScale(0.7, 0.8, 1, 1)
        self.moonGlow.setScale(5)
        self.moonGlow.findTexture('Sun').setQualityLevel(Texture.QLBest)
        self.moonModel.findTexture('Moon').setQualityLevel(Texture.QLBest)
        self.texGradient.setQualityLevel(Texture.QLBest)
        self.tsMoon = self._setupTexStageAlpha('tsMoon')
        self.texGradient.setWrapU(Texture.WMClamp)
        self.texGradient.setWrapV(Texture.WMClamp)
        self.moonModel.setTexture(self.tsMoon, self.texGradient)
        self.moonAlphaNode = NodePath('MoonAlphaNode')
        self.moonModel.setTexProjector(self.tsMoon, self.moonAlphaNode, NodePath())
        self.setMoonState(1.0)
        self.moonOverlay = loader.loadModel('models/effects/effectCards').find('**/effectJolly')
        self.moonOverlay.setBin('background', 111)
        self.moonOverlay.reparentTo(self.moonModel)
        self.moonOverlay.setBillboardPointEye(0.0)
        self.moonOverlay.setScale(0.9)
        self.moonOverlay.setColorScale(1, 1, 1, 0.25)
        self.moonOverlay.stash()
        self.moonOverlayIval = None
        areg = AttribNodeRegistry.getGlobalPtr()
        areg.addNode(self.ambLight)
        areg.addNode(self.dirLightSun)
        areg.addNode(self.dirLightShadowSun)
        messenger.send('nametagAmbientLightChanged', [self.ambLight])
        self.shadowCaster = None
        self.moonState = 1.0
        self.moonSize = 1.0
        self.moonOverlayAlpha = 0.0
        return None

    def getLight(self, tod):
        return self.dirLightSun

    def getShadowLight(self, tod):
        return self.dirLightShadowSun

    def _clearTexAttrib(self, geomNode):
        attrib = geomNode.node().getGeomState(0).removeAttrib(TextureAttrib.getClassType())
        geomNode.node().setGeomState(0, attrib)

    def _setupTexStageAlpha(self, name):
        ts = TextureStage(name)
        ts.setCombineRgb(TextureStage.CMReplace, TextureStage.CSPrevious, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMModulate, TextureStage.CSPrevious, TextureStage.COSrcAlpha, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        ts.setSort(2)
        return ts

    def _setupTexStageA(self, name):
        ts = TextureStage(name)
        ts.setCombineRgb(TextureStage.CMReplace, TextureStage.CSTexture, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        ts.setSort(1)
        return ts

    def _setupTexStageB(self, name):
        ts = TextureStage(name)
        ts.setColor(Vec4(0, 0, 0, 0))
        ts.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSConstant, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcAlpha, TextureStage.CSPrevious, TextureStage.COSrcAlpha, TextureStage.CSConstant, TextureStage.COSrcAlpha)
        ts.setSort(2)
        return ts

    def _setupTexStageC(self, name):
        ts = TextureStage(name)
        ts.setColor(Vec4(0, 0, 0, 0))
        ts.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSConstant, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcAlpha, TextureStage.CSPrevious, TextureStage.COSrcAlpha, TextureStage.CSConstant, TextureStage.COSrcAlpha)
        ts.setSort(3)
        return ts

    def _setupTexStageD(self, name):
        ts = TextureStage(name)
        ts.setCombineRgb(TextureStage.CMModulate, TextureStage.CSPrimaryColor, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMModulate, TextureStage.CSPrimaryColor, TextureStage.COSrcAlpha, TextureStage.CSPrevious, TextureStage.COSrcAlpha)
        ts.setSort(4)
        return ts

    def setStageColor(self, t, ts, startColor, endColor):
        ts.setColor(startColor * (1.0 - t) + endColor * t)

    def setMoonOverlayAlpha(self, alpha):
        self.moonOverlayAlpha = alpha
        if self.moonOverlayAlpha > 0.01:
            self.moonOverlay.unstash()
        else:
            self.moonOverlay.stash()
        self.moonOverlay.setColorScale(1, 1, 1, self.moonOverlayAlpha)

    def setMoonSize(self, size):
        self.moonSize = size
        self.moonModel.setScale(self.moonSize * self.moonBaseScale)

    def setMoonState(self, state):
        if state <= 0.0:
            state = 0.0
        self.moonState = state
        pos = 0.1 - state * 0.8
        self.moonAlphaNode.setPos(0, pos, 0)

    def transitionMoon(self, fromState, toState, duration=10.0):
        return LerpFunctionInterval(self.setMoonState, duration, fromData=fromState, toData=toState)

    def stashSun(self):
        self.sunWheelHeading.stash()

    def unstashSun(self):
        self.sunWheelHeading.unstash()
        self.sunTrack.setColorScale(1, 1, 1, 1)

    def applySunAngle(self):
        if self.shadowCaster and self.shadowCaster.shadowsEnabled:
            shadowDarkness = self.computeShadowDarkness()
            self.shadowCaster.updateShadowAmount(shadowDarkness)

    def getCurrentSunAngle(self):
        sunVecCurrent = Vec3(self.sunWheelHeading.getH(), self.sunWheelPitch.getP(), self.sunWheelRoll.getR())
        return sunVecCurrent

    def transitionSunAngle(self, newHpr, duration=10.0, fade=0, sunDirLast=None):
        if sunDirLast != None:
            sunVecCurrent = sunDirLast
        else:
            sunVecCurrent = Vec3(self.sunWheelHeading.getH(), self.sunWheelPitch.getP(), self.sunWheelRoll.getR())
        aH = PythonUtil.fitSrcAngle2Dest(self.sunWheelHeading.getH(), newHpr[0])
        aP = PythonUtil.fitSrcAngle2Dest(self.sunWheelPitch.getP(), newHpr[1])
        aR = PythonUtil.fitSrcAngle2Dest(self.sunWheelRoll.getR(), newHpr[2])
        self.sunWheelHeading.setH(aH)
        self.sunWheelPitch.setP(aP)
        self.sunWheelRoll.setR(aR)
        sunVecFitted = Vec3(aH, aP, aR)
        if fade:
            ival = Sequence(LerpColorScaleInterval(self.sunTrack, duration * 0.3, Vec4(1, 1, 1, 0)), LerpFunctionInterval(self.setSunTrueAngle, duration * 0.4, fromData=sunVecFitted, toData=newHpr), LerpColorScaleInterval(self.sunTrack, duration * 0.3, Vec4(1, 1, 1, 1)))
            return ival
        else:
            return LerpFunctionInterval(self.setSunTrueAngle, duration, fromData=sunVecFitted, toData=newHpr)
        return

    def computeShadowDarkness(self):
        lightHeight = self.sunLight.getZ(render)
        if lightHeight > 0:
            minHeight = 1500
            maxDarkness = 0.5
        else:
            minHeight = 3000
            maxDarkness = 0.4
        lightHeight = abs(lightHeight)
        maxHeight = self.lightDepth
        heightDif = maxHeight - (lightHeight - minHeight)
        if heightDif > maxHeight - minHeight:
            heightDif = maxHeight - minHeight
        heightProp = heightDif / (maxHeight - minHeight)
        iHeightProp = pow(max(1 - heightProp, 0), 0.5)
        iHeightPropMod = iHeightProp * maxDarkness
        iiHeightProp = 1 - iHeightPropMod
        return iiHeightProp

    def setSunLock(self, lock):
        self.lockSunPos = lock

    def setRelativeCompassH(self, h):
        self.relativeCompass.setH(h)

    def getSunTrueAngle(self):
        h = self.sunWheelHeading.getH()
        p = self.sunWheelPitch.getP()
        r = self.sunWheelRoll.getR()
        sunVec = self.boundSunAngle(Vec3(h, p, r))
        return sunVec

    def boundSunAngle(self, direction):
        newDir = Vec3(direction[0], direction[1], direction[2])
        for index in range(3):
            while newDir[index] > 360.0:
                newDir[index] -= 360.0

            while newDir[index] < 0.0:
                newDir[index] += 360.0

        return newDir

    def setSunTrueAngle(self, newHpr):
        if self.lockSunPos:
            return
        self.sunWheelHeading.setH(newHpr[0])
        self.sunWheelPitch.setP(newHpr[1])
        self.sunWheelRoll.setR(newHpr[2])
        if self.shadowCaster:
            shadowDarkness = self.computeShadowDarkness()
            self.shadowCaster.updateShadowAmount(shadowDarkness)
        sunHeight = self.sunLight.getZ(render)
        if sunHeight < -6000.0:
            self.sunModel.stash()
        else:
            self.sunModel.unstash()
        moonAppearHeight = 3000.0
        moonFadeHeight = 7000.0
        if -sunHeight < moonAppearHeight:
            self.moonModel.stash()
        elif -sunHeight < moonFadeHeight:
            fadeAmount = (-sunHeight - moonAppearHeight) / (moonFadeHeight - moonAppearHeight)
            self.moonModel.unstash()
            self.moonModel.setColorScale(1.0, 1.0, 1.0, fadeAmount)
        else:
            self.moonModel.setColorScale(1.0, 1.0, 1.0, 1.0)
            self.moonModel.unstash()

    def setupCloudIval(self):
        ival = Parallel(name='CloudIval')
        cloudNodeA = NodePath('CloudNodeA')
        anim = LerpPosInterval(cloudNodeA, startPos=VBase3(0.0, 0.0, 0.0), pos=VBase3(2.0, 1.0, 0.0), duration=400.0)
        ival.append(anim)
        cloudNodeB = NodePath('CloudNodeB')
        anim = LerpPosInterval(cloudNodeB, startPos=VBase3(0.0, 0.0, 0.0), pos=VBase3(-2.0, 0.0, 0.0), duration=400.0)
        ival.append(anim)
        self.clouds.setTexProjector(self.tsSides[0], cloudNodeA, NodePath())
        self.sides.setTexProjector(self.tsSides[0], cloudNodeB, NodePath())
        return ival

    def startCloudIval(self):
        if not self.cloudIval:
            self.cloudIval = self.setupCloudIval()
        self.cloudIval.loop()

    def stopCloudIval(self):
        if self.cloudIval:
            self.cloudIval.pause()
            self.cloudIval = None
        return

    def setCloudLevel(self, level):
        self.startCloudIval()
        cloudTex = self.cloudSettings.get(level)[0]
        uvSetName = self.cloudSettings.get(level)[1]
        self.sides.setTexture(self.tsSides[0], cloudTex)
        self.clouds.setTexture(self.tsSides[0], cloudTex)
        self.tsSides[0].setTexcoordName(uvSetName)
        self.tsSides[1].setColor(Vec4(0, 0, 0, 0))

    def transitionClouds(self, level, duration=5.0):
        self.stopCloudIval()
        cloudTex = self.cloudSettings.get(level)[0]
        uvSetName = self.cloudSettings.get(level)[1]
        self.sides.setTexture(self.tsSides[1], cloudTex)
        self.clouds.setTexture(self.tsSides[1], cloudTex)
        self.tsSides[1].setTexcoordName(uvSetName)
        ival = Sequence(LerpFunctionInterval(self.setStageColor, duration, fromData=0.0, toData=1.0, extraArgs=[self.tsSides[1], Vec4(0, 0, 0, 0), Vec4(1, 1, 1, 1)]), Func(self.setCloudLevel, level))
        return ival

    def setSky(self, skyType):
        settings = self.skySettings.get(skyType)
        if skyType == TODGlobals.SKY_OFF:
            self.stash()
        else:
            self.unstash()
        if settings:
            self.sides.setTexture(self.tsSides[2], settings[0][0])
            self.tsSides[2].setTexcoordName(settings[0][1])
            self.tsSides[1].setColor(Vec4(0, 0, 0, 0))
            self.tsSides[2].setColor(settings[0][2])
            self.sides.setColorScale(settings[0][3])
            self.top.setTexture(self.tsTop[0], settings[1][0])
            self.tsTop[0].setTexcoordName(settings[1][1])
            self.tsTop[1].setColor(Vec4(0, 0, 0, 0))
            self.top.setColorScale(settings[1][3])
            self.clouds.setColorScale(settings[2])
            self.horizon.setColorScale(settings[3])
        self.setLastSky(skyType)

    def setLastSky(self, skyType):
        self.lastSky = skyType

    def transitionSky(self, skyTypeA, skyTypeB, duration=10.0):
        self.setSky(skyTypeA)
        settingsA = self.skySettings.get(skyTypeA)
        settingsB = self.skySettings.get(skyTypeB)
        self.sides.setTexture(self.tsSides[1], settingsB[0][0])
        self.tsSides[1].setTexcoordName(settingsB[0][1])
        self.top.setTexture(self.tsTop[1], settingsB[1][0])
        self.tsTop[1].setTexcoordName(settingsB[1][1])
        ival = Sequence(Parallel(LerpFunctionInterval(self.setStageColor, duration, fromData=0.0, toData=1.0, extraArgs=[self.tsSides[2], settingsA[0][2], Vec4(0, 0, 0, 0)]), LerpFunctionInterval(self.setStageColor, duration, fromData=0.0, toData=1.0, extraArgs=[self.tsSides[1], Vec4(0, 0, 0, 0), settingsB[0][2]]), LerpFunctionInterval(self.setStageColor, duration, fromData=0.0, toData=1.0, extraArgs=[self.tsTop[1], Vec4(0, 0, 0, 0), Vec4(1, 1, 1, 1)]), LerpColorScaleInterval(self.sides, duration, settingsB[0][3]), LerpColorScaleInterval(self.top, duration, settingsB[1][3]), LerpColorScaleInterval(self.clouds, duration, settingsB[2]), LerpColorScaleInterval(self.horizon, duration, settingsB[3])), Func(self.setLastSky, skyTypeB))
        return ival

    def transitionSkyFromCurrent(self, skyTypeB, duration=10.0):
        settingsB = self.skySettings.get(skyTypeB)
        self.sides.setTexture(self.tsSides[1], settingsB[0][0])
        self.tsSides[1].setTexcoordName(settingsB[0][1])
        self.top.setTexture(self.tsTop[1], settingsB[1][0])
        self.tsTop[1].setTexcoordName(settingsB[1][1])
        tsStartColor = self.tsSides[2].getColor()
        ival = Parallel(LerpFunctionInterval(self.setStageColor, duration, fromData=0.0, toData=1.0, extraArgs=[self.tsSides[2], tsStartColor, Vec4(0, 0, 0, 0)]), LerpFunctionInterval(self.setStageColor, duration, fromData=0.0, toData=1.0, extraArgs=[self.tsSides[1], Vec4(0, 0, 0, 0), settingsB[0][2]]), LerpFunctionInterval(self.setStageColor, duration, fromData=0.0, toData=1.0, extraArgs=[self.tsTop[1], Vec4(0, 0, 0, 0), Vec4(1, 1, 1, 1)]), LerpColorScaleInterval(self.sides, duration, settingsB[0][3]), LerpColorScaleInterval(self.top, duration, settingsB[1][3]), LerpColorScaleInterval(self.clouds, duration, settingsB[2]), LerpColorScaleInterval(self.horizon, duration, settingsB[3]))
        return ival