from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from pirates.pirate import HumanDNA
from pirates.makeapirate import ClothingGlobals
from pirates.inventory.ItemConstants import DYE_COLORS
from pirates.pirate import BodyDefs
from pirates.inventory import ItemGlobals, DropGlobals
import TattooGlobals
from otp.otpbase import OTPRender
import copy
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
ZOMB_HAT = 5
ZOMB_SHIRT = 0
ZOMB_SHIRT_TEXTURE = 0
ZOMB_VEST = 3
ZOMB_VEST_TEXTURE = 3
ZOMB_COAT = 0
ZOMB_COAT_TEXTURE = 0
ZOMB_PANT = 1
ZOMB_PANT_TEXTURE = 5
ZOMB_BELT = 0
ZOMB_SHOE = 0
ZOMB_SHOE_TEXTURE = 0
body_textures = BodyDefs.femaleBodyTextures
face_textures = [
 'female_face_cauc_a', 'female_face_cauc_b', 'female_face_asian_a', 'female_face_dark_a', 'female_face_very_aged']
eye_iris_textures = [
 'pupilAqua', 'pupilBlue', 'pupilDarkBrown', 'pupilGreen', 'pupilHazel', 'pupilLightBrown']
female_hairs = [
 'style 0: bun', 'style 1: bun w/bangA', 'style 2: bun w/bangB', 'style 3: Ponytail', 'style 4: Ponytail w/bangA', 'style 5: Ponytail w/bangB', 'style 6: poof+barrette', 'style 7: poof+barrette w/bang', 'style 8: half down main+bun+backhair', 'style 9: half down main+pony+backhair', 'style 10: half down main+backhair+barrette', 'style 11: braid back+barrette', 'style 12: braid back+barrette w/bangA', 'style 13: braid back+barrette w/bangB', 'style 14: layered long', 'style 15: layered short', 'style 16: dreads short']
shirt_styles = [
 'S_short_sleeve_round_neck', 'S_short_sleeve_vneck', 'S_short_sleeve_square_neck', 'S_long_sleeve_vneck_puffy', 'S_long_sleeve_vneck_collar', 'S_long_sleeve_tall_collar']
vector_tattoos = [
 [
  0, 0.3, 0.862, 0.033, 0, 0], [0, 0.15, 0.79, 0.066, 271.1, 0], [0, 0.124, 0.61, 0.066, 271.1, 0], [0, 0.5, 0.5, 1.0, 0, 0], [0, 0.13, 0.35, 0.1, 0, 0], [0, 0.5, 0.5, 0.1, 0, 0], [0, 0.5, 0.5, 0.1, 0, 0], [0, 0.5, 0.5, 0.1, 0, 0]]
jewelry_geos_face = [
 'acc_none', 'acc_face_brow_spike_left', 'acc_face_brow_spike_right', 'acc_face_brow_ring_left', 'acc_face_brow_ring_right', 'acc_face_ear_cuff_a_left', 'acc_face_ear_cuff_a_right', 'acc_face_ear_cuff_b_left', 'acc_face_ear_cuff_b_right', 'acc_face_ear_cuff_c_left', 'acc_face_ear_cuff_c_right', 'acc_face_ear_open_left', 'acc_face_ear_open_right', 'acc_face_ear_stud_left', 'acc_face_ear_stud_right', 'acc_face_ear_spike_top_left', 'acc_face_ear_spike_top_right', 'acc_face_ear_spike_bot_left', 'acc_face_ear_spike_bot_right', 'acc_face_ear_hoop_a_left', 'acc_face_ear_hoop_a_right', 'acc_face_ear_hoop_b_left', 'acc_face_ear_hoop_b_right', 'acc_face_ear_bighoop_left', 'acc_face_ear_bighoop_right', 'acc_face_lip_ring_top_left', 'acc_face_lip_ring_top_right', 'acc_face_lip_ring_bot_left', 'acc_face_lip_ring_bot_right', 'acc_face_nose_ring_left', 'acc_face_nose_ring_right', 'acc_face_lip_ring_center', 'acc_face_lip_jawry', 'acc_face_nose_post_top', 'acc_face_nose_post_bot', 'acc_face_nose_ring_center', 'acc_face_lip_mustache']
jewelry_geos_body = [
 'acc_none', 'acc_body_ring_left_index_base', 'acc_body_ring_right_index_base', 'acc_body_ring_left_index_stone', 'acc_body_ring_right_index_stone', 'acc_body_ring_left_mid_base', 'acc_body_ring_right_mid_base', 'acc_body_ring_left_mid_stone', 'acc_body_ring_right_mid_stone', 'acc_body_ring_left_ring_base', 'acc_body_ring_right_ring_base', 'acc_body_ring_left_ring_stone', 'acc_body_ring_right_ring_stone', 'acc_body_ring_left_pinky_base', 'acc_body_ring_right_pinky_base', 'acc_body_ring_left_pinky_stone', 'acc_body_ring_right_pinky_stone']
jewelry_options = {'LBrow': [[0], [1], [3], [1, 3]],'RBrow': [[0], [2], [4], [2, 4]],'LEar': [[0], [13], [11], [15], [21, 19], [17], [23], [9], [7], [5], [23, 9, 7], [9, 7], [11, 17], [13, 9, 7], [15, 21], [19], [5, 7], [5, 7, 9, 17]],'REar': [[0], [14], [12], [16], [22, 20], [18], [24], [10], [8], [6], [24, 10, 8], [10, 8], [12, 18], [14, 10, 8], [16, 22], [20], [6, 8], [6, 8, 10, 18]],'Nose': [[0], [30], [33], [34], [29], [35], [33, 34], [33, 35], [33, 34, 35], [29, 30, 33, 34, 35], [36]],'Mouth': [[0], [25], [27], [21], [25], [26], [32], [25, 28], [31, 28], [25, 26, 27, 28, 31, 32], [36]],'LHand': [[0], [1], [1, 3], [5], [5, 7], [9], [9, 11], [13], [13, 15], [1, 5], [1, 9], [5, 13], [1, 5, 9, 13]],'RHand': [[0], [2], [2, 4], [6], [6, 8], [10], [10, 12], [14], [14, 16], [2, 6], [2, 10], [6, 14], [2, 6, 10, 14]]}
clothes_textures = ClothingGlobals.textures['FEMALE']
SliderNames = [
 'headWidth', 'headHeight', 'headRoundness', 'jawWidth', 'jawChinAngle', 'jawChinSize', 'jawLength', 'mouthWidth', 'mouthLipThickness', 'cheekFat', 'browProtruding', 'eyeCorner', 'eyeOpeningSize', 'eyeSpacing', 'noseBridgeWidth', 'noseNostrilWidth', 'noseLength', 'noseBump', 'noseNostrilHeight', 'noseNostrilAngle', 'noseBridgeBroke', 'noseNostrilBroke', 'earScale', 'earFlap', 'earPosition']
