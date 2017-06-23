import os
from pandac.PandaModules import *
from direct.showbase import AppRunnerGlobal
from otp.chat.WhiteList import WhiteList
from pirates.piratesbase.PLocalizer import enumeratePirateNameTokensLower

class PWhiteList(WhiteList):

    def __init__(self):
        vfs = VirtualFileSystem.getGlobalPtr()
        filename = Filename('pwhitelist.txt')
        searchPath = DSearchPath()
        if __debug__:
            searchPath.appendDirectory(Filename.expandFrom('../resources/phase_3/etc'))
        else:
            searchPath.appendDirectory(Filename.expandFrom('phase_3/etc'))

        found = vfs.resolveFilename(filename, searchPath)
        if not found:
            message = 'pwhitelist.txt file not found on %s' % searchPath
            raise IOError, message
        data = vfs.readFile(filename, 1)
        lines = data.split('\n')
        for token in enumeratePirateNameTokensLower():
            lines.append(token)

        WhiteList.__init__(self, lines)
