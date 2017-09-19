from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
import random

class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.holidayIdList = []
        self.noteablePathList = []

    def d_holidayNotify(self):
        self.sendUpdate('holidayNotify', [])

    def setHolidayIdList(self, holidayIdList):
        self.holidayIdList = holidayIdList

    def d_setHolidayIdList(self, holidayIdList):
        self.sendUpdate('setHolidayIdList', [holidayIdList])

    def b_setHolidayIdList(self, holidayIdList):
        self.setHolidayIdList(holidayIdList)
        self.d_setHolidayIdList(holidayIdList)

    def d_displayMessage(self, messageId):
        self.sendUpdate('displayMessage', [messageId])

    def d_playMusic(self, musicId, duration, requiredDoId):
        self.sendUpdate('playMusic', [(musicId, duration, requiredDoId)])

    def setNoteablePathList(self, noteablePathList):
        self.noteablePathList = noteablePathList

    def d_setNoteablePathList(self, noteablePathList):
        self.sendUpdate('setNoteablePathList', [noteablePathList])

    def b_setNoteablePathList(self, noteablePathList):
        self.setNoteablePathList(noteablePathList)
        self.d_setNoteablePathList(noteablePathList)