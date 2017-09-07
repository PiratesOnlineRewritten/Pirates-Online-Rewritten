from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import ModelNode, LODNode, NodePath
from pandac.PandaModules import TextureStage
from pandac.PandaModules import AnimControlCollection, Character, PartSubset
from pirates.ship import ShipGlobals
from pirates.ship import ShipBlueprints
MastSubset = PartSubset()
MastSubset.addExcludeJoint('def_sail*')
MastSubset.addExcludeJoint('def_ladder*')
SailSubset = PartSubset()
SailSubset.addExcludeJoint('transform')
SailSubset.addExcludeJoint('def_mast*')
SailSubset.addExcludeJoint('def_ladder*')
SailSubset.addIncludeJoint('def_sail*')
HitMastSubset = PartSubset()
HitMastSubset.addIncludeJoint('transform')
HitMastSubset.addIncludeJoint('def_ladder*')
HitMastSubset.addIncludeJoint('def_mast*')
HitMastSubset.addExcludeJoint('def_sail*')
MissingAnims = {ShipGlobals.SKEL_WARSHIPL3: ('tiedup', 'rolldown', 'rollup'),ShipGlobals.SKEL_INTERCEPTORL3: ('tiedup', 'rolldown', 'rollup')}
SailReplace = {ShipGlobals.QUEEN_ANNES_REVENGE: 0}

