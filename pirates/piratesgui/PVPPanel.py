from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.GuiPanel import GuiPanel
from pirates.piratesgui.ListFrame import ListFrame
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PVPRankGui
from pirates.pvp import PVPGlobals
from pirates.pvp import Beacon
from pirates.piratesgui import BorderFrame

class PVPPanel(BorderFrame.BorderFrame):

    def __init__(self, name, holder=None):
        w = PiratesGuiGlobals.PVPPanelWidth
        h = PiratesGuiGlobals.PVPPanelHeight
        BorderFrame.BorderFrame.__init__(self, relief=None, frameSize=(0.0, w, 0.0, h), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75))
        self.secondLayer = BorderFrame.BorderFrame(parent=self, relief=None, frameSize=(0.0, w, 0.0, h), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75))
        self.initialiseoptions(PVPPanel)
        if holder:
            self['frameSize'] = (
             0.0, w, 0.0 - len(holder.getItemList()) * 0.05, h)
            self.secondLayer['frameSize'] = (0.0, w, 0.0 - len(holder.getItemList()) * 0.05, h)
        self.list = ListFrame(PiratesGuiGlobals.PVPPageWidth, None, name, holder, frameColor=(0,
                                                                                              0,
                                                                                              0,
                                                                                              0))
        self.list.setup()
        self.list.reparentTo(self)
        self.list.setPos(0.005, 0.2, 0.0 - len(holder.getItemList()) * 0.05)
        self.renownDisplay = None
        if base.config.GetBool('want-land-infamy', 0) and not self.renownDisplay:
            self.renownDisplay = PVPRankGui.PVPRankGui(parent=base.a2dBottomRight, displayType=PVPRankGui.LAND_RENOWN_DISPLAY)
            self.renownDisplay.setPos(0.0, 0.0, 0.0)
        self.pvpTeamGraphic = None
        return

    def destroy(self):
        if self.list:
            self.list.destroy()
            self.list = None
        if self.renownDisplay:
            self.renownDisplay.destroy()
            self.renownDisplay = None
        if self.secondLayer:
            self.secondLayer.destroy()
            self.secondLayer = None
        if self.pvpTeamGraphic:
            self.pvpTeamGraphic.removeNode()
            self.pvpTeamGraphic = None
        BorderFrame.BorderFrame.destroy(self)
        return

    def cleanup(self):
        self.list.cleanup()

    def show(self, team):
        DirectFrame.show(self)
        self.setTeamGraphic(team)
        if self.renownDisplay:
            self.renownDisplay.show()

    def hide(self):
        DirectFrame.hide(self)
        if self.renownDisplay:
            self.renownDisplay.hide()

    def setTeamGraphic(self, team):
        if self.pvpTeamGraphic:
            self.pvpTeamGraphic.removeNode()
            self.pvpTeamGraphic = None
        if team > 0:
            self.pvpTeamGraphic = Beacon.getBeaconModel()
            self.pvpTeamGraphic.reparentTo(self)
            self.pvpTeamGraphic.setColor(PVPGlobals.getTeamColor(team))
            self.pvpTeamGraphic.setScale(0.23)
            self.pvpTeamGraphic.setPos(0.13, 0, 0.13)
        return