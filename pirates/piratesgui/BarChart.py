from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer

class BarChart(DirectFrame):

    def __init__(self, data, height, width, name='', titleColor=(1.0, 1.0, 1.0, 1.0), maxValue=None):
        self.width = width
        self.height = height
        self.barHeight = self.height / len(data) * 0.666
        self.titleColor = titleColor
        self.maxValue = maxValue
        self.data = data
        DirectFrame.__init__(self, relief=None, state=DGG.NORMAL)
        self.initialiseoptions(BarChart)
        self.name = name
        self.statBars = []
        self.title = DirectFrame(parent=self, relief=None, text=self.name, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.03,
                                                                                                                                                             0.01), text_fg=self.titleColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0, 0, self.height + 0.02))
        self.loadStatBars(self.data)

    def loadStatBars(self, data):
        for item in data:
            self.addBar(item, repack=0)

        self.repackBars()

    def addBar(self, data, repack=1):
        meter = DirectWaitBar(parent=self, relief=DGG.RAISED, borderWidth=(0.004, 0.004), range=data[2], value=data[1], frameColor=(0,
                                                                                                                                    0,
                                                                                                                                    0,
                                                                                                                                    0), barColor=(0.1,
                                                                                                                                                  0.7,
                                                                                                                                                  0.1,
                                                                                                                                                  1), frameSize=(0.17, self.width - 0.1, -self.barHeight * 0.25, self.barHeight * 0.75), text=str(data[1]), text_align=TextNode.ALeft, text_scale=0.03, text_fg=(1,
                                                                                                                                                                                                                                                                                                                 1,
                                                                                                                                                                                                                                                                                                                 1,
                                                                                                                                                                                                                                                                                                                 1), text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                  1), text_pos=(0,
                                                                                                                                                                                                                                                                                                                                                0), pos=(0,
                                                                                                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                                                                                                         0))
        if self.maxValue:
            meter['range'] = self.maxValue
        meterWidth = meter['frameSize'][1] - meter['frameSize'][0]
        percentFilled = float(meter['value']) / float(meter['range'])
        print percentFilled
        newTextPos = meterWidth * percentFilled + 0.18
        meter['text_pos'] = (newTextPos, 0)
        label = DirectLabel(parent=meter, relief=None, text=data[0], text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_pos=(0,
                                                                                                                                                       0), text_fg=PiratesGuiGlobals.TextFG2)
        self.statBars.append([meter, label])
        if repack:
            self.repackPanels()
        return

    def clearAllBars(self):
        for i in range(len(self.statBars)):
            self.statBars[i][0].destroy()

        self.statBars = []

    def repackBars(self):
        for i in range(len(self.statBars)):
            self.statBars[i][0].setPos(0, 0, self.height + 0.02 - (i + 1) * (self.height - 0.02) / len(self.statBars))

    def refreshBars(self, data):
        for statBar, datum in zip(self.statBars, data):
            meter = statBar[0]
            label = statBar[1]
            label['text'] = datum[0]
            meter['text'] = str(datum[1])
            meter['value'] = datum[1]
            meter['range'] = datum[2]
            if self.maxValue:
                meter['range'] = self.maxValue
            meterWidth = meter['frameSize'][1] - meter['frameSize'][0]
            percentFilled = min(1.0, float(meter['value']) / float(meter['range']))
            newTextPos = meterWidth * percentFilled + 0.18
            meter['text_pos'] = (newTextPos, 0)

    def destroy(self):
        self.clearAllBars()
        DirectFrame.destroy(self)

    def show(self):
        DirectFrame.show(self)

    def hide(self):
        DirectFrame.hide(self)
