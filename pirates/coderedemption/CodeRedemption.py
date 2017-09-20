from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PLocalizer
from pirates.coderedemption import CodeRedemptionGlobals

class CodeRedemption(DistributedObjectGlobal):

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)

    def redeemCode(self, code):
        if code:
            userName = ''
            accountId = 0
            self.sendUpdate('sendCodeForRedemption', [code, userName, accountId])

    def notifyClientCodeRedeemStatus(self, status, type, uid):
        if status == CodeRedemptionGlobals.ERROR_ID_GOOD:
            base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionGood)
        elif status == CodeRedemptionGlobals.ERROR_ID_OVERFLOW:
            base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionFull)
        elif status == CodeRedemptionGlobals.ERROR_ID_TIMEOUT:
            base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionTimeout)
        else:
            base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionBad)

        if type == -1:
            pass
        elif type == CodeRedemptionGlobals.CLOTHING:
            localAvatar.guiMgr.messageStack.showLoot([], cloth=uid)
        elif type == CodeRedemptionGlobals.JEWELRY:
            localAvatar.guiMgr.messageStack.showLoot([], jewel=uid)
        elif type == CodeRedemptionGlobals.TATTOO:
            localAvatar.guiMgr.messageStack.showLoot([], tattoo=uid)
        messenger.send('codeRedeemed', [status])