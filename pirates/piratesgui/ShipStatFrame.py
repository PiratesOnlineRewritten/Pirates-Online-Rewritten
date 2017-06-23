from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ShipSnapshot import ShipSnapshot

class ShipStatFrame(BorderFrame):

    def __init__(self, parent, shipOV=None, shipName='', shipClass=0, mastInfo=[], hp=0, maxHp=0, sp=0, maxSp=0, cargo=0, maxCargo=0, crew=0, maxCrew=0, adventureTime=0, **kw):
        optiondefs = (
         (
          'state', DGG.DISABLED, None), ('frameSize', (0.05, 0.64, 0.04, 0.39), None))
        self.defineoptions(kw, optiondefs)
        BorderFrame.__init__(self, parent, **kw)
        self.initialiseoptions(ShipStatFrame)
        self.showTask = None
        self.snapShot = ShipSnapshot(self, shipOV, shipName, shipClass, mastInfo, hp, maxHp, sp, maxSp, cargo, maxCargo, crew, maxCrew, adventureTime, pos=(0,
                                                                                                                                                            0,
                                                                                                                                                            0))
        return

    def destroy(self):
        if self.showTask:
            taskMgr.remove(self.showTask)
            self.showTask = None
        self.snapShot = None
        BorderFrame.destroy(self)
        return

    def scheduleShow(self, time=1):
        if self.showTask:
            taskMgr.remove(self.showTask)
            self.showTask = None
        if time:
            self.showTask = taskMgr.doMethodLater(time, self.show, 'ShipStatFrame-show', extraArgs=[])
        else:
            self.show()
        return

    def hide(self, *args):
        BorderFrame.hide(self)
        if self.showTask:
            taskMgr.remove(self.showTask)
            self.showTask = None
        return