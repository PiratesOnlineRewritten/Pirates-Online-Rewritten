from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.task import Task
from direct.showbase import ShadowPlacer
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.fsm import FSM
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import quickProfile
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.pirate import Biped, HumanBase
from pirates.pirate import HumanDNA
from pirates.makeapirate import PirateMale
from pirates.makeapirate import PirateFemale
from pirates.pirate.HumanAnimationMixer import HumanAnimationMixer
from pirates.pirate import BodyDefs
import random
import cPickle
TX = 0
TY = 1
TZ = 2
RX = 3
RY = 4
RZ = 5
SX = 6
SY = 7
SZ = 8
AnimDict = {}
AnimListDict = {'sf': Biped.DefaultAnimList,'ms': Biped.DefaultAnimList,'mi': Biped.DefaultAnimList,'tp': Biped.DefaultAnimList,'tm': Biped.DefaultAnimList}
CustomAnimDict = {'msf': Biped.msfCustomAnimList,'mms': Biped.mmsCustomAnimList,'mmi': Biped.mmiCustomAnimList,'mtp': Biped.mtpCustomAnimList,'mtm': Biped.mtmCustomAnimList,'fsf': Biped.fsfCustomAnimList,'fms': Biped.fmsCustomAnimList,'fmi': Biped.fmiCustomAnimList,'ftp': Biped.ftpCustomAnimList,'ftm': Biped.ftmCustomAnimList}
CastAnimDict = {'models/char/js': Biped.jsCustomAnimList,'models/char/wt': Biped.wtCustomAnimList,'models/char/es': Biped.esCustomAnimList,'models/char/td': Biped.tdCustomAnimList,'models/char/cb': Biped.cbCustomAnimList,'models/char/jg': Biped.jgCustomAnimList,'models/char/jr': Biped.jrCustomAnimList,'models/char/plf': Biped.plfCustomAnimList,'models/char/pls': Biped.plsCustomAnimList}
NewModelDict = {'sf': 'sf','ms': 'ms','mi': 'mi','tp': 'tp','tm': 'tm'}
PrebuiltAnimDict = {}
HeadPositions = BodyDefs.HeadPositions
HeadScales = BodyDefs.HeadScales
BodyScales = BodyDefs.BodyScales
PlayerNames = [
 "Cap'n Bruno Cannonballs", 'Bad-run Thomas', 'Carlos Saggingsails', 'Smugglin Willy Hawkins']

