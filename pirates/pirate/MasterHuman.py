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
NewModelDict = {'sf': 'sf','ms': 'ms','mi': 'mi','tp': 'tp','tm': 'tm'}
PrebuiltAnimDict = {}
HeadPositions = BodyDefs.HeadPositions
HeadScales = BodyDefs.HeadScales
BodyScales = BodyDefs.BodyScales
PlayerHeight = [
 5, 6, 6, 6, 7]
MaleBodyShapeControlJoints = (
 'def_spine02', 'def_spine03', 'def_spine04', 'def_shoulders', 'def_neck', 'def_left_clav', 'def_left_shoulder', 'def_left_elbow', 'def_left_wrist', 'def_left_thumb01', 'def_left_thumb02', 'def_left_thumb03', 'def_left_finger01', 'def_left_finger02', 'def_left_index01', 'def_left_index02', 'def_right_clav', 'def_right_shoulder', 'def_right_elbow', 'def_right_wrist', 'def_right_thumb01', 'def_right_thumb02', 'def_right_thumb03', 'def_right_finger01', 'def_right_finger02', 'def_right_index01', 'def_right_index02', 'tr_left_clav', 'tr_left_thumb01', 'tr_right_clav', 'tr_right_thumb01', 'def_hips', 'def_left_thigh', 'def_left_knee', 'def_left_ankle', 'def_left_ball', 'def_right_thigh', 'def_right_knee', 'def_right_ankle', 'def_right_ball', 'tr_sash01', 'tr_left_thigh', 'tr_right_thigh')
MaleBodyShapeTranslateJoints = (
 'tr_left_clav', 'tr_left_thumb01', 'tr_right_clav', 'tr_right_thumb01', 'tr_sash01', 'tr_left_thigh', 'tr_right_thigh')
MaleBodyShapeScaleJoints = (
 'def_spine02', 'def_spine03', 'def_spine04', 'def_shoulders', 'def_neck', 'def_left_clav', 'def_left_shoulder', 'def_left_elbow', 'def_left_wrist', 'def_left_thumb01', 'def_left_thumb02', 'def_left_thumb03', 'def_left_finger01', 'def_left_finger02', 'def_left_index01', 'def_left_index02', 'def_right_clav', 'def_right_shoulder', 'def_right_elbow', 'def_right_wrist', 'def_right_thumb01', 'def_right_thumb02', 'def_right_thumb03', 'def_right_finger01', 'def_right_finger02', 'def_right_index01', 'def_right_index02', 'def_hips', 'def_left_thigh', 'def_left_knee', 'def_left_ankle', 'def_left_ball', 'def_right_thigh', 'def_right_knee', 'def_right_ankle', 'def_right_ball')
MaleBodyShapeControlJointMatrix = BodyDefs.MaleBodyShapeControlJointMatrix
FemaleBodyShapeControlJoints = (
 'def_spine02', 'def_spine03', 'def_spine04', 'def_shoulders', 'def_neck', 'def_left_clav', 'def_left_chest', 'def_left_shoulder', 'def_left_elbow', 'def_left_wrist', 'def_left_thumb01', 'def_left_thumb02', 'def_left_thumb03', 'def_left_finger01', 'def_left_finger02', 'def_left_index01', 'def_left_index02', 'def_right_clav', 'def_right_chest', 'def_right_shoulder', 'def_right_elbow', 'def_right_wrist', 'def_right_thumb01', 'def_right_thumb02', 'def_right_thumb03', 'def_right_finger01', 'def_right_finger02', 'def_right_index01', 'def_right_index02', 'tr_left_clav', 'tr_left_chest', 'tr_right_clav', 'tr_right_chest', 'def_hips', 'def_hips_waistline', 'def_hips_waistline_back', 'tr_sash01', 'def_left_thigh', 'def_left_knee', 'def_left_ankle', 'def_left_ball', 'def_right_thigh', 'def_right_knee', 'def_right_ankle', 'def_right_ball', 'tr_left_thigh', 'tr_right_thigh')
FemaleBodyShapeTranslateJoints = (
 'tr_left_clav', 'tr_left_chest', 'tr_right_clav', 'tr_right_chest', 'tr_sash01', 'tr_left_thigh', 'tr_right_thigh')
FemaleBodyShapeScaleJoints = (
 'def_spine02', 'def_spine03', 'def_spine04', 'def_shoulders', 'def_neck', 'def_left_clav', 'def_left_chest', 'def_left_shoulder', 'def_left_elbow', 'def_left_wrist', 'def_left_thumb01', 'def_left_thumb02', 'def_left_thumb03', 'def_left_finger01', 'def_left_finger02', 'def_left_index01', 'def_left_index02', 'def_right_clav', 'def_right_chest', 'def_right_shoulder', 'def_right_elbow', 'def_right_wrist', 'def_right_thumb01', 'def_right_thumb02', 'def_right_thumb03', 'def_right_finger01', 'def_right_finger02', 'def_right_index01', 'def_right_index02', 'def_hips', 'def_hips_waistline', 'def_hips_waistline_back', 'def_left_thigh', 'def_left_knee', 'def_left_ankle', 'def_left_ball', 'def_right_thigh', 'def_right_knee', 'def_right_ankle', 'def_right_ball')
FemaleBodyShapeControlJointMatrix = BodyDefs.FemaleBodyShapeControlJointMatrix
MaleHeadShapeControlJoints = (
 'def_trs_forehead', 'def_trs_left_forehead', 'def_trs_right_forehead', 'def_trs_left_cheek', 'def_trs_right_cheek', 'trs_face_bottom', 'def_trs_mid_jaw', 'def_trs_left_jaw1', 'def_trs_left_jaw2', 'def_trs_right_jaw1', 'def_trs_right_jaw2', 'def_trs_mid_nose_top', 'def_trs_mid_nose_bot', 'def_trs_left_ear', 'def_trs_right_ear', 'trs_left_eyebrow', 'trs_left_eyeball', 'trs_left_eyelid', 'trs_left_eyesocket', 'trs_right_eyebrow', 'trs_right_eyeball', 'trs_right_eyelid', 'trs_right_eyesocket', 'trs_lips_top', 'trs_lips_bot', 'trs_lip_top', 'trs_lip_bot', 'trs_lip_left1', 'trs_lip_left2', 'trs_lip_left3', 'trs_lip_right1', 'trs_lip_right2', 'trs_lip_right3')
