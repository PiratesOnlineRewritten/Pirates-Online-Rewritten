from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui.GuiPanel import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ListFrame import ListFrame

class ObjectivesPanel(DirectFrame):

    def __init__(self, name, holder=None, mouseFade=False):
        DirectFrame.__init__(self, relief=None, frameSize=(0.0, PiratesGuiGlobals.ObjectivesPanelWidth, 0.0, PiratesGuiGlobals.ObjectivesPanelHeight))
        self.initialiseoptions(ObjectivesPanel)
        self.childFrame = GuiPanel(name, PiratesGuiGlobals.ObjectivesPanelWidth, PiratesGuiGlobals.ObjectivesPanelHeight)
        self.childFrame.initialiseoptions(GuiPanel)
        self.childFrame.reparentTo(self)
        self.list = ListFrame(PiratesGuiGlobals.ObjectivesPageWidth, PiratesGuiGlobals.ObjectivesPageHeight, name, holder, hideAll=False)
        self.list.setup()
        self.list.reparentTo(self.childFrame)
        self.childFrame.closeButton.hide()
        if mouseFade:
            self.childFrame.setMouseFade(True)
        else:
            self.childFrame.hide()
        return

    def destroy(self):
        DirectFrame.destroy(self)
        self.list.destroy()

    def cleanup(self):
        self.list.cleanup()