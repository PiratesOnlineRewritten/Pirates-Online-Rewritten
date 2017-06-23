from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from pirates.effects.FireworkGlobals import *
from pirates.effects.FireworkShow import FireworkShow
PortRoyalLocation = Point3(-1350, 180, 220)
PortRoyalLocation2 = Point3(50, 1500, 0)
PortRoyalH = 100.0
TortugaLocation = Point3(10525, 19000, 245)
TortugaLocation2 = Point3(8900, 18500, 80)
TortugaH = 0.0
PadresLocation = Point3(6700, -22800, 100)
PadresH = 0.0

class FireworkShowManager():

    def __init__(self):
        self.showType = None
        self.PortRoyalShow = None
        self.TortugaShow = None
        self.PadresShow = None
        return

    def beginPortRoyalShow(self, offset):
        taskMgr.remove('beginPortRoyalShow')
        if not self.PortRoyalShow:
            self.PortRoyalShow = FireworkShow(self.showType)
            self.PortRoyalShow.reparentTo(render)
            self.PortRoyalShow.setPos(PortRoyalLocation)
            self.PortRoyalShow.setH(PortRoyalH)
            self.PortRoyalShow.begin(offset)

    def beginTortugaShow(self, offset):
        taskMgr.remove('beginTortugaShow')
        if not self.TortugaShow:
            self.TortugaShow = FireworkShow(self.showType)
            self.TortugaShow.reparentTo(render)
            self.TortugaShow.setPos(TortugaLocation)
            self.TortugaShow.setH(TortugaH)
            self.TortugaShow.begin(offset)

    def beginPadresShow(self, offset):
        taskMgr.remove('beginPadresShow')
        if not self.PadresShow:
            self.PadresShow = FireworkShow(self.showType)
            self.PadresShow.reparentTo(render)
            self.PadresShow.setPos(PadresLocation)
            self.PadresShow.setH(PadresH)
            self.PadresShow.begin(offset)

    def enable(self, showType, timeOffset):
        self.showType = showType
        showDuration = 0.0
        if self.showType == FireworkShowType.FourthOfJuly:
            showDuration = 105.0
        wait = 10.0
        if timeOffset <= showDuration + wait:
            delay = max(0.0, wait - timeOffset)
            offset = max(0.0, timeOffset - delay - wait)
            taskMgr.doMethodLater(delay, self.beginPortRoyalShow, 'beginPortRoyalShow', extraArgs=[offset])
        timeOffset = timeOffset - (showDuration + wait)
        if timeOffset <= showDuration + wait:
            delay = max(0.0, wait - timeOffset)
            offset = max(0.0, timeOffset - delay - wait)
            taskMgr.doMethodLater(delay, self.beginTortugaShow, 'beginTortugaShow', extraArgs=[offset])
        timeOffset = timeOffset - (showDuration + wait)
        if timeOffset <= showDuration + wait:
            delay = max(0.0, wait - timeOffset)
            offset = max(0.0, timeOffset - delay - wait)
            taskMgr.doMethodLater(delay, self.beginPadresShow, 'beginPadresShow', extraArgs=[offset])

    def disable(self):
        self.showType = None
        taskMgr.remove('beginPortRoyalShow')
        taskMgr.remove('beginTortugaShow')
        taskMgr.remove('beginPadresShow')
        if self.PortRoyalShow:
            self.PortRoyalShow.cleanupShow()
            self.PortRoyalShow = None
        if self.TortugaShow:
            self.TortugaShow.cleanupShow()
            self.TortugaShow = None
        if self.PadresShow:
            self.PadresShow.cleanupShow()
            self.PadresShow = None
        return