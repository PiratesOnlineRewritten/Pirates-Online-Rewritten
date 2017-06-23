from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ScoreFrame import ScoreFrame
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pirates.piratesgui import BorderFrame
from direct.showbase.DirectObject import DirectObject
from pirates.piratesbase import PLocalizer
from pirates.pvp import PVPGlobals

class PVPBoard(DirectObject):

    def __init__(self, holder):
        pvpIcons = loader.loadModel('models/textureCards/pvp_arrow')
        self.holder = holder
        hasTeams = holder.hasTeams()
        self.borderOne = BorderFrame.BorderFrame(relief=None, frameSize=(-PiratesGuiGlobals.PVPCompletePageWidth * 0.33, PiratesGuiGlobals.PVPCompletePageWidth * 0.33, PiratesGuiGlobals.PVPCompletePageHeight * 0.5 - 0.1 - PiratesGuiGlobals.TMCompletePageHeight / 16.0 * len(holder.getItemList(1)), PiratesGuiGlobals.PVPCompletePageHeight * 0.5), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75))
        self.borderOneSecondLayer = BorderFrame.BorderFrame(parent=self.borderOne, relief=None, text='', text_scale=0.075, text_fg=PVPGlobals.getTeamColor(1), text_pos=(-0.65, 0.64), frameSize=(-PiratesGuiGlobals.PVPCompletePageWidth * 0.33, PiratesGuiGlobals.PVPCompletePageWidth * 0.33, PiratesGuiGlobals.PVPCompletePageHeight * 0.5 - 0.1 - PiratesGuiGlobals.TMCompletePageHeight / 16.0 * len(holder.getItemList(1)), PiratesGuiGlobals.PVPCompletePageHeight * 0.5), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75))
        self.borderOne.setPos(0.0625, 0, -0.1)
        if hasTeams:
            self.borderOneSecondLayer['text'] = PLocalizer.PVPTeamName % 1
            self.one = ScoreFrame(PiratesGuiGlobals.PVPCompletePageWidth - 1.2, PiratesGuiGlobals.PVPCompletePageHeight, holder, 1, sortOrder=2)
            self.one.setPos(-0.5, 0, -0.85)
        else:
            self.one = ScoreFrame(PiratesGuiGlobals.PVPCompletePageWidth - 1.0, PiratesGuiGlobals.PVPCompletePageHeight, holder, 1, sortOrder=2)
            self.one.setPos(-0.74, 0, -0.85)
        self.borderOne.hide()
        self.one.hide()
        if hasTeams:
            self.borderTwo = BorderFrame.BorderFrame(relief=None, frameSize=(-PiratesGuiGlobals.PVPCompletePageWidth * 0.33, PiratesGuiGlobals.PVPCompletePageWidth * 0.33, PiratesGuiGlobals.PVPCompletePageHeight * 0.5 - 0.1 - PiratesGuiGlobals.TMCompletePageHeight / 16.0 * len(holder.getItemList(2)), PiratesGuiGlobals.PVPCompletePageHeight * 0.5), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75))
            self.borderTwoSecondLayer = BorderFrame.BorderFrame(parent=self.borderTwo, relief=None, text=PLocalizer.PVPTeamName % 2, text_scale=0.075, text_fg=PVPGlobals.getTeamColor(2), text_pos=(-0.65, 0.64), frameSize=(-PiratesGuiGlobals.PVPCompletePageWidth * 0.33, PiratesGuiGlobals.PVPCompletePageWidth * 0.33, PiratesGuiGlobals.PVPCompletePageHeight * 0.5 - 0.1 - PiratesGuiGlobals.TMCompletePageHeight / 16.0 * len(holder.getItemList(2)), PiratesGuiGlobals.PVPCompletePageHeight * 0.5), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75))
            self.two = ScoreFrame(PiratesGuiGlobals.PVPCompletePageWidth - 1.2, PiratesGuiGlobals.PVPCompletePageHeight, holder, 2, sortOrder=2)
            self.borderTwo.setPos(0.0625, 0, -0.25 - PiratesGuiGlobals.TMCompletePageHeight / 16.0 * len(holder.getItemList(1)))
            self.two.setPos(-0.5, 0, -1.0 - PiratesGuiGlobals.TMCompletePageHeight / 16.0 * len(holder.getItemList(1)))
            self.borderTwo.hide()
            self.two.hide()
        else:
            self.borderTwo = None
            self.two = None
        return

    def hide(self):
        self.borderOne.hide()
        self.one.hide()
        if self.borderTwo:
            self.borderTwo.hide()
        if self.two:
            self.two.hide()

    def show(self):
        self.borderOne.show()
        self.one.show()
        if self.borderTwo:
            self.borderTwo.show()
        if self.two:
            self.two.show()

    def destroy(self):
        self.holder = None
        self.borderOne.destroy()
        self.borderOne = None
        self.borderOneSecondLayer.destroy()
        self.borderOneSecondLayer = None
        self.one.destroy()
        self.one = None
        if self.borderTwo:
            self.borderTwo.destroy()
            self.borderTwo = None
            self.borderTwoSecondLayer.destroy()
            self.borderTwoSecondLayer = None
        if self.two:
            self.two.destroy()
            self.two = None
        return