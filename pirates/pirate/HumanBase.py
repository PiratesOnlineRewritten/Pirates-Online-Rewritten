from pirates.pirate import HumanDNA
import copy

class HumanBase():

    def setDNA(self, dna=None):
        self.setDNAString(dna)

    def setDNAString(self, dnaString=None):
        if not dnaString:
            self.setDefaultDNA()
        else:
            self.style = copy.deepcopy(dnaString)

    def setDefaultDNA(self):
        newDNA = HumanDNA.HumanDNA()
        self.style = newDNA

    def setTutorial(self, val):
        self.style.setTutorial(val)

    def d_setTutorial(self, val):
        self.sendUpdate('setTutorial', [val])

    def b_setTutorial(self, val):
        self.setTutorial(val)
        self.d_setTutorial(val)

    def setName(self, val):
        self.style.setName(val)

    def setGender(self, val):
        self.style.setGender(val)

    def d_setGender(self, val):
        self.sendUpdate('setGender', [val])

    def b_setGender(self, val):
        self.setGender(val)
        self.d_setGender(val)

    def setBodyShape(self, val):
        self.style.setBodyShape(val)

    def d_setBodyShape(self, val):
        self.sendUpdate('setBodyShape', [val])

    def b_setBodyShape(self, val):
        self.setBodyShape(val)
        self.d_setBodyShape(val)

    def setBodyHeight(self, val):
        self.style.setBodyHeight(val)

    def d_setBodyHeight(self, val):
        self.sendUpdate('setBodyHeight', [val])

    def b_setBodyHeight(self, val):
        self.setBodyHeight(val)
        self.d_setBodyHeight(val)

    def setBodyColor(self, val):
        self.style.setBodyColor(val)

    def d_setBodyColor(self, val):
        self.sendUpdate('setBodyColor', [val])

    def b_setBodyColor(self, val):
        self.setBodyColor(val)
        self.d_setBodyColor(val)

    def setBodySkin(self, val):
        self.style.setBodySkin(val)

    def d_setBodySkin(self, val):
        self.sendUpdate('setBodySkin', [val])

    def b_setBodySkin(self, val):
        self.setBodySkin(val)
        self.d_setBodySkin(val)

    def setHeadSize(self, val):
        self.style.setHeadSize(val)

    def d_setHeadSize(self, val):
        self.sendUpdate('setHeadSize', [val])

    def b_setHeadSize(self, val):
        self.setHeadSize(val)
        self.d_setHeadSize(val)

    def setHeadWidth(self, val):
        self.style.setHeadWidth(val)

    def d_setHeadWidth(self, val):
        self.sendUpdate('setHeadWidth', [val])

    def b_setHeadWidth(self, val):
        self.setHeadWidth(val)
        self.d_setHeadWidth(val)

    def setHeadHeight(self, val):
        self.style.setHeadHeight(val)

    def d_setHeadHeight(self, val):
        self.sendUpdate('setHeadHeight', [val])

    def b_setHeadHeight(self, val):
        self.setHeadHeight(val)
        self.d_setHeadHeight(val)

    def setHeadRoundness(self, val):
        self.style.setHeadRoundness(val)

    def d_setHeadRoundness(self, val):
        self.sendUpdate('setHeadRoundness', [val])

    def b_setHeadRoundness(self, val):
        self.setHeadRoundness(val)
        self.d_setHeadRoundness(val)

    def setJawWidth(self, val):
        self.style.setJawWidth(val)

    def d_setJawWidth(self, val):
        self.sendUpdate('setJawWidth', [val])

    def b_setJawWidth(self, val):
        self.setJawWidth(val)
        self.d_setJawWidth(val)

    def setJawRoundness(self, val):
        self.style.setJawRoundness(val)

    def d_setJawRoundness(self, val):
        self.sendUpdate('setJawRoundness', [val])

    def b_setJawRoundness(self, val):
        self.setJawRoundness(val)
        self.d_setJawRoundness(val)

    def setJawAngle(self, val):
        self.style.setJawAngle(val)

    def d_setJawAngle(self, val):
        self.sendUpdate('setJawAngle', [val])

    def b_setJawAngle(self, val):
        self.setJawAngle(val)
        self.d_setJawAngle(val)

    def setJawLength(self, val):
        self.style.setJawLength(val)

    def d_setJawLength(self, val):
        self.sendUpdate('setJawLength', [val])

    def b_setJawLength(self, val):
        self.setJawLength(val)
        self.d_setJawLength(val)

    def setMouthWidth(self, val):
        self.style.setMouthWidth(val)

    def d_setMouthWidth(self, val):
        self.sendUpdate('setMouthWidth', [val])

    def b_setMouthWidth(self, val):
        self.setMouthWidth(val)
        self.d_setMouthWidth(val)

    def setMouthLipThickness(self, val):
        self.style.setMouthLipThickness(val)

    def d_setMouthLipThickness(self, val):
        self.sendUpdate('setMouthLipThickness', [val])

    def b_setMouthLipThickness(self, val):
        self.setMouthLipThickness(val)
        self.d_setMouthLipThickness(val)

    def setMouthFrown(self, val):
        self.style.setMouthFrown(val)

    def d_setMouthFrown(self, val):
        self.sendUpdate('setMouthFrown', [val])

    def b_setMouthFrown(self, val):
        self.setMouthFrown(val)
        self.d_setMouthFrown(val)

    def setCheekBoneHeight(self, val):
        self.style.setCheekBoneHeight(val)

    def d_setCheekBoneHeight(self, val):
        self.sendUpdate('setCheekBoneHeight', [val])

    def b_setCheekBoneHeight(self, val):
        self.setCheekBoneHeight(val)
        self.d_setCheekBoneHeight(val)

    def setCheekBoneWidth(self, val):
        self.style.setCheekBoneWidth(val)

    def d_setCheekBoneWidth(self, val):
        self.sendUpdate('setCheekBoneWidth', [val])

    def b_setCheekBoneWidth(self, val):
        self.setCheekBoneWidth(val)
        self.d_setCheekBoneWidth(val)

    def setCheekFat(self, val):
        self.style.setCheekFat(val)

    def d_setCheekFat(self, val):
        self.sendUpdate('setCheekFat', [val])

    def b_setCheekFat(self, val):
        self.setCheekFat(val)
        self.d_setCheekFat(val)

    def setBrowWidth(self, val):
        self.style.setBrowWidth(val)

    def d_setBrowWidth(self, val):
        self.sendUpdate('setBrowWidth', [val])

    def b_setBrowWidth(self, val):
        self.setBrowWidth(val)
        self.d_setBrowWidth(val)

    def setBrowProtruding(self, val):
        self.style.setBrowProtruding(val)

    def d_setBrowProtruding(self, val):
        self.sendUpdate('setBrowProtruding', [val])

    def b_setBrowProtruding(self, val):
        self.setBrowProtruding(val)
        self.d_setBrowProtruding(val)

    def setBrowAngle(self, val):
        self.style.setBrowAngle(val)

    def d_setBrowAngle(self, val):
        self.sendUpdate('setBrowAngle', [val])

    def b_setBrowAngle(self, val):
        self.setBrowAngle(val)
        self.d_setBrowAngle(val)

    def setBrowHeight(self, val):
        self.style.setBrowHeight(val)

    def d_setBrowHeight(self, val):
        self.sendUpdate('setBrowHeight', [val])

    def b_setBrowHeight(self, val):
        self.setBrowHeight(val)
        self.d_setBrowHeight(val)

    def setEyeCorner(self, val):
        self.style.setEyeCorner(val)

    def d_setEyeCorner(self, val):
        self.sendUpdate('setEyeCorner', [val])

    def b_setEyeCorner(self, val):
        self.setEyeCorner(val)
        self.d_setEyeCorner(val)

    def setEyeOpeningSize(self, val):
        self.style.setEyeOpeningSize(val)

    def d_setEyeOpeningSize(self, val):
        self.sendUpdate('setEyeOpeningSize', [val])

    def b_setEyeOpeningSize(self, val):
        self.setEyeOpeningSize(val)
        self.d_setEyeOpeningSize(val)

    def setEyeBulge(self, val):
        self.style.setEyeBulge(val)

    def d_setEyeBulge(self, val):
        self.sendUpdate('setEyeBulge', [val])

    def b_setEyeBulge(self, val):
        self.setEyeBulge(val)
        self.d_setEyeBulge(val)

    def setNoseBridgeWidth(self, val):
        self.style.setNoseBridgeWidth(val)

    def d_setNoseBridgeWidth(self, val):
        self.sendUpdate('setNoseBridgeWidth', [val])

    def b_setNoseBridgeWidth(self, val):
        self.setNoseBridgeWidth(val)
        self.d_setNoseBridgeWidth(val)

    def setNoseNostrilWidth(self, val):
        self.style.setNoseNostrilWidth(val)

    def d_setNoseNostrilWidth(self, val):
        self.sendUpdate('setNoseNostrilWidth', [val])

    def b_setNoseNostrilWidth(self, val):
        self.setNoseNostrilWidth(val)
        self.d_setNoseNostrilWidth(val)

    def setNoseLength(self, val):
        self.style.setNoseLength(val)

    def d_setNoseLength(self, val):
        self.sendUpdate('setNoseLength', [val])

    def b_setNoseLength(self, val):
        self.setNoseLength(val)
        self.d_setNoseLength(val)

    def setNoseBump(self, val):
        self.style.setNoseBump(val)

    def d_setNoseBump(self, val):
        self.sendUpdate('setNoseBump', [val])

    def b_setNoseBump(self, val):
        self.setNoseBump(val)
        self.d_setNoseBump(val)

    def setNoseNostrilHeight(self, val):
        self.style.setNoseNostrilHeight(val)

    def d_setNoseNostrilHeight(self, val):
        self.sendUpdate('setNoseNostrilHeight', [val])

    def b_setNoseNostrilHeight(self, val):
        self.setNoseNostrilHeight(val)
        self.d_setNoseNostrilHeight(val)

    def setNoseNostrilAngle(self, val):
        self.style.setNoseNostrilAngle(val)

    def d_setNoseNostrilAngle(self, val):
        self.sendUpdate('setNoseNostrilAngle', [val])

    def b_setNoseNostrilAngle(self, val):
        self.setNoseNostrilAngle(val)
        self.d_setNoseNostrilAngle(val)

    def setNoseNostrilIndent(self, val):
        self.style.setNoseNostrilIndent(val)

    def d_setNoseNostrilIndent(self, val):
        self.sendUpdate('setNoseNostrilIndent', [val])

    def b_setNoseNostrilIndent(self, val):
        self.setNoseNostrilIndent(val)
        self.d_setNoseNostrilIndent(val)

    def setNoseBridgeBroke(self, val):
        self.style.setNoseBridgeBroke(val)

    def d_setNoseBridgeBroke(self, val):
        self.sendUpdate('setNoseBridgeBroke', [val])

    def b_setNoseBridgeBroke(self, val):
        self.setNoseBridgeBroke(val)
        self.d_setNoseBridgeBroke(val)

    def setNoseNostrilBroke(self, val):
        self.style.setNoseNostrilBroke(val)

    def d_setNoseNostrilBroke(self, val):
        self.sendUpdate('setNoseNostrilBroke', [val])

    def b_setNoseNostrilBroke(self, val):
        self.setNoseNostrilBroke(val)
        self.d_setNoseNostrilBroke(val)

    def setEarScale(self, val):
        self.style.setEarScale(val)

    def d_setEarScale(self, val):
        self.sendUpdate('setEarScale', [val])

    def b_setEarScale(self, val):
        self.setEarScale(val)
        self.d_setEarScale(val)

    def setEarFlapAngle(self, val):
        self.style.setEarFlapAngle(val)

    def d_setEarFlapAngle(self, val):
        self.sendUpdate('setEarFlapAngle', [val])

    def b_setEarFlapAngle(self, val):
        self.setEarFlapAngle(val)
        self.d_setEarFlapAngle(val)

    def setEarPosition(self, val):
        self.style.setEarPosition(val)

    def d_setEarPosition(self, val):
        self.sendUpdate('setEarPosition', [val])

    def b_setEarPosition(self, val):
        self.setEarPosition(val)
        self.d_setEarPosition(val)

    def setEarLobe(self, val):
        self.style.setEarLobe(val)

    def d_setEarLobe(self, val):
        self.sendUpdate('setEarLobe', [val])

    def b_setEarLobe(self, val):
        self.setEarLobe(val)
        self.d_setEarLobe(val)

    def setHeadTexture(self, val):
        self.style.setHeadTexture(val)

    def d_setHeadTexture(self, val):
        self.sendUpdate('setHeadTexture', [val])

    def b_setHeadTexture(self, val):
        self.setHeadTexture(val)
        self.d_setHeadTexture(val)

    def setEyesColor(self, val):
        self.style.setEyesColor(val)

    def d_setEyesColor(self, val):
        self.sendUpdate('setEyesColor', [val])

    def b_setEyesColor(self, val):
        self.setEyesColor(val)
        self.d_setEyesColor(val)

    def setHairHair(self, val):
        self.style.setHairHair(val)

    def d_setHairHair(self, val):
        self.sendUpdate('setHairHair', [val])

    def b_setHairHair(self, val):
        self.setHairHair(val)
        self.d_setHairHair(val)

    def setHairBeard(self, val):
        self.style.setHairBeard(val)

    def d_setHairBeard(self, val):
        self.sendUpdate('setHairBeard', [val])

    def b_setHairBeard(self, val):
        self.setHairBeard(val)
        self.d_setHairBeard(val)

    def setHairMustache(self, val):
        self.style.setHairMustache(val)

    def d_setHairMustache(self, val):
        self.sendUpdate('setHairMustache', [val])

    def b_setHairMustache(self, val):
        self.setHairMustache(val)
        self.d_setHairMustache(val)

    def setHairColor(self, val):
        self.style.setHairColor(val)

    def d_setHairColor(self, val):
        self.sendUpdate('setHairColor', [val])

    def b_setHairColor(self, val):
        self.setHairColor(val)
        self.d_setHairColor(val)

    def setHatIdx(self, val):
        self.style.setHatIdx(val)

    def d_setHatIdx(self, val):
        self.sendUpdate('setHatIdx', [val])

    def b_setHatIdx(self, val):
        self.setHatIdx(val)
        self.d_setHatIdx(val)

    def setHatTexture(self, val):
        self.style.setHatTexture(val)

    def setHatColor(self, val):
        self.style.setHatColor(val)

    def d_setHatColor(self, val):
        self.sendUpdate('setHatColor', [val])

    def b_setHatColor(self, val):
        self.setHatColor(val)
        self.d_setHatColor(val)

    def setClothesByType(self, type, val1, val2, val3=-1):
        self.style.setClothesByType(type, val1, val2, val3)

    def setClothesShirt(self, val1, val2):
        self.style.setClothesShirt(val1, val2)

    def d_setClothesShirt(self, val1, val2):
        self.sendUpdate('setClothesShirt', [val1, val2])

    def b_setClothesShirt(self, val1, val2):
        self.setClothesShirt(val1, val2)
        self.d_setClothesShirt(val1, val2)

    def setClothesPant(self, val1, val2):
        self.style.setClothesPant(val1, val2)

    def d_setClothesPant(self, val1, val2):
        self.sendUpdate('setClothesPant', [val1, val2])

    def b_setClothesPant(self, val1, val2):
        self.setClothesPant(val1, val2)
        self.d_setClothesPant(val1, val2)

    def setClothesSock(self, val1, val2):
        self.style.setClothesSock(val1, val2)

    def d_setClothesSock(self, val1, val2):
        self.sendUpdate('setClothesSock', [val1, val2])

    def b_setClothesSock(self, val1, val2):
        self.setClothesSock(val1, val2)
        self.d_setClothesSock(val1, val2)

    def setClothesShoe(self, val1, val2):
        self.style.setClothesShoe(val1, val2)

    def d_setClothesShoe(self, val1, val2):
        self.sendUpdate('setClothesShoe', [val1, val2])

    def b_setClothesShoe(self, val1, val2):
        self.setClothesShoe(val1, val2)
        self.d_setClothesShoe(val1, val2)

    def setClothesVest(self, val1, val2):
        self.style.setClothesVest(val1, val2)

    def d_setClothesVest(self, val1, val2):
        self.sendUpdate('setClothesVest', [val1, val2])

    def b_setClothesVest(self, val1, val2):
        self.setClothesVest(val1, val2)
        self.d_setClothesVest(val1, val2)

    def setClothesCoat(self, val1, val2):
        self.style.setClothesCoat(val1, val2)

    def d_setClothesCoat(self, val1, val2):
        self.sendUpdate('setClothesCoat', [val1, val2])

    def b_setClothesCoat(self, val1, val2):
        self.setClothesCoat(val1, val2)
        self.d_setClothesCoat(val1, val2)

    def setClothesBelt(self, val1, val2):
        self.style.setClothesBelt(val1, val2)

    def d_setClothesBelt(self, val1, val2):
        self.sendUpdate('setClothesBelt', [val1, val2])

    def b_setClothesBelt(self, val1, val2):
        self.setClothesBelt(val1, val2)
        self.d_setClothesBelt(val1, val2)

    def setClothesTopColor(self, val1, val2, val3):
        self.style.setClothesTopColor(val1, val2, val3)

    def d_setClothesTopColor(self, val1, val2, val3):
        self.sendUpdate('setClothesTopColor', [val1, val2, val3])

    def b_setClothesTopColor(self, val1, val2, val3):
        self.setClothesTopColor(val1, val2, val3)
        self.d_setClothesTopColor(val1, val2, val3)

    def setClothesBotColor(self, val1, val2, val3):
        self.style.setClothesBotColor(val1, val2, val3)

    def d_setClothesBotColor(self, val1, val2, val3):
        self.sendUpdate('setClothesBotColor', [val1, val2, val3])

    def b_setClothesBotColor(self, val1, val2, val3):
        self.setClothesBotColor(val1, val2, val3)
        self.d_setClothesBotColor(val1, val2, val3)

    def setTattooChest(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.tattooChest = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def d_setTattooChest(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.sendUpdate('setTattooChest', [tattoo, offsetX, offsetY, scale, rotate, color])

    def b_setTattooChest(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.setTattooChest(tattoo, offsetX, offsetY, scale, rotate, color)
        self.d_setTattooChest(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone2(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.tattooZone2 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def d_setTattooZone2(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.sendUpdate('setTattooZone2', [tattoo, offsetX, offsetY, scale, rotate, color])

    def b_setTattooZone2(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.setTattooZone2(tattoo, offsetX, offsetY, scale, rotate, color)
        self.d_setTattooZone2(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone3(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.tattooZone3 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def d_setTattooZone3(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.sendUpdate('setTattooZone3', [tattoo, offsetX, offsetY, scale, rotate, color])

    def b_setTattooZone3(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.setTattooZone3(tattoo, offsetX, offsetY, scale, rotate, color)
        self.d_setTattooZone3(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone4(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.tattooZone4 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def d_setTattooZone4(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.sendUpdate('setTattooZone4', [tattoo, offsetX, offsetY, scale, rotate, color])

    def b_setTattooZone4(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.setTattooZone4(tattoo, offsetX, offsetY, scale, rotate, color)
        self.d_setTattooZone4(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone5(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.tattooZone5 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def d_setTattooZone5(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.sendUpdate('setTattooZone5', [tattoo, offsetX, offsetY, scale, rotate, color])

    def b_setTattooZone5(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.setTattooZone5(tattoo, offsetX, offsetY, scale, rotate, color)
        self.d_setTattooZone5(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone6(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.tattooZone6 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def d_setTattooZone6(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.sendUpdate('setTattooZone6', [tattoo, offsetX, offsetY, scale, rotate, color])

    def b_setTattooZone6(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.setTattooZone6(tattoo, offsetX, offsetY, scale, rotate, color)
        self.d_setTattooZone6(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone7(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.tattooZone7 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def d_setTattooZone7(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.sendUpdate('setTattooZone7', [tattoo, offsetX, offsetY, scale, rotate, color])

    def b_setTattooZone7(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.setTattooZone7(tattoo, offsetX, offsetY, scale, rotate, color)
        self.d_setTattooZone7(tattoo, offsetX, offsetY, scale, rotate, color)

    def setTattooZone8(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.style.tattooZone8 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def d_setTattooZone8(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.sendUpdate('setTattooZone8', [tattoo, offsetX, offsetY, scale, rotate, color])

    def b_setTattooZone8(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.setTattooZone8(tattoo, offsetX, offsetY, scale, rotate, color)
        self.d_setTattooZone8(tattoo, offsetX, offsetY, scale, rotate, color)

    def setJewelryZone1(self, val, primary=0, secondary=0):
        self.style.setJewelryZone1(val, primary, secondary)

    def d_setJewelryZone1(self, val, primary, secondary):
        self.sendUpdate('setJewelryZone1', [val, primary, secondary])

    def b_setJewelryZone1(self, val, primary, secondary):
        self.setJewelryZone1(val, primary, secondary)
        self.d_setJewelryZone1(val, primary, secondary)

    def setJewelryZone2(self, val, primary=0, secondary=0):
        self.style.setJewelryZone2(val, primary, secondary)

    def d_setJewelryZone2(self, val, primary, secondary):
        self.sendUpdate('setJewelryZone2', [val, primary, secondary])

    def b_setJewelryZone2(self, val, primary, secondary):
        self.setJewelryZone2(val, primary, secondary)
        self.d_setJewelryZone2(val, primary, secondary)

    def setJewelryZone3(self, val, primary=0, secondary=0):
        self.style.setJewelryZone3(val, primary, secondary)

    def d_setJewelryZone3(self, val, primary, secondary):
        self.sendUpdate('setJewelryZone3', [val, primary, secondary])

    def b_setJewelryZone3(self, val, primary, secondary):
        self.setJewelryZone3(val, primary, secondary)
        self.d_setJewelryZone3(val, primary, secondary)

    def setJewelryZone4(self, val, primary=0, secondary=0):
        self.style.setJewelryZone4(val, primary, secondary)

    def d_setJewelryZone4(self, val, primary, secondary):
        self.sendUpdate('setJewelryZone4', [val, primary, secondary])

    def b_setJewelryZone4(self, val, primary, secondary):
        self.setJewelryZone4(val, primary, secondary)
        self.d_setJewelryZone4(val, primary, secondary)

    def setJewelryZone5(self, val, primary=0, secondary=0):
        self.style.setJewelryZone5(val, primary, secondary)

    def d_setJewelryZone5(self, val, primary, secondary):
        self.sendUpdate('setJewelryZone5', [val, primary, secondary])

    def b_setJewelryZone5(self, val, primary, secondary):
        self.setJewelryZone5(val, primary, secondary)
        self.d_setJewelryZone5(val, primary, secondary)

    def setJewelryZone6(self, val, primary=0, secondary=0):
        self.style.setJewelryZone6(val, primary, secondary)

    def d_setJewelryZone6(self, val, primary, secondary):
        self.sendUpdate('setJewelryZone6', [val, primary, secondary])

    def b_setJewelryZone6(self, val, primary, secondary):
        self.setJewelryZone6(val, primary, secondary)
        self.d_setJewelryZone6(val, primary, secondary)

    def setJewelryZone7(self, val, primary=0, secondary=0):
        self.style.setJewelryZone7(val, primary, secondary)

    def d_setJewelryZone7(self, val, primary, secondary):
        self.sendUpdate('setJewelryZone7', [val, primary, secondary])

    def b_setJewelryZone7(self, val, primary, secondary):
        self.setJewelryZone7(val, primary, secondary)
        self.d_setJewelryZone7(val, primary, secondary)

    def setJewelryZone8(self, val, primary=0, secondary=0):
        self.style.setJewelryZone8(val, primary, secondary)

    def d_setJewelryZone8(self, val, primary, secondary):
        self.sendUpdate('setJewelryZone8', [val, primary, secondary])

    def b_setJewelryZone8(self, val, primary, secondary):
        self.setJewelryZone8(val, primary, secondary)
        self.d_setJewelryZone8(val, primary, secondary)

    def saveDNA(self, dna):
        self.b_setTutorial(dna.tutorial)
        self.b_setGender(dna.gender)
        self.b_setBodyShape(dna.getBodyShape())
        self.b_setBodyHeight(dna.getBodyHeight())
        self.b_setBodyColor(dna.getBodyColor())
        self.b_setBodySkin(dna.getBodySkin())
        self.b_setHeadSize(dna.getHeadSize())
        self.b_setHeadWidth(dna.getHeadWidth())
        self.b_setHeadHeight(dna.getHeadHeight())
        self.b_setHeadRoundness(dna.getHeadRoundness())
        self.b_setJawWidth(dna.getJawWidth())
        self.b_setJawRoundness(dna.getJawRoundness())
        self.b_setJawAngle(dna.getJawAngle())
        self.b_setMouthWidth(dna.getMouthWidth())
        self.b_setMouthLipThickness(dna.getMouthLipThickness())
        self.b_setMouthFrown(dna.getMouthFrown())
        self.b_setCheekBoneHeight(dna.getCheekBoneHeight())
        self.b_setCheekBoneWidth(dna.getCheekBoneWidth())
        self.b_setCheekFat(dna.getCheekFat())
        self.b_setBrowWidth(dna.getBrowWidth())
        self.b_setBrowProtruding(dna.getBrowProtruding())
        self.b_setBrowAngle(dna.getBrowAngle())
        self.b_setBrowHeight(dna.getBrowHeight())
        self.b_setEyeCorner(dna.getEyeCorner())
        self.b_setEyeOpeningSize(dna.getEyeOpeningSize())
        self.b_setEyeBulge(dna.getEyeBulge())
        self.b_setNoseBridgeWidth(dna.getNoseBridgeWidth())
        self.b_setNoseNostrilWidth(dna.getNoseNostrilWidth())
        self.b_setNoseLength(dna.getNoseLength())
        self.b_setNoseBump(dna.getNoseBump())
        self.b_setNoseNostrilHeight(dna.getNoseNostrilHeight())
        self.b_setNoseNostrilAngle(dna.getNoseNostrilAngle())
        self.b_setNoseBridgeBroke(dna.getNoseBridgeBroke())
        self.b_setNoseNostrilBroke(dna.getNoseNostrilBroke())
        self.b_setEarScale(dna.getEarScale())
        self.b_setEarFlapAngle(dna.getEarFlapAngle())
        self.b_setEarPosition(dna.getEarPosition())
        self.b_setEarLobe(dna.getEarLobe())
        self.b_setHeadTexture(dna.getHeadTexture())
        self.b_setHairHair(dna.getHairHair())
        self.b_setHairBeard(dna.getHairBeard())
        self.b_setHairMustache(dna.getHairMustache())
        self.b_setHairColor(dna.getHairColor())
        self.b_setHatIdx(dna.getHatIdx())
        self.b_setHatColor(dna.getHatColor())
        self.b_setEyesColor(dna.getEyesColor())
        self.b_setClothesShirt(dna.getClothesShirt()[0], dna.getClothesShirt()[1])
        self.b_setClothesPant(dna.getClothesPant()[0], dna.getClothesPant()[1])
        self.b_setClothesSock(dna.getClothesSock()[0], dna.getClothesSock()[1])
        self.b_setClothesShoe(dna.getClothesShoe()[0], dna.getClothesShoe()[1])
        self.b_setClothesVest(dna.getClothesVest()[0], dna.getClothesVest()[1])
        self.b_setClothesCoat(dna.getClothesCoat()[0], dna.getClothesCoat()[1])
        self.b_setClothesBelt(dna.getClothesBelt()[0], dna.getClothesBelt()[1])
        self.b_setClothesTopColor(dna.getClothesTopColor()[0], dna.getClothesTopColor()[1], dna.getClothesTopColor()[2])
        self.b_setClothesBotColor(dna.getClothesBotColor()[0], dna.getClothesBotColor()[1], dna.getClothesBotColor()[2])
