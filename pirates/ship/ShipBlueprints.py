from pandac.PandaModules import NodePath, TextureStage, ModelNode, SceneGraphReducer, TextureAttrib, CullFaceAttrib, GeomNode, TransparencyAttrib, CullBinAttrib
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals
BowSpritDict = {ShipGlobals.Prows.Skeleton: 'models/shipparts/prow_skeleton_zero',ShipGlobals.Prows.Lady: 'models/shipparts/prow_female_zero'}
LogoDict = {ShipGlobals.Logos.Navy: 'logo_redSkull',ShipGlobals.Logos.BlackPearl: 'ship_sailBP_patches',ShipGlobals.Logos.EITC: 'logo_eitc',ShipGlobals.Logos.EITC_Emblem: 'logo_eitc_emblem',ShipGlobals.Logos.PVP_French: 'logo_french_flag',ShipGlobals.Logos.PVP_Spanish: 'logo_spanish_flag',ShipGlobals.Logos.Bandit_Bull: 'pir_t_shp_logo_bandit_01',ShipGlobals.Logos.Bandit_Dagger: 'pir_t_shp_logo_bandit_02',ShipGlobals.Logos.Bandit_Scorpion: 'pir_t_shp_logo_bandit_03',ShipGlobals.Logos.Bandit_Claw: 'pir_t_shp_logo_bandit_04',ShipGlobals.Logos.Player_Hawk: 'pir_t_shp_log_hawk_solid',ShipGlobals.Logos.Player_Rose: 'pir_t_shp_log_rose',ShipGlobals.Logos.Player_Flame: 'pir_t_shp_log_flame',ShipGlobals.Logos.Player_SpanishBull: 'pir_t_shp_log_spanishbull',ShipGlobals.Logos.Player_Wolf: 'pir_t_shp_log_wolf_a',ShipGlobals.Logos.Player_Angel: 'pir_t_shp_log_angelwings',ShipGlobals.Logos.Player_Dragon: 'pir_t_shp_log_dragon',ShipGlobals.Logos.Player_Shield: 'pir_t_shp_log_swordandshield',ShipGlobals.Logos.Player_Heart: 'pir_t_shp_log_piercedheart',ShipGlobals.Logos.Treasure_Navy: 'pir_t_shp_log_navyTreasure_a',ShipGlobals.Logos.Treasure_EITC: 'pir_t_shp_log_eitcTreasure_a',ShipGlobals.Logos.Bounty_Hunter_Wasp: 'pir_t_shp_logo_wasp',ShipGlobals.Logos.Bounty_Hunter_Spider: 'pir_t_shp_logo_spider',ShipGlobals.Logos.Bounty_Hunter_Snake: 'pir_t_shp_logo_snake',ShipGlobals.Logos.Navy_Hunter_Unicorn: 'pir_t_shp_log_unicorn',ShipGlobals.Logos.Navy_Hunter_Lion: 'pir_t_shp_log_lion',ShipGlobals.Logos.Contest_Skull: 'pir_t_shp_logo_SkullCross',ShipGlobals.Logos.Contest_Octopus: 'pir_t_shp_logo_Octopus',ShipGlobals.Logos.Contest_Shark: 'pir_t_shp_logo_Shark',ShipGlobals.Logos.Contest_Mermaid: 'pir_t_shp_logo_Mermaid',ShipGlobals.Logos.Contest_StormCloud: 'pir_t_shp_logo_StormCloud'}
shipStyles = {ShipGlobals.Styles.Player: 'ships_static_a_palette_3cmla_1',ShipGlobals.Styles.Navy: 'ships_static_a_palette_3cmla_1_swp_1',ShipGlobals.Styles.EITC: 'ships_static_a_palette_3cmla_2_swp_2',ShipGlobals.Styles.Undead: 'ships_static_a_palette_3cmla_3_swp_3',ShipGlobals.Styles.BP: 'ships_static_a_palette_3cmla_4_swp_4',ShipGlobals.Styles.Treasure_Navy: 'ships_static_a_palette_3cmla_5_swp_5',ShipGlobals.Styles.Treasure_EITC: 'ships_static_a_palette_3cmla_6_swp_6',ShipGlobals.Styles.QueenAnnesRevenge: 'ships_static_qar_palette_3cmla_1',ShipGlobals.Styles.BountyHunter_A: 'ships_static_a_palette_3cmla_1',ShipGlobals.Styles.BountyHunter_B: 'ships_static_a_palette_3cmla_1',ShipGlobals.Styles.BountyHunter_C: 'ships_static_a_palette_3cmla_3_swp_3',ShipGlobals.Styles.BountyHunter_D: 'ships_static_a_palette_3cmla_4_swp_4',ShipGlobals.Styles.BountyHunter_E: 'ships_static_a_palette_3cmla_1_swp_1',ShipGlobals.Styles.BountyHunter_F: 'ships_static_a_palette_3cmla_1',ShipGlobals.Styles.BountyHunter_G: 'ships_static_a_palette_3cmla_3_swp_3',ShipGlobals.Styles.NavyHunter: 'ships_static_a_palette_3cmla_1_swp_1',ShipGlobals.Styles.Streamlined: 'ships_static_a_palette_3cmla_7_swp_7',ShipGlobals.Styles.CargoShip: 'ships_static_a_palette_3cmla_8_swp_8',ShipGlobals.Styles.Reinforced: 'ships_static_a_palette_3cmla_9_swp_9',ShipGlobals.Styles.SkullBones: 'ships_static_a_palette_3cmla_10_swp_10',ShipGlobals.Styles.FortuneHunter: 'ships_static_a_palette_3cmla_11_swp_11',ShipGlobals.Styles.FireStorm: 'ships_static_a_palette_3cmla_12_swp_12',ShipGlobals.Styles.IronClad: 'ships_static_a_palette_3cmla_13_swp_13',ShipGlobals.Styles.StormChaser: 'ships_static_a_palette_3cmla_14_swp_14'}
ColorDict = {ShipGlobals.Styles.Navy: 'pir_t_shp_clr_navy',ShipGlobals.Styles.EITC: 'pir_t_shp_clr_eitc',ShipGlobals.Styles.French: 'pir_t_shp_clr_french',ShipGlobals.Styles.Spanish: 'pir_t_shp_clr_spanish',ShipGlobals.Styles.BP: 'pir_t_shp_clr_blackPearl',ShipGlobals.Styles.Bandit01: 'pir_t_shp_clr_bandit_01',ShipGlobals.Styles.Bandit02: 'pir_t_shp_clr_bandit_02',ShipGlobals.Styles.Bandit03: 'pir_t_shp_clr_bandit_03',ShipGlobals.Styles.Bandit04: 'pir_t_shp_clr_bandit_04',ShipGlobals.Styles.Treasure_Navy: 'pir_t_shp_clr_navy',ShipGlobals.Styles.Treasure_EITC: 'pir_t_shp_clr_eitc',ShipGlobals.Styles.QueenAnnesRevenge: 'pir_t_shp_clr_bandit_01',ShipGlobals.Styles.BountyHunter_A: 'pir_t_shp_clr_7stripe_green',ShipGlobals.Styles.BountyHunter_B: 'pir_t_shp_clr_7stripe_red',ShipGlobals.Styles.BountyHunter_C: 'pir_t_shp_clr_bandit_03',ShipGlobals.Styles.BountyHunter_D: 'pir_t_shp_clr_7stripe_violet',ShipGlobals.Styles.BountyHunter_E: 'pir_t_shp_clr_bandit_01',ShipGlobals.Styles.BountyHunter_F: 'pir_t_shp_clr_blackPearl',ShipGlobals.Styles.BountyHunter_G: 'pir_t_shp_clr_bandit_04',ShipGlobals.Styles.NavyHunter: 'pir_t_shp_clr_navy',ShipGlobals.Styles.Streamlined: 'pir_t_shp_clr_bandit_01',ShipGlobals.Styles.CargoShip: 'pir_t_shp_clr_bandit_01',ShipGlobals.Styles.Reinforced: 'pir_t_shp_clr_bandit_01',ShipGlobals.Styles.SkullBones: 'pir_t_shp_clr_bandit_01',ShipGlobals.Styles.SailWhite: 'pir_t_shp_clr_white',ShipGlobals.Styles.SailBlack: 'pir_t_shp_clr_black',ShipGlobals.Styles.SailGray: 'pir_t_shp_clr_gray',ShipGlobals.Styles.SailBrown: 'pir_t_shp_clr_brown',ShipGlobals.Styles.SailGold: 'pir_t_shp_clr_gold',ShipGlobals.Styles.SailTan: 'pir_t_shp_clr_tan',ShipGlobals.Styles.SailOlive: 'pir_t_shp_clr_olive',ShipGlobals.Styles.SailRed: 'pir_t_shp_clr_red',ShipGlobals.Styles.SailOrange: 'pir_t_shp_clr_orange',ShipGlobals.Styles.SailYellow: 'pir_t_shp_clr_yellow',ShipGlobals.Styles.SailGreen: 'pir_t_shp_clr_green',ShipGlobals.Styles.SailCyan: 'pir_t_shp_clr_cyan',ShipGlobals.Styles.SailBlue: 'pir_t_shp_clr_blue',ShipGlobals.Styles.SailPurple: 'pir_t_shp_clr_purple',ShipGlobals.Styles.SailPink: 'pir_t_shp_clr_pink',ShipGlobals.Styles.SailRose: 'pir_t_shp_clr_rose',ShipGlobals.Styles.SailLime: 'pir_t_shp_clr_lime',ShipGlobals.Styles.SailMaroon: 'pir_t_shp_clr_maroon'}
wheel = None
MastData = {ShipGlobals.Masts.Main_Tri: {'maxHeight': 2,'prefix': 'main_tri'},ShipGlobals.Masts.Main_Square: {'maxHeight': 3,'prefix': 'main_square'},ShipGlobals.Masts.Fore_Tri: {'maxHeight': 1,'prefix': 'fore_tri'},ShipGlobals.Masts.Fore_Multi: {'maxHeight': 3,'prefix': 'fore_multi'},ShipGlobals.Masts.Aft_Tri: {'maxHeight': 1,'prefix': 'aft_tri'},ShipGlobals.Masts.Skel_Main_A: {'maxHeight': 3,'prefix': 'main_square_skeletonA'},ShipGlobals.Masts.Skel_Main_B: {'maxHeight': 3,'prefix': 'main_square_skeletonB'},ShipGlobals.Masts.Skel_Tri: {'maxHeight': 2,'prefix': 'main_tri_skeleton'},ShipGlobals.Masts.Skel_Fore: {'maxHeight': 2,'prefix': 'fore_skeleton'},ShipGlobals.Masts.Skel_Aft: {'maxHeight': 2,'prefix': 'aft_skeleton'}}
metaAnims = [
 'rolldown', 'rollup', 'idle', 'tiedup']
