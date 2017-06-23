from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBaseGlobal import *
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.pirate import HumanDNA
from pirates.npc import Skeleton
import random

class NPCGUI(DirectFrame, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('NPCGUI')

    def __init__(self, main=None):
        self.main = main
        self.parent = main.bookModel
        self.mode = None
        self.charGui = loader.loadModel('models/gui/char_gui')
        return

    def _makeButton(self, text, command, pos, parent, text_scale=(0.2, 0.2, 0.2)):
        b = DirectButton(parent=parent, image_scale=1.3, relief=None, image=(self.charGui.find('**/chargui_frame02'), self.charGui.find('**/chargui_frame02_down'), self.charGui.find('**/chargui_frame02_over')), text=text, text_pos=(0, -0.05, 0), text_fg=(1,
                                                                                                                                                                                                                                                               1,
                                                                                                                                                                                                                                                               1,
                                                                                                                                                                                                                                                               1), text_align=TextNode.ACenter, text_scale=text_scale, command=command, pos=pos)
        return b

    def enter(self):
        self.notify.debug('enter')
        if self.mode == None:
            self.load()
            self.mode = -1
        messenger.send('wakeup')
        self.showShapeCollections()
        self.show()
        return

    def exit(self):
        self.notify.debug('called NPCGUI exit')
        if self.mode != None:
            self.hide()
        return

    def save(self):
        if self.mode == -1:
            pass

    def assignAvatar(self, avatar):
        self.avatar = avatar

    def load(self):
        self.notify.debug('loading NPCGUI')
        self.loadShapeGUI()
        self.setupButtons()

    def loadShapeGUI(self):
        self.shapeFrameTitle = DirectFrame(parent=self.parent, pos=(0, 0, 0.8), scale=(0.66,
                                                                                       0.4,
                                                                                       0.53))
        self.shapeFrameTitle.hide()

    def unload(self):
        self.notify.debug('called NPCGUI unload')
        del self.main
        del self.parent
        del self.avatar

    def showShapeCollections(self):
        self.shapeFrameTitle.show()

    def hideShapeCollections(self):
        self.shapeFrameTitle.hide()

    def show(self):
        pass

    def hide(self):
        self.mode = -1
        self.hideShapeCollections()

    def setupButtons(self):
        self.gp1Button = self._makeButton(text=PLocalizer.SkeletonGP1, command=self.handleGP1, pos=(-0.95, 0, -2.0), parent=self.shapeFrameTitle)
        self.gp2Button = self._makeButton(text=PLocalizer.SkeletonGP2, command=self.handleGP2, pos=(-0.95, 0, -2.5), parent=self.shapeFrameTitle)
        self.gp4Button = self._makeButton(text=PLocalizer.SkeletonGP4, command=self.handleGP4, pos=(-0.95, 0, -3.0), parent=self.shapeFrameTitle)
        self.gp8Button = self._makeButton(text=PLocalizer.SkeletonGP8, command=self.handleGP8, pos=(-0.95, 0, -3.5), parent=self.shapeFrameTitle)
        self.djcrButton = self._makeButton(text=PLocalizer.SkeletonDJ1, command=self.handlecr, pos=(0.05,
                                                                                                    0,
                                                                                                    -1.75), parent=self.shapeFrameTitle)
        self.djjmButton = self._makeButton(text=PLocalizer.SkeletonDJ2, command=self.handlejm, pos=(0.05,
                                                                                                    0,
                                                                                                    -2.25), parent=self.shapeFrameTitle, text_scale=(0.18,
                                                                                                                                                     0.2,
                                                                                                                                                     0.2))
        self.djkoButton = self._makeButton(text=PLocalizer.SkeletonDJ3, command=self.handleko, pos=(0.05,
                                                                                                    0,
                                                                                                    -2.75), parent=self.shapeFrameTitle)
        self.djpaButton = self._makeButton(text=PLocalizer.SkeletonDJ4, command=self.handlepa, pos=(0.05,
                                                                                                    0,
                                                                                                    -3.25), parent=self.shapeFrameTitle)
        self.djtwButton = self._makeButton(text=PLocalizer.SkeletonDJ5, command=self.handletw, pos=(0.05,
                                                                                                    0,
                                                                                                    -3.75), parent=self.shapeFrameTitle)
        self.sp1Button = self._makeButton(text=PLocalizer.SkeletonSP1, command=self.handlesp1, pos=(1.05,
                                                                                                    0,
                                                                                                    -1), parent=self.shapeFrameTitle)
        self.sp2Button = self._makeButton(text=PLocalizer.SkeletonSP2, command=self.handlesp2, pos=(1.05,
                                                                                                    0,
                                                                                                    -1.5), parent=self.shapeFrameTitle)
        self.sp3Button = self._makeButton(text=PLocalizer.SkeletonSP3, command=self.handlesp3, pos=(1.05,
                                                                                                    0,
                                                                                                    -2), parent=self.shapeFrameTitle)
        self.sp4Button = self._makeButton(text=PLocalizer.SkeletonSP4, command=self.handlesp4, pos=(1.05,
                                                                                                    0,
                                                                                                    -2.5), parent=self.shapeFrameTitle)
        self.fr1Button = self._makeButton(text=PLocalizer.SkeletonFR1, command=self.handlefr1, pos=(1.05,
                                                                                                    0,
                                                                                                    -3.5), parent=self.shapeFrameTitle)
        self.fr2Button = self._makeButton(text=PLocalizer.SkeletonFR2, command=self.handlefr2, pos=(1.05,
                                                                                                    0,
                                                                                                    -4), parent=self.shapeFrameTitle)
        self.fr3Button = self._makeButton(text=PLocalizer.SkeletonFR3, command=self.handlefr3, pos=(1.05,
                                                                                                    0,
                                                                                                    -4.5), parent=self.shapeFrameTitle)
        self.fr4Button = self._makeButton(text=PLocalizer.SkeletonFR4, command=self.handlefr4, pos=(1.05,
                                                                                                    0,
                                                                                                    -5), parent=self.shapeFrameTitle)

    def reset(self):
        self.avatar.resetPick()
        self.handleGP1()

    def randomPick(self):
        cList = range(0, 16)
        cList.remove(self.main.skeletonType)
        choice = random.choice(cList)
        if choice == 0:
            self.handleGP1()
        elif choice == 1:
            self.handleGP2()
        elif choice == 2:
            self.handleGP4()
        elif choice == 3:
            self.handleGP8()
        elif choice == 4:
            self.handlecr()
        elif choice == 5:
            self.handlejm()
        elif choice == 6:
            self.handleko()
        elif choice == 7:
            self.handlepa()
        elif choice == 8:
            self.handletw()
        elif choice == 9:
            self.handlesp1()
        elif choice == 10:
            self.handlesp2()
        elif choice == 11:
            self.handlesp3()
        elif choice == 12:
            self.handlesp4()
        elif choice == 13:
            self.handlefr1()
        elif choice == 14:
            self.handlefr2()
        elif choice == 15:
            self.handlefr3()
        elif choice == 16:
            self.handlefr4()
        self.avatar.randomPick()
        self.avatar.setFromDNA()

    def handleGP1(self):
        self.main.loadSkeleton(0)
        self.main.placeSkeleton(0)
        self.notify.debug('clicked gp1')

    def handleGP2(self):
        self.main.loadSkeleton(1)
        self.main.placeSkeleton(1)
        self.notify.debug('clicked gp2')

    def handleGP4(self):
        self.main.loadSkeleton(2)
        self.main.placeSkeleton(2)
        self.notify.debug('clicked gp4')

    def handleGP8(self):
        self.main.loadSkeleton(3)
        self.main.placeSkeleton(3)
        self.notify.debug('clicked gp8')

    def handlecr(self):
        self.main.loadSkeleton(4)
        self.main.placeSkeleton(4)
        self.notify.debug('clicked crash')

    def handlejm(self):
        self.main.loadSkeleton(5)
        self.main.placeSkeleton(5)
        self.notify.debug('clicked jimmylegs')

    def handleko(self):
        self.main.loadSkeleton(6)
        self.main.placeSkeleton(6)
        self.notify.debug('clicked koleniko')

    def handlepa(self):
        self.main.loadSkeleton(7)
        self.main.placeSkeleton(7)
        self.notify.debug('clicked palifico')

    def handletw(self):
        self.main.loadSkeleton(8)
        self.main.placeSkeleton(8)
        self.notify.debug('clicked twins')

    def handlesp1(self):
        self.main.loadSkeleton(9)
        self.main.placeSkeleton(9)
        self.notify.debug('clicked sp1')

    def handlesp2(self):
        self.main.loadSkeleton(10)
        self.main.placeSkeleton(10)
        self.notify.debug('clicked sp2')

    def handlesp3(self):
        self.main.loadSkeleton(11)
        self.main.placeSkeleton(11)
        self.notify.debug('clicked sp3')

    def handlesp4(self):
        self.main.loadSkeleton(12)
        self.main.placeSkeleton(12)
        self.notify.debug('clicked sp4')

    def handlefr1(self):
        self.main.loadSkeleton(13)
        self.main.placeSkeleton(13)
        self.notify.debug('clicked fr1')

    def handlefr2(self):
        self.main.loadSkeleton(14)
        self.main.placeSkeleton(14)
        self.notify.debug('clicked fr2')

    def handlefr3(self):
        self.main.loadSkeleton(15)
        self.main.placeSkeleton(15)
        self.notify.debug('clicked fr3')

    def handlefr4(self):
        self.main.loadSkeleton(16)
        self.main.placeSkeleton(16)
        self.notify.debug('clicked fr4')