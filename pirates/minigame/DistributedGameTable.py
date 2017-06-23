import random
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.npc import Townfolk
from pirates.npc import Skeleton
from pirates.distributed import DistributedInteractive
from direct.directnotify import DirectNotifyGlobal
from pirates.pirate import HumanDNA
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PDialog
from otp.otpgui import OTPDialog
from pirates.pirate import AvatarTypes

class DistributedGameTable(DistributedInteractive.DistributedInteractive):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameTable')

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedGameTable')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        self.localAvatarSeat = -1
        self.maxHandCards = 2
        self.requestDialog = None
        self.seatLodNodeArray = []
        self.avId2ivals = {}
        self.possibleUndeadTypes = []
        self.possibleUndeadNames = []
        return

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)

    def setGameVariation(self, variation):
        self.gameVariation = variation

    def getGameVariation(self):
        return self.gameVariation

    def getInteractText(self):
        return PLocalizer.InteractTable

    def saveSequence(self, sequence, av):
        sequence.append(Func(self._removeIval, av, sequence))
        doId = av.doId
        if doId not in self.avId2ivals:
            disableEvent = av.uniqueName('disable')
            self.accept(disableEvent, Functor(self.finishAvIvals, av))
            self.avId2ivals[doId] = []
        self.avId2ivals[doId].append(sequence)

    def finishAvIvals(self, av):
        if av.doId in self.avId2ivals:
            ivals = self.avId2ivals[av.doId][:]
            for ival in ivals:
                ival.finish()

        self.ignore(av.uniqueName('disable'))

    def _removeIval(self, av, ival):
        self.avId2ivals[av.doId].remove(ival)
        if len(self.avId2ivals[av.doId]) == 0:
            del self.avId2ivals[av.doId]
            self.ignore(av.uniqueName('disable'))

    def showUseInfo(self):
        if self.disk:
            self.disk.hide()

    def setTableType(self, type):
        self.tableType = type
        self.setTableInfo(self.tableType)
        self.tableModel.reparentTo(self)
        self.tableModel.setName('table')

    def setDealerType(self, type):
        self.dealerType = type
        self.createDealer(self.dealerType)

    def setDealerName(self, name):
        self.dealerName = name

    def setAIList(self, list):
        self.AIList = list
        self.createAIPlayers(self.AIList)

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)

    def setSeatsLOD(self, highest):
        for node in self.seatLodNodeArray:
            if node:
                if highest:
                    node.forceSwitch(node.getHighestSwitch())
                else:
                    node.clearForceSwitch()

    def setTableInfo(self, type):
        self.stacksArray = []
        self.stackArray = []
        self.seatLocatorArray = []
        self.maximum_stacks = 5
        if type == 1:
            self.tableModel = loader.loadModel('models/props/table_bar_round_parlor')
            self.tableModel.setH(11)
            self.tableModel.flattenStrong()
            self.seatLocatorArray.append(self.tableModel.find('**/seat_1'))
            self.seatLocatorArray.append(self.tableModel.find('**/seat_2'))
            self.seatLocatorArray.append(self.tableModel.find('**/seat_3'))
            self.seatLocatorArray.append(self.tableModel.find('**/seat_4'))
            self.seatLocatorArray.append(self.tableModel.find('**/seat_5'))
            self.seatLocatorArray.append(self.tableModel.find('**/seat_6'))
            self.seatLocatorArray.append(self.tableModel.find('**/seat_7'))
            self.seatLocatorArray.append(self.tableModel.find('**/seat_8'))
            self.seatLocatorArray.append(self.tableModel.find('**/pot'))
            length = len(self.seatLocatorArray)
            for i in range(length):
                stacks = loader.loadModel('models/props/coinstacks')
                stacks.setLightOff()
                self.stacksArray.append(stacks)
                seat = self.seatLocatorArray[i]
                if seat:
                    if stacks:
                        stacks.reparentTo(seat)
                        stacks.setScale(1.55)
                        stack = stacks.find('**/stack_1')
                        self.stackArray.append(stack)
                        if stack:
                            stack.hide()
                        stack = stacks.find('**/stack_2')
                        self.stackArray.append(stack)
                        if stack:
                            stack.hide()
                        stack = stacks.find('**/stack_3')
                        self.stackArray.append(stack)
                        if stack:
                            stack.hide()
                        stack = stacks.find('**/stack_4')
                        self.stackArray.append(stack)
                        if stack:
                            stack.hide()
                        stack = stacks.find('**/stack_5')
                        self.stackArray.append(stack)
                        if stack:
                            stack.hide()

            text = self.getInteractText()
            self.setInteractOptions(proximityText=text, sphereScale=9, diskRadius=12)
            self.DealerPos = (
             Vec3(0, 6.5, 0), Vec3(180, 0, 0))
            self.HandPos = (Vec3(0, 1, 0), Vec3(0, -1, 0))
            self.NumSeats = 7
            self.SeatInfo = []
            self.SeatAnim = []
            self.PocketCards = []
            self.PocketCardPositions = []
            self.actors = []
            self.seatRadius = 6
            self.sittingOffset = -1.75
            degreeIncrement = 360 / (self.NumSeats + 1)
            for i in range(self.NumSeats + 1):
                if i != self.NumSeats:
                    self.actors.append(0)
                    self.SeatAnim.append(0)
                seat = NodePath('seat-%s' % i)
                seat.setH(-(i * degreeIncrement + 180) % 360)
                seatNode = NodePath('seatNode-%s' % i)
                seatNode.reparentTo(seat)
                seatNode.setY(-self.seatRadius)
                self.SeatInfo.append(seatNode)
                stool = loader.loadModel('models/props/stool_bar')
                lod = stool.find('**/+LODNode')
                if lod:
                    node = lod.node()
                    if node:
                        self.seatLodNodeArray.append(node)
                stool.setY(-0.9)
                stool.setZ(0.05)
                stool.flattenStrong()
                stool.reparentTo(seatNode)
                cardPos = NodePath('pocketCard-%s' % i)
                cardPos.reparentTo(seatNode)
                cardPos.setY(1.5)
                cardPos.setZ(3)
                self.PocketCardPositions.append(cardPos)
                for card in range(self.maxHandCards):
                    c = loader.loadModel('models/handheld/cards_1_high')
                    c.flattenStrong()
                    c.setTwoSided(1)
                    c.hide()
                    c.reparentTo(self)
                    self.PocketCards.append(c)

                self.displayStacks(i, 0)
                seat.reparentTo(self)

            self.displayStacks(self.getPotSeat(), 0)

    def randomInteger(self, length):
        return int(random.random() * length)

    def randomArraySelection(self, array):
        return array[self.randomInteger(len(array))]

    def createAiPlayerName(self, female, seed):
        state = random.getstate()
        random.seed(seed)
        if female:
            first_name_array = PLocalizer.PirateNames_FirstNamesFemale
        else:
            first_name_array = PLocalizer.PirateNames_FirstNamesMale
        last_name_prefix_array = PLocalizer.PirateNames_LastNamePrefixesGeneric
        last_name_suffix_array = PLocalizer.PirateNames_LastNameSuffixesGeneric
        string = ''
        string = string + self.randomArraySelection(first_name_array) + ' '
        string = string + self.randomArraySelection(last_name_prefix_array)
        string = string + self.randomArraySelection(last_name_suffix_array)
        random.setstate(state)
        return string

    def setAiPlayerName(self, avatar, name):
        if avatar:
            avatar.setName(name)
            avatar.name = name

    def _getActor(self, type=PiratesGlobals.VILLAGER_TEAM):
        if type == PiratesGlobals.VILLAGER_TEAM:
            return Townfolk.Townfolk()
        else:
            actor = Skeleton.Skeleton()
            chosenType, self.possibleUndeadTypes = AvatarTypes.pickPokerUndead(self.possibleUndeadTypes)
            self.possibleUndeadTypes.remove(chosenType)
            actor.setAvatarType(chosenType)
            actor.name, self.possibleUndeadNames = PLocalizer.pickPokerUndeadName(self.possibleUndeadNames)
            self.possibleUndeadNames.remove(actor.name)
            actor.addActive()
            actor.nametag3d.setPos(0, 0, 0)
        return actor

    def _getAvTeamFromVariation(self):
        if self.gameVariation == PiratesGlobals.PARLORGAME_VARIATION_UNDEAD:
            return PiratesGlobals.UNDEAD_TEAM
        return PiratesGlobals.VILLAGER_TEAM

    def createDealer(self, type):
        self.dealer = self._getActor(self._getAvTeamFromVariation())
        name = 'Dealer'
        if self._getAvTeamFromVariation() == PiratesGlobals.VILLAGER_TEAM:
            dna = HumanDNA.HumanDNA()
            dna.makeNPCTownfolk(seed=self.doId)
            dna.setName(name)
            dna.clothes.coat = 0
            dna.clothes.vest = 2
            dna.clothes.vestTexture = 4
            dna.clothes.vestColor = 13
            dna.clothes.shirt = 10
            self.dealer.setDNAString(dna)
            self.dealer.generateHuman(dna.gender, self.cr.human)
            self.setAiPlayerName(self.dealer, name)
        else:
            self.setAiPlayerName(self.dealer, name)
        self.dealer.reparentTo(self.SeatInfo[-1])
        self.dealer.setX(self.sittingOffset)
        self.dealer.hideShadow()
        self.dealer.disableMixing()
        self.dealer.loop('deal_idle')
        deck = loader.loadModel('models/handheld/cards_deck_high')
        deck.flattenStrong()
        topCard = loader.loadModel('models/handheld/cards_1_high')
        topCard.flattenStrong()
        deck.reparentTo(self.dealer.leftHandNode)
        topCard.reparentTo(self.dealer.leftHandNode)

    def createAIPlayers(self, AIList):
        self.AIPlayers = [
         0] * self.NumSeats
        for i in range(len(AIList)):
            if AIList[i] == 0:
                pass
            else:
                aiplayer = self._getActor(AIList[i])
                self.AIPlayers[i] = aiplayer
                self.actors[i] = aiplayer
                if AIList[i] == PiratesGlobals.VILLAGER_TEAM:
                    dna = HumanDNA.HumanDNA()
                    dna.makeNPCPirate(seed=self.doId + i)
                    aiplayer.setDNAString(dna)
                    aiplayer.generateHuman(dna.gender, self.cr.human)
                    name = None
                else:
                    name = aiplayer.getName()
                aiplayer.reparentTo(self.SeatInfo[i])
                aiplayer.setX(self.sittingOffset)
                female = False
                if AIList[i] == PiratesGlobals.VILLAGER_TEAM and dna.gender == 'f':
                    female = True
                seed = self.doId + i
                if not name:
                    name = self.createAiPlayerName(female, seed)
                    self.setAiPlayerName(aiplayer, name)
                if AIList[i] == PiratesGlobals.VILLAGER_TEAM:
                    aiplayer.hideShadow()
                aiplayer.disableMixing()
                aiplayer.loop('sit_idle')

        return

    def requestInteraction(self, avId, interactType=0):
        base.localAvatar.motionFSM.off()
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        base.localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def deleteRequestDialogs(self):
        if self.requestDialog:
            self.requestDialog.destroy()
            del self.requestDialog
            self.requestDialog = None
        return

    def requestCommand(self, value):
        self.deleteRequestDialogs()

    def requestSeatResponse(self, answer, seatIndex):
        if answer == 1:
            self.localAvatarSatDown(seatIndex)
            localAvatar.guiMgr.hideSeaChest()
            localAvatar.b_setGameState('ParlorGame')
        elif answer == 2:
            self.localAvatarGotUp(seatIndex)
        elif answer == 3:
            self.deleteRequestDialogs()
            self.requestDialog = PDialog.PDialog(text=PLocalizer.TableIsFullMessage, style=OTPDialog.Acknowledge, command=self.requestCommand)
            self.setDialogBin(self.requestDialog)
            localAvatar.motionFSM.on()
            self.cr.interactionMgr.start()
        elif answer == 5:
            localAvatar.guiMgr.showNonPayer(quest='Game_Table', focus=6)
            localAvatar.motionFSM.on()
            self.cr.interactionMgr.start()
        else:
            localAvatar.motionFSM.on()
            self.cr.interactionMgr.start()

    def localAvatarSatDown(self, seatIndex):
        self.actors[seatIndex] = localAvatar
        self.localAvatarSeat = seatIndex
        self.createGui()
        localAvatar.reparentTo(self.SeatInfo[seatIndex])
        localAvatar.setPos(self.sittingOffset, 0, 0)
        localAvatar.loop('idle')
        localAvatar.setHpr(0, 0, 0)
        satDown = Func(self.satDown, seatIndex)
        disableMixing = Func(localAvatar.disableMixing)
        sit = localAvatar.actorInterval('sit', mixingWanted=False)
        sit_idle = Func(localAvatar.loop, 'sit_idle')
        acceptInt = Func(self.acceptInteraction)
        sittingSeq = Sequence(satDown, disableMixing, sit, sit_idle, acceptInt)
        self.saveSequence(sittingSeq, localAvatar)
        sittingSeq.start()
        self.setSeatsLOD(True)

    def satDown(self, seatIndex):
        pass

    def createGui(self):
        pass

    def localAvatarGotUp(self, seatIndex):
        self.actors[seatIndex] = 0
        self.localAvatarSeat = -1

        def restore():
            localAvatar.setControlEffect('sit', 0)
            localAvatar.enableMixing()
            localAvatar.loop('idle')
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
            if localAvatar.guiMgr.seaChestActive:
                localAvatar.guiMgr.showChestTray()
            self.reparentAndMoveInRelationTo(localAvatar, self.getParent(), self.SeatInfo[seatIndex].getPos(self.getParent()))

        sittingSeq = Sequence(Func(self.gotUp, seatIndex), Func(localAvatar.disableMixing), localAvatar.actorInterval('sit', playRate=-1, mixingWanted=False), Func(restore), Func(self.setSeatsLOD, False))
        self.saveSequence(sittingSeq, localAvatar)
        sittingSeq.start()

    def gotUp(self, seatIndex):
        pass

    def setAvatarSeat(self, players):
        for seatIndex in range(len(players)):
            avId = players[seatIndex]
            if avId > 0 and avId != localAvatar.doId:
                avatar = self.cr.doId2do.get(avId)
                if avatar:
                    self.actors[seatIndex] = avatar
                    avatar.stopSmooth()
                    avatar.reparentTo(self.SeatInfo[seatIndex])
                    avatar.setPos(self.sittingOffset, 0, 0)
                    avatar.setHpr(0, 0, 0)
                    avatar.disableMixing()
                    if self.SeatAnim[seatIndex] == 0:
                        avatar.loop('sit_idle')
            elif avId == 0 and self.AIPlayers[seatIndex] == 0:
                self.actors[seatIndex] = 0

    def avatarSit(self, avId, seatIndex):
        if avId != localAvatar.doId:
            avatar = self.cr.doId2do.get(avId)
            if avatar:
                avatar.stopSmooth()
                avatar.reparentTo(self.SeatInfo[seatIndex])
                avatar.setPos(self.sittingOffset, 0, 0)
                avatar.setHpr(0, 0, 0)
                self.SeatAnim[seatIndex] = 1
                avatar.disableMixing()
                sit = avatar.actorInterval('sit', mixingWanted=False)
                sit_idle = Func(avatar.loop, 'sit_idle')
                setAnim = Func(self.setSeatAnim, seatIndex, 0)
                sittingSeq = Sequence(sit, sit_idle, setAnim)
                self.saveSequence(sittingSeq, avatar)
                sittingSeq.start()

    def avatarStand(self, avId, seatIndex):
        if avId != localAvatar.doId:
            avatar = self.cr.doId2do.get(avId)
            if avatar:
                self.SeatAnim[seatIndex] = 1
                avatar.disableMixing()
                stand = avatar.actorInterval('sit', playRate=-1, mixingWanted=False)
                enableMixing = Func(avatar.enableMixing)
                idle = Func(avatar.loop, 'idle')
                setAnim = Func(self.setSeatAnim, seatIndex, 0)
                relocate = Func(self.reparentAndMoveInRelationTo, avatar, self.getParent(), self.SeatInfo[seatIndex].getPos(self.getParent()))
                standSeq = Sequence(stand, enableMixing, idle, setAnim, relocate)
                self.saveSequence(standSeq, avatar)
                standSeq.start()

    def setSeatAnim(self, index, value):
        self.SeatAnim[index] = value

    def reparentAndMoveInRelationTo(self, object, parent, pos):
        object.setPos(pos)
        object.reparentTo(parent)
        object.startSmooth()

    def disable(self):
        DistributedInteractive.DistributedInteractive.disable(self)
        self.ignoreAll()
        avIds = self.avId2ivals.keys()
        for avId in avIds:
            for ival in self.avId2ivals.get(avId, []):
                ival.finish()

        del self.avId2ivals
        self.tableModel.removeNode()
        del self.tableModel
        if self.dealer:
            self.dealer.removeActive()
            self.dealer.delete()
            del self.dealer
        for townfolk in self.AIPlayers:
            if townfolk:
                townfolk.removeActive()
                townfolk.delete()

        del self.AIPlayers
        del self.actors
        for n in self.PocketCards:
            n.removeNode()

        del self.PocketCards
        del self.SeatInfo
        del self.SeatAnim

    def delete(self):
        DistributedInteractive.DistributedInteractive.delete(self)
        self.removeNode()

    def isLocalAvatarPlaying(self):
        self.notify.warning('isLocalAvatarPlaying() is deprecated. See isLocalAvatarSeated().')
        return self.isLocalAvatarSeated()

    def isLocalAvatarSeated(self):
        return self.localAvatarSeat != -1

    def receiveAISpeech(self, seat, messageTag):
        if self.AIList[seat] == 0:
            return
        else:
            message = eval('PLocalizer.' + messageTag)
            self.AIPlayers[seat].setChatAbsolute(message, CFSpeech | CFTimeout)

    def receiveAIThoughts(self, seat, message):
        pass

    def setDialogBin(self, dialog):
        dialog.setBin('gui-fixed', 10, 10)

    display_1 = [
     [
      0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [1, 0, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 0, 0], [1, 0, 1, 0, 0], [0, 1, 1, 0, 0], [1, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 1, 0, 1, 0], [1, 0, 0, 1, 0], [0, 0, 1, 1, 0], [0, 1, 1, 1, 0], [1, 0, 1, 1, 0]]
    display_2 = [
     [
      1, 1, 1, 1, 0], [0, 0, 0, 0, 1], [0, 1, 0, 0, 1], [1, 0, 0, 0, 1], [1, 1, 0, 0, 1], [0, 0, 1, 0, 1], [0, 0, 1, 0, 1], [0, 1, 1, 0, 1], [1, 0, 1, 0, 1], [0, 1, 1, 0, 1], [1, 0, 1, 0, 1], [0, 0, 0, 1, 1], [0, 1, 0, 1, 1], [1, 0, 0, 1, 1], [0, 0, 1, 1, 1], [0, 1, 1, 1, 1], [1, 0, 1, 1, 1]]
    display_3 = [
     1, 1, 1, 1, 1]

    def numberToStackDisplay(self, number):
        stack_display = self.display_1[0]
        if number >= 0 and number <= 15:
            stack_display = self.display_1[number]
        if number >= 16 and number <= 32:
            stack_display = self.display_2[number - 16]
        if number >= 33:
            stack_display = self.display_3
        return stack_display

    def displayStacks(self, seat, number):
        offset = seat * self.maximum_stacks
        stack_display = self.numberToStackDisplay(number)
        length = len(stack_display)
        for i in range(length):
            stack = self.stackArray[offset + i]
            if stack:
                if stack_display[i]:
                    stack.show()
                else:
                    stack.hide()

    def getPotSeat(self):
        return self.NumSeats + 1

    def updateStacks(self, chipsArray):
        for seat in range(self.NumSeats):
            self.displayStacks(seat, chipsArray[seat])