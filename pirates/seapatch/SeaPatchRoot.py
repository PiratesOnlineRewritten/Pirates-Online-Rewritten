
class SeaPatchRoot(object):

    def __init__(self):
        self.seaLevel = 0
        self.center = None
        self.anchor = None

    def setSeaLevel(self, seaLevel):
        self.seaLevel = seaLevel

    def getSeaLevel(self):
        return self.seaLevel

    def setCenter(self, center):
        self.center = center

    def getCenter(self):
        return self.center

    def setAnchor(self, anchor):
        self.anchor = anchor

    def getAnchor(self):
        return self.anchor

    def resetProperties(self):
        pass

    def animateHeight(self, doAnimate):
        pass

    def animateUv(self, doAnimate):
        pass

    def enable(self):
        pass

    def disable(self):
        pass
