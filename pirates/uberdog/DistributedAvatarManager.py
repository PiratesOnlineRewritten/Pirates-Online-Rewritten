from otp.uberdog.OtpAvatarManager import OtpAvatarManager
from otp.otpbase import OTPGlobals

class DistributedAvatarManager(OtpAvatarManager):

    def sendAvIdList(self, avIds):
        pass

    def sendRequestFinalize(self, avId):
        self.sendUpdate('requestFinalize', [0, avId])

    def sendRequestCreateAvatar(self, subId):
        self.sendUpdate('requestCreateAvatar', [0, subId])

    def sendRequestPopulateAvatar(self, avId, avatarData, usePattern, nicknameIndex, firstIndex, prefixIndex, suffixIndex):
        self.sendUpdate('requestPopulateAvatar', [0, avId, avatarData, usePattern, nicknameIndex, firstIndex, prefixIndex, suffixIndex])

    def sendRequestPatternName(self, avId, nicknameIndex, firstIndex, prefixIndex, suffixIndex):
        self.sendUpdate('requestPatternName', [0, avId, nicknameIndex, firstIndex, prefixIndex, suffixIndex])

    def populateAvatarResponse(self, success):
        if success:
            messenger.send('avatarPopulated')

    def patternNameResponse(self, success):
        if success:
            messenger.send('patternNameSet')

    def avatarListResponse(self, accounts, numInventoryManagers):
        base.cr.createInventoryManagers(numInventoryManagers)
        finalData = {}
        for sub in accounts:
            subId = sub[0]
            numPending = sub[1]
            maxAvatars = sub[2]
            maxSlots = sub[3]
            avatars = sub[4]
            avatarData = []
            for av in avatars:
                av[1].setName(av[0])
                avatarData.append({'name': av[0],'dna': av[1],'slot': av[2],'id': av[3],'creator': av[4],'shared': av[5],'online': av[6],'wishName': av[7],'wishState': av[8],'defaultShard': av[9],'lastLogout': av[10]})

            if numPending > 0:
                avatarData += [OTPGlobals.AvatarPendingCreate] * numPending
            curNum = len(avatarData)
            if maxAvatars > curNum:
                avatarData += [OTPGlobals.AvatarSlotAvailable] * (maxAvatars - curNum)
            curNum = len(avatarData)
            if maxSlots > curNum:
                avatarData += [OTPGlobals.AvatarSlotUnavailable] * (maxSlots - curNum)
            finalData[subId] = avatarData

        messenger.send('avatarList', [finalData])