import sys
import os
import time
import string
import bz2
import random
from direct.showbase.MessengerGlobal import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.EventManagerGlobal import *
from direct.task.TaskManagerGlobal import *
from direct.task.Task import Task
from direct.task.MiniTask import MiniTask, MiniTaskManager
from direct.directnotify.DirectNotifyGlobal import *
from pandac.PandaModules import *
from otp.launcher.LauncherBase import LauncherBase
from pirates.piratesbase import PLocalizer

class PiratesQuickLauncher(LauncherBase):
    GameName = 'Pirates'
    ArgCount = 3
    LauncherPhases = [
     1, 2, 3, 4, 5, 6]
    TmpOverallMap = [0.16, 0.16, 0.16, 0.16, 0.16, 0.2]
    ForegroundSleepTime = 0.001
    Localizer = PLocalizer
    DecompressMultifiles = True
    CompressionExt = 'bz2'
    PatchExt = 'pch'

    def __init__(self):
        print 'Running: PiratesQuickLauncher'
        self.heavyDownloadServerList = []
        self.heavyDownloadServer = None
        self.launcherFileDbFilename = '%s?%s' % (self.getValue('GAME_PATCHER_FILE_OPTIONS', 'patcher.ver'), random.randint(1, 1000000000))
        LauncherBase.__init__(self)
        self.contentDir = '/'
        self.serverDbFileHash = HashVal()
        self.launcherFileDbHash = HashVal()
        self.DECREASE_BANDWIDTH = 0
        self.httpChannel.setDownloadThrottle(0)
        self.showPhase = -1
        self.maybeStartGame()
        self.mainLoop()
        return

    def addDownloadVersion(self, serverFilePath):
        if self.heavyDownloadServer:
            url = URLSpec(self.heavyDownloadServer)
        else:
            url = URLSpec(self.downloadServer)
        origPath = url.getPath()
        if origPath[-1] == '/':
            url.setPath('%s%s' % (origPath, serverFilePath))
        else:
            url.setPath('%s/%s' % (origPath, serverFilePath))
        return url

    def downloadLauncherFileDbDone(self):
        settings = {}
        for line in self.ramfile.readlines():
            line = line.strip()
            equalIndex = line.find('=')
            if equalIndex >= 0:
                key = line[:equalIndex]
                value = line[equalIndex + 1:]
                settings[key] = value

        self.requiredInstallFiles = []
        if sys.platform == 'win32':
            fileList = settings['REQUIRED_INSTALL_FILES']
        else:
            if sys.platform == 'darwin':
                fileList = settings['REQUIRED_INSTALL_FILES_OSX']
            else:
                if sys.platform == 'linux2':
                    fileList = settings['REQUIRED_INSTALL_FILES_LINUX']
                else:
                    self.notify.warning('Unknown sys.platform: %s' % sys.platform)
                    fileList = settings['REQUIRED_INSTALL_FILES']
                for fileDesc in fileList.split():
                    fileName, flag = fileDesc.split(':')
                    directions = BitMask32(flag)
                    extract = directions.getBit(0)
                    requiredByLauncher = directions.getBit(1)
                    optionalDownload = directions.getBit(2)
                    self.notify.info('fileName: %s, flag:=%s directions=%s, extract=%s required=%s optDownload=%s' % (fileName, flag, directions, extract, requiredByLauncher, optionalDownload))
                    if not optionalDownload:
                        self.requiredInstallFiles.append(fileName)

                self.notify.info('requiredInstallFiles: %s' % self.requiredInstallFiles)
                self.mfDetails = {}
                for mfName in self.requiredInstallFiles:
                    currentVer = settings['FILE_%s.current' % mfName]
                    details = settings['FILE_%s.%s' % (mfName, currentVer)]
                    size, hash = details.split()
                    self.mfDetails[mfName] = (currentVer, int(size), hash)
                    self.notify.info('mfDetails[%s] = %s' % (mfName, self.mfDetails[mfName]))

            heavyDownloadServerString = settings['PATCHER_BASE_URL_HEAVY_LIFTING']
            for name in string.split(heavyDownloadServerString, ';'):
                url = URLSpec(name, 1)
                self.heavyDownloadServerList.append(url)

        self.getNextHeavyDownloadServer()
        self.resumeInstall()

    def getNextDownloadServer(self):
        if self.heavyDownloadServer:
            return self.getNextHeavyDownloadServer()
        else:
            return LauncherBase.getNextDownloadServer(self)

    def getNextHeavyDownloadServer(self):
        if not self.heavyDownloadServerList:
            self.notify.warning('No more heavy download servers')
            self.heavyDownloadServer = None
            return 0
        self.heavyDownloadServer = self.heavyDownloadServerList.pop(0)
        self.notify.info('Using heavy download server %s.' % self.heavyDownloadServer.cStr())
        return 1

    def resumeMultifileDownload(self):
        curVer, expectedSize, expectedMd5 = self.mfDetails[self.currentMfname]
        localFilename = Filename(self.topDir, Filename('_%s.%s.%s' % (self.currentMfname, curVer, self.CompressionExt)))
        serverFilename = '%s%s.%s.%s' % (self.contentDir, self.currentMfname, curVer, self.CompressionExt)
        if localFilename.exists():
            fileSize = localFilename.getFileSize()
            self.notify.info('Previous partial download exists for: %s size=%s' % (localFilename.cStr(), fileSize))
            self.downloadMultifile(serverFilename, localFilename, self.currentMfname, self.downloadMultifileDone, 0, fileSize, self.downloadMultifileWriteToDisk)
        else:
            self.downloadMultifile(serverFilename, localFilename, self.currentMfname, self.downloadMultifileDone, 0, 0, self.downloadMultifileWriteToDisk)

    def resumeInstall(self):
        while self.requiredInstallFiles:
            self.currentMfname = self.requiredInstallFiles.pop(0)
            self.currentPhaseName = self.Localizer.LauncherPhaseNames[self.currentPhase]
            self.notify.info('currentMfname: %s currentPhase: %s currentPhaseIndex: %s' % (self.currentMfname, self.currentPhase, self.currentPhaseIndex))
            curVer, expectedSize, expectedMd5 = self.mfDetails[self.currentMfname]
            self.curPhaseFile = Filename(self.topDir, Filename(self.currentMfname))
            self.notify.info('working on: %s' % self.curPhaseFile)
            if self.curPhaseFile.exists():
                self.notify.info('file exists')
                fileSize = self.curPhaseFile.getFileSize()
                self.notify.info('clientSize: %s expectedSize: %s' % (fileSize, expectedSize))
                if fileSize == expectedSize:
                    self.notify.info('file is correct size')
                    self.finalizePhase()
                    self.currentPhase += 1
                    self.currentPhaseIndex += 1
                    continue
                else:
                    self.notify.warning('file is not correct size, attempting to resume download')
                    self.resumeMultifileDownload()
                    return
            else:
                self.notify.info('file does not exist - start download')
                self.resumeMultifileDownload()
                return
            self.currentPhase += 1
            self.currentPhaseIndex += 1

        if not self.requiredInstallFiles:
            self.notify.info('ALL PHASES COMPLETE')
            messenger.send('launcherAllPhasesComplete')
            self.cleanup()
            return
        raise StandardError, 'Some phases not listed in LauncherPhases: %s' % self.requiredInstallFiles

    def getDecompressMultifile(self, mfname):
        if not self.DecompressMultifiles:
            self.decompressMultifileDone()
        else:
            self.notify.info('decompressMultifile: Decompressing multifile: ' + mfname)
            (curVer, expectedSize,expectedMd5) = self.mfDetails[self.currentMfname]
            localFilename = Filename(self.topDir, Filename('_%s.%s.%s' % (mfname, curVer, self.CompressionExt)))
            self.decompressMultifile(mfname, localFilename, self.decompressMultifileDone)

        self.notify.info('decompressMultifile: Multifile already decompressed: %s' % mfname)
        self.decompressMultifileDone()

    def decompressMultifile(self, mfname, localFilename, callback):
        self.notify.info('decompressMultifile: request: ' + localFilename.cStr())
        self.launcherMessage(self.Localizer.LauncherDecompressingFile % {'name': self.currentPhaseName,'current': self.currentPhaseIndex,'total': self.numPhases})
        task = MiniTask(self.decompressMultifileTask)
        task.mfname = mfname
        task.mfFilename = Filename(self.topDir, Filename('_' + task.mfname))
        task.mfFile = open(task.mfFilename.toOsSpecific(), 'wb')
        task.localFilename = localFilename
        task.callback = callback
        task.lastUpdate = 0
        task.decompressor = bz2.BZ2File(localFilename.toOsSpecific(), 'rb')
        self.miniTaskMgr.add(task, 'launcher-decompressMultifile')

    def decompressMultifileTask(self, task):
        self.maybeStartGame()
        bufferSize = config.GetInt('launcher-decompress-buffer-size', 8192)
        data = task.decompressor.read(bufferSize)
        if data:
            task.mfFile.write(data)
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                task.lastUpdate = now
                curSize = task.mfFilename.getFileSize()
                curVer, expectedSize, expectedMd5 = self.mfDetails[self.currentMfname]
                progress = curSize / float(expectedSize)
                self.launcherMessage(self.Localizer.LauncherDecompressingPercent % {'name': self.currentPhaseName,'current': self.currentPhaseIndex,'total': self.numPhases,'percent': int(round(progress * 100))})
                percentProgress = int(round(progress * self.decompressPercentage))
                totalPercent = self.downloadPercentage + percentProgress
                self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            self.foregroundSleep()
            return Task.cont
        else:
            task.mfFile.close()
            task.decompressor.close()
            unlinked = task.localFilename.unlink()
            if not unlinked:
                self.notify.warning('unlink failed on file: %s' % task.localFilename.cStr())
            realMf = Filename(self.topDir, Filename(self.currentMfname))
            renamed = task.mfFilename.renameTo(realMf)
            if not renamed:
                self.notify.warning('rename failed on file: %s' % task.mfFilename.cStr())
            self.launcherMessage(self.Localizer.LauncherDecompressingPercent % {'name': self.currentPhaseName,'current': self.currentPhaseIndex,'total': self.numPhases,'percent': 100})
            totalPercent = self.downloadPercentage + self.decompressPercentage
            self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            self.notify.info('decompressMultifileTask: Decompress multifile done: ' + task.localFilename.cStr())
            if self.dldb:
                self.dldb.setClientMultifileDecompressed(task.mfname)
            del task.decompressor
            task.callback()
            del task.callback
            return Task.done

    def decompressMultifileDone(self):
        self.finalizePhase()
        self.notify.info('Done updating multifiles in phase: %s' % self.currentPhase)
        self.progressSoFar += int(round(self.phaseOverallMap[self.currentPhase] * 100))
        self.notify.info('progress so far %s' % self.progressSoFar)
        self.currentPhase += 1
        self.currentPhaseIndex += 1
        self.maybeStartGame()
        self.resumeInstall()

    def finalizePhase(self):
        mfFilename = Filename(self.topDir, Filename(self.currentMfname))
        self.MakeNTFSFilesGlobalWriteable(mfFilename)
        vfs = VirtualFileSystem.getGlobalPtr()
        vfs.mount(mfFilename, '.', VirtualFileSystem.MFReadOnly)
        self.setPercentPhaseComplete(self.currentPhase, 100)
        messenger.send('phaseComplete-%s' % self.currentPhase)

    def getValue(self, key, default=None):
        return os.environ.get(key, default)

    def setValue(self, key, value):
        os.environ[key] = str(value)

    def getVerifyFiles(self):
        return config.GetInt('launcher-verify', 0)

    def getTestServerFlag(self):
        return self.getValue('IS_TEST_SERVER', 0)

    def getGameServer(self):
        return self.getValue('GAME_SERVER', '')

    def getLogFileName(self):
        return 'pirates'

    def getCDDownloadPath(self, origPath, serverFilePath):
        return '%s/%s/CD_%d/%s' % (origPath, self.getServerVersion(), self.fromCD, serverFilePath)

    def getDownloadPath(self, origPath, serverFilePath):
        return '%s/%s' % (origPath, serverFilePath)

    def hashIsValid(self, serverHash, hashStr):
        return serverHash.setFromDec(hashStr)

    def getAccountServer(self):
        return None

    def getNeedPwForSecretKey(self):
        return 0

    def getParentPasswordSet(self):
        return 0

    def canLeaveFirstIsland(self):
        return self.getPhaseComplete(4)

    def startGame(self):
        self.newTaskManager()
        eventMgr.restart()
        from pirates.piratesbase import PiratesStart
