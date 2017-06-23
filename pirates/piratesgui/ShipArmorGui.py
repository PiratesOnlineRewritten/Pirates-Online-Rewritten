from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui.GuiTray import GuiTray
from pirates.piratesgui import PiratesGuiGlobals
from pirates.ship import ShipGlobals

class ShipArmorGui(GuiTray):

    def __init__(self, parent, **kw):
        optiondefs = (('relief', None, None), )
        self.defineoptions(kw, optiondefs)
        GuiTray.__init__(self, parent, 0.5, 0.5, **kw)
        damageModel = loader.loadModel('models/gui/ship_damage')
        tex = damageModel.find('**/background*')
        self.damageGUI = DirectFrame(parent=self, pos=(0.0, 0.0, 0.0), relief=None, image=tex, image_scale=0.06, sortOrder=2)
        plane = Plane(Vec4(0, 0, 1, 0))
        pnl = PlaneNode('hpClipLeft')
        pnr = PlaneNode('hpClipRight')
        pnb = PlaneNode('hpClipBottom')
        pnl.setPlane(plane)
        pnr.setPlane(plane)
        pnb.setPlane(plane)
        self.clipLeft = NodePath(pnl)
        self.clipRight = NodePath(pnr)
        self.clipBottom = NodePath(pnb)
        tex = damageModel.find('**/hp_bar_left*')
        self.hpLeft = DirectFrame(parent=self.damageGUI, relief=None, image=tex, image_scale=0.06, image_color=(0.1,
                                                                                                                0.8,
                                                                                                                0.1,
                                                                                                                0.8))
        self.clipLeft.reparentTo(self.damageGUI)
        self.clipLeft.setHpr(0, 0, -49)
        self.hpLeft.setClipPlane(self.clipLeft)
        tex = damageModel.find('**/hp_bar_right*')
        self.hpRight = DirectFrame(parent=self.damageGUI, relief=None, image=tex, image_scale=0.06, image_color=(0.1,
                                                                                                                 0.8,
                                                                                                                 0.1,
                                                                                                                 0.8))
        self.clipRight.reparentTo(self.damageGUI)
        self.clipRight.setHpr(0, 0, 49)
        self.hpRight.setClipPlane(self.clipRight)
        tex = damageModel.find('**/hp_bar_bottom')
        self.hpRear = DirectFrame(parent=self.damageGUI, relief=None, image=tex, image_scale=0.06, image_color=(0.1,
                                                                                                                0.8,
                                                                                                                0.1,
                                                                                                                0.8))
        self.clipBottom.reparentTo(self.damageGUI)
        self.clipBottom.setHpr(0, 0, 109)
        self.hpRear.setClipPlane(self.clipBottom)
        return

    def setArmorStatus(self, location, status):
        if location == ShipGlobals.ARMOR_REAR:
            self.hpRear.setHpr(0, 0, 40 * status)
        elif location == ShipGlobals.ARMOR_LEFT:
            self.hpLeft.setHpr(0, 0, -120 * status)
        elif location == ShipGlobals.ARMOR_RIGHT:
            self.hpRight.setHpr(0, 0, 120 * status)