ControlShapes = {'headWidth': [[['def_trs_left_forehead', TX, 0.198, 0, 0, 0], ['def_trs_right_forehead', TX, -0.198, 0, 0, 0]], [['def_trs_left_forehead', TX, 0.198, 0, 0, 0], ['def_trs_right_forehead', TX, -0.198, 0, 0, 0]]],'headHeight': [[['def_trs_forehead', TZ, 0.566, 0, 0, 0], ['def_trs_left_forehead', TZ, 0.47, 0, 0, 0], ['def_trs_right_forehead', TZ, 0.47, 0, 0, 0]], [['def_trs_forehead', TZ, 0.566, 0, 0, 0], ['def_trs_left_forehead', TZ, 0.47, 0, 0, 0], ['def_trs_right_forehead', TZ, 0.47, 0, 0, 0]]],'headRoundness': [[['def_trs_left_jaw1', TX, 0.108, 0, 0, 0], ['def_trs_left_jaw1', TZ, -0.095, 0, 0, 0], ['def_trs_right_jaw1', TX, -0.108, 0, 0, 0], ['def_trs_right_jaw1', TZ, -0.095, 0, 0, 0]]],'jawWidth': [[['def_trs_left_jaw2', TX, 0.185, 0, 0, 0], ['def_trs_right_jaw2', TX, -0.185, 0, 0, 0]], [['def_trs_left_jaw2', TX, 0.185, 0, 0, 0], ['def_trs_right_jaw2', TX, -0.185, 0, 0, 0]]],'jawLength': [[['trs_face_bottom', TZ, -0.008, 0, 0, 0]], [['trs_face_bottom', TZ, -0.008, 0, 0, 0]]],'jawChinAngle': [[['def_trs_left_jaw1', TY, -0.17, 0, 0, 0], ['def_trs_right_jaw1', TY, -0.17, 0, 0, 0], ['def_trs_mid_jaw', TY, -0.244, 0, 0, 0]], [['def_trs_left_jaw1', TY, -0.17, 0, 0, 0], ['def_trs_right_jaw1', TY, -0.17, 0, 0, 0], ['def_trs_mid_jaw', TY, -0.244, 0, 0, 0]]],'jawChinSize': [[['def_trs_left_jaw1', TZ, -0.1, 0, 0, 0], ['def_trs_right_jaw1', TZ, -0.1, 0, 0, 0], ['def_trs_mid_jaw', TZ, -0.1, 0, 0, 0]], [['def_trs_left_jaw1', TZ, -0.1, 0, 0, 0], ['def_trs_right_jaw1', TZ, -0.1, 0, 0, 0], ['def_trs_mid_jaw', TZ, -0.1, 0, 0, 0]]],'mouthWidth': [[['trs_lips_top', SX, 1.2, 0, 0, 0], ['trs_lips_bot', SX, 1.2, 0, 0, 0]]],'mouthLipThickness': [[['trs_lips_top', SZ, 1.25, 0, 0, 0], ['trs_lips_bot', SZ, 1.25, 0, 0, 0]], [['trs_lips_top', SZ, 1.25, 0, 0, 0], ['trs_lips_bot', SZ, 1.25, 0, 0, 0]]],'cheekFat': [[['def_trs_left_cheek', TX, 0.156, 0, 0, 0], ['def_trs_right_cheek', TX, -0.156, 0, 0, 0]], [['def_trs_left_cheek', TX, 0.156, 0, 0, 0], ['def_trs_right_cheek', TX, -0.156, 0, 0, 0]]],'browProtruding': [[['trs_left_eyebrow', TY, -0.02, 0, 0, 0], ['trs_right_eyebrow', TY, -0.02, 0, 0, 0]]],'eyeCorner': [[['trs_left_eyesocket', RZ, 45 - 10, 0, 0, 0], ['trs_right_eyesocket', RZ, -(45 - 10), 0, 0, 0]], [['trs_left_eyesocket', RZ, 45 - 10, 0, 0, 0], ['trs_right_eyesocket', RZ, -(45 - 10), 0, 0, 0]]],'eyeOpeningSize': [[['trs_left_eyesocket', SX, 1.025, 0, 0, 0], ['trs_left_eyesocket', SZ, 1.025, 0, 0, 0], ['trs_right_eyesocket', SX, 1.025, 0, 0, 0], ['trs_right_eyesocket', SZ, 1.025, 0, 0, 0]], [['trs_left_eyesocket', SX, 1.025, 0, 0, 0], ['trs_left_eyesocket', SZ, 1.025, 0, 0, 0], ['trs_right_eyesocket', SX, 1.025, 0, 0, 0], ['trs_right_eyesocket', SZ, 1.025, 0, 0, 0]]],'eyeSpacing': [[['trs_left_eyesocket', TX, 0.006, 0, 0, 0], ['trs_right_eyesocket', TX, -0.006, 0, 0, 0]], [['trs_left_eyesocket', TX, 0.006, 0, 0, 0], ['trs_right_eyesocket', TX, -0.006, 0, 0, 0]]],'noseBridgeWidth': [[['def_trs_mid_nose_top', SX, 1.5, 0, 0, 0]], [['def_trs_mid_nose_top', SX, 1.5, 0, 0, 0]]],'noseNostrilWidth': [[['def_trs_mid_nose_bot', SX, 1.5, 0, 0, 0]], [['def_trs_mid_nose_bot', SX, 1.5, 0, 0, 0]]],'noseLength': [[['def_trs_mid_nose_bot', TZ, 0.057, 0, 0, 0]], [['def_trs_mid_nose_bot', TZ, 0.057, 0, 0, 0]]],'noseBump': [[['def_trs_mid_nose_top', TZ, 0.179, 0, 0, 0], ['def_trs_mid_nose_top', TY, -0.301, 0, 0, 0]], [['def_trs_mid_nose_top', TZ, 0.179, 0, 0, 0], ['def_trs_mid_nose_top', TY, -0.301, 0, 0, 0]]],'noseBridgeBroke': [[['def_trs_mid_nose_top', TX, 0.015, 0, 0, 0]], [['def_trs_mid_nose_top', TX, 0.015, 0, 0, 0]]],'noseNostrilHeight': [[['def_trs_mid_nose_bot', SY, 1.25, 0, 0, 0]], [['def_trs_mid_nose_bot', SY, 1.25, 0, 0, 0]]],'noseNostrilAngle': [[['def_trs_mid_nose_bot', RY, 12, 0, 0, 0]], [['def_trs_mid_nose_bot', RY, 12, 0, 0, 0]]],'noseNostrilBroke': [[['def_trs_mid_nose_bot', TX, 0.015, 0, 0, 0]], [['def_trs_mid_nose_bot', TX, 0.015, 0, 0, 0]]],'earScale': [[['def_trs_left_ear', SZ, 1.1, 0, 0, 0], ['def_trs_right_ear', SZ, 1.1, 0, 0, 0], ['def_trs_left_ear', SX, 1.1, 0, 0, 0], ['def_trs_right_ear', SX, 1.1, 0, 0, 0]], [['def_trs_left_ear', SZ, 1.1, 0, 0, 0], ['def_trs_right_ear', SZ, 1.1, 0, 0, 0], ['def_trs_left_ear', SX, 1.1, 0, 0, 0], ['def_trs_right_ear', SX, 1.1, 0, 0, 0]]],'earFlap': [[['def_trs_left_ear', RX, -20, 0, 0, 0], ['def_trs_right_ear', RX, 20, 0, 0, 0]], [['def_trs_left_ear', RX, -20, 0, 0, 0], ['def_trs_right_ear', RX, 20, 0, 0, 0]]],'earPosition': [[['def_trs_left_ear', TZ, 0.145, 0, 0, 0], ['def_trs_right_ear', TZ, 0.145, 0, 0, 0]], [['def_trs_left_ear', TZ, 0.145, 0, 0, 0], ['def_trs_right_ear', TZ, 0.145, 0, 0, 0]]]}

