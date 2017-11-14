from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from pirates.coderedemption import CodeRedemptionGlobals

class CodeRedemptionUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('CodeRedemptionUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.notify.info('%s going online' % self.__class__.__name__)

    def sendCodeForRedemption(self, code, username, accountId):
        sender = self.air.getMsgSender()
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        self.notify.debug('Received code redemption request for code %s from user %s (%s)' % (code, username, accountId))

        if not avatar:

            self.notify.warning('Received sendCodeForRedemption from non-existant avatar')
            self.air.writeServerEvent('suspicious-event', 
                message='Received sendCodeForRedemption from non-existant avatar',
                targetAvId=self.air.getAvatarIdFromSender(), 
                code=code)

            self.d_notifyClientCodeRedeemStatus(sender, CodeRedemptionGlobals.ERROR_ID_BAD, -1, 0)
            return

        if not config.GetBool('code-redemption-enabled', False):
            self.d_notifyClientCodeRedeemStatus(sender, CodeRedemptionGlobals.ERROR_ID_BAD, -1, 0)
            return

        redemptionData = self.getCodeDataFromCode(code)
        if not redemptionData:
            self.d_notifyClientCodeRedeemStatus(sender, CodeRedemptionGlobals.ERROR_ID_BAD, -1, 0)
            return

        itemType = redemptionData[CodeRedemptionGlobals.AvatarTypes.TYPE_IDX]
        maleItem = redemptionData[CodeRedemptionGlobals.AvatarTypes.MALE_IDX]
        femaleItem = redemptionData[CodeRedemptionGlobals.AvatarTypes.FEME_IDX]
        status = CodeRedemptionGlobals.ERROR_ID_GOOD
        uid = 0

        if itemType == CodeRedemptionGlobals.NORMAL_INVENTORY:
            pass
        else:
            self.notify.warning('Received code redemption for unsupported code type: %d' % itemType)
            self.d_notifyClientCodeRedeemStatus(sender, CodeRedemptionGlobals.ERROR_ID_BAD, itemType, 0)
            return 

        expireType = redemptionData[CodeRedemptionGlobals.AvatarTypes.EXPIRE_IDX]
        supportedTypes = [CodeRedemptionGlobals.NEVER_EXPIRE, CodeRedemptionGlobals.EXPIRE_ON_REDEEM]
        if expireType not in supportedTypes:
            self.notify.warning('Received code redemption with unsupported expire type; Defaulting to: %s' % CodeRedemptionGlobals.CODE_TYPES[CodeRedemptionGlobals.EXPIRE_ON_REDEEM])
            expireType = CodeRedemptionGlobals.EXPIRE_ON_REDEEM

        if expireType == CodeRedemptionGlobals.EXPIRE_ON_REDEEM:
            pass #TODO

        self.d_notifyClientCodeRedeemStatus(sender, status, itemType, uid)
        return

    def getCodeDataFromCode(self, code):
        codeIndex = CodeRedemptionGlobals.AwardTypes.GOLD #TODO
        return CodeRedemptionGlobals.AWARD_ID[codeIndex]

    def d_notifyClientCodeRedeemStatus(self, channel, status, type, uid):
        self.sendUpdateToChannel(channel, 'notifyClientCodeRedeemStatus', [status, type, uid])