

class Mappable():

    def __init__(self):
        pass

    def getMapNode(self):
        return None


class MappableArea(Mappable):

    def getMapName(self):
        return ''

    def getZoomLevels(self):
        return ((100, 200, 300), 1)

    def getFootprintNode(self):
        return None

    def getShopNodes(self):
        return ()

    def getCapturePointNodes(self, holidayId):
        return ()


class MappableGrid(MappableArea):

    def getGridParamters(self):
        return ()