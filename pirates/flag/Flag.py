if __name__ == '__main__':
    from direct.directbase import DirectStart
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *
import FlagGlobals
from FlagDNA import FlagDNA

class Flag(NodePath):
    notify = directNotify.newCategory('Flag')
    BgSortOffset = 10
    EmblemSortOffset = 20

    def __init__(self, name):
        NodePath.__init__(self, name)
        self.cm = CardMaker(name)
        self.cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        self.__model = NodePath(self.cm.generate())
        self.__setBaseModelColor(Vec4(1))
        self.assign(NodePath(GeomNode('flag')))
        self.setTransparency(1)
        self.shapeNode = loader.loadModel('models/flags/flag_shape')
        self.bgNode = loader.loadModel('models/flags/flag_bg')
        self.emblemNode = loader.loadModel('models/flags/flag_emblem')
        self.guiNode = loader.loadModel('models/flags/flag_gui')
        self.dna = FlagDNA()

    def __repr__(self):
        return NodePath.__repr__(self)

    def __str__(self):
        outStr = str(self.dna)
        outStr += '\n'
        outStr += NodePath.__str__(self)
        return outStr

    def getDNAString(self):
        return self.dna.getDNAString()

    def setDNAString(self, dnaStr):
        self.dna.setDNAString(dnaStr)
        self.activate()

    def __setBaseModelColor(self, color):
        geom = self.__model.node().modifyGeom(0)
        vertexData = geom.modifyVertexData()
        colorWriter = GeomVertexWriter(vertexData, 'color')
        for rowNum in range(vertexData.getNumRows()):
            colorWriter.setData4f(color)

    def activate(self):
        self.__activate()

    def __activate(self):
        self.clearColor()
        self.clearTexture()
        self.get_children().detact()
        if self.node().getNumGeoms() > 0:
            self.node().removeGeom(0)
        self.__setBaseModelColor(Vec4(1, 1, 1, 0))
        np = self.__model.copyTo(NodePath('blank'))
        self.node().addGeomsFrom(np.node())
        self.node().setEffect(DecalEffect.make())
        self.__setBaseModelColor(Vec4(1, 1, 1, 1))
        del np
        self.texTex = self.bgNode.findTexture('flag_bg_tex*')
        self.texTex.setWrapU(Texture.WMClamp)
        self.texTex.setWrapV(Texture.WMClamp)
        self.texTs = TextureStage('tex')
        self.texTs.setSort(5)
        self.shapeTs = TextureStage('shape')
        self.shapeTs.setSort(10)
        self.__setShapeStyle()
        self.__setBgStyle()
        for x in range(4):
            self.__setBgColor(x)

        self.__setBgHFlip()
        self.__setBgVFlip()
        self.__setLayoutStyle()
        self.__setLayoutXPos()
        self.__setLayoutYPos()
        self.__setLayoutRVal()
        self.__setLayoutScale()
        self.__activateEmblems()

    def __activateEmblems(self):
        oldEmblemNps = self.findAllMatches('**/emblem-*')
        for np in oldEmblemNps:
            np.detachNode()
            np.remove()
            np.removeNode()

        del oldEmblemNps
        for enum in self.getEmblemIndices():
            self.__activateEmblem(enum)

    def __activateEmblem(self, index):
        self.__setEmblemStyle(index)
        self.__updateEmblem(index)

    def flatten(self, callback=None):
        portraitSceneGraph = NodePath('PortraitSceneGraph')
        portraitSceneGraph.setTransparency(1)
        flagCopy = self.copyTo(portraitSceneGraph)
        flagCopy.setY(10)
        par = base.win.makeTextureBuffer('par', 256, 256)
        par.setOneShot(True)
        parcam = base.makeCamera(win=par, scene=portraitSceneGraph, clearColor=Vec4(0), lens=OrthographicLens())
        parcam.reparentTo(portraitSceneGraph)
        tex = par.getTexture()
        tex.setWrapU(Texture.WMClamp)
        tex.setWrapV(Texture.WMClamp)
        self.setTexture(tex, 1)
        self.setColor(Vec4(1))

        def completeFlatten(par=par, tex=tex):
            if not par.isActive():
                self.get_children().detact()
                self.clearEffect(DecalEffect.make().getType())
                if callback:
                    callback()
            else:
                taskMgr.doMethodLater(0, completeFlatten, 'cleanUp', extraArgs=[])

        completeFlatten()
        return tex

    def getShapeStyle(self):
        return self.dna.getShapeStyle()

    def setShapeStyle(self, val):
        self.dna.setShapeStyle(val)
        self.__activate()

    def __setShapeStyle(self):
        val = self.getShapeStyle()
        self.shapeTex = self.shapeNode.findTexture('*_%02d' % val)
        self.shapeTex.setWrapU(Texture.WMClamp)
        self.shapeTex.setWrapV(Texture.WMClamp)
        self.setName('flag (style: %02d)' % val)

    def getBgStyle(self):
        return self.dna.getBackgroundStyle()

    def setBgStyle(self, val):
        self.dna.setBackground(style=val)
        self.__setBgStyle()
        for x in range(4):
            self.__setBgColor(x)

        self.__setBgHFlip()
        self.__setBgVFlip()

    def __setBgStyle(self):
        oldBgNps = self.findAllMatches('**/bg-*')
        for np in oldBgNps:
            np.detachNode()
            np.remove()
            np.removeNode()

        del oldBgNps
        val = self.dna.bgData[0]
        bgTexCol = self.bgNode.findAllTextures('*_%02d_*' % val)
        bgTexCol = [ bgTexCol[x] for x in range(bgTexCol.getNumTextures()) ]
        sortDict = dict(zip([ `x` for x in bgTexCol ], bgTexCol))
        keys = sortDict.keys()
        keys.sort()
        bgTexCol = [ sortDict[name] for name in keys ]
        for bgnum in range(0, len(bgTexCol) + 1):
            bgNp = self.__model.copyTo(self, sort=self.BgSortOffset + bgnum)
            bgNp.setName('bg-%d (style: %02d)' % (bgnum, val))
            if bgnum > 0:
                tex = bgTexCol[bgnum - 1]
                tex.setWrapU(Texture.WMClamp)
                tex.setWrapV(Texture.WMClamp)
                bgNp.setTexture(TextureStage.getDefault(), tex)
            bgNp.setTexture(self.texTs, self.texTex)
            bgNp.setTexture(self.shapeTs, self.shapeTex)
            bgNp.setTexTransform(self.shapeTs, TransformState.makeScale2d(Vec2(0.995, 1.0)))

    def getBgColor(self, index):
        return self.dna.getBackgroundColor(index)

    def setBgColor(self, index, val):
        if 0 <= index < 4 and val < len(FlagGlobals.Colors):
            eval('self.dna.setBackground(color_%d = val)' % index)
            self.__setBgColor(index)

    def __setBgColor(self, index):
        val = self.getBgColor(index)
        bgNp = self.find('**/bg-%d*' % index)
        if not bgNp.isEmpty():
            bgNp.setColorScale(FlagGlobals.Colors[val])

    def getBgHFlip(self):
        return self.dna.getBackgroundHorizontalFlip()

    def setBgHFlip(self, val):
        self.dna.setBackground(hFlip=val)
        self.__setBgHFlip()

    def __setBgHFlip(self):
        val = self.getBgHFlip()
        bgNpCol = self.findAllMatches('**/bg-*')
        scale = [
         1.0, 1.0]
        if val:
            scale[0] *= -1
        bgTexTransform = bgNpCol[0].getTexTransform(TextureStage.getDefault())
        if bgTexTransform.getPos()[1]:
            scale[1] *= -1
        for bgNp in bgNpCol:
            self.__updateBackgroundStageRaw(bgNp, TextureStage.getDefault(), scale)

    def getBgVFlip(self):
        return self.dna.getBackgroundVerticalFlip()

    def setBgVFlip(self, val):
        self.dna.setBackground(vFlip=val)
        self.__setBgVFlip()

    def __setBgVFlip(self):
        val = self.getBgVFlip()
        bgNpCol = self.findAllMatches('**/bg-*')
        scale = [
         1.0, 1.0]
        bgTexTransform = bgNpCol[0].getTexTransform(TextureStage.getDefault())
        if bgTexTransform.getPos()[0]:
            scale[0] *= -1
        if val:
            scale[1] *= -1
        for bgNp in bgNpCol:
            self.__updateBackgroundStageRaw(bgNp, TextureStage.getDefault(), scale)

    def getLayoutStyle(self):
        return self.dna.getLayoutStyle()

    def setLayoutStyle(self, val):
        self.dna.setLayout(style=val)
        self.__setLayoutStyle()

    def __setLayoutStyle(self):
        val = self.getLayoutStyle()
        ePosMax = len(FlagGlobals.LayoutOffsets[val]) - 1
        for x in self.getEmblemIndices():
            newPos = PythonUtil.clampScalar(self.getEmblemPos(x), 0, ePosMax)
            self.setEmblemPos(x, newPos)

    def getLayoutXPos(self):
        return self.dna.getLayoutXPos()

    def setLayoutXPos(self, val):
        self.dna.setLayout(xpos=val)
        self.__setLayoutXPos()

    def __setLayoutXPos(self):
        for x in self.getEmblemIndices():
            self.__updateEmblem(x)

    def getLayoutYPos(self):
        return self.dna.getLayoutYPos()

    def setLayoutYPos(self, val):
        self.dna.setLayout(ypos=val)
        self.__setLayoutYPos()

    def __setLayoutYPos(self):
        for x in self.getEmblemIndices():
            self.__updateEmblem(x)

    def getLayoutRVal(self):
        return self.dna.getLayoutRVal()

    def setLayoutRVal(self, val):
        self.dna.setLayout(rval=val)
        self.__setLayoutRVal()

    def __setLayoutRVal(self):
        for x in self.getEmblemIndices():
            self.__updateEmblem(x)

    def getLayoutScale(self):
        return self.dna.getLayoutScale()

    def setLayoutScale(self, val):
        self.dna.setLayout(scale=val)
        self.__setLayoutScale()

    def __setLayoutScale(self):
        for x in self.getEmblemIndices():
            self.__updateEmblem(x)

    def addEmblem(self, index=-1, location=-1):
        takenIndices = self.getEmblemIndices()
        if index not in takenIndices:
            if index < 0:
                availableIndices = [ x for x in range(16) if x not in takenIndices ]
                index = availableIndices[0]
            if location < 0:
                self.dna.setEmblem(index, pos=self.dna.getRandomEmblemPos(index))
            self.dna.setEmblem(index, pos=location)
            self.__activateEmblem(index)
            return index
        return None

    def getEmblemStyle(self, index):
        return self.dna.getEmblemStyle(index)

    def setEmblemStyle(self, index, styleVal):
        self.dna.setEmblem(index, style=styleVal)
        self.__activateEmblem(index)

    def __setEmblemStyle(self, index):
        val = self.getEmblemStyle(index)
        eTex = self.emblemNode.findTexture('*_%02d' % val)
        eTex.setWrapU(Texture.WMClamp)
        eTex.setWrapV(Texture.WMClamp)
        oldNp = self.find('**/emblem-%02d*' % index)
        if not oldNp.isEmpty():
            oldNp.detachNode()
            oldNp.remove()
            oldNp.removeNode()
        del oldNp
        eNp = self.__model.copyTo(self, sort=self.EmblemSortOffset + index)
        eNp.setName('emblem-%02d (style: %02d)' % (index, val))
        eNp.setTexture(eTex, 1)
        eNp.setTexture(self.texTs, self.texTex)
        eNp.setTexture(self.shapeTs, self.shapeTex)
        eNp.setTexTransform(self.shapeTs, TransformState.makeScale2d(Vec2(0.995, 1.0)))
        self.__setEmblemColor(index)

    def getEmblemColor(self, index):
        return self.dna.getEmblemColor(index)

    def setEmblemColor(self, index, val):
        self.dna.setEmblem(index, color=val)
        self.__setEmblemColor(index)

    def __setEmblemColor(self, index):
        val = self.getEmblemColor(index)
        if index in self.getEmblemIndices():
            eNp = self.find('**/emblem-%02d*' % index)
            eNp.setColorScale(FlagGlobals.Colors[val])

    def getEmblemPos(self, index):
        return self.dna.getEmblemPos(index)

    def setEmblemPos(self, index, val):
        self.dna.setEmblem(index, pos=val)
        self.__setEmblemPos(index)

    def __setEmblemPos(self, index):
        if index in self.getEmblemIndices():
            self.__updateEmblem(index)

    def getEmblemRVal(self, index):
        return self.dna.getEmblemRVal(index)

    def setEmblemRVal(self, index, val):
        self.dna.setEmblem(index, rval=val)
        self.__setEmblemRVal(index)

    def __setEmblemRVal(self, index):
        if index in self.getEmblemIndices():
            self.__updateEmblem(index)

    def getEmblemScale(self, index):
        return self.dna.getEmblemScale(index)

    def setEmblemScale(self, index, val):
        self.dna.setEmblem(index, scale=val)
        self.__setEmblemScale(index)

    def __setEmblemScale(self, index):
        if index in self.getEmblemIndices():
            self.__updateEmblem(index)

    def clearEmblem(self, index):
        self.dna.clearEmblem(index)
        self.__activateEmblems()

    def getNumBgColorsUsed(self):
        return self.bgNode.findAllMatches('**/*_%02d_*' % self.dna.getBackgroundStyle()).getNumPaths() + 1

    def getNumEmblems(self):
        return self.dna.getNumEmblems()

    def getEmblemIndices(self):
        return self.dna.getEmblemIndices()

    def __updateBackgroundStageRaw(self, np, stage, bgData):
        bgPos = Vec2(0.5, 0.5)
        bgRot = 0
        bgScl = Vec2(*bgData)
        corner = TransformState.makePos2d(Vec2(-0.5, -0.5))
        bgXForm = TransformState.makePosRotateScale2d(bgPos, bgRot, bgScl).compose(corner)
        iBgXForm = bgXForm.invertCompose(TransformState.makeIdentity())
        np.setTexTransform(stage, iBgXForm)

    def __updateEmblem(self, index):
        eNp = self.find('**/emblem-%02d (style: *)' % index)
        self.__updateEmblemStage(eNp, TextureStage.getDefault(), [
         self.getEmblemPos(index), self.getEmblemRVal(index), self.getEmblemScale(index)])

    def __updateEmblemStage(self, np, stage, eData):
        if not np.isEmpty():
            ePos = FlagGlobals.LayoutOffsets[self.getLayoutStyle()][eData[0]]
            eRot = eData[1] * 360 / FlagGlobals.RotationCount
            eScl = FlagGlobals.EmblemScales[eData[2]]
            self.__updateEmblemStageRaw(np, stage, ePos, eRot, eScl)

    def __updateEmblemStageRaw(self, np, stage, position, rotation, scale, relToLayout=True):
        if not np.isEmpty():
            ePos = Vec2(*position)
            eRot = rotation
            eScl = PythonUtil.clampScalar(scale, FlagGlobals.EmblemScales[0], FlagGlobals.EmblemScales[-1])
            corner = TransformState.makePos2d(Vec2(-0.5, -0.5))
            if relToLayout:
                lPos = Vec2(self.getLayoutXPos(), self.getLayoutYPos()) / 255.0
                lRot = self.getLayoutRVal() * 360 / FlagGlobals.RotationCount
                lScl = FlagGlobals.LayoutScales[self.getLayoutScale()]
                lXForm = TransformState.makePosRotateScale2d(lPos, lRot, Vec2(lScl)).compose(corner)
                eXForm = TransformState.makePosRotateScale2d(ePos, eRot, Vec2(eScl)).compose(corner)
                final = lXForm.compose(eXForm).invertCompose(TransformState.makeIdentity())
            else:
                eXForm = TransformState.makePosRotateScale2d(ePos, eRot, Vec2(eScl)).compose(corner)
                final = eXForm.invertCompose(TransformState.makeIdentity())
            np.setTexTransform(stage, final)

    def getEmblemPosRaw(self, posIndex):
        corner = TransformState.makePos2d(Vec2(-0.5, -0.5))
        lPos = Vec2(self.getLayoutXPos(), self.getLayoutYPos()) / 255.0
        lRot = self.getLayoutRVal() * 360 / FlagGlobals.RotationCount
        lScl = FlagGlobals.LayoutScales[self.getLayoutScale()]
        pt = Vec2(*FlagGlobals.LayoutOffsets[self.getLayoutStyle()][posIndex])
        lXForm = TransformState.makePosRotateScale2d(lPos, lRot, Vec2(lScl)).compose(corner)
        return lXForm.getMat3().xformPoint(pt)

    def modifyStageRaw(self, np, stage, position, rotation, scale):
        if not np.isEmpty():
            pos = position
            rot = rotation
            scl = scale
            corner = TransformState.makePos2d(Vec2(-0.5, -0.5))
            xForm = TransformState.makePosRotateScale2d(pos, rot, Vec2(scl)).compose(corner)
            final = xForm.invertCompose(TransformState.makeIdentity())
            np.setTexTransform(stage, final)

    def randomize(self, shape=False, bg=False, emblems=False):
        self.dna.randomize(shape, bg, emblems)
        self.activate()

    def flattenEmblemIndices(self):
        self.dna.flattenEmblemIndices()
        self.activate()


if __name__ == '__main__':
    p = FlagDNA()
    p.setShapeStyle(0)
    p.setBackground(0, 1, 6, 5, 7, 0, 0)
    p.setLayout(0, 128, 128, 0, 2)
    p.setEmblem(0, 8, 4, 4, 0, 4)
    f = Flag('testflag')
    f.setDNAString(p.getDNAString())
    f.reparentTo(render)
    print f
    print `f`
    base.mouseInterface.node().setPos(0, 3, 0)
    run()