from direct.gui.DirectGui import *
from pandac.PandaModules import *

class DialMeter(DirectFrame):
    MeterFull = None
    MeterHalf = None

    def __init__(self, parent, **kw):
        optiondefs = (
         (
          'state', DGG.DISABLED, None), ('relief', None, None), ('meterColor', VBase4(0, 0, 0, 1), None), ('completeColor', None, None), ('baseColor', VBase4(1, 1, 1, 1), None), ('wantCover', True, None), ('dangerRatio', 0.25, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent=NodePath(), **kw)
        self.initialiseoptions(DialMeter)
        if self.MeterFull == None:
            card = loader.loadModel('models/textureCards/dialmeter')
            self.MeterFull = card.find('**/dialmeter_full')
            self.MeterHalf = card.find('**/dialmeter_half')
        self.meterFace = self.MeterFull.copyTo(self)
        self.meterFace.setTransparency(1)
        self.meterFace.setScale(1.15)
        self.meterFace.flattenStrong()
        self.meterFace.setColor(self['baseColor'])
        self.meterFaceHalf1 = self.MeterHalf.copyTo(self)
        self.meterFaceHalf1.setTransparency(1)
        self.meterFaceHalf1.setScale(1.1)
        self.meterFaceHalf1.flattenStrong()
        self.meterFaceHalf1.setColor(self['meterColor'])
        self.meterFaceHalf1.setY(-0.01)
        self.meterFaceHalf2 = self.MeterHalf.copyTo(self)
        self.meterFaceHalf2.setTransparency(1)
        self.meterFaceHalf2.setScale(1.1)
        self.meterFaceHalf2.flattenStrong()
        self.meterFaceHalf2.setColor(self['baseColor'])
        self.meterFaceHalf2.setY(-0.015)
        if self['wantCover']:
            cover = self.MeterFull.copyTo(self)
            cover.setColor(self['baseColor'])
            cover.setTransparency(1)
            cover.setScale(0.87)
            cover.flattenStrong()
        self.reparentTo(parent or aspect2d)
        self.backwards = 0
        return

    def setBackwards(self):
        self.backwards = 1

    def update(self, val, max):
        progress = 0
        if max > 0:
            progress = float(val) / max
        if progress == 0:
            meterColor = self['baseColor']
        elif progress == 1 and self['completeColor']:
            meterColor = self['completeColor']
        else:
            if progress <= self['dangerRatio']:
                meterColor = Vec4(0.8, 0.0, 0.0, 1.0)
            else:
                meterColor = self['meterColor']
            self.meterFaceHalf1.clearColorScale()
            self.meterFaceHalf2.clearColorScale()
            if progress == 0:
                self.meterFaceHalf1.hide()
                self.meterFaceHalf2.hide()
                self.meterFace.setColor(meterColor)
            else:
                if progress == 1:
                    self.meterFaceHalf1.hide()
                    self.meterFaceHalf2.hide()
                    self.meterFace.setColor(meterColor)
                else:
                    self.meterFaceHalf1.show()
                    self.meterFaceHalf2.show()
                    self.meterFace.setColor(self['baseColor'])
                    if progress < 0.5:
                        self.meterFaceHalf1.setColor(meterColor)
                        self.meterFaceHalf2.setColor(self['baseColor'])
                    else:
                        self.meterFaceHalf1.setColor(meterColor)
                        self.meterFaceHalf2.setColor(meterColor)
                        if self.backwards:
                            progress = progress - 0.5
                        progress = progress + 0.5
                startPoint = 180
                clockWise = 1
                if self.backwards:
                    self.meterFaceHalf2.setR(-180 * (progress / 0.5))
                self.meterFaceHalf1.setR(startPoint)
                self.meterFaceHalf2.setR(startPoint + clockWise * 180 * (progress / 0.5))