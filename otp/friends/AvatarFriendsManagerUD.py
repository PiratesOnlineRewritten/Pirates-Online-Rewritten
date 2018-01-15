from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class AvatarFriendsManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarFriendsManagerUD')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.notify.info('%s is going online' % self.__class__.__name__)

    def requestInvite(self, todo0):
        pass

    def friendConsidering(self, todo0):
        pass

    def invitationFrom(self, todo0, todo1):
        pass

    def retractInvite(self, todo0):
        pass

    def rejectInvite(self, todo0, todo1):
        pass

    def requestRemove(self, todo0):
        pass

    def rejectRemove(self, todo0, todo1):
        pass

    def updateAvatarFriend(self, todo0, todo1):
        pass

    def removeAvatarFriend(self, todo0):
        pass

    def updateAvatarName(self, todo0, todo1):
        pass

    def avatarOnline(self, todo0, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def avatarOffline(self, todo0):
        pass