MaleHeadShapeControlJointMatrix = {'def_trs_forehead': [],'def_trs_left_forehead': [],'def_trs_right_forehead': [],'def_trs_left_cheek': [],'def_trs_right_cheek': [],'def_trs_mid_jaw': [],'def_trs_left_jaw1': [],'def_trs_left_jaw2': [],'def_trs_right_jaw1': [],'def_trs_right_jaw2': [],'def_trs_mid_nose_top': [],'def_trs_mid_nose_bot': [],'def_trs_left_ear': [],'def_trs_right_ear': [],'trs_face_bottom': [],'trs_left_eyebrow': [],'trs_left_eyeball': [],'trs_left_eyelid': [],'trs_left_eyesocket': [],'trs_right_eyebrow': [],'trs_right_eyeball': [],'trs_right_eyelid': [],'trs_right_eyesocket': [],'trs_lips_top': [],'trs_lips_bot': [],'trs_lip_top': [],'trs_lip_bot': [],'trs_lip_left1': [],'trs_lip_left2': [],'trs_lip_left3': [],'trs_lip_right1': [],'trs_lip_right2': [],'trs_lip_right3': [],'initialized': []}
MaleHeadShapeInitialControlJointMatrix = {'def_trs_forehead': [],'def_trs_left_forehead': [],'def_trs_right_forehead': [],'def_trs_left_cheek': [],'def_trs_right_cheek': [],'def_trs_mid_jaw': [],'def_trs_left_jaw1': [],'def_trs_left_jaw2': [],'def_trs_right_jaw1': [],'def_trs_right_jaw2': [],'def_trs_mid_nose_top': [],'def_trs_mid_nose_bot': [],'def_trs_left_ear': [],'def_trs_right_ear': [],'trs_face_bottom': [],'trs_left_eyebrow': [],'trs_left_eyeball': [],'trs_left_eyelid': [],'trs_left_eyesocket': [],'trs_right_eyebrow': [],'trs_right_eyeball': [],'trs_right_eyelid': [],'trs_right_eyesocket': [],'trs_lips_top': [],'trs_lips_bot': [],'trs_lip_top': [],'trs_lip_bot': [],'trs_lip_left1': [],'trs_lip_left2': [],'trs_lip_left3': [],'trs_lip_right1': [],'trs_lip_right2': [],'trs_lip_right3': [],'initialized': []}
FemaleHeadShapeControlJoints = (
 'def_trs_forehead', 'def_trs_left_forehead', 'def_trs_right_forehead', 'def_trs_left_cheek', 'def_trs_right_cheek', 'trs_face_bottom', 'def_trs_mid_jaw', 'def_trs_left_jaw1', 'def_trs_left_jaw2', 'def_trs_right_jaw1', 'def_trs_right_jaw2', 'def_trs_mid_nose_top', 'def_trs_mid_nose_bot', 'def_trs_left_ear', 'def_trs_right_ear', 'trs_left_eyebrow', 'trs_left_eyeball', 'trs_left_eyelid', 'trs_left_eyesocket', 'trs_right_eyebrow', 'trs_right_eyeball', 'trs_right_eyelid', 'trs_right_eyesocket', 'trs_lips_top', 'trs_lips_bot', 'trs_lip_top', 'trs_lip_bot', 'trs_lip_left1', 'trs_lip_left2', 'trs_lip_left3', 'trs_lip_right1', 'trs_lip_right2', 'trs_lip_right3')
FemaleHeadShapeControlJointMatrix = {'def_trs_forehead': [],'def_trs_left_forehead': [],'def_trs_right_forehead': [],'def_trs_left_cheek': [],'def_trs_right_cheek': [],'def_trs_mid_jaw': [],'def_trs_left_jaw1': [],'def_trs_left_jaw2': [],'def_trs_right_jaw1': [],'def_trs_right_jaw2': [],'def_trs_mid_nose_top': [],'def_trs_mid_nose_bot': [],'def_trs_left_ear': [],'def_trs_right_ear': [],'trs_face_bottom': [],'trs_left_eyebrow': [],'trs_left_eyeball': [],'trs_left_eyelid': [],'trs_left_eyesocket': [],'trs_right_eyebrow': [],'trs_right_eyeball': [],'trs_right_eyelid': [],'trs_right_eyesocket': [],'trs_lips_top': [],'trs_lips_bot': [],'trs_lip_top': [],'trs_lip_bot': [],'trs_lip_left1': [],'trs_lip_left2': [],'trs_lip_left3': [],'trs_lip_right1': [],'trs_lip_right2': [],'trs_lip_right3': [],'initialized': []}
FemaleHeadShapeInitialControlJointMatrix = {'def_trs_forehead': [],'def_trs_left_forehead': [],'def_trs_right_forehead': [],'def_trs_left_cheek': [],'def_trs_right_cheek': [],'def_trs_mid_jaw': [],'def_trs_left_jaw1': [],'def_trs_left_jaw2': [],'def_trs_right_jaw1': [],'def_trs_right_jaw2': [],'def_trs_mid_nose_top': [],'def_trs_mid_nose_bot': [],'def_trs_left_ear': [],'def_trs_right_ear': [],'trs_face_bottom': [],'trs_left_eyebrow': [],'trs_left_eyeball': [],'trs_left_eyelid': [],'trs_left_eyesocket': [],'trs_right_eyebrow': [],'trs_right_eyeball': [],'trs_right_eyelid': [],'trs_right_eyesocket': [],'trs_lips_top': [],'trs_lips_bot': [],'trs_lip_top': [],'trs_lip_bot': [],'trs_lip_left1': [],'trs_lip_left2': [],'trs_lip_left3': [],'trs_lip_right1': [],'trs_lip_right2': [],'trs_lip_right3': [],'initialized': []}
MaleHeadInitHelper = {}
FemaleHeadInitHelper = {}
PlayerNames = [
 "Cap'n Bruno Cannonballs", 'Bad-run Thomas', 'Carlos Saggingsails', 'Smugglin Willy Hawkins']

