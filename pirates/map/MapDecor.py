from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectButton
from direct.showbase.PythonUtil import Enum
from direct.showutil.Rope import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PLocalizer
from direct.gui.DirectGui import *
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.ship.ShipMeter import ShipMeter

class Item(NodePath):

    def __init__(self, name, *args, **kwargs):
        NodePath.__init__(self, name, *args, **kwargs)

    def setPosition(self, worldNorth, *args, **kwargs):
        self.setPos(*args, **kwargs)

    def setRotation(self, worldNorth, rotation):
        self.setH(rotation)

    def destroy(self):
        pass


class Billboard(Item):

    def __init__(self, name, nodePath=NodePath(), *args, **kwargs):
        Item.__init__(self, name, *args, **kwargs)
        self._initBillboard(nodePath)
        self.setBin('fixed', 100)
        self.setDepthTest(0)

    def _initBillboard(self, nodePath):
        self.setEffect(BillboardEffect.make(Vec3(0, 0, 1), True, False, 0, nodePath, Point3(0)))
        self.node().setBounds(BoundingSphere(Point3(0), 0.15))

    def updateZoom(self, zoom):
        self.setScale(1 - zoom / 1.5)


class Spline(Item):

    def __init__(self, name, verts, *args, **kwargs):
        Item.__init__(self, name, *args, **kwargs)
        self.name = name
        self.verts = verts
        self._initRope()

    def _initRope(self):
        rope = Rope(self.name)
        rope.ropeNode.setRenderMode(RopeNode.RMTape)
        rope.ropeNode.setUvMode(RopeNode.UVDistance)
        rope.ropeNode.setUvDirection(1)
        rope.ropeNode.setUvScale(-60)
        rope.ropeNode.setThickness(0.005)
        rope.ropeNode.setUseVertexColor(1)
        topGui = loader.loadModel('models/gui/toplevel_gui')
        self.ropeTex = topGui.findTexture('pir_t_gui_linePencil')
        rope.setTexture(self.ropeTex)
        self.rope = rope
        self.rope.setup(4, self.verts)
        self.rope.reparentTo(self)


class Model(Item):

    def __init__(self, name, modelName, scale=1.0, modelPath=None, *args, **kwargs):
        Item.__init__(self, name, *args, **kwargs)
        self._initModel(modelName, scale, modelPath)

    def _initModel(self, modelName, scale, modelPath):
        if modelPath:
            geom = loader.loadModel(modelPath).find('**/%s' % modelName)
        else:
            geom = loader.loadModel(modelName, okMissing=True)
        if geom:
            self.geom = geom.instanceTo(self)
        elif __dev__ and base.config.GetBool('map-islands-debug', 1):
            geom = loader.loadModel('models/misc/smiley')
            self.geom = geom.instanceTo(self)
            scale = 0.05
            self.geom.setColorScale(Vec4(1, 0, 1, 1))
        else:
            self.geom = NodePath('dummy')
        self.geom.setScale(scale)

    def setPosition(self, worldNorth, *args, **kwargs):
        Item.setPosition(self, worldNorth, *args, **kwargs)
        self.headsUp(worldNorth, Vec3(self.getPos()))

    def setRotation(self, worldNorth, rotation):
        Item.setRotation(self, worldNorth, rotation)
        self.headsUp(worldNorth, Vec3(self.getPos()))
        self.geom.setH(rotation)


class PickableModel(Model):

    def __init__(self, name, modelName, scale=1.0, collisionIndex=17, modelPath=None, *args, **kwargs):
        Model.__init__(self, name, modelName, scale, modelPath, *args, **kwargs)
        bm = BitMask32.bit(collisionIndex)
        cGeom = self.geom.find('**/+CollisionNode;+s')
        if cGeom and not cGeom.isEmpty():
            cGeom.node().setIntoCollideMask(bm)
        self.setTag('name', name)


