from direct.gui.DirectGui import *
from pandac.PandaModules import *

class RadarUtil(DirectFrame):

    def __init__(self, *args, **kwargs):
        super(DirectFrame, self).__init__(*args, **kwargs)
        self.initialiseoptions(RadarUtil)
        self.model = None
        self.savePath = None
        self.pnm = None
        self.camRoot = None
        self.camera = None
        self.ctrlPanel = None
        self.resPanel = None
        self.modifyWorld()
        self.setupCamera()
        self.setupPictureFrame()
        self.setupControls()
        self.setupMouseTask()
        self.setTransparency(1)
        self.showThrough()
        self.destroyed = False
        return

    def destroy(self):
        if not self.destroyed:
            self.destroyed = True
            self.ctrlPanel = None
            self.resPanel = None
            self.resetWorld()
            self.resetCamera()
            self.resetPictureFrame()
            self.resetControls()
            self.resetMouseTasks()
            super(RadarUtil, self).destroy()
        return

    def isDestroyed(self):
        return self.destroyed

    def modifyWorld(self):
        base.setBackgroundColor(Vec4(0.8))
        render.find('**/seapatch').hide()
        for n in render.findAllMatches('**/+LODNode'):
            n.node().forceSwitch(n.node().getHighestSwitch())

        for n in render.findAllMatches('**/*nametag3d*'):
            n.hide()

        if hasattr(base, 'localAvatar'):
            localAvatar.guiMgr.request('Interface')
        aspect2d.hide()
        if hasattr(base, 'cr'):
            self.origTimeOfDay = base.cr.timeOfDayManager.getCurrentOrNextState()
            base.cr.timeOfDayManager.request('Off')
        render.setFogOff(100)

    def resetWorld(self):
        render.find('**/seapatch').show()
        render.clearFog()
        for n in render.findAllMatches('**/+LODNode'):
            n.node().clearForceSwitch()

        for n in render.findAllMatches('**/*nametag3d*'):
            n.show()

        if hasattr(base, 'localAvatar'):
            localAvatar.guiMgr.request('MouseLook')
        aspect2d.show()
        if hasattr(base, 'cr'):
            base.cr.timeOfDayManager.request(self.origTimeOfDay)
            del self.origTimeOfDay

    def setupCamera(self):
        self.origCamLens = base.cam.node().getLens()
        self.origCamParent = base.cam.getParent()
        if not self.camRoot:
            self.camRoot = render.attachNewNode('camRoot')
            self.camera = self.camRoot.attachNewNode('camera')
        oLens = OrthographicLens()
        oLens.setFar(100000)
        oLens.setAspectRatio(base.camLens.getAspectRatio())
        oLens.setFilmSize(1280)
        base.cam.node().setLens(oLens)
        base.camLens = oLens
        base.disableMouse()
        base.cam.reparentTo(self.camera)
        self.camera.setPosHpr(0, 0, 0, 0, -90, 0)
        self.camRoot.setPos(0, 0, 1500)

    def resetCamera(self):
        base.camLens = self.origCamLens
        base.cam.node().setLens(self.origCamLens)
        base.cam.reparentTo(self.origCamParent)
        del self.origCamLens
        del self.origCamParent
        self.camRoot.removeNode()
        del self.camRoot
        del self.camera

    def setupPictureFrame(self):
        self.picFrame = DirectFrame(parent=self, relief=None)
        DirectFrame(parent=self.picFrame, relief=DGG.FLAT, frameSize=(-2, -1, -1, 1), frameColor=(1,
                                                                                                  0,
                                                                                                  1,
                                                                                                  1))
        DirectFrame(parent=self.picFrame, relief=DGG.FLAT, frameSize=(1, 2, -1, 1), frameColor=(1,
                                                                                                0,
                                                                                                1,
                                                                                                1))
        return

    def resetPictureFrame(self):
        del self.picFrame

    def setupControls(self):
        if self.resPanel:
            self.resPanel.destroy()
        if self.ctrlPanel:
            self.ctrlPanel.destroy()
        self.resPanel = DirectFrame(parent=self, relief=None)
        self.resPanel.hide()
        self.ctrlPanel = DirectFrame(parent=self, relief=None)
        self.loadNameEntry = DirectEntry(parent=self.ctrlPanel, initialText='models/jungles/jungle_a', scale=0.05, width=25, pos=(-0.982, 0, 0.905), command=self.loadModelFromEntry)
        self.loadModelButton = DirectButton(parent=self.ctrlPanel, pos=(-1.17, 0, 0.908), scale=0.06, borderWidth=(0.1,
                                                                                                                   0.1), text='Load Model', command=self.loadModelFromEntry)
        self.findNameEntry = DirectEntry(parent=self.ctrlPanel, initialText='', scale=0.05, width=25, pos=(-0.982, 0, 0.755), command=self.findModelFromEntry)
        self.findModelButton = DirectButton(parent=self.ctrlPanel, pos=(-1.17, 0, 0.758), scale=0.06, borderWidth=(0.1,
                                                                                                                   0.1), text='Find Model', command=self.findModelFromEntry)
        self.savePathEntry = DirectEntry(parent=self.ctrlPanel, scale=0.05, width=25, pos=(-0.982, 0, 0.605), command=self.setSavePathFromEntry)
        self.setSavePathFromEntry()
        self.savePathButton = DirectButton(parent=self.ctrlPanel, pos=(-1.17, 0, 0.608), scale=0.06, borderWidth=(0.1,
                                                                                                                  0.1), text='Set Path', command=self.setSavePathFromEntry)
        self.sizeLabel = DirectLabel(parent=self.ctrlPanel, relief=None, pos=(-1.28,
                                                                              0,
                                                                              0.4), text='size', text_scale=0.05)
        self.sizeEntry = DirectEntry(parent=self.ctrlPanel, initialText=`(int(base.camLens.getFilmSize()[0]))`, scale=0.05, width=3, pos=(-1.187,
                                                                                                                                          0,
                                                                                                                                          0.4), command=self.handleSizeEntryUpdated)
        self.xLabel = DirectLabel(parent=self.ctrlPanel, relief=None, pos=(-1.277,
                                                                           0, 0.22), text='x', text_scale=0.05)
        self.xEntry = DirectEntry(parent=self.ctrlPanel, initialText=`(self.camera.getX())`, scale=0.05, width=3, pos=(-1.187,
                                                                                                                       0,
                                                                                                                       0.22), command=self.handleXEntryUpdated)
        self.yLabel = DirectLabel(parent=self.ctrlPanel, relief=None, pos=(-1.277,
                                                                           0, 0.1), text='y', text_scale=0.05)
        self.yEntry = DirectEntry(parent=self.ctrlPanel, initialText=`(self.camera.getY())`, scale=0.05, width=3, pos=(-1.187,
                                                                                                                       0,
                                                                                                                       0.1), command=self.handleYEntryUpdated)
        self.gScaleLabel = DirectLabel(parent=self.resPanel, relief=None, scale=0.05, pos=(1.03, 0, -0.75), text='gScale = ' + `(self.getGlobalScale())`, text_fg=Vec4(0, 0, 0, 1), text_bg=Vec4(1, 1, 1, 0), text_align=TextNode.ALeft, textMayChange=True)
        self.gPosLabel = DirectLabel(parent=self.resPanel, relief=None, scale=0.05, pos=(1.03, 0, -0.85), text='gPos = (0,0)', text_fg=Vec4(0, 0, 0, 1), text_bg=Vec4(1, 1, 1, 0), text_align=TextNode.ALeft, textMayChange=True)
        self.saveScreenButton = DirectButton(parent=self.ctrlPanel, pos=(-1.16719, 0, -0.75), scale=0.06, borderWidth=(0.1,
                                                                                                                       0.1), text='Save Screen', frameColor=(0,
                                                                                                                                                             1,
                                                                                                                                                             0,
                                                                                                                                                             1), command=self.saveScreenShot)
        self.exitButton = DirectButton(parent=self.ctrlPanel, pos=(-1.16719, 0, -0.9), scale=0.06, borderWidth=(0.1,
                                                                                                                0.1), text='Quit', frameColor=(0,
                                                                                                                                               1,
                                                                                                                                               0,
                                                                                                                                               1), command=self.destroy)
        return

    def resetControls(self):
        if self.resPanel:
            self.resPanel.destroy()
        if self.ctrlPanel:
            self.ctrlPanel.destroy()
        del self.resPanel
        del self.ctrlPanel
        del self.loadNameEntry
        del self.loadModelButton
        del self.findNameEntry
        del self.savePathEntry
        del self.savePath
        del self.savePathButton
        del self.sizeLabel
        del self.sizeEntry
        del self.xLabel
        del self.xEntry
        del self.yLabel
        del self.yEntry
        del self.gScaleLabel
        del self.gPosLabel
        del self.saveScreenButton
        del self.exitButton

    def setupMouseTask(self):
        self.accept('mouse1', self.startMouse1Drag)
        self.accept('mouse1-up', self.stopMouse1Drag)
        self.accept('mouse3', self.startMouse3Drag)
        self.accept('mouse3-up', self.stopMouse3Drag)

    def adjustFilmSize(self, amount):
        self.setFilmSize(base.camLens.getFilmSize()[0] + amount)

    def adjustFilmSizeFactor(self, orig, factor):
        self.setFilmSize(orig * factor)

    def startMouse1Drag(self):
        taskMgr.add(self.mouse1DragTask, 'mouse1Drag')

    def mouse1DragTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            if task.time == 0.0:
                task.startPt = Point2(base.mouseWatcherNode.getMouse())
                task.startCamPos = Point2(self.camera.getX(), self.camera.getY())
            mPt = Point2(base.mouseWatcherNode.getMouse())
            mDelta = mPt - task.startPt
            ts = TransformState.makeScale2d(base.camLens.getFilmSize() / 2.0)
            posDelta = ts.getMat3().xformPoint(mDelta)
            newPos = task.startCamPos - posDelta
            self.setCameraX(newPos[0])
            self.setCameraY(newPos[1])
        return task.cont

    def stopMouse1Drag(self):
        taskMgr.remove('mouse1Drag')

    def startMouse3Drag(self):
        taskMgr.add(self.mouse3DragTask, 'mouse3Drag')

    def mouse3DragTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            if task.time == 0.0:
                task.startPt = Point2(base.mouseWatcherNode.getMouse())
                task.startSize = base.camLens.getFilmSize()[0]
            mPt = Point2(base.mouseWatcherNode.getMouse())
            mDelta = mPt - task.startPt
            self.adjustFilmSizeFactor(task.startSize, 1 + mDelta[1] / 2.0)
        return task.cont

    def stopMouse3Drag(self):
        taskMgr.remove('mouse3Drag')

    def resetMouseTasks(self):
        self.stopMouse1Drag()
        self.stopMouse3Drag()
        self.ignoreAll()

    def handleSizeEntryUpdated(self, val):
        self.setFilmSize(float(val))

    def handleXEntryUpdated(self, val):
        self.setCameraX(float(val))

    def handleYEntryUpdated(self, val):
        self.setCameraY(float(val))

    def setFilmSize(self, size):
        base.camLens.setFilmSize(size)
        self.sizeEntry.enterText(`size`)
        self.gScaleLabel['text'] = 'scale: ' + `(self.getGlobalScale())`

    def setCameraX(self, x):
        self.camera.setX(x)
        self.xEntry.set('%3.1f' % -x)
        y = self.camera.getY()
        self.gPosLabel['text'] = 'x: %3.1f\ny: %3.1f' % (x, y)

    def setCameraY(self, y):
        self.camera.setY(y)
        self.yEntry.set('%3.1f' % -y)
        x = self.camera.getX()
        self.gPosLabel['text'] = 'x: %3.1f\ny: %3.1f' % (x, y)

    def loadModel(self, modelName):
        model = loader.loadModel(modelName)
        if model:
            if self.model:
                self.model.removeNode()
            self.model = model
            self.model.reparentTo(render)
            print modelName, ' loaded'
        else:
            print modelName, ' not loaded'

    def findModel(self, modelName):
        model = render.find('**/' + modelName + '*')
        if not model.isEmpty():
            self.findNameEntry.set(model.getName())
            pos, h = model.getPos(render), model.getH(render)
            self.camRoot.setX(pos[0])
            self.camRoot.setY(pos[1])
            self.camRoot.setH(h)
            self.setCameraX(0)
            self.setCameraY(0)
            self.camera.setPos(0, 0, 0)
        else:
            print modelName, ' not in scenegraph'

    def stashNamedNodes(self, names=[]):
        for name in names:
            self.model.findAllMatches('**/' + name).stash()

    def stashAllBut(self, nodepath):
        self.model.findAllMatches('**/*').stash()
        nodepath.findAllMatches('**/*;+s').unstash()
        while nodepath != nodepath.getTop():
            nodepath.unstash()
            nodepath = nodepath.getParent()

    def getGlobalScale(self):
        return int(base.camLens.getFilmSize()[1] / 2)

    def loadModelFromEntry(self, fileName=None):
        if not fileName:
            fileName = self.loadNameEntry.get()
        self.loadModel(fileName)

    def findModelFromEntry(self, fileName=None):
        if not fileName:
            fileName = self.findNameEntry.get()
        self.findModel(fileName)

    def setSavePathFromEntry(self, fileName=None):
        if not fileName:
            fileName = self.savePathEntry.get()
        if not fileName:
            fileName = 'screenshot'
        if '.' not in fileName[-4:]:
            fileName += '.tif'
        self.savePath = Filename(fileName)
        self.savePath.touch()
        vfs.resolveFilename(self.savePath, DSearchPath('.'))
        self.savePathEntry.set(`(self.savePath)`)

    def resizeForPicture(self):
        fs = base.camLens.getFilmSize()
        self.setFilmSize(int(fs[0] * 2))

    def resizeForViewing(self):
        fs = base.camLens.getFilmSize()
        self.setFilmSize(int(fs[0] / 2))

    def saveScreenShot(self):
        self.resizeForPicture()
        self.setSavePathFromEntry()
        self.ctrlPanel.hide()
        self.resPanel.show()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        filepath = self.savePath
        if not self.pnm:
            self.pnm = PNMImage(base.win.getXSize(), base.win.getYSize())
        if not base.win.getScreenshot(self.pnm):
            print 'Error: Screenshot not taken'
        elif not filepath.touch():
            print 'Error: invalid filepath: ' + `filepath`
        elif not self.pnm.write(filepath):
            print 'Error: Screenshot taken but not saved'
        else:
            filepath.resolveFilename(DSearchPath('.'))
            print 'Screenshot saved to ' + `filepath`
        self.resizeForViewing()
        self.ctrlPanel.show()
        self.resPanel.hide()