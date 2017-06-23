from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui.CannonDefenseHelpPanel import CannonDefenseHelpPanel
from pirates.piratesbase import PLocalizer

class CannonDefenseHelpManager():

    def __init__(self, fadeLength):
        self.ammo = None
        self.mine = None
        self.ammoPanel = None
        self.wave = None
        self.exit = None
        self.help = None
        self.__createPanels()
        self.__createIntervals(fadeLength)
        return

    def __createPanels(self):
        self.ammo = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['AmmoHeader'], PLocalizer.CannonDefenseHelp['AmmoBody'], 13, 0.61, 0.55)
        self.ammo.setPos(-0.1, 0, 1)
        self.ammo.arrow.setHpr(0, 0, 90)
        self.ammo.arrow.setPos(0.1, 0, -0.111)
        self.mine = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['MineHeader'], PLocalizer.CannonDefenseHelp['MineBody'], 12, 0.54, 0.2)
        self.mine.setPos(0.31, 0, -0.25)
        self.mine.arrow.setHpr(0, 0, -90)
        self.mine.arrow.setPos(0.04, 0, 0.311)
        self.ammoPanel = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['AmmoPanelHeader'], PLocalizer.CannonDefenseHelp['AmmoPanelBody'], 9, 0.45, 0.51)
        self.ammoPanel.setPos(0.2, 0, 0.06)
        self.ammoPanel.arrow.setHpr(0, 0, -180)
        self.ammoPanel.arrow.setPos(-0.127, 0, 0.25)
        self.wave = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['WaveHeader'], PLocalizer.CannonDefenseHelp['WaveBody'], 13, 0.6, 0.25)
        self.wave.setPos(-1.55, -0.21, -0.3)
        self.wave.arrow.setPos(0.71, 0, 0.19)
        self.exit = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['ExitHeader'], None, 0, 0.44, 0.08)
        self.exit.setPos(-0.45, 0, 0.45)
        self.exit.arrow.setScale(0.6, 1.0, 0.6)
        self.exit.arrow.setHpr(0, 0, 90)
        self.exit.arrow.setPos(0.23, 0, -0.065)
        self.help = CannonDefenseHelpPanel(PLocalizer.CannonDefenseHelp['HelpHeader'], None, 0, 0.51, 0.085)
        self.help.setPos(-0.82, 0, 0.28)
        self.help.arrow.setScale(0.3, 1.0, 0.3)
        self.help.arrow.setHpr(0, 0, 90)
        self.help.arrow.setPos(0.41, 0, -0.03)
        return

    def destroy(self):
        if self.mine:
            self.mine.removeNode()
            self.mine = None
        if self.ammoPanel:
            self.ammoPanel.removeNode()
            self.ammoPanel = None
        if self.ammo:
            self.ammo.removeNode()
            self.ammo = None
        if self.wave:
            self.wave.removeNode()
            self.wave = None
        if self.exit:
            self.exit.removeNode()
            self.exit = None
        if self.help:
            self.help.removeNode()
            self.help = None
        return

    def __createIntervals(self, length):
        opaque = Vec4(1, 1, 1, 1)
        transparent = Vec4(1, 1, 1, 0)
        self.fadeIn = Parallel(self.ammo.colorScaleInterval(length, opaque, transparent), self.mine.colorScaleInterval(length, opaque, transparent), self.ammoPanel.colorScaleInterval(length, opaque, transparent), self.wave.colorScaleInterval(length, opaque, transparent), self.exit.colorScaleInterval(length, opaque, transparent), self.help.colorScaleInterval(length, opaque, transparent))
        self.fadeOut = Parallel(self.ammo.colorScaleInterval(length, transparent), self.mine.colorScaleInterval(length, transparent), self.ammoPanel.colorScaleInterval(length, transparent), self.wave.colorScaleInterval(length, transparent), self.exit.colorScaleInterval(length, transparent), self.help.colorScaleInterval(length, transparent))