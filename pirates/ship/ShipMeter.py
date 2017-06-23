import copy
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
from pirates.ship import ShipGlobals
from pirates.ship.DistributedPlayerSimpleShipOV import DistributedPlayerSimpleShipOV
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiTray
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PiratesTimer
from pirates.piratesgui import StatusEffectsPanel
from pirates.pvp import PVPGlobals
from pirates.ship import ShipBlueprints
from pirates.ship import ShipUpgradeGlobals
HullDict = {ShipGlobals.WARSHIPL1: 'models/shipparts/warshipMeter',ShipGlobals.WARSHIPL2: 'models/shipparts/warshipMeter',ShipGlobals.WARSHIPL3: 'models/shipparts/warshipMeter',ShipGlobals.MERCHANTL1: 'models/shipparts/merchantMeter',ShipGlobals.MERCHANTL2: 'models/shipparts/merchantMeter',ShipGlobals.MERCHANTL3: 'models/shipparts/merchantMeter',ShipGlobals.INTERCEPTORL1: 'models/shipparts/interceptorMeter',ShipGlobals.INTERCEPTORL2: 'models/shipparts/interceptorMeter',ShipGlobals.INTERCEPTORL3: 'models/shipparts/interceptorMeter',ShipGlobals.BRIGL1: 'models/shipparts/brigMeter',ShipGlobals.BRIGL2: 'models/shipparts/brigMeter',ShipGlobals.BRIGL3: 'models/shipparts/brigMeter',ShipGlobals.BLACK_PEARL: 'models/shipparts/brigMeter',ShipGlobals.GOLIATH: 'models/shipparts/brigMeter',ShipGlobals.SHIP_OF_THE_LINE: 'models/shipparts/brigMeter',ShipGlobals.QUEEN_ANNES_REVENGE: 'models/shipparts/brigMeter',ShipGlobals.SKEL_WARSHIPL3: 'models/shipparts/warshipMeter',ShipGlobals.SKEL_INTERCEPTORL3: 'models/shipparts/interceptorMeter'}
MastDict = {ShipGlobals.Masts.Main_Square: 'models/shipparts/mainmast_square',ShipGlobals.Masts.Main_Tri: 'models/shipparts/L2mastTri',ShipGlobals.Masts.Fore_Tri: 'models/shipparts/L1foremast',ShipGlobals.Masts.Fore_Multi: 'models/shipparts/L2foremast',ShipGlobals.Masts.Aft_Tri: 'models/shipparts/L2aftmast',ShipGlobals.Masts.Skel_Main_A: 'models/shipparts/mainmast_square',ShipGlobals.Masts.Skel_Main_B: 'models/shipparts/mainmast_square',ShipGlobals.Masts.Skel_Tri: 'models/shipparts/L2mastTri',ShipGlobals.Masts.Skel_Fore: 'models/shipparts/L1foremast',ShipGlobals.Masts.Skel_Aft: 'models/shipparts/L2aftmast'}

