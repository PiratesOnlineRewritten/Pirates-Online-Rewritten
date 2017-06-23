from direct.task import Task

class UniqueIdManager():

    def __init__(self, repository, instance=None):
        self.instance = instance
        self.repository = repository
        self.uid2doId = {}
        self.uid2obj = {}
        self.uidCallbacks = {}

    def __str__(self):
        if self.instance == None:
            return 'No instance set'
        outStr = 'uidMgr for %d : %s\n' % (self.instance.doId, self.instance.getUniqueId())
        outStr += '-' * 50
        outStr += '\n'
        for uid in self.uid2doId:
            doId = self.uid2doId.get(uid, 0)
            obj = self.instance.air.doId2do.get(doId)
            if obj:
                obj = obj.__class__.__name__
            outStr += '%-22s : %d : %s\n' % (uid, doId, obj)

        return outStr

    def destroy(self):
        self.reset()
        self.instance = None
        self.repository = None
        return

    def reset(self):
        for currUid in self.uid2doId.keys():
            taskMgr.remove('uidCallback-' + currUid)

        self.uid2doId = {}
        self.uid2obj = {}
        self.uidCallbacks = {}

    def removeUid(self, uid, checkParents=True):
        if self.instance and checkParents:
            parentInstance = self.instance.getParentInstance()
            if parentInstance:
                parentInstance.uidMgr.removeUid(uid)
                return
        if self.uid2doId.has_key(uid):
            del self.uid2doId[uid]
        if self.uidCallbacks.has_key(uid):
            del self.uidCallbacks[uid]
        if self.instance:
            subInstances = self.instance.getSubInstances()
            for currSubInstance in subInstances:
                currSubInstance.uidMgr.removeUid(uid, checkParents=False)

    def addUid(self, uid, objId):
        if uid != '':
            self.uid2doId[uid] = objId
            taskMgr.doMethodLater(0.1, self._requestUidCallbackLater, 'uidCallback-' + uid, extraArgs=[uid, objId])

    def getDoId(self, uid, deep=True):
        doId = self.uid2doId.get(uid)
        if doId != None:
            return doId
        elif deep:
            if self.instance:
                subInstances = self.instance.getSubInstances()
                for currSubInstance in subInstances:
                    doId = currSubInstance.uidMgr.getDoId(uid)
                    if doId != None:
                        return doId

        else:
            return
        return

    def getDo(self, uid, deep=True):
        return self.repository.getDo(self.getDoId(uid, deep))

    def addUidCallback(self, uid, callback, timeout=None, onlyOnce=True):
        objDoId = self.uid2doId.get(uid)
        obj = self.repository.doId2do.get(objDoId)
        if objDoId:
            if obj and (obj.isGenerated() or timeout == 0):
                callback(objDoId)
                return True
            else:
                taskMgr.doMethodLater(0.1, self._requestUidCallbackLater, 'uidCallback-' + uid, extraArgs=[uid, objDoId])
        elif self.instance:
            subInstances = self.instance.getSubInstances()
            for currSubInstance in subInstances:
                result = currSubInstance.uidMgr.addUidCallback(uid, callback, timeout, onlyOnce)
                if result:
                    return result

        if timeout == 0:
            callback(objDoId)
            return True
        else:
            if not self.uidCallbacks.get(uid):
                self.uidCallbacks[uid] = []
            self.uidCallbacks[uid].append([callback, onlyOnce])
            return False

    def removeUidCallback(self, uid, callback):
        if self.uidCallbacks.has_key(uid):
            callbacks = self.uidCallbacks[uid][:]
            for currCallback in callbacks:
                if callback == currCallback[0]:
                    self.uidCallbacks[uid].remove(currCallback)

            if len(self.uidCallbacks[uid]) == 0:
                del self.uidCallbacks[uid]

    def _requestUidCallbackLater(self, uid, objId):
        object = self.repository.doId2do.get(objId)
        if object == None:
            return Task.done
        if object.isGenerated() == False:
            return Task.again
        self._requestUidCallback(uid, objId)
        return Task.done

    def _requestUidCallback(self, uid, objId=None, checkParents=True, objInstance=None):
        if objId == None:
            objId = self.uid2doId.get(uid)
        if objId and objInstance == None:
            objInstance = self
        if self.instance:
            parentInstance = self.instance.getParentInstance()
            if parentInstance and checkParents:
                parentInstance.uidMgr._requestUidCallback(uid, objId, checkParents=checkParents, objInstance=objInstance)
                return
        if objId and self.uidCallbacks.has_key(uid):
            callbacks = self.uidCallbacks[uid][:]
            for currCallback in callbacks:
                currCallback[0](objId)
                if currCallback[1]:
                    self.uidCallbacks[uid].remove(currCallback)

            if len(self.uidCallbacks[uid]) == 0:
                del self.uidCallbacks[uid]
        if self.instance:
            subInstances = self.instance.getSubInstances()
            for currSubInstance in subInstances:
                currSubInstance.uidMgr._requestUidCallback(uid, objId, checkParents=False, objInstance=objInstance)

        return

    def removeUidObj(self, uid):
        self.uid2obj.pop(uid, None)
        return

    def addUidObj(self, uid, obj):
        self.uid2obj[uid] = obj

    def getUidObj(self, uid):
        return self.uid2obj.get(uid)

    def justGetMeMeObject(self, uid, asyncCallback=None):
        obj = self.getUidObj(uid)
        if obj:
            return obj
        if asyncCallback:
            self.addUidCallback(uid, asyncCallback)
        else:
            objDoId = self.getDoId(uid)
            obj = self.repository.doId2do.get(objDoId)
        return obj