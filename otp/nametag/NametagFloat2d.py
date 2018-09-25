from otp.nametag.Nametag3d import Nametag3d


class NametagFloat2d(Nametag3d):

    def __init__(self):
        Nametag3d.__init__(self)
        self.is_3d = False
        self.updateContents()
