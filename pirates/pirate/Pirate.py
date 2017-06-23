from pirates.piratesbase import PiratesGlobals
from Human import Human
import AvatarTypes

class Pirate(Human):

    def __init__(self, other=None):
        Human.__init__(self, other)
        self.avatarType = AvatarTypes.Pirate


class PirateHeadPortrait(Human):

    def __init__(self):
        Human.__init__(self)
        self.avatarType = AvatarTypes.Townfolk

    def generatePortrait(self, other):
        highLod = other.getLOD('2000')
        face = highLod.findAllMatches('**/body_master_face')
        face.stash()
        body = highLod.findAllMatches('**/body_*')
        body.stash()
        clothing = highLod.findAllMatches('**/clothing_*')
        clothing.stash()
        face.unstash()
        hairs = highLod.findAllMatches('**/hair_*')
        eyes = highLod.findAllMatches('**/eye*')
        teeth = highLod.findAllMatches('**/teeth*')

    def shapeHead(self, other):
        import pdb
        pdb.set_trace()
        self.style = other.style
        self.generateHuman(self.style.gender, base.cr.humanHigh)