HullDict = {ShipGlobals.WARSHIPL1: 'frg_light',ShipGlobals.WARSHIPL2: 'frg_regular',ShipGlobals.WARSHIPL3: 'frg_war',ShipGlobals.MERCHANTL1: 'gal_light',ShipGlobals.MERCHANTL2: 'gal_regular',ShipGlobals.MERCHANTL3: 'gal_war',ShipGlobals.INTERCEPTORL1: 'slp_light',ShipGlobals.INTERCEPTORL2: 'slp_regular',ShipGlobals.INTERCEPTORL3: 'slp_war',ShipGlobals.BRIGL1: 'brig_light',ShipGlobals.BRIGL2: 'brig_regular',ShipGlobals.BRIGL3: 'brig_war',ShipGlobals.BLACK_PEARL: 'cas_blackPearl',ShipGlobals.GOLIATH: 'cas_goliath',ShipGlobals.QUEEN_ANNES_REVENGE: 'cas_queenAnnesRevenge',ShipGlobals.SHIP_OF_THE_LINE: 'lin_treasure',ShipGlobals.SKEL_WARSHIPL3: 'skl_frigate',ShipGlobals.SKEL_INTERCEPTORL3: 'skl_sloop'}
if config.GetBool('want-kraken', 0):
    HullDict[23] = 'frg_war_kraken'

