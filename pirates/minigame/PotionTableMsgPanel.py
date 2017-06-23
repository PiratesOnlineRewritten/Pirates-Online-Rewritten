from pirates.piratesgui.GuiPanel import *
from pirates.piratesgui.RequestButton import RequestButton
from pirates.piratesbase import PLocalizer

class PotionTableMsgPanel(GuiPanel):

    def __init__(self):
        GuiPanel.__init__(self, 'Training needed', 1, 0.4, showClose=False, titleSize=1.5)
        self.setPos((-0.5, 0, 0))
        self.bQuit = RequestButton(text='OK', command=self.quit)
        self.bQuit.reparentTo(self)
        self.bQuit.setPos(0.45, 0, 0.05)
        self.message = None
        return

    def show(self):
        if self.message is not None:
            self.message.removeNode()
        self.messageText = 'Please visit the gypsy before crafting potions.'
        self.message = DirectLabel(parent=self, relief=None, text=self.messageText, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=17, pos=(0.5,
                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                  0.2), textMayChange=0)
        self.unstash()
        localAvatar.motionFSM.off()
        return

    def quit(self):
        localAvatar.motionFSM.on()
        self.stash()