from pirates.ai.HolidayDates import *

class ConfigIds():
    CrewDays = 1


MessageHolidayConfigs = {ConfigIds.CrewDays: {'id': ConfigIds.CrewDays,'name': 'CrewDays (Msg)','dates': HolidayDates(HolidayDates.TYPE_WEEKLY, [
                                (
                                 Day.FRIDAY, 15, 0, 0), (Day.FRIDAY, 20, 0, 0), (Day.SATURDAY, 15, 0, 0), (Day.SATURDAY, 20, 0, 0)])
                        }
   }