class MastSet():

    def __init__(self):
        self.charRoot = None
        self.collisions = None
        self.breakAnim = None
        self.hitAnim = None
        self.metaAnims = {}
        return


class MastCache():

    def __init__(self):
        self.charRoot = None
        self.genericGeomSets = []
        self.customGeomSets = []
        self.collisions = None
        self.breakAnim = None
        self.metaAnims = {}
        self.hitAnim = None
        return

    def getMastSet(self, index, custom=False):
        data = MastSet()
        if custom:
            for lod in self.customGeomSets[index]:
                lod.reparentTo(NodePath(self.charRoot))

        else:
            for lod in self.genericGeomSets[index]:
                lod.reparentTo(NodePath(self.charRoot))

            data.charRoot = NodePath(self.charRoot).copyTo(NodePath()).node()
            data.collisions = NodePath(data.charRoot).find('**/collisions')
            if index == 0:
                data.collisions.findAllMatches('**/*_1*').detach()
                data.collisions.findAllMatches('**/*_2*').detach()
            elif index == 1:
                data.collisions.findAllMatches('**/*_2*').detach()
            if custom:
                for lod in self.customGeomSets[index]:
                    lod.detachNode()

            else:
                for lod in self.genericGeomSets[index]:
                    lod.detachNode()

        data.breakAnim = self.breakAnim
        data.metaAnims = self.metaAnims
        data.hitAnim = self.hitAnim
        return data


