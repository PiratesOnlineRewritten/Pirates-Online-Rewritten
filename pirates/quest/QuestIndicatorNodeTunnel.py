from pandac.PandaModules import Point3
from pirates.piratesgui.RadarGui import *
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from direct.showbase.PythonUtil import report, StackTrace

class QuestIndicatorNodeTunnel(QuestIndicatorNode):
    LOD_CENTER_OFFSET_X = 30

    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'TunnelIndicator', [
         self.LOD_CENTER_OFFSET_X], questStep)
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        self.ignore('tunnelSetLinks')
        QuestIndicatorNode.delete(self)
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def placeInWorld(self):

        @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
        def stepObjHere(tunnelObj):
            self.pendingStepObj = None
            area = base.cr.getDo(self.questStep.getOriginDoId())
            areaUid = area.getUniqueId()
            areaNodeName = tunnelObj.getAreaNodeNameFromAreaUid(areaUid)
            areaNode = area.getConnectorNodeNamed(areaNodeName)
            self.reparentTo(areaNode)
            self.setPosHpr(0, 0, 0, 0, 0, 0)
            self.setPos(self, self.LOD_CENTER_OFFSET_X, 0, 5)
            self.wrtReparentTo(area)
            return

        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        self.pendingStepObj = base.cr.relatedObjectMgr.requestObjects([self.questStep.getStepDoId()], eachCallback=stepObjHere)
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def loadZoneLevel(self, level):
        QuestIndicatorNode.loadZoneLevel(self, level)
        if level == 0:
            self.request('At')
        elif level == 1:
            self.request('Far')

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def unloadZoneLevel(self, level):
        QuestIndicatorNode.unloadZoneLevel(self, level)
        if level == 0:
            self.request('Far')
        elif level == 1:
            self.request('Off')

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def enterAt(self):
        QuestIndicatorNode.enterAt(self)
        self.pendingStepObj = None
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def exitAt(self):
        QuestIndicatorNode.exitAt(self)

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def startFarEffect(self):
        QuestIndicatorNode.startFarEffect(self)
        if self.farEffect:
            self.farEffect.setPos(0, 0, -5)

    def setZoneRadii(self, zoneRadii, zoneCenter=[0, 0]):
        QuestIndicatorNode.setZoneRadii(self, zoneRadii, zoneCenter)
        self.setZoneLODOffset(-1, Point3(-self.LOD_CENTER_OFFSET_X, 0, 0))