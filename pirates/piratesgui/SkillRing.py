from direct.gui.DirectGui import *
from pandac.PandaModules import *

class SkillRing(DirectFrame):
    card = None
    rechargeRing = None
    base = None

    def __init__(self, color, baseColor=Vec4(1.0, 1.0, 1.0, 1.0)):
        if color[0] == 1 and color[1] == 0:
            pass
        DirectFrame.__init__(self, parent=NodePath(), relief=None)
        self.__progress = None
        self.initialiseoptions(SkillRing)
        self.meterColor = baseColor
        self.meterActiveColor = color
        if not SkillRing.card:
            SkillRing.card = loader.loadModel('models/textureCards/skillIcons')
            SkillRing.rechargeRing = SkillRing.card.find('**/recharge_ring')
            SkillRing.base = SkillRing.card.find('**/base')
            SkillRing.baseOver = SkillRing.card.find('**/base_over')
        self.meterFaceHalf1 = None
        self.meterFaceHalf2 = None
        self.setupFace()
        self.meterFaceHalf1 = SkillRing.rechargeRing.copyTo(self)
        self.meterFaceHalf1.setColor(self.meterActiveColor)
        self.meterFaceHalf1.setTransparency(1)
        self.meterFaceHalf1.setScale(0.13)
        self.meterFaceHalf1.flattenStrong()
        self.meterFaceHalf2 = SkillRing.rechargeRing.copyTo(self)
        self.meterFaceHalf2.setColor(self.meterColor)
        self.meterFaceHalf2.setTransparency(1)
        self.meterFaceHalf2.setScale(0.13)
        self.meterFaceHalf2.flattenStrong()
        return

    def setupFace(self, specialImage=None):
        if specialImage:
            self.meterFace = specialImage.copyTo(self)
            self.meterFace.setTransparency(1)
            self.meterFace.setScale(0.22)
            self.meterFace.setPos(0, 0, -0.025)
            self.meterFace.flattenStrong()
            self.meterFaceOver = specialImage.copyTo(self)
            self.meterFaceOver.setTransparency(1)
            self.meterFaceOver.setScale(0.22)
            self.meterFaceOver.setPos(0, 0, -0.025)
            self.meterFaceOver.setColor(0.7, 0.7, 0.7, 1.0)
            self.meterFaceOver.flattenStrong()
            self.meterFaceOver.hide()
        else:
            self.meterFace = SkillRing.base.copyTo(self)
            self.meterFace.setTransparency(1)
            self.meterFace.setScale(0.15)
            self.meterFace.flattenStrong()
            self.meterFaceOver = SkillRing.baseOver.copyTo(self)
            self.meterFaceOver.setTransparency(1)
            self.meterFaceOver.setScale(0.15)
            self.meterFaceOver.flattenStrong()
            self.meterFaceOver.hide()
        if self.meterFaceHalf1:
            self.meterFaceHalf1.reparentTo(self)
        if self.meterFaceHalf2:
            self.meterFaceHalf2.reparentTo(self)

    def rollover(self, over):
        if over:
            self.meterFaceOver.show()
            self.meterFace.hide()
        else:
            self.meterFaceOver.hide()
            self.meterFace.show()

    def update(self, val, max):
        progress = 0
        if max > 0:
            progress = float(val) / max
        if progress <= 0:
            self.meterFaceHalf1.hide()
            self.meterFaceHalf2.hide()
        elif progress >= 1:
            self.meterFaceHalf1.setColor(self.meterActiveColor)
            self.meterFaceHalf1.show()
            self.meterFaceHalf2.setR(-180)
            self.meterFaceHalf2.setColor(self.meterActiveColor)
            self.meterFaceHalf2.show()
        else:
            self.meterFaceHalf1.show()
            self.meterFaceHalf2.show()
            self.meterFaceHalf1.setColor(self.meterActiveColor)
            if progress < 0.5:
                self.meterFaceHalf2.setColor(self.meterColor)
            else:
                self.meterFaceHalf2.setColor(self.meterActiveColor)
                progress = progress - 0.5
            self.meterFaceHalf2.setR(-180 * (progress / 0.5))