class SpritCache():

    def __init__(self):
        self.root = None
        self.high = None
        self.med = None
        self.low = None
        return

    def getAsset(self):
        return (
         self.high.copyTo(NodePath()), self.med.copyTo(NodePath()), self.low.copyTo(NodePath()))


class HullAsset():

    def __init__(self):
        self.root = None
        self.geoms = []
        self.locators = None
        self.collisions = None
        return


class HullCache():

    def __init__(self):
        self.root = None
        self.genericGeoms = []
        self.customGeoms = []
        self.locators = None
        self.collisions = None
        self.cannonRoot = None
        return

    def getHullAsset(self, custom=False):
        data = HullAsset()
        data.root = self.root.copyTo(NodePath())
        if custom:
            data.geoms = [ x.copyTo(NodePath()) for x in self.customGeoms ]
        else:
            data.geoms = [ x.copyTo(NodePath()) for x in self.genericGeoms ]
        data.locators = self.locators.copyTo(NodePath())
        data.collisions = self.collisions.copyTo(NodePath())
        return data


def preprocessSprits():
    spritDict = {}
    for prowType in BowSpritDict:
        file = BowSpritDict[prowType]
        model = loader.loadModel(file)
        high = model.find('**/geometry_*igh*')
        med = model.find('**/geometry_*ed*')
        low = model.find('**/geometry_*ow*')
        high.node().setPreserveTransform(ModelNode.PTDropNode)
        high.flattenStrong()
        med.node().setPreserveTransform(ModelNode.PTDropNode)
        med.flattenStrong()
        low.node().setPreserveTransform(ModelNode.PTDropNode)
        low.flattenStrong()
        data = SpritCache()
        data.high = high
        data.med = med
        data.low = low
        spritDict[prowType] = data

    return spritDict


def preFlatten(geom):
    gr = SceneGraphReducer()
    gr.applyAttribs(geom.node(), gr.TTColor | gr.TTColorScale | gr.TTTransform | gr.TTCullFace | gr.TTTexMatrix)


def collapse(np):
    np.findAllMatches('**/+GeomNode').wrtReparentTo(np)
    np.flattenStrong()


def stripAttribs(geom, cls):
    for np in geom.findAllMatches('**/+GeomNode'):
        node = np.node()
        for i in range(node.getNumGeoms()):
            gs = node.getGeomState(i)
            node.setGeomState(i, gs.removeAttrib(cls.getClassType()))

    if geom.node().getClassType() == GeomNode.getClassType():
        node = geom.node()
        for i in range(node.getNumGeoms()):
            gs = node.getGeomState(i)
            node.setGeomState(i, gs.removeAttrib(cls.getClassType()))


