from otp.avatar.Avatar import Avatar
from pirates.pirate import AvatarTypes

class JackSparrow(Avatar):

    def __init__(self):
        Avatar.__init__(self)
        self.avatarType = AvatarTypes.JackSparrow
        self.loadModel('models/char/js_2000')
        self.setName(self.avatarType.getName())
        self.setNameVisible(0)

    def delete(self):
        loader.unloadModel('models/char/js_2000')
        Avatar.delete(self)


class WillTurner(Avatar):

    def __init__(self):
        Avatar.__init__(self)
        self.avatarType = AvatarTypes.WillTurner
        self.loadModel('models/char/wt_2000')
        self.setName(self.avatarType.getName())
        self.setNameVisible(0)

    def delete(self):
        loader.unloadModel('models/char/wt_2000')
        Avatar.delete(self)


class ElizabethSwan(Avatar):

    def __init__(self):
        Avatar.__init__(self)
        self.avatarType = AvatarTypes.ElizabethSwan
        self.loadModel('models/char/es_2000')
        self.setName(self.avatarType.getName())
        self.setNameVisible(0)

    def delete(self):
        loader.unloadModel('models/char/es_2000')
        Avatar.delete(self)


class CaptBarbossa(Avatar):

    def __init__(self):
        Avatar.__init__(self)
        self.avatarType = AvatarTypes.CaptBarbossa
        self.loadModel('models/char/cb_2000')
        self.setName(self.avatarType.getName())
        self.setNameVisible(0)

    def delete(self):
        loader.unloadModel('models/char/cb_2000')
        Avatar.delete(self)


class TiaDalma(Avatar):

    def __init__(self):
        Avatar.__init__(self)
        self.avatarType = AvatarTypes.TiaDalma
        self.loadModel('models/char/td_2000')
        self.setName(self.avatarType.getName())
        self.setNameVisible(0)

    def delete(self):
        loader.unloadModel('models/char/td_2000')
        Avatar.delete(self)


class JoshGibbs(Avatar):

    def __init__(self):
        Avatar.__init__(self)
        self.avatarType = AvatarTypes.JoshameeGibbs
        self.loadModel('models/char/jg_2000')
        self.setName(self.avatarType.getName())
        self.setNameVisible(0)

    def delete(self):
        loader.unloadModel('models/char/jg_2000')
        Avatar.delete(self)


class JollyRoger(Avatar):

    def __init__(self):
        Avatar.__init__(self)
        self.avatarType = AvatarTypes.JollyRoger
        self.loadModel('models/char/jr_2000')
        self.setName(self.avatarType.getName())
        self.setNameVisible(0)

    def delete(self):
        loader.unloadModel('models/char/jr_2000')
        Avatar.delete(self)