from pandac.PandaModules import LineSegs, NodePath
import math

class RepairSawingLine():

    def __init__(self, parent, thickness, color, lineSpawnDist=0.01):
        self.points = []
        self.parent = parent
        self.thickness = thickness
        self.color = color
        self.lineNode = None
        self.lineDrawer = LineSegs()
        self.lineDrawer.setThickness(thickness)
        self.lineSpawnDist = lineSpawnDist
        self.currentPoint = None
        self.startPoint = None
        self.redraw()
        return

    def redraw(self):
        self.clearLine()
        self.lineDrawer.reset()
        self.lineDrawer.setThickness(self.thickness)
        self.lineDrawer.setColor(self.color)
        if len(self.points) > 0:
            self.lineDrawer.moveTo(self.points[0])
            for i in range(1, len(self.points)):
                p = self.points[i]
                self.lineDrawer.drawTo(p)
                self.currentPoint = p

        self.lineNode = NodePath(self.lineDrawer.create())
        self.lineNode.reparentTo(self.parent)
        self.lineNode.setBin('fixed', 37)
        self.lineNode.setTransparency(True)

    def update(self, point):
        if self.currentPoint == None or (point - self.currentPoint).length() >= self.lineSpawnDist:
            self.addPoint(point)
            self.redraw()
        return

    def addPoint(self, p):
        if len(self.points) == 0:
            self.startPoint = p
        self.points.append(p)

    def clearLine(self):
        if self.lineNode != None:
            self.lineNode.removeNode()
        return

    def reset(self):
        self.clearLine()
        self.points = []
        self.redraw()
        self.currentPoint = None
        self.startPoint = None
        return

    def show(self):
        self.lineNode.unstash()

    def hide(self):
        self.lineNode.stash()