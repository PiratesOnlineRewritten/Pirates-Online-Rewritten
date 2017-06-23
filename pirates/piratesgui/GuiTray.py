from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import PiratesGuiGlobals

class GuiTray(DirectFrame):

    def __init__(self, parent, w=0.5, h=0.1, draggable=0, **kw):
        self.width = w
        self.height = h
        self.__fader = None
        if draggable:
            optiondefs = (
             (
              'relief', DGG.RIDGE, None), ('state', DGG.NORMAL, None), ('frameColor', PiratesGuiGlobals.FrameColor, None), ('borderWidth', PiratesGuiGlobals.BorderWidth, None), ('frameSize', (0, self.width, 0, self.height), None))
        else:
            optiondefs = (
             ('relief', None, None), ('state', DGG.DISABLED, None), ('frameColor', PiratesGuiGlobals.FrameColor, None), ('borderWidth', PiratesGuiGlobals.BorderWidth, None), ('frameSize', (0, self.width, 0, self.height), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(GuiTray)
        self.draggable = draggable
        if self.draggable:
            self.dragBar = DirectButton(parent=self, relief=DGG.FLAT, frameColor=PiratesGuiGlobals.ButtonColor1, frameSize=(0, 0.02, 0, self.height - 0.01 * 2), pos=(0.01,
                                                                                                                                                                      0,
                                                                                                                                                                      0.01))
            self.dragBar.bind(DGG.B1PRESS, self.dragStart)
            self.dragBar.bind(DGG.B1RELEASE, self.dragStop)
            self.dragBar.bind(DGG.B2PRESS, self.dragStart)
            self.dragBar.bind(DGG.B2RELEASE, self.dragStop)
            self.dragBar.bind(DGG.B3PRESS, self.dragStart)
            self.dragBar.bind(DGG.B3RELEASE, self.dragStop)
        return

    def destroy(self):
        if self.__fader:
            self.__fader.pause()
            self.__fader = None
        DirectFrame.destroy(self)
        return

    def dragStart(self, event):
        self.bringToFront()
        if self.draggable:
            taskMgr.remove(self.taskName('dragTask'))
            vWidget2render2d = self.getPos(render2d)
            vMouse2render2d = Point3(event.getMouse()[0], 0, event.getMouse()[1])
            editVec = Vec3(vWidget2render2d - vMouse2render2d)
            task = taskMgr.add(self.dragTask, self.taskName('dragTask'))
            task.editVec = editVec

    def dragTask(self, task):
        mwn = base.mouseWatcherNode
        if mwn.hasMouse():
            vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
            newPos = vMouse2render2d + task.editVec
            self.setPos(render2d, newPos)
            newPos = self.getPos(aspect2d)
            x = newPos[0]
            y = newPos[1]
            z = newPos[2]
            x = x - x % 0.05
            y = 0.0
            z = z - z % 0.05
            x = min(base.a2dRight - self.width, max(base.a2dLeft, x))
            z = min(base.a2dTop - self.height, max(base.a2dBottom, z))
            self.setPos(aspect2d, x, y, z)
        return Task.cont

    def dragStop(self, event):
        if self.draggable:
            taskMgr.remove(self.taskName('dragTask'))

    def bringToFront(self):
        self.reparentTo(self.getParent())

    def show(self):
        if self.__fader:
            self.__fader.pause()
        self.setAlphaScale(1.0)
        DirectFrame.show(self)

    def hide(self):
        if self.__fader:
            self.__fader.pause()
        self.setAlphaScale(1.0)
        DirectFrame.hide(self)

    def fadeOut(self, delay=0.0, duration=0.5):
        if self.__fader:
            self.__fader.pause()
        self.__fader = Sequence(Wait(delay), LerpFunctionInterval(self.setAlphaScale, fromData=self.getColorScale()[3], toData=0.0, duration=duration), Func(self.hide))
        self.__fader.start()