class ShipMeter(DirectObject, NodePath):

    def __init__(self, shipId, shipClass=0, mastInfo=[], siegeTeam=0):
        NodePath.__init__(self, 'ShipMeter')
        self.shipId = shipId
        self.team = 0
        self.siegeTeam = siegeTeam
        self.shipClass = shipClass
        self.shipSailPattern = None
        self.shipHullType = None
        self.shipRiggingType = None
        self.modelClass = ShipGlobals.getModelClass(shipClass)
        self.hull = None
        self.panels = []
        self.masts = [None, None, None, None, None]
        self.sails = [None, None, None, None, None]
        self.mastModels = [None, None, None, None, None]
        self.bowsprit = None
        self.ram = None
        self.cabin = None
        self.panelStates = []
        self.mastStates = [
         None, None, None, None, None]
        self.mastTypes = [None, None, None, None, None]
        self.smokeEffects = []
        self.oldHullHp = []
        self.oldMastHp = [[], [], [], [], []]
        self.modelRoot = self.attachNewNode('modelRoot')
        if not self.shipSailPattern or not self.shipHullType or not self.shipRiggingType:
            shipOVs = base.cr.getOwnerViewDoList(DistributedPlayerSimpleShipOV)
            shipOVs = [ ov for ov in shipOVs if ov.doId == self.shipId ]
            for currShipOV in shipOVs:
                self.shipSailPattern = currShipOV.customSailPattern
                self.shipHullType = currShipOV.customHull
                self.shipRiggingType = currShipOV.customRigging

        if shipClass and mastInfo:
            self.setShipInfo(shipClass, mastInfo)
        elif self.shipId:
            shipOVs = base.cr.getOwnerViewDoList(DistributedPlayerSimpleShipOV)
            shipOVs = [ ov for ov in shipOVs if ov.doId == self.shipId ]
            for currShipOV in shipOVs:
                self.setHullType(currShipOV.shipClass)
                masts = ShipGlobals.getMastSetup(currShipOV.shipClass)
                for i in range(5):
                    if masts[i]:
                        self.setMastType(i, masts[i][0], masts[i][1])

        self.accept('setShipClass-%s' % self.shipId, self.setHullType)
        self.accept('setMastType-%s' % self.shipId, self.setMastType)
        self.accept('ShipChanged-%s' % self.shipId, self.shipCustomColor)
        self.accept('setHullHp-%s' % self.shipId, self.setHullHp)
        self.accept('setBowspritHp-%s' % self.shipId, self.setBowspritHp)
        self.accept('setCabinHp-%s' % self.shipId, self.setCabinHp)
        self.accept('setMastHp-%s' % self.shipId, self.setMastHp)
        self.accept('setSailHp-%s' % self.shipId, self.setSailHp)
        return

    def setCustomization(self, customHull, customRigging, customPattern, customLogo):
        self.shipSailPattern = customPattern
        self.shipRiggingType = customRigging
        self.shipHullType = customHull
        if self.hull:
            hullColor = ShipUpgradeGlobals.HULL_TYPES[self.shipHullType]['PreviewColor']
            self.hull.setColor(hullColor)
            sailColor = ShipUpgradeGlobals.SAILCOLOR_TYPES[self.shipSailPattern]['PreviewColor']
            riggingColor = ShipUpgradeGlobals.RIGGING_TYPES[self.shipRiggingType]['PreviewColor']
            blendColor = (sailColor[0] * riggingColor[0], sailColor[1] * riggingColor[1], sailColor[2] * riggingColor[2], sailColor[3] * riggingColor[3])
            for mast in self.mastModels:
                if mast:
                    sails = mast.findAllMatches('**/sail_*')
                    for mySail in sails:
                        mySail.setColor(blendColor)

    def shipCustomColor(self, info=None):
        if self.shipId:
            shipOVs = base.cr.getOwnerViewDoList(DistributedPlayerSimpleShipOV)
            shipOVs = [ ov for ov in shipOVs if ov.doId == self.shipId ]
            for currShipOV in shipOVs:
                self.shipSailPattern = currShipOV.customSailPattern
                self.shipHullType = currShipOV.customHull
                self.shipRiggingType = currShipOV.customRigging
                if self.hull:
                    hullColor = ShipUpgradeGlobals.HULL_TYPES[max(1, self.shipHullType)]['PreviewColor']
                    self.hull.setColor(hullColor)
                    sailColor = ShipUpgradeGlobals.SAILCOLOR_TYPES[max(1, self.shipSailPattern)]['PreviewColor']
                    riggingColor = ShipUpgradeGlobals.RIGGING_TYPES[max(1, self.shipRiggingType)]['PreviewColor']
                    blendColor = (sailColor[0] * riggingColor[0], sailColor[1] * riggingColor[1], sailColor[2] * riggingColor[2], sailColor[3] * riggingColor[3])
                    for mast in self.mastModels:
                        if mast:
                            sails = mast.findAllMatches('**/sail_*')
                            for mySail in sails:
                                mySail.setColor(blendColor)

    def destroy(self):
        self.modelRoot = None
        self.ignoreAll()
        self.removeNode()
        return

    def setHullType(self, type):
        if self.panels:
            return
        if not type:
            return
        self.shipClass = type
        self.modelClass = ShipGlobals.getModelClass(type)
        modelType = ShipGlobals.getModelClass(type)
        filePrefix = HullDict.get(modelType)
        self.hull = loader.loadModel(filePrefix)
        self.hull.reparentTo(self.modelRoot)
        shipHullType = self.shipHullType
        if not shipHullType:
            shipHullType = 1
        hullColor = ShipUpgradeGlobals.HULL_TYPES[shipHullType]['PreviewColor']
        self.hull.setColor(hullColor)
        allPanels = self.hull.findAllMatches('**/panel_*')
        for i in range(len(allPanels)):
            panel = self.hull.find('**/panel_' + str(i))
            if not panel.isEmpty():
                self.panels.append(panel)
                self.panelStates.append(0)
                self.smokeEffects.append(None)

        self.bowsprit = self.hull.find('**/bowsprit')
        self.ram = self.hull.find('**/ram')
        self.cabin = self.hull.find('**/cabin')
        if self.bowsprit:
            self.bowsprit.detachNode()
        if self.modelClass == 1:
            self.cabin.detachNode()
        self.placeMasts()
        return

    def setMastType(self, index, type, height):
        if self.masts[index]:
            return
        if not type:
            return
        filePrefix = MastDict.get(type)
        self.mastModels[index] = loader.loadModel(filePrefix)
        myMasts = []
        myMastStates = []
        mySails = []
        mastSegments = self.mastModels[index].findAllMatches('**/mast_*')
        if type == ShipGlobals.Masts.Fore_Multi:
            sail1 = self.mastModels[index].find('**/sail_1')
            sail2 = self.mastModels[index].find('**/sail_2')
            sail1.setName('sail_2')
            sail2.setName('sail_1')
            sail = self.mastModels[index].find('**/sail_0')
            if sail:
                sail.stash()
        sails = self.mastModels[index].findAllMatches('**/sail_*')
        sailPattern = self.shipSailPattern
        shipRiggingType = self.shipRiggingType
        if not sailPattern:
            sailPattern = 1
        if not shipRiggingType:
            shipRiggingType = 1
        sailColor = ShipUpgradeGlobals.SAILCOLOR_TYPES[sailPattern]['PreviewColor']
        riggingColor = ShipUpgradeGlobals.RIGGING_TYPES[shipRiggingType]['PreviewColor']
        blendColor = (sailColor[0] * riggingColor[0], sailColor[1] * riggingColor[1], sailColor[2] * riggingColor[2], sailColor[3] * riggingColor[3])
        for mySail in sails:
            mySail.setColor(blendColor)

        for i in range(3):
            mastSegment = self.mastModels[index].find('**/mast_' + str(i))
            if not mastSegment.isEmpty():
                if i >= height:
                    mastSegment.stash()
                else:
                    myMasts.append(mastSegment)
                    myMastStates.append(0)
            sail = self.mastModels[index].find('**/sail_' + str(i))
            if not sail.isEmpty():
                if i >= height:
                    sail.stash()
                    mySails.append(None)
                else:
                    mySails.append(sail)
            else:
                mySails.append(None)

        self.masts[index] = myMasts
        self.mastStates[index] = myMastStates
        self.mastTypes[index] = type
        self.sails[index] = mySails
        if self.hull:
            self.placeMasts()
        return

    def placeMasts(self):
        masts = ShipGlobals.getMastSetup(self.shipClass)
        for index in range(5):
            mast = self.masts[index]
            if mast:
                self.mastModels[index].reparentTo(self.modelRoot)
                type = self.mastTypes[index]
                id = masts[index][0]
                if id in (ShipGlobals.Masts.Fore_Multi, ShipGlobals.Masts.Fore_Tri, ShipGlobals.Masts.Skel_Fore):
                    locator = self.hull.find('**/location_foremast;+s')
                elif id in (ShipGlobals.Masts.Main_Square, ShipGlobals.Masts.Main_Tri, ShipGlobals.Masts.Skel_Main_A, ShipGlobals.Masts.Skel_Main_B, ShipGlobals.Masts.Skel_Tri):
                    if self.modelClass == 11 and index == 1:
                        locator = self.hull.find('**/location_mainmast_2;+s')
                    else:
                        locator = self.hull.find('**/location_mainmast_' + str(index) + ';+s')
                elif id in (ShipGlobals.Masts.Aft_Tri, ShipGlobals.Masts.Skel_Aft):
                    locator = self.hull.find('**/location_aftmast;+s')
                if locator:
                    self.mastModels[index].setPos(locator.getPos())
                    self.mastModels[index].setHpr(locator.getHpr())
                    self.mastModels[index].setScale(locator.getScale())

    def setHullHp(self, hpArray, maxHpArray):
        if not self.panels:
            return
        for i in range(len(self.panels)):
            if i <= len(hpArray) - 1:
                hpFraction = float(hpArray[i]) / float(maxHpArray[i])
                damageColor = self.getDamageColor(hpFraction)
                self.panels[i].setColorScale(damageColor)
                if self.oldHullHp:
                    if self.oldHullHp[i] > hpArray[i]:
                        self.playFlash(self.panels[i], damageColor)
                if hpArray[i] <= 0 and self.panelStates[i] == 0:
                    self.panelStates[i] = 1
                elif hpArray[i] > 0 and self.panelStates[i] == 1:
                    self.panelStates[i] = 0
                    if self.smokeEffects[i]:
                        self.smokeEffects[i].endLoop()
            else:
                self.panels[i].stash()

        self.oldHullHp = copy.copy(hpArray)

    def setMastHp(self, index, hpArray, maxHpArray):
        if not self.masts[index]:
            return
        for i in range(len(self.masts[index])):
            if i > len(hpArray) - 1:
                if self.masts[index][i]:
                    self.masts[index][i].stash()

        for i in range(len(hpArray)):
            if i <= len(self.masts[index]) - 1:
                hpFraction = float(hpArray[i]) / float(maxHpArray[i])
                damageColor = self.getDamageColor(hpFraction)
                self.masts[index][i].setColorScale(damageColor)
                if self.oldMastHp[index]:
                    if self.oldMastHp[index][i] > hpArray[i]:
                        self.playFlash(self.masts[index][i], damageColor)
                if hpFraction <= 0:
                    self.mastStates[index][i] = 1
                else:
                    self.mastStates[index][i] = 0

        hasBreak = 0
        for i in range(len(hpArray)):
            if i <= len(self.masts[index]) - 1:
                if self.mastStates[index][i] == 0 and hasBreak == 0:
                    self.masts[index][i].show()
                    if self.sails[index][i]:
                        self.sails[index][i].show()
                else:
                    hasBreak = 1
                    self.masts[index][i].hide()
                    if self.sails[index][i]:
                        self.sails[index][i].hide()
                    self.oldMastHp[index] = copy.copy(hpArray)

    def setSailHp(self, mastIndex, sailIndex, hp, maxHp):
        if self.sails[mastIndex]:
            if len(self.mastStates[mastIndex]) - 1 >= sailIndex:
                hpFraction = float(hp) / float(maxHp)
                damageColor = self.getDamageColor(hpFraction)
                self.sails[mastIndex][sailIndex].setColorScale(damageColor)
                self.playFlash(self.sails[mastIndex][sailIndex], damageColor)
        for i in range(sailIndex):
            if self.mastStates[mastIndex]:
                if len(self.mastStates[mastIndex]) - 1 >= sailIndex:
                    if self.mastStates[mastIndex][i] == 1:
                        self.sails[mastIndex][sailIndex].hide()

    def setBowspritHp(self, hp, maxHp):
        hpFraction = float(hp) / float(maxHp)
        damageColor = self.getDamageColor(hpFraction)
        if self.bowsprit:
            self.bowsprit.setColorScale(damageColor)
            if hpFraction <= 0:
                self.bowsprit.hide()
            else:
                self.bowsprit.show()
                self.playFlash(self.bowsprit, damageColor)

    def setRamHp(self, hp, maxHp):
        hpFraction = float(hp) / float(maxHp)
        damageColor = self.getDamageColor(hpFraction)
        if self.ram:
            self.ram.setColorScale(damageColor)
            if hpFraction <= 0:
                self.ram.hide()
            else:
                self.ram.show()
                self.playFlash(self.ram, damageColor)

    def setCabinHp(self, hp, maxHp):
        hpFraction = float(hp) / float(maxHp)
        damageColor = self.getDamageColor(hpFraction)
        if self.cabin:
            self.cabin.setColorScale(damageColor)
            if hpFraction <= 0:
                self.cabin.hide()
            else:
                self.cabin.show()
                self.playFlash(self.cabin, damageColor)

    def getDamageColor(self, hpFraction):
        if hpFraction >= 0.5:
            return Vec4(1, 1, 1, 1)
        elif hpFraction >= 0.25:
            return Vec4(1, 1, 0, 1)
        elif hpFraction > 0:
            return Vec4(1, 0, 0.1, 1)
        elif hpFraction <= 0:
            return Vec4(0.5, 0, 0, 1)

    def playFlash(self, target, normalColor):
        flash = Sequence(Func(target.setColor, Vec4(1, 1, 0, 1)), Wait(0.1), Func(target.setColor, Vec4(1, 0, 0, 1)), Wait(0.1), Func(target.setColor, Vec4(1, 1, 0, 1)), Wait(0.1), Func(target.setColor, Vec4(1, 0, 0, 1)), Wait(0.1), Func(target.setColor, Vec4(1, 1, 0, 1)), Wait(0.1), Func(target.setColor, Vec4(1, 0, 0, 1)), Wait(0.1), Func(target.setColorOff))
        flash.start()

    def setShipInfo(self, shipClass, mastInfo):
        self.setHullType(shipClass)
        for mast in mastInfo.iteritems():
            if mast[1]:
                self.setMastType(mast[0], mast[1][0], mast[1][1])

    def getFlat(self):
        self.flattenStrong()
        counter = 1
        whites = NodePath('whites')
        woods = self.attachNewNode(PandaNode('woods'))
        for sailSet in self.sails:
            if sailSet:
                for sail in sailSet:
                    if sail:
                        sail = sail.find('**/+GeomNode')
                        if self.team == 0:
                            sail.setColor(0.7, 0.7, 0.5, 1)
                        elif self.team == 1:
                            sail.setColor(0.3, 0.3, 0.3, 1)
                        elif self.team == 2:
                            if counter % 2:
                                sail.setColor(0.6, 0, 0, 1)
                            else:
                                sail.setColor(0.6, 0.6, 0.6, 1)
                        elif self.team == 3:
                            if counter % 2:
                                sail.setColor(0, 0, 0, 1)
                            else:
                                sail.setColor(0.6, 0.6, 0.6, 1)
                        sail.flattenStrong()
                        sail.reparentTo(whites)
                        counter += 1

        self.findAllMatches('**/+GeomNode').reparentTo(woods)
        whites.reparentTo(self)
        self.findAllMatches('**/+ModelNode').detach()
        woods.setColor(0.2, 0.15, 0, 1)
        self.flattenStrong()
        gn = self.find('**/+GeomNode')
        for i in xrange(gn.node().getNumGeoms()):
            gn.node().setGeomState(i, RenderState.makeEmpty())

        gn.setTwoSided(1)
        gn.flattenStrong()
        return gn

    def setTeam(self, team):
        self.team = team

    def setModelClass(self, mc):
        self.modelClass = mc