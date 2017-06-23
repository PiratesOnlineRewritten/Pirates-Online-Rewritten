from direct.gui.DirectGui import *
from pandac.PandaModules import *

class ChangeDialMeter(DirectFrame):
    MeterFull = None
    MeterHalf = None

    def __init__(self, parent, **kw):
        optiondefs = (
         (
          'state', DGG.DISABLED, None), ('relief', None, None), ('meterColor', VBase4(0, 0, 0, 1), None), ('meterColor2', VBase4(1, 1, 1, 1), None), ('baseColor', VBase4(1, 1, 1, 1), None), ('wantCover', True, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent=NodePath(), **kw)
        self.initialiseoptions(ChangeDialMeter)
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
        self.meterFaceHalf1.setScale(1.07)
        self.meterFaceHalf1.flattenStrong()
        self.meterFaceHalf1.setColor(self['meterColor'])
        self.meterFaceHalf2 = self.MeterHalf.copyTo(self)
        self.meterFaceHalf2.setTransparency(1)
        self.meterFaceHalf2.setScale(1.07)
        self.meterFaceHalf2.flattenStrong()
        self.meterFaceHalf2.setColor(self['meterColor2'])
        self.meterFaceHalf3 = self.MeterHalf.copyTo(self)
        self.meterFaceHalf3.setTransparency(1)
        self.meterFaceHalf3.setScale(1.07)
        self.meterFaceHalf3.flattenStrong()
        self.meterFaceHalf3.setColor(self['baseColor'])
        if self['wantCover']:
            cover = self.MeterFull.copyTo(self)
            cover.setColor(self['baseColor'])
            cover.setTransparency(1)
            cover.setScale(0.87)
            cover.flattenStrong()
        self.reparentTo(parent or aspect2d)
        return

    def update(self, val, val2, max):
        progress = 0
        if max > 0:
            progress = float(val) / max
            progress2 = float(val2) / max
        self.meterFaceHalf1.clearColorScale()
        self.meterFaceHalf2.clearColorScale()
        self.meterFaceHalf3.clearColorScale()
        if progress2 == 0:
            self.meterFaceHalf1.hide()
            self.meterFaceHalf2.hide()
            self.meterFaceHalf3.hide()
            self.meterFace.setColor(self['baseColor'])
        elif progress2 == 1:
            self.meterFaceHalf1.hide()
            self.meterFaceHalf2.hide()
            self.meterFaceHalf3.hide()
            self.meterFace.setColor(self['meterColor'])
        else:
            self.meterFaceHalf1.show()
            self.meterFaceHalf2.show()
            self.meterFaceHalf3.show()
            self.meterFace.setColor(self['baseColor'])
            if progress2 < 0.5:
                self.meterFaceHalf1.setColor(self['meterColor'])
                self.meterFaceHalf2.setColor(self['meterColor2'])
                self.meterFaceHalf3.setColor(self['baseColor'])
                self.meterFaceHalf2.setR(-180 * (progress / 0.5))
                self.meterFaceHalf3.setR(-180 * (progress2 / 0.5))
            elif progress2 - progress < 0.5:
                self.meterFaceHalf1.setColor(self['meterColor'])
                self.meterFaceHalf2.setColor(self['meterColor2'])
                self.meterFaceHalf3.setColor(self['meterColor'])
                progress2 = progress2 - 0.5
                progress = progress - 0.5
                self.meterFaceHalf2.setR(-180 * (progress2 / 0.5))
                self.meterFaceHalf3.setR(-180 * (progress / 0.5))
            else:
                self.meterFaceHalf1.setColor(self['meterColor'])
                self.meterFaceHalf2.setColor(self['meterColor2'])
                self.meterFaceHalf3.setColor(self['meterColor2'])
                progress = progress - 0.5
                progress2 = progress2 - 0.5
                self.meterFaceHalf2.setR(-180 * (progress / 0.5))
                self.meterFaceHalf3.setR(-180 * (progress2 / 0.5))