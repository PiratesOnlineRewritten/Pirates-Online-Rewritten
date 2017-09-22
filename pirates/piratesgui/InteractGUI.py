from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.distributed import InteractGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals

class InteractGUI(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, relief=None, sortOrder=3, pos=(-0.5, 0, -0.4))
        self.optionButtons = []
        self.initialiseoptions(InteractGUI)
        return

    def destroy(self):
        self.destroyOptionButtons()
        DirectFrame.destroy(self)

    def destroyOptionButtons(self):
        for optionButton in self.optionButtons:
            optionButton.destroy()

        if hasattr(self, 'title'):
            self.title.destroy()
            del self.title
        self.optionButtons = []

    def setOptions(self, title, optionIds, statusCodes, optionCallback, bribeType):
        z = 1.0
        self.destroyOptionButtons()
        self.title = DirectLabel(parent=self, relief=None, text=title, text_align=TextNode.ACenter, text_scale=0.07, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0, 0, z - 0.08), text_font=PiratesGlobals.getPirateOutlineFont())
        gui = loader.loadModel('models/gui/avatar_chooser_rope')
        topPanel = gui.find('**/avatar_c_A_top')
        topPanelOver = gui.find('**/avatar_c_A_top_over')
        middlePanel = gui.find('**/avatar_c_A_middle')
        middlePanelOver = gui.find('**/avatar_c_A_middle_over')
        bottomPanel = gui.find('**/avatar_c_A_bottom')
        bottomPanelOver = gui.find('**/avatar_c_A_bottom_over')
        for i, optionId, statusCode in zip(range(len(optionIds)), optionIds, statusCodes):
            optionName = InteractGlobals.InteractOptionNames.get(optionId, 'Error')
            optionHelp = InteractGlobals.InteractOptionHelpText.get(optionId, 'Error')
            print 'DEBUG: InteractGUI.optionName = %s' % optionName
            if (optionName == 'Bribe') & (bribeType == 1):
                optionName = PLocalizer.InteractBribeAlt
            if i == 0:
                image = (
                 topPanel, topPanel, topPanelOver, topPanel)
                textPos = (0, -0.03)
                z -= 0.19
            elif i == len(optionIds) - 1:
                image = (
                 bottomPanel, bottomPanel, bottomPanelOver, bottomPanel)
                textPos = (0, 0.033)
                if i == 1:
                    z -= 0.165
                else:
                    z -= 0.155
            else:
                image = (middlePanel, middlePanel, middlePanelOver, middlePanel)
                textPos = (0, -0.015)
                if i == 1:
                    z -= 0.11
                else:
                    z -= 0.105
            if statusCode == InteractGlobals.NORMAL:
                state = DGG.NORMAL
                textFg = PiratesGuiGlobals.TextFG1
                imageColor = (1, 1, 1, 1)
            elif statusCode == InteractGlobals.DISABLED:
                state = DGG.DISABLED
                textFg = (0.3, 0.25, 0.2, 1)
                imageColor = (0.8, 0.8, 0.8, 1)
            elif statusCode == InteractGlobals.HIGHLIGHT:
                state = DGG.NORMAL
                textFg = PiratesGuiGlobals.TextFG2
                imageColor = (1, 1, 1, 1)
            optionButton = DirectButton(parent=self, relief=None, state=state, pressEffect=0, text=optionName, text_fg=textFg, text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, text_scale=0.05, text_pos=textPos, image=image, image_scale=0.4, image_color=imageColor, pos=(0, 0, z), command=optionCallback, extraArgs=[optionId])
            self.optionButtons.append(optionButton)

        gui.removeNode()
        return