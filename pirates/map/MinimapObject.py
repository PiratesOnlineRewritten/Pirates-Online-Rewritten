from pandac.PandaModules import NodePath, Point3
from direct.showbase.DirectObject import DirectObject
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui.HpMeter import HpMeter
from direct.gui.DirectGui import DGG, OnscreenImage
from direct.interval.IntervalGlobal import *
from pirates.invasion import InvasionGlobals
from pirates.piratesgui import PiratesGuiGlobals

class MinimapObject(DirectObject):
    SORT = 0

    def __init__(self, name, worldNode, mapGeom):
        DirectObject.__init__(self)
        self.map = None
        self.worldNode = worldNode
        self.mapNode = NodePath(name)
        self.mapGeom = mapGeom.copyTo(self.mapNode)
        self.overlayNode = NodePath(name)
        return

    def getMapNode(self):
        return self.mapNode

    def getWorldNode(self):
        return self.worldNode

    def getOverlayNode(self):
        return self.overlayNode

    def addedToMap(self, map):
        self.map = map
        self.mapNode.setTransform(self.worldNode.getTransform(map.getWorldNode()))
        self._addedToMap(map)

    def _addedToMap(self, map):
        pass

    def updateOnMap(self, map):
        self._updateOnMap(map)

    def _updateOnMap(self, map):
        pass

    def removedFromMap(self, map):
        self.map = None
        self._removedFromMap(map)
        return

    def _removedFromMap(self, map):
        pass

    def removeFromMap(self):
        if self.map:
            self.map.removeObject(self)

    def doUpdateOnZoom(self, currentRadius):
        self._zoomChanged(currentRadius)
        self.accept('radar-zoom', self.zoomChanged)

    def stopUpdateOnZoom(self):
        self.ignore('radar-zoom')

    def zoomChanged(self, radius):
        self._zoomChanged(radius)

    def _zoomChanged(self, radius):
        pass


class DynamicMinimapObject(MinimapObject):

    def _updateOnMap(self, map):
        if self.worldNode:
            self.mapNode.setTransform(self.worldNode.getTransform(map.getWorldNode()))


class GridMinimapObject(DynamicMinimapObject):

    def __init__(self, name, worldNode, mapGeom):
        DynamicMinimapObject.__init__(self, name, worldNode, mapGeom)
        self.worldGridNode = None
        self.mapGridChild = self.mapNode.attachNewNode('gridNode')
        self.mapGeom.reparentTo(self.mapGridChild)
        self.overlayGridChild = self.overlayNode.attachNewNode('gridNode')
        return

    def _updateOnMap(self, map):
        if not self.worldGridNode or self.worldGridNode != self.worldNode.getParent():
            self.worldGridNode = self.worldNode.getParent()
            transform = self.worldGridNode.getTransform(map.getWorldNode())
            self.mapNode.setTransform(transform)
            self.overlayNode.setTransform(transform)
        transform = self.worldNode.getTransform()
        self.mapGridChild.setTransform(transform)
        self.overlayGridChild.setTransform(transform)


class MinimapFootprint(MinimapObject):

    def __init__(self, area):
        footprintNode = area.getFootprintNode()
        MinimapObject.__init__(self, 'footprint', area, footprintNode)


