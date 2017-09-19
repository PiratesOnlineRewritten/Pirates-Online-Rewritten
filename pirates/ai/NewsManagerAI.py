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

    def addHoliday(self, holidayId, time):
        found = any([holidayEntry[0]==holidayId for holidayEntry in self.holidayIdList])

        if found:
            self.notify.warning('Attempted to start already running holiday: %d' % holidayId)
            return

        self.holidayIdList.append([holidayId, time])
        self.notify.debug('Adding Holiday %d for a duration of %d' % (holidayId, time))

        self.sendUpdate('setHolidayIdList', [self.holidayIdList])

    def removeHoliday(self, holidayId):
        found = any([holidayEntry[0]==holidayId for holidayEntry in self.holidayIdList])

        if not found:
            self.notify.warning('Attempted to end none running holiday: %d' % holidayId)
            return

        self.holidayIdList = [holidayEntry for holidayEntry in self.holidayIdList if holidayEntry[0]!=holidayId]
        self.notify.debug('Removing Holiday %d' % holidayId)

        self.sendUpdate('setHolidayIdList', [self.holidayIdList])
    
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