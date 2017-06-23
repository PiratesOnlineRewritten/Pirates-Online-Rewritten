from pirates.minigame import CannonDefenseGlobals
from pirates.pirate.CannonCamera import CannonCamera
from direct.showbase.PythonUtil import ParamObj

class CannonDefenseCamera(CannonCamera):

    class ParamSet(CannonCamera.ParamSet):
        Params = {'minH': -60.0,'maxH': 60.0,'minP': -32.0,'maxP': 2.0,'sensitivityH': CannonDefenseGlobals.MOUSE_SENSITIVITY_H,'sensitivityP': CannonDefenseGlobals.MOUSE_SENSITIVITY_P}

    def __init__(self, params=None):
        CannonCamera.__init__(self, params)
        self.keyboardRate = CannonDefenseGlobals.KEYBOARD_RATE

    def enterActive(self):
        CannonCamera.enterActive(self)
        camera.setPos(0, -20, 15)
        camera.setP(-25)

    def changeModel(self, prop):
        if self.cannonProp:
            if prop.ship:
                self.reparentTo(prop.ship.avCannonView)
            else:
                self.reparentTo(prop.hNode)
        self.cannonProp = prop