def generateHullCache(modelClass):
    geom = loader.loadModel('models/shipparts/pir_m_shp_%s' % HullDict[modelClass])
    stripPrefix(geom, 'model:')
    for node in geom.findAllMatches('**/omit'):
        parent = node.getParent()
        omit = parent.attachNewNode(ModelNode('omit'))
        node.reparentTo(omit)
        node.setName('geom')

    preFlatten(geom)
    logic = loader.loadModel('models/shipparts/pir_m_shp_%s_logic' % HullDict[modelClass])
    locators = logic.find('**/locators')
    for side in ['left', 'right']:
        bad = locators.find('**/location_ropeLadder_0_%s' % side)
        if bad:
            bad.setName('location_ropeLadder_%s_0' % side)
        bad = locators.find('**/location_ropeLadder_1_%s' % side)
        if bad:
            bad.setName('location_ropeLadder_%s_1' % side)
        bad = locators.find('**/location_ropeLadder_1_%s1' % side)
        if bad:
            bad.setName('location_ropeLadder_%s_2' % side)

    collisions = logic.find('**/collisions')
    badPanel = collisions.find('**/collision_panel_3')
    if badPanel:
        badPanel.setName('collision_panel_2')
    collisions.find('**/collision_panel_0').setTag('Hull Code', '0')
    collisions.find('**/collision_panel_1').setTag('Hull Code', '1')
    collisions.find('**/collision_panel_2').setTag('Hull Code', '2')
    walls = collisions.find('**/collision_walls')
    if walls:
        walls.setTag('Hull Code', '255')
    else:
        collisions.attachNewNode('collision_walls')
    shipToShipCollide = collisions.find('**/collision_shiptoship')
    shipToShipCollide.setCollideMask(PiratesGlobals.ShipCollideBitmask)
    deck = collisions.find('**/collision_deck')
    if not deck:
        deck = collisions.attachNewNode('deck')
    mask = deck.getCollideMask()
    mask ^= PiratesGlobals.FloorBitmask
    mask |= PiratesGlobals.ShipFloorBitmask
    deck.setCollideMask(mask)
    floors = collisions.find('**/collision_floors')
    if not floors:
        floors = collisions.find('**/collision_floor')
    mask = floors.getCollideMask()
    mask ^= PiratesGlobals.FloorBitmask
    mask |= PiratesGlobals.ShipFloorBitmask
    floors.setCollideMask(mask)
    floors.setTag('Hull Code', str(255))
    geomHigh = geom.find('**/lod_high')
    geomMed = geom.find('**/lod_medium')
    if not geomMed:
        geomMed = geom.find('**/low_medium')
    if not geomMed:
        geomMed = geomHigh.copyTo(NodePath())
    geomLow = geom.find('**/lod_low')
    if not geomLow:
        geomLow = geomMed.copyTo(NodePath())
    geomSuperLow = geom.find('**/lod_superlow')
    if not geomSuperLow:
        geomSuperLow = geomLow.copyTo(NodePath())
    geomHigh.setName('high')
    geomMed.setName('med')
    geomLow.setName('low')
    geomSuperLow.setName('superlow')
    if modelClass in [21, 22, 23]:
        spike = loader.loadModel('models/shipparts/pir_m_shp_ram_spike')
        spikeTrans = locators.find('**/location_ram').getTransform(locators)
        spike.setTransform(spikeTrans)
        spike.flattenLight()
        spikeHi = spike.find('**/lod_high')
        spikeMed = spike.find('**/lod_medium')
        spikeLow = spike.find('**/lod_low')
        spikeHi.copyTo(geomHigh)
        spikeMed.copyTo(geomMed)
        spikeLow.copyTo(geomLow)
        spikeLow.copyTo(geomSuperLow)
    flipRoot = NodePath('root')
    collisions.reparentTo(flipRoot)
    locators.reparentTo(flipRoot)
    geomHigh.reparentTo(flipRoot)
    geomMed.reparentTo(flipRoot)
    geomLow.reparentTo(flipRoot)
    geomSuperLow.reparentTo(flipRoot)
    flipRoot.setH(180)
    flipRoot.flattenLight()
    omits = flipRoot.findAllMatches('**/omit')
    for node in omits:
        node.flattenStrong()

    for group in ['static', 'transparent', 'ropeLadder_*', 'stripeA', 'stripeB', 'pattern']:
        for node in flipRoot.findAllMatches('**/%s' % group):
            name = node.getName()
            for subNode in node.findAllMatches('**/*'):
                subNode.setName(name)

            node.flattenStrong()
            node.setName(name)

    geomHigh.detachNode()
    geomMed.detachNode()
    geomLow.detachNode()
    geomSuperLow.detachNode()
    locators.detachNode()
    collisions.detachNode()
    genericGeoms = [
     geomHigh, geomMed, geomLow, geomSuperLow]
    customGeoms = [ x.copyTo(NodePath()) for x in genericGeoms ]
    for np in genericGeoms:
        trans = np.find('**/transparent')
        if trans:
            trans.stash()
        np.flattenLight()
        sails = np.findAllMatches('**/sails')
        sails.stash()
        omits = np.findAllMatches('**/omit')
        omits.stash()
        for node in omits:
            node.node().setPreserveTransform(node.node().PTDropNode)

        generic = NodePath('generic')
        np.findAllMatches('**/+GeomNode').wrtReparentTo(generic)
        np.findAllMatches('*').detach()
        generic.flattenStrong()
        generic.reparentTo(np)
        stripAttribs(generic, TextureAttrib)
        stripAttribs(generic, TransparencyAttrib)
        stripAttribs(generic, CullBinAttrib)
        generic.setBin('ground', 1)
        collapse(generic)
        sails.unstash()
        sails.reparentTo(np)
        for node in sails:
            node.node().setPreserveTransform(node.node().PTDropNode)

        if trans:
            trans.unstash()
            trans.flattenStrong()
            if trans.node().isOfType(ModelNode.getClassType()):
                trans.node().setPreserveTransform(ModelNode.PTDropNode)
        deck = np.find('**/=cam=shground')
        if deck:
            deck.setName('deck')
        omits.unstash()

    for np in customGeoms:
        collapse(np.find('**/static'))

    data = HullCache()
    data.root = NodePath('hull')
    data.genericGeoms = genericGeoms
    data.customGeoms = customGeoms
    data.collisions = collisions
    data.locators = locators
    return data


