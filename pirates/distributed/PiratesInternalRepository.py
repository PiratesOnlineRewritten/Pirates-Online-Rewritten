from direct.distributed.AstronInternalRepository import AstronInternalRepository
from otp.distributed.OtpDoGlobals import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from panda3d.core import *
from pirates.uberdog.WebhooksUD import SlackWebhook, SlackAttachment, SlackField
import traceback
import sys

class PiratesInternalRepository(AstronInternalRepository):
    GameGlobalsId = OTP_DO_ID_PIRATES
    dbId = 4003

    def __init__(self, baseChannel, serverId=None, dcFileNames = None, dcSuffix='AI', connectMethod=None, threadedNet=None):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix, connectMethod, threadedNet)

    def handleConnected(self):
        if config.GetBool('send-hacker-test-message', False):
            self.logPotentialHacker('I am a test hacker message!', field='Test', thing='this')

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender() >> 32) & 0xFFFFFFFF

    def isDevServer(self):
        return 'dev' in config.GetString('server-version', '') or __dev__

    def setAllowClientSend(self, avId, distObj, fieldNameList=[]):
        dg = PyDatagram()
        dg.addServerHeader(distObj.GetPuppetConnectionChannel(avId), self.ourChannel, CLIENTAGENT_SET_FIELDS_SENDABLE)
        fieldIds = []
        for fieldName in fieldNameList:
            field = distObj.dclass.getFieldByName(fieldName)
            if field:
                fieldIds.append(field.getNumber())

        dg.addUint32(distObj.getDoId())
        dg.addUint16(len(fieldIds))
        for fieldId in fieldIds:
            dg.addUint16(fieldId)

        self.send(dg)

    def _isValidPlayerLocation(self, parentId, zoneId):
        return True

    def systemMessage(self, message, channel=10):
        msgDg = PyDatagram()
        msgDg.addUint16(6)
        msgDg.addString(message)

        self.writeServerEvent('system-message', 
            sourceChannel=self.ourChannel, 
            message=message, 
            targetChannel=channel)

        dg = PyDatagram()
        dg.addServerHeader(channel, self.ourChannel, CLIENTAGENT_SEND_DATAGRAM)
        dg.addString(msgDg.getMessage())
        self.send(dg)

    def kickChannel(self, channel, reason=1, message='An unexpected problem has occured.'):
        dg = PyDatagram()
        dg.addServerHeader(channel, self.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(reason)
        dg.addString(message)
        self.send(dg)      

    def logPotentialHacker(self, message, kickChannel=False, **kwargs):
        self.notify.warning(message)

        avatarId = self.getAvatarIdFromSender() or 0
        accountId = self.getAccountIdFromSender() or 0

        self.writeServerEvent('suspicious-event',
            message=message, 
            avatarId=avatarId, 
            accountId=accountId, 
            **kwargs)

        if config.GetBool('discord-log-hacks', False):
            hackWebhookUrl = config.GetString('discord-log-hacks-url', '')

            if hackWebhookUrl:
                districtName = 'Unknown'
                if hasattr(self, 'distributedDistrict'):
                    districtName = self.distributedDistrict.getName()

                header = 'Detected potential hacker on %s.' % districtName
                webhookMessage = SlackWebhook(hackWebhookUrl, message='@everyone' if config.GetBool('discord-ping-everyone', not config.GetBool('want-dev', False)) else '')

                attachment = SlackAttachment(pretext=message, title=header)

                for kwarg in kwargs:
                    attachment.addField(SlackField(title=kwarg, value=kwargs[kwarg]))

                attachment.addField(SlackField())

                avatar = self.doId2do.get(avatarId)
                if avatar:
                    attachment.addField(SlackField(title='Character Pos', value=str(avatar.getPos())))
                    attachment.addField(SlackField(title='Character Name', value=avatar.getName()))
                    attachment.addField(SlackField(title='Island', value=avatar.getParentObj().getLocalizerName()))

                attachment.addField(SlackField())
                attachment.addField(SlackField(title='Game Account Id', value=accountId))
                #TODO account name?

                attachment.addField(SlackField())
                attachment.addField(SlackField(title='Dev Server', value=self.isDevServer()))

                webhookMessage.addAttachment(attachment)
                webhookMessage.send()
            else:
                self.notify.warning('Discord Hacker Webhook url not defined!')

        if kickChannel:
            self.kickChannel(kickChannel)     

    def readerPollOnce(self):
        try:
            return AstronInternalRepository.readerPollOnce(self)
        except SystemExit, KeyboardInterrupt:
            raise
        except Exception as e:

            if config.GetBool('boot-on-error', False):
                avatar = self.doId2do.get(self.getAvatarIdFromSender(), None)

                if avatar:
                    self.kickChannel(self.getMsgSender())

            self.writeServerEvent('internal-exception', 
                avId=self.getAvatarIdFromSender(),
                accountId=self.getAccountIdFromSender(),
                exception=traceback.format_exc())

            self.notify.warning('internal-exception: %s (%s)' % (repr(e), self.getAvatarIdFromSender()))
            print traceback.format_exc()
            sys.exc_clear()

        return 1