from direct.distributed.DistributedObjectOV import DistributedObjectOV
from pirates.teleport.DistributedFSMBase import DistributedFSMBase

class DistributedFSMOV(DistributedObjectOV, DistributedFSMBase):

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, air, name='DistributedFSMOV'):
        DistributedFSMBase.__init__(self, name)
        DistributedObjectOV.__init__(self, air)
        self.__requestContext = 0
        self._requests = {}
        self.obj = None
        return

    def __repr__(self):
        return '%s (%s)' % (DistributedFSMBase.__repr__(self), self.doId)

    def getObj(self):
        if not self.obj:
            self.obj = self.cr.getDo(self.doId)
        return self.obj

    @report(types=['args'], dConfigParam=['dteleport'])
    def _incrementRequestContext(self):
        self.__requestContext += 1
        if self.__requestContext == 256:
            self.__requestContext = 1
        return self.__requestContext

    @report(types=['args'], dConfigParam=['dteleport'])
    def fsmRequestResponse(self, requestContext, reason):
        state, args, callback = self._requests.pop(requestContext, ('', (), None))
        if callback:
            callback(reason, state, *args)
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def d_fsmRequestResponse(self, requestContext, reason):
        self.sendUpdate('fsmRequestResponse', [requestContext, reason])

    @report(types=['args'], dConfigParam=['dteleport'])
    def b_requestFSMState(self, callback, state, *args):
        if callback:
            requestContext = self._incrementRequestContext()
            self._requests[requestContext] = (state, args, callback)
        else:
            requestContext = 0
        self.d_requestFSMState(requestContext, state, *args)

    @report(types=['args'], dConfigParam=['dteleport'])
    def d_requestFSMState(self, requestContext, state, *args):
        self.sendUpdate('requestFSMState', [requestContext, [(state,) + args]])

    @report(types=['args'], dConfigParam=['dteleport'])
    def setFSMState(self, stateContext, stateData):
        stateData = stateData[0]
        state = stateData[0]
        args = stateData[1:]
        return self.request(state, *args)