from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from pirates.mockup import PythonNodePath
from pirates.effects import DynamicLight
from pirates.creature import Creature
from pirates.creature.Alligator import Alligator
from pirates.creature.Bat import Bat
from pirates.creature.Chicken import Chicken
from pirates.creature.Crab import Crab
from pirates.creature.Dog import Dog
from pirates.creature.FlyTrap import FlyTrap
from pirates.creature.Monkey import Monkey
from pirates.creature.Pig import Pig
from pirates.creature.Rooster import Rooster
from pirates.creature.Scorpion import Scorpion
from pirates.creature.Seagull import Seagull
from pirates.creature.Raven import Raven
from pirates.creature.Stump import Stump
from pirates.creature.Wasp import Wasp
from pirates.npc import BomberZombie
from pirates.battle import EnemyGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import AvatarTypes
from pirates.ship import ShipGlobals
from pirates.effects import SoundFX
from pirates.effects import AmbientSoundFX
from pirates.effects import CausticsProjector
from pirates.effects import ExplodingBarrel
from pirates.world import WorldGlobals
from pirates.piratesbase import PLocalizerEnglish
LOD_STATE_NORMAL = 0
LOD_STATE_HIGH = 1
LOD_STATE_LOW = 2
LOD_STATE_LOWEST = 3
LOD_STATE_MED = 4
flickerTracks = []

def LightDynamic(levelObj, parent=render, drawIcon=True, modular=False):
    if levelObj is None:
        levelObj = WorldGlobals.LevelObject('', {})
    color = None
    if levelObj.data.has_key('Visual'):
        if levelObj.data['Visual'].has_key('Color'):
            color = levelObj.data['Visual']['Color']
    attenuation = None
    if levelObj.data.has_key('Attenuation'):
        quadAtten = float(levelObj.data['Attenuation'])
    else:
        quadAtten = 0
    if levelObj.data.has_key('QuadraticAttenuation'):
        quadAtten = float(levelObj.data['QuadraticAttenuation'])
        quadAtten = quadAtten * quadAtten / 100.0
    if levelObj.data.has_key('ConstantAttenuation'):
        constantAtten = float(levelObj.data['ConstantAttenuation'])
    else:
        constantAtten = 1
    if levelObj.data.has_key('LinearAttenuation'):
        linearAtten = float(levelObj.data['LinearAttenuation'])
    else:
        linearAtten = 0
    attenuation = (constantAtten, linearAtten, quadAtten)
    intensity = None
    if levelObj.data.has_key('Intensity'):
        intensity = float(levelObj.data['Intensity'])
    coneAngle = None
    dropOff = None
    if levelObj.data.has_key('ConeAngle'):
        coneAngle = float(levelObj.data['ConeAngle'])
        if coneAngle == 0.0:
            levelObj.data['ConeAngle'] = '60.0'
            coneAngle = 60.0
    if levelObj.data.has_key('DropOff'):
        dropOff = float(levelObj.data['DropOff'])
    exponent = None
    flickering = False
    if not modular or config.GetBool('allow-cave-flicker', 0):
        if levelObj.data.get('Flickering', False):
            flickering = True
        flickRate = 1.0
        if levelObj.data.has_key('FlickRate'):
            flickRate = float(levelObj.data['FlickRate'])
    lightType = DynamicLight.DYN_LIGHT_POINT
    if levelObj.data.has_key('LightType'):
        typeString = levelObj.data['LightType']
        if typeString == 'AMBIENT':
            lightType = DynamicLight.DYN_LIGHT_AMBIENT
        elif typeString == 'DIRECTIONAL':
            lightType = DynamicLight.DYN_LIGHT_DIRECTIONAL
        elif typeString == 'SPOT':
            lightType = DynamicLight.DYN_LIGHT_SPOT
    light = DynamicLight.DynamicLight(type=lightType, parent=parent, pos=levelObj.transform.getPos(), hpr=levelObj.transform.getHpr(), color=color, atten=attenuation, exp=exponent, flicker=flickering, drawIcon=drawIcon, modular=modular)
    if not modular:
        light.turnOff()
    if intensity:
        light.setIntensity(intensity)
    if coneAngle:
        light.setConeAngle(coneAngle)
    if dropOff:
        light.setDropOff(dropOff)
    if not modular or config.GetBool('allow-cave-flicker', 0):
        light.setFlickRate(flickRate)
    if not modular:
        light.turnOn()
        if hasattr(base, 'pe'):
            base.pe.dynamicLights.append(light)
    return light


