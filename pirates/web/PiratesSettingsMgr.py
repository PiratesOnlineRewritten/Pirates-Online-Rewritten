from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.web.SettingsMgr import SettingsMgr
from pirates.web.PiratesSettingsMgrBase import PiratesSettingsMgrBase

class PiratesSettingsMgr(SettingsMgr, PiratesSettingsMgrBase):
    notify = directNotify.newCategory('PiratesSettingsMgr')

    def _initSettings(self):
        SettingsMgr._initSettings(self)
        PiratesSettingsMgrBase._initSettings(self)