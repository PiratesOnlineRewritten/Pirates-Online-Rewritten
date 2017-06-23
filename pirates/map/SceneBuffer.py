from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import sys
import gc

class SceneBuffer(DirectObject):

    def __init__(self, name, size=Vec2(512, 512) * 2.0, camAspectRatio=1.0, clearColor=Vec4(0.85, 0.85, 0.85, 1.0), sceneGraph=None):
        DirectObject.__init__(self)
        self.name = name
        self.size = size
        if not sceneGraph:
            self.__sceneGraph = NodePath(self.name + '-render')
        else:
            self.__sceneGraph = sceneGraph
        self.camera = self.__sceneGraph.attachNewNode(Camera(self.name + 'camera'))
        self.camNode = self.camera.node()
        self.camLens = PerspectiveLens()
        self.camLens.setFov(30, 30)
        self.camNode.setLens(self.camLens)
        self.__texture = Texture(self.name)
        self.__buffer = None
        self.__createBuffer()
        self.accept('close_main_window', self.__destroyBuffer)
        self.accept('open_main_window', self.__createBuffer)
        return

    def __destroyBuffer(self):
        if self.__buffer:
            base.graphicsEngine.removeWindow(self.__buffer)
            self.__buffer = None
        return

    def __createBuffer(self):
        self.__destroyBuffer()
        self.__buffer = base.win.makeTextureBuffer(self.name, self.size[0], self.size[1], tex=self.__texture)
        dr = self.__buffer.makeDisplayRegion()
        dr.setCamera(self.camera)

    def getSceneRoot(self):
        return self.__sceneGraph

    def getTexture(self):
        return self.__texture

    def getTextureCard(self):
        if self.__buffer:
            return self.__buffer.getTextureCard()
        return NodePath('empty')

    def destroy(self):
        self.disable()
        self.camera = None
        self.camLens = None
        self.__sceneGraph = None
        self.__texture = None
        self.__destroyBuffer()
        self.ignore('close_main_window')
        self.ignore('open_main_window')
        return

    def enable(self):
        if self.__buffer:
            self.__createBuffer()
            self.__buffer.setActive(True)

    def disable(self):
        if self.__buffer:
            self.__buffer.setActive(False)