def LightModular(levelObj, parent=render, drawIcon=True):
    return LightDynamic(levelObj, parent, drawIcon, modular=True)


def CreateBomberZombie():
    bZombie = BomberZombie.BomberZombie()
    bZombie.barrel = ExplodingBarrel.ExplodingBarrel()
    lodNode = bZombie.barrel.find('**/+LODNode').node()
    lodNode.setSwitch(0, 50000, 0)
    lodNode.setSwitch(1, 50003, 50001)
    bZombie.barrel.reparentTo(bZombie.leftHandNode)
    bZombie.barrel.setScale(0.88)
    bZombie.barrel.lightUp()
    return bZombie


def CreateAnimal(species=None):
    if not species:
        species = 'Pig'
    exec 'animal = %s()' % species
    animal.setAvatarType(eval('AvatarTypes.%s' % species))
    return animal


CREATURE_CLASS_DICT = {'Crab': 'Crab','Stone Crab': 'Crab','Rock Crab': 'Crab','Giant Crab': 'Crab','Devourer Crab': 'Crab','FlyTrap': 'FlyTrap','Rancid FlyTrap': 'FlyTrap','Ancient FlyTrap': 'FlyTrap','Stump': 'Stump','Twisted Stump': 'Stump','Alligator': 'Alligator','Bayou Gator': 'Alligator','Huge Gator': 'Alligator','Big Gator': 'Alligator','Bat': 'Bat','Rabid Bat': 'Bat','Vampire Bat': 'Bat','Fire Bat': 'Bat','Wasp': 'Wasp','Killer Wasp': 'Wasp','Angry Wasp': 'Wasp','Soldier Wasp': 'Wasp','Scorpion': 'Scorpion','Dire Scorpion': 'Scorpion','Dread Scorpion': 'Scorpion'}

def CreateCreature(species=None):
    if not species:
        species = 'Crab'
    exec 'creature = %s()' % CREATURE_CLASS_DICT[species]
    creature.show()
    avatarTypeFunc = AvatarTypes.NPC_SPAWNABLES[species][AvatarTypes.AVATAR_TYPE_IDX]
    avatarType = avatarTypeFunc()
    creature.height = EnemyGlobals.getHeight(avatarType)
    baseStats = EnemyGlobals.getBaseStats(avatarType)
    enemyScale = EnemyGlobals.getEnemyScaleByType(avatarType, baseStats[1])
    creature.height *= enemyScale
    creature.setAvatarScale(enemyScale)
    creature.setAvatarType(avatarType)
    return creature


def CreateEffectProjector(type='CausticsProjector', drawIcon=True):
    projector = None
    if type == 'CausticsProjector':
        projector = CausticsProjector.CausticsProjector()
        projector.enableEffect()
    if drawIcon and projector:
        newModel = loader.loadModel('models/misc/smiley')
        newModel.setColor(0, 0.65, 0, 1)
        newModel.reparentTo(projector)
    return projector


def CreateSFX(sfxFile=None, volume=0.5, looping=True, delayMin=0, delayMax=0, pos=None, hpr=None, parent=None, drawIcon=True):
    soundFX = SoundFX.SoundFX(sfxFile=sfxFile, volume=volume, looping=looping, delayMin=delayMin, delayMax=delayMax, pos=pos, hpr=hpr, parent=parent, listenerNode=base.cam, drawIcon=drawIcon)
    return soundFX


