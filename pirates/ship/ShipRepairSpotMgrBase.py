from direct.fsm.StatePush import AttrSetter, FunctionCall, StateVar
from pirates.pvp import PVPGlobals

class ShipRepairSpotMgrBase():

    def __init__(self):
        self._state = DestructiveScratchPad(health=StateVar(0), speed=StateVar(0), armor=StateVar(0), modelClass=StateVar(0), pvpTeam=StateVar(0), siegeTeam=StateVar(0), fullHealth=StateVar(False), willBeFullHealth=StateVar(False), validShipClass=StateVar(False), hasTeam=StateVar(False))
        self._statePushes = []

    def destroy(self):
        for statePush in self._statePushes:
            statePush.destroy()

        del self._statePushes
        self._state.destroy()

    def _onShipReady(self):
        self._statePushes.extend([
         FunctionCall(self._evalFullHealth, self._state.health, self._state.speed, self._state.armor, self._state.willBeFullHealth).pushCurrentState(), FunctionCall(self._evalValidShipClass, self._state.modelClass).pushCurrentState(), FunctionCall(self._evalHasTeam, self._state.pvpTeam, self._state.siegeTeam).pushCurrentState()])

    def updateHealth(self, health):
        self._state.health.set(health)

    def updateSpeed(self, speed):
        self._state.speed.set(speed)

    def updateArmor(self, armor):
        self._state.armor.set(armor)

    def updateWillBeFullHealth(self, willBeFullHealth):
        self._state.willBeFullHealth.set(willBeFullHealth)

    def updateShipClass(self, modelClass):
        self._state.modelClass.set(modelClass)

    def updatePVPTeam(self, team):
        self._state.pvpTeam.set(team)

    def updateSiegeTeam(self, team):
        self._state.siegeTeam.set(team)

    def _evalFullHealth(self, health, speed, armor, willBeFullHealth):
        self._state.fullHealth.set(willBeFullHealth or health > 99.9 and speed > 99.9 and armor > 99.9)

    def _evalValidShipClass(self, modelClass):
        self._state.validShipClass.set(modelClass in PVPGlobals.ShipClass2repairLocators)

    def _evalHasTeam(self, pvpTeam, siegeTeam):
        self._state.hasTeam.set(pvpTeam or siegeTeam)