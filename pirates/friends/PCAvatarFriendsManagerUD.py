from direct.directnotify import DirectNotifyGlobal
from otp.friends.AvatarFriendsManagerUD import AvatarFriendsManagerUD

class PCAvatarFriendsManagerUD(AvatarFriendsManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCAvatarFriendsManagerUD')

    def __init__(self, air):
        AvatarFriendsManagerUD.__init__(self, air)