class ShipFactory():
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipFactory')

    def __init__(self, phasedLoading=False):
        self.wantProws = config.GetBool('want-sprits', 0)
        self.hulls = {}
        self.texInfo = ({}, {}, {})
        self.models = {}
        self.mastSets = {}
        ShipBlueprints.setupWheel()
        ShipBlueprints.setupShipTextures()
        self.preprocessMast(ShipGlobals.Masts.Main_Tri)
        self.preprocessMast(ShipGlobals.Masts.Fore_Tri)
        self.preprocessHull(ShipGlobals.INTERCEPTORL1)
        self.preprocessMast(ShipGlobals.Masts.Skel_Main_A)
        self.preprocessMast(ShipGlobals.Masts.Skel_Main_B)
        self.preprocessMast(ShipGlobals.Masts.Skel_Tri)
        self.preprocessMast(ShipGlobals.Masts.Skel_Fore)
        self.preprocessMast(ShipGlobals.Masts.Skel_Aft)
        self.preprocessHull(ShipGlobals.SKEL_INTERCEPTORL3)
        self.preprocessHull(ShipGlobals.SKEL_WARSHIPL3)
        if not phasedLoading:
            self.handlePhase4()
            self.handlePhase5()
        self.baseLayer = TextureStage('base')
        self.colorLayer = TextureStage('color')
        self.logoLayer = TextureStage('logo')
        self.logoLayerNoColor = TextureStage('logoNoColor')
        self.logoLayerNoColorInv = TextureStage('logoNoColorInverse')
        self.logoLayerInv = TextureStage('logoInverse')
        self.vertLayer = TextureStage('vertex')
        self.colorLayer.setSort(1)
        self.colorLayer.setCombineRgb(TextureStage.CMReplace, TextureStage.CSTexture, TextureStage.COSrcColor)
        self.colorLayer.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        self.colorLayer.setTexcoordName('uvColor')
        self.logoLayer.setSort(2)
        self.logoLayer.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        self.logoLayer.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSPrevious, TextureStage.COSrcAlpha)
        self.logoLayer.setTexcoordName('uvLogo')
        self.logoLayerInv.setSort(2)
        self.logoLayerInv.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COOneMinusSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        self.logoLayerInv.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSPrevious, TextureStage.COSrcAlpha)
        self.logoLayerInv.setTexcoordName('uvLogo')
        self.logoLayerNoColor.setSort(2)
        self.logoLayerNoColor.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSConstant, TextureStage.COSrcColor, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        self.logoLayerNoColor.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSPrevious, TextureStage.COSrcAlpha)
        self.logoLayerNoColor.setTexcoordName('uvLogo')
        self.logoLayerNoColor.setColor((1, 1, 1, 1))
        self.logoLayerNoColorInv.setSort(2)
        self.logoLayerNoColorInv.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COOneMinusSrcColor, TextureStage.CSConstant, TextureStage.COSrcColor, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        self.logoLayerNoColorInv.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSPrevious, TextureStage.COSrcAlpha)
        self.logoLayerNoColorInv.setTexcoordName('uvLogo')
        self.logoLayerNoColorInv.setColor((1, 1, 1, 1))
        self.vertLayer.setSort(3)
        self.vertLayer.setCombineRgb(TextureStage.CMModulate, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSPrimaryColor, TextureStage.COSrcColor)
        self.vertLayer.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSPrimaryColor, TextureStage.COSrcAlpha)
        self.baseLayer.setSort(4)
        self.baseLayer.setCombineRgb(TextureStage.CMModulate, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor)
        self.baseLayer.setCombineAlpha(TextureStage.CMModulate, TextureStage.CSTexture, TextureStage.COSrcAlpha, TextureStage.CSPrevious, TextureStage.COSrcAlpha)

    def handlePhase4(self):
        self.preprocessHull(ShipGlobals.INTERCEPTORL2)
        self.preprocessHull(ShipGlobals.INTERCEPTORL3)
        self.preprocessMast(ShipGlobals.Masts.Main_Square)
        self.preprocessMast(ShipGlobals.Masts.Aft_Tri)
        self.preprocessMast(ShipGlobals.Masts.Fore_Multi)
        self.preprocessHull(ShipGlobals.WARSHIPL1)
        self.preprocessHull(ShipGlobals.WARSHIPL2)
        self.preprocessHull(ShipGlobals.WARSHIPL3)
        self.preprocessHull(ShipGlobals.MERCHANTL1)
        self.preprocessHull(ShipGlobals.MERCHANTL2)
        self.preprocessHull(ShipGlobals.MERCHANTL3)
        self.preprocessHull(ShipGlobals.BRIGL1)
        self.preprocessHull(ShipGlobals.BRIGL2)
        self.preprocessHull(ShipGlobals.BRIGL3)
        self.preprocessHull(ShipGlobals.QUEEN_ANNES_REVENGE)
        self.sprits = ShipBlueprints.preprocessSprits()

    def handlePhase5(self):
        self.preprocessHull(ShipGlobals.BLACK_PEARL)
        self.preprocessHull(ShipGlobals.GOLIATH)
        self.preprocessHull(ShipGlobals.SHIP_OF_THE_LINE)
        self.preprocessHull(ShipGlobals.EL_PATRONS_SHIP)

    def preprocessMast(self, mastClass):
        self.mastSets[mastClass] = ShipBlueprints.generateMastCache(mastClass)

    def preprocessHull(self, modelClass):
        self.hulls[modelClass] = ShipBlueprints.generateHullCache(modelClass)

    def getHull(self, modelClass, custom):
        return self.hulls[modelClass].getHullAsset(custom)

    def getShip(self, shipClass, style=ShipGlobals.Styles.Undefined, logo=ShipGlobals.Logos.Undefined, hullDesign=None, detailLevel=2, wantWheel=True, hullMaterial=None, sailMaterial=None, sailPattern=None, prowType=None, invertLogo=False):
        from pirates.ship import Ship
        modelClass = ShipGlobals.getModelClass(shipClass)
        shipConfig = ShipGlobals.getShipConfig(shipClass)
        if style == ShipGlobals.Styles.Undefined:
            style = shipConfig['defaultStyle']
        complexCustomization = 0
        if sailPattern or sailMaterial or hullMaterial or SailReplace.has_key(shipClass):
            complexCustomization = 1
        if not prowType:
            prowType = shipConfig['prow']
        if not hullMaterial:
            hullMaterial = style
        if not sailMaterial:
            if SailReplace.has_key(shipClass):
                sailMaterial = SailReplace[shipClass]
            else:
                sailMaterial = style
        if not sailPattern:
            sailPattern = style
        shipHullTexture = ShipBlueprints.getShipTexture(hullMaterial)
        shipTextureSail = ShipBlueprints.getShipTexture(sailMaterial)
        logoTex = None
        if logo:
            logoTex = ShipBlueprints.getLogoTexture(logo)
        sailPatternTex = None
        if sailPattern:
            sailPatternTex = ShipBlueprints.getSailTexture(sailPattern)
        self.notify.debug('%s %s' % (sailPattern, logo))
        if logo == ShipGlobals.Logos.Undefined:
            logo = shipConfig['sailLogo']
        if logo in ShipGlobals.MAST_LOGO_PLACEMENT_LIST:
            placeLogos = 1
        else:
            placeLogos = 0
        if modelClass <= ShipGlobals.INTERCEPTORL3:
            mastHax = True
        else:
            mastHax = False
        customHull = hullDesign is not None
        customMasts = logo != 0 or sailPattern != 0
        hull = self.getHull(modelClass, customHull)
        breakAnims = {}
        metaAnims = {}
        hitAnims = {}
        root = NodePath('Ship')
        hull.locators.reparentTo(root)
        charRoot = root.attachNewNode(Character('ShipChar'))
        collisions = root.attachNewNode('collisions')
        lodNode = charRoot.attachNewNode(LODNode('lod'))
        if detailLevel == 0:
            lodNode.node().addSwitch(200, 0)
            lodNode.node().addSwitch(800, 200)
            lodNode.node().addSwitch(100000, 800)
            high = lodNode.attachNewNode('high')
            low = lodNode.attachNewNode('low')
            med = NodePath('med')
            superlow = lodNode.attachNewNode('superlow')
        else:
            if detailLevel == 1:
                lodNode.node().addSwitch(300, 0)
                lodNode.node().addSwitch(1000, 300)
                lodNode.node().addSwitch(2000, 1000)
                lodNode.node().addSwitch(100000, 2000)
                high = lodNode.attachNewNode('high')
                med = lodNode.attachNewNode('med')
                low = lodNode.attachNewNode('low')
                superlow = lodNode.attachNewNode('superlow')
            else:
                lodNode.node().addSwitch(750, 0)
                lodNode.node().addSwitch(3000, 750)
                lodNode.node().addSwitch(8000, 3000)
                lodNode.node().addSwitch(100000, 8000)
                high = lodNode.attachNewNode('high')
                med = lodNode.attachNewNode('med')
                low = lodNode.attachNewNode('low')
                superlow = lodNode.attachNewNode('superlow')
            mastSetup = ShipGlobals.getMastSetup(shipClass)
            for data in [(0, 'location_mainmast_0'), (1, 'location_mainmast_1'), (2, 'location_mainmast_2'), (3, 'location_aftmast*'), (4, 'location_foremast*')]:
                mastData = mastSetup.get(data[0])
                if mastData:
                    mast = self.mastSets[mastData[0]].getMastSet(mastData[1] - 1, customMasts)
                    mastRoot = hull.locators.find('**/%s' % data[1]).getTransform(hull.locators)
                    model = NodePath(mast.charRoot)
                    model.setTransform(mastRoot)
                    if complexCustomization:
                        model.setTexture(shipTextureSail)
                    useLogoTex = logoTex
                    if placeLogos:
                        mastNum = data[0]
                        if mastNum not in ShipGlobals.MAST_LOGO_PLACEMENT.get(modelClass):
                            useLogoTex = None
                    charBundle = mast.charRoot.getBundle(0)
                    if data[0] < 3:
                        for side in ['left', 'right']:
                            ropeNode = hull.locators.find('**/location_ropeLadder_%s_%s' % (side, data[0]))
                            if ropeNode:
                                transform = ropeNode.getTransform(NodePath(mast.charRoot))
                                charBundle.findChild('def_ladder_0_%s' % side).applyFreeze(transform)

                    if sailPatternTex and useLogoTex:
                        for node in model.findAllMatches('**/sails'):
                            node.setTextureOff(TextureStage.getDefault())
                            node.setTexture(self.colorLayer, sailPatternTex)
                            if invertLogo:
                                node.setTexture(self.logoLayerInv, logoTex)
                            else:
                                node.setTexture(self.logoLayer, logoTex)
                            node.setTexture(self.vertLayer, shipTextureSail)
                            node.setTexture(self.baseLayer, shipTextureSail)

                    else:
                        if sailPatternTex:
                            for node in model.findAllMatches('**/sails'):
                                node.setTextureOff(TextureStage.getDefault())
                                node.setTexture(self.colorLayer, sailPatternTex)
                                node.setTexture(self.vertLayer, shipTextureSail)
                                node.setTexture(self.baseLayer, shipTextureSail)

                        elif useLogoTex:
                            for node in model.findAllMatches('**/sails'):
                                node.setTextureOff(TextureStage.getDefault())
                                if invertLogo:
                                    node.setTexture(self.logoLayerNoColorInv, logoTex)
                                else:
                                    node.setTexture(self.logoLayerNoColor, logoTex)
                                node.setTexture(self.vertLayer, shipTextureSail)
                                node.setTexture(self.baseLayer, shipTextureSail)

                        model.flattenLight()
                        if detailLevel == 0:
                            model.find('**/low').copyTo(high)
                            model.find('**/low').copyTo(low)
                            model.find('**/superlow').copyTo(superlow)
                        else:
                            if detailLevel == 1:
                                model.find('**/med').copyTo(high)
                                model.find('**/med').copyTo(med)
                                low.node().stealChildren(model.find('**/low').node())
                                superlow.node().stealChildren(model.find('**/superlow').node())
                            elif detailLevel == 2:
                                high.node().stealChildren(model.find('**/high').node())
                                med.node().stealChildren(model.find('**/med').node())
                                low.node().stealChildren(model.find('**/low').node())
                                superlow.node().stealChildren(model.find('**/superlow').node())
                            mastRoot = mast.collisions.find('**/collision_masts')
                            if modelClass > ShipGlobals.INTERCEPTORL3 or data[0] != 3:
                                mastCode = str(data[0])
                                mastRoot.setTag('Mast Code', mastCode)
                            else:
                                mastRoot.setName('colldision_sub_mast')
                                mastRoot.reparentTo(collisions.find('**/collision_masts'))
                                mastCode = '0'
                            for coll in mast.collisions.findAllMatches('**/collision_sail_*'):
                                coll.setName('Sail-%s' % data[0])
                                coll.setTag('Mast Code', mastCode)

                            for coll in mast.collisions.findAllMatches('**/sail_*'):
                                coll.setName('Sail-%s' % data[0])
                                coll.setTag('Mast Code', mastCode)

                        collisions.node().stealChildren(mast.collisions.node())
                        charBundle = mast.charRoot.getBundle(0)
                        if mastHax and data[0] == 3:
                            breakAnims[0][0].storeAnim(charBundle.loadBindAnim(loader.loader, mast.breakAnim[0], -1, MastSubset, True), '1')
                            breakAnims[0][1].storeAnim(charBundle.loadBindAnim(loader.loader, mast.breakAnim[1], -1, MastSubset, True), '1')
                            tempHit = hitAnims[0]
                            tempHit[0].storeAnim(charBundle.loadBindAnim(loader.loader, mast.hitAnim, -1, HitMastSubset, True), '1')
                            tempHit[1].storeAnim(charBundle.loadBindAnim(loader.loader, mast.hitAnim, -1, PartSubset(), True), '1')
                        else:
                            breakAnims[data[0]] = (
                             AnimControlCollection(), AnimControlCollection())
                            breakAnims[data[0]][0].storeAnim(charBundle.loadBindAnim(loader.loader, mast.breakAnim[0], -1, MastSubset, True), '0')
                            breakAnims[data[0]][1].storeAnim(charBundle.loadBindAnim(loader.loader, mast.breakAnim[1], -1, MastSubset, True), '0')
                            tempHit = [AnimControlCollection(), AnimControlCollection()]
                            tempHit[0].storeAnim(charBundle.loadBindAnim(loader.loader, mast.hitAnim, -1, HitMastSubset, True), '0')
                            tempHit[1].storeAnim(charBundle.loadBindAnim(loader.loader, mast.hitAnim, -1, PartSubset(), True), '0')
                            hitAnims[data[0]] = tempHit
                        for anim, fileName in mast.metaAnims.iteritems():
                            if anim not in metaAnims:
                                metaAnims[anim] = AnimControlCollection()
                            if anim not in MissingAnims.get(modelClass, []):
                                ac = charBundle.loadBindAnim(loader.loader, fileName, -1, SailSubset, True)
                                if ac:
                                    metaAnims[anim].storeAnim(ac, str(metaAnims[anim].getNumAnims()))

                    charRoot.node().combineWith(mast.charRoot)

            if self.wantProws and prowType:
                highSprit, medSprit, lowSprit = self.sprits[prowType].getAsset()
                transform = hull.locators.find('**/location_bowsprit').getTransform(hull.locators)
                highSprit.setTransform(transform)
                medSprit.setTransform(transform)
                lowSprit.setTransform(transform)
                highSprit.reparentTo(hull.geoms[0])
                medSprit.reparentTo(hull.geoms[1])
                lowSprit.reparentTo(hull.geoms[2])
            if wantWheel:
                shipWheel = ShipBlueprints.getWheel()
                wheelPoint = hull.locators.find('**/location_wheel;+s').getTransform(hull.locators)
                shipWheel.setTransform(wheelPoint)
                shipWheel.flattenLight()
                shipWheel.find('**/collisions').copyTo(collisions)
                hull.geoms[0].node().stealChildren(shipWheel.find('**/high').node())
                hull.geoms[1].node().stealChildren(shipWheel.find('**/med').node())
                hull.geoms[2].node().stealChildren(shipWheel.find('**/low').node())
            if complexCustomization:
                hull.geoms[0].setTexture(shipHullTexture)
                hull.geoms[0].flattenLight()
                hull.geoms[1].setTexture(shipHullTexture)
                hull.geoms[1].flattenLight()
                hull.geoms[2].setTexture(shipHullTexture)
                hull.geoms[2].flattenLight()
                hull.geoms[3].setTexture(shipHullTexture)
                hull.geoms[3].flattenLight()
            high.attachNewNode(ModelNode('non-animated')).node().stealChildren(hull.geoms[0].node())
            med.attachNewNode(ModelNode('non-animated')).node().stealChildren(hull.geoms[1].node())
            low.attachNewNode(ModelNode('non-animated')).node().stealChildren(hull.geoms[2].node())
            superlow.attachNewNode(ModelNode('non-animated')).node().stealChildren(hull.geoms[3].node())
            collisions.node().stealChildren(hull.collisions.node())
            hull.locators.stash()
            charRoot.flattenStrong()
            ship = Ship.Ship(shipClass, root, breakAnims, hitAnims, metaAnims, collisions, hull.locators)
            if not complexCustomization:
                ship.char.setTexture(shipHullTexture)
        return ship

    def getAIShip(self, shipClass):
        from pirates.ship import ShipAI
        modelClass = ShipGlobals.getModelClass(shipClass)
        hull = self.getHull(modelClass, 0)
        root = NodePath('Ship')
        collisions = root.attachNewNode('collisions')
        mastSetup = ShipGlobals.getMastSetup(shipClass)
        for data in [(0, 'location_mainmast_0'), (1, 'location_mainmast_1'), (2, 'location_mainmast_2'), (3, 'location_aftmast*'), (4, 'location_foremast*')]:
            mastData = mastSetup.get(data[0])
            if mastData:
                mast = self.mastSets[mastData[0]].getMastSet(mastData[1] - 1)
                model = NodePath(mast.charRoot)
                model.setPos(hull.locators.find('**/%s' % data[1]).getPos(hull.locators))
                model.setHpr(hull.locators.find('**/%s' % data[1]).getHpr(hull.locators))
                model.setScale(hull.locators.find('**/%s' % data[1]).getScale(hull.locators))
                if modelClass > ShipGlobals.INTERCEPTORL3 or data[0] != 3:
                    mastCode = str(data[0])
                else:
                    mastCode = '0'
                mast.collisions.find('**/collision_masts').setTag('Mast Code', mastCode)
                collisions.node().stealChildren(mast.collisions.node())

        collisions.node().stealChildren(hull.collisions.node())
        hull.locators.reparentTo(root)
        ship = ShipAI.ShipAI(root, collisions, hull.locators)
        ship.modelRoot.setTag('Mast Code', str(255))
        ship.modelRoot.setTag('Hull Code', str(255))
        return ship