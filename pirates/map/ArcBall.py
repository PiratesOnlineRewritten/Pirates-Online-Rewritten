from pandac.PandaModules import *
from direct.showbase.PythonUtil import clampScalar
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence, Parallel, LerpFunc, Func, Wait
from direct.task.Task import Task
import math

def getPerpendicularVec(vec):
    if vec[0] == 0.0:
        return Vec3(1, 0, 0)
    elif vec[1] == 0.0:
        return Vec3(0, 1, 0)
    elif vec[2] == 0.0:
        return Vec3(0, 0, 1)
    else:
        return Vec3(1.0 / vec[0], -1.0 / vec[1], 0.0)


def lerp(a, b, t):
    return a + (b - a) * t


def sLerp(p0, p1, t, arcLen):
    return (p0 * math.sin((1 - t) * arcLen) + p1 * math.sin(t * arcLen)) / math.sin(arcLen)


def nLerp(a, b, t):
    r = lerp(a, b, t)
    r.normalize()
    return r


class ArcBall(NodePath, DirectObject):

    def __init__(self, name, radius=1, scrollFactor=1, camera=base.cam, frame=Vec4(-1, 1, -1, 1), keepUpright=0, mouseDownEvent='mouse1', mouseUpEvent='mouse1-up', *args, **kwargs):
        NodePath.__init__(self, name, *args, **kwargs)
        DirectObject.__init__(self)
        self._rNode = self.attachNewNode('rotateNode')
        self._setRadius(radius, False)
        self._setScrollFactor(scrollFactor, False)
        self._setCamera(camera, False)
        self._setFrame(frame, False)
        self._setKeepUpright(keepUpright)
        self._setMouseEvents(mouseDownEvent, mouseUpEvent)
        self.setRotateMode(0)
        self._setControlButtonState(0)
        self._setTiltLimit(25 * math.pi / 180, False)
        self.saveNorth()
        self._colBitMask = BitMask32(1 << 16)
        self._colNode = self.attachNewNode(CollisionNode(name + '-cNode'))
        self._colNode.node().addSolid(CollisionSphere(0, 0, 0, 1))
        self._colNode.node().setIntoCollideMask(self._colBitMask)
        self._mouseEnabled = True
        self._initCollisions()
        self.geom_node_path = self.attachNewNode('arrow')
        self.geom_node_path.setBin('fixed', 100)
        self.geom_node_path.setDepthTest(0)
        self.geom_node_path.setTransparency(1)
        self.head_geom_node = GeomNode('head')
        self.head_geom_node_path = self.geom_node_path.attachNewNode(self.head_geom_node)
        self.tail_geom_node = GeomNode('tail')
        self.tail_geom_node_path = self.geom_node_path.attachNewNode(self.tail_geom_node)
        self._ballIval = None
        return

    def removeNode(self):
        self.ignoreAll()
        NodePath.removeNode(self)

    def _setRadius(self, radius, reset=True):
        self._radius = radius

    def _setScrollFactor(self, scrollFactor, reset=True):
        self._scrollFactor = float(scrollFactor)

    def _setCamera(self, cam, reset=True):
        self.cam = cam
        self.camNode = cam.node()
        self.camLens = self.camNode.getLens()

    def _setFrame(self, frame, reset=True):
        self._frame = frame
        self.saveTransforms()

    def _setKeepUpright(self, keepUpright):
        self._keepUpright = keepUpright

    def _setControlButtonState(self, state):
        self._ctrlBtnState = state

    def _setTiltLimit(self, limit=math.pi / 6, reset=True):
        self._tiltLimit = limit
        if reset:
            self._applyConstraints()

    def _setMouseEvents(self, down, up):
        if hasattr(self, '_mouseDownEventStr'):
            self.ignore(self._mouseDownEventStr)
        if hasattr(self, '_mouseUpEventStr'):
            self.ignore(self._mouseUpEventStr)
        self._mouseDownEventStr = down
        self._mouseUpEventStr = up
        self.accept(self._mouseDownEventStr, self._mouseDown)
        self.accept(self._mouseUpEventStr, self._mouseUp)

    def setRadius(self, radius):
        self._setRadius(radius)

    def setScrollFactor(self, scrollFactor):
        self._setScrollFactor(scrollFactor)

    def setCamera(self, camera):
        self._setCamera(camera)

    def setFrame(self, frame):
        self._setFrame(frame)

    def setKeepUpright(self, keepUpright):
        self._setKeepUpright(keepUpright)

    def setMouseEvents(self, downEvent, upEvent):
        self._setMouseEvents(downEvent, upEvent)

    def setMouseEnabled(self, enabled):
        self._mouseEnabled = enabled
        if not self._mouseEnabled:
            self._mouseUp()

    def setRotateMode(self, mode):
        self.rMode = mode

    def enable(self):
        self.setMouseEnabled(True)

    def disable(self):
        if self._ballIval:
            self._ballIval.pause()
            self._ballIval = None
        self.setMouseEnabled(False)
        return

    def getRotateRoot(self):
        return self._rNode

    def attachForRotation(self, nodepath):
        nodepath.reparentTo(self._rNode)

    def getInternalHpr(self, *args, **kwargs):
        return self._rNode.getHpr(*args, **kwargs)

    def setInternalHpr(self, *args, **kwargs):
        self._rNode.setHpr(*args, **kwargs)

    def getInternalQuat(self, *args, **kwargs):
        return self._rNode.getQuat(*args, **kwargs)

    def setInternalQuat(self, *args, **kwargs):
        self._rNode.setQuat(*args, **kwargs)

    def _mouseDown(self, *args):
        if self._mouseEnabled:
            self._startRotateTask()

    def _mouseUp(self, *args):
        self._stopRotateTask()

    def _initCollisions(self):
        self.traverser = CollisionTraverser()
        self.colHandlerQueue = CollisionHandlerQueue()
        self.camRayNode = self.cam.attachNewNode(CollisionNode('camRayNode'))
        self.camRay = CollisionRay()
        self.camRayNode.node().addSolid(self.camRay)
        self.traverser.addCollider(self.camRayNode, self.colHandlerQueue)

    def _mouseRayCollide(self, rayBitMask=BitMask32.allOn()):
        if base.mouseWatcherNode.hasMouse():
            mousePt = base.mouseWatcherNode.getMouse()
            mousePt = self._transMouseToHomogenousFramePt(mousePt)
            self.camRay.setFromLens(self.camNode, mousePt[0], mousePt[1])
            self.camRayNode.node().setFromCollideMask(rayBitMask)
            self.traverser.traverse(self)
            self.traverser.traverse(self.getTop())
        else:
            self.colHandlerQueue.clearEntries()

    def _camRayCollide(self, rayBitMask=BitMask32.allOn()):
        self.camRay.setOrigin(Point3(0))
        self.camRay.setDirection(Vec3(0, 1, 0))
        self.camRayNode.node().setFromCollideMask(rayBitMask)
        self.traverser.traverse(self)
        self.traverser.traverse(self.getTop())

    def getHorizonCollisionPt(self, raySpace=None, rayDirection=None):
        raySpaceToSelf = raySpace.getTransform(self)
        rayOrig = raySpaceToSelf.getMat().xformPoint(Point3(0))
        rayDist = rayOrig.length()
        ray = raySpaceToSelf.getMat().xformPoint(rayDirection)
        a = rayOrig * (self._radius * self._radius) / (rayDist * rayDist)
        b = (-rayOrig).cross(ray).cross(-rayOrig)
        b.normalize()
        b *= math.sqrt(1 - 1 / rayDist / rayDist)
        return a + b

    def _getCollisionPt(self):
        entryCount = self.colHandlerQueue.getNumEntries()
        for x in range(entryCount):
            entry = self.colHandlerQueue.getEntry(x)
            if entry.getIntoNode().getName() == self.getName() + '-cNode':
                return entry.getSurfacePoint(entry.getIntoNodePath())

        camRay = self.camRayNode.node().getSolid(0).getDirection()
        pt = self.getHorizonCollisionPt(self.cam, camRay)
        return pt

    def getMouseRayCollisionPt(self, rayBitMask=None):
        if not rayBitMask:
            rayBitMask = self._colBitMask
        self._mouseRayCollide(rayBitMask)
        return self._getCollisionPt()

    def getCamRayCollisionPt(self, rayBitMask=None):
        if not rayBitMask:
            rayBitMask = self._colBitMask
        self._camRayCollide(rayBitMask)
        return self._getCollisionPt()

    def _getCollisionEntry(self):
        entryCount = self.colHandlerQueue.getNumEntries()
        if entryCount:
            self.colHandlerQueue.sort()
            return self.colHandlerQueue.getEntry(0)
        else:
            return None
        return None

    def getMouseRayCollisionEntry(self, rayBitMask=None):
        if not rayBitMask:
            rayBitMask = self._colBitMask
        self._mouseRayCollide(rayBitMask)
        return self._getCollisionEntry()

    def saveTransforms(self):
        frame = self._frame
        ll = Point3(frame[0], frame[2], 0)
        ur = Point3(frame[1], frame[3], 0)
        aspectTs = TransformState.makeScale2d(Point2(1 / base.camLens.getAspectRatio(), 1))
        ll = aspectTs.getMat().xformPoint(ll)
        ur = aspectTs.getMat().xformPoint(ur)
        posTs = TransformState.makePos2d(Point2(ll[0] + ur[0], ll[1] + ur[1]) / -2.0)
        scaleTs = TransformState.makeScale2d(Point2(2.0 / (ur[0] - ll[0]), 2.0 / (ur[1] - ll[1])))
        frameTs = scaleTs.compose(posTs)
        self._mouseToHomogenousFrameMat = Mat4(frameTs.getMat())
        self._mouseToHomogenousFrameMatInv = Mat4(frameTs.getInverse().getMat())
        self._camLensProjMat = Mat4(self.camLens.getProjectionMat())
        self._camLensProjMatInv = Mat4(self._camLensProjMat)
        self._camLensProjMatInv.invertInPlace()

    def _transMouseToHomogenousFramePt(self, pt):
        pt = Point3(pt[0], pt[1], 0)
        return self._mouseToHomogenousFrameMat.xformPoint(pt)

    def _transHomogenousFrameToMousePt(self, pt):
        return self._mouseToHomogenousFrameMatInv.xformPoint(pt)

    def _transCamSpaceToHomogenousFramePt(self, pt):
        pt = self._camLensProjMat.xform(Vec4(pt[0], pt[1], pt[2], 1))
        pt /= pt[3]
        return pt

    def _transHomogenousFrameToCamSpacePt(self, pt):
        pt = self._camLensProjMatInv.xform(Vec4(pt[0], pt[1], pt[2], 1))
        pt /= pt[3]
        return pt

    def setNorth(self, northVec):
        self._north = northVec

    def saveNorth(self):
        upSpaceNodePath = self
        Z = Vec3.unitZ()
        upSpaceToRNode = TransformState.makeHpr(upSpaceNodePath.getHpr(self._rNode))
        self._north = upSpaceToRNode.getMat().xformPoint(Z)

    def _applyConstraints(self):
        self._rotate(self.getOrthTiltLimitQuat(self._tiltLimit), 1.0)
        if self._keepUpright:
            self.clampOrientationAboutSpherePt(self.getCamRayCollisionPt())

    def getTiltLimitQuat(self, thetaLimit):
        Y = Vec3.unitY()
        Z = Vec3.unitZ()
        upSpaceNodePath = self
        rNodeNorth = Z
        arcballNorth = -Y
        rNodeToUpSpace = TransformState.makeHpr(self._rNode.getHpr(upSpaceNodePath))
        northPole = rNodeToUpSpace.getMat().xformPoint(rNodeNorth)
        dot = northPole.dot(arcballNorth)
        theta = math.acos(clampScalar(-1, 1, dot))
        if theta < thetaLimit:
            return Quat.identQuat()
        else:
            axis = northPole.cross(arcballNorth)
            axis.normalize()
            theta -= thetaLimit
            return Quat(math.cos(theta / 2.0), axis * math.sin(theta / 2.0))

    def getOrthTiltLimitQuat(self, thetaLimit=10):
        X = Vec3.unitX()
        Y = Vec3.unitY()
        Z = Vec3.unitZ()
        upSpaceNodePath = self
        rNodeNorth = Z
        arcballNorth = -Y
        baseQuat = self._rNode.getQuat(upSpaceNodePath)
        quatX = Quat.identQuat()
        quatY = Quat.identQuat()
        rNodeToUpSpace = TransformState.makeQuat(baseQuat)
        northPole = rNodeToUpSpace.getMat().xformPoint(rNodeNorth)
        dot = northPole.dot(X)
        proj = northPole - X * dot
        theta = math.acos(clampScalar(-1.0, 1.0, proj.dot(arcballNorth) / proj.length()))
        if theta > thetaLimit:
            theta -= thetaLimit
            if northPole.dot(Z) < 0.0:
                theta *= -1
            quatX = Quat(math.cos(theta / 2.0), X * math.sin(theta / 2.0))
            baseQuat *= quatX
            rNodeToUpSpace = TransformState.makeQuat(baseQuat)
            northPole = rNodeToUpSpace.getMat().xformPoint(rNodeNorth)
        dot = northPole.dot(Z)
        proj = northPole - Z * dot
        theta = math.acos(clampScalar(-1.0, 1.0, proj.dot(arcballNorth) / proj.length()))
        if theta > thetaLimit:
            theta -= thetaLimit
            if northPole.dot(X) >= 0.0:
                theta *= -1
            quatY = Quat(math.cos(theta / 2.0), Z * math.sin(theta / 2.0))
            baseQuat *= quatY
        return quatX * quatY

    def getUprightCorrectionQuat(self, pt):
        Y = Vec3.unitY()
        Z = Vec3.unitZ()
        rNodeNorth = self._north
        upSpaceNodePath = self
        axis = pt / pt.length()
        up = Z
        rNodeToUpSpace = TransformState.makeHpr(self._rNode.getHpr(upSpaceNodePath))
        northPole = rNodeToUpSpace.getMat().xformPoint(rNodeNorth)
        right = up.cross(axis)
        final = axis.cross(right)
        dot = northPole.dot(axis)
        proj = northPole - axis * dot
        theta = math.acos(clampScalar(-1.0, 1.0, proj.dot(final) / (proj.length() * final.length())))
        if northPole.dot(right) < 0.0:
            theta *= -1
        return Quat(math.cos(theta / 2.0), Vec3(axis) * math.sin(theta / 2.0))

    def _rotate(self, q, factor=1.0):
        q = nLerp(Quat(1, Vec3(0)), q, factor)
        self._rNode.setQuat(self._rNode.getQuat() * q)

    def _rotatePtToPt(self, p0, p1, factor=1.0):
        self._rotate(self._getPtToPtQuat(p0, p1), factor)

    def _getPtToPtQuat(self, p0, p1, factor=1.0):
        p0.normalize()
        p1.normalize()
        theta = math.acos(clampScalar(-1, 1, p0.dot(p1)))
        axis = p0.cross(p1)
        axis.normalize()
        if factor == 1.0:
            return Quat(math.cos(theta / 2.0), axis * math.sin(theta / 2.0))
        elif 0.0 < factor < 1.0:
            q = nLerp(Quat.identQuat(), Quat(math.cos(theta / 2.0), axis * math.sin(theta / 2.0)), factor)
            return q

    def _getRotateAboutAxisQuat(self, axis, p0, p1, factor=1.0):
        axis = axis / axis.length()
        dot0 = axis.dot(p0)
        proj0 = p0 - axis * dot0
        dot1 = axis.dot(p1)
        proj1 = p1 - axis * dot1
        axis = proj0.cross(proj1)
        area = axis.length()
        axis.normalize()
        theta = math.acos(clampScalar(-1, 1, proj0.dot(proj1) / (proj0.length() * proj1.length())))
        return (
         Quat(math.cos(theta / 2.0), axis * math.sin(theta / 2.0)), area)

    def _rotateQuatByQuat(self, q0, q1, factor=1.0):
        self._rNode.setQuat(nLerp(q0, q0 * q1, factor))

    def clampOrientationAboutSpherePt(self, pt):
        q = self.getUprightCorrectionQuat(pt)
        self._rotate(q, 1.0)

    def rotatePtToCenter(self, pt):
        centerPt = self.getCamRayCollisionPt()
        self._rotatePtToPt(pt, centerPt)
        self._applyConstraints()

    def rotateSpherePtToCenter(self, spherePt):
        pt = self._colNode.getRelativePoint(self._rNode, spherePt)
        self.rotatePtToCenter(pt)

    def clampSpherePtToHorizon(self, pt):
        camRaySpherePt = self.findCamRaySpherePt(pt)
        if camRaySpherePt and not pt.almostEqual(camRaySpherePt, 0.0001):
            camToSphere = self.cam.getTransform(self._rNode)
            OC = camToSphere.getMat().xformPoint(Vec3(0, 0, 0))
            theta = math.acos(clampScalar(-1.0, 1.0, self._radius / OC.length()))
            axis = OC.cross(pt)
            axis.normalize()
            q = Quat(math.cos(theta / 2), axis * math.sin(theta / 2))
            ts = TransformState.makeQuat(q)
            OC.normalize()
            OC *= self._radius
            newPt = ts.getMat().xformPoint(OC)
            dTheta = math.acos(clampScalar(-1.0, 1.0, pt.dot(newPt)))
            return (
             newPt, dTheta)
        else:
            return (
             pt, 0)

    def reorientNorth(self, time=0.0):
        self.setNorth(Vec3(0, 1, 0))
        curQ = self.getInternalQuat()
        pt = self.getCamRayCollision()
        upQ = self.getUprightCorrectionQuat(pt)

        def rotateFunc(t):
            self._rotateQuatByQuat(curQ, upQ, t)

        if self._ballIval:
            self._ballIval.pause()
        self._ballIval = LerpFunc(rotateFunc, duration=time)
        self._ballIval.start()

    def showRotationSphere(self):
        if not hasattr(self, '_ArcBall_rotGuide'):
            self._rotGuide = loader.loadModel('models/misc/sphere')
            self._rotGuide.setName('RotationGuide')
            self._rotGuide.setRenderModeWireframe()
            self._rotGuide.setTwoSided(1)
            self._rotGuide.setTextureOff(1)
            self._rotGuide.setColor(Vec4(1, 0, 0, 1))
            self._rotGuide.reparentTo(self.getRotateRoot())
        self._rotGuide.setScale(self._radius)
        self._rotGuide.show()

    def hideRotationSphere(self):
        if hasattr(self, '_ArcBall_rotGuide'):
            self._rotGuide.hide()

    def _startRotateTask(self, *args):
        self.saveTransforms()
        modePairs = (
         (0, 2), (1, 3))
        if not self._ctrlBtnState:
            rMode = modePairs[self.rMode][0]
        else:
            rMode = modePairs[self.rMode][1]
        if self.rMode in [1]:
            props = WindowProperties()
            props.setCursorHidden(1)
            base.win.requestProperties(props)
        task = taskMgr.add(self._rotateTask, self.getName() + '-rotateTask')
        task.rMode = rMode

    def _rotateTask(self, task):
        if not hasattr(task, 'startPt'):
            task.startPt = self.getMouseRayCollisionPt()
            task.camPt = self.getCamRayCollisionPt()
            task.quat = self._rNode.getQuat()
        if task.rMode == 0:
            pt = self.getMouseRayCollisionPt()
            q = self._getPtToPtQuat(task.startPt, pt)
            self._rotateQuatByQuat(task.quat, q, 1.0)
            self._applyConstraints()
        elif task.rMode == 1:
            dt = globalClock.getDt()
            pt = self.getMouseRayCollisionPt()
            self._rotatePtToPt(pt, task.startPt, dt * self._scrollFactor * 5)
            self._applyConstraints()
            self.createStraightArrow(task.startPt, pt, 0.02)
        elif task.rMode == 2:
            pt = self.getMouseRayCollisionPt()
            q, area = self._getRotateAboutAxisQuat(task.camPt, task.startPt, pt)
            self._rotateQuatByQuat(task.quat, q, 1.0)
            self.saveNorth()
        elif task.rMode == 3:
            dt = globalClock.getDt()
            pt = self.getMouseRayCollisionPt()
            q, area = self._getRotateAboutAxisQuat(task.camPt, pt, task.startPt)
            self._rotate(q, dt * self._scrollFactor * area * 300)
            self.createCurvedArrow(task.camPt, pt, task.startPt, 0.02)
            self.saveNorth()
        return task.cont

    def _stopRotateTask(self, *args):
        taskMgr.remove(self.getName() + '-rotateTask')
        self.tail_geom_node.removeAllGeoms()
        self.head_geom_node.removeAllGeoms()
        if self.rMode in [1]:
            props = WindowProperties()
            props.setCursorHidden(0)
            base.win.requestProperties(props)

    def createStraightArrow(self, p0, p1, width):
        p0.normalize()
        p1.normalize()
        dot = p0.dot(p1)
        cross = p0.cross(p1)
        arcLen = math.acos(clampScalar(-1, 1, dot))
        self.tail_geom_node.removeAllGeoms()
        self.head_geom_node.removeAllGeoms()
        if arcLen > 0.0:
            cross.normalize()
            cross *= width / 2.0
            theta = 2 * math.asin(width / 2.0)
            div = arcLen / theta
            steps = int(div)
            remainder = div - steps
            pts = []
            for n in range(steps + 1):
                pts.append(sLerp(p1, p0, n / div, arcLen) * self._radius)

            format = GeomVertexFormat.getV3c4t2()
            vertex_data = GeomVertexData('arc_ball', format, Geom.UHStatic)
            vertex_writer = GeomVertexWriter(vertex_data, 'vertex')
            color_writer = GeomVertexWriter(vertex_data, 'color')
            texture_writer = GeomVertexWriter(vertex_data, 'texcoord')
            triStrip = GeomTristrips(Geom.UHStatic)
            if len(pts) == 1:
                vertex_writer.addData3f(p1[0] - cross[0], p1[1] - cross[1], p1[2] - cross[2])
                vertex_writer.addData3f(p1[0] + cross[0], p1[1] + cross[1], p1[2] + cross[2])
                color_writer.addData4f(0, 1, 0, 1)
                color_writer.addData4f(0, 1, 0, 1)
                texture_writer.addData2f(1, 1)
                texture_writer.addData2f(0, 1)
                vertex_writer.addData3f(p0[0] - cross[0], p0[1] - cross[1], p0[2] - cross[2])
                vertex_writer.addData3f(p0[0] + cross[0], p0[1] + cross[1], p0[2] + cross[2])
                color_writer.addData4f(0, 1, 0, 1)
                color_writer.addData4f(0, 1, 0, 1)
                texture_writer.addData2f(1, 1 - remainder)
                texture_writer.addData2f(0, 1 - remainder)
                triStrip.addNextVertices(4)
            else:
                for pt in pts[:2]:
                    vertex_writer.addData3f(pt[0] - cross[0], pt[1] - cross[1], pt[2] - cross[2])
                    vertex_writer.addData3f(pt[0] + cross[0], pt[1] + cross[1], pt[2] + cross[2])
                    color_writer.addData4f(0, 1, 0, 1)
                    color_writer.addData4f(0, 1, 0, 1)

                texture_writer.addData2f(1, 1)
                texture_writer.addData2f(0, 1)
                texture_writer.addData2f(1, 0)
                texture_writer.addData2f(0, 0)
                triStrip.addNextVertices(4)
            geometry = Geom(vertex_data)
            geometry.addPrimitive(triStrip)
            self.head_geom_node.addGeom(geometry)
            format = GeomVertexFormat.getV3c4t2()
            vertex_data = GeomVertexData('arc_ball', format, Geom.UHStatic)
            vertex_writer = GeomVertexWriter(vertex_data, 'vertex')
            color_writer = GeomVertexWriter(vertex_data, 'color')
            texture_writer = GeomVertexWriter(vertex_data, 'texcoord')
            triStrip = GeomTristrips(Geom.UHStatic)
            for pt in pts[1:]:
                vertex_writer.addData3f(pt[0] - cross[0], pt[1] - cross[1], pt[2] - cross[2])
                vertex_writer.addData3f(pt[0] + cross[0], pt[1] + cross[1], pt[2] + cross[2])
                color_writer.addData4f(0, 1, 0, 1)
                color_writer.addData4f(0, 1, 0, 1)

            numPts = len(pts[1:])
            for x in range(numPts / 2):
                texture_writer.addData2f(1, 1)
                texture_writer.addData2f(0, 1)
                texture_writer.addData2f(1, 0)
                texture_writer.addData2f(0, 0)

            if numPts % 2:
                texture_writer.addData2f(1, 1)
                texture_writer.addData2f(0, 1)
            vertex_writer.addData3f(p0[0] - cross[0], p0[1] - cross[1], p0[2] - cross[2])
            vertex_writer.addData3f(p0[0] + cross[0], p0[1] + cross[1], p0[2] + cross[2])
            color_writer.addData4f(0, 1, 0, 1)
            color_writer.addData4f(0, 1, 0, 1)
            if numPts % 2:
                texture_writer.addData2f(1, 1 - remainder)
                texture_writer.addData2f(0, 1 - remainder)
            else:
                texture_writer.addData2f(1, remainder)
                texture_writer.addData2f(0, remainder)
            triStrip.addNextVertices(numPts * 2 + 2)
            geometry = Geom(vertex_data)
            geometry.addPrimitive(triStrip)
            self.tail_geom_node.addGeom(geometry)

    def createCurvedArrow(self, axis, p0, p1, width, numPanels=10):
        N = numPanels
        self.tail_geom_node.removeAllGeoms()
        self.head_geom_node.removeAllGeoms()
        axis = axis / axis.length()
        dot0 = axis.dot(p0)
        proj0 = p0 - axis * dot0
        dot1 = axis.dot(p1)
        proj1 = p1 - axis * dot1
        theta = math.acos(clampScalar(-1, 1, proj0.dot(proj1) / (proj0.length() * proj1.length())))
        if not proj0.almostEqual(proj1, 0.0001) and theta != 0:
            if proj0.lengthSquared() >= proj1.lengthSquared():
                A = proj0
                C = proj1
            else:
                A = proj1
                C = proj0
            a = A.length()
            aUnit = A / a
            x = A.dot(C) / a
            yy = C.lengthSquared() - x * x
            bUnit = A.cross(C).cross(A)
            bUnit.normalize()
            b = math.sqrt(max(0.0, yy / (1 - x * x / (a * a))))
            t = math.atan2(a, b / math.tan(theta))
            aUnit *= a
            bUnit *= b
            pts = [ aUnit * math.cos(x * t / N) + bUnit * math.sin(x * t / N) for x in range(N + 1) ]
            pts = [ pt + axis * math.sqrt(self._radius * self._radius - pt.lengthSquared()) for pt in pts ]
            if A != proj0:
                pts.reverse()
            format = GeomVertexFormat.getV3c4t2()
            vertex_data = GeomVertexData('arc_ball', format, Geom.UHStatic)
            vertex_writer = GeomVertexWriter(vertex_data, 'vertex')
            color_writer = GeomVertexWriter(vertex_data, 'color')
            texture_writer = GeomVertexWriter(vertex_data, 'texcoord')
            triStrip = GeomTristrips(Geom.UHStatic)
            cross = pts[0].cross(pts[1] - pts[0])
            cross.normalize()
            cross *= width / 2.0
            pt = pts[0]
            vertex_writer.addData3f(pt[0] + cross[0], pt[1] + cross[1], pt[2] + cross[2])
            vertex_writer.addData3f(pt[0] - cross[0], pt[1] - cross[1], pt[2] - cross[2])
            color_writer.addData4f(0, 1, 0, 1)
            color_writer.addData4f(0, 1, 0, 1)
            texture_writer.addData2f(0, 1)
            texture_writer.addData2f(1, 1)
            diffA = pts[1] - pts[0]
            diffB = pts[2] - pts[1]
            cross = pts[1].cross((diffB + diffA) / 2.0)
            cross.normalize()
            cross *= width / 2.0
            pt = pts[1]
            vertex_writer.addData3f(pt[0] + cross[0], pt[1] + cross[1], pt[2] + cross[2])
            vertex_writer.addData3f(pt[0] - cross[0], pt[1] - cross[1], pt[2] - cross[2])
            color_writer.addData4f(0, 1, 0, 1)
            color_writer.addData4f(0, 1, 0, 1)
            texture_writer.addData2f(0, 0)
            texture_writer.addData2f(1, 0)
            triStrip.addNextVertices(4)
            geometry = Geom(vertex_data)
            geometry.addPrimitive(triStrip)
            self.head_geom_node.addGeom(geometry)
            format = GeomVertexFormat.getV3c4t2()
            vertex_data = GeomVertexData('arc_ball', format, Geom.UHStatic)
            vertex_writer = GeomVertexWriter(vertex_data, 'vertex')
            color_writer = GeomVertexWriter(vertex_data, 'color')
            texture_writer = GeomVertexWriter(vertex_data, 'texcoord')
            triStrip = GeomTristrips(Geom.UHStatic)
            for x in range(len(pts[1:-1])):
                cross = pts[x + 1].cross(pts[x + 2] - pts[x])
                cross.normalize()
                cross *= width / 2.0
                pt = pts[x + 1]
                vertex_writer.addData3f(pt[0] + cross[0], pt[1] + cross[1], pt[2] + cross[2])
                vertex_writer.addData3f(pt[0] - cross[0], pt[1] - cross[1], pt[2] - cross[2])
                color_writer.addData4f(0, 1, 0, 1)
                color_writer.addData4f(0, 1, 0, 1)
                if x % 2:
                    texture_writer.addData2f(0, 1)
                    texture_writer.addData2f(1, 1)
                else:
                    texture_writer.addData2f(0, 0)
                    texture_writer.addData2f(1, 0)
                triStrip.addNextVertices(2)

            cross = pts[-1].cross(pts[-1] - pts[-2])
            cross.normalize()
            cross *= width / 2.0
            pt = pts[-1]
            vertex_writer.addData3f(pt[0] + cross[0], pt[1] + cross[1], pt[2] + cross[2])
            vertex_writer.addData3f(pt[0] - cross[0], pt[1] - cross[1], pt[2] - cross[2])
            color_writer.addData4f(0, 1, 0, 1)
            color_writer.addData4f(0, 1, 0, 1)
            if N % 2:
                texture_writer.addData2f(0, 0)
                texture_writer.addData2f(1, 0)
            else:
                texture_writer.addData2f(0, 1)
                texture_writer.addData2f(1, 1)
            triStrip.addNextVertices(2)
            geometry = Geom(vertex_data)
            geometry.addPrimitive(triStrip)
            self.tail_geom_node.addGeom(geometry)

    def _startArrowTask(self):
        taskMgr.add(self._arrowTask, self.getName() + '-arrowTask')

    def _arrowTask(self, task):
        if not hasattr(task, 'p0'):
            task.p0 = self.getMouseRayCollisionPt()
            task.p0.normalize()
        p1 = self.getMouseRayCollisionPt()
        p1.normalize()
        self.createStraightArrow(task.p0, p1, 0.02)
        return task.cont

    def _stopArrowTask(self):
        taskMgr.remove(self.getName() + '-arrowTask')