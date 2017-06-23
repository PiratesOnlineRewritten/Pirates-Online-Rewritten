import types
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pirates.piratesgui import PiratesGuiGlobals

class BorderFrame(DirectFrame):
    pieceNames = ('headBoard', 'background', 'top', 'right', 'bottom', 'left', 'topRight',
                  'bottomRight', 'bottomLeft', 'topLeft')
    nodeNames = dict(zip(pieceNames, ('headBoard', 'middle', 'top1', 'right', 'bottom',
                                      'left', 'topRight', 'bottomRight', 'bottomLeft',
                                      'topLeft')))

    def __init__(self, parent=None, **kw):
        optiondefs = (('relief', None, None), ('borderScale', 0.3, self.setBorderScale), ('bgBuffer', 0.025, self.setBgBuffer), ('bgColorScale', VBase4(1, 1, 1, 1), self.setBgColorScale), ('bgTransparency', 0, self.setBgTransparent), ('imageColorScale', VBase4(1, 1, 1, 1), None), ('cornerWidth', 0.15, None), ('draggable', 0, None), ('frameSize', (-0.5, 0.5, -0.5, 0.5), self.setFrameSize), ('modelName', 'general_frame_f', None), ('showHeadBoard', False, None), ('nameTag', '', None), ('state', DGG.NORMAL, self.setState), ('showBackground', True, None), ('flatten', 1, None))
        self.pieces = None
        self.guiComponents = {}
        self.nameTag = None
        self.nameTagLabel = None
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent=NodePath(), **kw)
        self.canBringToFront = True
        self.loadGeometry()
        self.initialiseoptions(BorderFrame)
        self.setupGeometry()
        self.reparentTo(parent or aspect2d, self['sortOrder'])
        return

    def destroy(self):
        if hasattr(self, 'frameParent') and self.frameParent:
            for child in self.frameParent.getChildren():
                childGui = self.guiDict.get(child.getName())
                if childGui:
                    childGui.destroy()
                else:
                    parts = child.getName().split('-')
                    simpleChildGui = self.guiDict.get(parts[-1])
                    if simpleChildGui:
                        simpleChildGui.destroy()

            self.frameParent.removeNode()
            self.frameParent = None
        if hasattr(self, 'behindParent') and self.behindParent:
            for child in self.behindParent.getChildren():
                childGui = self.guiDict.get(child.getName())
                if childGui:
                    childGui.destroy()
                else:
                    parts = child.getName().split('-')
                    simpleChildGui = self.guiDict.get(parts[-1])
                    if simpleChildGui:
                        simpleChildGui.destroy()

            self.behindParent.removeNode()
            self.behindParent = None
        DirectFrame.destroy(self)
        return

    def loadGeometry(self):
        if not self.pieces:
            modelGeom = loader.loadModel('models/gui/' + self['modelName'])
            self.pieces = dict(zip(self.pieceNames, [ modelGeom.find('**/%s' % self.nodeNames[pieceName]) for pieceName in self.pieceNames ]))
            self.nameTag = modelGeom.find('**/nameTag')
            for k in ('top', 'right', 'bottom', 'left'):
                tex = self.pieces[k].findTexture(TextureStage.getDefault())
                if tex:
                    tex.setWrapU(Texture.WMRepeat)
                    tex.setWrapV(Texture.WMRepeat)

            tex = self.pieces['background'].findTexture(TextureStage.getDefault())
            if tex:
                tex.setWrapU(Texture.WMMirror)
                tex.setWrapV(Texture.WMMirror)
            if self['nameTag'] and self.nameTag:
                from pirates.piratesbase import PiratesGlobals
                self.nameTagLabel = DirectLabel(parent=self.nameTag, relief=None, pos=(0,
                                                                                       0,
                                                                                       0.05), text=self['nameTag'], text_scale=0.2, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=(1,
                                                                                                                                                                                                  1,
                                                                                                                                                                                                  1,
                                                                                                                                                                                                  1), text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, textMayChange=1)
        return

    def copyFlattenedChild(self, node, parent):
        if not node:
            return
        if node.getNumChildren() == 0:
            child = node
            childCopy = child.copyTo(parent)
        else:
            child = node.getChild(0)
            childCopy = child.copyTo(parent)
            childCopy.setTransform(node.getTransform())
        childCopy.flattenStrong()
        return childCopy

    def setupGeometry(self):
        self.frameParent = self.attachNewNode(ModelNode('frameParent'))
        self.frameParent.stash()
        self.background = self.frameParent.attachNewNode('background')
        if not self['modelName']:
            self.background.setColor(0.5, 0.5, 0.5, 1)
        self.behindParent = self.frameParent.attachNewNode(ModelNode('behindParent'))
        self.guiComponents = {self.pieceNames[0]: self.copyFlattenedChild(self.pieces[self.pieceNames[0]], self.background)
           }
        if self['draggable']:
            self.guiComponents.update(dict(zip(self.pieceNames[1:], [ DirectButton(parent=self.frameParent, guiId=self.guiId + '-' + pieceName, relief=None, state=self['state'], geom=self.pieces[pieceName], rolloverSound=None, clickSound=None, pressEffect=0) for pieceName in self.pieceNames[1:] ])))
        else:
            self.guiComponents.update(dict(zip(self.pieceNames[1:], [ self.copyFlattenedChild(self.pieces[pieceName], self.frameParent)
             for pieceName in self.pieceNames[1:] ])))
        self.guiComponents['background'].setColorScale(self['bgColorScale'])
        self.guiComponents['background'].setTransparency(self['bgTransparency'])
        for guiComp in self.guiComponents:
            if self.guiComponents[guiComp]:
                self.guiComponents[guiComp].setColorScale(self['imageColorScale'])

        if not self['showBackground']:
            self.guiComponents['background'].stash()
        if not self['showHeadBoard'] and self.guiComponents['headBoard']:
            self.guiComponents['headBoard'].stash()
        if self['draggable']:
            for piece in self.getDraggableGeometry():
                piece.bind(DGG.B1PRESS, self.dragStart)
                piece.bind(DGG.B1RELEASE, self.dragStop)
                piece.bind(DGG.B2PRESS, self.dragStart)
                piece.bind(DGG.B2RELEASE, self.dragStop)
                piece.bind(DGG.B3PRESS, self.dragStart)
                piece.bind(DGG.B3RELEASE, self.dragStop)

        if self.nameTag:
            self.nameTag.reparentTo(self.frameParent)
        if not self['nameTag'] and self.nameTag:
            self.nameTag.stash()
        self.resetDecorations()
        return

    def resetHBorder(self, scale, frameSize):
        bScale = scale * (frameSize / self['borderScale'] - self['cornerWidth'] * 2.0 / scale)
        scale = self.guiComponents['top'].getScale()
        scale.setX(bScale)
        self.guiComponents['top'].setScale(scale)
        self.guiComponents['top'].setTexScale(TextureStage.getDefault(), 1, bScale)
        self.guiComponents['top'].setTexOffset(TextureStage.getDefault(), 0, -(bScale - 1) / 2.0)
        self.guiComponents['bottom'].setScale(scale)
        self.guiComponents['bottom'].setTexScale(TextureStage.getDefault(), 1, bScale)
        self.guiComponents['bottom'].setTexOffset(TextureStage.getDefault(), 0, -(bScale - 1) / 2.0)
        xPos = bScale - 1.0
        self.guiComponents['topRight'].setX(xPos)
        self.guiComponents['right'].setX(xPos)
        self.guiComponents['bottomRight'].setX(xPos)
        if self.guiComponents['headBoard']:
            self.guiComponents['headBoard'].setX(xPos / 2.0)
        if self.nameTag:
            self.nameTag.setX(0.5 + xPos / 2.0)

    def resetVBorder(self, scale, frameSize):
        bScale = scale * (frameSize / self['borderScale'] - self['cornerWidth'] * 2 / scale)
        scale = self.guiComponents['left'].getScale()
        scale.setZ(bScale)
        self.guiComponents['left'].setScale(scale)
        self.guiComponents['left'].setTexScale(TextureStage.getDefault(), 1, bScale)
        self.guiComponents['left'].setTexOffset(TextureStage.getDefault(), 0, -(bScale - 1) / 2.0)
        self.guiComponents['right'].setScale(scale)
        self.guiComponents['right'].setTexScale(TextureStage.getDefault(), 1, bScale)
        self.guiComponents['right'].setTexOffset(TextureStage.getDefault(), 0, -(bScale - 1) / 2.0)
        yPos = 1.0 - bScale
        self.guiComponents['bottomLeft'].setZ(yPos)
        self.guiComponents['bottom'].setZ(yPos)
        self.guiComponents['bottomRight'].setZ(yPos)

    def resetBackground(self, xScale, yScale, xFrameSize, yFrameSize):
        xbScale = xScale * (xFrameSize - self['bgBuffer'] * 2.0 / xScale)
        ybScale = yScale * (yFrameSize - self['bgBuffer'] * 2.0 / yScale)
        xScale = xScale * (xFrameSize / self['borderScale'] - self['bgBuffer'] * 2.0 / xScale)
        yScale = yScale * (yFrameSize / self['borderScale'] - self['bgBuffer'] * 2.0 / yScale)
        oldScale = self.guiComponents['background'].getScale()
        self.guiComponents['background'].setScale(xScale, oldScale[1], yScale)
        self.guiComponents['background'].setTexScale(TextureStage.getDefault(), xbScale, ybScale)
        self.guiComponents['background'].setTexOffset(TextureStage.getDefault(), -(xbScale - 1) / 2.0, -(ybScale - 1) / 2.0)
        self.guiComponents['background'].setX(-(self['cornerWidth'] - self['bgBuffer']))
        self.guiComponents['background'].setZ(self['cornerWidth'] - self['bgBuffer'])

    def resetDecorations(self):
        scale = self.getScale()
        invScale = Vec3(self['borderScale'] / scale[0], self['borderScale'] / scale[1], self['borderScale'] / scale[2])
        self.frameParent.setScale(invScale)
        frameSize = self['frameSize']
        if frameSize:
            xFrameSize, xFramePos = frameSize[1] - frameSize[0], frameSize[0]
            yFrameSize, yFramePos = frameSize[3] - frameSize[2], frameSize[2]
        else:
            xFrameSize, xFramePos = 1, -0.5
            yFrameSize, yFramePos = 1, -0.5
        self.frameParent.setX(xFramePos + self['cornerWidth'] / scale[0] * self['borderScale'])
        self.frameParent.setZ(yFrameSize + yFramePos - self['cornerWidth'] / scale[2] * self['borderScale'])
        ts = self.frameParent.getTransform().getInverse()
        self.behindParent.setTransform(ts)
        self.resetHBorder(scale[0], xFrameSize)
        self.resetVBorder(scale[2], yFrameSize)
        self.resetBackground(scale[0], scale[2], xFrameSize, yFrameSize)
        temp = self.frameParent.copyTo(NodePath('temp'))
        temp.unstash()
        if self['flatten']:
            temp.flattenStrong()
        if self.frameParent.getTransparency():
            temp.setTransparency(self.frameParent.getTransparency(), 1)
        self['geom'] = None
        if self['flatten']:
            self['geom'] = temp
            self.frameParent.stash()
        else:
            self.temp = temp
            self.frameParent.unstash()
        return

    def setScale(self, *args, **kwargs):
        DirectFrame.setScale(self, *args, **kwargs)
        if self.guiComponents:
            self.resetDecorations()

    def setFrameSize(self, *args, **kwargs):
        DirectFrame.setFrameSize(self, *args, **kwargs)
        if self.guiComponents:
            self.resetDecorations()

    def setBorderScale(self):
        if self.guiComponents:
            self.resetDecorations()

    def setBgBuffer(self):
        if self.guiComponents:
            self.resetDecorations()

    def getDraggableGeometry(self):
        return [ self.guiComponents[piece] for piece in self.pieceNames[1:] ]

    def setBackgroundVisible(self, visible):
        if visible:
            self.guiComponents['background'].show()
            self['state'] = DGG.NORMAL
        else:
            self.guiComponents['background'].hide()
            self['state'] = DGG.DISABLED
        self.resetDecorations()

    def setBackgroundTexture(self, texture):
        pass

    def placeItemBehindBorder(self, child):
        child.reparentTo(self.behindParent)
        self.resetDecorations()

    def dragStart(self, event):
        self.bringToFront()
        if self['draggable']:
            taskMgr.remove(self.taskName('dragTask'))
            vWidget2render2d = self.getPos(render2d)
            vMouse2render2d = Point3(event.getMouse()[0], 0, event.getMouse()[1])
            editVec = Vec3(vWidget2render2d - vMouse2render2d)
            task = taskMgr.add(self.dragTask, self.taskName('dragTask'))
            task.editVec = editVec

    def dragTask(self, task):
        mwn = base.mouseWatcherNode
        if mwn.hasMouse():
            vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
            newPos = vMouse2render2d + task.editVec
            self.setPos(render2d, newPos)
            newPos = self.getPos(aspect2d)
            x = newPos[0]
            y = newPos[1]
            z = newPos[2]
            x = x - x % 0.05
            y = 0
            z = z - z % 0.05
            frameSize = self['frameSize']
            if frameSize:
                w = frameSize[1] - frameSize[0]
                h = frameSize[3] - frameSize[2]
            else:
                w = 1
                h = 1
            x = min(base.a2dRight - w, max(base.a2dLeft, x))
            z = min(base.a2dTop - h, max(base.a2dBottom, z))
            self.setPos(aspect2d, x, y, z)
        return Task.cont

    def dragStop(self, event):
        if self['draggable']:
            taskMgr.remove(self.taskName('dragTask'))

    def setBringToFront(self, bringIt):
        self.canBringToFront = bringIt

    def bringToFront(self):
        if self.canBringToFront:
            self.reparentTo(self.getParent())

    def getInnerFrameSize(self):
        frameSize = self['frameSize']
        scaleX, scaleZ = self.getScale()[0], self.getScale()[2]
        borderScale = self['borderScale']
        factorX, factorZ = borderScale / scaleX, borderScale / scaleZ
        return Vec4(frameSize[0] + self['bgBuffer'] * factorX, frameSize[1] - self['bgBuffer'] * factorX, frameSize[2] + self['bgBuffer'] * factorZ, frameSize[3] - self['bgBuffer'] * factorZ)

    def setBgTransparent(self):
        if self.guiComponents:
            self.guiComponents['background'].setTransparency(self['bgTransparency'])

    def setBgColorScale(self):
        if self.guiComponents:
            self.guiComponents['background'].setColorScale(self['bgColorScale'])
