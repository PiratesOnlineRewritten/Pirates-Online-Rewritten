from pirates.uberdog.InventoryRequestBase import InventoryRequestBase
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.world import GameTypeGlobals

class InventoryRequestGameType(InventoryRequestBase):

    def __init__(self):
        InventoryRequestBase.__init__(self)

    def getGameStyles(self, gameType, callback=None):
        self._getGameInfo(True, gameType, callback=callback)

    def getGameOptions(self, gameType, gameStyle=None, callback=None):
        self._getGameInfo(False, gameType, gameStyle, callback)

    def _getGameInfo(self, styles, gameType, gameStyle=None, callback=None):

        def gotGameInfo(info):
            requestId = DistributedInventoryBase.getLastInventoryRequestId()
            if requestId in self.myInventoryRequests:
                self.myInventoryRequests.remove(requestId)
            if callback:
                callback(info)

        if styles:
            inventoryRequestId, styles = GameTypeGlobals.getGameStyles(gameType, gameStyle, callback=gotGameInfo)
        else:
            inventoryRequestId, options = GameTypeGlobals.getGameOptions(gameType, gameStyle, callback=gotGameInfo)
        if inventoryRequestId != None:
            self.myInventoryRequests.append(inventoryRequestId)
        return