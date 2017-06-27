from pandac.PandaModules import *
from direct.showbase.PythonUtil import clampScalar
from pirates.map.ArcBall import ArcBall
import math

class MapBall(ArcBall):

    def __init__(self, name, worldMap, maxTilt=math.pi / 4, mapSize=2.0, *args, **kwargs):
        ArcBall.__init__(self, name, *args, **kwargs)
        self.worldMap = worldMap
        maxTilt = clampScalar(0, math.pi / 4.0, maxTilt)
        _maxDist = math.tan(maxTilt * 2)
        self.tsMat = Mat3(TransformState.makeScale2d(Vec2(_maxDist / (mapSize / 2.0))).getMat3())
        self.tsMatInv = invert(self.tsMat)
        self._mapOrigin = self.mapPosToSpherePt(Point2(0))
        self._worldNorth = Point3(0, 1, 0)
        self._loadModels()

    def mapPosToSpherePt(self, mapPos):
        pt = self.tsMat.xformPoint(Point2(mapPos[0], mapPos[1]))
        try:
            theta = math.acos(2 / Vec3(pt[0], pt[1], 2).length())
        except ValueError:
            theta = 0

        sinTheta = math.sin(theta)
        z = 1 - 2 * sinTheta * sinTheta
        coef = (z + 1) / 2.0
        return Vec3(pt[0] * coef, pt[1] * coef, z)

    def spherePtToMapPos(self, spherePt):
        t = 2 / (spherePt[2] - 1)
        pt = Point2(spherePt[0], spherePt[1]) * t
        return self.tsMatInv.xformPoint(pt)

    def rotateMapPosToCenter(self, mapPos):
        spherePt = self.mapPosToSpherePt(mapPos)
        self.rotateSpherePtToCenter(spherePt)

    def _loadModels(self):
        self._modelInfo = {'globe': 'models/worldmap/world_map_globe'}
        self._models = dict(zip(self._modelInfo, (loader.loadModel(self._modelInfo[name]) for name in self._modelInfo)))
        self.attachForRotation(self._models['globe'])
        self._models['globe'].setBin('background', 0)
        self._models['globe'].setDepthWrite(0)
