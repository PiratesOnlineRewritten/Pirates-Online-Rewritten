import types
from direct.fsm import FSM
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import NewTutorialPanel
from otp.otpbase import OTPRender
USE_KEY_EVENT = 'shift'
END_INTERACT_EVENT = 'escape'
PROXIMITY = 0
MOUSE_OVER = 1

class InteractiveBase(FSM.FSM):
    DiskUseColor = None
    DiskDefaultColor = (0, 1, 0, 1)
    DiskWaitingColor = (0, 0, 1, 0.5)
    DiskEnemyTargetColor = (1, 0, 0, 1)
    DiskFriendlyTargetColor = (0, 0, 1, 1)

    def __init__(self):
        FSM.FSM.__init__(self, 'Interactive')
        self.useKeyHandler = self.handleUseKey
        self.mouseClickHandler = None
        self.mouseOverHandler = None
        self.__mouseClick = 0
        self.__mouseOver = 0
        self.__isTarget = 0
        self.hasProximityCollision = 0
        self.proximityCollisionId = None
        self.proximityCollisionNodePath = None
        self.disk = None
        self.diskRadius = 5
        self.offset = Vec3(0.0, 0.0, 0.0)
        self.useLabel = None
        self.proximityText = None
        self.tutorialMode = None
        self.tutorialPanel = None
        self.fader = None
        self.__isExclusiveInteraction = 1
        self.__endInteract = 1
        self.ignoreProximity = False
        self.allowInteract = True
        self.proximityCollisionEnterEvent = None
        return

    def delete(self):
        FSM.FSM.cleanup(self)
        del self.useKeyHandler
        del self.mouseClickHandler
        del self.mouseOverHandler
        self.fader = None
        return

    def generate(self):
        if self == base.localAvatar:
            return

    def disable(self):
        self.hideProximityInfo()
        if self.fader:
            self.fader.pause()
            self.fader = None
        if self.useLabel:
            self.useLabel.removeNode()
            self.useLabel = None
        FSM.FSM.cleanup(self)
        if self.__isTarget:
            if hasattr(base.cr, 'targetMgr') and self.proximityCollisionId:
                base.cr.targetMgr.removeTarget(self.proximityCollisionId)
            self.__isTarget = 0
        if hasattr(base, 'localAvatar') and localAvatar.currentTarget is self:
            localAvatar.currentTarget = None
        if self.hasProximityCollision:
            self.destroyProximitySphere()
            self.hasProximityCollision = 0
        if self.disk:
            self.disk.removeNode()
            self.disk = None
        if self.tutorialPanel:
            self.tutorialPanel.destroy()
            self.tutorialPanel = None
        self.ignoreAll()
        return

    def setInteractOptions(self, tutorialMode=None, proximityText=None, mouseClickText=None, mouseOver=0, mouseClick=0, otherCollision=None, otherCollisionName=None, sphereScale=12.0, diskRadius=5.0, parent=None, isTarget=0, exclusive=1, endInteract=1, allowInteract=True, resetState=1, offset=Point3(0, 0, 0)):
        self.tutorialMode = tutorialMode
        self.diskRadius = diskRadius
        self.sphereScale = sphereScale
        self.offset = offset
        if resetState:
            self.request('Off')
        self.proximityText = proximityText
        if mouseClick:
            self.__mouseClick = 1
            self.mouseClickEvent = self.uniqueName('mouseClick')
            self.mouseClickHandler = self.handleMouseClick
            self.mouseClickText = mouseClickText
        if mouseOver:
            self.__mouseOver = 1
            self.mouseOverEvent = self.uniqueName('mouseOver')
            self.mouseOverHandler = self.handleMouseOver
        if otherCollision:
            self.proximityCollisionNodePath = otherCollision
            self.proximityCollisionEnterEvent = 'enter' + otherCollisionName
            self.proximityCollisionExitEvent = 'exit' + otherCollisionName
            self.proximityCollisionId = otherCollision.id()
            self.hasProximityCollision = 1
            if self.ignoreProximity:
                self.proximityCollisionNodePath.stash()
        elif allowInteract or isTarget:
            self.setupProximitySphere(parent)
            if isinstance(sphereScale, types.TupleType):
                self.proximityCollisionNodePath.setScale(*sphereScale)
            else:
                self.proximityCollisionNodePath.setScale(sphereScale)
        if isTarget or mouseClick or mouseOver:
            if hasattr(base.cr, 'targetMgr'):
                self.makeTargetable()
            else:
                self.acceptOnce('targetMgrCreated', self.makeTargetable)
        self.__isExclusiveInteraction = exclusive
        self.__endInteract = endInteract
        self.allowInteract = allowInteract
        if resetState:
            self.request('Idle')

    def makeTargetable(self):
        base.cr.targetMgr.addTarget(self.proximityCollisionId, self)
        self.__isTarget = 1

    def isExclusiveInteraction(self):
        return self.__isExclusiveInteraction

    def setAllowInteract(self, isAllow):
        self.allowInteract = isAllow

    def setupProximitySphere(self, parent):
        if self.hasProximityCollision:
            self.proximityCollisionNodePath.setPos(self.offset)
            self.notify.warning('tried to create duplicate proximity sphere')
            return
        self.proximityCollisionEvent = self.uniqueName('proximityCollision')
        self.proximityCollisionEnterEvent = 'enter' + self.proximityCollisionEvent
        self.proximityCollisionExitEvent = 'exit' + self.proximityCollisionEvent
        proximityCollision = CollisionSphere(0, 0, 0, 1)
        proximityCollision.setTangible(0)
        proximityCollisionNode = CollisionNode(self.proximityCollisionEvent)
        proximityCollisionNode.setIntoCollideMask(PiratesGlobals.WallBitmask | PiratesGlobals.SelectBitmask)
        proximityCollisionNode.addSolid(proximityCollision)
        parentNP = self
        if parent:
            parentNP = parent
        self.proximityCollisionNodePath = parentNP.attachNewNode(proximityCollisionNode)
        self.proximityCollisionNodePath.setPos(self.offset)
        self.proximityCollisionNodePath.hide()
        self.proximityCollisionId = self.proximityCollisionNodePath.id()
        if self.ignoreProximity:
            self.proximityCollisionNodePath.stash()
        self.hasProximityCollision = 1

    def destroyProximitySphere(self):
        if self.hasProximityCollision:
            self.proximityCollision = None
            self.proximityCollisionNodePath.removeNode()
            self.proximityCollisionNodePath = None
            self.hasProximityCollision = 0
        return

    def isInteractiveMasked(self):
        return 0

    def handleEnterProximity(self, collEntry):
        if not self.allowInteract or self.isInteractiveMasked():
            return
        self.request('Proximity')

    def handleExitProximity(self, collEntry):
        self.request('Idle')

    def getPosRelToAv(self):
        if self.proximityCollisionNodePath:
            return self.proximityCollisionNodePath.getPos(base.localAvatar)
        else:
            return self.getPos(base.localAvatar)

    def loadTargetIndicator(self):
        if self.isGenerated():
            self.disk = loader.loadModel('models/effects/selectionCursor')
            self.disk.hide(OTPRender.MainCameraBitmask)
            self.disk.showThrough(OTPRender.EnviroCameraBitmask)
            self.disk.setScale(self.diskRadius)
            self.disk.setColorScale(*self.DiskDefaultColor)
            self.disk.getChild(0).setP(-90)
            self.disk.setPos(self.offset)
            self.disk.setLightOff()
            self.disk.setFogOff()
            self.disk.reparentTo(self)
            self.disk.setBin('shadow', 0)
            self.disk.setTransparency(TransparencyAttrib.MAlpha)
            self.disk.setDepthWrite(0)
            self.disk.setDepthTest(0)

    def loadUseLabel(self):
        self.useLabel = DirectLabel(parent=aspect2d, frameColor=(0.1, 0.1, 0.25, 0.2), text='', text_align=TextNode.ACenter, text_scale=0.06, text_pos=(0.02,
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

    def showProximityInfo(self):
        if self.tutorialMode:
            if self.allowInteract:
                self.__showTutorialPanel()
        elif not base.localAvatar.isAirborne():
            self.showProximityStuff()
            self.accept('jumpStart', self.hideProximityStuff)
            self.accept('jumpLand', self.showProximityStuff)
            self.accept('jumpLandHard', self.showProximityStuff)
        else:
            self.accept('jumpLand', self.showProximityStuff)
            self.accept('jumpLandHard', self.showProximityStuff)

    def hideProximityInfo(self):
        self.hideProximityStuff()
        self.ignore('jumpStart')
        self.ignore('jumpLand')
        self.ignore('jumpLandHard')

    def showProximityStuff(self):
        self.__showProximityText()
        self.__showTarget()
        self.accept(USE_KEY_EVENT, self.useKeyHandler)

    def hideProximityStuff(self):
        if self.tutorialMode:
            self.__hideTutorialPanel()
        else:
            self.__hideProximityText()
        self.__hideTarget()
        self.ignore(USE_KEY_EVENT)

    def showMouseOverInfo(self):
        pass

    def hideMouseOverInfo(self):
        pass

    def showMouseClickInfo(self):
        self.__showMouseOverText()
        self.__showTarget()
        if self.__mouseClick:
            self.accept(self.mouseClickEvent, self.mouseClickHandler)

    def hideMouseClickInfo(self):
        self.__hideMouseOverText()
        self.__hideTarget()
        if self.__mouseClick:
            self.ignore(self.mouseClickEvent)

    def showWaitingInfo(self):
        self.__showTarget()
        if self.disk:
            self.disk.setColorScale(*self.DiskWaitingColor)

    def hideWaitingInfo(self):
        self.__hideTarget()
        if self.disk:
            self.disk.setColorScale(*self.DiskDefaultColor)

    def showUseInfo(self):
        self.__showTarget()
        if self.disk:
            if self.DiskUseColor:
                self.disk.setColorScale(*self.DiskUseColor)
            else:
                self.disk.hide()

    def hideUseInfo(self):
        self.__hideTarget()
        if self.disk:
            self.disk.setColorScale(*self.DiskDefaultColor)

    def showEnemyTargetInfo(self):
        self.__showTarget()
        if self.disk:
            self.disk.setColorScale(*self.DiskEnemyTargetColor)

    def hideEnemyTargetInfo(self):
        self.__hideTarget()
        if self.disk:
            self.disk.setColorScale(*self.DiskDefaultColor)

    def showFriendlyTargetInfo(self):
        self.__showTarget()
        if self.disk:
            self.disk.setColorScale(*self.DiskFriendlyTargetColor)

    def hideFriendlyTargetInfo(self):
        self.__hideTarget()
        if self.disk:
            self.disk.setColorScale(*self.DiskDefaultColor)

    def __showTarget(self):
        if self.isInteractiveMasked():
            return
        if not self.disk:
            self.loadTargetIndicator()
        if self.disk:
            self.disk.show()

    def requestHideTarget(self):
        self.__hideTarget()

    def __hideTarget(self):
        if self.disk:
            self.disk.hide()

    def __loadTutorialPanel(self):
        self.tutorialPanel = NewTutorialPanel.NewTutorialPanel([self.tutorialMode])

    def __showTutorialPanel(self):
        if not self.tutorialPanel or self.tutorialPanel.isEmpty():
            self.__loadTutorialPanel()
        self.tutorialPanel.activate()
        self.__showTarget()
        self.accept(USE_KEY_EVENT, self.useKeyHandler)

    def __hideTutorialPanel(self):
        if self.tutorialPanel and not self.tutorialPanel.isEmpty():
            self.tutorialPanel.hide()
        self.__hideTarget()
        self.ignore(USE_KEY_EVENT)

    def __showProximityText(self):
        if self.proximityText and not self.isInteractiveMasked():
            if not self.useLabel:
                self.loadUseLabel()
            self.useLabel['text'] = self.proximityText
            if self.fader:
                self.fader.pause()
            fadeOut = LerpFunctionInterval(self.useLabel.setAlphaScale, fromData=0, toData=1, duration=0.5)
            self.fader = Sequence(Func(self.useLabel.show), fadeOut)
            self.fader.start()

    def refreshProximityText(self):
        if self.proximityText:
            if self.useLabel:
                self.useLabel['text'] = self.proximityText

    def __hideProximityText(self):
        if self.useLabel:
            if self.fader:
                self.fader.pause()
            toColor = self.getColorScale()
            fadeOut = LerpFunctionInterval(self.useLabel.setAlphaScale, fromData=toColor[3], toData=0, duration=0.5)
            self.fader = Sequence(fadeOut, Func(self.useLabel.hide))
            self.fader.start()

    def __showMouseOverText(self):
        if self.mouseClickText:
            if not self.useLabel:
                self.loadUseLabel()
            self.useLabel['text'] = self.mouseClickText
            if self.fader:
                self.fader.pause()
            fadeOut = LerpFunctionInterval(self.useLabel.setAlphaScale, fromData=self.getColorScale()[3], toData=1, duration=0.5)
            self.fader = Sequence(Func(self.useLabel.show), fadeOut)
            self.fader.start()

    def __hideMouseOverText(self):
        if self.useLabel:
            if self.fader:
                self.fader.pause()
            fadeOut = LerpFunctionInterval(self.useLabel.setAlphaScale, fromData=self.getColorScale()[3], toData=0, duration=0.5)
            self.fader = Sequence(fadeOut, Func(self.useLabel.hide))
            self.fader.start()

    def handleUseKey(self, interactType=0):
        if not self.allowInteract or base.cr.activeWorld == None:
            return
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr and base.localAvatar.guiMgr.mainMenu and not base.localAvatar.guiMgr.mainMenu.isHidden():
            return
        base.cr.activeWorld.handleUseKey(self)
        currentInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if currentInteractive and currentInteractive != self and currentInteractive.isExclusiveInteraction():
            currentInteractive.requestExit()
        self.requestInteraction(base.localAvatar.doId, interactType)
        return

    def handleEndInteractKey(self):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr and base.localAvatar.guiMgr.mainMenu and not base.localAvatar.guiMgr.mainMenu.isHidden():
            base.localAvatar.guiMgr.toggleMainMenu()
        else:
            if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
                base.localAvatar.guiMgr.setIgnoreEscapeHotKey(False)
            self.requestExit()

    def handleMouseClick(self):
        if not self.allowInteract:
            return
        self.handleUseKey()

    def handleMouseOver(self, on):
        if not self.allowInteract:
            return
        if on:
            self.request('MouseOver')
        elif self.state == 'MouseOver':
            self.request('Idle')

    def enterIdle(self):
        if self.__mouseOver:
            self.accept(self.mouseOverEvent, self.mouseOverHandler)
        if self.proximityCollisionEnterEvent:
            self.accept(self.proximityCollisionEnterEvent, self.handleEnterProximity)

    def exitIdle(self):
        if self.__mouseOver:
            self.ignore(self.mouseOverEvent)
        if self.proximityCollisionEnterEvent:
            self.ignore(self.proximityCollisionEnterEvent)

    def enterMouseOver(self):
        if self.__mouseClick:
            self.accept(self.mouseClickEvent, self.mouseClickHandler)
            self.showMouseClickInfo()
        if self.__mouseOver:
            self.showMouseOverInfo()
            self.accept(self.mouseOverEvent, self.mouseOverHandler)
        if self.proximityCollisionEnterEvent:
            self.accept(self.proximityCollisionEnterEvent, self.handleEnterProximity)

    def exitMouseOver(self):
        if self.__mouseClick:
            self.hideMouseClickInfo()
            self.ignore(self.mouseClickEvent)
        if self.__mouseOver:
            self.hideMouseOverInfo()
            self.ignore(self.mouseOverEvent)
        if self.proximityCollisionEnterEvent:
            self.ignore(self.proximityCollisionEnterEvent)

    def enterProximity(self):
        base.cr.interactionMgr.addInteractive(self, PROXIMITY)
        self.accept(self.proximityCollisionExitEvent, self.handleExitProximity)
        if self.__mouseClick:
            self.accept(self.mouseClickEvent, self.mouseClickHandler)
        messenger.send('enterProximityOfInteractive')

    def exitProximity(self):
        base.cr.interactionMgr.removeInteractive(self, PROXIMITY)
        self.ignore(self.proximityCollisionExitEvent)
        self.hideProximityInfo()
        if self.__mouseClick:
            self.ignore(self.mouseClickEvent)
        messenger.send('exitProximityOfInteractive')

    def enterWaiting(self):
        self.showWaitingInfo()
        if self.__endInteract:
            self.accept(END_INTERACT_EVENT, self.handleEndInteractKey)

    def exitWaiting(self):
        self.hideWaitingInfo()
        if self.__endInteract:
            self.ignore(END_INTERACT_EVENT)

    def enterUse(self):
        self.showUseInfo()
        if self.hasProximityCollision:
            self.proximityCollisionNodePath.stash()
        base.cr.interactionMgr.setCurrentInteractive(self)
        base.localAvatar.guiMgr.setIgnoreEscapeHotKey(True)
        if self.__endInteract:
            self.accept(END_INTERACT_EVENT, self.handleEndInteractKey)

    def exitUse(self):
        self.hideUseInfo()
        if self.hasProximityCollision and not self.proximityCollisionNodePath.isEmpty() and not self.ignoreProximity:
            self.proximityCollisionNodePath.unstash()
        base.cr.interactionMgr.setCurrentInteractive(None)
        base.localAvatar.guiMgr.setIgnoreEscapeHotKey(False)
        if self.__endInteract:
            self.ignore(END_INTERACT_EVENT)
        return

    def setIgnoreProximity(self, ignore):
        self.ignoreProximity = ignore
        if self.hasProximityCollision:
            if ignore:
                self.proximityCollisionNodePath.stash()
            else:
                self.proximityCollisionNodePath.unstash()

    def getEndInteract(self):
        return self.__endInteract