class BillboardModel(Billboard, PickableModel):

    def __init__(self, name, modelName, nodePath=NodePath(), offset=0.0, scale=1.0, collisionIndex=17, *args, **kwargs):
        Billboard.__init__(self, name, nodePath)
        PickableModel.__init__(self, modelName, scale, collisionIndex)
        self.geom.setY(-(offset + 0.0075))


class BillboardCard(Billboard, PickableModel):

    def __init__(self, name, cardName, modelPath, nodePath=NodePath(), offset=0.0, scale=1.0, collisionIndex=17, *args, **kwargs):
        Billboard.__init__(self, name, nodePath)
        PickableModel.__init__(self, name, cardName, scale, collisionIndex, modelPath)
        self.geom.setP(-90)


class Ship(Item):

    def __init__(self, shipInfo, *args, **kwargs):
        name = shipInfo[1]
        Item.__init__(self, name, *args, **kwargs)
        self.setTag('shipName', name)
        self.shipModel = ShipMeter(shipInfo[0], shipInfo[2], shipInfo[3])
        self.shipModel.reparentTo(self)
        self.shipModel.setScale(0.13)
        self.shipModel.setTwoSided(1)
        formattedName = '\x01smallCaps\x01\x01slant\x01' + name.replace(' ', '\n') + '\x02\x02'
        self.text = Text(name + '-text', NodePath(), 0.0, formattedName, 0, scale=0.017)
        self.text.reparentTo(self)
        if self.shipModel.getBounds().isEmpty():
            r = 10
        else:
            r = self.shipModel.getBounds().getRadius()
        self.text.setPos(0, -r * 0.75, 0.001)
        self.setBin('fixed', 300)
        self.text.setBin('fixed', 301)
        self.shipNode = NodePath('Ship')
        self.shipNode.reparentTo(self)
        self.shipNode.setBillboardPointEye()
        self.shipNode.setPos(0, -0.005, 0)
        self.shipNode.setHpr(0, 30, 0)
        self.shipModel.reparentTo(self.shipNode)

    def setRotation(self, worldNorth, rotation):
        self.shipModel.setH(rotation)

    def updateZoom(self, zoom):
        self.text.setScale(1 - zoom / 1.5)

    def destroy(self):
        if self.shipModel:
            self.shipModel.destroy()
            self.shipModel = None
        return


class Island(PickableModel):

    def __init__(self, name, islandUid, modelName, isTeleportIsland, scale=1.0, collisionIndex=17, stencilId=0, *args, **kwargs):
        PickableModel.__init__(self, name, modelName, (scale / 160.0), collisionIndex, *args, **kwargs)
        self.setTag('islandUid', islandUid)
        if isTeleportIsland or base.config.GetBool('teleport-all'):
            self.setTag('isTeleportIsland', 'True')
        self._isCurrentIsland = False
        self._isReturnIsland = False
        self._isPortOfCall = False
        self._hasTeleportToken = False
        self.setAsCurrentIsland(localAvatar.getCurrentIsland() == islandUid)
        self.setAsReturnIsland(localAvatar.getReturnLocation() == islandUid)
        self.setHasTeleportToken(localAvatar.hasIslandTeleportToken(islandUid))
        self.geom.setBin('background', 1)
        self.geom.setDepthWrite(0)

    def setAsCurrentIsland(self, isCurrent):
        self._isCurrentIsland = isCurrent
        self.updateCanTeleportTo()

    def isCurrentIsland(self):
        return self._isCurrentIsland

    def setAsReturnIsland(self, isReturn):
        pass

    def isReturnIsland(self):
        return self._isReturnIsland

    def setAsPortOfCall(self, isPortOfCall):
        self._isPortOfCall = isPortOfCall
        self.updateCanTeleportTo()

    def isPortOfCall(self):
        return self._isPortOfCall

    def setHasTeleportToken(self, hasToken):
        self._hasTeleportToken = hasToken
        self.updateCanTeleportTo()

    def getHasTeleportToken(self, hasToken):
        return self._hasTeleportToken

    def updateCanTeleportTo(self):
        self.setTag('canTeleportTo', str(bool((self._hasTeleportToken or self._isCurrentIsland or self._isPortOfCall or base.cr.distributedDistrict.worldCreator.isPvpIslandByUid(self.getTag('islandUid')) or base.config.GetBool('teleport-all', 0)) and not base.cr.distributedDistrict.worldCreator.isMysteriousIslandByUid(self.getTag('islandUid')))))

    def getCanTeleportTo(self):
        return self.getTag('canTeleportTo') == 'True'

    def isTeleportIsland(self):
        return self.getTag('isTeleportIsland') == 'True'

    def mouseOver(self, pos):
        pass

    def mouseLeft(self):
        pass


