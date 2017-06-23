from pandac.PandaModules import CardMaker, NodePath

def getBeaconModel():
    return loader.loadModel('models/textureCards/pvp_arrow').find('**/pvp_arrow')


__beacon = None

def initBeacon():
    global __beacon
    geom = getBeaconModel()
    geom.setBillboardAxis(1)
    geom.setZ(1)
    geom.setScale(2)
    __beacon = geom


initBeacon()

def getBeacon(parent):
    return __beacon.copyTo(parent)