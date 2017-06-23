from direct.fsm.StatePush import FunctionCall, StateVar
from pirates.pvp import PVPGlobals
from pirates.ship.ShipRepairSpotMgrBase import ShipRepairSpotMgrBase

class ShipRepairSpotMgr(ShipRepairSpotMgrBase):

    def __init__(self, cr, shipId=None):
        ShipRepairSpotMgrBase.__init__(self)
        self.cr = cr
        self._state.add(needModels=StateVar(False), needHoles=StateVar(False))
        self.setShipId(shipId)

    def setShipId(self, shipId):
        self._ship = self.cr.doId2do.get(shipId, None)
        if self._ship:
            self._onShipReady()
        return

    def destroy(self):
        self._state.needHoles.set(False)
        self._state.needModels.set(False)
        ShipRepairSpotMgrBase.destroy(self)
        del self._ship
        del self.cr

    def _onShipReady(self):
        ShipRepairSpotMgrBase._onShipReady(self)
        self._statePushes.extend([FunctionCall(self._evalNeedModels, self._state.validShipClass, self._state.hasTeam).pushCurrentState(), FunctionCall(self._evalNeedHoles, self._state.fullHealth, self._state.needModels).pushCurrentState(), FunctionCall(self._needModelsChanged, self._state.needModels).pushCurrentState(), FunctionCall(self._needHolesChanged, self._state.needHoles).pushCurrentState(),
         FunctionCall(self._handleRepairSpotIndicesChanged, PVPGlobals.ShipClass2repairLocators[self._ship.modelClass]).pushCurrentState()])

    def _evalNeedModels(self, validShipClass, hasTeam):
        if base.config.GetBool('want-repair-game', 0):
            self._state.needModels.set(validShipClass)
        else:
            self._state.needModels.set(validShipClass and hasTeam)

    def _evalNeedHoles(self, fullHealth, needModels):
        self._state.needHoles.set(needModels and not fullHealth)

    def _needModelsChanged(self, needModels):
        if needModels:
            self._ship._addRepairSpotModels()
        else:
            self._ship._removeRepairSpotModels()

    def _needHolesChanged(self, needHoles):
        if needHoles:
            self._ship._addRepairSpotHoles()
        else:
            self._ship._removeRepairSpotHoles()

    def _handleRepairSpotIndicesChanged(self, indices):
        if self._state.needModels.get():
            self._state.needModels.set(False)
            self._state.needModels.set(True)