from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.ship import ShipGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.pvp import PVPGlobals
from pirates.quest import QuestConstants
from pirates.piratesgui.ShipFrameDeploy import ShipFrameDeploy
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from pirates.band.DistributedBandMember import DistributedBandMember
from pirates.piratesgui.ShipSelectionPanel import ShipSelectionPanel

class ShipDeployPanel(ShipSelectionPanel):
    notify = directNotify.newCategory('ShipDeployPanel')

    def __init__(self, title, doneCallback, siegeTeam=0):
        ShipSelectionPanel.__init__(self, title, doneCallback, pages=[self.OWN, self.FRIEND, self.CREW, self.GUILD, self.PUBLIC])
        self.initialiseoptions(ShipDeployPanel)
        self._siegeTeam = siegeTeam
        if localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_SHIP and localAvatar.getCurrentIsland() != QuestConstants.LocationIds.PORT_ROYAL_ISLAND:
            text = PLocalizer.DinghyNeedFirstShip % PLocalizer.LocationNames[QuestConstants.LocationIds.PORT_ROYAL_ISLAND]
        else:
            text = PLocalizer.DinghyNeedShip
        self.noShipHint = DirectLabel(parent=self, relief=None, text=text, text_font=PiratesGlobals.getPirateFont(), text_scale=0.08, text_fg=PiratesGuiGlobals.TextFG1, text_wordwrap=10, textMayChange=1, pos=(0.55,
                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                 0.8))
        return

    def setPage(self, pageId):
        ShipSelectionPanel.setPage(self, pageId)
        if not self.shipFrames[pageId]:
            if pageId == self.OWN:
                if localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_SHIP and localAvatar.getCurrentIsland() != QuestConstants.LocationIds.PORT_ROYAL_ISLAND:
                    self.noShipHint['text'] = PLocalizer.DinghyNeedFirstShip % PLocalizer.LocationNames[QuestConstants.LocationIds.PORT_ROYAL_ISLAND]
                elif self._siegeTeam and localAvatar.getSiegeTeam() and localAvatar.getSiegeTeam() != self._siegeTeam:
                    if localAvatar.getSiegeTeam() == PVPGlobals.FrenchTeam:
                        self.noShipHint['text'] = PLocalizer.DinghyWrongSiegeShip % PLocalizer.PVPFrench
                    else:
                        self.noShipHint['text'] = PLocalizer.DinghyWrongSiegeShip % PLocalizer.PVPSpanish
                else:
                    self.noShipHint['text'] = PLocalizer.DinghyNeedShip
            elif pageId == self.FRIEND:
                self.noShipHint['text'] = PLocalizer.DinghyNoFriendShip
            elif pageId == self.CREW:
                self.noShipHint['text'] = PLocalizer.DinghyNoCrewShip
            elif pageId == self.GUILD:
                self.noShipHint['text'] = PLocalizer.DinghyNoGuildShip
            elif pageId == self.PUBLIC:
                self.noShipHint['text'] = PLocalizer.DinghyNoPublicShip
            self.noShipHint.show()
        else:
            self.noShipHint.hide()

    def _makeFrame(self, shipId, shipName, shipClass, mastInfo, shipHp, shipSp, cargo, crew, time, siegeTeam, avatarName, customHull, customRigging, customPattern, customLogo, callback):
        shipFrame = self.getFrame(shipId)
        if shipFrame:
            shipFrame.addCrewMemberName(avatarName)
        else:
            shipFrame = ShipFrameDeploy(parent=None, relief=None, shipId=shipId, shipName=shipName, shipClass=shipClass, mastInfo=mastInfo, shipType=ShipFrameDeploy.STFriend, siegeTeam=siegeTeam, avatarName=avatarName, command=callback, extraArgs=[shipId])
            shipFrame.enableStats(shipName, shipClass, mastInfo, shipHp, shipSp, cargo, crew, time)
            shipFrame.setCustomization(customHull=customHull, customRigging=customRigging, customPattern=customPattern, customLogo=customLogo)
        return shipFrame

    def addOwnShip(self, shipId, callback):
        shipOV = base.cr.getOwnerView(shipId)
        if not shipOV or self._siegeTeam and localAvatar.getSiegeTeam() and localAvatar.getSiegeTeam() != self._siegeTeam:
            return
        shipFrame = self.getFrame(shipId)
        if not shipFrame:
            mastInfo = ShipGlobals.getMastSetup(shipOV.shipClass)
            shipFrame = ShipFrameDeploy(parent=None, shipId=shipId, shipName=shipOV.name, shipClass=shipOV.shipClass, mastInfo=mastInfo, shipType=ShipFrameDeploy.STOwn, siegeTeam=self._siegeTeam, command=callback, extraArgs=[shipId])
            shipFrame.enableStatsOV(shipOV)
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()) and shipOV.shipClass not in ShipGlobals.UNPAID_SHIPS:
                shipFrame.nameLabel['text'] = PLocalizer.noFreebooterCap
                shipFrame.nameLabel['text_fg'] = (1, 0.7, 0.7, 1)
        self.addFrameOwn(shipFrame)
        return

    def addBandShip(self, shipInfo, callback):
        bandMemberId, shipId, shipHp, shipSp, cargo, crew, time, siegeTeam, avatarName, customHull, customRigging, customPattern, customLogo = shipInfo
        if localAvatar.getSiegeTeam() and localAvatar.getSiegeTeam() != siegeTeam:
            return
        bandMember = base.cr.getDo(bandMemberId)
        if bandMember:
            shipInfo = bandMember.getShipInfo()
            if shipInfo and shipInfo[0] == shipId:
                shipId, shipName, shipClass, mastInfo = shipInfo
                shipFrame = self._makeFrame(shipId, shipName, shipClass, ShipGlobals.getMastSetup(shipClass), shipHp, shipSp, cargo, crew, time, siegeTeam, avatarName, customHull, customRigging, customPattern, customLogo, callback)
                shipFrame.addCrewMemberName(avatarName)
                self.addFrameCrew(shipFrame)

    def addFriendShip(self, shipInfo, callback):
        friendId, shipId, shipHp, shipSp, cargo, crew, time, shipClass, shipName, siegeTeam, avatarName, customHull, customRigging, customPattern, customLogo = shipInfo
        if localAvatar.getSiegeTeam() and localAvatar.getSiegeTeam() != siegeTeam:
            return
        shipFrame = self._makeFrame(shipId, shipName, shipClass, ShipGlobals.getMastSetup(shipClass), shipHp, shipSp, cargo, crew, time, siegeTeam, avatarName, customHull, customRigging, customPattern, customLogo, callback)
        shipFrame.addCrewMemberName(avatarName)
        self.addFrameFriend(shipFrame)

    def addGuildShip(self, shipInfo, callback):
        guildmateId, shipId, shipHp, shipSp, cargo, crew, time, shipClass, shipName, siegeTeam, avatarName, customHull, customRigging, customPattern, customLogo = shipInfo
        if localAvatar.getSiegeTeam() and localAvatar.getSiegeTeam() != siegeTeam:
            return
        shipFrame = self._makeFrame(shipId, shipName, shipClass, ShipGlobals.getMastSetup(shipClass), shipHp, shipSp, cargo, crew, time, siegeTeam, avatarName, customHull, customRigging, customPattern, customLogo, callback)
        shipFrame.addCrewMemberName(avatarName)
        self.addFrameGuild(shipFrame)

    def addPublicShip(self, shipInfo, callback):
        ownerId, shipId, shipHp, shipSp, cargo, crew, time, shipClass, shipName, siegeTeam, avatarName, customHull, customRigging, customPattern, customLogo = shipInfo
        if localAvatar.getSiegeTeam() and localAvatar.getSiegeTeam() != siegeTeam:
            return
        shipFrame = self._makeFrame(shipId, shipName, shipClass, ShipGlobals.getMastSetup(shipClass), shipHp, shipSp, cargo, crew, time, siegeTeam, avatarName, customHull, customRigging, customPattern, customLogo, callback)
        self.addFramePublic(shipFrame)