class Text(Billboard):

    def __init__(self, name, nodePath, offset, text, stencilId, scale=0.025, *args, **kwargs):
        Billboard.__init__(self, name, nodePath, *args, **kwargs)
        self.setBin('fixed', 110)
        self.scale = scale
        self.textNode = OnscreenText(text=text, fg=Vec4(0, 0, 0, 1), scale=scale, shadow=Vec4(0, 0, 0, 0), mayChange=True, font=PiratesGlobals.getPirateFont())
        self.textNode.detachNode()
        sNode = self.attachNewNode('stencil')
        sNode.setY(-offset)
        self.textNode.instanceTo(sNode)
        sNode.setDepthTest(False)

    def setBold(self, bold):
        self.textNode.setShadow(Vec4(0, 0, 0, bold))

    def setTextScale(self, scale):
        self.textNode.setScale(self.scale * scale)


class TextIsland(Island):

    def __init__(self, name, islandUid, modelName, isTeleportIsland, nodePath=NodePath(), offset=0.0, scale=1.0, collisionIndex=17, stencilId=0, *args, **kwargs):
        Island.__init__(self, name, islandUid, modelName, isTeleportIsland, scale, collisionIndex, stencilId, *args, **kwargs)
        pencil = self.geom.find('**/pencil*')
        if not pencil.isEmpty():
            pass
        self.name = name
        self.helpBox = None
        self.helpLabel = None
        self.textScaleNode = self.attachNewNode('textScale')

        def formatName(name, lineWidth):
            tokens = name.split()
            out = ''
            count = 0
            for token in tokens:
                if count + len(token) < lineWidth:
                    count += len(token) + 1
                    out = '%s %s' % (out, token)
                else:
                    count = len(token) + 1
                    out = '%s\n%s' % (out, token)

            out.strip()
            return '\x01smallCaps\x01%s\x02' % (out,)

        formattedName = formatName(self.name, 10)
        self.text = Text(name + '-text', nodePath, offset, formattedName, stencilId)
        self.text.reparentTo(self.textScaleNode)
        self.text.setBin('background', 2)
        if self.getNetTag('islandUid') == '1160614528.73sdnaik':
            mesh = self.geom
            t, T = self.text.getTightBounds()
            i, I = mesh.getTightBounds()
        else:
            mesh = self.geom.find('**/top_mesh')
            t, T = self.text.getTightBounds()
            if not mesh.isEmpty():
                i, I = mesh.getTightBounds()
            else:
                i, I = self.geom.getTightBounds()
            i *= self.geom.getScale()[0]
            I *= self.geom.getScale()[0]
        self.textScaleNode.setPos(0, (i[1] - I[1]) / 2 - T[2], 0.001)
        compassGui = loader.loadModel('models/gui/compass_gui')
        topGui = loader.loadModel('models/gui/toplevel_gui')
        icons = loader.loadModel('models/textureCards/icons')
        self.button = self.text.attachNewNode('button')
        bg = topGui.find('**/treasure_w_b_slot_empty')
        bg.setScale(0.14)
        bg.reparentTo(self.button)
        buttonPos = Point3(t[0] - 0.022, 0, (t[2] + T[2]) / 2.0)
        self.button.flattenStrong()
        self.button.setPos(buttonPos)
        self.button.setColorScaleOff()
        self.button.hide()
        self.teleportIconDisabled = compassGui.find('**/compass_icon_objective_grey')
        self.teleportIconDisabled.setScale(0.14)
        self.teleportIconDisabled.reparentTo(self.button)
        self.teleportIconEnabled = compassGui.find('**/compass_icon_objective_green')
        self.teleportIconEnabled.setScale(0.14)
        self.teleportIconEnabled.reparentTo(self.button)
        self.manIcon = icons.find('**/icon_stickman')
        self.manIcon.setScale(0.035)
        self.manIcon.reparentTo(self.button)
        t, T = self.text.getTightBounds()
        p0 = VBase3(t[0], 0, t[2])
        p1 = VBase3(T[0], 0, t[2])
        p2 = VBase3(T[0], 0, T[2])
        p3 = VBase3(t[0], 0, T[2])
        self.colNode = self.text.attachNewNode(CollisionNode('cNode-' + name))
        self.colNode.node().addSolid(CollisionPolygon(p0, p1, p2, p3))
        self.colNode.node().setFromCollideMask(BitMask32.allOff())
        self.colNode.node().setIntoCollideMask(BitMask32.bit(collisionIndex))
        self.createHelpBox()
        self.updateState()
        return

    def updateZoom(self, zoom):
        self.textScaleNode.setScale(1 - zoom / 1.5)

    def setAsCurrentIsland(self, isCurrent):
        Island.setAsCurrentIsland(self, isCurrent)
        self.updateState()

    def setAsReturnIsland(self, isReturn):
        Island.setAsReturnIsland(self, isReturn)
        self.updateState()

    def setAsPortOfCall(self, isPortOfCall):
        Island.setAsPortOfCall(self, isPortOfCall)
        self.updateState()

    def setHasTeleportToken(self, hasToken):
        Island.setHasTeleportToken(self, hasToken)
        self.updateState()

    def updateState(self, mouseOver=False):
        if not hasattr(self, 'button'):
            return
        self.button.hide()
        self.teleportIconEnabled.hide()
        self.teleportIconDisabled.hide()
        if self.isCurrentIsland():
            self.manIcon.show()
            self.button.show()
        if self.isTeleportIsland():
            self.button.show()
            self.manIcon.hide()
            self.teleportIconDisabled.show()
            self.teleportIconDisabled.clearColorScale()
            self.button.setColorScale(0.5, 0.5, 0.5, 1)
            self.setHelpLabel(PLocalizer.MapNeedsTeleportToken)
        if self.getCanTeleportTo():
            self.button.show()
            self.button.clearColorScale()
            self.teleportIconDisabled.hide()
            self.teleportIconEnabled.show()
            self.text.setBold(1)
            if not self.isCurrentIsland() and self.isReturnIsland():
                self.setHelpLabel(PLocalizer.MapCanTeleportReturn)
            elif not self.isCurrentIsland() and self.isPortOfCall():
                self.setHelpLabel(PLocalizer.MapCanTeleportPortOfCall)
            else:
                self.setHelpLabel(PLocalizer.MapCanTeleport)
            if mouseOver:
                self.geom.setColorScale(0.5, 1, 0.5, 1)
        if self.isCurrentIsland() and not mouseOver:
            self.button.show()
            self.button.clearColorScale()
            self.button.setScale(1)
            self.text.setBold(1)
            self.teleportIconEnabled.hide()
            self.teleportIconDisabled.hide()
            self.manIcon.show()
            if not self.isTeleportIsland():
                self.setHelpLabel(PLocalizer.MapCurrentIsland)
        if self.isCurrentIsland() and mouseOver:
            self.button.show()
            self.button.clearColorScale()
            self.button.setScale(1)
            self.text.setBold(1)
            self.teleportIconEnabled.show()
            self.teleportIconDisabled.hide()
            self.manIcon.hide()
        if not self.isCurrentIsland() and not mouseOver:
            self.setHelpLabel('')
            self.text.setBold(0)
            self.manIcon.hide()

    def mouseOver(self, pos):
        self.updateState(mouseOver=True)
        self.showDetails(pos)

    def mouseLeft(self):
        self.geom.clearColorScale()
        self.hideDetails()
        self.updateState(mouseOver=False)

    def createHelpBox(self):
        if not self.helpBox:
            self.helpLabel = DirectLabel(parent=aspect2d, relief=None, text='', text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=12, text_shadow=(0,
                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                          1), textMayChange=1, sortOrder=91)
            height = -(self.helpLabel.getHeight() + 0.01)
            width = max(0.25, self.helpLabel.getWidth() + 0.04)
            self.helpBox = BorderFrame(parent=aspect2d, state=DGG.DISABLED, frameSize=(-0.04, width, height, 0.05), pos=(0,
                                                                                                                         0,
                                                                                                                         0), sortOrder=90)
            self.helpLabel.reparentTo(self.helpBox)
            self.helpBox.hide()
        return

    def setHelpLabel(self, text):
        self.helpLabel['text'] = text
        self.helpLabel.resetFrameSize()
        height = -(self.helpLabel.getHeight() + 0.01)
        width = max(0.25, self.helpLabel.getWidth() + 0.04)
        self.helpBox['frameSize'] = (-0.04, width, height, 0.05)
        self.helpBox.resetFrameSize()

    def showDetails(self, pos):
        if self.helpLabel['text'] != '':
            self.helpBox.setPos(pos - Point3(self.helpBox['frameSize'][1] * 1.25, 0, 0))
            self.helpBox.setBin('gui-popup', 0)
            self.helpBox.show()

    def hideDetails(self):
        if self.helpBox:
            self.helpBox.hide()


