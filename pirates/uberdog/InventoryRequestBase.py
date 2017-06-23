from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase

class InventoryRequestBase():

    def __init__(self):
        self.myInventoryRequests = []

    def __del__(self):
        self.cancelAllInventoryRequests()

    def getInventory(self, inventoryId, callback, timeout=30):

        def gotInventory(inventory):
            requestId = DistributedInventoryBase.getLastInventoryRequestId()
            if requestId in self.myInventoryRequests:
                self.myInventoryRequests.remove(requestId)
            if callback:
                callback(inventory)

        requestId = DistributedInventoryBase.getInventory(inventoryId, gotInventory, timeout)
        if requestId:
            self.myInventoryRequests.append(requestId)
        return requestId

    def cancelGetInventory(self, requestId):
        if requestId in self.myInventoryRequests:
            self.myInventoryRequests.remove(requestId)
            DistributedInventoryBase.cancelGetInventory(requestId)
            return True
        return False

    def cancelAllInventoryRequests(self):
        canceled = False
        for currRequest in self.myInventoryRequests:
            DistributedInventoryBase.cancelGetInventory(currRequest)
            canceled = True

        self.myInventoryRequests = []
        return canceled