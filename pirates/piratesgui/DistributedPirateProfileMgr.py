from direct.distributed import DistributedObject

class DistributedPirateProfileMgr(DistributedObject.DistributedObject):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        base.cr.profileMgr = self

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        base.cr.profileMgr = None
        return

    def delete(self):
        DistributedObject.DistributedObject.disable(self)

    def requestAvatar(self, avId):
        self.sendUpdate('requestAvatar', [avId, localAvatar.getDoId()])

    def receiveAvatarInfo(self, dna, guildId, guildName, founder, hp, maxHp, voodoo, maxVoodoo, shardId, disableButtons, showGoTo):
        messenger.send('avatarInfoRetrieved', [dna, guildId, guildName, founder, hp, maxHp, voodoo, maxVoodoo, shardId, disableButtons, showGoTo])

    def receiveAvatarSkillLevels(self, level, cannon, sailing, cutlass, pistol, doll, dagger, grenade, staff, potions, fishing):
        messenger.send('avatarSkillLevelsRetrieved', [level, cannon, sailing, cutlass, pistol, doll, dagger, grenade, staff, potions, fishing])

    def receiveAvatarOnlineInfo(self, islandName, locationName, siege, profileIcon):
        messenger.send('avatarOnlineInfoRetrieved', [islandName, locationName, siege, profileIcon])

    def receiveAvatarShipInfo(self, guildState, crewState, friendState):
        messenger.send('avatarShipInfoRetrieved', [guildState, crewState, friendState])

    def receiveAvatarChatPermissions(self, chatPermission):
        messenger.send('avatarChatPermissionsRetrieved', [chatPermission])