class Human(HumanBase.HumanBase, Biped.Biped):
    notify = DirectNotifyGlobal.directNotify.newCategory('Human')
    prebuiltAnimData = {}

    def __init__(self, other=None):
        Biped.Biped.__init__(self, other, HumanAnimationMixer)
        self.zombie = False
        self.crazyColorSkin = False
        self.crazyColorSkinIndex = 0
        self.flattenPending = None
        self.flattenSuperLowName = None
        self.optimizeLOD = base.config.GetBool('optimize-avatar-lod', 1)
        self.loaded = 0
        self.playingRate = None
        self.shadowFileName = 'models/misc/drop_shadow'
        self.setFont(PiratesGlobals.getInterfaceFont())
        self.__blinkName = 'blink-' + str(self.this)
        self.eyeLids = None
        self.eyeBalls = None
        self.eyeIris = None
        self.reducedAnimList = None
        self.headNode = None
        self.headEffects = NodePath('headEffects')
        self.extraNode = None
        self.scaleNode = None
        self.rootNode = None
        self.floorOffsetZ = 0.0
        self.isGhost = 0
        self.headFudgeHpr = Vec3(0, 0, 0)
        self.randGen = random.Random()
        self.randGen.seed(random.random())
        self.eyeFSM = ClassicFSM('eyeFSM', [
         State('off', self.enterEyeFSMOff, self.exitEyeFSMOff, [
          'open', 'closed']),
         State('open', self.enterEyeFSMOpen, self.exitEyeFSMOpen, [
          'closed', 'off']),
         State('closed', self.enterEyeFSMClosed, self.exitEyeFSMClosed, [
          'open', 'off'])], 'off', 'off')
        self.eyeFSM.enterInitialState()
        if other != None:
            self.copyHuman(other)
        return

    def removeCopiedNodes(self):
        self.dropShadow = self.find('**/drop_shadow*')
        if not self.dropShadow.isEmpty():
            self.deleteDropShadow()
        else:
            self.dropShadow = None
        billboardNode = self.find('**/billboardNode')
        if not billboardNode.isEmpty():
            billboardNode.removeNode()
        self.getGeomNode().getParent().removeNode()
        return

    def flattenHuman(self):
        self.getWeaponJoints()

    def flattenSuperLow(self):
        name = 'flattenSuperLow-%s' % self.this
        self.flattenSuperLowName = name
        model = self.getLOD('500')
        self.accept(name, self.__doneFlattenSuperLow)
        taskMgr.remove(name)
        taskMgr.add(self.flattenSuperLowTask, name, extraArgs=[model], taskChain='background')

    def flattenSuperLowTask(self, model):
        model = model.copyTo(NodePath())
        rhn = model.find('**/rightHand')
        lhn = model.find('**/leftHand')
        if lhn:
            lhn.detachNode()
        if rhn:
            rhn.detachNode()
        node = model.node()
        gr = SceneGraphReducer()
        model.node().setAttrib(TransparencyAttrib.make(0), 2000)
        gr.applyAttribs(node, SceneGraphReducer.TTApplyTextureColor | SceneGraphReducer.TTTexMatrix | SceneGraphReducer.TTOther | SceneGraphReducer.TTCullFace | SceneGraphReducer.TTTransform | SceneGraphReducer.TTColor | SceneGraphReducer.TTColorScale)
        num_removed = gr.flatten(node, -1)
        gr.makeCompatibleState(node)
        gr.collectVertexData(node, ~(SceneGraphReducer.CVDFormat | SceneGraphReducer.CVDName | SceneGraphReducer.CVDAnimationType))
        gr.unify(node, 0)
        name = self.flattenSuperLowName
        if name:
            messenger.send(name, [model], taskChain='default')

    def __doneFlattenSuperLow(self, flat):
        self.headNode = flat.find('**/def_head01')
        self.rootNode = flat.find('**/dx_root')
        self.getWeaponJoints()
        orig = self.getLOD('500')
        orig.getChildren().detach()
        self.loadModel(flat, lodName='500', copy=False, autoBindAnims=False)
        self.getWeaponJoints()
        if hasattr(self, 'animProp') and self.animProp:
            self.resetAnimProp()
        self.findAllMatches('**/def_head01').detach()
        self.findAllMatches('**/dx_root').detach()
        for lodName in self.getLODNames():
            if lodName == '500':
                self.headNode.reparentTo(self.getLOD(lodName).find('**/+Character'))
                self.rootNode.reparentTo(self.getLOD(lodName).find('**/+Character'))
            else:
                self.headNode.instanceTo(self.getLOD(lodName).find('**/+Character'))
                self.rootNode.instanceTo(self.getLOD(lodName).find('**/+Character'))

        self.headEffects.reparentTo(self.headNode)

    def __doneFlattenHuman(self, models):
        self.flattenPending = None
        self.getWeaponJoints()
        return

    def copyHuman(self, other):
        self.gender = other.gender
        self.loaded = other.loaded
        self.loadAnimatedHead = other.loadAnimatedHead
        self.rootScale = other.rootScale

    def delete(self):
        try:
            self.Human_deleted
        except:
            self.Human_deleted = 1
            taskMgr.remove(self.__blinkName)
            name = self.flattenSuperLowName
            if name:
                self.flattenSuperLowName = None
                self.ignore(name)
                taskMgr.remove(name)
            if self.dropShadow and not self.dropShadow.isEmpty():
                self.deleteDropShadow()
            del self.eyeFSM
            self.controlShapes = None
            self.sliderNames = None
            Biped.Biped.delete(self)

        return

    def isDeleted(self):
        try:
            self.Human_deleted
            if self.Human_deleted == 1:
                return True
        except:
            return False

    def fixEyes(self):
        self.eyeLids = {}
        self.eyeBalls = {}
        self.eyeIris = {}
        for lodName in self.getLODNames():
            geom = self.getPart('head', lodName)
            self.eyeLids[lodName] = geom.findAllMatches('**/*eyelid*')
            self.eyeBalls[lodName] = geom.findAllMatches('**/eye_ball*')
            self.eyeIris[lodName] = geom.findAllMatches('**/eye_iris*')
            self.eyeLids[lodName].stash()
            self.eyeBalls[lodName].unstash()
            self.eyeIris[lodName].unstash()

    def makeAnimDict(self, gender, animNames):
        self.animTable = []
        for currAnim in animNames:
            anim = animNames.get(currAnim)
            for currAnimName in anim:
                self.animTable.append([currAnimName, currAnimName])

        self.reducedAnimList = self.animTable

    def forceLoadAnimDict(self):
        for anim in self.animDict.keys():
            self.getAnimControls(anim)

    def createAnimDict(self, customList=None):
        filePrefix = 'models/char/m'
        genderPrefix = 'm'
        if self.style.gender == 'f':
            self.type = BodyDefs.femaleFrames[self.style.getBodyShape()]
            filePrefix = 'models/char/f'
            genderPrefix = 'f'
        else:
            self.type = BodyDefs.maleFrames[self.style.getBodyShape()]
        if self.reducedAnimList is None:
            self.animDict = self.prebuiltAnimData[genderPrefix + self.type]
            return
        filePrefix += 'p'
        animList = self.reducedAnimList
        self.animDict = {}
        for anim in animList:
            animSuffix = ''
            for i in range(0, len(CustomAnimDict[genderPrefix + self.type])):
                if anim[0] == CustomAnimDict[genderPrefix + self.type][i]:
                    animSuffix = '_' + genderPrefix + NewModelDict.get(self.type)
                    break

            self.animDict[anim[0]] = filePrefix + '_' + anim[1] + animSuffix

        return filePrefix

    def getIsPaid(self):
        return True

    def setupGhostNodes(self):
        lod = NodePath(self.getLODNode())
        for node in lod.getChildren():
            eyes = node.findAllMatches('**/eye*')
            if eyes:
                eyes.wrtReparentTo(eyes[0].getParent().attachNewNode(ModelNode('eyes')))

    def loadHuman(self, other):
        other.style = self.style
        other.gender = self.style.gender
        other.model.dna = self.style
        self.createAnimDict()
        if self.style.gender == 'f':
            self.headFudgeHpr = Vec3(0, 0, 0)
            idx = 1
        else:
            self.headFudgeHpr = Vec3(0, 0, 0)
            idx = 0
        other.zombie = self.zombie
        other.crazyColorSkin = self.crazyColorSkin
        other.setCrazyColorSkinIndex(self.getCrazyColorSkinIndex())
        yieldThread('anim dict')
        other.isPaid = self.getIsPaid()
        other.showLOD(2000)
        yieldThread('showLOD')
        base.loadingScreen.tick()
        if other.zombie:
            other.showZombie()
        if hasattr(self, 'motionFSM'):
            self.motionFSM.setAvatar(self)
        base.loadingScreen.tick()
        yieldThread('zombie')
        other.applyBodyShaper()
        base.loadingScreen.tick()
        yieldThread('body shaper')
        base.loadingScreen.tick()
        other.applyHeadShaper()
        yieldThread('head shaper')
        base.loadingScreen.tick()
        if self.zombie == 2:
            other.model.eyeBalls.unstash()
            other.model.irises.stash()
        else:
            if self.zombie:
                other.model.eyeBalls.stash()
                other.model.irises.stash()
            else:
                other.model.eyeBalls.unstash()
                other.model.irises.unstash()
            base.loadingScreen.tick()
            self.copyActor(other)
            base.loadingScreen.tick()
            self.floorOffsetZ = other.rootNode.getZ()
            yieldThread('copyActor')
            self.copyHuman(other)
            if self.isGhost:
                self.setupGhostNodes()
            gnodes = self.getLOD('500').findAllMatches('**/+GeomNode')
            for node in gnodes:
                node.setTextureOff(other.model.tattooStage)

            base.loadingScreen.tick()
            self.flattenSuperLow()
            self.rootNode = self.getLOD('500').find('**/dx_root')
            self.headNode = self.getLOD('500').find('**/def_head01')
            lodNames = self.getLODNames()
            self.scaleNode = self.controlJoint(None, 'legs', 'def_scale_jt', lodNames[0])
            if len(lodNames) > 1:
                for i in range(1, len(lodNames)):
                    self.controlJoint(self.scaleNode, 'legs', 'def_scale_jt', lodNames[i])

        self.setGlobalScale(self.calcBodyScale())
        yieldThread('copyHuman')
        base.loadingScreen.tick()
        self.loadAnimsOnAllLODs(self.animDict, 'modelRoot')
        base.loadingScreen.tick()
        yieldThread('loadAnims')
        other.zombie = 0
        other.crazyColorSkin = 0
        other.setCrazyColorSkinIndex(0)
        other.showNormal()
        yieldThread('show normal')
        self.initializeNametag3d()
        self.initializeDropShadow()
        self.setName(self.getName())
        yieldThread('misc nodes')
        base.loadingScreen.tick()
        self.loaded = 1
        return

    def setGlobalScale(self, scale):
        self.scaleNode.setScale(scale)
        self.rootScale = scale
        self.scaleNode.setZ(-(self.floorOffsetZ * (1 - scale)))

    def initializeMiscNodes(self):
        self.initializeNametag3d()
        self.initializeDropShadow()

    def undoControlJoints(self):
        self.getGeomNode().getParent().findAllMatches('def_*').detach()
        self.getGeomNode().getParent().findAllMatches('trs_*').detach()
        self.findAllMatches('def_*').detach()
        self.findAllMatches('trs_*').detach()

    def cleanupHuman(self, gender='m'):
        self.eyeFSM.request('off')
        self.undoControlJoints()
        self.removeCopiedNodes()
        self.eyeLids = {}
        self.eyeBalls = {}
        self.eyeIris = {}
        self.flush()
        self.loaded = 0
        self.master = 0

    def getCrazyColorSkinIndex(self):
        return self.crazyColorSkinIndex

    def setCrazyColorSkinIndex(self, index):
        if len(HumanDNA.crazySkinColors) > index:
            self.crazyColorSkinIndex = index
        else:
            self.notify.warning('(Human)index: %d is out of bounds for crazyColorSkin: %d' % (index, len(HumanDNA.crazySkinColors)))

    def generateHuman(self, gender, others, useFaceTex=False):
        parent = self.getParent()
        self.detachNode()
        if gender == 'f':
            other = others[1]
        else:
            other = others[0]
        if self.loaded:
            self.cleanupHuman()
        other.useFaceTex = useFaceTex
        self.loadHuman(other)
        if self.isLocal():
            self.renderReflection = True
        self.setRenderReflection()
        self.resetEffectParent()
        self.enableMixing()
        self.reparentTo(parent)

    def getShadowJoint(self):
        return self.nametagNodePath

    def getNametagJoints(self):
        joints = []
        for lodName in self.getLODNames():
            bundle = self.getPartBundle('modelRoot', lodName)
            joint = bundle.findChild('name_tag')
            if joint:
                joints.append(joint)

        return joints

    def __blinkOpenEyes(self, task):
        if self.eyeFSM.getCurrentState().getName() == 'closed':
            self.eyeFSM.request('open')
        r = self.randGen.random()
        if r < 0.1:
            t = 0.2
        else:
            t = r * 4.0 + 1.0
        taskMgr.doMethodLater(t, self.__blinkCloseEyes, self.__blinkName)
        return Task.done

    def __blinkCloseEyes(self, task):
        if self.eyeFSM.getCurrentState().getName() != 'open':
            taskMgr.doMethodLater(4.0, self.__blinkCloseEyes, self.__blinkName)
        else:
            self.eyeFSM.request('closed')
            taskMgr.doMethodLater(0.125, self.__blinkOpenEyes, self.__blinkName)
        return Task.done

    def startBlink(self):
        taskMgr.remove(self.__blinkName)
        if self.eyeLids:
            self.openEyes()
        taskMgr.doMethodLater(self.randGen.random() * 4.0 + 1, self.__blinkCloseEyes, self.__blinkName)

    def stopBlink(self):
        taskMgr.remove(self.__blinkName)
        if self.eyeLids:
            self.eyeFSM.request('open')

    def closeEyes(self):
        self.eyeFSM.request('closed')

    def openEyes(self):
        self.eyeFSM.request('open')

    def enterEyeFSMOff(self):
        pass

    def exitEyeFSMOff(self):
        pass

    def enterEyeFSMOpen(self):
        for lodName in self.getLODNames():
            self.eyeLids[lodName].hide()
            self.eyeBalls[lodName].show()
            self.eyeIris[lodName].show()

    def exitEyeFSMOpen(self):
        pass

    def enterEyeFSMClosed(self):
        return
        for lodName in self.getLODNames():
            self.eyeLids[lodName].show()
            self.eyeBalls[lodName].hide()
            self.eyeIris[lodName].hide()

    def exitEyeFSMClosed(self):
        pass

    def getGlobalScale(self):
        return self.rootScale

    def calcBodyScale(self):
        idx = 0
        if self.gender == 'f':
            idx = 1
        mappedValue = (0.8 + (1 + self.style.getBodyHeight()) * 0.2) * BodyScales[idx][self.style.getBodyShape()]
        return mappedValue

    @classmethod
    def setupAnimDicts(cls):
        for t in BodyDefs.maleFrames:
            cls.storeAnimDict('models/char/mp', 'm', t)

        for t in BodyDefs.femaleFrames:
            cls.storeAnimDict('models/char/fp', 'f', t)

    @classmethod
    def storeAnimDict(cls, prefix, gender, type):
        qualifier = gender + type
        animList = AnimListDict[type]
        cls.prebuiltAnimData[qualifier] = {}
        for anim in animList:
            if anim[0] == 'intro':
                continue
            animSuffix = ''
            for i in range(0, len(CustomAnimDict[qualifier])):
                if anim[0] == CustomAnimDict[qualifier][i]:
                    animSuffix = '_' + gender + NewModelDict.get(type)
                    break

            cls.prebuiltAnimData[qualifier][anim[0]] = prefix + '_' + anim[1] + animSuffix


Human.setupAnimDicts()