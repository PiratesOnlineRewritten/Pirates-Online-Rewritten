import sys
import os
import tokenize
import copy
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import PythonUtil, DirectObject
from direct.showbase import AppRunnerGlobal
from otp.speedchat import SpeedChatGlobals
from pirates.piratesgui import NewTutorialPanel
from pirates.npc import Skeleton
from pirates.pirate import Pirate
from pirates.pirate import HumanDNA
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import RadarGui
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.inventory import ItemGlobals
from pirates.inventory.InventoryGlobals import Locations
notify = DirectNotifyGlobal.directNotify.newCategory('QuestParser')
lineDict = {}
globalVarDict = {}
funcDefs = {}
curId = None
currFuncId = None
subtitleEvent = 'subtitleConfirm'

def Nothing():
    pass


def init():
    globalVarDict.update({'render': render,'camera': camera,'hidden': hidden,'aspect2d': aspect2d,'localToon': base.localAvatar,'inventory': base.localAvatar.inventory})


def clear():
    globalVarDict.clear()


def readFile(filename):
    global curId
    global currFuncId
    notify.debug('THE PARSED FILE IS %s' % filename)
    lastReadFile = filename
    scriptFile = StreamReader(vfs.openReadFile(filename, 1), 1)
    gen = tokenize.generate_tokens(scriptFile.readline)
    line = getLineOfTokens(gen)
    while line is not None:
        if line == []:
            line = getLineOfTokens(gen)
            continue
        if line[0] == 'ID':
            parseId(line)
        elif line[0] == 'FUNC_DEF':
            parseFuncDef(line)
        elif currFuncId:
            funcDefs[currFuncId].append(line)
        else:
            lineDict[curId].append(line)
        line = getLineOfTokens(gen)

    return


def reReadFile():
    if lastReadFile:
        readFile(lastReadFile)


def getLineOfTokens(gen):
    tokens = []
    nextNeg = 0
    token = gen.next()
    if token[0] == tokenize.ENDMARKER:
        return None
    while token[0] != tokenize.NEWLINE and token[0] != tokenize.NL:
        if token[0] == tokenize.COMMENT:
            pass
        elif token[0] == tokenize.OP and token[1] == '-':
            nextNeg = 1
        elif token[0] == tokenize.NUMBER:
            if nextNeg:
                tokens.append(-eval(token[1]))
                nextNeg = 0
            else:
                tokens.append(eval(token[1]))
        elif token[0] == tokenize.STRING:
            tokens.append(eval(token[1]))
        elif token[0] == tokenize.NAME:
            tokens.append(token[1])
        else:
            notify.warning('Ignored token type: %s on line: %s' % (tokenize.tok_name[token[0]], token[2][0]))
        token = gen.next()

    return tokens


def parseId(line):
    global curId
    global currFuncId
    curId = line[1]
    currFuncId = None
    notify.debug('Setting current scriptId to: %s' % curId)
    lineDict[curId] = []
    return


def parseFuncDef(line):
    global curId
    global currFuncId
    currFuncId = line[1]
    curId = None
    notify.debug('Setting current funcDef to: %s' % currFuncId)
    funcDefs[currFuncId] = []
    return


def questDefined(scriptId):
    return lineDict.has_key(scriptId)