def getAnimBundle(name):
    model = loader.loadModel(name)
    if model:
        return model.find('**/+AnimBundleNode').node().getBundle()
    else:
        return None
    return None


def generateMastCache(mastClass):
    data = MastCache()
    prefix = MastData[mastClass]['prefix']
    height = MastData[mastClass]['maxHeight']
    model_prefix = 'models/char/pir_r_shp_mst_%s' % prefix
    anim_prefix = 'models/char/pir_a_shp_mst_%s_' % prefix
    geom = loader.loadModel(model_prefix).find('**/+Character')
    stripPrefix(geom, 'model:')
    if mastClass == ShipGlobals.Masts.Fore_Multi:
        geom.findAllMatches('**/sail_0*').detach()
        for name in ('_1', '_1_rope', '_2', '_2_rope'):
            for node in geom.findAllMatches('**/boom%s' % name):
                node.setName('boom')

    preFlatten(geom)
    if mastClass in (6, 7, 8, 9, 10):
        for node in geom.findAllMatches('**/sail_0'):
            node.setName('skel_sail_0')

        for node in geom.findAllMatches('**/sail_1'):
            node.setName('skel_sail_1')

        for node in geom.findAllMatches('**/sail_2'):
            node.setName('skel_sail_2')

    for node in geom.findAllMatches('**/sail_0'):
        stripAttribs(node, TextureAttrib)

    for node in geom.findAllMatches('**/sail_1'):
        stripAttribs(node, TextureAttrib)

    for node in geom.findAllMatches('**/sail_2'):
        stripAttribs(node, TextureAttrib)

    geomSet = [
     geom.find('**/lod_high'), geom.find('**/lod_medium'), geom.find('**/lod_low'), geom.find('**/lod_superlow')]
    tex = geomSet[0].find('**/static').findAllTextures('*')[0]
    logic = loader.loadModel(model_prefix + '_logic')
    stripPrefix(logic, 'model:')
    data.collisions = logic.find('**/collisions')
    if not data.collisions.find('**/collision_masts'):
        data.collisions.find('**/collision_mast_0').setName('collision_masts')
    sails = data.collisions.findAllMatches('**/collision_sails')
    for node in sails:
        node.setTag('Sail', '1')

    sails.wrtReparentTo(data.collisions.find('**/collision_masts'))
    geomSet[0].setName('high')
    geomSet[1].setName('med')
    geomSet[2].setName('low')
    geomSet[3].setName('superlow')
    data.charRoot = geom.node()
    data.breakAnim = (
     anim_prefix + 'break', anim_prefix + 'broken')
    data.hitAnim = anim_prefix + 'hit'
    for anim in metaAnims:
        data.metaAnims[anim] = anim_prefix + anim

    geom.findAllMatches('**/rigging_anchors').detach()
    geom.findAllMatches('**/breaks').detach()
    geom.findAllMatches('**/def_mast_base').detach()
    height = MastData[mastClass]['maxHeight']
    matchSet = range(height)
    for i in range(height):
        matchSet = [ x for x in matchSet if x > i ]
        reducedSet = []
        foundReduction = False
        for j in range(len(geomSet)):
            currGeom = geomSet[j].copyTo(NodePath())
            for match in matchSet:
                cruft = currGeom.findAllMatches('**/*_%s*' % match)
                if cruft:
                    cruft.detach()
                    foundReduction = True

            if foundReduction or not matchSet:
                for group in ['static', 'transparent']:
                    for node in currGeom.findAllMatches('**/%s' % group):
                        node.flattenStrong()
                        node.setName(group)

                reducedSet.append(currGeom)

        customSet = []
        for np in reducedSet:
            sails = np.find('**/sails;+s')
            if not sails:
                np.attachNewNode(ModelNode('sails'))
            customSet.append(np.copyTo(NodePath()))

        for np in reducedSet:
            np.find('static').node().setPreserveTransform(ModelNode.PTDropNode)
            np.find('custom').node().setPreserveTransform(ModelNode.PTDropNode)
            np.find('**/sails').node().setPreserveTransform(ModelNode.PTDropNode)
            np.flattenStrong()
            trans = np.findAllMatches('**/transparent')
            if trans:
                for node in trans:
                    node.node().setPreserveTransform(ModelNode.PTDropNode)
                    node.stash()

                stripAttribs(np, TextureAttrib)
                for node in trans:
                    node.unstash()

            else:
                stripAttribs(np, TextureAttrib)

        for np in customSet:
            np.flattenStrong()
            np.find('static').node().setPreserveTransform(ModelNode.PTDropNode)
            np.find('custom').node().setPreserveTransform(ModelNode.PTDropNode)
            np.find('**/sails').node().setPreserveTransform(ModelNode.PTDropNode)
            trans = np.findAllMatches('**/transparent')
            if trans:
                for node in trans:
                    node.node().setPreserveTransform(ModelNode.PTDropNode)
                    node.stash()

                stripAttribs(np, TextureAttrib)
                for node in trans:
                    node.unstash()

        data.genericGeomSets.append(reducedSet)
        data.customGeomSets.append(customSet)

    NodePath(data.charRoot).removeChildren()
    data.collisions.reparentTo(NodePath(data.charRoot))
    return data


