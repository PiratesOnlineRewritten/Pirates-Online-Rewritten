from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectOV
from pirates.ship import ShipGlobals
from pirates.battle.Teamable import Teamable
from pirates.ship import ShipUpgradeGlobals
from pirates.ship import ShipGlobals

class DistributedPlayerSimpleShipOV(DistributedObjectOV.DistributedObjectOV, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerSimpleShipOV')

    def __init__(self, cr):
        DistributedObjectOV.DistributedObjectOV.__init__(self, cr)
        Teamable.__init__(self)
        self.shipClass = 0
        self.maxHp = 0
        self.Hp = 0
        self.deltaHp = 0
        self.maxSp = 0
        self.Sp = 0
        self.deltaSp = 0
        self.cargo = []
        self.maxCargo = 0
        self.crew = []
        self.mastStates = [0, 0, 0, 0, 0]
        self.armorStates = [0, 0, 0]
        self.healthState = 0.0
        self.crewCount = 0
        self.state = 'Off'
        self.timerTime = 0
        self.timerTimestamp = 0
        self.customHull = 0
        self.customRigging = 0
        self.customSailPattern = 0
        self.customSailLogo = 0
        self.customProw = 0
        self.customCannon = 0

    def __repr__(self):
        return 'DistributedPlayerSimpleShipOV(%s)' % self.doId

    def announceGenerate(self):
        DistributedObjectOV.DistributedObjectOV.announceGenerate(self)
        messenger.send('DistributedShipOV-announceGenerate', sentArgs=[self.doId])
        self.updateLocalHealth()

    def updateLocalHealth(self):
        self.mastHealth = [ x[0] * (x[1] / 100.0) for x in zip(self.maxMastHealth, self.mastStates) ]
        self.armor = [ x[0] * (x[1] / 100.0) for x in zip(self.maxArmor, self.armorStates) ]
        self.Hp = self.maxHp * (self.healthState / 100.0)
        self.Sp = sum(self.mastHealth)
        messenger.send('setShipHp-%s' % self.getDoId(), [self.Hp, self.maxHp])
        messenger.send('setShipSp-%s' % self.getDoId(), [self.Sp, self.maxSp])

    def setShipUpfitList(self, dataList):
        counter = 0
        while dataList:
            newData = dataList[0]
            dataList = dataList[1:]
            if counter == 0:
                self.customHull = newData
            elif counter == 1:
                self.customRigging = newData
            elif counter == 2:
                self.customSailPattern = newData
            elif counter == 3:
                self.customSailLogo = newData
            counter += 1

        if self.customHull:
            self.loadStats()
        messenger.send('ShipChanged-%s' % self.doId)

    def delete(self):
        DistributedObjectOV.DistributedObjectOV.delete(self)
        messenger.send('DistributedShipOV-delete', sentArgs=[self.doId])

    def loadStats(self):
        self.stats = ShipGlobals.getShipConfig(self.shipClass)
        self.maxHp = self.stats['hp']
        self.maxSp = self.stats['sp']
        self.maxMastHealth = ShipGlobals.getMastHealth(self.shipClass, self.maxSp)
        self.maxArmor = ShipGlobals.getHullArmor(self.modelClass)
        self.maxHp = int(self.maxHp * ShipUpgradeGlobals.HULL_TYPES[self.customHull]['Armor'])
        self.Hp = self.maxHp * (self.healthState / 100.0)
        self.maxCrew = self.stats['maxCrew']
        self.acceleration = self.stats['acceleration']
        self.maxSpeed = self.stats['maxSpeed']
        self.reverseAcceleration = self.stats['reverseAcceleration']
        self.maxReverseSpeed = self.stats['maxReverseSpeed']
        self.turnRate = self.stats['turn']
        self.maxTurn = self.stats['maxTurn']
        shipTypeInfo = ShipGlobals.getShipConfig(self.shipClass)
        self.maxCargo = int(shipTypeInfo['maxCargo'] * ShipUpgradeGlobals.HULL_TYPES[self.customHull]['Cargo'])
        self.cannonConfig = self.stats['cannons']
        self.lBroadsideConfig = self.stats['leftBroadsides']
        self.rBroadsideConfig = self.stats['rightBroadsides']

    def setName(self, name):
        self.name = name
        messenger.send('setName-%s' % self.getDoId(), [self.name, self.getTeam()])

    def setShipClass(self, shipClass):
        self.shipClass = shipClass
        messenger.send('setShipClass-%s' % self.getDoId(), [self.shipClass])
        self.modelClass = ShipGlobals.getModelClass(shipClass)
        self.loadStats()

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def setCrew(self, crewArray):
        if self.crew != crewArray:
            messenger.send('setShipCrew-%s' % self.getDoId(), [crewArray, self.maxCrew])
        self.crew = crewArray
        self.crewCount = len(self.crew)

    def setCargo(self, cargo):
        self.cargo = cargo
        shipTypeInfo = ShipGlobals.getShipConfig(self.shipClass)
        maxCargo = int(shipTypeInfo['maxCargo'] * ShipUpgradeGlobals.HULL_TYPES[self.customHull]['Cargo'])
        messenger.send('setShipCargo-%s' % self.getDoId(), [self.cargo, maxCargo])

    def setGameState(self, stateName, avId, timeStamp, localChange=0):
        self.state = stateName
        messenger.send('setState-%s' % self.getDoId(), [self.state])
        if self.state in ('Off', ) and self.getDoId() == localAvatar.getActiveShipId():
            localAvatar.b_setActiveShipId(0)

    def setTimer(self, time, timestamp):
        elapsedTime = globalClockDelta.localElapsedTime(timestamp)
        localTime = globalClock.getFrameTime()
        self.timerTimestamp = localTime - elapsedTime
        self.timerTime = time
        messenger.send('setShipTimer-%s' % self.getDoId(), [self.getTimeLeft()])

    def getTimeLeft(self):
        timePassed = globalClock.getFrameTime() - self.timerTimestamp
        return max(0, self.timerTime - timePassed)

    def setMastStates(self, mainMast1, mainMast2, mainMast3, aftMast, foreMast):
        self.mastStates = [
         mainMast1, mainMast2, mainMast3, aftMast, foreMast]
        self.updateLocalHealth()

    def setArmorStates(self, rear, left, right):
        self.armorStates = [
         rear, left, right]

    def setHealthState(self, health):
        self.healthState = health
        self.updateLocalHealth()