def CreateAmbientSFX(pos=None, parent=None):
    soundFX = AmbientSoundFX.AmbientSoundFX()
    return soundFX


def CreateEntity(entityType, objData=None, parent=None):
    newEntity = entityType()
    if parent:
        newEntity.reparentTo(parent)
    if objData:
        properties = objData.get('properties')
        if properties:
            for key in properties:
                newEntity.setProperty(key, properties[key])

    return newEntity


GREETING_ANIMATIONS = [
 '', 'emote_wave', 'emote_wink', 'emote_clap', 'emote_yawn', 'emote_smile', 'emote_no', 'emote_yes', 'attention', 'emote_flex', 'emote_fear', 'emote_sad', 'crazy_ned_day_interact']

class ShipNP(NodePath):

    def __init__(self, shipObj):
        NodePath.__init__(self, 'ShipModel')
        self.shipObj = shipObj
        self.shipObj.setOwner(self)
        self.shipObj.manufactureCannons()


def getShipEnumerations():
    enums = []
    shipClasses = ShipGlobals.__shipConfigs.keys()
    shipClasses.sort()
    for shipClass in shipClasses:
        shipStr = str(shipClass) + ': ' + PLocalizerEnglish.ShipClassNames[shipClass]
        enums.append(shipStr)

    return enums


def getStyleEnumerations():
    styleInfo = PLocalizerEnglish.ShipStyleNames
    styles = styleInfo.keys()
    styles.sort()
    return [
     '-1: Default'] + [ str(x) + ': ' + styleInfo[x] for x in styles ]


def getLogoEnumerations():
    logoInfo = PLocalizerEnglish.ShipLogoNames
    logos = logoInfo.keys()
    logos.sort()
    return [
     '-1: Default'] + [ str(x) + ': ' + logoInfo[x] for x in logos ]


def getShipInfo(objectData):
    if ':' in objectData['Category']:
        shipClass = int(objectData['Category'].split(':')[0])
    else:
        typeStr = objectData['Category']
        level = objectData.get('Level')
        if level:
            level = int(level)
        teamStr = 'Player'
        specifiedTeam = objectData.get('Team')
        if specifiedTeam:
            teamStr = specifiedTeam
        teamId = PiratesGlobals.teamStr2TeamId(teamStr)
        shipClass = ShipGlobals.WARSHIPL3
        newShipClass = None
        if hasattr(ShipGlobals, typeStr):
            newShipClass = eval('ShipGlobals.' + typeStr)
        if newShipClass:
            shipClass = newShipClass
        elif typeStr == 'NavyMerchant' or typeStr == 'Merchant' and teamId and teamId == PiratesGlobals.NAVY_TEAM:
            shipClass = ShipGlobals.NAVY_VANGUARD
        elif typeStr == 'Merchant':
            shipClass = ShipGlobals.MERCHANTL2
        elif typeStr == 'Interceptor':
            if level == 2:
                shipClass = ShipGlobals.INTERCEPTORL2
            elif level == 3:
                shipClass = ShipGlobals.INTERCEPTORL3
            else:
                shipClass = ShipGlobals.INTERCEPTORL1
        elif typeStr == 'InterceptorTutorial':
            shipClass = ShipGlobals.STUMPY_SHIP
        elif typeStr == 'TutorialEnemyShip':
            shipClass = ShipGlobals.SKEL_SHADOW_CROW_FR
    style = objectData.get('StyleOverride', '%s:Default' % ShipGlobals.Styles.Undefined)
    logo = objectData.get('LogoOverride', '%s:Default' % ShipGlobals.Logos.Undefined)
    style = int(style.split(':')[0])
    logo = int(logo.split(':')[0])
    return (
     shipClass, style, logo)