class NPCMoviePlayer(DirectObject.DirectObject):

    def __init__(self, scriptId, toon, npc):
        print 'initializing movie player'
        self.scriptId = scriptId
        self.toon = toon
        self.isLocalToon = self.toon == base.localAvatar
        if self.isLocalToon:
            self.toon.currentDialogMovie = self
        self.npc = npc
        self.privateVarDict = {}
        self.toonHeads = {}
        self.chars = []
        self.uniqueId = 'scriptMovie_' + str(self.scriptId) + '_' + str(toon.getDoId()) + '_' + str(npc.getDoId())
        self.setVar('toon', self.toon)
        self.setVar('npc', self.npc)
        self.chapterDict = {}
        self.timeoutTrack = None
        self.currentTrack = None
        self.events = {}
        self.npcTeam = None
        self.cleanedUp = False
        self.changeGameState = True
        self.oldGameState = None
        self.gameStateLock = None
        self.enableLock = None
        self.enableCameraLock = None
        self.compassPirate = None
        self.compassSkeleton = None
        self.msgPanelCount = 0
        self.dialogues = []
        return

    def getVar(self, varName):
        if len(globalVarDict) == 0:
            init()
        if self.privateVarDict.has_key(varName):
            return self.privateVarDict[varName]
        elif globalVarDict.has_key(varName):
            return globalVarDict[varName]
        else:
            notify.error('Variable not defined: %s' % varName)

    def delVar(self, varName):
        if self.privateVarDict.has_key(varName):
            del self.privateVarDict[varName]
        elif globalVarDict.has_key(varName):
            del globalVarDict[varName]
        else:
            notify.warning('Variable not defined: %s' % varName)

    def setVar(self, varName, var):
        self.privateVarDict[varName] = var

    def cleanup(self):
        if self.cleanedUp == True:
            return
        if self.isLocalToon and self.toon.currentDialogMovie is self:
            self.toon.currentDialogMovie = None
        if self.currentTrack:
            self.currentTrack.pause()
            self.currentTrack = None
        self.ignoreAll()
        taskMgr.remove(self.uniqueId)
        for toonHeadFrame in self.toonHeads.values():
            toonHeadFrame.destroy()

        while self.chars:
            self.__unloadChar(self.chars[0])

        del self.toonHeads
        del self.privateVarDict
        del self.chapterDict
        del self.toon
        del self.npc
        del self.timeoutTrack
        self.cleanedUp = True
        if self.oldGameState:
            if not self.enableLock:
                localAvatar.gameFSM.lockFSM = False
            localAvatar.b_setGameState(self.oldGameState)
            localAvatar.gameFSM.lockFSM = self.gameStateLock
            self.oldGameState = None
        for dialogue in self.dialogues:
            if dialogue:
                dialogue.stop()

        self.dialogues = []
        return

    def __unloadChar(self, char):
        char.removeActive()
        if char.style.name == 'mk' or char.style.name == 'mn':
            char.stopEarTask()
        char.delete()
        self.chars.remove(char)

    def timeout(self, fFinish=0):
        if self.timeoutTrack:
            if fFinish:
                self.timeoutTrack.finish()
            else:
                self.timeoutTrack.start()

    def finishMovie(self):
        messenger.send('dialogFinish')
        base.localAvatar.guiMgr.subtitler.clearText()
        self.cleanup()

    def finish(self):
        self.currentTrack.pause()
        self.npc.showName()
        self.npc.nametag3d.setZ(0)

    def finishUpAll(self):
        if self.currentTrack:
            self.currentTrack.finish()
        if self.cleanedUp == True:
            return
        trackList = self.chapterDict.keys()
        for currTrack in trackList:
            if self.cleanedUp == False and len(self.chapterDict[currTrack]) > 0:
                self.currentTrack = self.chapterDict[currTrack].pop(0)
                self.currentTrack.start()
                self.currentTrack.finish()

        self.cleanup()
        messenger.send('closeTutorialWindow')

    def overrideOldAvState(self, avState):
        oldGameState = self.oldGameState
        self.oldGameState = avState
        self.gameStateLock = localAvatar.gameFSM.lockFSM
        return oldGameState

    def playNextChapter(self, eventName, timeStamp=0.0):
        trackList = self.chapterDict[eventName]
        if trackList:
            self.currentTrack = trackList.pop(0)
            self.currentTrack.start()
        else:
            notify.debug('Movie ended waiting for an event (%s)' % eventName)

    def play(self):
        lineNum = 0
        self.currentEvent = 'start'
        lines = lineDict.get(self.scriptId)
        if lines is None:
            notify.error('No movie defined for scriptId: %s' % self.scriptId)
        chapterList = []
        timeoutList = []
        print self.npc
        print self.toon
        for currEvent in self.events.keys():
            self.ignore(currEvent)

        self.events = {}
        for line in lines:
            print line
            lineNum += 1
            command = line[0]
            chapterList, nextEvent = self.parseLine(command, line, chapterList, timeoutList, lineNum)
            if nextEvent:
                self.closePreviousChapter(chapterList)
                chapterList = []
                self.currentEvent = nextEvent

        self.closePreviousChapter(chapterList)
        if timeoutList:
            self.timeoutTrack = Sequence(*timeoutList)
        self.playNextChapter('start')
        localAvatar.guiMgr.combatTray.hideSkills()
        localAvatar.guiMgr.combatTray.disableTray()
        if self.changeGameState and localAvatar.gameFSM.state != 'Dialog':
            self.oldGameState = localAvatar.gameFSM.state
            self.gameStateLock = localAvatar.gameFSM.lockFSM
            localAvatar.b_setGameState('Dialog')
        return

    def parseFuncDefLines(self, funcDef):
        lineNum = 0
        lines = funcDef
        if lines is None:
            notify.error('No movie defined for scriptId: %s' % self.scriptId)
        lineList = []
        timeoutList = []
        for line in lines:
            print line
            lineNum += 1
            command = line[0]
            lineList, nextEvent = self.parseLine(command, line, lineList, timeoutList, lineNum)

        return (
         Sequence(*lineList), nextEvent)

    def parseLine(self, command, line, chapterList, timeoutList, lineNum=-1):
        resultingNextEvent = None
        if command == 'UPON_TIMEOUT':
            uponTimeout = 1
            iList = timeoutList
            line = line[1:]
            command = line[0]
        else:
            uponTimeout = 0
            iList = chapterList
        if command == 'CALL':
            if uponTimeout:
                self.notify.error('CALL not allowed in an UPON_TIMEOUT')
            iList.append(self.parseCall(line))
            return (
             chapterList, resultingNextEvent)
        else:
            if command == 'DEBUG':
                iList.append(self.parseDebug(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'WAIT':
                if uponTimeout:
                    self.notify.error('WAIT not allowed in an UPON_TIMEOUT')
                iList.append(self.parseWait(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'CHAT':
                iList.append(self.parseChat(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'CLEAR_CHAT':
                iList.append(self.parseClearChat(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'INTERACTIONAL_CHAT':
                iList.append(self.parseInteractionalChat(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'CLEAR_INTERACTIONAL_CHAT':
                iList.append(self.parseClearInteractionalChat(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'FINISH_QUEST_MOVIE':
                chapterList.append(Func(self.finishMovie))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'CHAT_CONFIRM':
                if uponTimeout:
                    self.notify.error('CHAT_CONFIRM not allowed in an UPON_TIMEOUT')
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                resultingNextEvent = 'doneChatPage'
                iList.append(Func(self.acceptOnce, resultingNextEvent, self.playNextChapter, [
                 resultingNextEvent]))
                iList.append(self.parseChatConfirm(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'LOCAL_CHAT_CONFIRM':
                if uponTimeout:
                    self.notify.error('LOCAL_CHAT_CONFIRM not allowed in an UPON_TIMEOUT')
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                resultingNextEvent = 'doneChatPage'
                iList.append(Func(self.acceptOnce, resultingNextEvent, self.playNextChapter, [
                 resultingNextEvent]))
                iList.append(self.parseLocalChatConfirm(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'LOCAL_CHAT_PERSIST':
                iList.append(self.parseLocalChatPersist(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'LOCAL_CHAT_TO_CONFIRM':
                if uponTimeout:
                    self.notify.error('LOCAL_CHAT_TO_CONFIRM not allowed in an UPON_TIMEOUT')
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                resultingNextEvent = 'doneChatPage'
                iList.append(Func(self.acceptOnce, resultingNextEvent, self.playNextChapter, [
                 resultingNextEvent]))
                iList.append(self.parseLocalChatToConfirm(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'CC_CHAT_CONFIRM':
                if uponTimeout:
                    self.notify.error('CC_CHAT_CONFIRM not allowed in an UPON_TIMEOUT')
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                resultingNextEvent = 'doneChatPage'
                iList.append(Func(self.acceptOnce, resultingNextEvent, self.playNextChapter, [
                 resultingNextEvent]))
                iList.append(self.parseCCChatConfirm(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'CC_CHAT_TO_CONFIRM':
                if uponTimeout:
                    self.notify.error('CC_CHAT_TO_CONFIRM not allowed in an UPON_TIMEOUT')
                avatarName = line[1]
                avatar = self.getVar(avatarName)
                resultingNextEvent = 'doneChatPage'
                iList.append(Func(self.acceptOnce, resultingNextEvent, self.playNextChapter, [
                 resultingNextEvent]))
                iList.append(self.parseCCChatToConfirm(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'SUBTITLE_CHAT':
                iList.append(self.parseSubtitleChat(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'SUBTITLE_CHAT_ANIM':
                newList, resultingNextEvent = self.parseSubtitleChatAnim(line)
                iList.append(newList)
                return (
                 chapterList, resultingNextEvent)
            elif command == 'SUBTITLE_CLEAR_CHAT':
                iList.append(self.parseSubtitleClearChat(line))
                return (
                 chapterList, resultingNextEvent)
            elif command == 'SUBTITLE_CHAT_CONFIRM':
                if uponTimeout:
                    self.notify.error('SUBTITLE_CHAT_CONFIRM not allowed in an UPON_TIMEOUT')
                iList.append(Func(self.acceptOnce, subtitleEvent, self.playNextChapter, [
                 subtitleEvent]))
                iList.append(self.parseSubtitleChatConfirm(line))
                return (
                 chapterList, subtitleEvent)
            if self.isLocalToon:
                if command == 'LOAD':
                    self.parseLoad(line)
                elif command == 'LOAD_SFX':
                    self.parseLoadSfx(line)
                elif command == 'LOAD_DIALOGUE':
                    self.parseLoadDialogue(line)
                elif command == 'SIMPLE_DIALOGUE':
                    self.changeGameState = False
                elif command == 'LOAD_CC_DIALOGUE':
                    self.parseLoadCCDialogue(line)
                elif command == 'LOAD_CHAR':
                    self.parseLoadChar(line)
                elif command == 'LOAD_CLASSIC_CHAR':
                    self.parseLoadClassicChar(line)
                elif command == 'UNLOAD_CHAR':
                    iList.append(self.parseUnloadChar(line))
                elif command == 'LOAD_SUIT':
                    self.parseLoadSuit(line)
                elif command == 'SET':
                    self.parseSet(line)
                elif command == 'LOCK_LOCALTOON':
                    iList.append(self.parseLockLocalToon(line))
                elif command == 'FREE_LOCALTOON':
                    iList.append(self.parseFreeLocalToon(line))
                elif command == 'REPARENTTO':
                    iList.append(self.parseReparent(line))
                elif command == 'WRTREPARENTTO':
                    iList.append(self.parseWrtReparent(line))
                elif command == 'SHOW':
                    iList.append(self.parseShow(line))
                elif command == 'HIDE':
                    iList.append(self.parseHide(line))
                elif command == 'STASH_UID':
                    iList.append(self.parseStashUid(line))
                elif command == 'UNSTASH_UID':
                    iList.append(self.parseStashUid(line, False))
                elif command == 'POS':
                    iList.append(self.parsePos(line))
                elif command == 'SETX':
                    iList.append(self.parseSetX(line))
                elif command == 'SETY':
                    iList.append(self.parseSetY(line))
                elif command == 'SETZ':
                    iList.append(self.parseSetZ(line))
                elif command == 'SETNAMETAGZ':
                    iList.append(self.parseSetNametagZ(line))
                elif command == 'HPR':
                    iList.append(self.parseHpr(line))
                elif command == 'SETH':
                    iList.append(self.parseSetH(line))
                elif command == 'SETP':
                    iList.append(self.parseSetP(line))
                elif command == 'SETR':
                    iList.append(self.parseSetR(line))
                elif command == 'SCALE':
                    iList.append(self.parseScale(line))
                elif command == 'LOOKAT':
                    iList.append(self.parseLookAt(line))
                elif command == 'LOOKATFACE':
                    iList.append(self.parseLookAtFace(line))
                elif command == 'POSHPRSCALE':
                    iList.append(self.parsePosHprScale(line))
                elif command == 'COLOR':
                    iList.append(self.parseColor(line))
                elif command == 'COLOR_SCALE':
                    iList.append(self.parseColorScale(line))
                elif command == 'ADD_LAFFMETER':
                    iList.append(self.parseAddLaffMeter(line))
                elif command == 'LAFFMETER':
                    iList.append(self.parseLaffMeter(line))
                elif command == 'OBSCURE_LAFFMETER':
                    iList.append(self.parseObscureLaffMeter(line))
                elif command == 'ARROWS_ON':
                    iList.append(self.parseArrowsOn(line))
                elif command == 'ARROWS_OFF':
                    iList.append(self.parseArrowsOff(line))
                elif command == 'START_THROB':
                    iList.append(self.parseStartThrob(line))
                elif command == 'STOP_THROB':
                    iList.append(self.parseStopThrob(line))
                elif command == 'SHOW_FRIENDS_LIST':
                    iList.append(self.parseShowFriendsList(line))
                elif command == 'HIDE_FRIENDS_LIST':
                    iList.append(self.parseHideFriendsList(line))
                elif command == 'OBSCURE_CHAT':
                    iList.append(self.parseObscureChat(line))
                elif command == 'ADD_INVENTORY':
                    iList.append(self.parseAddInventory(line))
                elif command == 'SET_INVENTORY':
                    iList.append(self.parseSetInventory(line))
                elif command == 'SET_INVENTORY_YPOS':
                    iList.append(self.parseSetInventoryYPos(line))
                elif command == 'SET_INVENTORY_DETAIL':
                    iList.append(self.parseSetInventoryDetail(line))
                elif command == 'PLAY_SFX':
                    iList.append(self.parsePlaySfx(line))
                elif command == 'STOP_SFX':
                    iList.append(self.parseStopSfx(line))
                elif command == 'PLAY_ANIM':
                    iList.append(self.parsePlayAnim(line))
                elif command == 'LOOP_ANIM':
                    iList.append(self.parseLoopAnim(line))
                elif command == 'LERP_POS':
                    iList.append(self.parseLerpPos(line))
                elif command == 'LERP_HPR':
                    iList.append(self.parseLerpHpr(line))
                elif command == 'LERP_SCALE':
                    iList.append(self.parseLerpScale(line))
                elif command == 'LERP_POSHPRSCALE':
                    iList.append(self.parseLerpPosHprScale(line))
                elif command == 'LERP_COLOR':
                    iList.append(self.parseLerpColor(line))
                elif command == 'LERP_COLOR_SCALE':
                    iList.append(self.parseLerpColorScale(line))
                elif command == 'DEPTH_WRITE_ON':
                    iList.append(self.parseDepthWriteOn(line))
                elif command == 'DEPTH_WRITE_OFF':
                    iList.append(self.parseDepthWriteOff(line))
                elif command == 'DEPTH_TEST_ON':
                    iList.append(self.parseDepthTestOn(line))
                elif command == 'DEPTH_TEST_OFF':
                    iList.append(self.parseDepthTestOff(line))
                elif command == 'SET_BIN':
                    iList.append(self.parseSetBin(line))
                elif command == 'CLEAR_BIN':
                    iList.append(self.parseClearBin(line))
                elif command == 'TOON_HEAD':
                    iList.append(self.parseToonHead(line))
                elif command == 'SEND_EVENT':
                    iList.append(self.parseSendEvent(line))
                elif command == 'FUNCTION':
                    iList.append(self.parseFunction(line))
                elif command == 'START_INTERACT':
                    iList.append(self.parseStartInteract(line))
                elif command == 'STOP_INTERACT':
                    iList.append(self.parseStopInteract(line))
                elif command == 'CAMERA_INTERACT':
                    iList.append(self.parseCameraInteract(line))
                elif command == 'LOCK_CAMERAFSM':
                    self.enableCameraLock = True
                elif command == 'START_NPC_INTERACT':
                    iList.append(Func(localAvatar.gameFSM.startNPCInteract, self.npc))
                elif command == 'END_NPC_INTERACT':
                    iList.append(Func(localAvatar.gameFSM.endNPCInteract))
                elif command == 'START_LETTERBOX':
                    iList.append(Func(self.letterboxOn))
                elif command == 'STOP_LETTERBOX':
                    iList.append(Func(self.letterboxOff))
                elif command == 'HIDE_GUI':
                    iList.append(Func(self.toon.guiMgr.hideTrays))
                    iList.append(Func(self.toon.guiMgr.setIgnoreAllKeys, True))
                elif command == 'SHOW_GUI':
                    iList.append(Func(self.toon.guiMgr.showTrays))
                    iList.append(Func(self.toon.guiMgr.setIgnoreAllKeys, False))
                elif command == 'SHOW_QUEST_PANEL':
                    iList.append(Func(self.toon.guiMgr.showQuestPanel))
                elif command == 'SHOW_CHEST_TRAY':
                    iList.append(Func(self.toon.guiMgr.showChestTray))
                elif command == 'HIDE_CHEST_TRAY':
                    iList.append(Func(self.toon.guiMgr.hideChestTray))
                elif command == 'ALLOW_SKILL_PAGE_ONLY':
                    iList.append(Func(self.toon.guiMgr.allowSkillPageOnly))
                elif command == 'ALLOW_LOOKOUT_PAGE_ONLY':
                    iList.append(Func(self.toon.guiMgr.allowLookoutPageOnly))
                elif command == 'ENABLE_SEA_CHEST':
                    iList.append(Func(self.toon.guiMgr.setSeaChestAllowed, True))
                elif command == 'DISABLE_SEA_CHEST':
                    iList.append(Func(self.toon.guiMgr.setSeaChestAllowed, False))
                elif command == 'IGNORE_WEAPON_KEYS_ON':
                    iList.append(Func(self.toon.guiMgr.setIgnoreAllKeys, True))
                elif command == 'IGNORE_WEAPON_KEYS_OFF':
                    iList.append(Func(self.toon.guiMgr.setIgnoreAllKeys, False))
                elif command == 'IGNORE_MAIN_MENU_KEY_ON':
                    iList.append(Func(self.toon.guiMgr.setIgnoreMainMenuHotKey, True))
                elif command == 'IGNORE_MAIN_MENU_KEY_OFF':
                    iList.append(Func(self.toon.guiMgr.setIgnoreMainMenuHotKey, False))
                elif command == 'TOGGLE_SKILL_PAGE_DEMO_ON':
                    iList.append(Func(self.toon.guiMgr.toggleSkillPageDemo, True))
                elif command == 'TOGGLE_SKILL_PAGE_DEMO_OFF':
                    iList.append(Func(self.toon.guiMgr.toggleSkillPageDemo, False))
                elif command == 'WAIT_EVENT':
                    if uponTimeout:
                        self.notify.error('WAIT_EVENT not allowed in an UPON_TIMEOUT')
                    nextEvents = self.parseWaitEvent(line)
                    resultingNextEvent = nextEvents[0]

                    def proceed(self=self, resultingNextEvent=resultingNextEvent):
                        self.playNextChapter(resultingNextEvent)

                    def handleEvent(*args):
                        proceed = args[0]
                        proceed()
                        eventNames = args[1]
                        for currEventName in eventNames:
                            self.ignore(currEventName)

                    for currNextEvent in nextEvents:
                        iList.append(Func(self.accept, currNextEvent, handleEvent, [
                         proceed, nextEvents]))

                elif command == 'WAIT_EVENT_CHAT':
                    if uponTimeout:
                        self.notify.error('WAIT_EVENT not allowed in an UPON_TIMEOUT')
                    resultingNextEvent, prompts = self.parseWaitEventChat(line)

                    def proceed(self=self, resultingNextEvent=resultingNextEvent):
                        self.currentTrack.pause()
                        self.playNextChapter(resultingNextEvent)

                    def handleEvent(*args):
                        proceed = args[0]
                        proceed()

                    iList.append(Func(self.acceptOnce, resultingNextEvent, handleEvent, [
                     proceed]))
                    for currPrompt in prompts:
                        iList.append(Wait(currPrompt[0]))
                        iList.append(currPrompt[1])

                elif command == 'SET_MUSIC_VOLUME':
                    iList.append(self.parseSetMusicVolume(line))
                elif command == 'CREATE_MSG_PANEL':
                    iList.append(self.parseCreateMsgPanel(line, 0.2, 0, 0.2))
                elif command == 'CREATE_CHAT_TUT_PANEL':
                    iList.append(self.parseCreateMsgPanel(line, 2.0, -1.0, -0.6))
                elif command == 'CLEAR_MSG_PANEL':
                    iList.append(self.parseClearMsgPanel(line))
                elif command == 'SET_TEAM':
                    iList.append(self.parseSetTeam(line))
                elif command == 'RESTORE_TEAM':
                    iList.append(self.parseRestoreTeam(line))
                elif command == 'TOGGLE_COMPASS':
                    iList.append(self.parseToggleCompass(line))
                elif command == 'DEMO_COMPASS_ICON_SHOW':
                    iList.append(self.parseDemoCompassIconShow(line))
                elif command == 'DEMO_COMPASS_ICON_HIDE':
                    iList.append(self.parseDemoCompassIconHide(line))
                elif command == 'UNEQUIP_WEAPON':
                    iList.append(self.parseUnequipWeapon(line))
                elif command == 'EQUIP_WEAPON':
                    iList.append(self.parseEquipWeapon(line))
                elif command == 'ENABLE_AIM':
                    iList.append(self.parseEnableAim(line))
                elif command == 'SET_AIM_BOUNDS':
                    iList.append(self.parseSetAimBounds(line))
                elif command == 'CLEAR_AIM_BOUNDS':
                    iList.append(self.parseClearAimBounds(line))
                elif command == 'KICK_OUT_OF_AREA':
                    iList.append(self.parseKickOutOfArea(line))
                elif command == 'PERFORM_STANDARD_CLEANUP':
                    iList.extend(self.parsePerformStandardCleanup(line))
                elif command == 'PERFORM_STANDARD_INIT':
                    iList.extend(self.parsePerformStandardInit(line))
                elif command == 'ENABLE_LOCKFSM':
                    base.localAvatar.gameFSM.lockFSM = True
                    self.gameStateLock = True
                    self.enableLock = True
                elif command == 'DISABLE_LOCKFSM':
                    base.localAvatar.gameFSM.lockFSM = False
                    self.gameStateLock = False
                    self.enableLock = None
                elif command == 'SET_EQUIPPED_WEAPONS':
                    iList.extend(self.parseSetEquippedWeapons(line))
                elif command == 'CLEAR_COMPASS_EFFECTS':
                    iList.extend(self.parseClearCompassEffects(line))
                else:
                    notify.warning('Unknown command token: %s for scriptId: %s on line: %s' % (command, self.scriptId, lineNum))
        return (
         chapterList, resultingNextEvent)

    def letterboxOn(self):
        base.transitions.letterboxOn()

    def letterboxOff(self):
        base.transitions.letterboxOff()

    def closePreviousChapter(self, iList):
        trackList = self.chapterDict.setdefault(self.currentEvent, [])
        trackList.append(Sequence(*iList))

    def parseDemoCompassIconShow(self, line):
        targetObj = localAvatar
        targetObjId = targetObj.doId
        self.npc.battleCollisionBitmask &= ~(PiratesGlobals.TargetBitmask | PiratesGlobals.RadarAvatarBitmask)
        objectType = RadarGui.RADAR_OBJ_TYPE_DEFAULT
        fadeInFunc = Func(Nothing)
        teamId = None
        if len(line) > 1:
            if line[1] == 'exit0':
                tunnelNode = localAvatar.attachNewNode('demo-node-tunnel')
                tunnelNode.setPos(localAvatar, 0, 120, 0)
                return Sequence(Func(localAvatar.guiMgr.radarGui.addDemoTunnel, tunnelNode))
            elif line[1] == 'exit1':
                return Sequence()
            elif line[1] == 'localAvatar':
                return Sequence()
            elif line[1] == 'friend':
                targetObjId = 'friend'
                pirate = Pirate.Pirate()
                style = HumanDNA.HumanDNA()
                style.makeNPCTownfolk()
                pirate.setDNAString(style)
                pirate.generateHuman(style.gender, base.cr.humanHigh)
                pirate.reparentTo(localAvatar)
                pirate.setPos(5, 10, 0.5)
                pirate.setH(150)
                pirate.loop('idle')
                pirate.hide()
                fadeInFunc = Func(pirate.fadeIn, 1.5)
                self.compassPirate = pirate
                pirateNode = localAvatar.attachNewNode('demo-node-pirate')
                pirateNode.setPos(localAvatar, 50, 75, 0)
                return Sequence(Func(localAvatar.guiMgr.radarGui.addDemoNpc, pirateNode, localAvatar.guiMgr.radarGui.DEMO_FRIEND), fadeInFunc)
            elif line[1] == 'enemy':
                targetObjId = 'enemy'
                skeleton = Skeleton.Skeleton()
                skeleton.style = '4'
                skeleton.generateSkeleton()
                skeleton.reparentTo(localAvatar)
                skeleton.setPos(-5, 10, 0.5)
                skeleton.setH(-150)
                skeleton.loop('idle')
                skeleton.hide()
                fadeInFunc = Func(skeleton.fadeIn, 1)
                self.compassSkeleton = skeleton
                skeletonNode = localAvatar.attachNewNode('demo-node-skeleton')
                skeletonNode.setPos(localAvatar, -50, 75, 0)
                return Sequence(Func(localAvatar.guiMgr.radarGui.addDemoNpc, skeletonNode, localAvatar.guiMgr.radarGui.DEMO_ENEMY), fadeInFunc)
            elif line[1] == 'quest':
                questNode = localAvatar.attachNewNode('demo-node-quest')
                questNode.setPos(localAvatar, 0, 200, 0)
                return Sequence(Func(localAvatar.guiMgr.radarGui.addDemoQuest, questNode))
        return

    def parseDemoCompassIconHide(self, line):
        return Sequence(Func(localAvatar.guiMgr.radarGui.removeRadarObject, localAvatar.doId, True), Func(localAvatar.guiMgr.radarGui.removeRadarObject, self.npc.doId, True), Func(localAvatar.guiMgr.radarGui.removeRadarObject, 'enemy', True), Func(localAvatar.guiMgr.radarGui.removeRadarObject, 'friend', True), Func(localAvatar.guiMgr.radarGui.setPos, -0.4, 0, -0.4), Func(localAvatar.guiMgr.radarGui.clearCloseUp))

    def parseToggleCompass(self, line):
        receive = False
        destPos = None
        if len(line) > 1 and line[1] == 'RECEIVE':
            receive = True
            if len(line) > 2:
                destPos = Point3(line[2], line[3], line[4])
        return Func(localAvatar.guiMgr.radarGui.toggleDisplay, receive, destPos)

    def parseCreateMsgPanel(self, line, x=-1.2, y=-1, z=-0.6):
        lineLen = len(line)
        scriptYes = scriptNo = None
        if lineLen == 2:
            string, msg = line
        else:
            if lineLen == 3:
                string, msg, scriptYes = line
            else:
                if lineLen == 4:
                    string, msg, scriptYes, scriptNo = line
                else:
                    notify.error('invalid parseCreateMsgPanel command')
                    return
                tutorialPanel = NewTutorialPanel.NewTutorialPanel(line[1:len(line)])

                def closeTutorialWindow(msg):
                    messenger.send('closeTutorialWindow')
                    messenger.send(msg)

                if scriptYes:

                    def _handleYesTutorial():
                        nmp = None
                        if scriptYes in lineDict.keys():
                            nmp = NPCMoviePlayer(scriptYes, self.toon, self.npc)
                        closeTutorialWindow(scriptYes)
                        if nmp and self.npc and hasattr(self.npc, 'currentDialogMovie') and self.npc.currentDialogMovie:
                            self.npc.swapCurrentDialogMovie(nmp)
                            nmp.play()
                        return

                    tutorialPanel.setYesCommand(_handleYesTutorial)
            if scriptNo:

                def _handleNoTutorial():
                    if scriptNo in lineDict.keys():
                        nmp = NPCMoviePlayer(scriptNo, self.toon, self.npc)
                        nmp.play()
                    closeTutorialWindow(scriptNo)

                tutorialPanel.setNoCommand(_handleNoTutorial)
        tutorialWindow = 'tutorialWindow%s' % self.msgPanelCount
        self.setVar(tutorialWindow, tutorialPanel)
        self.msgPanelCount += 1
        return Func(self.getVar(tutorialWindow).activate)

    def parseClearMsgPanel(self, line):
        return Func(messenger.send, 'closeTutorialWindowAll')

    def parseSetTeam(self, line):
        token, avatar, teamName = line
        av = self.getVar(avatar)
        self.npcTeam = av.getTeam()
        team = PiratesGlobals.teamStr2TeamId(teamName)
        return Func(av.setTeam, team)

    def parseRestoreTeam(self, line):
        if self.npcTeam:
            token, avatar = line
            av = self.getVar(avatar)
            ival = Func(av.setTeam, self.npcTeam)
            self.npcTeam = None
            return ival
        return

    def parseLoad(self, line):
        if len(line) == 3:
            token, varName, modelPath = line
            node = loader.loadModel(modelPath)
        elif len(line) == 4:
            token, varName, modelPath, subNodeName = line
            node = loader.loadModel(modelPath).find('**/' + subNodeName)
        else:
            notify.error('invalid parseLoad command')
        self.setVar(varName, node)

    def parseLoadSfx(self, line):
        token, varName, fileName = line
        sfx = base.loadSfx(fileName)
        self.setVar(varName, sfx)

    def parseLoadDialogue(self, line):
        token, varName, fileName = line
        dialogue = base.loadSfx(fileName)
        self.setVar(varName, dialogue)
        self.dialogues.append(dialogue)

    def parseLoadCCDialogue(self, line):
        token, varName, filenameTemplate = line
        if self.toon.getStyle().gender == 'm':
            classicChar = 'mickey'
        else:
            classicChar = 'minnie'
        filename = filenameTemplate % classicChar
        if base.config.GetString('language', 'english') == 'japanese':
            dialogue = base.loadSfx(filename)
        else:
            dialogue = None
        self.setVar(varName, dialogue)
        return

    def parseLoadChar(self, line):
        token, name, charType = line
        char = Char.Char()
        dna = CharDNA.CharDNA()
        dna.newChar(charType)
        char.setDNAString(dna)
        if charType == 'mk' or charType == 'mn':
            char.startEarTask()
        char.nametag.manage(base.marginManager)
        char.addActive()
        char.hideName()
        self.setVar(name, char)

    def parseLoadClassicChar(self, line):
        token, name = line
        char = Char.Char()
        dna = CharDNA.CharDNA()
        if self.toon.getStyle().gender == 'm':
            charType = 'mk'
        else:
            charType = 'mn'
        dna.newChar(charType)
        char.setDNAString(dna)
        char.startEarTask()
        char.nametag.manage(base.marginManager)
        char.addActive()
        char.hideName()
        self.setVar(name, char)
        self.chars.append(char)

    def parseUnloadChar(self, line):
        token, name = line
        char = self.getVar(name)
        track = Sequence()
        track.append(Func(self.__unloadChar, char))
        track.append(Func(self.delVar, name))
        return track

    def parseLoadSuit(self, line):
        token, name, suitType = line
        suit = Suit.Suit()
        dna = SuitDNA.SuitDNA()
        dna.newSuit(suitType)
        suit.setDNAString(dna)
        self.setVar(name, suit)

    def parseSet(self, line):
        token, varName, value = line
        self.setVar(varName, value)

    def parseCall(self, line):
        token, scriptId = line
        nmp = NPCMoviePlayer(scriptId, self.toon, self.npc)
        return Func(nmp.play)

    def parseLockLocalToon(self, line):
        return Sequence(Func(self.toon.motionFSM.off))

    def parseFreeLocalToon(self, line):
        return Sequence(Func(self.toon.motionFSM.on))

    def parseDebug(self, line):
        token, str = line
        return Func(notify.debug, str)

    def parseReparent(self, line):
        if len(line) == 3:
            token, childNodeName, parentNodeName = line
            subNodeName = None
        elif len(line) == 4:
            token, childNodeName, parentNodeName, subNodeName = line
        childNode = self.getVar(childNodeName)
        if subNodeName:
            parentNode = self.getVar(parentNodeName).find(subNodeName)
        else:
            parentNode = self.getVar(parentNodeName)
        return ParentInterval(childNode, parentNode)

    def parseWrtReparent(self, line):
        if len(line) == 3:
            token, childNodeName, parentNodeName = line
            subNodeName = None
        elif len(line) == 4:
            token, childNodeName, parentNodeName, subNodeName = line
        childNode = self.getVar(childNodeName)
        if subNodeName:
            parentNode = self.getVar(parentNodeName).find(subNodeName)
        else:
            parentNode = self.getVar(parentNodeName)
        return WrtParentInterval(childNode, parentNode)

    def parseShow(self, line):
        token, nodeName = line
        node = self.getVar(nodeName)
        return Func(node.show)

    def parseHide(self, line):
        token, nodeName = line
        node = self.getVar(nodeName)
        return Func(node.hide)

    def parseStashUid(self, line, stash=True):
        track = Sequence()
        uids = line[1:]
        for currUid in uids:
            node = base.cr.uidMgr.justGetMeMeObject(currUid)
            if node:
                if stash:
                    track.append(Func(node.stash))
                else:
                    track.append(Func(node.unstash))
            else:
                notify.warning('could not find object with uid %s' % currUid)

                def Nothing():
                    pass

                track.append(Func(Nothing))

        return track

    def parsePos(self, line):
        if len(line) == 5:
            token, nodeName, x, y, z = line
            node = self.getVar(nodeName)
            return Func(node.setPos, x, y, z)
        elif len(line) == 6:
            token, nodeName, relNodeName, x, y, z = line
            node = self.getVar(nodeName)
            relNode = self.getVar(relNodeName)
            return Func(node.setPos, relNode, x, y, z)

    def parseSetX(self, line):
        if len(line) == 3:
            token, nodeName, val = line
            node = self.getVar(nodeName)
            return Func(node.setX, val)
        elif len(line) == 4:
            token, nodeName, relNodeName, val = line
            node = self.getVar(nodeName)
            relNode = self.getVar(relNodeName)
            return Func(node.setX, relNode, val)

    def parseSetY(self, line):
        if len(line) == 3:
            token, nodeName, val = line
            node = self.getVar(nodeName)
            return Func(node.setY, val)
        elif len(line) == 4:
            token, nodeName, relNodeName, val = line
            node = self.getVar(nodeName)
            relNode = self.getVar(relNodeName)
            return Func(node.setY, relNode, val)

    def parseSetZ(self, line):
        if len(line) == 3:
            token, nodeName, val = line
            node = self.getVar(nodeName)
            return Func(node.setZ, val)
        elif len(line) == 4:
            token, nodeName, relNodeName, val = line
            node = self.getVar(nodeName)
            relNode = self.getVar(relNodeName)
            return Func(node.setZ, relNode, val)

    def parseSetNametagZ(self, line):
        if len(line) == 3:
            token, nodeName, val = line
            node = self.getVar(nodeName)
            return Func(node.nametag3d.setZ, val)
        elif len(line) == 4:
            token, nodeName, relNodeName, val = line
            node = self.getVar(nodeName)
            relNode = self.getVar(relNodeName)
            return Func(node.nametag3d.setZ, relNode, val)

    def parseHpr(self, line):
        if len(line) == 5:
            token, nodeName, h, p, r = line
            node = self.getVar(nodeName)
            return Func(node.setHpr, h, p, r)
        elif len(line) == 6:
            token, nodeName, relNodeName, h, p, r = line
            node = self.getVar(nodeName)
            relNode = self.getVar(relNodeName)
            return Func(node.setHpr, relNode, h, p, r)

    def parseSetH(self, line):
        if len(line) == 3:
            token, nodeName, val = line
            node = self.getVar(nodeName)
            return Func(node.setH, val)
        elif len(line) == 4:
            token, nodeName, relNodeName, val = line
            node = self.getVar(nodeName)
            relNode = self.getVar(relNodeName)
            return Func(node.setH, relNode, val)

    def parseSetP(self, line):
        if len(line) == 3:
            token, nodeName, val = line
            node = self.getVar(nodeName)
            return Func(node.setP, val)
        elif len(line) == 4:
            token, nodeName, relNodeName, val = line
            node = self.getVar(nodeName)
            relNode = self.getVar(relNodeName)
            return Func(node.setP, relNode, val)

    def parseSetR(self, line):
        if len(line) == 3:
            token, nodeName, val = line
            node = self.getVar(nodeName)
            return Func(node.setR, val)
        elif len(line) == 4:
            token, nodeName, relNodeName, val = line
            node = self.getVar(nodeName)
            relNode = self.getVar(relNodeName)
            return Func(node.setR, relNode, val)

    def parseLookAt(self, line):
        token, nodeName, targetNodeName = line
        targetNode = self.getVar(targetNodeName)
        node = self.getVar(nodeName)
        return Func(node.lookAt, targetNode)

    def parseLookAtFace(self, line):
        token, nodeName, targetNodeName = line
        targetNode = self.getVar(targetNodeName)
        node = self.getVar(nodeName)
        return Func(node.lookAt, targetNode.headNode)

    def parseCameraInteract(self, line):
        token, nodeName, targetNodeName = line
        track = Sequence()
        targetNode = self.getVar(targetNodeName)
        node = self.getVar(nodeName)
        track.append(Func(node.reparentTo, targetNode))
        track.append(Func(node.setPos, 3, 10, 8))
        track.append(Func(node.lookAt, targetNode))
        track.append(Func(node.setP, -20))
        return track

    def parseScale(self, line):
        token, nodeName, x, y, z = line
        node = self.getVar(nodeName)
        return Func(node.setScale, x, y, z)

    def parsePosHprScale(self, line):
        token, nodeName, x, y, z, h, p, r, sx, sy, sz = line
        node = self.getVar(nodeName)
        return Func(node.setPosHprScale, x, y, z, h, p, r, sx, sy, sz)

    def parseColor(self, line):
        token, nodeName, r, g, b, a = line
        node = self.getVar(nodeName)
        return Func(node.setColor, r, g, b, a)

    def parseColorScale(self, line):
        token, nodeName, r, g, b, a = line
        node = self.getVar(nodeName)
        return Func(node.setColorScale, r, g, b, a)

    def parseWait(self, line):
        token, waitTime = line
        return Wait(waitTime)

    def parseChat(self, line):
        print 'parsing chat line'
        toonId = self.toon.getDoId()
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        print avatar
        chatString = eval('PLocalizer.' + line[2])
        chatFlags = CFSpeech | CFTimeout
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[3:])
        if extraChatFlags:
            chatFlags |= extraChatFlags
        if len(dialogueList) > 0:
            dialogue = dialogueList[0]
        else:
            dialogue = None
        return Func(avatar.setChatAbsolute, chatString, chatFlags, dialogue)

    def parseClearChat(self, line):
        toonId = self.toon.getDoId()
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatFlags = CFSpeech | CFTimeout
        return Func(avatar.setChatAbsolute, '', chatFlags)

    def parseInteractionalChat(self, line):
        lineLen = len(line)
        avatar = self.getVar(line[1])
        text = eval('PLocalizer.' + line[2])
        audio = None
        if lineLen > 3:
            audio = self.getVar(line[3])
        return Func(localAvatar.guiMgr.createInteractionalSubtitle, text, avatar, audio)

    def parseClearInteractionalChat(self, line):
        return Func(localAvatar.guiMgr.clearInteractionalSubtitle)

    def execEventCommands(self, eventName):
        commands = self.events.get(eventName)
        if commands == None:
            return
        script, nextEvent = self.parseLine(commands)
        scriptSeq = Sequence(*script)
        scriptSeq.play()
        return

    def parseExtraChatArgs(self, args):
        quitButton = 0
        extraChatFlags = None
        dialogueList = []
        for arg in args:
            if type(arg) == type(0):
                quitButton = arg
            elif type(arg) == type(''):
                if len(arg) > 2 and arg[:2] == 'CF':
                    extraChatFlags = eval(arg)
                else:
                    dialogueList.append(self.getVar(arg))
            else:
                notify.error('invalid argument type')

        return (
         quitButton, extraChatFlags, dialogueList)

    def parseChatConfirm(self, line):
        lineLength = len(line)
        toonId = self.toon.getDoId()
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatString = eval('PLocalizer.' + line[2])
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[3:])
        return Func(avatar.setPageChat, toonId, 0, chatString, quitButton, extraChatFlags, dialogueList)

    def parseLocalChatConfirm(self, line):
        lineLength = len(line)
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatString = eval('PLocalizer.' + line[2])
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[3:])
        return Func(avatar.setLocalPageChat, chatString, quitButton, extraChatFlags, dialogueList)

    def parseLocalChatPersist(self, line):
        lineLength = len(line)
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        chatString = eval('PLocalizer.' + line[2])
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[3:])
        if len(dialogueList) > 0:
            dialogue = dialogueList[0]
        else:
            dialogue = None
        return Func(avatar.setChatAbsolute, chatString, CFSpeech, dialogue)

    def parseLocalChatToConfirm(self, line):
        lineLength = len(line)
        avatarKey = line[1]
        avatar = self.getVar(avatarKey)
        toAvatarKey = line[2]
        toAvatar = self.getVar(toAvatarKey)
        localizerAvatarName = string.capitalize(toAvatar.getName())
        toAvatarName = eval('PLocalizer.' + localizerAvatarName)
        chatString = eval('PLocalizer.' + line[3])
        chatString = chatString.replace('%s', toAvatarName)
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[4:])
        return Func(avatar.setLocalPageChat, chatString, quitButton, extraChatFlags, dialogueList)

    def parseCCChatConfirm(self, line):
        lineLength = len(line)
        avatarName = line[1]
        avatar = self.getVar(avatarName)
        if self.toon.getStyle().gender == 'm':
            chatString = eval('PLocalizer.' + line[2] % 'Mickey')
        else:
            chatString = eval('PLocalizer.' + line[2] % 'Minnie')
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[3:])
        return Func(avatar.setLocalPageChat, chatString, quitButton, extraChatFlags, dialogueList)

    def parseCCChatToConfirm(self, line):
        lineLength = len(line)
        avatarKey = line[1]
        avatar = self.getVar(avatarKey)
        toAvatarKey = line[2]
        toAvatar = self.getVar(toAvatarKey)
        localizerAvatarName = string.capitalize(toAvatar.getName())
        toAvatarName = eval('PLocalizer.' + localizerAvatarName)
        if self.toon.getStyle().gender == 'm':
            chatString = eval('PLocalizer.' + line[3] % 'Mickey')
        else:
            chatString = eval('PLocalizer.' + line[3] % 'Minnie')
        chatString = chatString.replace('%s', toAvatarName)
        quitButton, extraChatFlags, dialogueList = self.parseExtraChatArgs(line[4:])
        return Func(avatar.setLocalPageChat, chatString, quitButton, extraChatFlags, dialogueList)

    def parseSubtitleChat(self, line):
        chatString = eval('PLocalizer.' + line[1])
        if len(line) == 3:
            dialogue = self.getVar(line[2])
        else:
            dialogue = None
        if dialogue:
            return Sequence(Func(base.localAvatar.guiMgr.subtitler.showText, chatString, None, dialogue), Wait(dialogue.length()))
        else:
            return Func(base.localAvatar.guiMgr.subtitler.showText, chatString, None, dialogue)
        return

    def parseSubtitleChatAnim(self, line):
        chatString = line[1]
        funcRef = funcDefs.get(chatString)
        funcSeq = None
        nextEvent = None
        idleAnimName = None
        if funcRef:
            funcSeq, nextEvent = self.parseFuncDefLines(funcRef)
        else:
            chatString = eval('PLocalizer.' + line[1])
            funcSeq = Func(base.localAvatar.guiMgr.subtitler.showText, chatString, None, None)
        dialogue = self.getVar(line[2])
        actor = self.getVar(line[3])
        animName = line[4]
        if len(line) == 6:
            idleAnimName = line[5]
        if dialogue:
            animDuration = actor.getDuration(animName)
            seq = Sequence(Wait(2), Parallel(SoundInterval(dialogue, duration=animDuration), Sequence(actor.actorInterval(animName)), funcSeq))
            if idleAnimName:
                seq.append(Func(actor.loop, idleAnimName))
            return (seq, nextEvent)
        return

    def parseSubtitleClearChat(self, line):
        return Func(base.localAvatar.guiMgr.subtitler.clearText)

    def parseSubtitleChatConfirm(self, line):
        lineLength = len(line)
        chatString = eval('PLocalizer.' + line[1])
        if len(line) == 3:
            dialogue = self.getVar(line[2])
        else:
            dialogue = None
        return Func(base.localAvatar.guiMgr.subtitler.confirmText, chatString, subtitleEvent, None, dialogue)

    def parsePlaySfx(self, line):
        if len(line) == 2:
            token, sfxName = line
            looping = 0
        elif len(line) == 3:
            token, sfxName, looping = line
        else:
            notify.error('invalid number of arguments')
        sfx = self.getVar(sfxName)
        return Func(base.playSfx, sfx, looping)

    def parseStopSfx(self, line):
        token, sfxName = line
        sfx = self.getVar(sfxName)
        return Func(sfx.stop)

    def parsePlayAnim(self, line):
        if len(line) == 3:
            token, actorName, animName = line
            playRate = 1.0
        elif len(line) == 4:
            token, actorName, animName, playRate = line
        else:
            notify.error('invalid number of arguments')
        actor = self.getVar(actorName)
        return Sequence(Func(actor.setPlayRate, playRate, animName), Func(actor.play, animName))

    def parseLoopAnim(self, line):
        if len(line) == 3:
            token, actorName, animName = line
            playRate = 1.0
        elif len(line) == 4:
            token, actorName, animName, playRate = line
        else:
            notify.error('invalid number of arguments')
        actor = self.getVar(actorName)
        return Sequence(Func(actor.setPlayRate, playRate, animName), Func(actor.loop, animName))

    def parseLerpPos(self, line):
        token, nodeName, x, y, z, t = line
        node = self.getVar(nodeName)
        return Sequence(LerpPosInterval(node, t, Point3(x, y, z), blendType='easeInOut'), duration=0.0)

    def parseLerpHpr(self, line):
        token, nodeName, h, p, r, t = line
        node = self.getVar(nodeName)
        return Sequence(LerpHprInterval(node, t, VBase3(h, p, r), blendType='easeInOut'), duration=0.0)

    def parseLerpScale(self, line):
        token, nodeName, x, y, z, t = line
        node = self.getVar(nodeName)
        return Sequence(LerpScaleInterval(node, t, VBase3(x, y, z), blendType='easeInOut'), duration=0.0)

    def parseLerpPosHprScale(self, line):
        token, nodeName, x, y, z, h, p, r, sx, sy, sz, t = line
        node = self.getVar(nodeName)
        return Sequence(LerpPosHprScaleInterval(node, t, VBase3(x, y, z), VBase3(h, p, r), VBase3(sx, sy, sz), blendType='easeInOut'), duration=0.0)

    def parseLerpColor(self, line):
        token, nodeName, sr, sg, sb, sa, er, eg, eb, ea, t = line
        node = self.getVar(nodeName)
        return Sequence(LerpColorInterval(node, t, VBase4(er, eg, eb, ea), startColorScale=VBase4(sr, sg, sb, sa), blendType='easeInOut'), duration=0.0)

    def parseLerpColorScale(self, line):
        token, nodeName, sr, sg, sb, sa, er, eg, eb, ea, t = line
        node = self.getVar(nodeName)
        return Sequence(LerpColorScaleInterval(node, t, VBase4(er, eg, eb, ea), startColorScale=VBase4(sr, sg, sb, sa), blendType='easeInOut'), duration=0.0)

    def parseDepthWriteOn(self, line):
        token, nodeName, depthWrite = line
        node = self.getVar(nodeName)
        return Sequence(Func(node.setDepthWrite, depthWrite))

    def parseDepthWriteOff(self, line):
        token, nodeName = line
        node = self.getVar(nodeName)
        return Sequence(Func(node.clearDepthWrite))

    def parseDepthTestOn(self, line):
        token, nodeName, depthTest = line
        node = self.getVar(nodeName)
        return Sequence(Func(node.setDepthTest, depthTest))

    def parseDepthTestOff(self, line):
        token, nodeName = line
        node = self.getVar(nodeName)
        return Sequence(Func(node.clearDepthTest))

    def parseSetBin(self, line):
        if len(line) == 3:
            token, nodeName, binName = line
            sortOrder = 0
        else:
            token, nodeName, binName, sortOrder = line
        node = self.getVar(nodeName)
        return Sequence(Func(node.setBin, binName, sortOrder))

    def parseClearBin(self, line):
        token, nodeName = line
        node = self.getVar(nodeName)
        return Sequence(Func(node.clearBin))

    def parseWaitEvent(self, line):
        token = line[0]
        eventNames = line[1:]
        return eventNames

    def parseWaitEventChat(self, line):
        lineLen = len(line)
        token = line[0]
        eventName = line[1]
        argIdx = 2
        av = self.getVar(line[argIdx])
        if av:
            uniqueEventName = av.uniqueName(eventName)
            argIdx = 3
        prompts = []
        promptsList = line[argIdx:len(line)]
        while promptsList:
            chatCommand = ['CHAT', str(promptsList[1]), str(promptsList[2])]
            command = self.parseChat(chatCommand)
            prompts.append([promptsList[0], command])
            promptsList = promptsList[3:len(promptsList)]

        return (uniqueEventName, prompts)

    def parseSendEvent(self, line):
        token, eventName = line
        return Func(messenger.send, eventName)

    def parseFunction(self, line):
        token, objectName, functionName = line
        object = self.getVar(objectName)
        cfunc = compile('object' + '.' + functionName, '<string>', 'eval')
        return Func(eval(cfunc))

    def parseAddLaffMeter(self, line):
        token, maxHpDelta = line
        newMaxHp = maxHpDelta + self.toon.getMaxHp()
        newHp = newMaxHp
        laffMeter = self.getVar('laffMeter')
        return Func(laffMeter.adjustFace, newHp, newMaxHp)

    def parseLaffMeter(self, line):
        token, newHp, newMaxHp = line
        laffMeter = self.getVar('laffMeter')
        return Func(laffMeter.adjustFace, newHp, newMaxHp)

    def parseObscureLaffMeter(self, line):
        token, val = line
        return Func(self.toon.laffMeter.obscure, val)

    def parseAddInventory(self, line):
        token, track, level, number = line
        inventory = self.getVar('inventory')
        countSound = loadSfx(SoundGlobals.SFX_GUI_CLICK_01)
        return Sequence(Func(base.playSfx, countSound), Func(inventory.buttonBoing, track, level), Func(inventory.addItems, track, level, number), Func(inventory.updateGUI, track, level))

    def parseSetInventory(self, line):
        token, track, level, number = line
        inventory = self.getVar('inventory')
        return Sequence(Func(inventory.setItem, track, level, number), Func(inventory.updateGUI, track, level))

    def parseSetInventoryYPos(self, line):
        token, track, level, yPos = line
        inventory = self.getVar('inventory')
        button = inventory.buttons[track][level].stateNodePath[0]
        text = button.find('**/+TextNode')
        return Sequence(Func(text.setY, yPos))

    def parseSetInventoryDetail(self, line):
        if len(line) == 2:
            token, val = line
        else:
            if len(line) == 4:
                token, val, track, level = line
            else:
                notify.error('invalid line for parseSetInventoryDetail: %s' % line)
            inventory = self.getVar('inventory')
            if val == -1:
                return Func(inventory.noDetail)
            elif val == 0:
                return Func(inventory.hideDetail)
            else:
                if val == 1:
                    return Func(inventory.showDetail, track, level)
                notify.error('invalid inventory detail level: %s' % val)

    def parseShowFriendsList(self, line):
        pass

    def parseHideFriendsList(self, line):
        pass

    def parseObscureChat(self, line):
        token, val0, val1 = line
        return Func(self.toon.chatMgr.obscure, val0, val1)

    def parseArrowsOn(self, line):
        arrows = self.getVar('arrows')
        token, x1, y1, h1, x2, y2, h2 = line
        return Func(arrows.arrowsOn, x1, y1, h1, x2, y2, h2)

    def parseArrowsOff(self, line):
        arrows = self.getVar('arrows')
        return Func(arrows.arrowsOff)

    def parseStartThrob(self, line):
        token, nodeName, r, g, b, a, r2, g2, b2, a2, t = line
        node = self.getVar(nodeName)
        startCScale = Point4(r, g, b, a)
        destCScale = Point4(r2, g2, b2, a2)
        self.throbIval = Sequence(LerpColorScaleInterval(node, t / 2.0, destCScale, startColorScale=startCScale, blendType='easeInOut'), LerpColorScaleInterval(node, t / 2.0, startCScale, startColorScale=destCScale, blendType='easeInOut'))
        return Func(self.throbIval.loop)

    def parseStopThrob(self, line):
        return Func(self.throbIval.finish)

    def parseToonHead(self, line):
        if len(line) == 5:
            token, toonName, x, z, toggle = line
            scale = 1.0
        else:
            token, toonName, x, z, toggle, scale = line
        toon = self.getVar(toonName)
        toonId = toon.getDoId()
        toonHeadFrame = self.toonHeads.get(toonId)
        if not toonHeadFrame:
            toonHeadFrame = ToonHeadFrame.ToonHeadFrame(toon)
            toonHeadFrame.tag1Node.setActive(1)
            toonHeadFrame.hide()
            self.toonHeads[toonId] = toonHeadFrame
            self.setVar('%sToonHead' % toonName, toonHeadFrame)
        if toggle:
            return Sequence(Func(toonHeadFrame.setPos, x, 0, z), Func(toonHeadFrame.setScale, scale), Func(toonHeadFrame.show))
        else:
            return Func(toonHeadFrame.hide)

    def parseToonHeadScale(self, line):
        token, toonName, scale = line
        toon = self.getVar(toonName)
        toonId = toon.getDoId()
        toonHeadFrame = self.toonHeads.get(toonId)
        return Func(toonHeadFrame.setScale, scale)

    def parseSetMusicVolume(self, line):
        if base.config.GetString('language', 'english') == 'japanese':
            try:
                loader = base.cr.playGame.place.loader
                type = 'music'
                duration = 0
                fromLevel = 1.0
                if len(line) == 2:
                    token, level = line
                else:
                    if len(line) == 3:
                        token, level, type = line
                    else:
                        if len(line) == 4:
                            token, level, type, duration = line
                        elif len(line) == 5:
                            token, level, type, duration, fromLevel = line
                        if type == 'battleMusic':
                            music = loader.battleMusic
                        else:
                            if type == 'activityMusic':
                                music = loader.activityMusic
                            music = loader.music
                    if duration == 0:
                        return Func(music.setVolume, level)

                    def setVolume(level):
                        music.setVolume(level)

                    return LerpFunctionInterval(setVolume, fromData=fromLevel, toData=level, duration=duration)
            except AttributeError:
                pass

        else:
            return Wait(0.0)

    def parseStartInteract(self, line):
        mySeq = Sequence()
        if self.toon.gameFSM.state == 'Cannon':
            mySeq.append(Func(self.toon.cannon.modeFSM.request, 'tutorialCutscene'))
        mySeq.append(Func(self.npc.startInteract, self.toon))
        mySeq.append(Func(self.npc.requestInteraction, self.toon.doId))
        return mySeq

    def parseStopInteract(self, line):
        mySeq = Sequence()
        mySeq.append(Func(self.toon.show))
        mySeq.append(Func(self.npc.showName))
        mySeq.append(Func(self.npc.nametag3d.setZ, 0))
        if self.toon.gameFSM.state == 'Cannon':
            mySeq.append(Func(self.toon.cannon.modeFSM.request, 'fireCannon'))
        mySeq.append(Func(self.npc.stopInteract, self.toon))
        mySeq.append(Func(self.npc.requestStopInteract))
        return mySeq

    def parseUnequipWeapon(self, line):

        def uniquipCurrWeapon():
            currentWeaponId, isWeaponDrawn = localAvatar.getCurrentWeapon()
            if currentWeaponId and localAvatar.gameFSM.state == 'Battle':
                localAvatar.guiMgr.combatTray.toggleWeapon(currentWeaponId)

        return Func(uniquipCurrWeapon)

    def parseEquipWeapon(self, line):
        if len(line) == 2:
            token, weapon = line
            if weapon == 10106:
                weapon = 2001
        else:
            weapon = 0

        def equipCurrWeapon(weapon):
            if weapon == 0:
                weapon, isWeaponDrawn = localAvatar.getCurrentWeapon()
            localAvatar.toggleWeapon(weapon, localAvatar.currentWeaponSlotId)

        def equipPistol():
            weapons = localAvatar.getInventory().getAllWeapons()
            for slot in weapons:
                if weapons[slot][1] == ItemGlobals.FLINTLOCK_PISTOL:
                    pistolSlotId = slot
                    break

            if pistolSlotId > Locations.RANGE_EQUIP_WEAPONS[1]:

                def handleSlotUpdate(slot):
                    localAvatar.guiMgr.setIgnoreAllKeys(False)
                    localAvatar.guiMgr.combatTray.toggleWeapon(ItemGlobals.FLINTLOCK_PISTOL, 2)
                    localAvatar.guiMgr.setIgnoreAllKeys(True)
                    localAvatar.motionFSM.off()

                localAvatar.getInventory().swapItems(pistolSlotId, 2)
                self.accept('inventoryLocation-%s' % localAvatar.getInventory().doId, handleSlotUpdate)
            else:
                localAvatar.guiMgr.setIgnoreAllKeys(False)
                localAvatar.guiMgr.combatTray.toggleWeapon(ItemGlobals.FLINTLOCK_PISTOL, pistolSlotId)
                localAvatar.guiMgr.setIgnoreAllKeys(True)
                localAvatar.motionFSM.off()

        return Func(equipPistol)

    def parseEnableAim(self, line):
        return Func(localAvatar.cameraFSM.request, 'FPS')

    def parseSetAimBounds(self, line):
        token, baseH, minH, maxH = line
        return Func(localAvatar.cameraFSM.fpsCamera.setHBounds, baseH, minH, maxH)

    def parseClearAimBounds(self, line):
        return Func(localAvatar.cameraFSM.fpsCamera.clearHBounds)

    def parseKickOutOfArea(self, line):
        return Func(base.cr.activeWorld.worldGrid.quickLoadOtherSide)

    def deleteCompassProps(self):
        if self.compassPirate:
            self.compassPirate.cleanupHuman()
            self.compassPirate.delete()
            self.compassPirate = None
        if self.compassSkeleton:
            self.compassSkeleton.delete()
            self.compassSkeleton = None
        return

    def parsePerformStandardInit(self, line):
        commands = []
        commands.append(Func(self.toon.setAllowSocialPanel, False))
        return commands

    def parsePerformStandardCleanup(self, line):
        commands = []
        commands.append(Func(self.overrideOldAvState, None))
        commands.append(self.parseClearMsgPanel(line))
        commands.append(self.parseFreeLocalToon(line))
        commands.append(self.parseClearInteractionalChat(line))
        commands.append(self.parseStopInteract(line))
        commands.append(Func(self.deleteCompassProps))
        commands.append(Func(self.letterboxOff))
        commands.append(Func(self.toon.guiMgr.showTrays))
        commands.append(Func(self.toon.b_setGameState, self.toon.gameFSM.defaultState))
        commands.append(Func(self.toon.setAllowSocialPanel, True))
        return commands

    def parseSetEquippedWeapons(self, line):
        token, weapon = line
        if weapon == 'All':
            weapons = localAvatar.equippedWeapons
        else:
            validIndexes = []
            if weapon == 'Pistol':
                validIndexes = [
                 1]
            weapons = []
            for currIdx in range(len(localAvatar.equippedWeapons)):
                if currIdx in validIndexes:
                    weapons.append(localAvatar.equippedWeapons[currIdx])
                else:
                    weapons.append(0)

        return [
         Func(localAvatar.guiMgr.cleanupEquippedWeapons), Func(localAvatar.guiMgr.setEquippedWeapons, weapons)]

    def parseClearCompassEffects(self, line):
        return [
         Func(localAvatar.guiMgr.radarGui.cleanupEffects)]


searchPath = DSearchPath()
if AppRunnerGlobal.appRunner:
    searchPath.appendDirectory(Filename.expandFrom('$POTCO_2_ROOT'))
else:
    searchPath.appendDirectory(Filename('etc'))
    searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$PIRATES/src/quest')))
    searchPath.appendDirectory(Filename.fromOsSpecific('pirates/src/quest'))
    searchPath.appendDirectory(Filename.fromOsSpecific('pirates/quest'))
    searchPath.appendDirectory(Filename('.'))
scriptFile = Filename('QuestScripts.txt')
found = vfs.resolveFilename(scriptFile, searchPath)
if not found:
    message = 'QuestScripts.txt file not found on %s' % searchPath
    raise IOError, message
lastReadFile = scriptFile
readFile(scriptFile)