from pirates.piratesbase import PLocalizer

class SiegeManagerBase():
    ANNOUNCER_ZONE = 555

    def __init__(self):
        self._useIslandRegen = False
        self._useRepairSpots = False
        self._useRepairKit = False

    def setUseIslandRegen(self, useIslandRegen):
        if self._useIslandRegen and not useIslandRegen:
            self._disableUseIslandRegen()
        elif not self._useIslandRegen and useIslandRegen:
            self._enableUseIslandRegen()
        self._useIslandRegen = useIslandRegen

    def _enableUseIslandRegen(self):
        messenger.send(self.getUseIslandRegenEvent(), [True])

    def _disableUseIslandRegen(self):
        messenger.send(self.getUseIslandRegenEvent(), [False])

    def getUseIslandRegenEvent(self):
        return 'useIslandRegen-%s' % self.doId

    def getUseIslandRegen(self):
        return self._useIslandRegen

    def setUseRepairSpots(self, useRepairSpots):
        if self._useRepairSpots and not useRepairSpots:
            self._disableRepairSpots()
        elif not self._useRepairSpots and useRepairSpots:
            self._enableRepairSpots()
        self._useRepairSpots = useRepairSpots

    def _enableRepairSpots(self):
        messenger.send(self.getUseRepairSpotsEvent(), [True])

    def _disableRepairSpots(self):
        messenger.send(self.getUseRepairSpotsEvent(), [False])

    def getUseRepairSpotsEvent(self):
        return 'useRepairSpots-%s' % self.doId

    def getUseRepairSpots(self):
        return self._useRepairSpots

    def setUseRepairKit(self, useRepairKit):
        if self._useRepairKit and not useRepairKit:
            self._disableRepairKit()
        elif not self._useRepairKit and useRepairKit:
            self._enableRepairKit()
        self._useRepairKit = useRepairKit

    def _enableRepairKit(self):
        messenger.send(self.getUseRepairKitEvent(), [True])

    def _disableRepairKit(self):
        messenger.send(self.getUseRepairKitEvent(), [False])

    def getUseRepairKitEvent(self):
        return 'useRepairKit-%s' % self.doId

    def getUseRepairKit(self):
        return self._useRepairKit