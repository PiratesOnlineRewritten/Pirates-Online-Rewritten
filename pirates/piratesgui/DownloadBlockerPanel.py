from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.showbase.PythonUtil import GoldenRectangle
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PLocalizer

class DownloadBlockerPanel(GuiPanel.GuiPanel):
    Reasons = Enum('GENERIC,ISLAND,BOAT,TELEPORT,LOOKOUT')
    _Messages = {Reasons.GENERIC: PLocalizer.DownloadBlockerMsgGeneric,Reasons.ISLAND: PLocalizer.DownloadBlockerMsgIsland,Reasons.BOAT: PLocalizer.DownloadBlockerMsgBoat,Reasons.TELEPORT: PLocalizer.DownloadBlockerMsgTeleport,Reasons.LOOKOUT: PLocalizer.DownloadBlockerMsgLookout}

    def __init__(self, reason=None):
        if reason is None:
            reason = DownloadBlockerPanel.Reasons.GENERIC
        height = 0.6
        GuiPanel.GuiPanel.__init__(self, PLocalizer.DownloadBlockerPanelTitle, GoldenRectangle.getLongerEdge(height), height)
        self._reason = reason
        self._message = DirectLabel(parent=self, relief=None, text=DownloadBlockerPanel._Messages[self._reason], text_pos=(0.2,
                                                                                                                           0), text_scale=0.072, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=9, pos=(0.291294,
                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                 0.400258), textMayChange=1)
        taskMgr.doMethodLater(10, self.destroy, 'downloadBlockerTimer', extraArgs=[])
        return

    def destroy(self):
        taskMgr.remove('downloadBlockerTimer')
        GuiPanel.GuiPanel.destroy(self)