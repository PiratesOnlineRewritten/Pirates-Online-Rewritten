

class TargetManagerBase():

    def __init__(self):
        self.objectDict = {}

    def delete(self):
        del self.objectDict

    def getUniqueId(self, obj):
        return obj.get_key()

    def addTarget(self, nodePathId, obj):
        self.objectDict[nodePathId] = obj

    def removeTarget(self, nodePathId):
        if self.objectDict.has_key(nodePathId):
            del self.objectDict[nodePathId]

    def getObjectFromNodepath(self, nodePath):
        target = nodePath.getNetPythonTag('MonstrousObject')
        if not target:
            target = self.objectDict.get(nodePath.get_key(), None)
        return target