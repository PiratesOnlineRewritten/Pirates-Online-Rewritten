from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController

class StormEye(EffectController, NodePath):

    def __init__(self):
        NodePath.__init__(self, 'StormEye')
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/celestial.egg')
        self.effectModel.setPos(0, 0, 15)
        self.effectModel.setSy(0.5)
        self.effectModel.setP(-90)
        self.effectModel.setTransparency(TransparencyAttrib.MAlpha)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setBin('background', 115)
        self.duration = 10
        cloud = loader.loadModel('models/effects/cloud.egg')
        self.cloudCoverTexStageArr = []
        ts = TextureStage('cloudCover1')
        ts.setMode(TextureStage.MReplace)
        self.cloudCoverTexStageArr.append(ts)
        ts = TextureStage('cloudCoverInterpolate2')
        ts.setColor(Vec4(0.0, 0.0, 0.0, 1.0))
        ts.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSConstant, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMModulate, TextureStage.CSPrevious, TextureStage.COSrcAlpha, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        self.cloudCoverTexStageArr.append(ts)
        ts = TextureStage('cloudCoverInterpolate4')
        ts.setColor(Vec4(0.0, 0.0, 0.0, 1.0))
        ts.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSConstant, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMModulate, TextureStage.CSPrevious, TextureStage.COSrcAlpha, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        self.cloudCoverTexStageArr.append(ts)
        self.lensNode = render.attachNewNode(LensNode('cloudProjection'))
        lens = PerspectiveLens()
        self.lensNode.node().setLens(lens)
        self.lensNode.reparentTo(self)
        self.lensNode.setPos(0.0, 0.0, 900.0)
        self.lensNode.setP(90)
        self.effectModel.projectTexture(self.cloudCoverTexStageArr[0], cloud.find('**/1').findTexture('1'), self.lensNode)
        self.effectModel.projectTexture(self.cloudCoverTexStageArr[1], cloud.find('**/2').findTexture('2'), self.lensNode)
        self.effectModel.projectTexture(self.cloudCoverTexStageArr[2], cloud.find('**/4').findTexture('4'), self.lensNode)

    def createTrack(self):
        fadeIn = LerpColorScaleInterval(self, 1.5, Vec4(1.0, 1.0, 1.0, 1.0), startColorScale=Vec4(1.0, 1.0, 1.0, 0.0))
        fadeOut = LerpColorScaleInterval(self, 1.5, Vec4(1.0, 1.0, 1.0, 0.0), startColorScale=Vec4(1.0, 1.0, 1.0, 1.0))
        cloud1 = Sequence(LerpFunctionInterval(self.cloudCoverTexStageArr[1].setColor, 4.5, toData=Vec4(0.9, 0.9, 0.9, 1.0), fromData=Vec4(0.75, 0.75, 0.75, 1.0)), LerpFunctionInterval(self.cloudCoverTexStageArr[1].setColor, 4.5, toData=Vec4(0.75, 0.75, 0.75, 1.0), fromData=Vec4(0.9, 0.9, 0.9, 1.0)))
        cloud2 = Sequence(LerpFunctionInterval(self.cloudCoverTexStageArr[2].setColor, 2.5, toData=Vec4(1.0, 1.0, 1.0, 1.0), fromData=Vec4(0.75, 0.75, 0.75, 1.0)), LerpFunctionInterval(self.cloudCoverTexStageArr[2].setColor, 2.5, toData=Vec4(0.75, 0.75, 0.75, 1.0), fromData=Vec4(1.0, 1.0, 1.0, 1.0)))
        swirl = LerpHprInterval(self.lensNode, 10.0, Vec3(-360, 90, 0), Vec3(0, 90, 0))
        self.startEffect = Sequence(Wait(0.5), Func(cloud1.loop), Func(cloud2.loop), Func(swirl.loop), Func(self.effectModel.reparentTo, self), fadeIn)
        self.endEffect = Sequence(Wait(0.5), fadeOut, Func(cloud1.finish), Func(cloud2.finish), Func(swirl.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)