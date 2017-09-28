from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.distributed.PiratesInternalRepository import PiratesInternalRepository
from direct.distributed.PyDatagram import *
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *
from pirates.uberdog.PiratesRPCServerUD import PiratesRPCServerUD

class PiratesUberRepository(PiratesInternalRepository):
    notify = directNotify.newCategory('PiratesUberRepository')
    notify.setInfo(True)

    def __init__(self, baseChannel, serverId):
        PiratesInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')
        self.rpc = None
        self.districtTracker = None

    def handleConnected(self):
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        if config.GetBool('want-rpc-server', True):
            self.rpc = PiratesRPCServerUD(self)
            self.rpc.daemon = True
            self.rpc.start()

        self.createGlobals()
        self.notify.info('UberDOG ready!')

    def createGlobals(self):
        """
        Create "global" objects.
        """

        self.centralLogger = self.generateGlobalObject(OTP_DO_ID_CENTRAL_LOGGER, 'CentralLogger')
        self.csm = self.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.travelAgent = self.generateGlobalObject(OTP_DO_ID_PIRATES_TRAVEL_AGENT, 'DistributedTravelAgent')
        self.inventoryManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_INVENTORY_MANAGER, 'DistributedInventoryManager')
        self.holidayMgr = self.generateGlobalObject(OTP_DO_ID_PIRATES_HOLIDAY_MANAGER, 'HolidayManager')
        self.codeMgr = self.generateGlobalObject(OTP_DO_ID_PIRATES_CODE_REDEMPTION, 'CodeRedemption')
        self.chatManager = self.generateGlobalObject(OTP_DO_ID_CHAT_MANAGER, 'DistributedChatManager')
        self.speedChatRelay = self.generateGlobalObject(OTP_DO_ID_PIRATES_SPEEDCHAT_RELAY, 'PiratesSpeedchatRelay')
        self.crewMatchManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_CREW_MATCH_MANAGER, 'DistributedCrewMatchManager')
        self.guildManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_GUILD_MANAGER, 'PCGuildManager')
