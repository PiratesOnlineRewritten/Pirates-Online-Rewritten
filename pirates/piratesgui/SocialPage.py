from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals

class SocialPage(DirectFrame):

    def __init__(self, title):
        spacer = 0.1
        DirectFrame.__init__(self, relief=None, state=DGG.NORMAL, frameColor=PiratesGuiGlobals.FrameColor, borderWidth=PiratesGuiGlobals.BorderWidth, frameSize=(0.0, PiratesGuiGlobals.SocialPageWidth, spacer, PiratesGuiGlobals.SocialPageHeight - PiratesGuiGlobals.GridCell), pos=(PiratesGuiGlobals.BorderWidth[0], 0, PiratesGuiGlobals.BorderWidth[0] + PiratesGuiGlobals.GridCell), sortOrder=5)
        self.initialiseoptions(SocialPage)
        self.recountTaskName = base.cr.specialName('SocialPage-RecountMembers')
        self.title = title
        self.count = 0
        return

    def destroy(self):
        taskMgr.remove(self.recountTaskName)
        DirectFrame.destroy(self)

    def show(self):
        DirectFrame.show(self)

    def hide(self):
        DirectFrame.hide(self)

    def startRecountMembers(self):
        taskMgr.remove(self.recountTaskName)
        taskMgr.doMethodLater(0.1, self.updateCount, self.recountTaskName)

    def updateCount(self):
        pass