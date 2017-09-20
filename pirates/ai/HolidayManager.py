from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify

class HolidayManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('HolidayManager')

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.callback = None

    def requestChooserHoliday(self, callback):
        self.callback = callback
        self.sendUpdate('requestChooserHoliday', [])

    def requestChooserHolidayResponse(self, holidayIds):
        if not self.callback:
            return
        self.callback(holidayIds)
        self.callback = None