class MasterHuman(HumanBase.HumanBase, Biped.Biped):
    notify = DirectNotifyGlobal.directNotify.newCategory('Human')
    prebuiltAnimData = {}

    def __init__(self, other=None):
        Biped.Biped.__init__(self, other, HumanAnimationMixer)
        self.model = None
        self.useFaceTex = True
        self.joints = {}
        self.jointTrans = {}
        self.jointTrans2 = {}
        self.zombie = False
        self.crazyColorSkin = False
        self.crazyColorSkinIndex = 0
        self.flattenPending = None
        self.optimizeLOD = base.config.GetBool('optimize-avatar-lod', 1)
        self.master = 0
        self.loaded = 0
        self.playingRate = None
        self.shadowFileName = 'models/misc/drop_shadow'
        self.setFont(PiratesGlobals.getInterfaceFont())
        self.__blinkName = 'blink-' + str(self.this)
        self.eyeLids = None
        self.eyeBalls = None
        self.eyeIris = None
        self.reducedAnimList = None
        self.rootScale = 1.0
        self.headNode = None
        self.extraNode = None
        self.scaleNode = None
        self.rootNode = None
        self.floorOffsetZ = 0.0
        self.headFudgeHpr = Vec3(0, 0, 0)
        self.frozeSomething = True
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
        self.isPaid = False
        return

    def removeCopiedNodes(self):
        self.dropShadow = self.find('**/drop_shadow*')
        if not self.dropShadow.isEmpty():
            self.deleteDropShadow()
        else:
            self.dropShadow = None
        return

    def flattenHuman(self):
        self.deleteNametag3d()
        self.getWeaponJoints()

    def __doneFlattenHuman(self, models):
        self.flattenPending = None
        self.getWeaponJoints()
        return

    def copyHuman(self, other):
        self.gender = other.gender
        self.loaded = other.loaded
        self.type = other.type
        self.loadAnimatedHead = other.loadAnimatedHead
        self.model = None
        return

    def delete(self):
        try:
            self.Human_deleted
        except:
            self.Human_deleted = 1
            taskMgr.remove(self.__blinkName)
            if self.dropShadow and not self.dropShadow.isEmpty():
                self.deleteDropShadow()
            del self.eyeFSM
            self.controlShapes = None
            self.sliderNames = None
            if self.model:
                self.model.delete()
                del self.model
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

    def getCrazyColorSkinIndex(self):
        return self.crazyColorSkinIndex

    def setCrazyColorSkinIndex(self, index):
        if len(HumanDNA.crazySkinColors) > index:
            self.crazyColorSkinIndex = index
        else:
            self.notify.warning('(MasterHuman)index: %d is out of bounds for crazyColorSkin: %d' % (index, len(HumanDNA.crazySkinColors)))

    def generateSkinColor(self):
        skinColor = self.style.getSkinColor()
        lowColor = self.model.lowLODSkinColor
        color = VBase4(lowColor[0] * skinColor[0], lowColor[1] * skinColor[1], lowColor[2] * skinColor[2], 1.0)
        self.model.faces[0].setColorScale(skinColor)
        if self.model.newAvatars:
            self.model.currentBody.setColorScale(skinColor)
            if self.optimizeLOD:
                self.model.currentBody[2].setColorScale(color)
                self.model.faces[0][2].setColorScale(color)
        else:
            numPaths = self.model.body.getNumPaths()
            medIdx = numPaths / 3
            lowIdx = numPaths / 3 * 2
            if self.zombie:
                self.model.body.setColorScale(Vec4(1, 1, 1, 1))
                if self.optimizeLOD:
                    color = VBase4(121 / 255.0, 124 / 255.0, 103 / 255.0, 1.0)
                    for i in xrange(lowIdx, numPaths):
                        self.model.body[i].setColorScale(color)

                    self.model.faceZomb[2].setColorScale(color)
            else:
                self.model.body.setColorScale(skinColor)
                lowColor = self.model.lowLODSkinColor
                if self.optimizeLOD:
                    color = VBase4(lowColor[0] * skinColor[0], lowColor[1] * skinColor[1], lowColor[2] * skinColor[2], 1.0)
                    for i in xrange(lowIdx, numPaths):
                        self.model.body[i].setColorScale(color)

    def generateSkinTexture(self):
        bodyTextureIdx = self.style.body.skin
        if self.zombie:
            if self.gender == 'f':
                bodyTextureIdx = PirateFemale.ZOMB_BODY_TEXTURE
            else:
                bodyTextureIdx = PirateMale.ZOMB_BODY_TEXTURE
        if self.gender == 'f':
            body_textures = PirateFemale.body_textures[self.style.body.shape]
        else:
            body_textures = PirateMale.body_textures[self.style.body.shape]
        tex_name = self.getTrySafe(body_textures, bodyTextureIdx)
        if tex_name != None:
            tex = self.model.bodyTextures.findTexture(tex_name)
        else:
            return
        if tex:
            for parts in self.model.bodys:
                numPaths = parts.getNumPaths()
                for i in xrange(numPaths):
                    parts[i].setTexture(tex, 1)

        return

    def generateFaceTexture(self, default):
        if default:
            faceTextureIdx = 0
        else:
            faceTextureIdx = self.style.head.texture
        if faceTextureIdx >= len(self.model.faceTexturesSet):
            faceTextureIdx = 0
        self.model.faces[0].setTexture(self.model.faceTexturesSet[faceTextureIdx])

    def generateHairColor(self, colorName=None, colorModel=None):
        self.model.setHairBaseColor()

    def getTrySafe(self, list, idx):
        try:
            if type(idx) == str:
                lookup = idx.split('_cut')[0]
            else:
                lookup = idx
            return list[lookup]
        except:
            return None

        return None

    def generateEyesTexture(self):
        eyesTextureIdx = self.style.head.eyes.color
        if self.gender == 'f':
            eye_iris_textures = PirateFemale.eye_iris_textures
        else:
            eye_iris_textures = PirateMale.eye_iris_textures
        tex_name = self.getTrySafe(eye_iris_textures, eyesTextureIdx)
        if tex_name != None:
            tex = self.eyeIrisTextures.findTexture(tex_name)
        else:
            return
        if tex:
            self.model.irises.setTexture(tex, 1)
        return

    def generateHatColor(self):
        style = self.model.dna
        if self.zombie:
            style = self.model.dnaZomb
        hatColor = style.lookupHatColor()
        geom = self.getGeomNode()
        parts = geom.findAllMatches('**/hat_band*')
        parts.setColorScale(hatColor)

    def generateClothesColor(self):
        style = self.model.dna
        if self.zombie:
            style = self.model.dnaZomb
        clothesTopColor = style.lookupClothesTopColor()
        clothesBotColor = style.lookupClothesBotColor()
        geom = self.getGeomNode()
        if self.optimizeLOD:

            def tempColorParts(parts, ct):
                numPaths = parts.getNumPaths()
                lowIdx = numPaths / 3 * 2
                for j in xrange(lowIdx):
                    parts[j].setColorScale(ct)

                for j in xrange(lowIdx, numPaths):
                    cl = parts[j].getColorScale()
                    compoundColor = VBase4(cl[0] * ct[0], cl[1] * ct[1], cl[2] * ct[2], 1.0)
                    parts[j].setColorScale(compoundColor)

        else:

            def tempColorParts(parts, ct):
                parts.setColorScale(ct)

        colorParts = tempColorParts
        parts = geom.findAllMatches('**/clothing_layer1_shirt*')
        colorParts(parts, clothesTopColor[0])
        parts = geom.findAllMatches('**/clothing_layer2_vest*')
        colorParts(parts, clothesTopColor[1])
        parts = geom.findAllMatches('**/clothing_layer3_coat*')
        colorParts(parts, clothesTopColor[2])
        parts = geom.findAllMatches('**/clothing_layer1_pant*')
        colorParts(parts, clothesBotColor[0])
        del colorParts

    def generateTexture(self):
        self.generateFaceTexture(not self.useFaceTex)
        self.generateEyesTexture()

    def generateColor(self):
        self.generateSkinColor()
        self.generateHairColor()
        self.generateHatColor()

    def makeAnimDict(self, gender, animNames):
        self.animTable = []
        for currAnim in animNames:
            anim = animNames.get(currAnim)
            for currAnimName in anim:
                self.animTable.append([currAnimName, currAnimName])

        self.reducedAnimList = self.animTable

    def forceLoadAnimDict(self):
        for anim in self.animTable:
            self.getAnimControls(anim[0])

    def createAnimDict(self, customList=None):
        if self.reducedAnimList is None:
            self.animDict = self.prebuiltAnimData[self.gender + self.type]
            return
        if self.gender == 'f':
            filePrefix = 'models/char/f'
            genderPrefix = 'f'
        else:
            filePrefix = 'models/char/m'
            genderPrefix = 'm'
        filePrefix += 'p'
        animList = self.reducedAnimList
        if animList is None:
            animList = AnimListDict[self.type]
        self.animDict = {}
        for anim in animList:
            animSuffix = ''
            for i in range(0, len(CustomAnimDict[genderPrefix + self.type])):
                if anim[0] == CustomAnimDict[genderPrefix + self.type][i]:
                    animSuffix = '_' + genderPrefix + NewModelDict.get(self.type)
                    break

            self.animDict[anim[0]] = filePrefix + '_' + anim[1] + animSuffix

        if self.reducedAnimList is None:
            self.animDict.pop('intro')
        return filePrefix

    def generateBody(self, copy=1):
        if self.gender == 'm':
            filePrefix = 'models/char/mp'
        else:
            filePrefix = 'models/char/fp'
        messenger.send('tick')
        lodString = '2000'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '2000', copy)
        messenger.send('tick')
        if loader.loadModel(filePrefix + '_' + '1000', allowInstance=True) != None:
            lodString = '1000'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '1000', copy)
        messenger.send('tick')
        if loader.loadModel(filePrefix + '_' + '500', allowInstance=True) != None:
            lodString = '500'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '500', copy)
        messenger.send('tick')
        self.makeSubpart('head', ['zz_head01'], [])
        self.makeSubpart('torso', ['zz_spine01'], ['zz_head01'])
        self.makeSubpart('legs', ['dx_root'], ['zz_spine01'])
        self.setSubpartsComplete(True)
        self.eyeIrisTextures = loader.loadModel('models/misc/eye_iris.bam')
        return

    def setLODs(self):
        self.setLODNode()
        avatarDetail = base.config.GetString('avatar-detail', 'high')
        if avatarDetail == 'high':
            dist = [
             0, 20, 80, 1000000000]
        else:
            if avatarDetail == 'med':
                dist = [
                 0, 10, 20, 1000000000]
            elif avatarDetail == 'low':
                dist = [
                 0, 0, 10, 1000000000]
            else:
                raise StandardError, 'Invalid avatar-detail: %s' % avatarDetail
            self.addLOD(2000, dist[1], dist[0])
            self.addLOD(1000, dist[2], dist[1])
            self.addLOD(500, dist[3], dist[2])
            if self.optimizeLOD:
                lowLOD = self.getLOD('500')
                lowLOD.setTransparency(0, 1000)
        self.getLODNode().setCenter(Point3(0, 0, 5))

    def showLOD(self, lodName):
        self.generateTexture()
        self.model.setFromDNA()
        tex = self.model.faces[0][2].findTexture('*face*')

    def loadHuman(self, gender='m', other=None):
        self.gender = gender
        if self.gender == 'f':
            controlShapes = PirateFemale.ControlShapes
            sliderNames = PirateFemale.SliderNames
        else:
            controlShapes = PirateMale.ControlShapes
            sliderNames = PirateMale.SliderNames
        self.setLODs()
        self.loadAnimatedHead = True
        self.generateBody()
        if self.gender == 'f':
            self.type = BodyDefs.femaleFrames[self.style.getBodyShape()]
            self.model = PirateFemale.PirateFemale(self, self.style)
        else:
            self.type = BodyDefs.maleFrames[self.style.getBodyShape()]
            self.model = PirateMale.PirateMale(self, self.style)
        self.faceAwayFromViewer()
        self.lods = self.getLODNames()
        if self.gender == 'f':
            self.headFudgeHpr = Vec3(0, 0, 0)
            idx = 1
        else:
            self.headFudgeHpr = Vec3(0, 0, 0)
            idx = 0
        messenger.send('tick')
        self.model.setupHead(2000)
        messenger.send('tick')
        self.model.setupBody(2000)
        messenger.send('tick')
        self.model.setupClothing(2000)
        messenger.send('tick')
        if self.master:
            self.model.setupSelectionChoices('NPC')
        self.showNormal()
        self.createAnimDict()
        messenger.send('tick')
        self.initAnimsOnAllLODs(['head', 'legs', 'torso', 'modelRoot'])
        messenger.send('tick')
        self.controlShapes = controlShapes
        self.sliderNames = sliderNames
        self.initHeadControlShapes()
        self.storeJoints()
        self.find('**/nametag3d').detachNode()
        self.findAllMatches('**/name_tag').detach()
        self.rootNode = self.getLOD('2000').find('**/dx_root')
        self.floorOffsetZ = self.rootNode.getZ()
        messenger.send('tick')
        root = self.getLOD('500')
        gr = SceneGraphReducer()
        gr.applyAttribs(root.node(), gr.TTTransform | gr.TTTexMatrix | gr.TTOther)
        gr.makeCompatibleFormat(root.node(), 0)
        gr.premunge(root.node(), RenderState.makeEmpty())
        gr.decompose(root.node())
        stashedSet = root.findAllMatches('**/@@*')
        stashedSet.unstash()
        gr.makeCompatibleFormat(root.node(), 0)
        stashedSet.stash()
        messenger.send('tick')
        for face in self.model.faces[0]:
            node = face.node()
            for i in range(node.getNumGeoms()):
                face.node().setGeomState(i, RenderState.makeEmpty())

    def initializeMiscNodes(self):
        self.initializeNametag3d()
        self.initializeDropShadow()
        if self.getLOD('2000') == None:
            return
        exposedHeadJoint = self.getLOD('2000').find('**/def_head01')
        if not exposedHeadJoint.isEmpty():
            idx = 0
            if self.gender == 'f':
                idx = 1
            exposedHeadJoint.setScale(1)
            self.headNode.reparentTo(exposedHeadJoint)
            self.headNode.setScale(HeadScales[idx][self.style.getBodyShape()])
        return

    def undoControlJoints(self):
        self.getGeomNode().getParent().findAllMatches('def_*').detach()
        self.getGeomNode().getParent().findAllMatches('trs_*').detach()
        self.findAllMatches('def_*').detach()
        self.findAllMatches('trs_*').detach()

    def cleanupHuman(self, gender='m'):
        self.eyeFSM.request('off')
        self.undoControlJoints()
        self.eyeLids = {}
        self.eyeBalls = {}
        self.eyeIris = {}
        self.flush()
        self.loaded = 0
        self.master = 0

    def generateHuman(self, gender='m'):
        self.loadHuman(self.style.gender)

    def getShadowJoint(self):
        return self

    def getNametagJoints(self):
        joints = []
        for lodName in self.getLODNames():
            bundle = self.getPartBundle('legs', lodName)
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
            if not self.eyeLids[lodName].isEmpty():
                self.eyeLids[lodName].hide()
                self.eyeBalls[lodName].show()
                self.eyeIris[lodName].show()

    def exitEyeFSMOpen(self):
        pass

    def enterEyeFSMClosed(self):
        return
        for lodName in self.getLODNames():
            if not self.eyeLids[lodName].isEmpty():
                self.eyeLids[lodName].show()
                self.eyeBalls[lodName].hide()
                self.eyeIris[lodName].hide()

    def exitEyeFSMClosed(self):
        pass

    def setControlValue(self, r, name):
        if self.style.getGender() == 'f':
            matrixF = FemaleHeadShapeControlJointMatrix
            matrixI = FemaleHeadShapeInitialControlJointMatrix
        else:
            matrixF = MaleHeadShapeControlJointMatrix
            matrixI = MaleHeadShapeInitialControlJointMatrix
        shapes = self.controlShapes
        ctl = shapes[name]
        slider = ctl[0]
        if r < 0.0:
            if len(ctl) > 1:
                slider = ctl[1]
        for i in range(0, len(slider)):
            jointName = slider[i][0]
            jointCtls = self.findAllMatches(jointName)
            posI = matrixI[jointName][0]
            hprI = matrixI[jointName][1]
            sclI = matrixI[jointName][2]
            posF = VBase3(posI[0], posI[1], posI[2])
            hprF = VBase3(hprI[0], hprI[1], hprI[2])
            sclF = VBase3(sclI[0], sclI[1], sclI[2])
            self.notify.debug('scv: %s initial %s' % (jointName, posI))
            dr = slider[i][4] * r
            ctl[0][i][5] = dr
            posDelta = VBase3(0, 0, 0)
            hprDelta = VBase3(0, 0, 0)
            sclDelta = VBase3(0, 0, 0)
            for sliderIdx in xrange(0, len(matrixF[jointName])):
                sliderName = matrixF[jointName][sliderIdx]
                jointSet = shapes[sliderName][0]
                for jointIdx in xrange(0, len(jointSet)):
                    if jointSet[jointIdx][0] == jointName:
                        if jointSet[jointIdx][1] == TX:
                            posDelta.setX(posDelta.getX() + jointSet[jointIdx][5])
                        elif jointSet[jointIdx][1] == TY:
                            posDelta.setY(posDelta.getY() + jointSet[jointIdx][5])
                        elif jointSet[jointIdx][1] == TZ:
                            posDelta.setZ(posDelta.getZ() + jointSet[jointIdx][5])
                        elif jointSet[jointIdx][1] == RX:
                            hprDelta.setX(hprDelta.getX() + jointSet[jointIdx][5])
                        elif jointSet[jointIdx][1] == RY:
                            hprDelta.setY(hprDelta.getY() + jointSet[jointIdx][5])
                        elif jointSet[jointIdx][1] == RZ:
                            hprDelta.setZ(hprDelta.getZ() + jointSet[jointIdx][5])
                        elif jointSet[jointIdx][1] == SX:
                            if r < 0.0:
                                sclDelta.setX(sclDelta.getX() + jointSet[jointIdx][5] / jointSet[jointIdx][2])
                            else:
                                sclDelta.setX(sclDelta.getX() + jointSet[jointIdx][5])
                        elif jointSet[jointIdx][1] == SY:
                            if r < 0.0:
                                sclDelta.setY(sclDelta.getY() + jointSet[jointIdx][5] / jointSet[jointIdx][2])
                            else:
                                sclDelta.setY(sclDelta.getY() + jointSet[jointIdx][5])
                        elif jointSet[jointIdx][1] == SZ:
                            if r < 0.0:
                                sclDelta.setZ(sclDelta.getZ() + jointSet[jointIdx][5] / jointSet[jointIdx][2])
                            else:
                                sclDelta.setZ(sclDelta.getZ() + jointSet[jointIdx][5])
                        else:
                            self.notify.warning('scv:wrong element = %s' % jointSet[jointIdx][1])

            self.notify.debug('scv: %s composite posDelta = %s' % (jointName, posDelta))
            posF.setX(posI[0] + posDelta[0])
            posF.setY(posI[1] + posDelta[1])
            posF.setZ(posI[2] + posDelta[2])
            self.notify.debug('scv: %s final posDelta%s' % (jointName, posF))
            self.notify.debug('scv: %s composite hprDelta = %s' % (jointName, hprDelta))
            hprF.setX(hprI[0] + hprDelta[0])
            hprF.setY(hprI[1] + hprDelta[1])
            hprF.setZ(hprI[2] + hprDelta[2])
            self.notify.debug('scv: %s final hprDelta%s' % (jointName, hprF))
            self.notify.debug('scv: %s composite sclDelta = %s' % (jointName, sclDelta))
            sclF.setX(sclI[0] + sclDelta[0])
            sclF.setY(sclI[1] + sclDelta[1])
            sclF.setZ(sclI[2] + sclDelta[2])
            self.notify.debug('scv: %s final sclDelta%s' % (jointName, sclF))
            for j in range(0, jointCtls.getNumPaths()):
                jointCtl = jointCtls[j]
                jointCtl.setPosHprScale(posF, hprF, sclF)

    def applyBodyShaper(self):
        if self.style.getGender() == 'f':
            tjs = FemaleBodyShapeTranslateJoints
            sjs = FemaleBodyShapeScaleJoints
            matrix = FemaleBodyShapeControlJointMatrix
        else:
            tjs = MaleBodyShapeTranslateJoints
            sjs = MaleBodyShapeScaleJoints
            matrix = MaleBodyShapeControlJointMatrix
        type = self.style.getBodyShape()
        for jointName in tjs:
            transData = self.jointTrans[jointName]
            vector = matrix[jointName][type]
            self.joints[jointName].applyFreezeMatrix(vector, transData[1], transData[2])

        for jointName in sjs:
            transData = self.jointTrans[jointName]
            vector = matrix[jointName][type]
            self.joints[jointName].applyFreezeMatrix(transData[0], transData[1], vector)

        value = self.style.getHeadSize()
        mappedValue = 0.9 + (1 + value) * 0.1
        transData = self.jointTrans['def_extra_jt']
        self.joints['def_extra_jt'].applyFreezeMatrix(transData[0], transData[1], Vec3(2 - mappedValue, mappedValue, 1))
        transData = self.jointTrans['def_head01']
        idx = 0
        if self.style.gender == 'f':
            idx = 1
        self.joints['def_head01'].applyFreezeMatrix(transData[0], transData[1], Vec3(HeadScales[idx][self.style.getBodyShape()]))
        self.setGlobalScale(self.calcBodyScale())

    def undoBodyShaper(self):
        if self.style.getGender() == 'f':
            cjs = FemaleBodyShapeControlJoints
        else:
            cjs = MaleBodyShapeControlJoints

    def applyHeadShaper(self):
        self.setHeadControlShapeValues()

    def undoHeadShaper(self):
        if self.style.getGender() == 'f':
            cjs = FemaleHeadShapeControlJoints
        else:
            cjs = MaleHeadShapeControlJoints

    def createControlJoints(self):
        if self.style.getGender() == 'f':
            cjs = FemaleHeadShapeControlJoints
        else:
            cjs = MaleHeadShapeControlJoints
        for jointName in cjs:
            for lodName in self.getLODNames():
                if lodName == '2000':
                    joint = self.controlJoint(None, 'legs', jointName, lodName)
                elif lodName == '1000':
                    continue
                elif lodName == '500':
                    continue

        return

    def initHeadControlShapes(self):
        if self.style.getGender() == 'f':
            cjs = FemaleHeadShapeControlJoints
            matrixF = FemaleHeadShapeControlJointMatrix
            matrixI = FemaleHeadShapeInitialControlJointMatrix
            matrixIHelper = FemaleHeadInitHelper
        else:
            cjs = MaleHeadShapeControlJoints
            matrixF = MaleHeadShapeControlJointMatrix
            matrixI = MaleHeadShapeInitialControlJointMatrix
            matrixIHelper = MaleHeadInitHelper
        if len(matrixF['initialized']) > 0:
            return
        initializedMatrixI = len(matrixI['initialized'])
        initializedMatrixF = len(matrixF['initialized'])
        for jointName in cjs:
            transform = TransformState.makeMat(self.getJointTransform('legs', jointName, '2000'))
            pos = Vec3(transform.getPos())
            hpr = Vec3(transform.getHpr())
            scale = Vec3(transform.getScale())
            matrixI[jointName].append(pos)
            matrixI[jointName].append(hpr)
            matrixI[jointName].append(scale)
            matrixIHelper[jointName] = [
             pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2], scale[0], scale[1], scale[2]]

        matrixI['initialized'].append('initialized')
        shapes = self.controlShapes
        names = self.sliderNames
        for i in xrange(0, len(shapes)):
            slider = shapes[names[i]]
            for k in xrange(0, len(slider[0])):
                slider[0][k][4] = slider[0][k][2]
                if len(slider) > 1:
                    slider[1][k][4] = slider[1][k][2]

        for i in xrange(0, len(shapes)):
            slider = shapes[names[i]]
            for k in xrange(0, len(slider[0])):
                jointCtl = slider[0][k]
                jointName = jointCtl[0]
                matrixF[jointName].append(names[i])
                pos = matrixI[jointName][0]
                hpr = matrixI[jointName][1]
                scl = matrixI[jointName][2]
                if jointCtl[1] < 3:
                    posDelta = jointCtl[4] - pos[jointCtl[1]]
                    jointCtl[4] = posDelta
                    if len(slider) > 1:
                        jointCtl = slider[1][k]
                        jointCtl[4] = posDelta
                elif jointCtl[1] > 2 and jointCtl[1] < 6:
                    hprDelta = jointCtl[4] - hpr[jointCtl[1] - 3]
                    jointCtl[4] = hprDelta
                    if len(slider) > 1:
                        jointCtl = slider[1][k]
                        jointCtl[4] = hprDelta
                else:
                    sclDelta = jointCtl[4] - scl[jointCtl[1] - 6]
                    jointCtl[4] = sclDelta
                    if len(slider) > 1:
                        jointCtl = slider[1][k]
                        jointCtl[4] = sclDelta

        matrixF['initialized'].append('initialized')

    def setHeadControlShapeValues_old(self):
        value = self.style.getHeadSize()
        mappedValue = 0.9 + (1 + value) * 0.1
        self.setControlValue(self.style.getHeadWidth(), 'headWidth')
        self.setControlValue(self.style.getHeadHeight(), 'headHeight')
        self.setControlValue(self.style.getHeadRoundness(), 'headRoundness')
        self.setControlValue(self.style.getJawWidth(), 'jawWidth')
        self.setControlValue(self.style.getJawAngle(), 'jawChinAngle')
        self.setControlValue(self.style.getJawChinSize(), 'jawChinSize')
        self.setControlValue(self.style.getJawLength(), 'jawLength')
        self.setControlValue(self.style.getMouthWidth(), 'mouthWidth')
        self.setControlValue(self.style.getMouthLipThickness(), 'mouthLipThickness')
        self.setControlValue(self.style.getCheekFat(), 'cheekFat')
        self.setControlValue(self.style.getBrowProtruding(), 'browProtruding')
        self.setControlValue(self.style.getEyeCorner(), 'eyeCorner')
        self.setControlValue(self.style.getEyeOpeningSize(), 'eyeOpeningSize')
        self.setControlValue(self.style.getEyeBulge(), 'eyeSpacing')
        self.setControlValue(self.style.getNoseBridgeWidth(), 'noseBridgeWidth')
        self.setControlValue(self.style.getNoseNostrilWidth(), 'noseNostrilWidth')
        self.setControlValue(self.style.getNoseLength(), 'noseLength')
        self.setControlValue(self.style.getNoseBump(), 'noseBump')
        self.setControlValue(self.style.getNoseNostrilHeight(), 'noseNostrilHeight')
        self.setControlValue(self.style.getNoseNostrilAngle(), 'noseNostrilAngle')
        self.setControlValue(self.style.getNoseBridgeBroke(), 'noseBridgeBroke')
        self.setControlValue(self.style.getNoseNostrilBroke(), 'noseNostrilBroke')
        self.setControlValue(self.style.getEarScale(), 'earScale')
        self.setControlValue(self.style.getEarFlapAngle(), 'earFlap')
        self.setControlValue(self.style.getEarPosition(), 'earPosition')

    def getGlobalScale(self):
        return self.scaleNode.getScale()

    def setGlobalScale(self, scale):
        transData = self.jointTrans['def_head01']
        pos = Vec3(transData[0])
        pos.setZ(-(self.floorOffsetZ * (1 - scale)))
        self.joints['def_scale_jt'].applyFreezeMatrix(pos, transData[1], Vec3(scale))
        self.rootScale = scale

    def calcBodyScale(self):
        idx = 0
        if self.gender == 'f':
            idx = 1
        mappedValue = (0.8 + (1 + self.style.getBodyHeight()) * 0.2) * BodyScales[idx][self.style.getBodyShape()]
        return mappedValue

    def showZombie(self):
        self.model.irises.stash()
        self.model.faces[0].stash()
        self.model.faceZomb.unstash()
        self.generateSkinTexture()

    def showNormal(self):
        self.model.irises.unstash()
        self.model.faces[0].unstash()
        self.model.faceZomb.stash()
        self.generateSkinTexture()

    def takeAwayTexture(self, geoms, omitFace=False):
        emptyRenderState = RenderState.makeEmpty()
        eyeIrisColor = VBase4(0, 0, 0, 1)
        for i in range(0, geoms.getNumPaths()):
            element = geoms[i]
            if 'eye_iris' in element.getName():
                element.setColorScale(eyeIrisColor)
            elif omitFace and 'master_face' in element.getName():
                continue
            element.setTextureOff()
            geom = element.node()
            for j in range(0, geom.getNumGeoms()):
                geom.setGeomState(j, emptyRenderState)

    def optimizeMedLOD(self):
        medLOD = self.getLOD('1000')
        geoms = medLOD.findAllMatches('**/teeth*')
        geoms.stash()
        self.medSkinGone = False
        geoms = medLOD.find('**/body_forearm*')
        if geoms.isEmpty():
            self.medSkinGone = True
            geoms = medLOD.findAllMatches('**/body_*')
            self.takeAwayTexture(geoms, True)
        geoms = medLOD.findAllMatches('**/hair_*')
        self.takeAwayTexture(geoms)
        if self.gender != 'f':
            geoms = medLOD.findAllMatches('**/beard_*')
            self.takeAwayTexture(geoms)
            geoms = medLOD.findAllMatches('**/mustache_*')
            self.takeAwayTexture(geoms)
        geoms = medLOD.findAllMatches('**/eye_*')
        self.takeAwayTexture(geoms)
        geoms = medLOD.findAllMatches('**/clothing_layer2_belt_*')
        self.takeAwayTexture(geoms)
        geoms = medLOD.findAllMatches('**/clothing_layer1_shoe_*')
        self.takeAwayTexture(geoms)

    def optimizeLowLOD(self):
        lowLOD = self.getLOD('500')
        geoms = lowLOD.findAllMatches('**/teeth*')
        geoms.stash()
        geoms = lowLOD.findAllMatches('**/+GeomNode')
        self.takeAwayTexture(geoms)

    def setHeadControlShapeValues(self):
        value = self.style.getHeadSize()
        mappedValue = 0.9 + (1 + value) * 0.1
        self.setControlValue_new(self.style.getHeadWidth(), 'headWidth')
        self.setControlValue_new(self.style.getHeadHeight(), 'headHeight')
        self.setControlValue_new(self.style.getHeadRoundness(), 'headRoundness')
        self.setControlValue_new(self.style.getJawWidth(), 'jawWidth')
        self.setControlValue_new(self.style.getJawAngle(), 'jawChinAngle')
        self.setControlValue_new(self.style.getJawChinSize(), 'jawChinSize')
        self.setControlValue_new(self.style.getJawLength(), 'jawLength')
        self.setControlValue_new(self.style.getMouthWidth(), 'mouthWidth')
        self.setControlValue_new(self.style.getMouthLipThickness(), 'mouthLipThickness')
        self.setControlValue_new(self.style.getCheekFat(), 'cheekFat')
        self.setControlValue_new(self.style.getBrowProtruding(), 'browProtruding')
        self.setControlValue_new(self.style.getEyeCorner(), 'eyeCorner')
        self.setControlValue_new(self.style.getEyeOpeningSize(), 'eyeOpeningSize')
        self.setControlValue_new(self.style.getEyeBulge(), 'eyeSpacing')
        self.setControlValue_new(self.style.getNoseBridgeWidth(), 'noseBridgeWidth')
        self.setControlValue_new(self.style.getNoseNostrilWidth(), 'noseNostrilWidth')
        self.setControlValue_new(self.style.getNoseLength(), 'noseLength')
        self.setControlValue_new(self.style.getNoseBump(), 'noseBump')
        self.setControlValue_new(self.style.getNoseNostrilHeight(), 'noseNostrilHeight')
        self.setControlValue_new(self.style.getNoseNostrilAngle(), 'noseNostrilAngle')
        self.setControlValue_new(self.style.getNoseBridgeBroke(), 'noseBridgeBroke')
        self.setControlValue_new(self.style.getNoseNostrilBroke(), 'noseNostrilBroke')
        self.setControlValue_new(self.style.getEarScale(), 'earScale')
        self.setControlValue_new(self.style.getEarFlapAngle(), 'earFlap')
        self.setControlValue_new(self.style.getEarPosition(), 'earPosition')
        self.postProcess_setHeadControlShapeValues()

    def setControlValue_new(self, r, name):
        ctl = self.controlShapes[name]
        zeroindex = ctl[0]
        sliders = zeroindex
        if r < 0.0:
            if len(ctl) > 1:
                sliders = ctl[1]
        for i in range(0, len(sliders)):
            zeroindex[i][5] = sliders[i][4] * r

    def postProcess_setHeadControlShapeValues(self):
        if self.style.getGender() == 'f':
            cjs = FemaleHeadShapeControlJoints
            matrixF = FemaleHeadShapeControlJointMatrix
            matrixIHelper = FemaleHeadInitHelper
        else:
            cjs = MaleHeadShapeControlJoints
            matrixF = MaleHeadShapeControlJointMatrix
            matrixIHelper = MaleHeadInitHelper
        for jointName in cjs:
            transList = list(matrixIHelper[jointName])
            for sliderName in matrixF[jointName]:
                for sliderJoint in self.controlShapes[sliderName][0]:
                    if sliderJoint[0] == jointName:
                        transList[sliderJoint[1]] += sliderJoint[5]

            self.joints[jointName].applyFreezeMatrix(Vec3(*transList[0:3]), Vec3(*transList[3:6]), Vec3(*transList[6:9]))

    def quickGetJointTransform(self, jointName):
        return self.joints[jointName][0].getDefaultValue()

    def storeJoints(self):
        if self.style.gender == 'm':
            bJoints = MaleBodyShapeControlJoints
            hJoints = MaleHeadShapeControlJoints
        else:
            bJoints = FemaleBodyShapeControlJoints
            hJoints = FemaleHeadShapeControlJoints
        for name in bJoints + hJoints + ('def_head01', 'def_extra_jt', 'def_scale_jt'):
            joint = self.getJoints(jointName=name)
            self.joints[name] = joint[0]
            ts = TransformState.makeMat(joint[0].getDefaultValue())
            self.jointTrans[name] = (Vec3(ts.getPos()), Vec3(ts.getHpr()), Vec3(ts.getScale()))

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
            animSuffix = ''
            for i in range(0, len(CustomAnimDict[qualifier])):
                if anim[0] == CustomAnimDict[qualifier][i]:
                    animSuffix = '_' + gender + NewModelDict.get(type)
                    break

            cls.prebuiltAnimData[qualifier][anim[0]] = prefix + '_' + anim[1] + animSuffix

        cls.prebuiltAnimData[qualifier].pop('intro')


MasterHuman.setupAnimDicts()