class PirateFemale(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateFemale')

    def __init__(self, pirate, dna):
        self.pirate = pirate
        self.texDict = {}
        self.bodySets = [{}, {}, {}]
        self.dna = dna
        self.dnaZomb = HumanDNA.HumanDNA('f')
        self.makeZombie()
        self.loaded = 0
        self.tattooZones = [
         [
          0, 1, 2, 3, 4, 5, 6, 9, 10], [13, 15, 31], [14, 16, 32], [-1], [0], [0], [0], [0]]
        self.tattooStage = TextureStage('tattoo')
        self.tattooStage.setTexcoordName('tattoomap')
        self.tattoos = [
         1, 2, 3, 4, 5, 6, 7, 8]
        self.currentClothing = {'HAT': [0, 0, 0],'SHIRT': [0, 0, 0],'VEST': [0, 0, 0],'COAT': [0, 0, 0],'BELT': [0, 0, 0],'PANT': [0, 0, 0],'SHOE': [0, 0, 0]}
        self.currentClothingModels = {'HAT': NodePathCollection(),'HAT': NodePathCollection(),'HAIR': NodePathCollection(),'SHIRT': NodePathCollection(),'VEST': NodePathCollection(),'COAT': NodePathCollection(),'BELT': [NodePathCollection(), NodePathCollection()],'PANT': NodePathCollection(),'SHOE': NodePathCollection()}
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
            posY = tattoo[2]
            t = TransformState.makePosRotateScale2d(Vec2(tattoo[1], posY), tattoo[4], Vec2(scaleX, scaleY))
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
        posY = tattoo[2]
        t = TransformState.makePosRotateScale2d(Vec2(tattoo[1], posY), tattoo[4], Vec2(scaleX, scaleY))
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
                            if tc[k].getTexcoordName().getName().find('Light') != -1:
                                tc[k].setMode(TextureStage.MBlend)
                                tc[k].setSort(10)
                            elif tc[k].getTexcoordName().getName().find('Dark') != -1:
                                tc[k].setSort(0)

        setupMultiTexture(self.hairPieces)
        setupMultiTexture(self.eyeBrows)

    def showHair(self):
        for i in range(0, len(self.hairs[self.hairIdx])):
            if not self.hairPieces[self.hairs[self.hairIdx][i]].isEmpty():
                self.hairPieces[self.hairs[self.hairIdx][i]].unstash()

    def hideHair(self):
        for i in range(0, len(self.hairs[self.hairIdx])):
            if not self.hairPieces[self.hairs[self.hairIdx][i]].isEmpty():
                self.hairPieces[self.hairs[self.hairIdx][i]].stash()
            if not self.hairCuts[self.hairs[self.hairIdx][i]].isEmpty():
                self.hairCuts[self.hairs[self.hairIdx][i]].stash()

    def handleHeadHiding(self):
        hairIdx = [
         self.pirate.style.getHairHair(), self.pirate.style.getHairBaseColor()]
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
        self.currentClothingModels['HAIR'] = currentHair
        self.currentClothingModels['HAT'].stash()
        texInfo = clothes_textures['HAT'][hatIdx[0]][hatIdx[1]][0].split('+')
        if self.texDict[texInfo[0]]:
            if len(texInfo) > 1:
                for base in (0, 2, 4):
                    currentHat[base].setTexture(self.texDict[texInfo[0]], 3)
                    currentHat[base + 1].setTexture(self.texDict[texInfo[1]], 4)

            else:
                currentHat.setTexture(self.texDict[texInfo[0]])
            currentHat.setColorScale(hatColor)
        self.currentClothingModels['HAT'] = currentHat
        if hatIdx[0] > 0:
            currentHat.setColorScale(hatColor)
            if 14 not in self.hairs[hairIdx[0]]:
                currentHat.unstash()
        self.setHairBaseColor()

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
                faceSet[i].clearColorScale()
                faceSet[i].copyTo(flattenMe)

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
        self.tooths.append(geom.findAllMatches('**/teeth_*'))
        if base.config.GetBool('want-gen-pics-buttons'):
            self.eyes = self.pirate.findAllMatches('**/eye_*')
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
        self.hair = geom.findAllMatches('**/hair*')
        self.hairPieces = []
        hairList = [
         '**/hair_a0', '**/hair_b0', '**/hair_c0', '**/hair_d0', '**/hair_e0', '**/hair_f0', '**/hair_g0', '**/hair_h0', '**/hair_i0', '**/hair_j0', '**/hair_k0', '**/hair_l0', '**/hair_m0', '**/hair_n0', '**/hair_o0_reg*']
        self.hairPieces.append(geom.findAllMatches('**/hair_a0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_b0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_c0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_d0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_e0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_f0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_g0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_h0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_i0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_j0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_k0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_l0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_m0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_n0'))
        self.hairPieces.append(geom.findAllMatches('**/hair_o0_reg*'))
        self.hairs = []
        self.hairIdx = self.pirate.style.getHairHair()
        self.hairs.append([0, 1, 2])
        self.hairs.append([0, 1, 2, 3])
        self.hairs.append([0, 1, 2, 4])
        self.hairs.append([0, 5])
        self.hairs.append([0, 5, 3])
        self.hairs.append([0, 5, 4])
        self.hairs.append([2, 6, 10])
        self.hairs.append([2, 6, 7, 10])
        self.hairs.append([0, 1, 8])
        self.hairs.append([0, 5, 8])
        self.hairs.append([0, 8, 10])
        self.hairs.append([0, 9, 11])
        self.hairs.append([0, 9, 3, 11])
        self.hairs.append([0, 9, 4, 11])
        self.hairs.append([0, 10])
        self.hairs.append([0, 10, 3])
        self.hairs.append([0, 10, 4])
        self.hairs.append([12])
        self.hairs.append([13])
        self.hairs.append([14])
        hairCutList = [
         '**/hair_a0_cut*', '**/hair_b0_cut*', '**/hair_c0_cut*', '**/hair_d0_cut*', '**/hair_e0_cut*', '**/hair_f0_cut*', '**/hair_g0_cut*', '**/hair_h0_cut*', '**/hair_i0_cut*', '**/hair_j0_cut*', '**/hair_k0_cut*', '**/hair_l0_cut*', '**/hair_m0_cut*', '**/hair_n0_cut*', '**/hair_o0_cut*']
        self.hairCuts = []
        self.hairCuts.append(geom.findAllMatches('**/hair_a0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_b0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_c0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_d0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_e0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_f0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_g0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_h0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_i0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_j0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_k0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_l0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_m0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_n0_cut*'))
        self.hairCuts.append(geom.findAllMatches('**/hair_o0_cut*'))
        self.eyeBrows.unstash()
        self.beard = geom.findAllMatches('**/beard_*')
        self.beards = []
        self.beardIdx = 0
        self.beards.append(geom.findAllMatches('**/beard_none*'))
        self.mustache = geom.findAllMatches('**/mustache_*')
        self.mustaches = []
        self.mustacheIdx = 0
        self.mustaches.append(geom.findAllMatches('**/mustache_none*'))
        self.hat = geom.findAllMatches('**/clothing_layer1_hat_*')
        self.hats = []
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_none*'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_dress_hat'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_navy_hat*'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_navy_fancy'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_band_workers*'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_bandanna_full*'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_bandanna_reg*'))
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
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_french'))
        self.hats.append(geom.findAllMatches('**/clothing_layer1_hat_beanie'))
        self.colorableHats = [4, 5, 6]
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
        self.eyeBrows.unstash()
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

    def setupBody(self, lodName='2000'):
        geom = self.pirate.getGeomNode()
        self.bodys = []
        self.bodyIdx = 0
        self.body = geom.findAllMatches('**/body_*')
        faceParts = []
        for i in xrange(self.body.getNumPaths()):
            if self.body[i].getName().find('master_face') >= 0:
                faceParts.append(self.body[i])

        for part in faceParts:
            self.body.removePath(part)

        if self.newAvatars:
            self.stripTexture(self.body)
        self.bodyPiecesToGroup = {0: 0,1: 0,2: 0,3: 0,4: 0,5: 0,6: 0,7: 0,8: 0,9: 0,10: 0,11: 0,12: 0,13: 1,14: 2,15: 1,16: 2,17: 1,18: 2,19: 0,20: 0,21: 0,22: 0,23: 0,24: 0,25: 0,26: 0,27: 0,28: 0,29: 0,30: 0,31: 1,32: 2}
        self.groupsToBodyPieces = [
         [
          0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], [13, 15, 17, 31], [14, 16, 18, 32]]
        layerBList = [
         '**/body_neck1', '**/body_neck2', '**/body_neck_back', '**/body_collar1', '**/body_chest_center', '**/body_collar_round', '**/body_chest_remain', '**/body_ribs1', '**/body_ribs2', '**/body_torso_upper', '**/body_clavicles', '**/body_belly_button', '**/body_waist_line', '**/body_bicep_left', '**/body_bicep_right', '**/body_forearm_left', '**/body_forearm_right', '**/body_hand_left', '**/body_hand_right', '**/body_upper_hips', '**/body_hips', '**/body_thigh_left', '**/body_thigh_right', '**/body_knee_left', '**/body_knee_right', '**/body_uppercalf_left', '**/body_uppercalf_right', '**/body_lowercalf_left', '**/body_lowercalf_right', '**/body_foot_left', '**/body_foot_right', '**/body_armpit_left', '**/body_armpit_right']
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

        self.bodys.append(geom.findAllMatches('**/body_neck1'))
        self.bodys.append(geom.findAllMatches('**/body_neck2'))
        self.bodys.append(geom.findAllMatches('**/body_neck_back'))
        self.bodys.append(geom.findAllMatches('**/body_collar1'))
        self.bodys.append(geom.findAllMatches('**/body_chest_center'))
        self.bodys.append(geom.findAllMatches('**/body_collar_round'))
        self.bodys.append(geom.findAllMatches('**/body_chest_remain'))
        self.bodys.append(geom.findAllMatches('**/body_ribs1'))
        self.bodys.append(geom.findAllMatches('**/body_ribs2'))
        self.bodys.append(geom.findAllMatches('**/body_torso_upper'))
        self.bodys.append(geom.findAllMatches('**/body_clavicles'))
        self.bodys.append(geom.findAllMatches('**/body_belly_button'))
        self.bodys.append(geom.findAllMatches('**/body_waist_line'))
        self.bodys.append(geom.findAllMatches('**/body_bicep_left'))
        self.bodys.append(geom.findAllMatches('**/body_bicep_right'))
        self.bodys.append(geom.findAllMatches('**/body_forearm_left'))
        self.bodys.append(geom.findAllMatches('**/body_forearm_right'))
        self.bodys.append(geom.findAllMatches('**/body_hand_left'))
        self.bodys.append(geom.findAllMatches('**/body_hand_right'))
        self.bodys.append(geom.findAllMatches('**/body_upper_hips'))
        self.bodys.append(geom.findAllMatches('**/body_hips'))
        self.bodys.append(geom.findAllMatches('**/body_thigh_left'))
        self.bodys.append(geom.findAllMatches('**/body_thigh_right'))
        self.bodys.append(geom.findAllMatches('**/body_knee_left'))
        self.bodys.append(geom.findAllMatches('**/body_knee_right'))
        self.bodys.append(geom.findAllMatches('**/body_uppercalf_left'))
        self.bodys.append(geom.findAllMatches('**/body_uppercalf_right'))
        self.bodys.append(geom.findAllMatches('**/body_lowercalf_left'))
        self.bodys.append(geom.findAllMatches('**/body_lowercalf_right'))
        self.bodys.append(geom.findAllMatches('**/body_foot_left'))
        self.bodys.append(geom.findAllMatches('**/body_foot_right'))
        self.bodys.append(geom.findAllMatches('**/body_armpit_left'))
        self.bodys.append(geom.findAllMatches('**/body_armpit_right'))
        for part in self.bodys:
            part.stash()

        self.currentBody = NodePathCollection()
        self.bodyTextures = loader.loadModel('models/misc/female_body.bam')
        self.notify.debug('loaded body textures %s' % self.bodyTextures)
        self.numBodys = len(body_textures)
        self.bodyTextureIdx = self.pirate.style.getBodySkin()
        self.lowLODSkinColor = VBase4(0.85, 0.74, 0.68, 1.0)
        self.faceTextures = loader.loadModel('models/misc/female_face.bam')
        self.faceTexturesSet = []
        self.notify.debug('loaded face textures %s' % self.faceTextures)
        self.numFaces = len(face_textures)
        self.faceTextureIdx = self.pirate.style.getHeadTexture()
        self.numEyeColors = len(eye_iris_textures)
        self.eyesColorIdx = self.pirate.style.getEyesColor()
        self.skinColorIdx = self.pirate.style.getBodyColor()
        self.hairColorIdx = self.pirate.style.getHairColor()
        self.clothesShirtColorIdx = self.pirate.style.getClothesTopColor()[0]
        self.clothesVestColorIdx = self.pirate.style.getClothesTopColor()[1]
        self.clothesCoatColorIdx = self.pirate.style.getClothesTopColor()[2]
        self.clothesPantColorIdx = self.pirate.style.getClothesBotColor()[0]
        self.clothesSashColorIdx = self.pirate.style.getClothesBotColor()[1]
        self.clothesPantSashColorIdx = self.pirate.style.getClothesBotColor()[2]
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

        return None

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
         '**/clothing_layer1_shirt_common_base', '**/clothing_layer1_shirt_common_low_vcut', '**/clothing_layer1_shirt_common_front', '**/clothing_layer1_shirt_common_breast', '**/clothing_layer1_shirt_common_belt_front', '**/clothing_layer1_shirt_common_belt_interior', '**/clothing_layer1_shirt_common_belly_front', '**/clothing_layer1_shirt_common_waist_line', '**/clothing_layer1_shirt_short_sleeve1*', '**/clothing_layer1_shirt_short_sleeve_puffy*', '**/clothing_layer1_shirt_long_sleeve_puffy*', '**/clothing_layer1_shirt_long_sleeve_lowcut*', '**/clothing_layer1_shirt_long_sleeve_collar*', '**/clothing_layer1_shirt_long_sleeve_tallcollar*', '**/clothing_layer1_shirt_gypsy', '**/clothing_layer1_pant_short_*', '**/clothing_layer1_pant_shorts_*', '**/clothing_layer1_pant_skirt_*', '**/clothing_layer1_skirt_gypsy_short', '**/clothing_layer1_skirt_gypsy_long', '**/clothing_layer1_sock_stockings_*', '**/clothing_layer1_shoe_none_*', '**/clothing_layer1_shoe_boot_short*', '**/clothing_layer1_shoe_boot_medium*', '**/clothing_layer1_shoe_boot_kneehigh*', '**/clothing_layer1_shoe_boot_tall*', '**/clothing_layer1_pant_navy_*', '**/clothing_layer1_shoe_navy*', '**/clothing_layer1_hat_dress_hat;+s', '**/clothing_layer1_hat_navy_hat*;+s', '**/clothing_layer1_hat_navy_fancy;+s', '**/clothing_layer1_hat_band_workers*;+s', '**/clothing_layer1_hat_bandanna_full*;+s', '**/clothing_layer1_hat_bandanna_reg*;+s', '**/clothing_layer1_hat_navy_fancy_feather;+s', '**/clothing_layer1_hat_dress_hat_feather;+s', '**/clothing_layer1_hat_french;+s', '**/clothing_layer1_hat_french_feather;+s', '**/clothing_layer1_hat_spanish;+s', '**/clothing_layer1_hat_spanish_feather;+s', '**/clothing_layer1_hat_french_1;+s', '**/clothing_layer1_hat_french_2;+s', '**/clothing_layer1_hat_french_3;+s', '**/clothing_layer1_hat_spanish_1;+s', '**/clothing_layer1_hat_spanish_2;+s', '**/clothing_layer1_hat_spanish_3;+s', '**/clothing_layer1_hat_land_1;+s', '**/clothing_layer1_hat_land_2;+s', '**/clothing_layer1_hat_land_3;+s', '**/clothing_layer1_hat_holiday;+s', '**/clothing_layer1_hat_party_1;+s', '**/clothing_layer1_hat_party_2;+s', '**/clothing_layer1_hat_GM;+s', '**/clothing_layer1_hat_beanie;+s']
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_base'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_low_vcut'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_front'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_breast'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_belt_front'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_belt_interior'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_belly_front'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_common_waist_line'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_short_sleeve1*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_short_sleeve_puffy*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_long_sleeve_puffy*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_long_sleeve_lowcut*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_long_sleeve_collar*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_long_sleeve_tallcollar*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shirt_gypsy'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_short_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_shorts_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_skirt_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_skirt_gypsy_short'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_skirt_gypsy_long'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_sock_stockings_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_none_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_boot_short*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_boot_medium*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_boot_kneehigh*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_boot_tall*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_pant_navy_*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_shoe_navy*'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_dress_hat;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_navy_hat*;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_navy_fancy;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_band_workers*;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_bandanna_full*;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_bandanna_reg*;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_navy_fancy_feather;+s'))
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_dress_hat_feather;+s'))
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
        self.clothingsLayer1.append(geom.findAllMatches('**/clothing_layer1_hat_beanie;+s'))
        self.layer1LODs = []
        for item in layer1List:
            itemInfo = {}
            for lod in ['500', '1000', '2000']:
                itemInfo[lod] = self.pirate.getLOD(lod).findAllMatches(item)

            self.layer1LODs.append(itemInfo)

        self.partLayer['SHIRT'] = self.clothingsLayer1
        self.partLayer['PANT'] = self.clothingsLayer1
        self.partLayer['SHOE'] = self.clothingsLayer1
        self.partLayer['HAT'] = self.clothingsLayer1
        self.clothesTextures = loader.loadModel('models/misc/female_clothes.bam')
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

        self.texDict['FP_none'] = None
        self.clothingsShirt.append([[0, 1, 2, 3, 6, 7, 8], -4, -7, -8, -9, -11, -12, -31, -32])
        self.clothingsShirt.append([[0, 1, 2, 3, 6, 7, 9], -2, -4, -5, -6, -7, -8, -9, -10, -11, -12, -31, -32])
        self.clothingsShirt.append([[0, 1, 2, 3, 6, 7, 10], -1, -4, -5, -6, -7, -8, -9, -11, -12, -13, -14, -31, -32])
        self.clothingsShirt.append([[0, 1, 2, 3, 6, 7, 11], -2, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -31, -32])
        self.clothingsShirt.append([[0, 1, 2, 3, 4, 5, 6, 7, 12], -2, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -19, -31, -32])
        self.clothingsShirt.append([[0, 1, 2, 3, 4, 5, 6, 7, 13], -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -19, -31, -32])
        self.clothingsShirt.append([[14], -1, -2, -4, -5, -6, -7, -8, -9, -11, -12, -13, -14, -31, -32])
        self.clothingsHat.append([[]])
        self.clothingsHat.append([[28, 35]])
        self.clothingsHat.append([[29]])
        self.clothingsHat.append([[30, 34]])
        self.clothingsHat.append([[31]])
        self.clothingsHat.append([[32]])
        self.clothingsHat.append([[33]])
        self.clothingsHat.append([[36, 37]])
        self.clothingsHat.append([[38, 39]])
        self.clothingsHat.append([[40]])
        self.clothingsHat.append([[41]])
        self.clothingsHat.append([[42]])
        self.clothingsHat.append([[43]])
        self.clothingsHat.append([[44]])
        self.clothingsHat.append([[45]])
        self.clothingsHat.append([[46]])
        self.clothingsHat.append([[47]])
        self.clothingsHat.append([[48]])
        self.clothingsHat.append([[49]])
        self.clothingsHat.append([[50]])
        self.clothingsHat.append([[51]])
        self.clothingsHat.append([[52]])
        self.clothingsHat.append([[36]])
        self.clothingsHat.append([[53]])
        self.clothingsPant.append([[15], -19, -20, -21, -22, -23, -24, -25, -26])
        self.clothingsPant.append([[16], -19, -20, -21, -22])
        self.clothingsPant.append([[17], -19, -20, -21, -22])
        self.clothingsPant.append([[18], -19, -20, -21, -22, -23, -24])
        self.clothingsPant.append([[19], -19, -20, -21, -22, -23, -24, -25, -26, -27, -28])
        self.clothingsPant.append([[26], -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30])
        self.clothingsSock.append([[]])
        self.clothingsSock.append([[20], -23, -24, -25, -26, -27, -28, -29, -30])
        self.clothingsShoe.append([[21]])
        self.clothingsShoe.append([[22], -29, -30])
        self.clothingsShoe.append([[23], -27, -28, -29, -30])
        self.clothingsShoe.append([[24], -25, -26, -27, -28, -29, -30])
        self.clothingsShoe.append([[25], -23, -24, -25, -26, -27, -28, -29, -30])
        self.clothingsShoe.append([[27], -29, -30])
        layer2List = [
         '**/clothing_layer2_vest_none*', '**/clothing_layer2_vest_closed*', '**/clothing_layer2_vest_lowcut*', '**/clothing_layer2_vest_corset_high*', '**/clothing_layer2_vest_corset_low*', '**/clothing_layer2_belt_none*', '**/clothing_layer2_belt_sash_reg_base_front', '**/clothing_layer2_belt_sash_reg_base_interior', '**/clothing_layer2_belt_sash_reg_cloth', '**/clothing_layer2_belt_square_interior', '**/clothing_layer2_belt_square_buckle_front', '**/clothing_layer2_belt_square_strap_front']
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_vest_none*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_vest_closed*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_vest_lowcut*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_vest_corset_high*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_vest_corset_low*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_none*'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_sash_reg_base_front'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_sash_reg_base_interior'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_sash_reg_cloth'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_square_interior'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_square_buckle_front'))
        self.clothingsLayer2.append(geom.findAllMatches('**/clothing_layer2_belt_square_strap_front'))
        if base.config.GetBool('want-gen-pics-buttons'):
            self.clothesByType = {'SHIRT': self.clothingsLayer1[:15],'VEST': self.clothingsLayer2[:5],'PANT': self.clothingsLayer1[15:20] + self.clothingsLayer1[26:27],'COAT': self.clothingsLayer3,'BELT': self.clothingsLayer2[5:],'SHOE': self.clothingsLayer1[22:26] + self.clothingsLayer1[27:28],'HAT': self.clothingsLayer1[28:]}
        self.partLayer['VEST'] = self.clothingsLayer2
        self.partLayer['BELT'] = self.clothingsLayer2
        self.clothingsVest.append([[0]])
        self.clothingsVest.append([[1], -11, -12])
        self.clothingsVest.append([[2], -11, -12])
        self.clothingsVest.append([[3], -7, -8, -11, -12])
        self.clothingsVest.append([[4], -7, -8, -11, -12])
        self.clothingsBelt.append([[5]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[6, 7]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[9, 10, 11]])
        self.clothingsBelt.append([[6, 7, 8]])
        self.clothingsBelt.append([[9, 10, 11]])
        layer3List = [
         '**/clothing_layer3_coat_none*', '**/clothing_layer3_coat_long*', '**/clothing_layer3_coat_short*', '**/clothing_layer3_coat_navy*', '**/clothing_layer3_coat_eitc*']
        self.clothingsLayer3.append(geom.findAllMatches('**/clothing_layer3_coat_none*'))
        self.clothingsLayer3.append(geom.findAllMatches('**/clothing_layer3_coat_long*'))
        self.clothingsLayer3.append(geom.findAllMatches('**/clothing_layer3_coat_short*'))
        self.clothingsLayer3.append(geom.findAllMatches('**/clothing_layer3_coat_navy*'))
        self.clothingsLayer3.append(geom.findAllMatches('**/clothing_layer3_coat_eitc*'))
        self.partLayer['COAT'] = self.clothingsLayer3
        self.clothingsCoat.append([[0]])
        self.clothingsCoat.append([[1], -9, -12, -13, -14, -15, -16, -31, -32])
        self.clothingsCoat.append([[2], -9, -12, -13, -14, -15, -16, -31, -32])
        self.clothingsCoat.append([[3], -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -19, -31, -32])
        self.clothingsCoat.append([[4], -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -19, -31, -32])
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
        choices = data['FEMALE']
        self.choices = {}
        self.choices['FACE'] = choices.get('FACE', [])
        self.choices['HAIR'] = choices.get('HAIR', [])
        if type == 'DEFAULT':
            mapClothing = DropGlobals.getMakeAPirateClothing()
        else:
            mapClothing = ItemGlobals.getAllClothingIds(gender='f')
        hats = ItemGlobals.getGenderType(ItemGlobals.HAT, 'f', mapClothing)
        choiceHats = {}
        for hatId in hats:
            modelId = ItemGlobals.getFemaleModelId(hatId)
            texId = ItemGlobals.getFemaleTextureId(hatId)
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
        shirts = ItemGlobals.getGenderType(ItemGlobals.SHIRT, 'f', mapClothing)
        choiceShirts = {}
        for shirtId in shirts:
            modelId = ItemGlobals.getFemaleModelId(shirtId)
            texId = ItemGlobals.getFemaleTextureId(shirtId)
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
        vests = ItemGlobals.getGenderType(ItemGlobals.VEST, 'f', mapClothing)
        choiceVests = {}
        for vestId in vests:
            modelId = ItemGlobals.getFemaleModelId(vestId)
            texId = ItemGlobals.getFemaleTextureId(vestId)
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
        coats = ItemGlobals.getGenderType(ItemGlobals.COAT, 'f', mapClothing)
        choiceCoats = {}
        for coatId in coats:
            modelId = ItemGlobals.getFemaleModelId(coatId)
            texId = ItemGlobals.getFemaleTextureId(coatId)
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
        pants = ItemGlobals.getGenderType(ItemGlobals.PANT, 'f', mapClothing)
        choicePants = {}
        for pantId in pants:
            modelId = ItemGlobals.getFemaleModelId(pantId)
            texId = ItemGlobals.getFemaleTextureId(pantId)
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
        belts = ItemGlobals.getGenderType(ItemGlobals.BELT, 'f', mapClothing)
        choiceBelts = {}
        for beltId in belts:
            modelId = ItemGlobals.getFemaleModelId(beltId)
            texId = ItemGlobals.getFemaleTextureId(beltId)
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
        shoes = ItemGlobals.getGenderType(ItemGlobals.SHOE, 'f', mapClothing)
        choiceShoes = {}
        for shoeId in shoes:
            modelId = ItemGlobals.getFemaleModelId(shoeId)
            texId = ItemGlobals.getFemaleTextureId(shoeId)
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
        length = len(clothes_textures[part][geomIdx])
        if length == 0 or texIdx >= length:
            self.notify.debug('returning early')
            return
        texture = clothes_textures[part][geomIdx][texIdx]
        texName = texture[0].split('+')
        lowLODColor = texture[1]
        if len(texName) == 1:
            tex = self.clothesTextures.findTexture(texName[0])
            self.setClothesTexture(tex, pieces, self.partLayer[part], lowLODColor)
        else:
            tex = self.clothesTextures.findTexture(texName[0])
            self.setClothesTexture(tex, [pieces[0]], self.partLayer[part], lowLODColor)
            if len(pieces) > 2:
                self.setClothesTexture(tex, [pieces[2]], self.partLayer[part], lowLODColor)
            tex = self.clothesTextures.findTexture(texName[1])
            self.setClothesTexture(tex, [pieces[1]], self.partLayer[part], lowLODColor)

    def getTextureName(self, partIdx, idx, texIdx):
        try:
            return clothes_textures[partIdx][idx][texIdx]
        except:
            return None

        return None

    def handleClothesHiding(self):
        if not self.newAvatars:
            self.handleClothesHidingOld()
            self.setupTattoos()
            return
        self.notify.debug('should never get here in MAP with want-new-avatars turned on')
        dna = self.pirate.style
        if self.pirate.zombie and 0:
            dna = self.dnaZomb
        bodySet = [set(), set(), set()]
        shirtIdx = dna.getClothesShirt()
        vestIdx = dna.getClothesVest()
        coatIdx = dna.getClothesCoat()
        pantIdx = dna.getClothesPant()
        beltIdx = dna.getClothesBelt()
        sockIdx = dna.getClothesSock()
        shoeIdx = dna.getClothesShoe()
        hatIdx = dna.getClothesHat()
        if self.pirate.zombie:
            shirtIdx = self.dnaZomb.getClothesShirt()
            vestIdx = self.dnaZomb.getClothesVest()
            pantIdx = self.dnaZomb.getClothesPant()
        style2Pant = 'neither'
        if shirtIdx[0] > 3:
            style2pant = 'belt'
        if beltIdx[0] != 0:
            style1 = 'belt'
            style2Pant = 'belt'
            style1Shirt = 'belt'
        else:
            style1Shirt = 'nobelt'
            style1 = 'nobelt'
            style2Pant = 'neither'
        if vestIdx[0] > 2:
            style2Pant = 'belt'
            style3Shirt = 'vest2'
            style1Shirt = 'belt'
        else:
            if vestIdx[0] == 2:
                style2Pant = 'lowVest'
                style3Shirt = 'vest2'
                style1Shirt = 'belt'
            else:
                if vestIdx[0] == 1:
                    style2Pant = 'belt'
                    style3Shirt = 'vest1'
                    style1Shirt = 'belt'
                else:
                    style3Shirt = 'neither'
                    if shirtIdx[0] > 3:
                        style2Pant = 'belt'
                if coatIdx[0] > 0:
                    style2Shirt = 'coat'
                else:
                    style2Shirt = 'noCoat'
                if shoeIdx[0] == 4:
                    style1Pant = 'tallBoot'
                else:
                    style1Pant = 'shortBoot'
                if coatIdx[0] == 1:
                    style3Pant = 'longCoat'
                else:
                    if coatIdx[0] == 2:
                        style3Pant = 'shortCoat'
                    else:
                        if coatIdx[0] == 3:
                            style3Pant = 'noCoat'
                        else:
                            if coatIdx[0] == 4:
                                style3Pant = 'longCoat'
                            else:
                                style3Pant = 'noCoat'
                            if pantIdx[0] == 2:
                                style3Vest = 'skirt'
                            else:
                                style3Vest = 'pants'
                            layerPant = self.clothingsPant[pantIdx[0]]
                            layerShoe = self.clothingsShoe[shoeIdx[0]]
                            layerShirt = self.clothingsShirt[shirtIdx[0]]
                            layerVest = self.clothingsVest[vestIdx[0]]
                            layerBelt = self.clothingsBelt[beltIdx[0]]
                            layerCoat = self.clothingsCoat[coatIdx[0]]
                            currentVest = self.vestSets[vestIdx[0]][style1][style2Shirt][style3Vest]
                            if style1Shirt == 'belt':
                                currentShirt = self.shirtSets[shirtIdx[0]][style1Shirt][style2Shirt][style3Shirt]
                            else:
                                currentShirt = self.shirtSets[shirtIdx[0]][style1Shirt][style2Shirt]
                            currentCoat = self.coatSets[coatIdx[0]]
                            if coatIdx[0] > 0:
                                currentBelt = self.beltSets[beltIdx[0]]['coat3']
                            else:
                                currentBelt = self.beltSets[beltIdx[0]]['full']
                            currentPant = self.pantSets[pantIdx[0]][style1Pant][style2Pant][style3Pant]
                            currentShoe = self.shoeSets[shoeIdx[0]][style3Vest]
                            layerPant = self.clothingsPant[pantIdx[0]]
                            parts = NodePathCollection()
                            self.currentClothingModels['PANT'].stash()
                            currentPant.unstash()
                            self.currentClothingModels['PANT'] = currentPant
                            texInfo = clothes_textures['PANT'][pantIdx[0]][pantIdx[1]]
                            if self.texDict[texInfo[0]]:
                                pantColor = dna.lookupClothesBotColor()[0]
                                currentPant.setTexture(self.texDict[texInfo[0]])
                                currentPant.setColorScale(pantColor)
                            self.currentClothingModels['SHOE'].stash()
                            currentShoe.unstash()
                            self.currentClothingModels['SHOE'] = currentShoe
                            texInfo = clothes_textures['SHOE'][shoeIdx[0]][shoeIdx[1]]
                            if self.texDict[texInfo[0]]:
                                shoeColor = dna.lookupClothesBotColor()[2]
                                currentShoe.setTexture(self.texDict[texInfo[0]])
                            self.currentClothingModels['SHIRT'].stash()
                            self.currentClothingModels['SHIRT'] = currentShirt
                            if vestIdx[0] <= 2 and coatIdx[0] not in (3, 4):
                                currentShirt.unstash()
                                texInfo = clothes_textures['SHIRT'][shirtIdx[0]][shirtIdx[1]]
                                if self.texDict[texInfo[0]]:
                                    currentShirt.setTexture(self.texDict[texInfo[0]])
                                    shirtColor = dna.lookupClothesTopColor()[0]
                                    currentShirt.setColorScale(shirtColor)
                                self.currentClothingModels['SHIRT'] = currentShirt
                                for i in layerShirt[1:]:
                                    bodySet[self.bodyPiecesToGroup[-i]].add(-i)

                            self.currentClothingModels['VEST'].stash()
                            if coatIdx[0] not in (3, 4):
                                currentVest.unstash()
                                self.currentClothingModels['VEST'] = currentVest
                                texInfo = clothes_textures['VEST'][vestIdx[0]][vestIdx[1]]
                                if self.texDict[texInfo[0]]:
                                    vestColor = dna.lookupClothesTopColor()[1]
                                    currentVest.setTexture(self.texDict[texInfo[0]])
                                    currentVest.setColorScale(vestColor)
                                for i in layerVest[1:]:
                                    bodySet[self.bodyPiecesToGroup[-i]].add(-i)

                            self.handleHeadHiding()
                            self.currentClothingModels['BELT'][0].stash()
                            self.currentClothingModels['BELT'][1].stash()
                            if coatIdx[0] not in (3, 4):
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

                                for i in layerBelt[1:]:
                                    bodySet[self.bodyPiecesToGroup[-i]].add(-i)

                            self.currentClothingModels['COAT'].stash()
                            currentCoat.unstash()
                            self.currentClothingModels['COAT'] = currentCoat
                            texInfo = clothes_textures['COAT'][coatIdx[0]][coatIdx[1]]
                            if self.texDict[texInfo[0]]:
                                coatColor = dna.lookupClothesTopColor()[2]
                                currentCoat.setTexture(self.texDict[texInfo[0]])
                                currentCoat.setColorScale(coatColor)
                            for partSet in [layerCoat, layerPant, layerShoe]:
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
                    bodyTexIdx = 0
                tex = self.texDict[body_textures[self.pirate.style.getBodyShape()][bodyTexIdx]]
                self.currentBody.setTexture(tex)
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
        dna = self.pirate.style
        if self.pirate.zombie:
            dna = self.dnaZomb
        shirtIdx = dna.getClothesShirt()
        vestIdx = dna.getClothesVest()
        coatIdx = dna.getClothesCoat()
        pantIdx = dna.getClothesPant()
        beltIdx = dna.getClothesBelt()
        sockIdx = dna.getClothesSock()
        shoeIdx = dna.getClothesShoe()
        hatIdx = dna.getClothesHat()
        layerPant = self.clothingsPant[pantIdx[0]]
        parts = NodePathCollection()
        if self.clothesTextures != None:
            self.setPartTexture('PANT', pantIdx[0], pantIdx[1], layerPant[0])
        for j in range(0, len(layerPant[0])):
            parts = self.clothingsLayer1[layerPant[0][j]]
            if parts.getNumPaths():
                parts.unstash()

        self.handleLayer1Hiding(layerPant)
        layerShoe = self.clothingsShoe[shoeIdx[0]]
        parts = NodePathCollection()
        if self.clothesTextures != None:
            self.setPartTexture('SHOE', shoeIdx[0], shoeIdx[1], layerShoe[0])
        for j in range(0, len(layerShoe[0])):
            parts = self.clothingsLayer1[layerShoe[0][j]]
            if parts.getNumPaths():
                parts.unstash()

        self.handleLayer1Hiding(layerShoe)
        if shoeIdx[0] == 4:
            self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'knee', 'uppercalf')
            if pantIdx[0] == 2:
                self.handleLayer2Hiding(self.clothingsLayer1, layerShoe, 'top')
        layerShirt = self.clothingsShirt[shirtIdx[0]]
        parts = NodePathCollection()
        if vestIdx[0] < 3:
            if self.clothesTextures != None:
                self.setPartTexture('SHIRT', shirtIdx[0], shirtIdx[1], layerShirt[0])
            for j in range(0, len(layerShirt[0])):
                parts = self.clothingsLayer1[layerShirt[0][j]]
                if parts.getNumPaths():
                    parts.unstash()

            if parts.getNumPaths():
                self.handleLayer1Hiding(layerShirt)
            if shirtIdx[0] > 3:
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
            if vestIdx[0] == 1:
                self.handleLayer2Hiding(self.clothingsLayer1, layerShirt, 'base', 'low_vcut', 'front')
                self.handleLayer2Hiding(self.clothingsLayer1, layerShirt, 'breast', 'belt', 'waist')
                self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'belt')
            elif vestIdx[0] == 2:
                self.handleLayer2Hiding(self.clothingsLayer1, layerShirt, 'base', 'front', 'waist')
                self.handleLayer2Hiding(self.clothingsLayer1, layerShirt, 'belt')
                self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'belt', '_abs')
                if pantIdx[0] == 2:
                    self.handleLayer2Hiding(self.clothingsLayer2, layerVest, 'bottom_pant')
                else:
                    self.handleLayer2Hiding(self.clothingsLayer2, layerVest, 'bottom_skirt')
            else:
                self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'belt')
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

        if parts.getNumPaths():
            self.handleLayer2Hiding(self.clothingsLayer1, layerShirt, 'belt')
            self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'belt')
            self.handleLayer2Hiding(self.clothingsLayer2, layerVest, 'belt')
        layerCoat = self.clothingsCoat[coatIdx[0]]
        parts = NodePathCollection()
        if self.clothesTextures != None:
            self.setPartTexture('COAT', coatIdx[0], coatIdx[1], layerCoat[0])
        for j in range(0, len(layerCoat[0])):
            parts = self.clothingsLayer3[layerCoat[0][j]]
            if parts.getNumPaths():
                parts.unstash()

        if coatIdx[0] == 3:
            self.handleLayer3Hiding(self.clothingsLayer2, layerVest, layerShirt, True)
            self.handleLayer3Hiding(self.clothingsLayer2, layerBelt, None, True)
            self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'abs_interior', 'abs', 'belt_interior', 'side')
            self.handleLayer1Hiding(layerCoat)
        elif coatIdx[0] == 4:
            self.handleLayer3Hiding(self.clothingsLayer2, layerVest, layerShirt, True)
            self.handleLayer3Hiding(self.clothingsLayer2, layerBelt, None, True)
            self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'abs_interior', 'longcoat_interior', 'abs', 'side')
            self.handleLayer1Hiding(layerCoat)
        elif parts.getNumPaths():
            self.handleLayer3Hiding(self.clothingsLayer2, layerVest, layerShirt)
            self.handleLayer2Hiding(self.clothingsLayer2, layerBelt, '_cloth', 'interior')
            if pantIdx[0] == 2:
                if coatIdx[0] == 1:
                    self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'side', 'longcoat', 'tails')
                if coatIdx[0] == 2:
                    self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'side', 'interior', 'back')
            else:
                self.handleLayer2Hiding(self.clothingsLayer1, layerPant, 'interior')
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
            self.notify.debug('hiding %s' % parts[-idx][0].getName())

    def handleLayer2Hiding(self, clothingLayer, layer1Element, hide1='base', hide2=None, hide3=None, hide4=None):
        for i in range(0, len(layer1Element[0])):
            parts = clothingLayer[layer1Element[0][i]]
            for j in range(0, parts.getNumPaths()):
                if hide1 != None and parts[j].getName().find(hide1) != -1:
                    parts[j].stash()
                    self.notify.debug('hiding %s' % parts[j].getName())
                elif hide2 != None and parts[j].getName().find(hide2) != -1:
                    parts[j].stash()
                    self.notify.debug('hiding %s' % parts[j].getName())
                elif hide3 != None and parts[j].getName().find(hide3) != -1:
                    parts[j].stash()
                    self.notify.debug('hiding %s' % parts[j].getName())
                elif hide4 != None and parts[j].getName().find(hide4) != -1:
                    parts[j].stash()
                    self.notify.debug('hiding %s' % parts[j].getName())

        return

    def handleLayer3Hiding(self, clothingLayer, layer2Element, layer1Element, hideAll=False):
        for i in range(0, len(layer2Element[0])):
            parts = clothingLayer[layer2Element[0][i]]
            for j in range(0, parts.getNumPaths()):
                if hideAll:
                    parts[j].stash()
                    self.notify.debug('hiding %s' % parts[j].getName())
                elif parts[j].getName().find('front') < 0:
                    parts[j].stash()
                    self.notify.debug('hiding %s' % parts[j].getName())

        if layer1Element == None:
            return
        for i in range(0, len(layer1Element[0])):
            parts = self.clothingsLayer1[layer1Element[0][i]]
            for j in range(0, parts.getNumPaths()):
                if hideAll:
                    parts[j].stash()
                elif parts[j].getName().find('front') < 0:
                    if parts[j].getName().find('vcut') < 0:
                        parts[j].stash()

        return

    def getTattooBaseTexture(self):
        return 'female_tattoomap'

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

    def handleJewelryOptions(self, key, increment=True):
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
            self.jewelrySets[key][idx][0].setColorScale(primaryColor)
        self.jewelrySets[key][idx][1].unstash()
        if secondaryColor:
            self.jewelrySets[key][idx][1].setColorScale(secondaryColor)
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
        self.notify.debug('Zombie? %s' % zombie)
        if self.pirate.style == None:
            self.clothingsShirt[0][0].unstash()
            self.clothingsPant[0][0].unstash()
            self.bodys[5].stash()
            self.bodys[10].stash()
            self.bodys[11].stash()
        else:
            if zombie:
                self.makeZombie()
            self.handleClothesHiding()
            self.hairIdx = self.pirate.style.getHairHair()
            self.handleJewelryHiding()
            self.handleHeadHiding()
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
        tex = self.clothesTextures.findTexture(clothes_textures['PANT'][1][0][0])

        def getBasicData():
            return {'tallBoot': {'belt': {'noCoat': NodePathCollection(),'longCoat': NodePathCollection(),'shortCoat': NodePathCollection(),'navyCoat': NodePathCollection()},'lowVest': {'noCoat': NodePathCollection(),'longCoat': NodePathCollection(),'shortCoat': NodePathCollection(),'navyCoat': NodePathCollection()},'neither': {'noCoat': NodePathCollection(),'longCoat': NodePathCollection(),'shortCoat': NodePathCollection(),'navyCoat': NodePathCollection()}},'shortBoot': {'belt': {'noCoat': NodePathCollection(),'longCoat': NodePathCollection(),'shortCoat': NodePathCollection(),'navyCoat': NodePathCollection()},'lowVest': {'noCoat': NodePathCollection(),'longCoat': NodePathCollection(),'shortCoat': NodePathCollection(),'navyCoat': NodePathCollection()},'neither': {'noCoat': NodePathCollection(),'longCoat': NodePathCollection(),'shortCoat': NodePathCollection(),'navyCoat': NodePathCollection()}}}

        for pantIdx in xrange(len(self.clothingsPant)):
            pant = self.clothingsPant[pantIdx]
            texName = clothes_textures['PANT'][pantIdx][0]
            tex = self.texDict.get(texName[0])
            flattenedSet = getBasicData()
            for lod in ['2000', '1000', '500']:
                pantData = getBasicData()
                for idx in pant[0]:
                    pieceSet = self.layer1LODs[idx][lod]
                    for i in xrange(pieceSet.getNumPaths()):
                        piece = pieceSet[i]
                        name = piece.getName()
                        longCoat = False
                        shortCoat = False
                        navyCoat = False
                        anyCoat = False
                        skirt = pantIdx == 2
                        belt = False
                        lowVest = False
                        tallBoot = False
                        if name.find('interior') < 0:
                            anyCoat = True
                        if name.find('side') < 0:
                            if name.find('longcoat') < 0:
                                if name.find('tails') < 0:
                                    longCoat = True
                                if name.find('navyCoat') < 0:
                                    navyCoat = True
                                if anyCoat and name.find('back') < 0:
                                    shortCoat = True
                            if name.find('belt') < 0:
                                belt = True
                                if name.find('_abs') < 0:
                                    lowVest = True
                            if name.find('knee') < 0 and name.find('uppercalf') < 0:
                                tallBoot = True
                            pantData['shortBoot']['neither']['noCoat'].addPath(piece)
                            if skirt:
                                if longCoat:
                                    pantData['shortBoot']['neither']['longCoat'].addPath(piece)
                                if shortCoat:
                                    pantData['shortBoot']['neither']['shortCoat'].addPath(piece)
                                if navyCoat:
                                    pantData['shortBoot']['neither']['navyCoat'].addPath(piece)
                            elif anyCoat:
                                pantData['shortBoot']['neither']['longCoat'].addPath(piece)
                                pantData['shortBoot']['neither']['shortCoat'].addPath(piece)
                                pantData['shortBoot']['neither']['navyCoat'].addPath(piece)
                            if belt:
                                pantData['shortBoot']['belt']['noCoat'].addPath(piece)
                                if skirt:
                                    if longCoat:
                                        pantData['shortBoot']['belt']['longCoat'].addPath(piece)
                                    if shortCoat:
                                        pantData['shortBoot']['belt']['shortCoat'].addPath(piece)
                                    if navyCoat:
                                        pantData['shortBoot']['belt']['navyCoat'].addPath(piece)
                                elif anyCoat:
                                    pantData['shortBoot']['belt']['longCoat'].addPath(piece)
                                    pantData['shortBoot']['belt']['shortCoat'].addPath(piece)
                                    pantData['shortBoot']['belt']['navyCoat'].addPath(piece)
                            if lowVest:
                                pantData['shortBoot']['lowVest']['noCoat'].addPath(piece)
                                if skirt:
                                    if longCoat:
                                        pantData['shortBoot']['lowVest']['longCoat'].addPath(piece)
                                    if shortCoat:
                                        pantData['shortBoot']['lowVest']['shortCoat'].addPath(piece)
                                elif anyCoat:
                                    pantData['shortBoot']['lowVest']['longCoat'].addPath(piece)
                                    pantData['shortBoot']['lowVest']['shortCoat'].addPath(piece)
                                    pantData['shortBoot']['lowVest']['navyCoat'].addPath(piece)
                        elif tallBoot:
                            pantData['tallBoot']['neither']['noCoat'].addPath(piece)
                            if skirt:
                                if longCoat:
                                    pantData['tallBoot']['neither']['longCoat'].addPath(piece)
                                if shortCoat:
                                    pantData['tallBoot']['neither']['shortCoat'].addPath(piece)
                                if navyCoat:
                                    pantData['tallBoot']['neither']['navyCoat'].addPath(piece)
                            elif anyCoat:
                                pantData['tallBoot']['neither']['longCoat'].addPath(piece)
                                pantData['tallBoot']['neither']['shortCoat'].addPath(piece)
                                pantData['tallBoot']['neither']['navyCoat'].addPath(piece)
                            if belt:
                                pantData['tallBoot']['belt']['noCoat'].addPath(piece)
                                if skirt:
                                    if longCoat:
                                        pantData['tallBoot']['belt']['longCoat'].addPath(piece)
                                    if shortCoat:
                                        pantData['tallBoot']['belt']['shortCoat'].addPath(piece)
                                    if navyCoat:
                                        pantData['tallBoot']['belt']['navyCoat'].addPath(piece)
                                elif anyCoat:
                                    pantData['tallBoot']['belt']['longCoat'].addPath(piece)
                                    pantData['tallBoot']['belt']['shortCoat'].addPath(piece)
                                    pantData['tallBoot']['belt']['navyCoat'].addPath(piece)
                            if lowVest:
                                pantData['tallBoot']['lowVest']['noCoat'].addPath(piece)
                                if skirt:
                                    if longCoat:
                                        pantData['tallBoot']['lowVest']['longCoat'].addPath(piece)
                                    if shortCoat:
                                        pantData['tallBoot']['lowVest']['shortCoat'].addPath(piece)
                                    if navyCoat:
                                        pantData['tallBoot']['lowVest']['navyCoat'].addPath(piece)
                                elif anyCoat:
                                    pantData['tallBoot']['lowVest']['longCoat'].addPath(piece)
                                    pantData['tallBoot']['lowVest']['shortCoat'].addPath(piece)
                                    pantData['tallBoot']['lowVest']['navyCoat'].addPath(piece)

                for style1 in ['shortBoot', 'tallBoot']:
                    for style2 in ['belt', 'lowVest', 'neither']:
                        for style3 in ['shortCoat', 'longCoat', 'noCoat', 'navyCoat']:
                            data = pantData[style1][style2][style3]
                            geomSet = self.flattenData(data, lod, tex)
                            flattenedSet[style1][style2][style3].addPathsFrom(geomSet)

            self.pantSets.append(flattenedSet)

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
            if shoeIdx != 4:
                combinedSet = NodePathCollection()
                flattenedSet = {'pants': combinedSet,'skirt': combinedSet}
            else:
                flattenedSet = {'pants': NodePathCollection(),'skirt': NodePathCollection()}
            for lod in ['2000', '1000', '500']:
                shoeData = {'pants': NodePathCollection(),'skirt': NodePathCollection()}
                for idx in shoe[0]:
                    pieceSet = self.layer1LODs[idx][lod]
                    for i in xrange(pieceSet.getNumPaths()):
                        piece = pieceSet[i]
                        if shoeIdx == 4:
                            if piece.getName().find('top') < 0:
                                shoeData['skirt'].addPath(piece)
                        shoeData['pants'].addPath(piece)

                data = shoeData
                if shoeIdx == 4:
                    geomSet = self.flattenData(data['skirt'], lod, tex)
                    flattenedSet['skirt'].addPathsFrom(geomSet)
                geomSet = self.flattenData(data['pants'], lod, tex)
                flattenedSet['pants'].addPathsFrom(geomSet)

            self.shoeSets.append(flattenedSet)

    def generateShirtSets(self):
        self.shirtSets = []
        tex = self.clothesTextures.findTexture(clothes_textures['SHIRT'][1][0][0])

        def getBasicData():
            return {'belt': {'coat': {'vest1': NodePathCollection(),'vest2': NodePathCollection(),'neither': NodePathCollection()},'noCoat': {'vest1': NodePathCollection(),'vest2': NodePathCollection(),'neither': NodePathCollection()}},'nobelt': {'coat': NodePathCollection(),'noCoat': NodePathCollection()}}

        for shirtIdx in xrange(len(self.clothingsShirt)):
            shirt = self.clothingsShirt[shirtIdx]
            texName = clothes_textures['SHIRT'][shirtIdx][0]
            tex = self.texDict.get(texName[0])
            flattenedSet = getBasicData()
            for lod in ['2000', '1000', '500']:
                shirtData = getBasicData()
                for idx in shirt[0]:
                    pieceSet = self.layer1LODs[idx][lod]
                    for i in xrange(pieceSet.getNumPaths()):
                        piece = pieceSet[i]
                        name = piece.getName()
                        front = name.find('front') < 0
                        belt = name.find('belt') < 0
                        coat = not front or not name.find('vcut') < 0
                        vest2 = belt and name.find('base') < 0 and front and name.find('waist') < 0
                        vest1 = vest2 and name.find('low_vcut') < 0 and name.find('breast') < 0
                        shirtData['nobelt']['noCoat'].addPath(piece)
                        if coat:
                            shirtData['nobelt']['coat'].addPath(piece)
                        if belt:
                            shirtData['belt']['noCoat']['neither'].addPath(piece)
                            if vest1:
                                shirtData['belt']['noCoat']['vest1'].addPath(piece)
                            if vest2:
                                shirtData['belt']['noCoat']['vest2'].addPath(piece)
                            if coat:
                                shirtData['belt']['coat']['neither'].addPath(piece)
                                if vest1:
                                    shirtData['belt']['coat']['vest1'].addPath(piece)
                                if vest2:
                                    shirtData['belt']['coat']['vest2'].addPath(piece)

                for style2 in ['coat', 'noCoat']:
                    for style3 in ['vest1', 'vest2', 'neither']:
                        data = shirtData['belt'][style2][style3]
                        geomSet = self.flattenData(data, lod, tex)
                        flattenedSet['belt'][style2][style3].addPathsFrom(geomSet)

                for style2 in ['coat', 'noCoat']:
                    data = shirtData['nobelt'][style2]
                    geomSet = self.flattenData(data, lod, tex)
                    flattenedSet['nobelt'][style2].addPathsFrom(geomSet)

            self.shirtSets.append(flattenedSet)

    def generateVestSets(self):

        def getBasicData():
            return {'belt': {'coat': {'pants': NodePathCollection(),'skirt': NodePathCollection()},'noCoat': {'pants': NodePathCollection(),'skirt': NodePathCollection()}},'nobelt': {'coat': {'pants': NodePathCollection(),'skirt': NodePathCollection()},'noCoat': {'pants': NodePathCollection(),'skirt': NodePathCollection()}}}

        self.vestSets = []
        for vestIdx in xrange(len(self.clothingsVest)):
            vest = self.clothingsVest[vestIdx]
            texName = clothes_textures['VEST'][vestIdx][0]
            tex = self.texDict.get(texName[0])
            flattenedSet = getBasicData()
            for lod in ['2000', '1000', '500']:
                vestData = getBasicData()
                for idx in vest[0]:
                    pieceSet = self.layer2LODs[idx][lod]
                    for i in xrange(pieceSet.getNumPaths()):
                        piece = pieceSet[i]
                        name = piece.getName()
                        pants = name.find('bottom_skirt') < 0
                        skirt = name.find('bottom_pant') < 0
                        belt = name.find('belt') < 0
                        coat = name.find('front') >= 0
                        if pants:
                            vestData['nobelt']['noCoat']['pants'].addPath(piece)
                        if skirt:
                            vestData['nobelt']['noCoat']['skirt'].addPath(piece)
                        if coat:
                            if pants:
                                vestData['nobelt']['coat']['pants'].addPath(piece)
                            if skirt:
                                vestData['nobelt']['coat']['skirt'].addPath(piece)
                        if belt:
                            if pants:
                                vestData['belt']['noCoat']['pants'].addPath(piece)
                            if skirt:
                                vestData['belt']['noCoat']['skirt'].addPath(piece)
                            if coat:
                                if pants:
                                    vestData['belt']['coat']['pants'].addPath(piece)
                                if skirt:
                                    vestData['belt']['coat']['skirt'].addPath(piece)

                for style1 in ['belt', 'nobelt']:
                    for style2 in ['coat', 'noCoat']:
                        for style3 in ['pants', 'skirt']:
                            data = vestData[style1][style2][style3]
                            geomSet = self.flattenData(data, lod, tex)
                            flattenedSet[style1][style2][style3].addPathsFrom(geomSet)

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
        tex = self.clothesTextures.findTexture(clothes_textures['VEST'][1][0][0].split('+')[0])
        for beltIdx in xrange(len(self.clothingsBelt)):
            belt = self.clothingsBelt[beltIdx]
            texName = clothes_textures['BELT'][beltIdx][0]
            tex = self.texDict.get(texName[0])
            flattenedSet = {'full': [NodePathCollection(), NodePathCollection()],'coat3': [NodePathCollection(), NodePathCollection()]}
            for lod in ['2000', '1000', '500']:
                beltData = {'full': [NodePathCollection(), NodePathCollection()],'coat3': [NodePathCollection(), NodePathCollection()]}
                idx1 = belt[0][0]
                pieceSet1 = self.layer2LODs[idx1][lod]
                for i in xrange(pieceSet1.getNumPaths()):
                    piece = pieceSet1[i]
                    name = piece.getName()
                    beltData['full'][0].addPath(piece)
                    if name.find('_cloth') < 0 and name.find('interior') < 0:
                        beltData['coat3'][0].addPath(piece)

                if len(belt[0]) > 2:
                    idx3 = belt[0][2]
                    pieceSet3 = self.layer2LODs[idx3][lod]
                    for i in xrange(pieceSet3.getNumPaths()):
                        piece = pieceSet3[i]
                        name = piece.getName()
                        beltData['full'][0].addPath(piece)
                        if name.find('_cloth') < 0 and name.find('interior') < 0:
                            beltData['coat3'][0].addPath(piece)

                if len(belt[0]) > 1:
                    idx2 = belt[0][1]
                    pieceSet2 = self.layer2LODs[idx2][lod]
                    for i in xrange(pieceSet2.getNumPaths()):
                        piece = pieceSet2[i]
                        name = piece.getName()
                        beltData['full'][1].addPath(piece)
                        if name.find('_cloth') < 0 and name.find('interior') < 0:
                            beltData['coat3'][0].addPath(piece)

                for style in ['full', 'coat3']:
                    for i in [0, 1]:
                        data = beltData[style]
                        flattenNode = NodePath('flatten Me')
                        for j in xrange(data[i].getNumPaths()):
                            nc = data[i][j]
                            nc.copyTo(flattenNode)

                        flattenNode.flattenStrong()
                        geomSet = flattenNode.findAllMatches('**/+GeomNode')
                        geomSet.reparentTo(self.pirate.getLOD(lod).getChild(0))
                        self.stripTexture(geomSet)
                        geomSet.stash()
                        flattenNode.removeNode()
                        flattenedSet[style][i].addPathsFrom(geomSet)

            self.beltSets.append(flattenedSet)

    def generateHairSets(self):
        cuts = [
         '', 'cut_c', 'cut_c', 'cut_c', 'cut_e', 'cut_c', 'cut_d', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c', 'cut_c']

        def getBasicData():
            data = []
            for i in xrange(len(self.hats)):
                data.append(NodePathCollection())

            return data

        dreads = self.hairPieces[14]
        for i in range(dreads.getNumPaths()):
            if dreads[i].getName().find('acc') >= 0:
                dreads[i].setColorScaleOff(10)

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
                        hairCut = self.hairCutLODs[partIdx][lod]
                        if hatIdx == 0 or partIdx == 14:
                            hairIndices.add(partIdx)
                            hairData.addPathsFrom(hair)
                        else:
                            cutFound = 0
                            for j in xrange(hairCut.getNumPaths()):
                                if hairCut[j].getName().find(cuts[hatIdx]) >= 0:
                                    hairCutIndices.add(partIdx)
                                    hairData.addPath(hairCut[j])
                                    cutFound = 1
                                elif hatIdx == 6:
                                    if hairCut[j].getName().find(cuts[hatIdx + 1]) >= 0:
                                        hairCutIndices.add(partIdx)
                                        hairData.addPath(hairCut[j])
                                        cutFound = 1

                            if not cutFound:
                                if partIdx == 2:
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
                        if 14 in self.hairs[hairIdx]:
                            geomSet = self.flattenData(hairData, lod, False, 'hair_dreads')
                        else:
                            geomSet = self.flattenData(hairData, lod, False)
                        flattenedSet[hatIdx].addPathsFrom(geomSet)
                        dataCache[lod][hatIdx, t1, t2] = geomSet

            self.hairSets.append(flattenedSet)

        self.dataCache = dataCache

    def flattenSet(self, parts, layerSet, lod, texStrip=True):
        flattenMe = NodePath('flattenMe')
        for i in parts:
            geomData = layerSet[i][lod]
            for j in xrange(geomData.getNumPaths()):
                geomData[j].copyTo(flattenMe)

        flattenMe.flattenStrong()
        geomSet = flattenMe.findAllMatches('**/+GeomNode')
        if texStrip:
            self.stripTexture(geomSet)
        geomSet.reparentTo(self.pirate.getLOD(lod).getChild(0))
        geomSet.stash()
        return geomSet

    def flattenData(self, geomData, lod, texStrip=True, overrideNode=None, flattenStrong=True):
        flattenMe = NodePath('flattenMe')
        for i in xrange(geomData.getNumPaths()):
            geomData[i].copyTo(flattenMe)

        if flattenStrong:
            flattenMe.flattenStrong()
        if lod == '500':
            gr = SceneGraphReducer()
            gr.makeCompatibleFormat(flattenMe.node(), 0)
        geomSet = flattenMe.findAllMatches('**/+GeomNode')
        if texStrip:
            self.stripTexture(geomSet)
        if overrideNode:
            overrideNP = self.pirate.getLOD(lod).getChild(0).attachNewNode(overrideNode)
            geomSet.reparentTo(overrideNP)
            geomSet = NodePathCollection()
            geomSet.addPath(overrideNP)
        else:
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
            geomNode = geomSet[i].node()
            for j in xrange(geomNode.getNumGeoms()):
                geomState = geomNode.getGeomState(j)
                geomNode.setGeomState(j, geomState.removeAttrib(TextureAttrib.getClassType()))