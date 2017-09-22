from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from pirates.pirate import HumanDNA
from pirates.makeapirate import ClothingGlobals
from pirates.inventory.ItemConstants import DYE_COLORS
from pirates.piratesbase import Freebooter
import random
import TattooGlobals
from pirates.pirate import BodyDefs
from pirates.inventory import ItemGlobals, DropGlobals
from otp.otpbase import OTPRender
TX = 0
TY = 1
TZ = 2
RX = 3
RY = 4
RZ = 5
SX = 6
SY = 7
SZ = 8
HAT = 0
SHIRT = 1
VEST = 2
COAT = 3
PANT = 4
BELT = 5
SOCK = 6
SHOE = 7
ZOMB_BODY_TEXTURE = 1
ZOMB_HAIR_COLOR = 7
ZOMB_HAT = 8
ZOMB_SHIRT = 0
ZOMB_SHIRT_TEXTURE = 0
ZOMB_VEST = 0
ZOMB_VEST_TEXTURE = 0
ZOMB_COAT = 0
ZOMB_COAT_TEXTURE = 0
ZOMB_PANT = 1
ZOMB_PANT_TEXTURE = 11
ZOMB_BELT = 0
ZOMB_SHOE = 0
ZOMB_SHOE_TEXTURE = 0
body_textures = BodyDefs.maleBodyTextures
face_textures = [
 'male_face_cauc_a', 'male_face_cauc_b', 'male_face_asian_a', 'male_face_dark_a', 'male_face_cauc_c', 'male_face_asian_b', 'male_face_dark_b']
eye_iris_textures = [
 'pupilAqua', 'pupilBlue', 'pupilDarkBrown', 'pupilGreen', 'pupilHazel', 'pupilLightBrown']
male_hairs = [
 'style 0: bald', 'style 1: base w/A_top', 'style 2: base w/A1_top', 'style 3: base w/A_top + A2_sides', 'style 4: base w/A1_top + A2_sides', 'style 5: base w/A_top + B_ponytail', 'style 6: base w/A1_top + B_ponytail', 'style 8: base w/A_top + E_spike', 'style 9: base w/A1_top + E_spike', 'style 10: balding f0', 'style 11: balding g0', 'style 12: base w/A_top + H_mullet', 'style 13: base w/A1_top + H_mullet', 'style 14: mohawk i0']
vector_tattoos = [
 [
  0, 0.127, 0.194, 0.191, 0, 0], [0, 0.203, 0.579, 0.079, 271.1, 0], [0, 0.203, 0.831, 0.079, 271.1, 0], [0, 0.5, 0.5, 1.0, 0, 0], [0, 0.13, 0.35, 0.1, 0, 0], [0, 0.5, 0.5, 0.1, 0, 0], [0, 0.5, 0.5, 0.1, 0, 0], [0, 0.5, 0.5, 0.1, 0, 0]]
jewelry_geos_face = [
 'acc_none', 'acc_face_brow_spike_left', 'acc_face_brow_spike_right', 'acc_face_brow_ring_left', 'acc_face_brow_ring_right', 'acc_face_ear_cuff_a_left', 'acc_face_ear_cuff_a_right', 'acc_face_ear_cuff_b_left', 'acc_face_ear_cuff_b_right', 'acc_face_ear_cuff_c_left', 'acc_face_ear_cuff_c_right', 'acc_face_ear_open_left', 'acc_face_ear_open_right', 'acc_face_ear_stud_left', 'acc_face_ear_stud_right', 'acc_face_ear_spike_top_left', 'acc_face_ear_spike_top_right', 'acc_face_ear_spike_bot_left', 'acc_face_ear_spike_bot_right', 'acc_face_ear_hoop_a_left', 'acc_face_ear_hoop_a_right', 'acc_face_ear_hoop_b_left', 'acc_face_ear_hoop_b_right', 'acc_face_ear_bighoop_left', 'acc_face_ear_bighoop_right', 'acc_face_lip_ring_top_left', 'acc_face_lip_ring_top_right', 'acc_face_lip_ring_bot_left', 'acc_face_lip_ring_bot_right', 'acc_face_nose_ring_left', 'acc_face_nose_ring_right', 'acc_face_lip_ring_center', 'acc_face_lip_jawry', 'acc_face_nose_post_top', 'acc_face_nose_post_bot', 'acc_face_nose_ring_center', 'acc_face_lip_mustache']
jewelry_geos_body = [
 'acc_none', 'acc_body_ring_left_index_base', 'acc_body_ring_right_index_base', 'acc_body_ring_left_index_stone', 'acc_body_ring_right_index_stone', 'acc_body_ring_left_mid_base', 'acc_body_ring_right_mid_base', 'acc_body_ring_left_mid_stone', 'acc_body_ring_right_mid_stone', 'acc_body_ring_left_ring_base', 'acc_body_ring_right_ring_base', 'acc_body_ring_left_ring_stone', 'acc_body_ring_right_ring_stone', 'acc_body_ring_left_pinky_base', 'acc_body_ring_right_pinky_base', 'acc_body_ring_left_pinky_stone', 'acc_body_ring_right_pinky_stone']
jewelry_options = {'LBrow': [[0], [1], [3], [1, 3]],'RBrow': [[0], [2], [4], [2, 4]],'LEar': [[0], [13], [11], [15], [21, 19], [17], [23], [9], [7], [5], [23, 9, 7], [9, 7], [11, 17], [13, 9, 7], [15, 21], [19], [5, 7], [5, 7, 9, 17]],'REar': [[0], [14], [12], [16], [22, 20], [18], [24], [10], [8], [6], [24, 10, 8], [10, 8], [12, 18], [14, 10, 8], [16, 22], [20], [6, 8], [6, 8, 10, 18]],'Nose': [[0], [30], [33], [34], [29], [35], [33, 34], [33, 35], [33, 34, 35], [29, 30, 33, 34, 35], [36]],'Mouth': [[0], [25], [27], [21], [25], [26], [32], [25, 28], [31, 28], [25, 26, 27, 28, 31, 32], [36]],'LHand': [[0], [1], [1, 3], [5], [5, 7], [9], [9, 11], [13], [13, 15], [1, 5], [1, 9], [5, 13], [1, 5, 9, 13]],'RHand': [[0], [2], [2, 4], [6], [6, 8], [10], [10, 12], [14], [14, 16], [2, 6], [2, 10], [6, 14], [2, 6, 10, 14]]}
clothes_textures = ClothingGlobals.textures['MALE']
SliderNames = [
 'headWidth', 'headHeight', 'headRoundness', 'jawWidth', 'jawChinAngle', 'jawChinSize', 'jawLength', 'mouthWidth', 'mouthLipThickness', 'cheekFat', 'browProtruding', 'eyeCorner', 'eyeOpeningSize', 'eyeSpacing', 'noseBridgeWidth', 'noseNostrilWidth', 'noseLength', 'noseBump', 'noseNostrilHeight', 'noseNostrilAngle', 'noseBridgeBroke', 'noseNostrilBroke', 'earScale', 'earFlap', 'earPosition']
ControlShapes = {'headWidth': [[['def_trs_left_forehead', TX, 0.224, 0, 0, 0], ['def_trs_right_forehead', TX, -0.224, 0, 0, 0]], [['def_trs_left_forehead', TX, 0.224, 0, 0, 0], ['def_trs_right_forehead', TX, -0.224, 0, 0, 0]]],'headHeight': [[['def_trs_forehead', TZ, 0.663, 0, 0, 0], ['def_trs_left_forehead', TZ, 0.569, 0, 0, 0], ['def_trs_right_forehead', TZ, 0.569, 0, 0, 0]], [['def_trs_forehead', TZ, 0.663, 0, 0, 0], ['def_trs_left_forehead', TZ, 0.569, 0, 0, 0], ['def_trs_right_forehead', TZ, 0.569, 0, 0, 0]]],'headRoundness': [[['def_trs_forehead', TZ, 0.608, 0, 0, 0], ['def_trs_left_forehead', TZ, 0.574, 0, 0, 0], ['def_trs_right_forehead', TZ, 0.574, 0, 0, 0], ['def_trs_mid_jaw', TZ, -0.176, 0, 0, 0], ['def_trs_mid_jaw', TY, -0.288, 0, 0, 0]]],'jawWidth': [[['def_trs_left_jaw2', TX, 0.218, 0, 0, 0], ['def_trs_right_jaw2', TX, -0.218, 0, 0, 0]], [['def_trs_left_jaw2', TX, 0.218, 0, 0, 0], ['def_trs_right_jaw2', TX, -0.218, 0, 0, 0]]],'jawLength': [[['trs_face_bottom', TZ, -0.02, 0, 0, 0]], [['trs_face_bottom', TZ, -0.02, 0, 0, 0]]],'jawChinAngle': [[['def_trs_left_jaw1', TY, -0.234, 0, 0, 0], ['def_trs_right_jaw1', TY, -0.234, 0, 0, 0], ['def_trs_mid_jaw', TY, -0.313, 0, 0, 0]], [['def_trs_left_jaw1', TY, -0.234, 0, 0, 0], ['def_trs_right_jaw1', TY, -0.234, 0, 0, 0], ['def_trs_mid_jaw', TY, -0.313, 0, 0, 0]]],'jawChinSize': [[['def_trs_left_jaw1', TX, 0.114, 0, 0, 0], ['def_trs_left_jaw1', TY, -0.209, 0, 0, 0], ['def_trs_left_jaw1', TZ, -0.118, 0, 0, 0], ['def_trs_right_jaw1', TX, -0.114, 0, 0, 0], ['def_trs_right_jaw1', TY, -0.209, 0, 0, 0], ['def_trs_right_jaw1', TZ, -0.118, 0, 0, 0], ['def_trs_mid_jaw', TZ, -0.201, 0, 0, 0]], [['def_trs_left_jaw1', TX, 0.114, 0, 0, 0], ['def_trs_left_jaw1', TY, -0.209, 0, 0, 0], ['def_trs_left_jaw1', TZ, -0.118, 0, 0, 0], ['def_trs_right_jaw1', TX, -0.114, 0, 0, 0], ['def_trs_right_jaw1', TY, -0.209, 0, 0, 0], ['def_trs_right_jaw1', TZ, -0.118, 0, 0, 0], ['def_trs_mid_jaw', TZ, -0.201, 0, 0, 0]]],'mouthWidth': [[['trs_lips_top', SX, 1.2, 0, 0, 0], ['trs_lips_bot', SX, 1.2, 0, 0, 0]]],'mouthLipThickness': [[['trs_lip_top', SZ, 1.2, 0, 0, 0], ['trs_lip_bot', SZ, 1.2, 0, 0, 0], ['trs_lip_left1', SZ, 1.2, 0, 0, 0], ['trs_lip_right1', SZ, 1.2, 0, 0, 0], ['trs_lip_left2', SZ, 1.2, 0, 0, 0], ['trs_lip_right2', SZ, 1.2, 0, 0, 0], ['trs_lip_left3', SZ, 1.2, 0, 0, 0], ['trs_lip_right3', SZ, 1.2, 0, 0, 0]], [['trs_lip_top', SZ, 1.2, 0, 0, 0], ['trs_lip_bot', SZ, 1.2, 0, 0, 0], ['trs_lip_left1', SZ, 1.2, 0, 0, 0], ['trs_lip_right1', SZ, 1.2, 0, 0, 0], ['trs_lip_left2', SZ, 1.2, 0, 0, 0], ['trs_lip_right2', SZ, 1.2, 0, 0, 0], ['trs_lip_left3', SZ, 1.2, 0, 0, 0], ['trs_lip_right3', SZ, 1.2, 0, 0, 0]]],'cheekFat': [[['def_trs_left_cheek', TX, 0.216, 0, 0, 0], ['def_trs_right_cheek', TX, -0.216, 0, 0, 0]], [['def_trs_left_cheek', TX, 0.216, 0, 0, 0], ['def_trs_right_cheek', TX, -0.216, 0, 0, 0]]],'browProtruding': [[['trs_left_eyebrow', TY, -0.05, 0, 0, 0], ['trs_right_eyebrow', TY, 0.05, 0, 0, 0]]],'eyeCorner': [[['trs_left_eyesocket', RZ, 45 - 10, 0, 0, 0], ['trs_right_eyesocket', RZ, -(45 - 10), 0, 0, 0]], [['trs_left_eyesocket', RZ, 45 - 10, 0, 0, 0], ['trs_right_eyesocket', RZ, -(45 - 10), 0, 0, 0]]],'eyeOpeningSize': [[['trs_left_eyesocket', SX, 1.1, 0, 0, 0], ['trs_left_eyesocket', SZ, 1.1, 0, 0, 0], ['trs_right_eyesocket', SX, 1.1, 0, 0, 0], ['trs_right_eyesocket', SZ, 1.1, 0, 0, 0]], [['trs_left_eyesocket', SX, 1.1, 0, 0, 0], ['trs_left_eyesocket', SZ, 1.1, 0, 0, 0], ['trs_right_eyesocket', SX, 1.1, 0, 0, 0], ['trs_right_eyesocket', SZ, 1.1, 0, 0, 0]]],'eyeSpacing': [[['trs_left_eyesocket', TX, 0.008, 0, 0, 0], ['trs_right_eyesocket', TX, -0.008, 0, 0, 0]], [['trs_left_eyesocket', TX, 0.008, 0, 0, 0], ['trs_right_eyesocket', TX, -0.008, 0, 0, 0]]],'noseBridgeWidth': [[['def_trs_mid_nose_top', SX, 1.25, 0, 0, 0]], [['def_trs_mid_nose_top', SX, 1.25, 0, 0, 0]]],'noseNostrilWidth': [[['def_trs_mid_nose_bot', SX, 1.2, 0, 0, 0]], [['def_trs_mid_nose_bot', SX, 1.2, 0, 0, 0]]],'noseLength': [[['def_trs_mid_nose_bot', TZ, 0.112, 0, 0, 0]], [['def_trs_mid_nose_bot', TZ, 0.112, 0, 0, 0]]],'noseBump': [[['def_trs_mid_nose_top', TY, -0.442, 0, 0, 0], ['def_trs_mid_nose_top', TZ, 0.265, 0, 0, 0]], [['def_trs_mid_nose_top', TY, -0.442, 0, 0, 0], ['def_trs_mid_nose_top', TZ, 0.265, 0, 0, 0]]],'noseBridgeBroke': [[['def_trs_mid_nose_top', TX, 0.015, 0, 0, 0]], [['def_trs_mid_nose_top', TX, 0.015, 0, 0, 0]]],'noseNostrilHeight': [[['def_trs_mid_nose_bot', SY, 1.25, 0, 0, 0]], [['def_trs_mid_nose_bot', SY, 1.25, 0, 0, 0]]],'noseNostrilAngle': [[['def_trs_mid_nose_bot', RY, 15, 0, 0, 0]], [['def_trs_mid_nose_bot', RY, 15, 0, 0, 0]]],'noseNostrilBroke': [[['def_trs_mid_nose_bot', TX, 0.015, 0, 0, 0]], [['def_trs_mid_nose_bot', TX, 0.015, 0, 0, 0]]],'earScale': [[['def_trs_left_ear', SZ, 1.1, 0, 0, 0], ['def_trs_right_ear', SZ, 1.1, 0, 0, 0], ['def_trs_left_ear', SX, 1.1, 0, 0, 0], ['def_trs_right_ear', SX, 1.1, 0, 0, 0]], [['def_trs_left_ear', SZ, 1.1, 0, 0, 0], ['def_trs_right_ear', SZ, 1.1, 0, 0, 0], ['def_trs_left_ear', SX, 1.1, 0, 0, 0], ['def_trs_right_ear', SX, 1.1, 0, 0, 0]]],'earFlap': [[['def_trs_left_ear', RX, -20, 0, 0, 0], ['def_trs_right_ear', RX, -160, 0, 0, 0]], [['def_trs_left_ear', RX, -20, 0, 0, 0], ['def_trs_right_ear', RX, -160, 0, 0, 0]]],'earPosition': [[['def_trs_left_ear', TZ, 0.216, 0, 0, 0], ['def_trs_right_ear', TZ, 0.216, 0, 0, 0]], [['def_trs_left_ear', TZ, 0.216, 0, 0, 0], ['def_trs_right_ear', TZ, 0.216, 0, 0, 0]]]}

