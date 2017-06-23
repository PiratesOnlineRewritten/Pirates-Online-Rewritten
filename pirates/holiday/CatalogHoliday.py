from pirates.ai import HolidayGlobals
from pirates.holiday import CatalogHolidayGlobals
from pirates.piratesbase import PLocalizer

def getCatalogItemsForHoliday(holidayId):
    holidayClass = HolidayGlobals.getHolidayClass(holidayId)
    if holidayClass != HolidayGlobals.CATALOGHOLIDAY:
        return []
    holidayConfig = HolidayGlobals.getHolidayConfig(holidayId)
    if holidayConfig not in CatalogHolidayGlobals.CatalogHolidayConfigs:
        return []
    return CatalogHolidayGlobals.CatalogHolidayConfigs[holidayConfig].get('items', [])


def getCatalogItemsForHolidays(holidayIds):
    items = []
    for holidayId in holidayIds:
        items.extend(getCatalogItemsForHoliday(holidayId))

    return items


def getCatalogDisplayNameForHoliday(holidayId):
    holidayClass = HolidayGlobals.getHolidayClass(holidayId)
    if holidayId in HolidayGlobals.HOLIDAYS_WITH_CATALOGS:
        holidayName = PLocalizer.HOLIDAYIDS_TO_NAMES.get(holidayClass, 'error')
        return holidayName
    if holidayClass != HolidayGlobals.CATALOGHOLIDAY:
        return 'not-catalog-holiday'
    holidayConfig = HolidayGlobals.getHolidayConfig(holidayId)
    if holidayConfig not in CatalogHolidayGlobals.CatalogHolidayConfigs:
        return 'not-catalog-config'
    return PLocalizer.CatalogHolidayNames.get(holidayConfig, {}).get('displayName', 'no-display-name')


def getCatalogTabNameForHoliday(holidayId):
    holidayClass = HolidayGlobals.getHolidayClass(holidayId)
    if holidayId in HolidayGlobals.HOLIDAYS_WITH_CATALOGS:
        holidayName = PLocalizer.HOLIDAYIDS_TO_NAMES.get(holidayClass, 'error')
        return holidayName
    if holidayClass != HolidayGlobals.CATALOGHOLIDAY:
        return 'not-catalog-holiday'
    holidayConfig = HolidayGlobals.getHolidayConfig(holidayId)
    if holidayConfig not in CatalogHolidayGlobals.CatalogHolidayConfigs:
        return 'not-catalog-config'
    return PLocalizer.CatalogHolidayNames.get(holidayConfig, {}).get('tabName', 'no-tab-name')