class MinimapShop(MinimapObject):
    SORT = 2
    SIGN_DICT = {'blacksmith': '**/shopCoin_blacksmith','shipwright': '**/shopCoin_shipwright','gunsmith': '**/shopCoin_gunsmith','weapons': '**/shopCoin_gunsmith','tailor': '**/shopCoin_tailor','barber': '**/shopCoin_barber','jeweler': '**/shopCoin_jeweler','tattoo': '**/shopCoin_tattoo','voodoo': '**/shopCoin_voodoo','gypsy': '**/shopCoin_voodoo','tavern': '**/shopCoin_tavern','fishmaster': '**/shopCoin_fishing','cannonmaster': '**/shopCoin_cannon','stowaway': '**/shopCoin_stowaway','catalogrep': '**/shopCoin_catalog'}
    SIGNS = {}
    HELP_DICT = {'blacksmith': PLocalizer.ShopBlacksmith,'shipwright': PLocalizer.ShopShipwright,'gunsmith': PLocalizer.ShopGunsmith,'weapons': PLocalizer.ShopGunsmith,'tailor': PLocalizer.ShopTailor,'barber': PLocalizer.ShopBarber,'jeweler': PLocalizer.ShopJewelry,'tattoo': PLocalizer.ShopTattoo,'voodoo': PLocalizer.ShopGypsy,'gypsy': PLocalizer.ShopGypsy,'tavern': PLocalizer.ShopTavern,'fishmaster': PLocalizer.ShopFishmaster,'cannonmaster': PLocalizer.ShopCannoneer,'stowaway': PLocalizer.ShopStowaway,'catalogrep': PLocalizer.ShopCatalogRep}

    @classmethod
    def loadSigns(cls):
        if not MinimapShop.SIGNS:
            coins = loader.loadModel('models/textureCards/shopCoins')
            for coin in coins.findAllMatches('**/shopCoin_*'):
                coin.setP(-90)
                coin.flattenStrong()

            for pattern, signName in MinimapShop.SIGN_DICT.iteritems():
                MinimapShop.SIGNS[pattern] = coins.find(signName)

    @classmethod
    def getShopType(cls, shopString):
        for pattern in MinimapShop.SIGN_DICT:
            if pattern in shopString:
                return pattern

        return None

    def __init__(self, uid, worldNode, shopType):
        self.loadSigns()
        worldNode.setHpr(0, 0, 0)
        MinimapObject.__init__(self, uid, worldNode, MinimapShop.SIGNS[shopType])
        self.shopType = shopType
        self.button = None
        return

    def _addedToMap(self, map):
        self.mapGeom.setScale(aspect2d, 0.06)
        overlayNode = map.getOverlayNode()
        transform = self.mapGeom.getTransform(overlayNode)
        self.button = GuiButton(parent=overlayNode, state=DGG.NORMAL, image=self.mapGeom, pos=transform.getPos(), image_hpr=transform.getHpr(), image_scale=transform.getScale(), helpText=MinimapShop.HELP_DICT[self.shopType], helpPos=(-0.27, 0, 0.07), helpDelay=0, helpOpaque=True, sortOrder=MinimapShop.SORT)
        self.button.setAlphaScale(1, 1)
        self.mapGeom.detachNode()

    def _removedFromMap(self, map):
        if self.button:
            self.button.destroy()
            self.button = None
        return

    def _updateOnMap(self, map):
        MinimapObject._updateOnMap(self, map)
        if self.button:
            if base.localAvatar.guiMgr.invasionScoreboard or base.localAvatar.isInInvasion():
                self.button.hide()
            else:
                self.button.show()


