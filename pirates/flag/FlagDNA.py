if __name__ == '__main__':
    from direct.showbase import ShowBase
from direct.showbase import PythonUtil
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
import FlagGlobals
import random

class FlagDNA(AvatarDNA.AvatarDNA):
    DefaultShapeData = 0
    DefaultBackgroundData = [0, 1, 0, 0, 0, 0, 0]
    DefaultLayoutData = [0, 128, 128, 0, 2]
    DefaultEmblemData = [0, 0, 0, 0, 4]

    def __init__(self):
        self.shape = 0
        self.bgData = self.DefaultBackgroundData[:]
        self.layoutData = self.DefaultLayoutData[:]
        self.emblems = {}

    def __repr__(self):
        return `[
         self.shape, self.bgData, self.layoutData, self.emblems]`

    def __str__(self):
        output = 'Flag DNA\n'
        output += '------------------------------\n'
        output += ' Shape\n'
        output += ' -----\n'
        output += '  %-20s%-20s\n' % ('Style:', FlagGlobals.Shapes.getString(self.getShapeStyle()))
        output += ' \nBackground\n'
        output += ' ----------\n'
        output += '  %-20s%-20s\n' % ('Style:', FlagGlobals.Backgrounds.getString(self.getBackgroundStyle()))
        output += '  %-20s %-20s\n' % ('Color-0:', `(FlagGlobals.Colors[self.getBackgroundColor(0)])`)
        output += '  %-20s %-20s\n' % ('Color-1:', `(FlagGlobals.Colors[self.getBackgroundColor(1)])`)
        output += '  %-20s %-20s\n' % ('Color-2:', `(FlagGlobals.Colors[self.getBackgroundColor(2)])`)
        output += '  %-20s %-20s\n' % ('Color-3:', `(FlagGlobals.Colors[self.getBackgroundColor(3)])`)
        output += '  %-20s %-20s\n' % ('H-flip:', `(bool(self.getBackgroundHorizontalFlip()))`)
        output += '  %-20s %-20s\n' % ('V-flip:', `(bool(self.getBackgroundVerticalFlip()))`)
        output += ' \nLayout\n'
        output += ' ----------\n'
        output += '  %-20s%-20s\n' % ('Style:', FlagGlobals.Backgrounds.getString(self.getLayoutStyle()))
        output += '  %-20s %-20s\n' % ('X-Pos:', `(self.getLayoutXPos())`)
        output += '  %-20s %-20s\n' % ('Y-Pos:', `(self.getLayoutYPos())`)
        output += '  %-20s %-20s\n' % ('R-Val:', `(self.getLayoutRVal())`)
        output += '  %-20s %-20s\n' % ('Scale:', `(self.getLayoutScale())`)
        for enum in self.getEmblemIndices():
            output += ' \nEmblem-%02d\n' % enum
            output += ' ---------\n'
            output += '  %-20s %-20s\n' % ('Style', FlagGlobals.Emblems.getString(self.getEmblemStyle(enum)))
            output += '  %-20s %-20s\n' % ('Color:', `(FlagGlobals.Colors[self.getEmblemColor(enum)])`)
            output += '  %-20s %-20s\n' % ('Pos:', `(self.getEmblemPos(enum))`)
            output += '  %-20s %-20s\n' % ('R-Val:', `(self.getEmblemRVal(enum))`)
            output += '  %-20s %-20s\n' % ('Scale:', `(self.getEmblemScale(enum))`)

        return output

    def setShapeStyle(self, style):
        self.__setShapeStyle(style)

    def setBackground(self, style=None, color_0=None, color_1=None, color_2=None, color_3=None, hFlip=None, vFlip=None):
        if style is not None:
            self.__setBackgroundStyle(style)
        if color_0 is not None:
            self.__setBackgroundColor(0, color_0)
        if color_1 is not None:
            self.__setBackgroundColor(1, color_1)
        if color_2 is not None:
            self.__setBackgroundColor(2, color_2)
        if color_3 is not None:
            self.__setBackgroundColor(3, color_3)
        if hFlip is not None:
            self.__setBackgroundHorizontalFlip(hFlip)
        if vFlip is not None:
            self.__setBackgroundVerticalFlip(vFlip)
        return

    def setLayout(self, style=None, xpos=None, ypos=None, rval=None, scale=None):
        if style is not None:
            self.__setLayoutStyle(style)
        if xpos is not None:
            self.__setLayoutXPos(xpos)
        if ypos is not None:
            self.__setLayoutYPos(ypos)
        if rval is not None:
            self.__setLayoutRVal(rval)
        if scale is not None:
            self.__setLayoutScale(scale)
        return

    def setEmblem(self, index, style=None, color=None, pos=None, rval=None, scale=None):
        emblem = self.emblems.setdefault(index, self.DefaultEmblemData[:])
        if style is not None:
            self.__setEmblemStyle(index, style)
        if color is not None:
            self.__setEmblemColor(index, color)
        if pos is not None:
            self.__setEmblemPos(index, pos)
        if rval is not None:
            self.__setEmblemRVal(index, rval)
        if scale is not None:
            self.__setEmblemScale(index, scale)
        return

    def clearEmblem(self, index):
        self.emblems.pop(index, None)
        return

    def flattenEmblemIndices(self):
        indices = self.getEmblemIndices()
        indices.sort()
        newEmblems = dict(zip(range(len(indices)), [ self.emblems[x] for x in indices ]))
        self.emblems = newEmblems

    def __setShapeStyle(self, val):
        self.shape = PythonUtil.clampScalar(val, 0, FlagGlobals.ShapeCount)

    def __setBackgroundStyle(self, val):
        self.bgData[0] = PythonUtil.clampScalar(val, 0, FlagGlobals.BackgroundCount - 1)

    def __setBackgroundColor(self, index, val):
        self.bgData[1 + index] = PythonUtil.clampScalar(val, 0, FlagGlobals.ColorCount - 1)

    def __setBackgroundHorizontalFlip(self, val):
        self.bgData[5] = bool(val)

    def __setBackgroundVerticalFlip(self, val):
        self.bgData[6] = bool(val)

    def __setLayoutStyle(self, val):
        self.layoutData[0] = PythonUtil.clampScalar(val, 0, FlagGlobals.LayoutCount - 1)

    def __setLayoutXPos(self, val):
        self.layoutData[1] = PythonUtil.clampScalar(val, FlagGlobals.XPosLowCount, FlagGlobals.XPosHiCount - 1)

    def __setLayoutYPos(self, val):
        self.layoutData[2] = PythonUtil.clampScalar(val, FlagGlobals.YPosLowCount, FlagGlobals.YPosHiCount - 1)

    def __setLayoutRVal(self, val):
        self.layoutData[3] = int(val) % FlagGlobals.RotationCount

    def __setLayoutScale(self, val):
        self.layoutData[4] = PythonUtil.clampScalar(val, 0, FlagGlobals.LayoutScaleCount - 1)

    def __setEmblemStyle(self, emblemNum, val):
        self.emblems[emblemNum][0] = PythonUtil.clampScalar(val, 0, FlagGlobals.EmblemCount - 1)

    def __setEmblemColor(self, emblemNum, val):
        self.emblems[emblemNum][1] = PythonUtil.clampScalar(val, 0, FlagGlobals.ColorCount - 1)

    def __setEmblemPos(self, emblemNum, val):
        PosCount = len(FlagGlobals.LayoutOffsets[self.layoutData[0]])
        self.emblems[emblemNum][2] = PythonUtil.clampScalar(val, 0, PosCount - 1)

    def __setEmblemRVal(self, emblemNum, val):
        self.emblems[emblemNum][3] = int(val) % FlagGlobals.RotationCount

    def __setEmblemScale(self, emblemNum, val):
        self.emblems[emblemNum][4] = PythonUtil.clampScalar(val, 0, FlagGlobals.EmblemScaleCount - 1)

    def getShapeStyle(self):
        return self.shape

    def getBackgroundStyle(self):
        return self.bgData[0]

    def getBackgroundColor(self, index):
        return self.bgData[1 + index]

    def getBackgroundHorizontalFlip(self):
        return self.bgData[5]

    def getBackgroundVerticalFlip(self):
        return self.bgData[6]

    def getLayoutStyle(self):
        return self.layoutData[0]

    def getLayoutXPos(self):
        return self.layoutData[1]

    def getLayoutYPos(self):
        return self.layoutData[2]

    def getLayoutRVal(self):
        return self.layoutData[3]

    def getLayoutScale(self):
        return self.layoutData[4]

    def getEmblemIndices(self):
        return self.emblems.keys()

    def getNumEmblems(self):
        return len(self.emblems)

    def getEmblemStyle(self, emblemNum):
        return self.emblems[emblemNum][0]

    def getEmblemColor(self, emblemNum):
        return self.emblems[emblemNum][1]

    def getEmblemPos(self, emblemNum):
        return self.emblems[emblemNum][2]

    def getEmblemRVal(self, emblemNum):
        return self.emblems[emblemNum][3]

    def getEmblemScale(self, emblemNum):
        return self.emblems[emblemNum][4]

    def __getRandomShapeStyle(self):
        return random.randrange(0, len(FlagGlobals.Shapes))

    def __getRandomBackgroundStyle(self):
        return random.randrange(0, len(FlagGlobals.Backgrounds))

    def __getRandomBackgroundColor(self):
        return random.randrange(0, len(FlagGlobals.Colors))

    def __getRandomBackgroundHorizontalFlip(self):
        return random.randrange(0, 2)

    def __getRandomBackgroundVerticalFlip(self):
        return random.randrange(0, 2)

    def __getRandomLayoutStyle(self):
        return random.randrange(0, len(FlagGlobals.Layouts))

    def __getRandomLayoutXPos(self):
        return random.randrange(64, 192)

    def __getRandomLayoutYPos(self):
        return random.randrange(55, 200)

    def __getRandomLayoutRVal(self):
        return random.randrange(0, 12)

    def __getRandomLayoutScale(self):
        return random.randrange(0, 5)

    def __getRandomNumEmblems(self):
        return random.randint(0, FlagGlobals.MaxEmblemCount)

    def __getRandomEmblemStyle(self):
        return random.randrange(0, len(FlagGlobals.Emblems))

    def __getRandomEmblemColor(self):
        return random.randrange(0, len(FlagGlobals.Colors))

    def __getRandomEmblemPos(self, index=-1):

        def genRandPos():
            return random.randrange(0, len(FlagGlobals.LayoutOffsets[self.layoutData[0]]))

        pos = genRandPos()
        return pos

    def __getRandomEmblemRVal(self):
        return random.randrange(0, 12)

    def __getRandomEmblemScale(self):
        return random.randrange(0, 9)

    def randomizeShape(self):
        self.shape = self.__getRandomShapeStyle()

    def randomizeBackground(self, style=False, colors=False, flip=False):
        if style | colors | flip == False:
            style = True
            colors = True
            flip = True
        if style:
            self.bgData[0] = self.__getRandomShapeStyle()
        if colors:
            self.bgData[1] = self.__getRandomBackgroundColor()
            self.bgData[2] = self.__getRandomBackgroundColor()
            self.bgData[3] = self.__getRandomBackgroundColor()
            self.bgData[4] = self.__getRandomBackgroundColor()
        if flip:
            self.bgData[5] = self.__getRandomBackgroundHorizontalFlip()
            self.bgData[6] = self.__getRandomBackgroundVerticalFlip()

    def randomizeEmblem(self, index):
        eData = [
         self.__getRandomEmblemStyle(), self.__getRandomEmblemColor(), self.__getRandomEmblemPos(index), self.__getRandomEmblemRVal(), self.__getRandomEmblemScale()]
        self.emblems[index] = eData

    def randomize(self, shape=False, bg=False, emblems=False):
        if shape | bg | emblems == False:
            shape = True
            bg = True
            emblems = True
        if shape:
            self.randomizeShape()
        if bg:
            self.randomizeBackground()
        if emblems:
            for x in range(self.__getRandomNumEmblems()):
                self.setEmblem(x)
                self.randomizeEmblem(x)

    def getRandomEmblemPos(self, index=-1):
        return self.__getRandomEmblemPos(index)

    def getDNAString(self):
        data = PyDatagram()
        data.addUint8(self.shape)
        for item in self.bgData:
            data.addUint8(item)

        for item in self.layoutData:
            data.addUint8(item)

        for enum in self.emblems.keys():
            emblem = self.emblems.get(enum, None)
            if emblem:
                for item in emblem:
                    data.addUint8(item)

        return data.getMessage()

    def setDNAString(self, dnaStr):
        data = PyDatagram(dnaStr)
        iter = PyDatagramIterator(data)
        self.setShapeStyle(int(iter.getUint8()))
        bgData = [
         0] * len(self.bgData)
        layoutData = [0] * len(self.layoutData)
        for x in range(len(bgData)):
            bgData[x] = int(iter.getUint8())

        self.setBackground(*bgData)
        for x in range(len(layoutData)):
            layoutData[x] = int(iter.getUint8())

        self.setLayout(*layoutData)
        self.emblems = {}
        eCount = 0
        while iter.getRemainingSize() >= len(self.DefaultEmblemData):
            edata = self.DefaultEmblemData[:]
            for x in range(0, len(edata)):
                edata[x] = int(iter.getUint8())

            self.setEmblem(eCount, *edata)
            eCount += 1


if __name__ == '__main__':
    f = FlagDNA()
    print f
    print `f`