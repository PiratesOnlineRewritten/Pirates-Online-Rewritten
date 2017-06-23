from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PiratesGuiGlobals

class BlinkButton(GuiButton.GuiButton):

    def __init__(self, parent, **kw):
        card = loader.loadModel('models/textureCards/skillIcons')
        base1 = card.find('**/base')
        base2 = card.find('**/base_over')
        base3 = card.find('**/base_down')
        seq = NodePath(SequenceNode(''))
        base2.copyTo(seq)
        base1.copyTo(seq)
        base1.copyTo(seq)
        base1.copyTo(seq)
        seq.node().setFrameRate(1.5)
        seq.node().loop(True)
        optiondefs = (
         ('sortOrder', 0, None), ('relief', None, None), ('image', (seq, base3, base2), None))
        self.defineoptions(kw, optiondefs)
        GuiButton.GuiButton.__init__(self, parent=parent, **kw)
        self.initialiseoptions(BlinkButton)
        return