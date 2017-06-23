from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBaseGlobal import *
from direct.task.Task import Task
from pandac.PandaModules import *
from pandac.PandaModules import NodePath
from pirates.map.MinimapObject import GridMinimapObject
from pirates.movement import DistributedMovingObject
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
from pirates.ship import ShipGlobals

class DistributedFormation(DistributedMovingObject.DistributedMovingObject):
    notify = directNotify.newCategory('Formation')

    def __init__(self, cr):
        base.formation = self
        self.notify.warning('creating formation')
        DistributedMovingObject.DistributedMovingObject.__init__(self, cr)
        NodePath.__init__(self, 'formation-node')
        self.name = 'formation'
        self.iconModelPath = None
        self.iconCardName = None
        self.icon = None
        self.iconScale = 1.0
        self.nametagIcon = None
        self.minimapIcon = None
        self.worldMapIcon = None
        self.iconParentDoId = None
        self.formationIconIndex = None
        self.reparentTo(render)
        return

    def announceGenerate(self):
        DistributedMovingObject.DistributedMovingObject.announceGenerate(self)
        self.setupSmoothing()
        if self.formationIconIndex == ShipGlobals.FORMATION_ICON_SKULL:
            self.iconScale = 5.0
            self.miniMapiconScale = 7.0
            self.mapIconInfo = ('pir_t_gui_gen_goldSkull', 'models/gui/toplevel_gui', 14.0 / 80)
            self.setIconPath('models/gui/toplevel_gui', '**/pir_t_gui_gen_goldSkull*')
        else:
            self.iconScale = 1.0
            self.miniMapiconScale = 1.0
            self.mapIconInfo = ('topgui_icon_ship_chest03', 'models/textureCards/icons', 2.0 / 80)
            self.setIconPath('models/textureCards/icons', '**/topgui_icon_ship_chest03*')

    def disable(self):
        DistributedMovingObject.DistributedMovingObject.disable(self)
        base.formation = None
        taskMgr.remove(self.updateIconParentTaskName())
        self.stopSmooth()
        self.destroyIcon()
        return

    def setupSmoothing(self):
        self.activateSmoothing(1, 0)
        self.smoother.setDelay(OTPGlobals.NetworkLatency * 1.5)
        broadcastPeriod = 2.0
        self.smoother.setMaxPositionAge(broadcastPeriod * 1.25 * 10)
        self.smoother.setExpectedBroadcastPeriod(broadcastPeriod)
        self.smoother.setDefaultToStandingStill(False)
        self.startSmooth()

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getFormationIconIndex(self):
        return self.formationIconIndex

    def setFormationIconIndex(self, iconIndex):
        self.formationIconIndex = iconIndex

    def setIconParentDoId(self, parentDoId):
        self.iconParentDoId = parentDoId
        taskMgr.remove(self.updateIconParentTaskName())
        if self.updateIconParent() == Task.again:
            taskMgr.doMethodLater(1, self.updateIconParent, self.updateIconParentTaskName())

    def getIconParent(self):
        iconParent = base.cr.getDo(self.iconParentDoId)
        if not iconParent:
            iconParent = self
        return iconParent

    def updateIconParentTaskName(self):
        return 'formationUpdateIconParent-%s' % self.doId

    def updateIconParent(self, task=None):
        iconParent = base.cr.getDo(self.iconParentDoId)
        if not iconParent:
            return Task.again
        if self.nametagIcon:
            self.nametagIcon.reparentTo(iconParent)
        return Task.done

    def setIconPath(self, modelPath, cardName):
        self.destroyIcon()
        self.iconModelPath = modelPath
        self.iconCardName = cardName
        self.createIcon()

    def createIcon(self):
        if not self.iconModelPath or not self.iconCardName:
            return
        iconModel = loader.loadModel(self.iconModelPath)
        if not iconModel:
            return
        icon = iconModel.find(self.iconCardName)
        if not icon:
            return
        icon.setPos(0, 0, 0)
        icon.setScale(self.iconScale)
        icon.flattenLight()
        self.icon = icon
        if self.icon:
            self.createNametagIcon()
            self.createMinimapIcon()
            self.createMapPageIcon()

    def destroyIcon(self):
        if not self.icon:
            return
        self.destroyNametagIcon()
        self.destroyMinimapIcon()
        self.destroyMapPageIcon()
        self.icon.removeNode()
        self.icon = None
        return

    def createNametagIcon(self):
        if self.nametagIcon or not self.icon:
            return
        self.nametagIcon = self.getIconParent().attachNewNode('formation-nametagIcon')
        self.icon.instanceTo(self.nametagIcon)
        self.nametagIcon.setTag('cam', 'formation-nametag')
        self.nametagIcon.setFogOff()
        self.nametagIcon.setLightOff()
        self.nametagIcon.setPos(0, 0, 650)
        self.nametagIcon.setBillboardPointEye()
        self.nametagIcon.setScale(150.0)
        OTPRender.renderReflection(False, self.nametagIcon, 'p_ship_nametag', None)
        if base.hideShipNametags:
            self.hideNametagIcon()
        self.accept('hide-ship-nametags', self.hideNametagIcon)
        self.accept('show-ship-nametags', self.showNametagIcon)
        return

    def destroyNametagIcon(self):
        if not self.nametagIcon:
            return
        self.nametagIcon.removeNode()
        self.nametagIcon = None
        self.ignore('hide-ship-nametags')
        self.ignore('show-ship-nametags')
        return

    def showNametagIcon(self):
        self.notify.info('show formation nametag')
        if self.nametagIcon:
            self.nametagIcon.unstash()

    def hideNametagIcon(self):
        self.notify.info('hiding formation nametag')
        if self.nametagIcon:
            self.nametagIcon.stash()

    def createMinimapIcon(self):
        if self.minimapIcon:
            return
        if not self.iconModelPath or not self.iconCardName:
            return
        icon = MinimapFormation(self, self, self.iconModelPath, self.iconCardName)
        self.minimapIcon = icon
        self.accept('transferMinimapObjects', self.transferMinimapObject)
        minimap = localAvatar.guiMgr.getMinimap()
        if minimap:
            minimap.addObject(self.minimapIcon)

    def transferMinimapObject(self, guiMgr):
        guiMgr.transferMinimapObject(self.getMinimapObject())

    def destroyMinimapIcon(self):
        self.ignore('transferMinimapObjects')
        if not self.minimapIcon:
            return
        self.minimapIcon.removeFromMap()
        self.minimapIcon = None
        return

    def getMinimapObject(self):
        if self.isDisabled():
            return None
        if not self.minimapIcon:
            self.createMinimapIcon()
        return self.minimapIcon

    def createMapPageIcon(self):
        localAvatar.guiMgr.mapPage.addFleet(self)

    def destroyMapPageIcon(self):
        localAvatar.guiMgr.mapPage.removeFleet(self)


