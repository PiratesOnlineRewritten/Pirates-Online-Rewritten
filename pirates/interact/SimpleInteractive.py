from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import CollisionNode, CollisionSphere, TransparencyAttrib, TextNode
from direct.gui.DirectGui import DirectLabel
from direct.interval.IntervalGlobal import Func
from direct.interval.LerpInterval import LerpFunctionInterval
from direct.interval.MetaInterval import Sequence
from otp.otpbase import OTPRender
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
USE_KEY_EVENT = 'shift'

class SimpleInteractive(DirectObject):

    def __init__(self, object, name, proximityText):
        DirectObject.__init__(self)
        self.object = object
        self.proximityText = proximityText
        self.proximityEvent = name
        self.enterProximityEvent = 'enter' + name
        self.exitProximityEvent = 'exit' + name
        self.useLabel = None
        self.fader = None
        self.size = 6
        self.disk = None
        proximitySphere = CollisionSphere(0, 0, 0, self.size)
        proximitySphere.setTangible(0)
        proximityNode = CollisionNode(self.proximityEvent)
        proximityNode.setIntoCollideMask(PiratesGlobals.WallBitmask)
        proximityNode.addSolid(proximitySphere)
        self.proximityNodePath = self.object.attachNewNode(proximityNode)
        self.accept(self.enterProximityEvent, self.approach)
        self.accept(self.exitProximityEvent, self.leave)
        return

    def createInteractionDisk(self):
        self.disk = loader.loadModel('models/effects/selectionCursor')
        self.disk.setScale(self.size)
        self.disk.setColorScale(0, 1, 0, 1)
        self.disk.setP(-90)
        self.disk.setZ(0.025)
        self.disk.setBillboardAxis(6)
        self.disk.reparentTo(self.object)
        self.disk.setBin('shadow', 0)
        self.disk.setTransparency(TransparencyAttrib.MAlpha)
        self.disk.setDepthWrite(0)
        self.disk.setDepthTest(0)

    def loadUseLabel(self, text):
        self.useLabel = DirectLabel(parent=aspect2d, frameColor=(0.1, 0.1, 0.25, 0.2), text=text, text_align=TextNode.ACenter, text_scale=0.06, text_pos=(0.02,
                                                                                                                                                          0.02), text_fg=(1,
                                                                                                                                                                          1,
                                                                                                                                                                          1,
                                                                                                                                                                          1), text_shadow=(0,
                                                                                                                                                                                           0,
                                                                                                                                                                                           0,
                                                                                                                                                                                           1), textMayChange=1, text_font=PiratesGlobals.getPirateOutlineFont())
        self.useLabel.setPos(0, 0, -0.7)
        self.useLabel.setAlphaScale(0)
        self.useLabel.hide()

    def fadeInText(self):
        if self.fader:
            self.fader.pause()

    def interactionAllowed(self, avId):
        return True

    def approach(self, collEntry):
        if not self.interactionAllowed(localAvatar.doId):
            return
        if not self.disk:
            self.createInteractionDisk()
        if self.proximityText:
            if not self.useLabel:
                self.loadUseLabel(self.proximityText)
            if self.fader:
                self.fader.pause()
            fadeIn = LerpFunctionInterval(self.useLabel.setAlphaScale, fromData=0, toData=1, duration=0.5)
            self.fader = Sequence(Func(self.useLabel.show), fadeIn)
            self.fader.start()
        self.disk.show()
        self.accept(USE_KEY_EVENT, self.handleUseKey)

    def requestInteraction(self, avId):
        pass

    def handleUseKey(self):
        self.requestInteraction(localAvatar.doId)

    def leave(self, collEntry):
        if self.disk:
            self.disk.hide()
        if self.proximityText:
            if self.fader:
                self.fader.pause()
                self.fader = None
            if self.useLabel:
                self.useLabel.hide()
        self.ignore(USE_KEY_EVENT)
        return