class OceanAreaText(Text):

    def __init__(self, name, areaUid):
        name = PLocalizer.LocationNames[name]
        text = ''
        for l in range(len(name)):
            text = text + name[l] + ' '

        text = '\x01slant\x01\x01smallCaps\x01' + text + '\x02\x02'
        Text.__init__(self, name, NodePath(), 0, text, 0, 0.017)
        self.uid = areaUid
        self.fadeIval = None
        self.hidden = False
        return

    def fadeOut(self):
        self.hidden = True
        self.fadeTo(0, 'easeOut')

    def fadeIn(self):
        self.hidden = False
        self.fadeTo(1, 'easeIn')

    def fadeTo(self, value, blendType):
        if self.fadeIval:
            self.fadeIval.pause()
            self.fadeIval = None
        self.setTransparency(1)
        self.fadeIval = LerpFunc(self.setAlphaScale, duration=0.15 * abs(value - self.getColorScale().getW()), fromData=self.getColorScale().getW(), toData=value, blendType=blendType)
        self.fadeIval.start()
        return

    def updateZoom(self, zoom):
        Text.updateZoom(self, zoom)
        if zoom >= 0.0 and self.hidden:
            self.fadeIn()
        elif zoom < 0.0 and not self.hidden:
            self.fadeOut()


