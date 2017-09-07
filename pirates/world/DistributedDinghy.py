from pandac.PandaModules import *
from direct.showbase.PythonUtil import report
from direct.interval.IntervalGlobal import *
from otp.otpgui import OTPDialog
from pirates.distributed.DistributedInteractive import DistributedInteractive
from pirates.piratesbase import PLocalizer, PiratesGlobals
from pirates.piratesgui.ShipDeployPanel import ShipDeployPanel
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.piratesgui import PDialog
from operator import itemgetter
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals

class DistributedDinghy(DistributedInteractive):
    notify = directNotify.newCategory('DistributedDinghy')
    camPos = Point3(227.48, 222.273, 71.208)
    camHpr = VBase3(172.233, -15.2738, -0.376993)

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedDinghy')
        DistributedInteractive.__init__(self, cr)
        self.interactRadius = 25
        self.diskRadius = 45
        self.dinghyDisabledDialog = None
        self.teamFullDialog = None
        self.locationId = 0
        self.shipSelection = None
        self.camIval = None
        self.camTask = None
        self.avGameState = None
        self.invReq = None
        self.selectionSent = False
        self.ownShipSelection = None
        self.accept('clientLogout', self.cleanupTeamFullDialog)
        self.accept('shardSwitchComplete', self.cleanupTeamFullDialog)
        return

    def generate(self):
        DistributedInteractive.generate(self)
        self.setInteractOptions(proximityText=PLocalizer.DeployShipInstructions, sphereScale=self.interactRadius, diskRadius=self.diskRadius)

    def disable(self):
        DistributedInteractive.disable(self)
        if self.invReq:
            DistributedInventoryBase.cancelGetInventory(localAvatar.getInventoryId())
            self.invReq = None
        self.get_children().detach()
        return

    def delete(self):
        if self.camIval:
            self.camIval.pause()
            self.camIval = None
        if self.camTask:
            taskMgr.remove(self.camTask)
            self.camTask = None
        DistributedInteractive.delete(self)
        return

    def setInteractRadius(self, radius):
        self.interactRadius = radius

    def setLocationId(self, locationId):
        self.locationId = locationId
        if self.locationId == 0:
            self.diskRadius = 65
        else:
            self.diskRadius = 45

    def setSiegeTeam(self, team):
        self._siegeTeam = team

    def loadTargetIndicator(self):
        DistributedInteractive.loadTargetIndicator(self)
        if self.locationId == 0:
            self.disk.setZ(render, 0.01)
            self.disk.setP(render, 0)
            self.disk.setR(render, 0)
            self.disk.clearBin()
            self.disk.clearDepthTest()

    def defaultFilter(self, request, args):
        if request == 'Use':
            if self.getCurrentOrNextState() != 'Waiting':
                return None
        return DistributedInteractive.defaultFilter(self, request, args)

    def requestInteraction(self, avId, interactType=0, instant=0):
        if not base.launcher.getPhaseComplete(5):
            self.showDownloadAcknowledge()
            return None
        self.cleanupDinghyDisabledDialog()
        if localAvatar.zombie and avId == localAvatar.doId:
            localAvatar.guiMgr.createWarning(PLocalizer.ZombieNoBoats, PiratesGuiGlobals.TextFG6)
            return None
        DistributedInteractive.requestInteraction(self, avId, interactType, instant)
        return None

    def showDownloadAcknowledge(self):
        base.cr.centralLogger.writeClientEvent('Player encountered phase 5 blocker trying to use a dinghy')
        if not self.dinghyDisabledDialog:
            self.dinghyDisabledDialog = PDialog.PDialog(text=PLocalizer.NoMainWorld, style=OTPDialog.Acknowledge, command=self.cleanupDinghyDisabledDialog)

    def cleanupDinghyDisabledDialog(self, extraArgs=None):
        if self.dinghyDisabledDialog:
            self.dinghyDisabledDialog.destroy()
            self.dinghyDisabledDialog = None
        return

    def showTeamFullAcknowledge(self):
        if not self.teamFullDialog:
            self.teamFullDialog = PDialog.PDialog(text=PLocalizer.PrivateerAllTeamsFull, style=OTPDialog.YesNo, command=self.handleTeamFullAcknowledge)

    def showSingleTeamFullAcknowledge(self):
        if not self.teamFullDialog:
            self.teamFullDialog = PDialog.PDialog(text=PLocalizer.PrivateerSingleTeamFull, style=OTPDialog.YesNo, command=self.handleSingleTeamFullConfirmation)

    def handleTeamFullAcknowledge(self, value):
        if value == 1:
            base.localAvatar.guiMgr.crewHUD.b_activateAvatarLookoutPVP()
        self.cleanupTeamFullDialog()

    def handleSingleTeamFullConfirmation(self, value):
        if value == 1:
            if self.ownShipSelection:
                self.selectionSent = False
                if self._siegeTeam == 1:
                    self.ownShipSelected(self.ownShipSelection, 2)
                else:
                    self.ownShipSelected(self.ownShipSelection, 1)
        self.cleanupTeamFullDialog()

    def cleanupTeamFullDialog(self, extraArgs=None):
        if self.teamFullDialog:
            self.teamFullDialog.destroy()
            self.teamFullDialog = None
        return

    def enterWaiting(self):
        DistributedInteractive.enterWaiting(self)
        self.avGameState = localAvatar.getGameState()
        if self.avGameState == 'Battle':
            self.avGameState = 'LandRoam'
        localAvatar.b_setGameState('DinghyInteract', [self])

    def exitWaiting(self):
        DistributedInteractive.exitWaiting(self)
        if self.newState != 'Use' and self.avGameState:
            if localAvatar.getGameState() == 'DinghyInteract':
                localAvatar.b_setGameState(self.avGameState)
                if self.avGameState in ['WaterRoam', 'BattleWaterRoam']:
                    localAvatar.motionFSM.setWaterState(True, True)
                    base.cr.interactionMgr.start()
            self.avGameState = None
        if self.invReq:
            DistributedInventoryBase.cancelGetInventory(localAvatar.getInventoryId())
            self.invReq = None
        return

    def denyAccess(self, type):
        self.requestExit()
        if type == PiratesGlobals.PrivateerBothTeamFull:
            self.showTeamFullAcknowledge()
        elif type == PiratesGlobals.PrivateerSingleTeamFull:
            self.showSingleTeamFullAcknowledge()
        elif type == PiratesGlobals.ZombieNoBoats:
            localAvatar.guiMgr.createWarning(PLocalizer.ZombieNoBoats, PiratesGuiGlobals.TextFG6)
        elif type == PiratesGlobals.ShipNeedCompass:
            localAvatar.guiMgr.createWarning(PLocalizer.ShipNeedCompass, PiratesGuiGlobals.TextFG6)

    def offerOptions(self):
        self.invReq = DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), self.invArrived, 10)

    def invArrived(self, inv):
        self.invReq = None
        if inv:
            self.request('Use')
        else:
            self.requestExit()
        return

    def enterUse(self):
        DistributedInteractive.enterUse(self)
        if self.shipSelection:
            self.shipSelection.destroy()
        self.shipSelection = ShipDeployPanel(PLocalizer.ChooseShipTitle, self.requestExit, siegeTeam=self._siegeTeam)
        self.shipSelection.hide()
        self.selectionSent = False
        self.startCamIval()
        self.offerOwnOptions(localAvatar.getInventory().getShipDoIdList())

    def exitUse(self):
        DistributedInteractive.exitUse(self)
        if self.avGameState:
            if localAvatar.getGameState() == 'DinghyInteract':
                localAvatar.b_setGameState(self.avGameState)
                if self.avGameState in ['WaterRoam', 'BattleWaterRoam']:
                    localAvatar.motionFSM.setWaterState(True, True)
                    base.cr.interactionMgr.start()
            self.avGameState = None
        if self.camIval:
            self.camIval.pause()
            self.camIval = None
        if self.camTask:
            taskMgr.remove(self.camTask)
            self.camTask = None
        if self.shipSelection:
            self.shipSelection.destroy()
            self.shipSelection = None
        return

    def offerOwnOptions(self, shipIds):
        if self.shipSelection:
            for shipId in shipIds:
                self.shipSelection.addOwnShip(shipId, self.ownShipSelected)

    def offerBandOptions(self, options):
        if self.shipSelection:
            optionsSorted = sorted(options, key=itemgetter(5))
            for shipInfo in optionsSorted:
                self.shipSelection.addBandShip(shipInfo, self.bandShipSelected)

    def offerFriendOptions(self, options):
        if self.shipSelection:
            optionsSorted = sorted(options, key=itemgetter(5))
            for shipInfo in optionsSorted:
                self.shipSelection.addFriendShip(shipInfo, self.friendShipSelected)

    def offerGuildOptions(self, options):
        if self.shipSelection:
            optionsSorted = sorted(options, key=itemgetter(5))
            for shipInfo in optionsSorted:
                self.shipSelection.addGuildShip(shipInfo, self.guildShipSelected)

    def offerPublicOptions(self, publicOptions):
        if self.shipSelection:
            publicOptionsSorted = sorted(publicOptions, key=itemgetter(5))
            for shipInfo in publicOptionsSorted:
                self.shipSelection.addPublicShip(shipInfo, self.publicShipSelected)

    def ownShipSelected(self, shipId, teamSpec=0):
        if shipId >= 0:
            self.b_selectOwnShip(shipId, teamSpec)
            self.ownShipSelection = shipId
        self.selectionMade()

    def friendShipSelected(self, friendId):
        if friendId >= 0:
            self.b_selectFriendShip(friendId)
        self.selectionMade()

    def bandShipSelected(self, shipId):
        if shipId >= 0:
            self.b_selectBandShip(shipId)
        self.selectionMade()

    def guildShipSelected(self, shipId):
        if shipId >= 0:
            self.b_selectGuildShip(shipId)
        self.selectionMade()

    def publicShipSelected(self, shipId):
        if shipId >= 0:
            self.b_selectPublicShip(shipId)
        self.selectionMade()

    def b_selectOwnShip(self, shipId, teamSpec=0):
        if not self.selectionSent:
            self.selectionSent = True
            self.d_selectOwnShip(shipId, teamSpec)

    def d_selectOwnShip(self, shipId, teamSpec=0):
        self.sendUpdate('selectOwnShip', [shipId, teamSpec])

    def b_selectFriendShip(self, shipId):
        if not self.selectionSent:
            self.selectionSent = True
            self.d_selectFriendShip(shipId)

    def d_selectFriendShip(self, friendId):
        self.sendUpdate('selectFriendShip', [friendId])

    def b_selectBandShip(self, shipId):
        if not self.selectionSent:
            self.selectionSent = True
            self.d_selectBandShip(shipId)

    @report(types=['frameCount', 'args'], dConfigParam='shipboard')
    def d_selectBandShip(self, shipId):
        self.sendUpdate('selectBandShip', [shipId])

    def b_selectGuildShip(self, shipId):
        if not self.selectionSent:
            self.selectionSent = True
            self.d_selectGuildShip(shipId)

    @report(types=['frameCount', 'args'], dConfigParam='shipboard')
    def d_selectGuildShip(self, shipId):
        self.sendUpdate('selectGuildShip', [shipId])

    def b_selectPublicShip(self, shipId):
        if not self.selectionSent:
            self.selectionSent = True
            self.d_selectPublicShip(shipId)

    @report(types=['frameCount', 'args'], dConfigParam='shipboard')
    def d_selectPublicShip(self, shipId):
        self.sendUpdate('selectPublicShip', [shipId])

    def selectionMade(self):
        self.requestExit()

    def startCamIval(self):
        self.camTask = None
        camera.wrtReparentTo(self.getParentObj())
        if self.camIval:
            self.camIval.pause()
        hpr = VBase3(self.camHpr)
        if hpr[0] - camera.getH() > 180:
            hpr.setX(hpr[0] - 360)
        self.camIval = Sequence()
        self.camIval.append(Func(self.shipSelection.show))
        self.camIval.start()
        return

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='shipboard')
    def sendAvatarToShip(self, shipId):
        self.requestExit()
        if shipId:
            self.cr.loadingScreen.showTarget(ocean=True)
            self.cr.loadingScreen.showHint(ocean=True)
            self.ownShipSelection = None
        else:
            localAvatar.guiMgr.createWarning('Ship was not available')
        return