def getMastInfo(shipClass, modelClass):
    defs = mastDefs.get(modelClass)
    setup = getMastSetup(shipClass)
    return dict([ (x, [defs[x], setup[x]]) for x in range(len(defs)) if defs[x] ])


def stripPrefix(root, prefix):
    for node in root.findAllMatches('**/%s*' % prefix):
        node.setName(node.getName()[len(prefix):])


def setupWheel():
    global wheel
    model = loader.loadModel('models/shipparts/pir_m_shp_prt_wheel')
    wheel = NodePath('wheelRoot')
    r = model.find('**/+LODNode')
    r.flattenStrong()
    collisions = model.find('**/collisions')
    high = r.find('**/lod_high')
    med = r.find('**/lod_med')
    low = r.find('**/lod_low')
    high.reparentTo(wheel.attachNewNode(ModelNode('high')))
    med.reparentTo(wheel.attachNewNode(ModelNode('med')))
    low.reparentTo(wheel.attachNewNode(ModelNode('low')))
    collisions.reparentTo(wheel)


def getWheel():
    return wheel.copyTo(NodePath())


shipTextures = {}
sailColors = {}
logoTextures = {}

def setupShipTextures():
    global shipTextures
    model = loader.loadModel('models/shipparts/pir_m_shp_text_swap.bam')
    modelQAR = loader.loadModel('models/shipparts/pir_m_shp_text_qar.bam')
    for i in shipStyles:
        if i != ShipGlobals.Styles.QueenAnnesRevenge:
            textures = model.find('**/%s' % shipStyles[i]).findAllTextures('*')
        else:
            textures = modelQAR.find('**/%s' % shipStyles[i]).findAllTextures('*')
        if textures:
            shipTextures[i] = textures[0]

    model = loader.loadModel('models/textureCards/sailColors.bam')
    for style, name in ColorDict.iteritems():
        sailColors[style] = model.find('**/%s' % name).findAllTextures('*')[0]

    model = loader.loadModel('models/textureCards/sailLogo.bam')
    for num, name in LogoDict.iteritems():
        logoTextures[num] = model.find('**/%s' % name).findAllTextures('*')[0]


def getShipTexture(style):
    if shipTextures.get(style):
        return shipTextures.get(style)
    else:
        return shipTextures.get(ShipGlobals.Styles.Player)


def getSailTexture(style):
    return sailColors.get(style, None)


def getLogoTexture(num):
    return logoTextures.get(num, None)