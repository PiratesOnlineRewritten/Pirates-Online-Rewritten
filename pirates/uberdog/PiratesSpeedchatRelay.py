from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.uberdog.SpeedchatRelay import SpeedchatRelay
from otp.uberdog import SpeedchatRelayGlobals

class PiratesSpeedchatRelay(SpeedchatRelay):

    def __init__(self, cr):
        SpeedchatRelay.__init__(self, cr)

    def sendQuestSpeedchat(self, receiverId, questInt, msgType, taskNum):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.PIRATES_QUEST, [questInt, msgType, taskNum])