class MinimapCapturePoint(MinimapObject):
    SORT = 4

    def __init__(self, worldNode, holiday, zone):
        MinimapObject.__init__(self, 'capturePoint-%d' % zone, worldNode, NodePath('capturePoint'))
        self.holidayId = holiday
        self.zone = zone
        self.hpMeter = None
        self.barricadeIcon = None
        self.barricadeDestroyed = None
        self.blinker = None
        self.sentRemove = False
        self.hp = 0
        self.maxHp = 0
        whiteColor = (1.0, 1.0, 1.0, 1.0)
        self.blinker = Sequence(Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor))
        return

    def setHp(self, hp, maxHp):
        if self.hpMeter:
            hpMismatch = hp != self.hpMeter.meter['value'] and hp != maxHp
            self.hp = hp
            self.maxHp = hp
            self.hpMeter.update(hp, maxHp)
            if hpMismatch:
                if self.blinker:
                    self.blinker.finish()
                    self.blinker.start()
            if hp <= 0 and maxHp >= 0 and not self.sentRemove:
                self.sentRemove = True
                if self.hpMeter:
                    self.hpMeter.destroy()
                self.hpMeter = None
                if self.blinker:
                    self.blinker.pause()
                    self.blinker = None
                if self.barricadeIcon:
                    self.barricadeIcon.destroy()
                    self.barricadeIcon = None
                if self.barricadeDestroyed and self.zone != InvasionGlobals.getTotalCapturePoints(self.holidayId):
                    self.barricadeDestroyed.show()
                return True
            else:
                return False
        return

    def setBarColor(self, color=None):
        if self.barricadeIcon:
            if color:
                barricadeColor = color
            else:
                barricadeColor = (1.0, 0.5, 0.0, 1)
            self.barricadeIcon.setColor(barricadeColor)
        if self.hpMeter:
            if not color:
                if self.maxHp <= 0:
                    hpFraction = 0
                else:
                    hpFraction = float(self.hp) / float(self.maxHp)
                if hpFraction >= 0.5:
                    color = (0.1, 0.7, 0.1, 1)
                elif hpFraction >= 0.25:
                    color = (1.0, 1.0, 0.1, 1)
                else:
                    color = (1.0, 0.0, 0.0, 1)
            self.hpMeter.meter['barColor'] = color
            if color == PiratesGuiGlobals.TextFG2:
                self.hpMeter.categoryLabel['text_fg'] = color
            else:
                self.hpMeter.categoryLabel['text_fg'] = PiratesGuiGlobals.TextFG1

    def _addedToMap(self, map):
        self.mapGeom.setScale(aspect2d, 0.3)
        overlayNode = map.getOverlayNode()
        worldNode = map.getWorldNode()
        transform = self.mapGeom.getTransform(overlayNode)
        self.hpMeter = HpMeter(width=0.4, parent=overlayNode)
        self.hpMeter.setP(-90)
        if self.zone != InvasionGlobals.getTotalCapturePoints(self.holidayId):
            self.hpMeter.setPos(transform.getPos() + (50, 0, 0))
        else:
            self.hpMeter.setPos(InvasionGlobals.getMainCapturePointHpPos(self.holidayId))
        self.hpMeter.setScale(transform.getScale())
        self.hpMeter['sortOrder'] = MinimapCapturePoint.SORT
        self.hpMeter.setAlphaScale(1, 1)
        self.hpMeter.categoryLabel['text_scale'] = 0.1
        self.hpMeter.update(1, 1)
        topGui = loader.loadModel('models/gui/toplevel_gui')
        if self.zone != InvasionGlobals.getTotalCapturePoints(self.holidayId):
            self.barricadeIcon = OnscreenImage(parent=self.mapGeom, image=topGui.find('**/pir_t_gui_gen_barricade'), scale=1.5, hpr=(0,
                                                                                                                                     90,
                                                                                                                                     0), color=(1.0,
                                                                                                                                                0.5,
                                                                                                                                                0.0,
                                                                                                                                                1))
        self.barricadeDestroyed = OnscreenImage(parent=overlayNode, image=topGui.find('**/pir_t_gui_gen_Xred'), scale=transform.getScale() * 4.0, pos=transform.getPos(), hpr=(0,
                                                                                                                                                                               -90,
                                                                                                                                                                               0))
        self.barricadeDestroyed.hide()
        topGui.removeNode()
        self.mouseOver = GuiButton(parent=self.hpMeter, relief=None, state=DGG.NORMAL, scale=3.0, image=None, frameSize=(-0.1, 0.15, -0.03, 0.03), helpText=PLocalizer.CapturePointNames[self.holidayId][self.zone], helpPos=(0.1, 0, -0.08), helpDelay=0, helpOpaque=True, sortOrder=MinimapShop.SORT)
        return

    def _removedFromMap(self, map):
        if self.blinker:
            self.blinker.pause()
        self.blinker = None
        if self.hpMeter:
            self.hpMeter.destroy()
        self.hpMeter = None
        if self.barricadeIcon:
            self.barricadeIcon.destroy()
        self.barricadeIcon = None
        if self.barricadeDestroyed:
            self.barricadeDestroyed.destroy()
        self.barricadeDestroyed = None
        return

    def getZone(self):
        return self.zone