from otp.chat.ChatInputWhiteList import ChatInputWhiteList
from pirates.chat.PWhiteList import PWhiteList

class PChatInputWhiteList(ChatInputWhiteList):

    def __init__(self, parent=None, **kw):
        ChatInputWhiteList.__init__(self, parent, **kw)
        self.initialiseoptions(PChatInputWhiteList)
        self.whiteList = PWhiteList()
        self.accept('SetChatBoxPercentage', self.textBoxScale)
        self.setDefaultWidth()

    def delete(self):
        ChatInputWhiteList.delete()

    def textBoxScale(self, percentage):
        iPercentage = 1.0 / percentage
        self['text_scale'] = (self.origTextScale[0] * iPercentage, self.origTextScale[1] * 1.0)
        self['frameSize'] = (self.origFrameSize[0] * iPercentage, self.origFrameSize[1] * iPercentage, self.origFrameSize[2], self.origFrameSize[3])
        self.setDefaultWidth()
        self['width'] = self.defaultWidth
        self.set('')

    def setDefaultWidth(self, size=None):
        if size != None:
            self.defaultWidth = size
        else:
            entrySize = self['frameSize'][1]
            textWidth = entrySize / self['text_scale'][0]
            self.defaultWidth = textWidth
        return

    def sendChatByMode(self, text):
        state = self.getCurrentOrNextState()
        messenger.send('sentRegularChat')
        if state == 'PlayerWhisper':
            base.talkAssistant.sendAccountTalk(text, self.whisperId)
        elif state == 'AvatarWhisper':
            base.talkAssistant.sendWhisperTalk(text, self.whisperId)
        elif state == 'GuildChat':
            base.talkAssistant.sendGuildTalk(text)
        elif state == 'CrewChat':
            base.talkAssistant.sendPartyTalk(text)
        elif state == 'ShipPVPChat':
            base.talkAssistant.sendShipPVPCrewTalk(text)
        else:
            base.talkAssistant.sendOpenTalk(text)