class MinimapFormation(GridMinimapObject):
    ICON = None
    ICON_TRACKED = None
    DEFAULT_COLOR = VBase4(1.0, 1.0, 1.0, 1)

    def __init__(self, formation, iconParent, modelPath, cardName):
        if not MinimapFormation.ICON:
            card = loader.loadModel(modelPath)
            MinimapFormation.ICON = card.find(cardName)
            MinimapFormation.ICON.clearTransform()
            MinimapFormation.ICON.setHpr(0, -90, 0)
            MinimapFormation.ICON.setScale(250 * formation.miniMapiconScale)
            MinimapFormation.ICON.flattenStrong()
            gui = loader.loadModel('models/gui/gui_main')
            MinimapFormation.ICON_TRACKED = gui.find('**/icon_objective_grey')
            MinimapFormation.ICON_TRACKED.setScale(1.25 * formation.miniMapiconScale)
            MinimapFormation.ICON_TRACKED.setColorScale(Vec4(1, 1, 0, 1), 1)
            MinimapFormation.ICON_TRACKED.flattenStrong()
        GridMinimapObject.__init__(self, formation.getName(), iconParent, MinimapFormation.ICON)
        self.trackedNode = NodePath(formation.getName())
        self.trackedIcon = MinimapFormation.ICON_TRACKED.copyTo(self.trackedNode)
        self.trackedIcon.reparentTo(self.mapGeom, sort=-1)
        self.trackedIcon.hide()
        self.isTracked = False
        self.siegeTeam = 0
        self.refreshIconColor()

    def setIsTracked(self, isTracked):
        self.isTracked = isTracked
        if self.isTracked:
            self.trackedIcon.show()
        else:
            self.trackedIcon.hide()

    def refreshIconColor(self):
        self.setIconColor()

    def setIconColor(self, color=None):
        self.mapGeom.setColorScale(color or self.DEFAULT_COLOR, 1)

    def _zoomChanged(self, radius):
        self.mapGeom.setScale(radius / 1000.0)