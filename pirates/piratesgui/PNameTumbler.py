from pandac.PandaModules import *
from direct.showbase.ShowBaseGlobal import *
from direct.showbase import DirectObject
from direct.task import Task
from direct.gui.DirectGui import *
from direct.gui import OnscreenText
from otp.namepanel import NameTumbler
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
import random
import string

class PNameTumbler(NameTumbler.NameTumbler):

    def __init__(self, nameList, category):
        NameTumbler.NameTumbler.__init__(self, nameList, category)
        self.tumblerColor = (1, 1, 1, 1)
        self.charGui = None
        self.triangleGui = None
        return

    def loadTumblerGUI(self):
        self.charGui = loader.loadModel('models/gui/char_gui')
        self.triangleGui = loader.loadModel('models/gui/triangle')
        self.tumblerscrollList = self.makeScrollList(self.displayList, [
         TextNode.ACenter, 'title'])
        self.tumblerscrollList['relief'] = DGG.FLAT
        self.tumblerscrollList['command'] = self.listsChanged
        self.tumblerscrollList.reparentTo(self)
        self.tumblerscrollList.resetFrameSize()
        self.hilight = self.makeHighlight((0, 0, -0.27))
        self.hilight.reparentTo(self.tumblerscrollList)
        if self.category != '':
            self.check = self.makeCheckBox((-0.617, 0, 0.374), self.category, self.toggleTumbler)
            self.check.reparentTo(self)
        self.getRandomResult()

    def unloadTumblerGUI(self):
        if self.charGui:
            self.charGui.removeNode()
            self.charGui = None
        if self.triangleGui:
            self.triangleGui.removeNode()
            self.triangleGui = None
        NameTumbler.NameTumbler.unloadTumblerGUI(self)
        return

    def makeHighlight(self, pos):
        return DirectFrame(parent=self, relief=DGG.FLAT, frameColor=(1, 1, 1, 0.4), frameSize=(-1.4,
                                                                                               4.2,
                                                                                               -2.2,
                                                                                               -1.1), borderWidth=(1,
                                                                                                                   0.5), pos=pos, scale=1.0)

    def makeCheckbox(self, pos, text, command):
        c = DirectCheckButton(parent=self, relief=None, scale=0.1, boxBorder=0.08, boxRelief=None, pos=pos, text=text, text_fg=(1,
                                                                                                                                1,
                                                                                                                                1,
                                                                                                                                1), text_scale=0.8, text_pos=(0.4,
                                                                                                                                                              0), indicator_pos=(0,
                                                                                                                                                                                 0,
                                                                                                                                                                                 0), indicator_text_fg=(1,
                                                                                                                                                                                                        1,
                                                                                                                                                                                                        1,
                                                                                                                                                                                                        1), command=command, text_align=TextNode.ALeft)
        return c

    def makeScrollList(self, items, nitemMakeExtraArgs):
        lst = items[:]
        dsl = DirectScrolledList(parent=self, relief=None, items=lst, itemMakeFunction=self.makeLabel, itemMakeExtraArgs=nitemMakeExtraArgs, command=None, text_fg=PiratesGuiGlobals.TextFG2, pos=(-0.08, 0, 0.03), scale=0.06, incButton_pos=(1.5,
                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                               -6.5), incButton_relief=None, incButton_image=(self.triangleGui.find('**/triangle'), self.triangleGui.find('**/triangle_down'), self.triangleGui.find('**/triangle_over')), incButton_image_scale=2, incButton_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                         90), decButton_pos=(1.5,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             2.5), decButton_relief=None, decButton_image=(self.triangleGui.find('**/triangle'), self.triangleGui.find('**/triangle_down'), self.triangleGui.find('**/triangle_over')), decButton_image_scale=2, decButton_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      270), itemFrame_relief=None, itemFrame_pos=(-1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0), itemFrame_scale=1.0, itemFrame_image=self.charGui.find('**/chargui_frame04'), itemFrame_image_scale=(13,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           10,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           10), itemFrame_image_pos=(2.4,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     -2), itemFrame_text_fg=(1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             1), forceHeight=1.1, numItemsVisible=5)
        return dsl

    def makeLabel(self, te, index, others=[]):
        alig = others[0]
        if alig == TextNode.ARight:
            newpos = (0.44, 0, 0)
        elif alig == TextNode.ALeft:
            newpos = (0, 0, 0)
        else:
            newpos = (2.3, 0, 0)
        df = DirectFrame(state='normal', relief=None, text=te, text_scale=1.0, text_pos=newpos, text_align=alig, text_fg=(1,
                                                                                                                          1,
                                                                                                                          1,
                                                                                                                          1), textMayChange=0)
        df.bind(DGG.B1PRESS, lambda x, df=df: self.nameClickedOn(index))
        return df