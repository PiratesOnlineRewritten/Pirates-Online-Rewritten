from direct.distributed import DistributedObjectGlobal

class DistributedMatchMaker(DistributedObjectGlobal.DistributedObjectGlobal):
    notify = directNotify.newCategory('DistributedMatchMaker')

    def __init__(self, cr):
        DistributedObjectGlobal.DistributedObjectGlobal.__init__(self, cr)

    def requestActivity(self, gameType, gameCategory=-1, options=[], shipIds=[]):
        self.notify.debug('requestActivity...')
        self.sendUpdate('requestActivity', [gameType, gameCategory, options, shipIds])

    def requestJoin(self, matchId):
        self.notify.debug('requestJoin...')
        self.sendUpdate('requestJoin', [matchId])

    def skipJoin(self, matchId, clearSearch=False):
        self.notify.debug('skipJoin %s %s...' % (matchId, clearSearch))
        self.sendUpdate('skipJoin', [matchId, clearSearch])

    def cancelRequest(self, matchId):
        self.sendUpdate('cancelRequest', [matchId])