class Swirl(Model):

    def __init__(self, name, scale=1.0, speed=1, *args, **kwargs):
        Model.__init__(self, name, 'models/worldmap/world_map_swirl', (scale / 80.0), *args, **kwargs)
        self.swirl = self.attachNewNode('swirl')
        self.geom.reparentTo(self.swirl)
        self.swirlLoop = self.swirl.hprInterval(duration=10.0 / speed, startHpr=Vec3(0, 0, 0), hpr=Vec3(360, 0, 0))
        self.swirlLoop.loop()


class Dart(PickableModel):

    def __init__(self, name, parent, defaultPos, color=Vec4(1), offset=0.0, *args, **kwargs):
        self.startScale = 0.075
        self.highlightScale = 0.1
        PickableModel.__init__(self, name, modelName='icon_objective_grey', scale=self.startScale, collisionIndex=17, modelPath='models/gui/compass_main', *args, **kwargs)
        self.defaultPos = defaultPos
        self.edgeMode = False
        self.helpBox = None
        self.helpLabel = None
        self.normalModeNode = self.attachNewNode('normal')
        self.normalModeNode.setColorScale(color)
        self.normalModeNode.setY(-(offset + 0.0075))
        self.geom.instanceTo(self.normalModeNode)
        self.colNode = self.normalModeNode.attachNewNode(CollisionNode('cNode'))
        self.colNode.node().addSolid(CollisionSphere(Point3(0, 0, 0), 0.25))
        self.colNode.setScale(1 / 20.0)
        self.colNode.node().setFromCollideMask(BitMask32.allOff())
        self.colNode.node().setIntoCollideMask(BitMask32.bit(17))
        self.setTag('dart', name)
        self.setPos(self.defaultPos)
        self.createHelpBox()
        questId = localAvatar.activeQuestId
        qs = localAvatar.getQuestById(questId)
        if qs:
            title = qs.getStatusText()
            self.setHelpLabel(title)
        return

    def toggleHelpText(self):
        if self.helpBox:
            if not self.helpBox.isHidden():
                self.hideDetails()

    def createHelpBox(self):
        if not self.helpBox:
            self.helpLabel = DirectLabel(parent=aspect2d, relief=None, text='', text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=12, text_shadow=(0,
                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                          1), textMayChange=1, sortOrder=91)
            height = -(self.helpLabel.getHeight() + 0.01)
            width = max(0.25, self.helpLabel.getWidth() + 0.04)
            self.helpBox = BorderFrame(parent=aspect2d, state=DGG.DISABLED, frameSize=(-0.04, width, height, 0.05), pos=(0,
                                                                                                                         0,
                                                                                                                         0), sortOrder=90)
            self.helpLabel.reparentTo(self.helpBox)
            self.helpBox.hide()
        return

    def setHelpLabel(self, text):
        self.helpLabel['text'] = text
        self.helpLabel.resetFrameSize()
        height = -(self.helpLabel.getHeight() + 0.01)
        width = max(0.25, self.helpLabel.getWidth() + 0.04)
        self.helpBox['frameSize'] = (-0.04, width, height, 0.05)
        self.helpBox.resetFrameSize()

    def showDetails(self, pos):
        if self.helpLabel['text'] != '':
            self.helpBox.setPos(pos + Point3(self.helpBox['frameSize'][1] * 0.25, 0, 0))
            self.helpBox.setBin('gui-popup', 0)
            self.helpBox.show()
            self.geom.setScale(self.highlightScale)

    def hideDetails(self):
        if self.helpBox:
            self.helpBox.hide()
            self.geom.setScale(self.startScale)

    def mouseOver(self, pos):
        self.showDetails(pos)

    def mouseLeft(self):
        self.hideDetails()

    def getDefaultPos(self):
        return self.defaultPos

    def setEdgeMode(self, edgeMode):
        self.edgeMode = edgeMode
        if self.edgeMode:
            self.edgeModeNode.unstash()
        else:
            self.edgeModeNode.stash()

    def setColorScale(self, *args, **kwargs):
        self.edgeModeNode.setColorScale(*args, **kwargs)
        self.normalModeNode.setColorScale(*args, **kwargs)

    def setScale(self, *args, **kwargs):
        self.normalModeNode.setScale(*args, **kwargs)

    def setPosition(self, worldPos, *args, **kwargs):
        NodePath.setPos(self, *args, **kwargs)
        if self.edgeMode:
            self.edgeModeNode.setPos(*args, **kwargs)


DecorTypes = Enum('Item,                    Billboard,                    Model,                    BillboardModel,                    BillboardCard,                    Island,                    Text,                    TextIsland,                    Dart,                    Swirl,                    OceanAreaText,                    Ship,                    Spline,                    ')
DecorClasses = {DecorTypes.Item: Item,DecorTypes.Billboard: Billboard,DecorTypes.Model: Model,DecorTypes.BillboardModel: BillboardModel,DecorTypes.BillboardCard: BillboardCard,DecorTypes.Island: Island,DecorTypes.Text: Text,DecorTypes.TextIsland: TextIsland,DecorTypes.Dart: Dart,DecorTypes.Swirl: Swirl,DecorTypes.OceanAreaText: OceanAreaText,DecorTypes.Ship: Ship,DecorTypes.Spline: Spline}