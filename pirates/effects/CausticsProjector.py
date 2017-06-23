from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

class CausticsProjector(NodePath):
    globalGeomList = []
    causticsTex = []
    texStage = None
    swapTexIval = None
    currTexIndex = 0

    def __init__(self, geomList=[]):
        NodePath.__init__(self, 'CausticsProjector')
        self.geomList = geomList
        self.lens = PerspectiveLens()
        self.projector = self.attachNewNode(LensNode('Projector'))
        self.projector.node().setLens(self.lens)
        if not CausticsProjector.causticsTex:
            CausticsProjector.causticsTex = []
            causticsCards = loader.loadModel('models/effects/causticsCards')
            for card in causticsCards.findAllMatches('**/*caustics*'):
                texture = card.findAllTextures()[0]
                texture.setBorderColor(VBase4(0.0, 0.0, 0.0, 1.0))
                texture.setWrapU(Texture.WMBorderColor)
                texture.setWrapV(Texture.WMBorderColor)
                CausticsProjector.causticsTex.append(texture)

            CausticsProjector.texStage = TextureStage('CausticsTextureStage')
            CausticsProjector.texStage.setMode(TextureStage.MAdd)

    def setLensFov(self, angleA, angleB):
        self.lens.setFov(angleA, angleB)

    def attachGeom(self, geom):
        self.geomList.append(geom)
        geom.projectTexture(CausticsProjector.texStage, CausticsProjector.causticsTex[0], self.projector)

    def removeGeom(self, geom):
        geom.clearTexture(CausticsProjector.texStage)
        if geom in self.geomList:
            self.geomList.remove(geom)
        if geom in CausticsProjector.globalGeomList:
            CausticsProjector.globalGeomList.remove(geom)

    def enableEffect(self):
        for geom in self.geomList:
            CausticsProjector.globalGeomList.append(geom)

        if not CausticsProjector.swapTexIval:
            CausticsProjector.swapTexIval = Sequence(Func(self.swapTexture), Wait(0.1))
            CausticsProjector.swapTexIval.loop()

    def disableEffect(self):
        for geom in self.geomList:
            if geom in CausticsProjector.globalGeomList:
                CausticsProjector.globalGeomList.remove(geom)

    def swapTexture(self):
        CausticsProjector.currTexIndex = (CausticsProjector.currTexIndex + 1) % len(CausticsProjector.causticsTex)
        for geom in CausticsProjector.globalGeomList:
            geom.setTexture(CausticsProjector.texStage, CausticsProjector.causticsTex[CausticsProjector.currTexIndex])

    def destroy(self):
        self.disableEffect()
        self.geomList = []
        if not CausticsProjector.globalGeomList:
            if CausticsProjector.swapTexIval:
                CausticsProjector.swapTexIval.pause()
                CausticsProjector.swapTexIval = None
        return