class PirateMale(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateMale')

    def __init__(self, pirate, dna):
        self.pirate = pirate
        self.dna = dna
        self.dnaZomb = HumanDNA.HumanDNA()
        self.makeZombie()
        self.loaded = 0
        self.texDict = {}
        self.bodySets = [{}, {}, {}]
        self.tattooZones = [
         [
          1, 2, 3, 4, 5], [9, 11, 13], [8, 10, 12], [-1], [0], [2], [16, 17], [18, 19]]
        self.tattooStage = TextureStage('tattoo')
        self.tattooStage.setTexcoordName('tattoomap')
        self.tattoos = [
         1, 2, 3, 4, 5, 6, 7, 8]
        self.currentClothing = {'HAT': [0, 0, 0],'SHIRT': [0, 0, 0],'VEST': [0, 0, 0],'COAT': [0, 0, 0],'BELT': [0, 0, 0],'PANT': [0, 0, 0],'SHOE': [0, 0, 0]}
        self.currentClothingModels = {'HAT': NodePathCollection(),'HAIR': NodePathCollection(),'BEARD': NodePathCollection(),'MUSTACHE': NodePathCollection(),'SHIRT': NodePathCollection(),'VEST': NodePathCollection(),'COAT': NodePathCollection(),'BELT': [NodePathCollection(), NodePathCollection()],'PANT': NodePathCollection(),'SHOE': NodePathCollection()}
        self.currentBody = NodePathCollection()
        self.currentBody.addPath(NodePath('temp'))
        self.currentBody.addPath(NodePath('temp'))
        self.currentBody.addPath(NodePath('temp'))
        self.currentTatttooZones = [
         NodePathCollection(), NodePathCollection(), NodePathCollection()]
        self.newAvatars = base.config.GetBool('want-new-avatars', 1)

    def delete(self):
        del self.pirate
        del self.dna
        del self.dnaZomb

    def setHairBaseColor(self):
        dna = self.pirate.style
        if self.pirate.zombie:
            dna = self.dnaZomb
        baseColor = dna.getHairBaseColor()
        self.currentClothingModels['HAIR'].setColorScale(baseColor)
        self.currentClothingModels['BEARD'].setColorScale(baseColor)
        self.currentClothingModels['MUSTACHE'].setColorScale(baseColor)
        self.eyeBrows.setColorScale(baseColor)

    def setupTattoos(self):
        self.tattoos[0] = self.pirate.style.getTattooChest()
        self.tattoos[1] = self.pirate.style.getTattooZone2()
        self.tattoos[2] = self.pirate.style.getTattooZone3()
        self.tattoos[3] = self.pirate.style.getTattooZone4()
        self.tattoos[4] = self.pirate.style.getTattooZone5()
        self.tattoos[5] = self.pirate.style.getTattooZone6()
        self.tattoos[6] = self.pirate.style.getTattooZone7()
        self.tattoos[7] = self.pirate.style.getTattooZone8()
        for i in range(4):
            tattooArea = self.currentTattooZones[i]
            tattoo = self.tattoos[i]
            zones = self.tattooZones[i]
            tex, scale = TattooGlobals.getTattooImage(tattoo[0])
            scaleX = tattoo[3] * scale
            scaleY = tattoo[3]
            t = TransformState.makePosRotateScale2d(Vec2(tattoo[1], tattoo[2]), tattoo[4], Vec2(scaleX, scaleY))
            tma = TexMatrixAttrib.make(self.tattooStage, t)
            tattooArea.setAttrib(tma)
            tattooArea.setTexture(self.tattooStage, tex)

    def updateTattoo(self, index):
        if index > 3:
            return
        tattoo = self.tattoos[index]
        tattooArea = self.currentTattooZones[index]
        tex, scale = TattooGlobals.getTattooImage(tattoo[0])
        scaleX = tattoo[3] * scale
        scaleY = tattoo[3]
        t = TransformState.makePosRotateScale2d(Vec2(tattoo[1], tattoo[2]), tattoo[4], Vec2(scaleX, scaleY))
        tma = TexMatrixAttrib.make(self.tattooStage, t)
        tattooArea.setAttrib(tma)
        tattooArea.setTexture(self.tattooStage, tex)

    def setupHairMultiTexture(self):

        def setupMultiTexture(parts):
            for i in range(0, len(parts)):
                if not parts[i].isEmpty():
                    for j in range(0, parts[i].getNumPaths()):
                        hair = parts[i][j]
                        tc = hair.findAllTextureStages()
                        for k in range(0, tc.getNumTextureStages()):
                            if tc[k].getName().find('dummy') != -1:
                                tc.removeTextureStage(tc[k])
                                break

                        for k in range(0, tc.getNumTextureStages()):
                            if tc[k].getTexcoordName().getName().find('light') != -1:
                                tc[k].setMode(TextureStage.MBlend)
                                tc[k].setSort(10)
                            elif tc[k].getTexcoordName().getName().find('dark') != -1:
                                tc[k].setSort(0)

        setupMultiTexture(self.hairPieces)
        setupMultiTexture(self.beards)
        setupMultiTexture(self.mustaches)
        setupMultiTexture(self.eyeBrows)

    def showHair(self):
        for i in range(0, len(self.hairs[self.hairIdx])):
            pi = self.hairs[self.hairIdx][i]
            if not self.hairPieces[pi].isEmpty():
                self.hairPieces[pi].unstash()

    def hideHair(self):
        for i in range(0, len(self.hairs[self.hairIdx])):
            if not self.hairPieces[self.hairs[self.hairIdx][i]].isEmpty():
                self.hairPieces[self.hairs[self.hairIdx][i]].stash()
            if not self.hairCuts[self.hairs[self.hairIdx][i]].isEmpty():
                self.hairCuts[self.hairs[self.hairIdx][i]].stash()

    def handleHeadHiding(self):
        hairIdx = [self.pirate.style.getHairHair(), self.pirate.style.getHairBaseColor()]
        hatIdx = self.pirate.style.getClothesHat() + [self.pirate.style.getHatColor()]
        if self.pirate.zombie and 0:
            hatIdx = [
             ZOMB_HAT, 0, 0]
            hatColor = self.dnaZomb.lookupHatColor()
        else:
            hatColor = DYE_COLORS[hatIdx[2]]
        currentHat = self.hatSets[hatIdx[0]]
        currentHair = self.hairSets[hairIdx[0]][hatIdx[0]]
        self.currentClothingModels['HAIR'].stash()
        currentHair.unstash()
        self.currentClothingModels['BEARD'].stash()
        self.currentClothingModels['MUSTACHE'].stash()
        currentBeardIdx = self.pirate.style.getHairBeard()
        currentBeard = self.beards[currentBeardIdx]
        currentStache = self.mustaches[self.pirate.style.getHairMustache()]
        baseColor = self.pirate.style.getHairBaseColor()
        currentBeard.setColorScale(baseColor)
        currentStache.setColorScale(baseColor)
        currentBeard.unstash()
        if not (currentBeardIdx > 0 and currentBeardIdx < 4):
            currentStache.unstash()
        self.currentClothingModels['BEARD'] = currentBeard
        self.currentClothingModels['MUSTACHE'] = currentStache
        self.currentClothingModels['HAIR'] = currentHair
        self.currentClothingModels['HAT'].stash()
        texInfo = clothes_textures['HAT'][hatIdx[0]][hatIdx[1]]
        texName = texInfo[0].split('+')
        if self.texDict[texName[0]]:
            if len(texName) > 1:
                for base in (0, 2, 4):
                    currentHat[base].setTexture(self.texDict[texName[0]], 3)
                    currentHat[base + 1].setTexture(self.texDict[texName[1]], 4)

            else:
                currentHat.setTexture(self.texDict[texName[0]])
            currentHat.setColorScale(hatColor)
        self.currentClothingModels['HAT'] = currentHat
        if hatIdx[0] > 0:
            currentHat.setColorScale(hatColor)
            currentHat.unstash()
            if hatIdx[0] == 7:
                if hairIdx[0] in [0, 9, 10, 13]:
                    for i in range(0, currentHat.getNumPaths()):
                        if currentHat[i].getName().find('bald') == -1:
                            currentHat[i].stash()

                else:
                    for i in range(0, currentHat.getNumPaths()):
                        if currentHat[i].getName().find('bald') != -1:
                            currentHat[i].stash()

        self.setHairBaseColor()

    def showFacialHair(self):
        self.currentClothingModels['BEARD'].stash()
        self.currentClothingModels['MUSTACHE'].stash()
        currentBeard = self.beards[self.beardIdx]
        currentStache = self.mustaches[self.mustacheIdx]
        baseColor = self.pirate.style.getHairBaseColor()
        currentBeard.setColorScale(baseColor)
        currentStache.setColorScale(baseColor)
        currentBeard.unstash()
        if not (self.beardIdx > 0 and self.beardIdx < 4):
            currentStache.unstash()
        self.currentClothingModels['BEARD'] = currentBeard
        self.currentClothingModels['MUSTACHE'] = currentStache

    def setupHead(self, lodName='2000'):
        geom = self.pirate.getGeomNode()
        self.faceZomb = geom.findAllMatches('**/gh_master_face')
        self.faces = []
        faceData = NodePathCollection()
        irisData = NodePathCollection()
        eyeData = NodePathCollection()
        for lod in ['2000', '1000', '500']:
            flattenMe = NodePath('flattenMe')
            lodNP = self.pirate.getLOD(lod)
            faceSet = lodNP.findAllMatches('**/body_master_face')
            faceSet.addPathsFrom(lodNP.findAllMatches('**/eyelid*'))
            for i in xrange(faceSet.getNumPaths()):
                faceSet[i].copyTo(flattenMe)

            flattenMe.flattenStrong()
            faceParts = flattenMe.findAllMatches('**/+GeomNode')
            lodNP.findAllMatches('**/body_master_face').detach()
            lodNP.findAllMatches('**/eyelid*').detach()
            faceParts.reparentTo(lodNP.getChild(0))
            faceData.addPathsFrom(faceParts)
            flattenMe = NodePath('flattenMe')
            eyeballs = lodNP.findAllMatches('**/eye_ball*')
            for i in xrange(eyeballs.getNumPaths()):
                eyeballs[i].copyTo(flattenMe)

            flattenMe.flattenStrong()
            eyeBallParts = flattenMe.findAllMatches('**/+GeomNode')
            lodNP.findAllMatches('**/eye_ball*').detach()
            eyeBallParts.reparentTo(lodNP.getChild(0))
            eyeData.addPathsFrom(eyeBallParts)
            irisSet = lodNP.findAllMatches('**/eye_iris*')
            flattenMe = NodePath('flattenMe')
            for i in xrange(irisSet.getNumPaths()):
                irisSet[i].copyTo(flattenMe)

            flattenMe.flattenStrong()
            lodNP.findAllMatches('**/eye_iris*').detach()
            irisParts = flattenMe.findAllMatches('**/+GeomNode')
            irisParts.reparentTo(lodNP.getChild(0))
            irisData.addPathsFrom(irisParts)

        self.faces.append(faceData)
        self.irises = irisData
        self.eyeBalls = eyeData
        self.teeth = geom.findAllMatches('**/teeth*')
        self.tooths = []
        self.toothIdx = 0
        self.tooths.append(geom.findAllMatches('**/teeth_none*'))
        self.tooths.append(geom.findAllMatches('**/teeth_all*'))
        self.eyeBrow = geom.findAllMatches('**/hair_eyebrow_*')
        self.eyeBrows = []
        self.eyeBrowIdx = 0
        self.eyeBrows = NodePathCollection()
        for lod in ['2000', '1000', '500']:
            eyebrows = self.pirate.getLOD(lod).findAllMatches('**/hair_eyebrow_*')
            flattenMe = NodePath('flattenMe')
            for i in xrange(eyebrows.getNumPaths()):
                eyebrows[i].copyTo(flattenMe)

            flattenMe.flattenStrong()
            geoms = flattenMe.findAllMatches('**/+GeomNode')
            self.pirate.getLOD(lod).findAllMatches('**/hair_eyebrow_*').detach()
            geoms.reparentTo(self.pirate.getLOD(lod).getChild(0))
            self.eyeBrows.addPathsFrom(geoms)

        self.eyeBrows.stash()
        if base.config.GetBool('want-gen-pics-buttons'):
            self.eyes = self.pirate.findAllMatches('**/eye_*')
        self.hair = geom.findAllMatches('**/hair*')
        hairList = [
         '**/hair_none*', '**/hair_base', '**/hair_a0', '**/hair_a1', '**/hair_a2', '**/hair_b1', '**/hair_d0', '**/hair_e1', '**/hair_f0', '**/hair_g0', '**/hair_h0', '**/hair_i0']
        self.hairPieces = []
        self.hairPieces.append(geom.findAllMatches('**/hair_none*'))
        self.hairPieces.append(geom.findAllMatches('**/hair_base'))
        self.hairPieces.append(geom.findAllMatches('**/hair_a0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_a1'))
        self.hairPieces.append(geom.findAllMatches('**/hair_a2'))
        self.hairPieces.append(geom.findAllMatches('**/hair_b1'))
        self.hairPieces.append(geom.findAllMatches('**/hair_d0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_e1'))
        self.hairPieces.append(geom.findAllMatches('**/hair_f0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_g0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_h0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_i0'))
        self.hairs = []
        self.hairIdx = self.pirate.style.getHairHair()
        self.hairs.append([0])
        self.hairs.append([1, 2])
        self.hairs.append([1, 3])
        self.hairs.append([1, 2, 4])
        self.hairs.append([1, 3, 4])
        self.hairs.append([1, 2, 5])
        self.hairs.append([1, 3, 5])
        self.hairs.append([1, 2, 7])
        self.hairs.append([1, 3, 7])
        self.hairs.append([8])
        self.hairs.append([9])
        self.hairs.append([1, 2, 10])
        self.hairs.append([1, 3, 10])
        self.hairs.append([11])
        hairCutList = [
         '**/hair_none*', '**/hair_base_cut*', '**/hair_a0_cut*', '**/hair_a1_cut*', '**/hair_a2_cut*', '**/hair_b1_cut*', '**/hair_d0_cut*', '**/hair_e1_cut*', '**/hair_f0_cut*', '**/hair_g0_cut*', '**/hair_h0_cut*', '**/hair_i0_cut*']
        self.hairCuts = []
        self.hairCuts.append(geom.findAllMatches('**/hair_none*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_base_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_a0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_a1_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_a2_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_b1_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_d0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_e1_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_f0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_g0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_h0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_i0_cut*'))
        self.beard = geom.findAllMatches('**/beard_*')
        self.beards = []
        self.beardIdx = self.pirate.style.getHairBeard()
        self.beards.append(geom.findAllMatches('**/beard_none*'))
        self.beards.append(geom.findAllMatches('**/beard_a0*'))
        self.beards.append(geom.findAllMatches('**/beard_a1*'))
        self.beards.append(geom.findAllMatches('**/beard_h0*'))
        self.beards.append(geom.findAllMatches('**/beard_c1*'))
        self.beards.append(geom.findAllMatches('**/beard_c2*'))
        self.beards.append(geom.findAllMatches('**/beard_c3*'))
        self.beards.append(geom.findAllMatches('**/beard_f0*'))
        self.beards.append(geom.findAllMatches('**/beard_f1*'))
        self.beards.append(geom.findAllMatches('**/beard_g0*'))
        self.beards.append(geom.findAllMatches('**/beard_i0*'))
        self.beard.stash()
        self.mustache = geom.findAllMatches('**/mustache_*')
        self.mustaches = []
        self.mustacheIdx = self.pirate.style.getHairMustache()
        self.mustaches.append(geom.findAllMatches('**/mustache_none*'))
        self.mustaches.append(geom.findAllMatches('**/mustache_d0*'))
        self.mustaches.append(geom.findAllMatches('**/mustache_d1*'))
        self.mustaches.append(geom.findAllMatches('**/mustache_d2*'))
        self.mustaches.append(geom.findAllMatches('**/mustache_d3*'))
        self.mustaches.append(geom.findAllMatches('**/mustache_e0*'))
        self.mustaches.append(geom.findAllMatches('**/mustache_e1*'))
        self.mustache.stash()
        self.eyeBrows.unstash()
        self.hat = geom.findAllMatches('**/clothing_layer1_hat_*')
        self.hats = []
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_none'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_captain'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_tricorn'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_navy'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_india_navy'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_admiral'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_bandanna_full'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_bandanna_reg*'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_band_beanie'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_barbossa'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_french'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_spanish'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_french_1'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_french_2'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_french_3'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_spanish_1'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_spanish_2'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_spanish_3'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_land_1'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_land_2'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_land_3'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_holiday'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_party_1'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_party_2'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_GM'))
        self.colorableHats = [6, 7, 8]
        self.hat.stash()
        self.eyepatch = geom.findAllMatches('**/eye_patch*')
        self.eyepatch.stash()
        self.wig = geom.findAllMatches('**/wig*')
        self.wig.stash()
        self.jewelryFaceParts = []
        for name in jewelry_geos_face:
            self.jewelryFaceParts.append(self.pirate.findAllMatches('**/%s' % name))

        self.jewelryBodyParts = []
        for name in jewelry_geos_body:
            self.jewelryBodyParts.append(self.pirate.findAllMatches('**/%s' % name))

        for npc in self.jewelryFaceParts:
            length = npc.getNumPaths()
            for i in range(length):
                node = npc[i]
                node.showThrough(OTPRender.GlowCameraBitmask)

        for npc in self.jewelryBodyParts:
            length = npc.getNumPaths()
            for i in range(length):
                node = npc[i]
                node.showThrough(OTPRender.GlowCameraBitmask)

        self.accBody = geom.findAllMatches('**/acc_body*')
        self.numBodyJewelry = self.accBody.getNumPaths()
        self.accFace = geom.findAllMatches('**/acc_face*')
        self.numFaceJewelry = self.accFace.getNumPaths()
        self.accBody.stash()
        self.accFace.stash()
        self.jewelrySets = {}
        for key in jewelry_options.keys():
            self.jewelrySets[key] = []
            options = jewelry_options[key]
            if key == 'LHand' or key == 'RHand':
                parts = self.jewelryBodyParts
            else:
                parts = self.jewelryFaceParts
            for piece in options:
                primary = NodePathCollection()
                secondary = NodePathCollection()
                length = len(piece)
                if length == 1:
                    primary.addPathsFrom(parts[piece[0]])
                elif length > 1:
                    primary.addPathsFrom(parts[piece[0]])
                    for idx in range(1, length):
                        secondary.addPathsFrom(parts[piece[idx]])

                data = [
                 primary, secondary]
                self.jewelrySets[key].append(data)

        self.currentJewelry = {'LEar': [0, 0, 0],'REar': [0, 0, 0],'LBrow': [0, 0, 0],'RBrow': [0, 0, 0],'Nose': [0, 0, 0],'Mouth': [0, 0, 0],'LHand': [0, 0, 0],'RHand': [0, 0, 0]}
        self.hairLODs = []
        self.hairCutLODs = []
        for item in hairList:
            itemInfo = {}
            for lod in ['500', '1000', '2000']:
                itemInfo[lod] = self.pirate.getLOD(lod).findAllMatches(item)

            self.hairLODs.append(itemInfo)

        for item in hairCutList:
            itemInfo = {}
            for lod in ['500', '1000', '2000']:
                itemInfo[lod] = self.pirate.getLOD(lod).findAllMatches(item)

            self.hairCutLODs.append(itemInfo)

        self.generateHairSets()
        self.hair.stash()

    def setBlendValue(self, val, attr):
        self.pirate.setBlendValue(0.0, self.blendShapes[attr][0])
        if len(self.blendShapes[attr]) > 1:
            self.pirate.setBlendValue(0.0, self.blendShapes[attr][1])
        if val >= 0.0:
            if len(self.blendShapes[attr]) > 1:
                blendName = self.blendShapes[attr][1]
            else:
                blendName = self.blendShapes[attr][0]
        else:
            blendName = self.blendShapes[attr][0]
            val = -val
        self.pirate.setBlendValue(val, blendName)

    def setupBody(self, lodName=2000):
        geom = self.pirate.getGeomNode()
        self.body = self.pirate.findAllMatches('**/body_*')
        faceParts = []
        for i in xrange(self.body.getNumPaths()):
            if self.body[i].getName().find('master_face') >= 0:
                faceParts.append(self.body[i])

        for part in faceParts:
            self.body.removePath(part)

        if self.newAvatars:
            self.stripTexture(self.body)
        self.bodyPiecesToGroup = {0: 0,1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 2,9: 1,10: 2,11: 1,12: 2,13: 1,14: 2,15: 1,16: 0,17: 0,18: 0,19: 0,20: 0,21: 0}
        self.groupsToBodyPieces = [
         [
          0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21], [9, 11, 13, 15], [8, 10, 12, 14]]
        layerBList = [
         '**/body_neck*', '**/body_torso_base', '**/body_torso_back', '**/body_torso_front', '**/body_collar_sharp', '**/body_collar_round', '**/body_belt', '**/body_waist', '**/body_armpit_right', '**/body_armpit_left', '**/body_shoulder_right', '**/body_shoulder_left', '**/body_forearm_right', '**/body_forearm_left', '**/body_hand_right', '**/body_hand_left', '**/body_knee_right', '**/body_knee_left', '**/body_shin_right', '**/body_shin_left', '**/body_foot_right', '**/body_foot_left']
        self.layerBodyLODs = []
        for part in layerBList:
            bodyParts = {}
            for lod in ['2000', '1000', '500']:
                bodyParts[lod] = self.pirate.getLOD(lod).find(part)

            self.layerBodyLODs.append(bodyParts)

        chest = NodePathCollection()
        leftArm = NodePathCollection()
        rightArm = NodePathCollection()
        self.currentTattooZones = [
         chest, leftArm, rightArm, self.faces[0]]
        for i in self.bodyPiecesToGroup.items():
            self.currentTattooZones[i[1]].addPath(self.layerBodyLODs[i[0]]['2000'])
            self.currentTattooZones[i[1]].addPath(self.layerBodyLODs[i[0]]['1000'])
            self.currentTattooZones[i[1]].addPath(self.layerBodyLODs[i[0]]['500'])

        self.bodys = []
        self.bodyIdx = 0
        self.bodys.append(geom.findAllMatches('**/body_neck*'))
        self.bodys.append(geom.findAllMatches('**/body_torso_base'))
        self.bodys.append(geom.findAllMatches('**/body_torso_back'))
        self.bodys.append(geom.findAllMatches('**/body_torso_front'))
        self.bodys.append(geom.findAllMatches('**/body_collar_sharp'))
        self.bodys.append(geom.findAllMatches('**/body_collar_round'))
        self.bodys.append(geom.findAllMatches('**/body_belt'))
        self.bodys.append(geom.findAllMatches('**/body_waist'))
        self.bodys.append(geom.findAllMatches('**/body_armpit_right'))
        self.bodys.append(geom.findAllMatches('**/body_armpit_left'))
        self.bodys.append(geom.findAllMatches('**/body_shoulder_right'))
        self.bodys.append(geom.findAllMatches('**/body_shoulder_left'))
        self.bodys.append(geom.findAllMatches('**/body_forearm_right'))
        self.bodys.append(geom.findAllMatches('**/body_forearm_left'))
        self.bodys.append(geom.findAllMatches('**/body_hand_right'))
        self.bodys.append(geom.findAllMatches('**/body_hand_left'))
        self.bodys.append(geom.findAllMatches('**/body_knee_right'))
        self.bodys.append(geom.findAllMatches('**/body_knee_left'))
        self.bodys.append(geom.findAllMatches('**/body_shin_right'))
        self.bodys.append(geom.findAllMatches('**/body_shin_left'))
        self.bodys.append(geom.findAllMatches('**/body_foot_right'))
        self.bodys.append(geom.findAllMatches('**/body_foot_left'))
        for part in self.bodys:
            part.stash()

        self.currentBody = NodePathCollection()
        self.bodyTextures = loader.loadModel('models/misc/male_body.bam')
        self.numBodys = len(body_textures[0])
        self.bodyTextureIdx = self.pirate.style.getBodySkin()
        self.lowLODSkinColor = VBase4(0.81, 0.69, 0.62, 1.0)
        self.faceTextures = loader.loadModel('models/misc/male_face.bam')
        self.faceTexturesSet = []
        self.numFaces = len(face_textures)
        self.faceTextureIdx = self.pirate.style.getHeadTexture()
        self.numEyeColors = len(eye_iris_textures)
        self.eyesColorIdx = self.pirate.style.getEyesColor()
        self.skinColorIdx = self.pirate.style.getBodyColor()
        self.hairColorIdx = self.pirate.style.getHairColor()
        for shape in body_textures:
            for texName in shape:
                tex = self.bodyTextures.findTexture(texName)
                if tex:
                    self.texDict[texName] = tex
                else:
                    self.texDict[texName] = None

        for texName in face_textures:
            tex = self.bodyTextures.findTexture(texName)
            if tex:
                self.texDict[texName] = tex
            else:
                self.texDict[texName] = None

        for texName in face_textures:
            tex = self.faceTextures.findTexture(texName)
            if tex:
                self.faceTexturesSet.append(tex)
            else:
                self.notify.error('missing texture')

        return

    def setupClothing(self, lodName='2000'):
        geom = self.pirate.getGeomNode()
        self.clothing = self.pirate.findAllMatches('**/clothing_*')
        self.clothingsAcc = []
        self.clothingAccIdx = 0
        self.clothingsLayer1 = []
        self.clothingsLayer2 = []
        self.clothingsLayer3 = []
        self.clothingsShirt = []
        self.clothingShirtIdx = 0
        self.clothingShirtTexture = 0
        self.clothingsVest = []
        self.clothingVestIdx = 0
        self.clothingVestTexture = 0
        self.clothingsCoat = []
        self.clothingCoatIdx = 0
        self.clothingCoatTexture = 0
        self.clothingsPant = []
        self.clothingPantIdx = 0
        self.clothingPantTexture = 0
        self.clothingsBelt = []
        self.clothingBeltIdx = 0
        self.clothingBeltTexture = 0
        self.clothingsSock = []
        self.clothingSockIdx = 0
        self.clothingSockTexture = 0
        self.clothingsShoe = []
        self.clothingShoeIdx = 0
        self.clothingShoeTexture = 0
        self.clothingsHat = []
        self.clothingHatIdx = 0
        self.clothingHatTexture = 0
        self.partLayer = {}
        layer1List = [
         '**/clothing_layer1_shirt_common_open_base', '**/clothing_layer1_shirt_common_bottom_open_base', '**/clothing_layer1_shirt_common_closed_base', '**/clothing_layer1_shirt_common_closed_front', '**/clothing_layer1_shirt_common_bottom_out_closed_base', '**/clothing_layer1_shirt_common_bottom_out_closed_front', '**/clothing_layer1_shirt_common_bottom_in_closed_base', '**/clothing_layer1_shirt_common_bottom_in_closed_front', '**/clothing_layer1_shirt_common_collar_square', '**/clothing_layer1_shirt_common_collar_v_high1', '**/clothing_layer1_shirt_common_collar_v_high2', '**/clothing_layer1_shirt_common_collar_v_low', '**/clothing_layer1_shirt_common_veryshort_sleeve', '**/clothing_layer1_shirt_common_short_sleeve', '**/clothing_layer1_shirt_common_long_straight_sleeve', '**/clothing_layer1_shirt_common_long_puffy_sleeve', '**/clothing_layer1_pant_tucked_*', '**/clothing_layer1_pant_untucked_*', '**/clothing_layer1_pant_shorts_*', '**/clothing_layer1_pant_short_*', '**/clothing_layer1_pant_navy*', '**/clothing_layer1_pant_eitc*', '**/clothing_layer1_shoe_none_*', '**/clothing_layer1_shoe_boot_tall_*', '**/clothing_layer1_shoe_boot_short_*', '**/clothing_layer1_shoe_boot_cuff_*', '**/clothing_layer1_shoe_navy*', '**/clothing_layer1_shoe_india_navy*', '**/clothing_layer1_shirt_apron', '**/clothing_layer1_pant_apron', '**/clothing_layer1_pant_apron_skirt', '**/clothing_layer1_hat_captain;+s', '**/clothing_layer1_hat_tricorn;+s', '**/clothing_layer1_hat_navy;+s', '**/clothing_layer1_hat_india_navy;+s', '**/clothing_layer1_hat_admiral;+s', '**/clothing_layer1_hat_bandanna_full;+s', '**/clothing_layer1_hat_bandanna_reg*;+s', '**/clothing_layer1_hat_band_beanie;+s', '**/clothing_layer1_hat_barbossa;+s', '**/clothing_layer1_hat_barbossa_feather;+s', '**/clothing_layer1_hat_french;+s', '**/clothing_layer1_hat_french_feather;+s', '**/clothing_layer1_hat_spanish;+s', '**/clothing_layer1_hat_spanish_feather;+s', '**/clothing_layer1_hat_french_1;+s', '**/clothing_layer1_hat_french_2;+s', '**/clothing_layer1_hat_french_3;+s', '**/clothing_layer1_hat_spanish_1;+s', '**/clothing_layer1_hat_spanish_2;+s', '**/clothing_layer1_hat_spanish_3;+s', '**/clothing_layer1_hat_land_1;+s', '**/clothing_layer1_hat_land_2;+s', '**/clothing_layer1_hat_land_3;+s', '**/clothing_layer1_hat_holiday;+s', '**/clothing_layer1_hat_party_1;+s', '**/clothing_layer1_hat_party_2;+s', '**/clothing_layer1_hat_GM;+s', '**/clothing_layer1_shirt_common_collar_v_high3']
        self.layer1LODs = []
        for item in layer1List:
            itemInfo = {}
            for lod in ['500', '1000', '2000']:
                itemInfo[lod] = self.pirate.getLOD(lod).findAllMatches(item)

            self.layer1LODs.append(itemInfo)

        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_open_base'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_bottom_open_base'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_closed_base'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_closed_front'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_bottom_out_closed_base'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_bottom_out_closed_front'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_bottom_in_closed_base'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_bottom_in_closed_front'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_collar_square'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_collar_v_high1'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_collar_v_high2'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_collar_v_low'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_veryshort_sleeve'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_short_sleeve'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_long_straight_sleeve'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_long_puffy_sleeve'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_tucked_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_untucked_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_shorts_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_short_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_navy*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_eitc*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_none_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_boot_tall_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_boot_short_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_boot_cuff_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_navy*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_india_navy*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_apron'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_apron'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_apron_skirt'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_captain;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_tricorn;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_navy;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_india_navy;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_admiral;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_bandanna_full;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_bandanna_reg;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_band_beanie;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_barbossa;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_barbossa_feather;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_french;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_french_feather;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_spanish;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_spanish_feather;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_french_1;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_french_2;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_french_3;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_spanish_1;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_spanish_2;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_spanish_3;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_land_1;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_land_2;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_land_3;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_holiday;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_party_1;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_party_2;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_GM;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_collar_v_high3'))
        self.partLayer['SHIRT'] = self.clothingsLayer1
        self.partLayer['PANT'] = self.clothingsLayer1
        self.partLayer['SHOE'] = self.clothingsLayer1
        self.partLayer['HAT'] = self.clothingsLayer1
        self.clothesTextures = loader.loadModel('models/misc/male_clothes.bam')
        self.clothingsShirt.append([[]])
        self.clothingsShirt.append([[2, 3, 4, 5, 9], -1, -2, -3, -4, -5])
        self.clothingsShirt.append([[2, 3, 4, 5, 9], -1, -2, -3, -4, -5])
        self.clothingsShirt.append([[2, 3, 4, 5, 10, 13], -1, -2, -3, -4, -5, -8, -9, -10, -11])
        self.clothingsShirt.append([[2, 3, 4, 5, 9, 13], -1, -2, -3, -4, -5, -8, -9, -10, -11])
        self.clothingsShirt.append([[0, 1, 13], -1, -2, -8, -9, -10, -11])
        self.clothingsShirt.append([[2, 3, 4, 5, 11, 15], -1, -2, -3, -8, -9, -10, -11, -12, -13])
        self.clothingsShirt.append([[2, 3, 4, 5, 9, 14], -1, -2, -3, -4, -5, -8, -9, -10, -11, -12, -13])
        self.clothingsShirt.append([[0, 1, 14], -1, -2, -8, -9, -10, -11, -12, -13])
        self.clothingsShirt.append([[28], -1, -2, -3, -4, -8, -9, -10, -11])
        self.clothingsShirt.append([[2, 3, 4, 5, 9, 14], -1, -2, -3, -4, -5, -8, -9, -10, -11, -12, -13])
        self.clothingsShirt.append([[2, 3, 4, 5, 10, 15], -1, -2, -3, -4, -5, -6, -8, -9, -10, -11, -12, -13])
        self.clothingsShirt.append([[2, 3, 4, 5, 15, 58], -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13])
        self.clothingsHat.append([[]])
        self.clothingsHat.append([[31]])
        self.clothingsHat.append([[32]])
        self.clothingsHat.append([[33]])
        self.clothingsHat.append([[34]])
        self.clothingsHat.append([[35]])
        self.clothingsHat.append([[36]])
        self.clothingsHat.append([[37]])
        self.clothingsHat.append([[38]])
        self.clothingsHat.append([[39, 40]])
        self.clothingsHat.append([[41, 42]])
        self.clothingsHat.append([[43, 44]])
        self.clothingsHat.append([[45]])
        self.clothingsHat.append([[46]])
        self.clothingsHat.append([[47]])
        self.clothingsHat.append([[48]])
        self.clothingsHat.append([[49]])
        self.clothingsHat.append([[50]])
        self.clothingsHat.append([[51]])
        self.clothingsHat.append([[52]])
        self.clothingsHat.append([[53]])
        self.clothingsHat.append([[54]])
        self.clothingsHat.append([[55]])
        self.clothingsHat.append([[56]])
        self.clothingsHat.append([[57]])
        self.clothingsPant.append([[16], -6, -7, -16, -17])
        self.clothingsPant.append([[17], -6, -7, -16, -17])
        self.clothingsPant.append([[18], -6, -7])
        self.clothingsPant.append([[19], -6, -7])
        self.clothingsPant.append([[20], -6, -7, -16, -17, -18, -19, -20, -21])
        self.clothingsPant.append([[21], -6, -7, -16, -17, -18, -19, -20, -21])
        self.clothingsPant.append([[30, 29], -6, -7, -16, -17, -18, -19])
        self.clothingsShoe.append([[22]])
        self.clothingsShoe.append([[23], -18, -19, -20, -21])
        self.clothingsShoe.append([[24], -20, -21])
        self.clothingsShoe.append([[26], -18, -19, -20, -21])
        self.clothingsShoe.append([[27], -18, -19, -20, -21])
        self.clothingsShoe.append([[25], -20, -21, -18, -19])
        layer2List = [
         '**/clothing_layer2_vest_none*', '**/clothing_layer2_vest_open*', '**/clothing_layer2_vest_closed*', '**/clothing_layer2_vest_long_closed*', '**/clothing_layer2_belt_none*', '**/clothing_layer2_belt_sash_reg_base', '**/clothing_layer2_belt_sash_reg_front', '**/clothing_layer2_belt_oval', '**/clothing_layer2_belt_buckle_oval', '**/clothing_layer2_belt_square', '**/clothing_layer2_belt_buckle_square']
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_vest_none*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_vest_open*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_vest_closed*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_vest_long_closed*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_none*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_sash_reg_base'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_sash_reg_front'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_oval'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_buckle_oval'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_square'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_buckle_square'))
        self.partLayer['VEST'] = self.clothingsLayer2
        self.partLayer['BELT'] = self.clothingsLayer2
        self.clothingsVest.append([[0]])
        self.clothingsVest.append([[1], -1, -2])
        self.clothingsVest.append([[2], -1, -2, -3])
        self.clothingsVest.append([[3], -1, -2, -3])
        self.clothingsBelt.append([[4]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[7, 8]])
        self.clothingsBelt.append([[7, 8]])
        self.clothingsBelt.append([[9, 10]])
        self.clothingsBelt.append([[7, 8]])
        self.clothingsBelt.append([[7, 8]])
        self.clothingsBelt.append([[7, 8]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[7, 8]])
        self.clothingsBelt.append([[7, 8]])
        self.clothingsBelt.append([[9, 10]])
        self.clothingsBelt.append([[9, 10]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[9, 10]])
        self.clothingsBelt.append([[9, 10]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[5, 6]])
        self.clothingsBelt.append([[9, 10]])
        self.clothingsBelt.append([[9, 10]])
        self.clothingsBelt.append([[9, 10]])
        self.clothingsBelt.append([[9, 10]])
        self.clothingsLayer3.append(geom.findAllMatches('**/clothing_layer3_coat_none*'))
        self.clothingsLayer3.append(geom.findAllMatches('**/clothing_layer3_coat_long*'))
        self.clothingsLayer3.append(geom.findAllMatches('**/clothing_layer3_coat_short*'))
        self.clothingsLayer3.append(geom.findAllMatches('**/clothing_layer3_coat_navy*'))
        self.clothingsLayer3.append(geom.findAllMatches('**/clothing_layer3_coat_eitc*'))
        layer3List = [
         '**/clothing_layer3_coat_none*', '**/clothing_layer3_coat_long*', '**/clothing_layer3_coat_short*', '**/clothing_layer3_coat_navy*', '**/clothing_layer3_coat_eitc*']
        if base.config.GetBool('want-gen-pics-buttons'):
            self.clothesByType = {'SHIRT': self.clothingsLayer1[:16] + self.clothingsLayer1[28:29],'VEST': self.clothingsLayer2[:4],'PANT': self.clothingsLayer1[16:22] + self.clothingsLayer1[29:30],'COAT': self.clothingsLayer3,'BELT': self.clothingsLayer2[4:],'SHOE': self.clothingsLayer1[22:28],'HAT': self.clothingsLayer1[31:]}
        self.partLayer['COAT'] = self.clothingsLayer3
        self.clothingsCoat.append([[0]])
        self.clothingsCoat.append([[1], -1, -2, -8, -9, -10, -11, -12, -13])
        self.clothingsCoat.append([[2], -1, -2, -8, -9, -10, -11, -12, -13])
        self.clothingsCoat.append([[3], -1, -2, -3, -4, -5, -8, -9, -10, -11, -12, -13])
        self.clothingsCoat.append([[4], -1, -2, -3, -4, -5, -8, -9, -10, -11, -12, -13])
        for type in clothes_textures.values():
            for model in type:
                for texInfo in model:
                    textures = texInfo[0].split('+')
                    for texName in textures:
                        tex = self.clothesTextures.findTexture(texName)
                        if tex:
                            self.texDict[texName] = tex
                        else:
                            self.texDict[texName] = None

        self.texDict['PM_none'] = None
        if self.newAvatars:
            self.generateShirtSets()
            self.generatePantSets()
            self.generateShoeSets()
            self.layer2LODs = []
            for item in layer2List:
                itemInfo = {}
                for lod in ['500', '1000', '2000']:
                    itemInfo[lod] = self.pirate.getLOD(lod).findAllMatches(item)

                self.layer2LODs.append(itemInfo)

            self.generateVestSets()
            self.generateBeltSets()
            self.layer3LODs = []
            for item in layer3List:
                itemInfo = {}
                for lod in ['500', '1000', '2000']:
                    itemInfo[lod] = self.pirate.getLOD(lod).findAllMatches(item)

                self.layer3LODs.append(itemInfo)

            self.generateCoatSets()
        self.generateHatSets()
        self.clothing.stash()
        return

    def setupSelectionChoices(self, type, versionFilter=None, rarityFilter=None, isFromLoot=True, isFromShop=True, isFromQuest=True, isFromPromo=True, isFromPVP=True, isFromNPC=True, holidayFilter=None):
        data = ClothingGlobals.SELECTION_CHOICES.get(type, None)
        if not data:
            return
        choices = data['MALE']
        self.choices = {}
        self.choices['FACE'] = choices.get('FACE', [])
        self.choices['HAIR'] = choices.get('HAIR', [])
        self.choices['BEARD'] = choices.get('BEARD', [])
        self.choices['MUSTACHE'] = choices.get('MUSTACHE', [])
        if type == 'DEFAULT':
            mapClothing = DropGlobals.getMakeAPirateClothing()
        else:
            mapClothing = ItemGlobals.getAllClothingIds(gender='m')
        hats = ItemGlobals.getGenderType(ItemGlobals.HAT, 'm', mapClothing)
        choiceHats = {}
        for hatId in hats:
            modelId = ItemGlobals.getMaleModelId(hatId)
            texId = ItemGlobals.getMaleTextureId(hatId)
            canDyeItem = ItemGlobals.canDyeItem(hatId)
            toBeAdded = True
            if versionFilter is not None:
                toBeAdded = ItemGlobals.getVersion(hatId) == versionFilter
            if toBeAdded and rarityFilter is not None:
                toBeAdded = ItemGlobals.getRarity(hatId) == rarityFilter
            if toBeAdded and holidayFilter is not None:
                toBeAdded = ItemGlobals.getHoliday(hatId) == holidayFilter
            toBeAdded &= isFromLoot and ItemGlobals.isFromLoot(hatId) or isFromShop and ItemGlobals.isFromShop(hatId) or isFromQuest and ItemGlobals.isFromQuest(hatId) or isFromPromo and ItemGlobals.isFromPromo(hatId) or isFromPVP and ItemGlobals.isFromPVP(hatId) or isFromNPC and ItemGlobals.isFromNPC(hatId)
            if toBeAdded:
                choiceHats[hatId] = [
                 modelId, texId, canDyeItem]

        choiceHats[0] = [
         0, 0, 0]
        self.choices['HAT'] = choiceHats
        shirts = ItemGlobals.getGenderType(ItemGlobals.SHIRT, 'm', mapClothing)
        choiceShirts = {}
        for shirtId in shirts:
            modelId = ItemGlobals.getMaleModelId(shirtId)
            texId = ItemGlobals.getMaleTextureId(shirtId)
            canDyeItem = ItemGlobals.canDyeItem(shirtId)
            toBeAdded = True
            if versionFilter is not None:
                toBeAdded = ItemGlobals.getVersion(shirtId) == versionFilter
            if toBeAdded and rarityFilter is not None:
                toBeAdded = ItemGlobals.getRarity(shirtId) == rarityFilter
            if toBeAdded and holidayFilter is not None:
                toBeAdded = ItemGlobals.getHoliday(shirtId) == holidayFilter
            toBeAdded &= isFromLoot and ItemGlobals.isFromLoot(shirtId) or isFromShop and ItemGlobals.isFromShop(shirtId) or isFromQuest and ItemGlobals.isFromQuest(shirtId) or isFromPromo and ItemGlobals.isFromPromo(shirtId) or isFromPVP and ItemGlobals.isFromPVP(shirtId) or isFromNPC and ItemGlobals.isFromNPC(shirtId)
            if toBeAdded:
                choiceShirts[shirtId] = [
                 modelId, texId, canDyeItem]

        if type == 'NPC':
            choiceShirts[0] = [
             0, 0, 0]
        self.choices['SHIRT'] = choiceShirts
        vests = ItemGlobals.getGenderType(ItemGlobals.VEST, 'm', mapClothing)
        choiceVests = {}
        for vestId in vests:
            modelId = ItemGlobals.getMaleModelId(vestId)
            texId = ItemGlobals.getMaleTextureId(vestId)
            canDyeItem = ItemGlobals.canDyeItem(vestId)
            toBeAdded = True
            if versionFilter is not None:
                toBeAdded = ItemGlobals.getVersion(vestId) == versionFilter
            if toBeAdded and rarityFilter is not None:
                toBeAdded = ItemGlobals.getRarity(vestId) == rarityFilter
            if toBeAdded and holidayFilter is not None:
                toBeAdded = ItemGlobals.getHoliday(vestId) == holidayFilter
            toBeAdded &= isFromLoot and ItemGlobals.isFromLoot(vestId) or isFromShop and ItemGlobals.isFromShop(vestId) or isFromQuest and ItemGlobals.isFromQuest(vestId) or isFromPromo and ItemGlobals.isFromPromo(vestId) or isFromPVP and ItemGlobals.isFromPVP(vestId) or isFromNPC and ItemGlobals.isFromNPC(vestId)
            if toBeAdded:
                choiceVests[vestId] = [
                 modelId, texId, canDyeItem]

        choiceVests[0] = [
         0, 0, 0]
        self.choices['VEST'] = choiceVests
        coats = ItemGlobals.getGenderType(ItemGlobals.COAT, 'm', mapClothing)
        choiceCoats = {}
        for coatId in coats:
            modelId = ItemGlobals.getMaleModelId(coatId)
            texId = ItemGlobals.getMaleTextureId(coatId)
            canDyeItem = ItemGlobals.canDyeItem(coatId)
            toBeAdded = True
            if versionFilter is not None:
                toBeAdded = ItemGlobals.getVersion(coatId) == versionFilter
            if toBeAdded and rarityFilter is not None:
                toBeAdded = ItemGlobals.getRarity(coatId) == rarityFilter
            if toBeAdded and holidayFilter is not None:
                toBeAdded = ItemGlobals.getHoliday(coatId) == holidayFilter
            toBeAdded &= isFromLoot and ItemGlobals.isFromLoot(coatId) or isFromShop and ItemGlobals.isFromShop(coatId) or isFromQuest and ItemGlobals.isFromQuest(coatId) or isFromPromo and ItemGlobals.isFromPromo(coatId) or isFromPVP and ItemGlobals.isFromPVP(coatId) or isFromNPC and ItemGlobals.isFromNPC(coatId)
            if toBeAdded:
                choiceCoats[coatId] = [
                 modelId, texId, canDyeItem]

        choiceCoats[0] = [
         0, 0, 0]
        self.choices['COAT'] = choiceCoats
        pants = ItemGlobals.getGenderType(ItemGlobals.PANT, 'm', mapClothing)
        choicePants = {}
        for pantId in pants:
            modelId = ItemGlobals.getMaleModelId(pantId)
            texId = ItemGlobals.getMaleTextureId(pantId)
            canDyeItem = ItemGlobals.canDyeItem(pantId)
            toBeAdded = True
            if versionFilter is not None:
                toBeAdded = ItemGlobals.getVersion(pantId) == versionFilter
            if toBeAdded and rarityFilter is not None:
                toBeAdded = ItemGlobals.getRarity(pantId) == rarityFilter
            if toBeAdded and holidayFilter is not None:
                toBeAdded = ItemGlobals.getHoliday(pantId) == holidayFilter
            toBeAdded &= isFromLoot and ItemGlobals.isFromLoot(pantId) or isFromShop and ItemGlobals.isFromShop(pantId) or isFromQuest and ItemGlobals.isFromQuest(pantId) or isFromPromo and ItemGlobals.isFromPromo(pantId) or isFromPVP and ItemGlobals.isFromPVP(pantId) or isFromNPC and ItemGlobals.isFromNPC(pantId)
            if toBeAdded:
                choicePants[pantId] = [
                 modelId, texId, canDyeItem]

        if type == 'NPC':
            choicePants[0] = [
             0, 0, 0]
        self.choices['PANT'] = choicePants
        belts = ItemGlobals.getGenderType(ItemGlobals.BELT, 'm', mapClothing)
        choiceBelts = {}
        for beltId in belts:
            modelId = ItemGlobals.getMaleModelId(beltId)
            texId = ItemGlobals.getMaleTextureId(beltId)
            canDyeItem = ItemGlobals.canDyeItem(beltId)
            toBeAdded = True
            if versionFilter is not None:
                toBeAdded = ItemGlobals.getVersion(beltId) == versionFilter
            if toBeAdded and rarityFilter is not None:
                toBeAdded = ItemGlobals.getRarity(beltId) == rarityFilter
            if toBeAdded and holidayFilter is not None:
                toBeAdded = ItemGlobals.getHoliday(beltId) == holidayFilter
            toBeAdded &= isFromLoot and ItemGlobals.isFromLoot(beltId) or isFromShop and ItemGlobals.isFromShop(beltId) or isFromQuest and ItemGlobals.isFromQuest(beltId) or isFromPromo and ItemGlobals.isFromPromo(beltId) or isFromPVP and ItemGlobals.isFromPVP(beltId) or isFromNPC and ItemGlobals.isFromNPC(beltId)
            if toBeAdded:
                choiceBelts[beltId] = [
                 modelId, texId, canDyeItem]

        choiceBelts[0] = [
         0, 0, 0]
        self.choices['BELT'] = choiceBelts
        shoes = ItemGlobals.getGenderType(ItemGlobals.SHOE, 'm', mapClothing)
        choiceShoes = {}
        for shoeId in shoes:
            modelId = ItemGlobals.getMaleModelId(shoeId)
            texId = ItemGlobals.getMaleTextureId(shoeId)
            canDyeItem = ItemGlobals.canDyeItem(shoeId)
            toBeAdded = True
            if versionFilter is not None:
                toBeAdded = ItemGlobals.getVersion(shoeId) == versionFilter
            if toBeAdded and rarityFilter is not None:
                toBeAdded = ItemGlobals.getRarity(shoeId) == rarityFilter
            if toBeAdded and holidayFilter is not None:
                toBeAdded = ItemGlobals.getHoliday(shoeId) == holidayFilter
            toBeAdded &= isFromLoot and ItemGlobals.isFromLoot(shoeId) or isFromShop and ItemGlobals.isFromShop(shoeId) or isFromQuest and ItemGlobals.isFromQuest(shoeId) or isFromPromo and ItemGlobals.isFromPromo(shoeId) or isFromPVP and ItemGlobals.isFromPVP(shoeId) or isFromNPC and ItemGlobals.isFromNPC(shoeId)
            if toBeAdded:
                choiceShoes[shoeId] = [
                 modelId, texId, canDyeItem]

        choiceShoes[0] = [
         0, 0, 0]
        self.choices['SHOE'] = choiceShoes
        return

    def setClothesTexture(self, tex, listParts, layer, color=None):
        for i in range(0, len(listParts)):
            parts = layer[listParts[i]]
            if tex:
                parts.setTexture(tex, 1)
            if color:
                parts.setColorScale(color)

    def setPartTexture(self, part, geomIdx, texIdx, pieces):
        numParts = len(clothes_textures[part])
        if numParts == 0:
            return
        if geomIdx >= numParts:
            self.notify.warning('part (%s) geom index (%s), capping it (%s)' % (part, geomIdx, numParts - 1))
            geomIdx = numParts - 1
        numTextures = len(clothes_textures[part][geomIdx])
        if numTextures == 0:
            return
        if texIdx >= numTextures:
            self.notify.warning('part (%s) texture index (%s) out of range (%s), capping it (%s)' % (part, geomIdx, texIdx, numTextures - 1))
            texIdx = numTextures - 1
        texture = clothes_textures[part][geomIdx][texIdx]
        texName = texture[0].split('+')
        lowLODColor = texture[1]
        if len(texName) > 1:
            tex = self.texDict[texName[0]]
            self.setClothesTexture(tex, [pieces[0]], self.partLayer[part], lowLODColor)
            tex = self.texDict[texName[1]]
            self.setClothesTexture(tex, [pieces[1]], self.partLayer[part], lowLODColor)
        else:
            tex = self.clothesTextures.findTexture(texName[0])
            self.setClothesTexture(tex, pieces, self.partLayer[part], lowLODColor)

    def getTextureName(self, partIdx, idx, texIdx):
        try:
            return clothes_textures[partIdx][idx][texIdx]
        except:
            return None

        return None

    def handleJewelryHiding(self):
        jewelryDNA = {'LEar': self.pirate.style.getJewelryZone1(),'REar': self.pirate.style.getJewelryZone2(),'LBrow': self.pirate.style.getJewelryZone3(),'RBrow': self.pirate.style.getJewelryZone4(),'Nose': self.pirate.style.getJewelryZone5(),'Mouth': self.pirate.style.getJewelryZone6(),'LHand': self.pirate.style.getJewelryZone7(),'RHand': self.pirate.style.getJewelryZone8()}
        for key in self.currentJewelry.keys():
            primaryColor = HumanDNA.jewelryColors[jewelryDNA[key][1]]
            secondaryColor = HumanDNA.jewelryColors[jewelryDNA[key][2]]
            oldIdx = self.currentJewelry[key][0]
            newIdx = jewelryDNA[key][0]
            for np in self.jewelrySets[key][oldIdx]:
                np.stash()

            for npIdx in range(len(self.jewelrySets[key][newIdx])):
                np = self.jewelrySets[key][newIdx][npIdx]
                np.unstash()
                if npIdx == 0 and primaryColor:
                    np.setColor(primaryColor)
                elif secondaryColor:
                    np.setColor(secondaryColor)

            self.currentJewelry[key] = jewelryDNA[key]

    def handleClothesHiding(self):
        if not self.newAvatars:
            self.handleClothesHidingOld()
            self.setupTattoos()
            return
        if self.pirate.zombie and 0:
            dna = self.dnaZomb
        else:
            dna = self.pirate.style
        shirtIdx = dna.getClothesShirt()
        vestIdx = dna.getClothesVest()
        coatIdx = dna.getClothesCoat()
        pantIdx = dna.getClothesPant()
        beltIdx = dna.getClothesBelt()
        shoeIdx = dna.getClothesShoe()
        hatIdx = dna.getClothesHat()
        if self.pirate.zombie:
            shirtIdx = self.dnaZomb.getClothesShirt()
            pantIdx = self.dnaZomb.getClothesPant()
        hairIdx = [dna.getHairHair(), dna.getHairColor()]
        if beltIdx[0] != 0:
            style1 = 'belt'
        else:
            style1 = 'nobelt'
        if vestIdx[0] != 3:
            stylePant = style1
        else:
            stylePant = 'belt'
        layerPant = self.clothingsPant[pantIdx[0]]
        layerShoe = self.clothingsShoe[shoeIdx[0]]
        layerShirt = self.clothingsShirt[shirtIdx[0]]
        layerShirtModified = [[]] + layerShirt[1:]
        for elem in layerShirt[0]:
            if beltIdx[0] != 0:
                if elem == 4:
                    elem = 6
                elif elem == 5:
                    elem = 7
                layerShirtModified[0].append(elem)

        layerVest = self.clothingsVest[vestIdx[0]]
        layerBelt = self.clothingsBelt[beltIdx[0]]
        layerCoat = self.clothingsCoat[coatIdx[0]]
        currentVest = self.vestSets[vestIdx[0]][style1]['full']
        currentShirt = self.shirtSets[shirtIdx[0]][style1]['full']
        currentCoat = self.coatSets[coatIdx[0]]
        currentBelt = self.beltSets[beltIdx[0]]['full']
        currentPant = self.pantSets[pantIdx[0]][stylePant]
        currentShoe = self.shoeSets[shoeIdx[0]]
        if coatIdx[0] > 0:
            if coatIdx[0] in [3, 4]:
                currentVest = self.vestSets[vestIdx[0]]['nobelt']['covered']
                currentShirt = self.shirtSets[vestIdx[0]]['nobelt']['covered']
                currentBelt = self.beltSets[beltIdx[0]]['covered']
            else:
                if coatIdx[0] == 2 and vestIdx[0] == 3:
                    currentVest = self.vestSets[vestIdx[0]][style1]['coatSpecial']
                elif vestIdx[0] > 0:
                    currentVest = self.vestSets[vestIdx[0]][style1]['coat']
                if vestIdx[0] > 1:
                    currentShirt = self.shirtSets[shirtIdx[0]][style1]['coat+closedVest']
                else:
                    currentShirt = self.shirtSets[shirtIdx[0]][style1]['coat']
                currentBelt = self.beltSets[beltIdx[0]]['coat']
        elif vestIdx[0] > 1:
            currentShirt = self.shirtSets[shirtIdx[0]][style1]['closedVest']
        elif vestIdx[0] > 0:
            currentShirt = self.shirtSets[shirtIdx[0]][style1]['openVest']
        self.currentClothingModels['SHIRT'].stash()
        currentShirt.unstash()
        clothingList = clothes_textures['SHIRT'][shirtIdx[0]]
        textureIndex = shirtIdx[1]
        if textureIndex < len(clothingList):
            texInfo = clothingList[textureIndex]
        else:
            print 'PirateMale->Shirt texture out of range! Setting to 0\n  Texture list %s index %s' % (clothingList, textureIndex)
            texInfo = clothingList[0]
        if self.texDict[texInfo[0]]:
            currentShirt.setTexture(self.texDict[texInfo[0]])
            shirtColor = dna.lookupClothesTopColor()[0]
            currentShirt.setColorScale(shirtColor)
        self.currentClothingModels['SHIRT'] = currentShirt
        self.currentClothingModels['VEST'].stash()
        texInfo = clothes_textures['VEST'][vestIdx[0]][vestIdx[1]]
        currentVest.unstash()
        self.currentClothingModels['VEST'] = currentVest
        if self.texDict[texInfo[0]]:
            vestColor = dna.lookupClothesTopColor()[1]
            currentVest.setTexture(self.texDict[texInfo[0]])
            currentVest.setColorScale(vestColor)
        self.currentClothingModels['COAT'].stash()
        texInfo = clothes_textures['COAT'][coatIdx[0]][coatIdx[1]]
        currentCoat.unstash()
        self.currentClothingModels['COAT'] = currentCoat
        if self.texDict[texInfo[0]]:
            coatColor = dna.lookupClothesTopColor()[2]
            currentCoat.setTexture(self.texDict[texInfo[0]])
            currentCoat.setColorScale(coatColor)
        self.handleHeadHiding()
        self.currentClothingModels['BELT'][0].stash()
        self.currentClothingModels['BELT'][1].stash()
        texInfo = clothes_textures['BELT'][beltIdx[0]][beltIdx[1]]
        currentBelt[0].unstash()
        currentBelt[1].unstash()
        texNames = texInfo[0].split('+')
        self.currentClothingModels['BELT'] = currentBelt
        if len(texNames) > 1:
            tex1 = self.texDict[texNames[0]]
            tex2 = self.texDict[texNames[1]]
            if tex1:
                currentBelt[0].setTexture(tex1)
            if tex2:
                currentBelt[1].setTexture(tex2)
        else:
            tex1 = self.texDict[texNames[0]]
            if tex1:
                currentBelt[0].setTexture(tex1)
                currentBelt[1].setTexture(tex1)
        beltColor = dna.lookupClothesBotColor()[1]
        for i in [0, 1]:
            currentBelt[i].setColorScale(beltColor)

        self.currentClothingModels['PANT'].stash()
        clothingList = clothes_textures['PANT'][pantIdx[0]]
        textureIndex = pantIdx[1]
        if textureIndex < len(clothingList):
            texInfo = clothingList[textureIndex]
        else:
            print 'PirateMale->Pant Texture out of range! Setting to 0\n  TextureList %s index %s' % (clothingList, textureIndex)
            texInfo = clothingList[0]
        currentPant.unstash()
        self.currentClothingModels['PANT'] = currentPant
        if self.texDict[texInfo[0]]:
            pantColor = dna.lookupClothesBotColor()[0]
            currentPant.setTexture(self.texDict[texInfo[0]])
            currentPant.setColorScale(pantColor)
        self.currentClothingModels['SHOE'].stash()
        if pantIdx[0] != 4 and pantIdx[0] != 5:
            currentShoe.unstash()
        texInfo = clothes_textures['SHOE'][shoeIdx[0]][shoeIdx[1]]
        if self.texDict[texInfo[0]]:
            currentShoe.setTexture(self.texDict[texInfo[0]])
        self.currentClothingModels['SHOE'] = currentShoe
        bodySet = [set(), set(), set()]
        for partSet in [layerShirtModified, layerVest, layerCoat, layerPant, layerShoe, layerBelt]:
            for i in partSet[1:]:
                bodySet[self.bodyPiecesToGroup[-i]].add(-i)

        bodyList = [ list(x) for x in bodySet ]
        for pieces in bodyList:
            pieces.sort()

        bodyTuple = [ tuple(x) for x in bodyList ]
        for i in xrange(3):
            if bodyTuple[i] not in self.bodySets[i]:
                flattenedSet = NodePathCollection()
                for lod in self.pirate.getLODNames():
                    flattenMe = NodePath('flattenMe')
                    for j in self.groupsToBodyPieces[i]:
                        if j not in bodySet[i]:
                            self.layerBodyLODs[j][lod].copyTo(flattenMe)

                    flattenMe.flattenStrong()
                    lodParts = flattenMe.findAllMatches('**/+GeomNode')
                    self.stripTexture(lodParts)
                    lodParts.reparentTo(self.pirate.getLOD(lod).getChild(0))
                    flattenedSet.addPathsFrom(lodParts)

                self.bodySets[i][bodyTuple[i]] = flattenedSet

        if self.pirate.zombie:
            bodyTexIdx = ZOMB_BODY_TEXTURE
        else:
            bodyTexIdx = 0
        tex = self.texDict[body_textures[self.pirate.style.getBodyShape()][bodyTexIdx]]
        currentBody = NodePathCollection()
        currentChest = self.bodySets[0][bodyTuple[0]]
        currentLeftArm = self.bodySets[1][bodyTuple[1]]
        currentRightArm = self.bodySets[2][bodyTuple[2]]
        currentBody.addPathsFrom(currentChest)
        currentBody.addPathsFrom(currentLeftArm)
        currentBody.addPathsFrom(currentRightArm)
        if tex:
            currentBody.setTexture(tex)
        if self.pirate.zombie:
            skinColor = VBase4(1, 1, 1, 1)
        if hasattr(self.pirate, 'crazyColorSkin') and self.pirate.crazyColorSkin == True:
            i = self.pirate.getCrazyColorSkinIndex()
            skinColor = HumanDNA.crazySkinColors[i]
        else:
            skinColor = self.pirate.style.getSkinColor()
        self.faces[0].setColorScale(skinColor)
        currentBody.setColorScale(skinColor)
        self.currentBody.stash()
        currentBody.unstash()
        self.currentBody = currentBody
        self.currentTattooZones = [currentChest, currentLeftArm, currentRightArm, self.faces[0]]
        self.setupTattoos()

    def handleClothesHidingOld(self):
        self.clothing.stash()
        self.body.unstash()
        if self.pirate.zombie:
            dna = self.dnaZomb
        else:
            dna = self.pirate.style
        shirtIdx = dna.getClothesShirt()
        vestIdx = dna.getClothesVest()
        coatIdx = dna.getClothesCoat()
        pantIdx = dna.getClothesPant()
        beltIdx = dna.getClothesBelt()
        shoeIdx = dna.getClothesShoe()
        hatIdx = dna.getClothesHat()
        layerPant = self.clothingsPant[pantIdx[0]]
        parts = NodePathCollection()
        if self.clothesTextures != None:
            if pantIdx[0] == 6:
                self.setPartTexture('PANT', pantIdx[0], pantIdx[1], [layerPant[0][1]])
            else:
                self.setPartTexture('PANT', pantIdx[0], pantIdx[1], layerPant[0])
        for j in range(0, len(layerPant[0])):
            parts = self.clothingsLayer1[layerPant[0][j]]
            if parts.getNumPaths():
                parts.unstash()

        self.handleLayer1Hiding(layerPant)
        if pantIdx[0] == 4 or pantIdx[0] == 5:
            layerShoe = self.clothingsShoe[0]
        else:
            layerShoe = self.clothingsShoe[shoeIdx[0]]
        parts = NodePathCollection()
        if self.clothesTextures != None:
            self.setPartTexture('SHOE', shoeIdx[0], shoeIdx[1], layerShoe[0])
        for j in range(0, len(layerShoe[0])):
            parts = self.clothingsLayer1[layerShoe[0][j]]
            if parts.getNumPaths():
                parts.unstash()

        self.handleLayer1Hiding(layerShoe)
        numShirts = len(self.clothingsShirt)
        myShirtIdx = shirtIdx[0]
        if myShirtIdx >= numShirts:
            self.notify.warning('shirt (%s) out of range, capping it (%s)' % (myShirtIdx, numShirts - 1))
            myShirtIdx = numShirts - 1
        layerShirt = self.clothingsShirt[myShirtIdx]
        parts = NodePathCollection()
        layerShirtModified = []
        layerShirt0Modified = []
        for elem in layerShirt[0]:
            if beltIdx[0] != 0:
                if elem == 4:
                    elem = 6
                elif elem == 5:
                    elem = 7
            layerShirt0Modified.append(elem)

        layerShirtModified.append(layerShirt0Modified)
        for elem in layerShirt[1:]:
            layerShirtModified.append(elem)

        if self.clothesTextures != None:
            self.setPartTexture('SHIRT', shirtIdx[0], shirtIdx[1], layerShirtModified[0])

        for j in range(0, len(layerShirtModified[0])):
            parts = self.clothingsLayer1[layerShirtModified[0][j]]
            if parts.getNumPaths():
                parts.unstash()

        if parts.getNumPaths():
            self.handleLayer1Hiding(layerShirtModified)
            if vestIdx[0] != 2:
                if shirtIdx[0] not in (5, 7, 8, 9):
                    self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'belt')

        layerVest = self.clothingsVest[vestIdx[0]]
        parts = NodePathCollection()
        if self.clothesTextures != None:
            self.setPartTexture('VEST', vestIdx[0], vestIdx[1], layerVest[0])

        for j in range(0, len(layerVest[0])):
            parts = self.clothingsLayer2[layerVest[0][j]]
            if parts.getNumPaths():
                parts.unstash()

        if parts.getNumPaths():
            if vestIdx[0] > 1:
                self.handleLayer2Hiding(self.clothingsLayer1, layerShirtModified, 'base', 'front', 'collar_v_low')
            else:
                self.handleLayer2Hiding(self.clothingsLayer1, layerShirtModified)
            self.handleLayer1Hiding(layerVest)

        self.handleHeadHiding()
        layerBelt = self.clothingsBelt[beltIdx[0]]
        parts = NodePathCollection()
        if self.clothesTextures != None:
            self.setPartTexture('BELT', beltIdx[0], beltIdx[1], layerBelt[0])

        for j in range(0, len(layerBelt[0])):
            parts = self.clothingsLayer2[layerBelt[0][j]]
            if parts.getNumPaths():
                parts.unstash()

        if parts.getNumPaths() or vestIdx[0] == 3:
            self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'belt')

        if parts.getNumPaths() and vestIdx[0] == 3:
            self.handleLayer2Hiding(self.clothingsLayer2, layerVest, 'belt')

        layerCoat = self.clothingsCoat[coatIdx[0]]
        parts = NodePathCollection()
        if self.clothesTextures != None:
            self.setPartTexture('COAT', coatIdx[0], coatIdx[1], layerCoat[0])
            
        for j in range(0, len(layerCoat[0])):
            parts = self.clothingsLayer3[layerCoat[0][j]]
            if parts.getNumPaths():
                parts.unstash()

        if parts.getNumPaths():
            if coatIdx[0] == 2 and vestIdx[0] == 3:
                self.handleLayer3Hiding(self.clothingsLayer2, layerVest, layerShirtModified, 'legs_base')
            else:
                self.handleLayer3Hiding(self.clothingsLayer2, layerVest, layerShirtModified)
            self.handleLayer2Hiding(self.clothingsLayer2, layerBelt)
            self.handleLayer1Hiding(layerCoat)
        self.pirate.generateColor()
        self.pirate.generateClothesColor()
        return

    def handleClothesGui(self, type, texIdx):
        clothing = self.currentClothing[type]
        if texIdx >= len(clothes_textures[type][clothing[0]]):
            self.currentClothing[type][1] = 0
        if texIdx < 0:
            self.currentClothing[type][1] = len(clothes_textures[type][clothing[0]]) - 1
        self.pirate.setClothesByType(type, clothing[0], clothing[1])
        self.handleClothesHiding()

    def getTextureChoices(self, clothesIdx):
        return clothes_textures[clothesIdx]

    def handleLayer1Hiding(self, element):
        parts = self.bodys
        for i in range(1, len(element)):
            idx = element[i]
            parts[-idx].stash()

    def handleLayer2Hiding(self, clothingLayer, layer1Element, hide1='base', hide2=None, hide3=None):
        for i in range(0, len(layer1Element[0])):
            idx = layer1Element[0][i]
            parts = clothingLayer[idx]
            for j in range(0, parts.getNumPaths()):
                if hide1 != None and parts[j].getName().find(hide1) != -1:
                    parts[j].stash()
                elif hide2 != None and parts[j].getName().find(hide2) != -1:
                    parts[j].stash()
                elif hide3 != None and parts[j].getName().find(hide3) != -1:
                    parts[j].stash()

        return

    def handleLayer3Hiding(self, clothingLayer, layer2Element, layer1Element, show1=None):
        for i in range(0, len(layer2Element[0])):
            parts = clothingLayer[layer2Element[0][i]]
            for j in range(0, parts.getNumPaths()):
                if parts[j].getName().find('front') < 0:
                    if show1:
                        if parts[j].getName().find(show1) < 0:
                            parts[j].stash()
                    else:
                        parts[j].stash()

        if layer1Element == None:
            return
        for i in range(0, len(layer1Element[0])):
            parts = self.clothingsLayer1[layer1Element[0][i]]
            for j in range(0, parts.getNumPaths()):
                if parts[j].getName().find('front') < 0:
                    if parts[j].getName().find('collar') < 0:
                        parts[j].stash()

        return

    def getTattooBaseTexture(self):
        return 'male_tattoomap'

    def handleTattooMapping(self):
        parts = self.body.getNumPaths()
        tex, scale = TattooGlobals.getTattooImage(0)
        for i in range(parts):
            self.body.getPath(i).setTexture(self.tattooStage, tex)

    def hideAllJewelry(self):
        self.jewelryLEarIdx = [0, 0, 0]
        self.jewelryREarIdx = [0, 0, 0]
        self.jewelryLBrowIdx = [0, 0, 0]
        self.jewelryRBrowIdx = [0, 0, 0]
        self.jewelryNoseIdx = [0, 0, 0]
        self.jewelryMouthIdx = [0, 0, 0]
        self.jewelryLHandIdx = [0, 0, 0]
        self.jewelryRHandIdx = [0, 0, 0]
        self.accFace.stash()
        self.accBody.stash()

    def handleJewelryOptions(self, key, increment=True):
        print 'handleJewelryOptions'
        options = jewelry_options[key]
        idx = self.currentJewelry[key][0]
        primaryColor = HumanDNA.jewelryColors[self.currentJewelry[key][1]]
        secondaryColor = HumanDNA.jewelryColors[self.currentJewelry[key][2]]
        self.jewelrySets[key][idx][0].stash()
        self.jewelrySets[key][idx][1].stash()
        if increment:
            idx += 1
            length = len(self.jewelrySets[key])
            if idx >= length:
                idx = 0
        else:
            idx -= 1
            length = len(self.jewelrySets[key])
            if idx < length:
                idx = length - 1
        self.jewelrySets[key][idx][0].unstash()
        if primaryColor:
            self.jewelrySets[key][idx][0].setColor(primaryColor)
        self.jewelrySets[key][idx][1].unstash()
        if secondaryColor:
            self.jewelrySets[key][idx][1].setColor(secondaryColor)
        self.currentJewelry[key][0] = idx

    def initialParts(self):
        self.clothing.stash()
        self.hair.stash()
        self.beard.stash()
        self.mustache.stash()
        self.hat.stash()
        self.eyepatch.stash()
        self.wig.stash()
        self.accBody.stash()
        self.accFace.stash()

    def setFromDNA(self):
        zombie = self.pirate.zombie
        if self.pirate.style == None:
            self.clothingsPant[0][0].unstash()
            self.bodys[5].stash()
            self.bodys[10].stash()
            self.bodys[11].stash()
        else:
            self.tattoos[0] = self.pirate.style.getTattooChest()
            self.handleClothesHiding()
            self.handleHeadHiding()
            self.hairIdx = self.pirate.style.getHairHair()
            self.beardIdx = self.pirate.style.getHairBeard()
            self.mustacheIdx = self.pirate.style.getHairMustache()
            self.handleJewelryHiding()
        return

    def makeZombie(self):
        self.dnaZomb.setHairColor(ZOMB_HAIR_COLOR)
        self.dnaZomb.setClothesShirt(ZOMB_SHIRT, ZOMB_SHIRT_TEXTURE)
        self.dnaZomb.setClothesVest(ZOMB_VEST, ZOMB_VEST_TEXTURE)
        self.dnaZomb.setClothesCoat(ZOMB_COAT, ZOMB_COAT_TEXTURE)
        self.dnaZomb.setClothesPant(ZOMB_PANT, ZOMB_PANT_TEXTURE)
        self.dnaZomb.setClothesBelt(ZOMB_BELT)
        self.dnaZomb.setClothesShoe(ZOMB_SHOE, ZOMB_SHOE_TEXTURE)
        self.dnaZomb.setClothesTopColor(0, 0, 0)
        self.dnaZomb.setClothesBotColor(0, 0, 0)

    def generatePantSets(self):
        self.pantSets = []
        for pantIdx in xrange(len(self.clothingsPant)):
            pant = self.clothingsPant[pantIdx]
            texName = clothes_textures['PANT'][pantIdx][0]
            if pantIdx in ClothingGlobals.shopkeep_pant_geoms:
                tex = None
            else:
                tex = self.texDict.get(texName[0])
            flattenedSet = {'belt': NodePathCollection(),'nobelt': NodePathCollection()}
            for lod in ['2000', '1000', '500']:
                pantData = {'belt': NodePathCollection(),'nobelt': NodePathCollection()}
                for idx in pant[0]:
                    pieceSet = self.layer1LODs[idx][lod]
                    for i in xrange(pieceSet.getNumPaths()):
                        piece = pieceSet[i]
                        if piece.getName().find('belt') < 0:
                            pantData['nobelt'].addPath(piece)
                            pantData['belt'].addPath(piece)
                        else:
                            pantData['nobelt'].addPath(piece)

                for style1 in ['belt', 'nobelt']:
                    data = pantData[style1]
                    geomSet = self.flattenData(data, lod, tex)
                    flattenedSet[style1].addPathsFrom(geomSet)

            self.pantSets.append(flattenedSet)

        return

    def generateHatSets(self):
        self.hatSets = []
        for hatIdx in xrange(len(self.clothingsHat)):
            hat = self.clothingsHat[hatIdx]
            texName = clothes_textures['HAT'][hatIdx][0]
            sTex = texName[0].split('+')
            if len(sTex) > 1:
                tex = self.texDict.get(sTex[0])
            else:
                tex = self.texDict.get(texName[0])
            flattenedSet = NodePathCollection()
            for lod in ['2000', '1000', '500']:
                for idx in hat[0]:
                    hatData = NodePathCollection()
                    pieceSet = self.layer1LODs[idx][lod]
                    for i in xrange(pieceSet.getNumPaths()):
                        piece = pieceSet[i]
                        hatData.addPath(piece)

                    geomSet = self.flattenHatData(hatData, lod)
                    flattenedSet.addPathsFrom(geomSet)

            self.hatSets.append(flattenedSet)

    def generateShoeSets(self):
        self.shoeSets = []
        for shoeIdx in xrange(len(self.clothingsShoe)):
            shoe = self.clothingsShoe[shoeIdx]
            texName = clothes_textures['SHOE'][shoeIdx][0]
            tex = self.texDict.get(texName[0])
            flattenedSet = NodePathCollection()
            for lod in ['2000', '1000', '500']:
                shoeData = NodePathCollection()
                for idx in shoe[0]:
                    pieceSet = self.layer1LODs[idx][lod]
                    for i in xrange(pieceSet.getNumPaths()):
                        piece = pieceSet[i]
                        shoeData.addPath(piece)

                geomSet = self.flattenData(shoeData, lod, tex)
                flattenedSet.addPathsFrom(geomSet)

            self.shoeSets.append(flattenedSet)

    def generateShirtSets(self):
        self.shirtSets = []
        for shirtIdx in xrange(len(self.clothingsShirt)):
            shirt = self.clothingsShirt[shirtIdx]
            texName = clothes_textures['SHIRT'][shirtIdx][0]
            tex = self.texDict.get(texName[0])
            flattenedSet = {'nobelt': {'full': NodePathCollection(),'openVest': NodePathCollection(),'closedVest': NodePathCollection(),'coat': NodePathCollection(),'coat+closedVest': NodePathCollection(),'covered': NodePathCollection()},'belt': {'full': NodePathCollection(),'openVest': NodePathCollection(),'closedVest': NodePathCollection(),'coat': NodePathCollection(),'coat+closedVest': NodePathCollection(),'covered': NodePathCollection()}}
            for lod in ['2000', '1000', '500']:
                shirtData = {'nobelt': {'full': NodePathCollection(),'openVest': NodePathCollection(),'closedVest': NodePathCollection(),'coat': NodePathCollection(),'coat+closedVest': NodePathCollection(),'covered': NodePathCollection()},'belt': {'full': NodePathCollection(),'openVest': NodePathCollection(),'closedVest': NodePathCollection(),'coat': NodePathCollection(),'coat+closedVest': NodePathCollection(),'covered': NodePathCollection()}}
                for idx in shirt[0]:
                    if idx == 4 or idx == 5:
                        if idx == 4:
                            pieceSet = self.layer1LODs[6][lod]
                        else:
                            pieceSet = self.layer1LODs[7][lod]
                        for i in xrange(pieceSet.getNumPaths()):
                            piece = pieceSet[i]
                            shirtData['belt']['full'].addPath(piece)
                            if piece.getName().find('base') < 0:
                                shirtData['belt']['openVest'].addPath(piece)
                                if piece.getName().find('front') < 0 and piece.getName().find('collar_v_low') < 0:
                                    shirtData['belt']['closedVest'].addPath(piece)
                                if piece.getName().find('front') >= 0 or piece.getName().find('collar') >= 0:
                                    shirtData['belt']['coat'].addPath(piece)
                                if piece.getName().find('collar') >= 0 and piece.getName().find('collar_v_low') < 0:
                                    shirtData['belt']['coat+closedVest'].addPath(piece)

                        pieceSet = self.layer1LODs[idx][lod]
                        for i in xrange(pieceSet.getNumPaths()):
                            piece = pieceSet[i]
                            shirtData['nobelt']['full'].addPath(piece)
                            if piece.getName().find('base') < 0:
                                shirtData['nobelt']['openVest'].addPath(piece)
                                if piece.getName().find('front') < 0 and piece.getName().find('collar_v_low') < 0:
                                    shirtData['nobelt']['closedVest'].addPath(piece)
                                if piece.getName().find('front') >= 0 or piece.getName().find('collar') >= 0:
                                    shirtData['nobelt']['coat'].addPath(piece)
                                if piece.getName().find('collar') >= 0 and piece.getName().find('collar_v_low') < 0:
                                    shirtData['nobelt']['coat+closedVest'].addPath(piece)

                    else:
                        pieceSet = self.layer1LODs[idx][lod]
                        for i in xrange(pieceSet.getNumPaths()):
                            piece = pieceSet[i]
                            shirtData['belt']['full'].addPath(piece)
                            shirtData['nobelt']['full'].addPath(piece)
                            if piece.getName().find('base') < 0:
                                shirtData['belt']['openVest'].addPath(piece)
                                shirtData['nobelt']['openVest'].addPath(piece)
                                if piece.getName().find('front') < 0 and piece.getName().find('collar_v_low') < 0:
                                    shirtData['belt']['closedVest'].addPath(piece)
                                    shirtData['nobelt']['closedVest'].addPath(piece)
                                if piece.getName().find('front') >= 0 or piece.getName().find('collar') >= 0:
                                    shirtData['belt']['coat'].addPath(piece)
                                    shirtData['nobelt']['coat'].addPath(piece)
                                if piece.getName().find('collar') >= 0 and piece.getName().find('collar_v_low') < 0:
                                    shirtData['belt']['coat+closedVest'].addPath(piece)
                                    shirtData['nobelt']['coat+closedVest'].addPath(piece)

                for style1 in ['belt', 'nobelt']:
                    for style2 in ['full', 'openVest', 'closedVest', 'coat', 'coat+closedVest']:
                        data = shirtData[style1][style2]
                        geomSet = self.flattenData(data, lod, tex)
                        flattenedSet[style1][style2].addPathsFrom(geomSet)

            self.shirtSets.append(flattenedSet)

    def generateVestSets(self):
        self.vestSets = []
        for vestIdx in xrange(len(self.clothingsVest)):
            vest = self.clothingsVest[vestIdx]
            texName = clothes_textures['VEST'][vestIdx][0]
            tex = self.texDict.get(texName[0])
            flattenedSet = {'belt': {'full': NodePathCollection(),'coat': NodePathCollection(),'coatSpecial': NodePathCollection(),'covered': NodePathCollection()},'nobelt': {'full': NodePathCollection(),'coat': NodePathCollection(),'coatSpecial': NodePathCollection(),'covered': NodePathCollection()}}
            for lod in ['2000', '1000', '500']:
                vestData = {'belt': {'full': NodePathCollection(),'coat': NodePathCollection(),'coatSpecial': NodePathCollection(),'covered': NodePathCollection()},'nobelt': {'full': NodePathCollection(),'coat': NodePathCollection(),'coatSpecial': NodePathCollection(),'covered': NodePathCollection()}}
                for idx in vest[0]:
                    pieceSet = self.layer2LODs[idx][lod]
                    for i in xrange(pieceSet.getNumPaths()):
                        piece = pieceSet[i]
                        legs_base = piece.getName().find('legs_base') >= 0
                        front = piece.getName().find('front') >= 0
                        coat = front
                        coatSpecial = front or legs_base
                        belt = not piece.getName().find('belt') >= 0
                        if belt:
                            vestData['belt']['full'].addPath(piece)
                            if coatSpecial:
                                vestData['belt']['coatSpecial'].addPath(piece)
                            if coat:
                                vestData['belt']['coat'].addPath(piece)
                        vestData['nobelt']['full'].addPath(piece)
                        if coatSpecial:
                            vestData['nobelt']['coatSpecial'].addPath(piece)
                        if coat:
                            vestData['nobelt']['coat'].addPath(piece)

                for style1 in ['belt', 'nobelt']:
                    for style2 in ['full', 'coat', 'coatSpecial']:
                        data = vestData[style1][style2]
                        geomSet = self.flattenData(data, lod, tex)
                        flattenedSet[style1][style2].addPathsFrom(geomSet)

            self.vestSets.append(flattenedSet)

    def generateCoatSets(self):
        self.coatSets = []
        for coatIdx in xrange(len(self.clothingsCoat)):
            coat = self.clothingsCoat[coatIdx]
            texName = clothes_textures['COAT'][coatIdx][0]
            tex = self.texDict.get(texName[0])
            flattenedSet = NodePathCollection()
            for lod in ['2000', '1000', '500']:
                geomSet = self.flattenSet(coat[0], self.layer3LODs, lod, tex)
                flattenedSet.addPathsFrom(geomSet)

            self.coatSets.append(flattenedSet)

    def generateBeltSets(self):
        self.beltSets = []
        for beltIdx in xrange(len(self.clothingsBelt)):
            belt = self.clothingsBelt[beltIdx]
            texName = clothes_textures['BELT'][beltIdx][0][0].split('+')
            tex = self.texDict.get(texName[0])
            flattenedSet = {'full': [NodePathCollection(), NodePathCollection()],'coat': [NodePathCollection(), NodePathCollection()],'covered': [NodePathCollection(), NodePathCollection()]}
            for lod in ['2000', '1000', '500']:
                beltData = {'full': [NodePathCollection(), NodePathCollection()],'coat': [NodePathCollection(), NodePathCollection()]}
                idx1 = belt[0][0]
                pieceSet1 = self.layer2LODs[idx1][lod]
                for i in xrange(pieceSet1.getNumPaths()):
                    piece = pieceSet1[i]
                    beltData['full'][0].addPath(piece)
                    if piece.getName().find('base') < 0:
                        beltData['coat'][0].addPath(piece)

                if len(belt[0]) > 1:
                    idx2 = belt[0][1]
                    pieceSet2 = self.layer2LODs[idx2][lod]
                    for i in xrange(pieceSet2.getNumPaths()):
                        piece = pieceSet2[i]
                        beltData['full'][1].addPath(piece)
                        if piece.getName().find('base') < 0:
                            beltData['coat'][1].addPath(piece)

                for style in ['full', 'coat']:
                    for i in [0, 1]:
                        data = beltData[style]
                        geomSet = self.flattenData(data[i], lod, tex)
                        flattenedSet[style][i].addPathsFrom(geomSet)

            self.beltSets.append(flattenedSet)

    def generateHairSets(self):
        cuts = [
         'cut_none', 'cut_captain', 'cut_tricorn', 'cut_navy', 'cut_admiral', 'cut_admiral', 'cut_bandanna_full', 'cut_bandanna', 'cut_beanie', 'cut_admiral', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full', 'cut_bandanna_full']

        def getBasicData():
            data = []
            for i in xrange(len(self.hats)):
                data.append(NodePathCollection())

            return data

        nonCutOpts = {}
        self.hairSets = []
        dataCache = {'2000': {},'1000': {},'500': {}}
        for hairIdx in xrange(len(self.hairs)):
            hairParts = self.hairs[hairIdx]
            flattenedSet = getBasicData()
            for hatIdx in xrange(len(self.hats)):
                for lod in ['2000', '1000', '500']:
                    hairIndices = set()
                    hairCutIndices = set()
                    hairData = NodePathCollection()
                    for partIdx in hairParts:
                        hair = self.hairLODs[partIdx][lod]
                        if partIdx == 1 or hatIdx == 0:
                            hairData.addPathsFrom(hair)
                            hairIndices.add(partIdx)
                        elif partIdx > 0:
                            hairCut = self.hairCutLODs[partIdx][lod]
                            cutFound = 0
                            for j in xrange(hairCut.getNumPaths()):
                                if hairCut[j].getName().find(cuts[hatIdx]) >= 0:
                                    hairCutIndices.add(partIdx)
                                    hairData.addPath(hairCut[j])
                                    cutFound = 1

                            if not cutFound:
                                if hatIdx == 7 and partIdx == 2 or partIdx == 5 or partIdx == 8 or partIdx == 10:
                                    hairIndices.add(partIdx)
                                    hairData.addPathsFrom(hair)

                    hl = list(hairIndices)
                    hl.sort()
                    t1 = tuple(hl)
                    hcl = list(hairCutIndices)
                    hcl.sort()
                    t2 = tuple(hcl)
                    cachedCopy = dataCache[lod].get((hatIdx, t1, t2))
                    if cachedCopy:
                        flattenedSet[hatIdx].addPathsFrom(cachedCopy)
                    else:
                        geomSet = self.flattenData(hairData, lod, False)
                        flattenedSet[hatIdx].addPathsFrom(geomSet)
                        dataCache[lod][hatIdx, t1, t2] = geomSet

            self.hairSets.append(flattenedSet)

        self.dataCache = dataCache

    def flattenSet(self, parts, layerSet, lod, stripTex=True):
        flattenMe = NodePath('flattenMe')
        for i in parts:
            geomData = layerSet[i][lod]
            for j in xrange(geomData.getNumPaths()):
                geomData[j].copyTo(flattenMe)

        flattenMe.flattenStrong()
        geomSet = flattenMe.findAllMatches('**/+GeomNode')
        if stripTex:
            self.stripTexture(geomSet)
        geomSet.reparentTo(self.pirate.getLOD(lod).getChild(0))
        geomSet.stash()
        return geomSet

    def flattenData(self, geomData, lod, stripTex=True, flattenStrong=True):
        flattenMe = NodePath('flattenMe')
        for i in xrange(geomData.getNumPaths()):
            geomData[i].copyTo(flattenMe)

        if flattenStrong:
            flattenMe.flattenStrong()
        geomSet = flattenMe.findAllMatches('**/+GeomNode')
        if stripTex:
            self.stripTexture(geomSet)
        geomSet.reparentTo(self.pirate.getLOD(lod).getChild(0))
        geomSet.stash()
        return geomSet

    def flattenHatData(self, geomData, lod):
        flattenMe = NodePath('flattenMe')
        for i in xrange(geomData.getNumPaths()):
            geomPart = geomData[i].copyTo(flattenMe)
            geomPart.setState(geomPart.getState().removeAttrib(TextureAttrib.getClassType()))
            geomNode = geomPart.node()
            for j in xrange(geomNode.getNumGeoms()):
                geomState = geomNode.getGeomState(j)
                if not geomState.isEmpty():
                    if geomState.getAttrib(TextureAttrib.getClassType()).getTexture():
                        if geomState.getAttrib(TextureAttrib.getClassType()).getTexture().getName().find('feather') < 0:
                            geomNode.setGeomState(j, geomState.removeAttrib(TextureAttrib.getClassType()))

        geomSet = flattenMe.findAllMatches('**/+GeomNode')
        for i in xrange(geomSet.getNumPaths()):
            geomSet.reparentTo(self.pirate.getLOD(lod).getChild(0))
            geomSet.stash()

        return geomSet

    def stripTexture(self, geomSet):
        for i in xrange(geomSet.getNumPaths()):
            geomSet[i].setState(geomSet[i].getState().removeAttrib(TextureAttrib.getClassType()))
            geomNode = geomSet[i].node()
            for j in xrange(geomNode.getNumGeoms()):
                geomState = geomNode.getGeomState(j)
                geomNode.setGeomState(j, geomState.removeAttrib(TextureAttrib.getClassType()))