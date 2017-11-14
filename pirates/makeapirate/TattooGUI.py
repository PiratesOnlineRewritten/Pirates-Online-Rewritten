from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBaseGlobal import *
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from CharGuiBase import CharGuiSlider, CharGuiPicker
import random
from pirates.pirate import HumanDNA
from math import sin
from math import cos
from math import pi
import TattooGlobals
import PirateMale
import PirateFemale
Zone1_Tab = 0
Zone2_Tab = 1
Zone3_Tab = 2
Zone4_Tab = 3
Zone5_Tab = 4
Zone6_Tab = 5
Zone7_Tab = 6
Zone8_Tab = 7
ZONE1 = 0
ZONE2 = 1
ZONE3 = 2
ZONE4 = 3
ZONE5 = 4
ZONE6 = 5
ZONE7 = 6
ZONE8 = 7
TYPE = 0
OFFSETX = 1
OFFSETY = 2
SCALE = 3
ROTATE = 4
COLOR = 5

class TattooGUI(DirectFrame, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('TattooGUI')

    def __init__(self, main=None):
        self.main = main
        self._parent = main.bookModel
        self.avatar = main.avatar
        self.mode = None
        self.shownMale = None
        self.shownFemale = None
        self.vTattoos = [
         1, 2, 3, 4, 5, 6, 7, 8]
        self.currTattoo = -1
        self.cStage = TextureStage('cardstage')
        factory = CardMaker('fact')
        factory.setFrame(-0.5, 0.5, -0.5, 0.5)
        self.map = NodePath(factory.generate())
        return

    def enter(self):
        self.notify.debug('enter')
        if self.mode == None:
            self.load()
            self.mode = -1
        self.show()
        return

    def exit(self):
        self.hide()

    def save(self):
        if self.mode == -1:
            pass
        self.saveDNA()

    def assignAvatar(self, avatar):
        self.avatar = avatar
        self.applyBaseTexture(self.avatar.getTattooBaseTexture())

    def load(self):
        self.loadTabs()
        self.loadZone1GUI()
        self.map.reparentTo(self.zone1Frame)
        self.map.setPos(1.5, 0, -0.6)
        self.map.setScale(1.4)
        self.setupButtons()

    def loadZone1GUI(self):
        self.zone1FrameTitle = DirectFrame(parent=self._parent, relief=DGG.FLAT, frameColor=(1,
                                                                                            1,
                                                                                            0,
                                                                                            1), text='Chest Tattoo', text_scale=0.18, text_pos=(0,
                                                                                                                                                0), pos=(0.0,
                                                                                                                                                         0,
                                                                                                                                                         0.7), scale=(0.66,
                                                                                                                                                                      0.4,
                                                                                                                                                                      0.53))
        self.zone1FrameTitle.hide()
        self.zone1Frame = DirectFrame(parent=self.zone1FrameTitle, relief=DGG.FLAT, frameSize=(-0.2, 0.2, -0.05, 0.05), frameColor=(0.8,
                                                                                                                                    0.8,
                                                                                                                                    0.8,
                                                                                                                                    0), text='Blank', text_scale=0.14, text_pos=(0, -0.02), text_align=TextNode.ACenter, text_fg=(1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1), text_shadow=(0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   1), pos=(-1.0, 0.0, -0.2))
        self.zone1Frame.hide()
        self.zone2FrameTitle = DirectFrame(parent=self._parent, relief=DGG.FLAT, frameColor=(1,
                                                                                            1,
                                                                                            0,
                                                                                            1), text='LeftArm Tattoo', text_scale=0.18, text_pos=(0,
                                                                                                                                                  0), pos=(0.0,
                                                                                                                                                           0,
                                                                                                                                                           0.7), scale=(0.66,
                                                                                                                                                                        0.4,
                                                                                                                                                                        0.53))
        self.zone2FrameTitle.hide()
        self.zone2Frame = DirectFrame(parent=self.zone2FrameTitle, relief=DGG.FLAT, frameSize=(-0.2, 0.2, -0.05, 0.05), frameColor=(0.8,
                                                                                                                                    0.8,
                                                                                                                                    0.8,
                                                                                                                                    0), text='Blank', text_scale=0.14, text_pos=(0, -0.02), text_align=TextNode.ACenter, text_fg=(1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1), text_shadow=(0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   1), pos=(-1.0, 0.0, -0.2))
        self.zone2Frame.hide()
        self.zone3FrameTitle = DirectFrame(parent=self._parent, relief=DGG.FLAT, frameColor=(1,
                                                                                            1,
                                                                                            0,
                                                                                            1), text='RightArm Tattoo', text_scale=0.18, text_pos=(0,
                                                                                                                                                   0), pos=(0.0,
                                                                                                                                                            0,
                                                                                                                                                            0.7), scale=(0.66,
                                                                                                                                                                         0.4,
                                                                                                                                                                         0.53))
        self.zone3FrameTitle.hide()
        self.zone3Frame = DirectFrame(parent=self.zone3FrameTitle, relief=DGG.FLAT, frameSize=(-0.2, 0.2, -0.05, 0.05), frameColor=(0.8,
                                                                                                                                    0.8,
                                                                                                                                    0.8,
                                                                                                                                    0), text='Blank', text_scale=0.14, text_pos=(0, -0.02), text_align=TextNode.ACenter, text_fg=(1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1), text_shadow=(0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   1), pos=(-1.0, 0.0, -0.2))
        self.zone3Frame.hide()
        self.zone4FrameTitle = DirectFrame(parent=self._parent, relief=DGG.FLAT, frameColor=(1,
                                                                                            1,
                                                                                            0,
                                                                                            1), text='Face Tattoo', text_scale=0.18, text_pos=(0,
                                                                                                                                               0), pos=(0.0,
                                                                                                                                                        0,
                                                                                                                                                        0.7), scale=(0.66,
                                                                                                                                                                     0.4,
                                                                                                                                                                     0.53))
        self.zone4FrameTitle.hide()
        self.zone4Frame = DirectFrame(parent=self.zone4FrameTitle, relief=DGG.FLAT, frameSize=(-0.2, 0.2, -0.05, 0.05), frameColor=(0.8,
                                                                                                                                    0.8,
                                                                                                                                    0.8,
                                                                                                                                    0), text='Blank', text_scale=0.14, text_pos=(0, -0.02), text_align=TextNode.ACenter, text_fg=(1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1), text_shadow=(0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   1), pos=(-1.0, 0.0, -0.2))
        self.zone4Frame.hide()
        self.zone5FrameTitle = DirectFrame(parent=self._parent, relief=DGG.FLAT, frameColor=(1,
                                                                                            1,
                                                                                            0,
                                                                                            1), text='Zone5 Tattoo', text_scale=0.18, text_pos=(0,
                                                                                                                                                0), pos=(0.0,
                                                                                                                                                         0,
                                                                                                                                                         0.7), scale=(0.66,
                                                                                                                                                                      0.4,
                                                                                                                                                                      0.53))
        self.zone5FrameTitle.hide()
        self.zone5Frame = DirectFrame(parent=self.zone5FrameTitle, relief=DGG.FLAT, frameSize=(-0.2, 0.2, -0.05, 0.05), frameColor=(0.8,
                                                                                                                                    0.8,
                                                                                                                                    0.8,
                                                                                                                                    0), text='Blank', text_scale=0.14, text_pos=(0, -0.02), text_align=TextNode.ACenter, text_fg=(1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1), text_shadow=(0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   1), pos=(-1.0, 0.0, -0.2))
        self.zone5Frame.hide()
        self.zone6FrameTitle = DirectFrame(parent=self._parent, relief=DGG.FLAT, frameColor=(1,
                                                                                            1,
                                                                                            0,
                                                                                            1), text='Zone6 Tattoo', text_scale=0.18, text_pos=(0,
                                                                                                                                                0), pos=(0.0,
                                                                                                                                                         0,
                                                                                                                                                         0.7), scale=(0.66,
                                                                                                                                                                      0.4,
                                                                                                                                                                      0.53))
        self.zone6FrameTitle.hide()
        self.zone6Frame = DirectFrame(parent=self.zone6FrameTitle, relief=DGG.FLAT, frameSize=(-0.2, 0.2, -0.05, 0.05), frameColor=(0.8,
                                                                                                                                    0.8,
                                                                                                                                    0.8,
                                                                                                                                    0), text='Blank', text_scale=0.14, text_pos=(0, -0.02), text_align=TextNode.ACenter, text_fg=(1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1), text_shadow=(0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   1), pos=(-1.0, 0.0, -0.2))
        self.zone6Frame.hide()
        self.zone7FrameTitle = DirectFrame(parent=self._parent, relief=DGG.FLAT, frameColor=(1,
                                                                                            1,
                                                                                            0,
                                                                                            1), text='Zone7 Tattoo', text_scale=0.18, text_pos=(0,
                                                                                                                                                0), pos=(0.0,
                                                                                                                                                         0,
                                                                                                                                                         0.7), scale=(0.66,
                                                                                                                                                                      0.4,
                                                                                                                                                                      0.53))
        self.zone7FrameTitle.hide()
        self.zone7Frame = DirectFrame(parent=self.zone7FrameTitle, relief=DGG.FLAT, frameSize=(-0.2, 0.2, -0.05, 0.05), frameColor=(0.8,
                                                                                                                                    0.8,
                                                                                                                                    0.8,
                                                                                                                                    0), text='Blank', text_scale=0.14, text_pos=(0, -0.02), text_align=TextNode.ACenter, text_fg=(1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1), text_shadow=(0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   1), pos=(-1.0, 0.0, -0.2))
        self.zone7Frame.hide()
        self.zone8FrameTitle = DirectFrame(parent=self._parent, relief=DGG.FLAT, frameColor=(1,
                                                                                            1,
                                                                                            0,
                                                                                            1), text='Zone8 Tattoo', text_scale=0.18, text_pos=(0,
                                                                                                                                                0), pos=(0.0,
                                                                                                                                                         0,
                                                                                                                                                         0.7), scale=(0.66,
                                                                                                                                                                      0.4,
                                                                                                                                                                      0.53))
        self.zone8FrameTitle.hide()
        self.zone8Frame = DirectFrame(parent=self.zone8FrameTitle, relief=DGG.FLAT, frameSize=(-0.2, 0.2, -0.05, 0.05), frameColor=(0.8,
                                                                                                                                    0.8,
                                                                                                                                    0.8,
                                                                                                                                    0), text='Blank', text_scale=0.14, text_pos=(0, -0.02), text_align=TextNode.ACenter, text_fg=(1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                  1), text_shadow=(0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   1), pos=(-1.0, 0.0, -0.2))
        self.zone8Frame.hide()
        self.oXSlider = CharGuiSlider(self.main, parent=self.zone1FrameTitle, text='OffsetX', command=self.handleOxSlider, range=(0.0,
                                                                                                                                  1.0))
        self.oXSlider['extraArgs'] = [
         self.oXSlider]
        self.oXSlider.setPos(-0.5, 0, -2.0)
        self.oYSlider = CharGuiSlider(self.main, parent=self.zone1FrameTitle, text='OffsetY', command=self.handleOySlider, range=(0.0,
                                                                                                                                  1.0))
        self.oYSlider['extraArgs'] = [
         self.oYSlider]
        self.oYSlider.setPos(-0.5, 0, -2.3)
        self.scaleSlider = CharGuiSlider(self.main, parent=self.zone1FrameTitle, text='Scale', command=self.handleScaleSlider, range=(0.01,
                                                                                                                                      1))
        self.scaleSlider['extraArgs'] = [
         self.scaleSlider]
        self.scaleSlider.setPos(-0.5, 0, -2.6)
        self.rotateSlider = CharGuiSlider(self.main, parent=self.zone1FrameTitle, text='Rotate', command=self.handleRotateSlider, range=(0,
                                                                                                                                         360))
        self.rotateSlider['extraArgs'] = [
         self.rotateSlider]
        self.rotateSlider.setPos(-0.5, 0, -2.9)
        self.editZone1 = DirectButton(parent=self.zone1FrameTitle, relief=DGG.RAISED, frameSize=(-0.3, 0.3, -0.15, 0.15), borderWidth=(0.025,
                                                                                                                                       0.025), text='Edit', text_scale=0.15, text_align=TextNode.ACenter, text_pos=(0, -0.025), command=self.setEdit, extraArgs=[Zone1_Tab], pos=(-0.8, 0, -1.0))
        self.editZone2 = DirectButton(parent=self.zone2FrameTitle, relief=DGG.RAISED, frameSize=(-0.3, 0.3, -0.15, 0.15), borderWidth=(0.025,
                                                                                                                                       0.025), text='Edit', text_scale=0.15, text_align=TextNode.ACenter, text_pos=(0, -0.025), command=self.setEdit, extraArgs=[Zone2_Tab], pos=(-0.8, 0, -1.0))
        self.editZone3 = DirectButton(parent=self.zone3FrameTitle, relief=DGG.RAISED, frameSize=(-0.3, 0.3, -0.15, 0.15), borderWidth=(0.025,
                                                                                                                                       0.025), text='Edit', text_scale=0.15, text_align=TextNode.ACenter, text_pos=(0, -0.025), command=self.setEdit, extraArgs=[Zone3_Tab], pos=(-0.8, 0, -1.0))
        self.editZone4 = DirectButton(parent=self.zone4FrameTitle, relief=DGG.RAISED, frameSize=(-0.3, 0.3, -0.15, 0.15), borderWidth=(0.025,
                                                                                                                                       0.025), text='Edit', text_scale=0.15, text_align=TextNode.ACenter, text_pos=(0, -0.025), command=self.setEdit, extraArgs=[Zone4_Tab], pos=(-0.8, 0, -1.0))
        self.editZone5 = DirectButton(parent=self.zone5FrameTitle, relief=DGG.RAISED, frameSize=(-0.3, 0.3, -0.15, 0.15), borderWidth=(0.025,
                                                                                                                                       0.025), text='Edit', text_scale=0.15, text_align=TextNode.ACenter, text_pos=(0, -0.025), command=self.setEdit, extraArgs=[Zone5_Tab], pos=(-0.8, 0, -1.0))
        self.editZone5.hide()
        self.editButtons = [
         self.editZone1, self.editZone2, self.editZone3, self.editZone4, self.editZone5, self.editZone5, self.editZone5, self.editZone5]

    def loadTabs(self):
        self.zone1Tab = DirectButton(parent=self._parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='Chest', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone1_Tab], pos=(-0.97, 0, 1.02))
        self.zone1Tab.hide()
        self.zone2Tab = DirectButton(parent=self._parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='LeftArm', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone2_Tab], pos=(-0.72, 0, 1.02))
        self.zone2Tab.hide()
        self.zone3Tab = DirectButton(parent=self._parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='RightArm', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone3_Tab], pos=(-0.47, 0, 1.02))
        self.zone3Tab.hide()
        self.zone4Tab = DirectButton(parent=self._parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='Face', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone4_Tab], pos=(-0.22, 0, 1.02))
        self.zone4Tab.hide()
        self.zone5Tab = DirectButton(parent=self._parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='Zone5', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone5_Tab], pos=(0.03,
                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                           1.02))
        self.zone5Tab.hide()
        self.zone6Tab = DirectButton(parent=self._parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='Zone6', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone6_Tab], pos=(0.28,
                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                           1.02))
        self.zone6Tab.hide()
        self.zone7Tab = DirectButton(parent=self._parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='Zone7', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone7_Tab], pos=(0.53,
                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                           1.02))
        self.zone7Tab.hide()
        self.zone8Tab = DirectButton(parent=self._parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='Zone8', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone8_Tab], pos=(0.78,
                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                           1.02))
        self.zone8Tab.hide()

    def unload(self):
        del self.main
        del self._parent
        del self.avatar

    def setMode(self, mode, updateAnyways=0):
        messenger.send('wakeup')
        if not updateAnyways:
            if self.mode == mode:
                return
            else:
                self.mode = mode
        self.currTattoo = mode
        if mode == Zone1_Tab:
            self.zone1Tab['state'] = DGG.DISABLED
            self.zone1Tab['relief'] = DGG.SUNKEN
            self.showZone1TattooCollections()
            self.zone2Tab['state'] = DGG.NORMAL
            self.zone2Tab['relief'] = DGG.RAISED
            self.hideZone2TattooCollections()
            self.zone3Tab['state'] = DGG.NORMAL
            self.zone3Tab['relief'] = DGG.RAISED
            self.hideZone3TattooCollections()
            self.zone4Tab['state'] = DGG.NORMAL
            self.zone4Tab['relief'] = DGG.RAISED
            self.hideZone4TattooCollections()
            self.zone5Tab['state'] = DGG.NORMAL
            self.zone5Tab['relief'] = DGG.RAISED
            self.hideZone5TattooCollections()
            self.zone6Tab['state'] = DGG.NORMAL
            self.zone6Tab['relief'] = DGG.RAISED
            self.hideZone6TattooCollections()
            self.zone7Tab['state'] = DGG.NORMAL
            self.zone7Tab['relief'] = DGG.RAISED
            self.hideZone7TattooCollections()
            self.zone8Tab['state'] = DGG.NORMAL
            self.zone8Tab['relief'] = DGG.RAISED
            self.hideZone8TattooCollections()
            self.reparentCommonGui(self.zone1Frame, self.zone1FrameTitle)
        elif mode == Zone2_Tab:
            self.zone1Tab['state'] = DGG.NORMAL
            self.zone1Tab['relief'] = DGG.RAISED
            self.hideZone1TattooCollections()
            self.zone2Tab['state'] = DGG.DISABLED
            self.zone2Tab['relief'] = DGG.SUNKEN
            self.showZone2TattooCollections()
            self.zone3Tab['state'] = DGG.NORMAL
            self.zone3Tab['relief'] = DGG.RAISED
            self.hideZone3TattooCollections()
            self.zone4Tab['state'] = DGG.NORMAL
            self.zone4Tab['relief'] = DGG.RAISED
            self.hideZone4TattooCollections()
            self.zone5Tab['state'] = DGG.NORMAL
            self.zone5Tab['relief'] = DGG.RAISED
            self.hideZone5TattooCollections()
            self.zone6Tab['state'] = DGG.NORMAL
            self.zone6Tab['relief'] = DGG.RAISED
            self.hideZone6TattooCollections()
            self.zone7Tab['state'] = DGG.NORMAL
            self.zone7Tab['relief'] = DGG.RAISED
            self.hideZone7TattooCollections()
            self.zone8Tab['state'] = DGG.NORMAL
            self.zone8Tab['relief'] = DGG.RAISED
            self.hideZone8TattooCollections()
            self.reparentCommonGui(self.zone2Frame, self.zone2FrameTitle)
        elif mode == Zone3_Tab:
            self.zone1Tab['state'] = DGG.NORMAL
            self.zone1Tab['relief'] = DGG.RAISED
            self.hideZone1TattooCollections()
            self.zone2Tab['state'] = DGG.NORMAL
            self.zone2Tab['relief'] = DGG.RAISED
            self.hideZone2TattooCollections()
            self.zone3Tab['state'] = DGG.DISABLED
            self.zone3Tab['relief'] = DGG.SUNKEN
            self.showZone3TattooCollections()
            self.zone4Tab['state'] = DGG.NORMAL
            self.zone4Tab['relief'] = DGG.RAISED
            self.hideZone4TattooCollections()
            self.zone5Tab['state'] = DGG.NORMAL
            self.zone5Tab['relief'] = DGG.RAISED
            self.hideZone5TattooCollections()
            self.zone6Tab['state'] = DGG.NORMAL
            self.zone6Tab['relief'] = DGG.RAISED
            self.hideZone6TattooCollections()
            self.zone7Tab['state'] = DGG.NORMAL
            self.zone7Tab['relief'] = DGG.RAISED
            self.hideZone7TattooCollections()
            self.zone8Tab['state'] = DGG.NORMAL
            self.zone8Tab['relief'] = DGG.RAISED
            self.hideZone8TattooCollections()
            self.reparentCommonGui(self.zone3Frame, self.zone3FrameTitle)
        elif mode == Zone4_Tab:
            self.zone1Tab['state'] = DGG.NORMAL
            self.zone1Tab['relief'] = DGG.RAISED
            self.hideZone1TattooCollections()
            self.zone2Tab['state'] = DGG.NORMAL
            self.zone2Tab['relief'] = DGG.RAISED
            self.hideZone2TattooCollections()
            self.zone3Tab['state'] = DGG.NORMAL
            self.zone3Tab['relief'] = DGG.RAISED
            self.hideZone3TattooCollections()
            self.zone4Tab['state'] = DGG.DISABLED
            self.zone4Tab['relief'] = DGG.SUNKEN
            self.showZone4TattooCollections()
            self.zone5Tab['state'] = DGG.NORMAL
            self.zone5Tab['relief'] = DGG.RAISED
            self.hideZone5TattooCollections()
            self.zone6Tab['state'] = DGG.NORMAL
            self.zone6Tab['relief'] = DGG.RAISED
            self.hideZone6TattooCollections()
            self.zone7Tab['state'] = DGG.NORMAL
            self.zone7Tab['relief'] = DGG.RAISED
            self.hideZone7TattooCollections()
            self.zone8Tab['state'] = DGG.NORMAL
            self.zone8Tab['relief'] = DGG.RAISED
            self.hideZone8TattooCollections()
            self.reparentCommonGui(self.zone4Frame, self.zone4FrameTitle)
        elif mode == Zone5_Tab:
            self.zone1Tab['state'] = DGG.NORMAL
            self.zone1Tab['relief'] = DGG.RAISED
            self.hideZone1TattooCollections()
            self.zone2Tab['state'] = DGG.NORMAL
            self.zone2Tab['relief'] = DGG.RAISED
            self.hideZone2TattooCollections()
            self.zone3Tab['state'] = DGG.NORMAL
            self.zone3Tab['relief'] = DGG.RAISED
            self.hideZone3TattooCollections()
            self.zone4Tab['state'] = DGG.NORMAL
            self.zone4Tab['relief'] = DGG.RAISED
            self.hideZone4TattooCollections()
            self.zone5Tab['state'] = DGG.DISABLED
            self.zone5Tab['relief'] = DGG.SUNKEN
            self.showZone5TattooCollections()
            self.zone6Tab['state'] = DGG.NORMAL
            self.zone6Tab['relief'] = DGG.RAISED
            self.hideZone6TattooCollections()
            self.zone7Tab['state'] = DGG.NORMAL
            self.zone7Tab['relief'] = DGG.RAISED
            self.hideZone7TattooCollections()
            self.zone8Tab['state'] = DGG.NORMAL
            self.zone8Tab['relief'] = DGG.RAISED
            self.hideZone8TattooCollections()
            self.reparentCommonGui(self.zone5Frame, self.zone5FrameTitle)
        elif mode == Zone6_Tab:
            self.zone1Tab['state'] = DGG.NORMAL
            self.zone1Tab['relief'] = DGG.RAISED
            self.hideZone1TattooCollections()
            self.zone2Tab['state'] = DGG.NORMAL
            self.zone2Tab['relief'] = DGG.RAISED
            self.hideZone2TattooCollections()
            self.zone3Tab['state'] = DGG.NORMAL
            self.zone3Tab['relief'] = DGG.RAISED
            self.hideZone3TattooCollections()
            self.zone4Tab['state'] = DGG.NORMAL
            self.zone4Tab['relief'] = DGG.RAISED
            self.hideZone4TattooCollections()
            self.zone5Tab['state'] = DGG.NORMAL
            self.zone5Tab['relief'] = DGG.RAISED
            self.hideZone5TattooCollections()
            self.zone6Tab['state'] = DGG.DISABLED
            self.zone6Tab['relief'] = DGG.SUNKEN
            self.showZone6TattooCollections()
            self.zone7Tab['state'] = DGG.NORMAL
            self.zone7Tab['relief'] = DGG.RAISED
            self.hideZone7TattooCollections()
            self.zone8Tab['state'] = DGG.NORMAL
            self.zone8Tab['relief'] = DGG.RAISED
            self.hideZone8TattooCollections()
            self.reparentCommonGui(self.zone6Frame, self.zone6FrameTitle)
        elif mode == Zone7_Tab:
            self.zone1Tab['state'] = DGG.NORMAL
            self.zone1Tab['relief'] = DGG.RAISED
            self.hideZone1TattooCollections()
            self.zone2Tab['state'] = DGG.NORMAL
            self.zone2Tab['relief'] = DGG.RAISED
            self.hideZone2TattooCollections()
            self.zone3Tab['state'] = DGG.NORMAL
            self.zone3Tab['relief'] = DGG.RAISED
            self.hideZone3TattooCollections()
            self.zone4Tab['state'] = DGG.NORMAL
            self.zone4Tab['relief'] = DGG.RAISED
            self.hideZone4TattooCollections()
            self.zone5Tab['state'] = DGG.NORMAL
            self.zone5Tab['relief'] = DGG.RAISED
            self.hideZone5TattooCollections()
            self.zone6Tab['state'] = DGG.NORMAL
            self.zone6Tab['relief'] = DGG.RAISED
            self.hideZone6TattooCollections()
            self.zone7Tab['state'] = DGG.DISABLED
            self.zone7Tab['relief'] = DGG.SUNKEN
            self.showZone7TattooCollections()
            self.zone8Tab['state'] = DGG.NORMAL
            self.zone8Tab['relief'] = DGG.RAISED
            self.hideZone8TattooCollections()
            self.reparentCommonGui(self.zone7Frame, self.zone7FrameTitle)
        elif mode == Zone8_Tab:
            self.zone1Tab['state'] = DGG.NORMAL
            self.zone1Tab['relief'] = DGG.RAISED
            self.hideZone1TattooCollections()
            self.zone2Tab['state'] = DGG.NORMAL
            self.zone2Tab['relief'] = DGG.RAISED
            self.hideZone2TattooCollections()
            self.zone3Tab['state'] = DGG.NORMAL
            self.zone3Tab['relief'] = DGG.RAISED
            self.hideZone3TattooCollections()
            self.zone4Tab['state'] = DGG.NORMAL
            self.zone4Tab['relief'] = DGG.RAISED
            self.hideZone4TattooCollections()
            self.zone5Tab['state'] = DGG.NORMAL
            self.zone5Tab['relief'] = DGG.RAISED
            self.hideZone5TattooCollections()
            self.zone6Tab['state'] = DGG.NORMAL
            self.zone6Tab['relief'] = DGG.RAISED
            self.hideZone6TattooCollections()
            self.zone7Tab['state'] = DGG.NORMAL
            self.zone7Tab['relief'] = DGG.RAISED
            self.hideZone7TattooCollections()
            self.zone8Tab['state'] = DGG.DISABLED
            self.zone8Tab['relief'] = DGG.SUNKEN
            self.showZone8TattooCollections()
            self.reparentCommonGui(self.zone8Frame, self.zone8FrameTitle)

    def setEdit(self, mode):
        print 'editing %s' % mode
        self.guiNextTattooButton.show()
        self.guiLastTattooButton.show()
        self.oXSlider.show()
        self.oYSlider.show()
        self.rotateSlider.show()
        self.scaleSlider.show()
        self.editButtons[mode]['state'] = DGG.DISABLED
        self.editButtons[mode]['relief'] = DGG.SUNKEN
        if self.avatar.pirate.style.gender == 'f':
            self.avatar.tattoos[mode] = PirateFemale.vector_tattoos[mode][:]
        else:
            self.avatar.tattoos[mode] = PirateMale.vector_tattoos[mode][:]
        if mode == Zone1_Tab:
            idx = self.avatar.pirate.style.getTattooChest()[0]
        elif mode == Zone2_Tab:
            idx = self.avatar.pirate.style.getTattooZone2()[0]
        elif mode == Zone3_Tab:
            idx = self.avatar.pirate.style.getTattooZone3()[0]
        elif mode == Zone4_Tab:
            idx = self.avatar.pirate.style.getTattooZone4()[0]
        elif mode == Zone5_Tab:
            idx = self.avatar.pirate.style.getTattooZone5()[0]
        elif mode == Zone6_Tab:
            idx = self.avatar.pirate.style.getTattooZone6()[0]
        elif mode == Zone7_Tab:
            idx = self.avatar.pirate.style.getTattooZone7()[0]
        elif mode == Zone8_Tab:
            idx = self.avatar.pirate.style.getTattooZone8()[0]
        self.avatar.tattoos[mode][0] = idx
        self.vTattoos[mode] = self.avatar.tattoos[mode][:]
        self.restore()

    def reparentCommonGui(self, currTattoo, currTattooFrame):
        self.guiNextTattooButton.reparentTo(currTattoo)
        self.guiLastTattooButton.reparentTo(currTattoo)
        self.map.reparentTo(currTattoo)
        self.oXSlider.reparentTo(currTattooFrame)
        self.oYSlider.reparentTo(currTattooFrame)
        self.scaleSlider.reparentTo(currTattooFrame)
        self.rotateSlider.reparentTo(currTattooFrame)
        self.guiNextTattooButton.hide()
        self.guiLastTattooButton.hide()
        self.oXSlider.hide()
        self.oYSlider.hide()
        self.scaleSlider.hide()
        self.rotateSlider.hide()

    def showZone1TattooCollections(self):
        self.zone1FrameTitle.show()
        self.zone1Frame.show()

    def hideZone1TattooCollections(self):
        self.zone1FrameTitle.hide()
        self.zone1Frame.hide()
        self.editZone1['state'] = DGG.NORMAL
        self.editZone1['relief'] = DGG.RAISED

    def showZone2TattooCollections(self):
        self.zone2FrameTitle.show()
        self.zone2Frame.show()

    def hideZone2TattooCollections(self):
        self.zone2FrameTitle.hide()
        self.zone2Frame.hide()
        self.editZone2['state'] = DGG.NORMAL
        self.editZone2['relief'] = DGG.RAISED

    def showZone3TattooCollections(self):
        self.zone3FrameTitle.show()
        self.zone3Frame.show()

    def hideZone3TattooCollections(self):
        self.zone3FrameTitle.hide()
        self.zone3Frame.hide()
        self.editZone3['state'] = DGG.NORMAL
        self.editZone3['relief'] = DGG.RAISED

    def showZone4TattooCollections(self):
        self.zone4FrameTitle.show()
        self.zone4Frame.show()

    def hideZone4TattooCollections(self):
        self.zone4FrameTitle.hide()
        self.zone4Frame.hide()
        self.editZone4['state'] = DGG.NORMAL
        self.editZone4['relief'] = DGG.RAISED

    def showZone5TattooCollections(self):
        self.zone5FrameTitle.show()
        self.zone5Frame.show()

    def hideZone5TattooCollections(self):
        self.zone5FrameTitle.hide()
        self.zone5Frame.hide()

    def showZone6TattooCollections(self):
        self.zone6FrameTitle.show()
        self.zone6Frame.show()

    def hideZone6TattooCollections(self):
        self.zone6FrameTitle.hide()
        self.zone6Frame.hide()

    def showZone7TattooCollections(self):
        self.zone7FrameTitle.show()
        self.zone7Frame.show()

    def hideZone7TattooCollections(self):
        self.zone7FrameTitle.hide()
        self.zone7Frame.hide()

    def showZone8TattooCollections(self):
        self.zone8FrameTitle.show()
        self.zone8Frame.show()

    def hideZone8TattooCollections(self):
        self.zone8FrameTitle.hide()
        self.zone8Frame.hide()

    def show(self):
        self.zone1Tab.show()
        self.zone2Tab.show()
        self.zone3Tab.show()
        self.zone4Tab.show()
        self.zone5Tab.show()
        self.zone6Tab.show()
        self.zone7Tab.show()
        self.zone8Tab.show()

    def hide(self):
        self.mode = -1
        self.hideZone1TattooCollections()
        self.zone1Tab.hide()
        self.zone1Tab['state'] = DGG.NORMAL
        self.hideZone2TattooCollections()
        self.zone2Tab.hide()
        self.zone2Tab['state'] = DGG.NORMAL
        self.hideZone3TattooCollections()
        self.zone3Tab.hide()
        self.zone3Tab['state'] = DGG.NORMAL
        self.hideZone4TattooCollections()
        self.zone4Tab.hide()
        self.zone4Tab['state'] = DGG.NORMAL
        self.hideZone5TattooCollections()
        self.zone5Tab.hide()
        self.zone5Tab['state'] = DGG.NORMAL
        self.hideZone6TattooCollections()
        self.zone6Tab.hide()
        self.zone6Tab['state'] = DGG.NORMAL
        self.hideZone7TattooCollections()
        self.zone7Tab.hide()
        self.zone7Tab['state'] = DGG.NORMAL
        self.hideZone8TattooCollections()
        self.zone8Tab.hide()
        self.zone8Tab['state'] = DGG.NORMAL
        self.saveDNA()

    def setupButtons(self):
        self.guiNextTattooButton = DirectButton(parent=self.zone1Frame, relief=DGG.RAISED, pos=(0.3, 0.0, -0.5), scale=(2.0,
                                                                                                                        2.0,
                                                                                                                        2.0), command=self.handleNextTattoo, frameSize=(-0.09, 0.09, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                                                                                                0.008), text='>>', text_pos=(0, -0.015), text_scale=0.1)
        self.guiLastTattooButton = DirectButton(parent=self.zone1Frame, relief=DGG.RAISED, pos=(-0.3, 0.0, -0.5), scale=(2.0,
                                                                                                                         2.0,
                                                                                                                         2.0), command=self.handleLastTattoo, frameSize=(-0.09, 0.09, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                                                                                                 0.008), text='<<', text_pos=(0, -0.015), text_scale=0.1)

    def reset(self):
        if self.avatar.pirate.style.gender == 'f':
            for i in range(0, 8):
                self.avatar.tattoos[i] = PirateFemale.vector_tattoos[i][:]

        else:
            for i in range(0, 8):
                self.avatar.tattoos[i] = PirateMale.vector_tattoos[i][:]

            for i in range(0, 8):
                self.vTattoos[i] = self.avatar.tattoos[i][:]

        val = self.avatar.tattoos[ZONE1]
        self.avatar.pirate.setTattooChest(val[TYPE], val[OFFSETX], val[OFFSETY], val[SCALE], val[ROTATE], val[COLOR])
        val = self.avatar.tattoos[ZONE2]
        self.avatar.pirate.setTattooZone2(val[TYPE], val[OFFSETX], val[OFFSETY], val[SCALE], val[ROTATE], val[COLOR])
        val = self.avatar.tattoos[ZONE3]
        self.avatar.pirate.setTattooZone3(val[TYPE], val[OFFSETX], val[OFFSETY], val[SCALE], val[ROTATE], val[COLOR])
        val = self.avatar.tattoos[ZONE4]
        self.avatar.pirate.setTattooZone4(val[TYPE], val[OFFSETX], val[OFFSETY], val[SCALE], val[ROTATE], val[COLOR])
        val = self.avatar.tattoos[ZONE5]
        self.avatar.pirate.setTattooZone5(val[TYPE], val[OFFSETX], val[OFFSETY], val[SCALE], val[ROTATE], val[COLOR])
        val = self.avatar.tattoos[ZONE6]
        self.avatar.pirate.setTattooZone6(val[TYPE], val[OFFSETX], val[OFFSETY], val[SCALE], val[ROTATE], val[COLOR])
        val = self.avatar.tattoos[ZONE7]
        self.avatar.pirate.setTattooZone7(val[TYPE], val[OFFSETX], val[OFFSETY], val[SCALE], val[ROTATE], val[COLOR])
        val = self.avatar.tattoos[ZONE8]
        self.avatar.pirate.setTattooZone8(val[TYPE], val[OFFSETX], val[OFFSETY], val[SCALE], val[ROTATE], val[COLOR])
        self.avatar.handleTattooMapping()
        self.updateCard()
        self.restore()

    def saveDNA(self):
        tattoo = self.avatar.tattoos[ZONE1]
        self.avatar.pirate.setTattooChest(tattoo[TYPE], tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE], tattoo[COLOR])
        tattoo = self.avatar.tattoos[ZONE2]
        self.avatar.pirate.setTattooZone2(tattoo[TYPE], tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE], tattoo[COLOR])
        tattoo = self.avatar.tattoos[ZONE3]
        self.avatar.pirate.setTattooZone3(tattoo[TYPE], tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE], tattoo[COLOR])
        tattoo = self.avatar.tattoos[ZONE4]
        self.avatar.pirate.setTattooZone4(tattoo[TYPE], tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE], tattoo[COLOR])
        tattoo = self.avatar.tattoos[ZONE5]
        self.avatar.pirate.setTattooZone5(tattoo[TYPE], tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE], tattoo[COLOR])
        tattoo = self.avatar.tattoos[ZONE6]
        self.avatar.pirate.setTattooZone6(tattoo[TYPE], tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE], tattoo[COLOR])
        tattoo = self.avatar.tattoos[ZONE7]
        self.avatar.pirate.setTattooZone7(tattoo[TYPE], tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE], tattoo[COLOR])
        tattoo = self.avatar.tattoos[ZONE8]
        self.avatar.pirate.setTattooZone8(tattoo[TYPE], tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE], tattoo[COLOR])

    def loadFromDNA(self):
        if self.avatar.pirate.style.gender == 'f':
            for i in range(0, 8):
                self.avatar.tattoos[i] = PirateFemale.vector_tattoos[i][:]

        else:
            for i in range(0, 8):
                self.avatar.tattoos[i] = PirateMale.vector_tattoos[i][:]

            self.avatar.tattoos[0][0] = self.avatar.pirate.style.getTattooChest()[0]
            self.avatar.tattoos[1][0] = self.avatar.pirate.style.getTattooZone2()[0]
            self.avatar.tattoos[2][0] = self.avatar.pirate.style.getTattooZone3()[0]
            self.avatar.tattoos[3][0] = self.avatar.pirate.style.getTattooZone4()[0]
            self.avatar.tattoos[4][0] = self.avatar.pirate.style.getTattooZone5()[0]
            self.avatar.tattoos[5][0] = self.avatar.pirate.style.getTattooZone6()[0]
            self.avatar.tattoos[6][0] = self.avatar.pirate.style.getTattooZone7()[0]
            self.avatar.tattoos[7][0] = self.avatar.pirate.style.getTattooZone8()[0]
            for i in range(0, 8):
                self.vTattoos[i] = self.avatar.tattoos[i][:]

    def restore(self):
        val = self.vTattoos[self.currTattoo]
        self.oXSlider.node().setValue(val[OFFSETX])
        self.oYSlider.node().setValue(val[OFFSETY])
        self.scaleSlider.node().setValue(val[SCALE])
        self.rotateSlider.node().setValue(val[ROTATE])

    def randomPick(self):
        pass

    def applyBaseTexture(self, textureName='male_tattoomap'):
        t1 = loader.loadTexture('maps/' + textureName + '.jpg')
        self.map.setTexture(t1)

    def handleNextTattoo(self):
        tattoo = self.vTattoos[self.currTattoo]
        tattoo[TYPE] += 1
        if tattoo[TYPE] >= len(TattooGlobals.tattooNames):
            tattoo[TYPE] = 0
        self.avatar.tattoos[self.currTattoo][TYPE] = tattoo[TYPE]
        self.mapTexture(self.currTattoo, tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE])
        self.updateCard()
        self.avatar.updateTattoo(self.currTattoo)
        self.notify.info('Current Tattoo: %s' % TattooGlobals.tattooNames[self.avatar.tattoos[self.currTattoo][TYPE]])

    def handleLastTattoo(self):
        tattoo = self.vTattoos[self.currTattoo]
        tattoo[TYPE] -= 1
        if tattoo[TYPE] < 0:
            tattoo[TYPE] = len(TattooGlobals.tattooNames) - 1
        self.avatar.tattoos[self.currTattoo][TYPE] = tattoo[TYPE]
        self.mapTexture(self.currTattoo, tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE])
        self.updateCard()
        self.avatar.updateTattoo(self.currTattoo)
        self.notify.info('Current Tattoo: %s' % TattooGlobals.tattooNames[self.avatar.tattoos[self.currTattoo][TYPE]])

    def updateCard(self):
        tattooFrame = [
         self.zone1Frame, self.zone2Frame, self.zone3Frame, self.zone4Frame, self.zone5Frame, self.zone6Frame, self.zone7Frame, self.zone8Frame]
        tattoo = self.avatar.tattoos[self.currTattoo]
        tex, scale = TattooGlobals.getTattooImage(tattoo[0])
        t = TransformState.makePosRotateScale2d(Vec2(tattoo[OFFSETX], tattoo[OFFSETY]), tattoo[ROTATE], Vec2(tattoo[SCALE] * scale, tattoo[SCALE]))
        self.map.setTexTransform(self.cStage, t)
        self.map.setTexture(self.cStage, tex)
        tattooFrame[self.currTattoo]['text'] = TattooGlobals.tattooNames[self.avatar.tattoos[self.currTattoo][TYPE]]

    def mapTexture(self, index, offsetx, offsety, scale, rotate):
        S = Vec2(1 / float(scale), 1 / float(scale))
        Iv = Vec2(offsetx, offsety)
        Vm = Vec2(sin(rotate * pi / 180.0), cos(rotate * pi / 180.0))
        Vms = Vec2(Vm[0] * S[0], Vm[1] * S[1])
        Vn = Vec2(Vm[1], -Vm[0])
        Vns = Vec2(Vn[0] * S[0], Vn[1] * S[1])
        F = Vec2(-Vns.dot(Iv) + 0.5, -Vms.dot(Iv) + 0.5)
        self.avatar.tattoos[index][1] = F[0]
        self.avatar.tattoos[index][2] = F[1]
        self.avatar.tattoos[index][3] = S[0]
        self.avatar.tattoos[index][4] = rotate
        self.vTattoos[index] = [self.vTattoos[index][TYPE], offsetx, offsety, scale, rotate, self.vTattoos[index][COLOR]]

    def handleOxSlider(self, pgs):
        if self.currTattoo < 0:
            return
        value = pgs['value']
        tattoo = self.vTattoos[self.currTattoo]
        self.mapTexture(self.currTattoo, value, tattoo[OFFSETY], tattoo[SCALE], tattoo[ROTATE])
        self.updateCard()
        self.avatar.updateTattoo(self.currTattoo)

    def handleOySlider(self, pgs):
        if self.currTattoo < 0:
            return
        value = pgs['value']
        tattoo = self.vTattoos[self.currTattoo]
        self.mapTexture(self.currTattoo, tattoo[OFFSETX], value, tattoo[SCALE], tattoo[ROTATE])
        self.updateCard()
        self.avatar.updateTattoo(self.currTattoo)

    def handleScaleSlider(self, pgs):
        if self.currTattoo < 0:
            return
        value = pgs['value']
        tattoo = self.vTattoos[self.currTattoo]
        self.mapTexture(self.currTattoo, tattoo[OFFSETX], tattoo[OFFSETY], value, tattoo[ROTATE])
        self.updateCard()
        self.avatar.updateTattoo(self.currTattoo)

    def handleRotateSlider(self, pgs):
        if self.currTattoo < 0:
            return
        value = pgs['value']
        tattoo = self.vTattoos[self.currTattoo]
        self.mapTexture(self.currTattoo, tattoo[OFFSETX], tattoo[OFFSETY], tattoo[SCALE], value)
        self.updateCard()
        self.avatar.updateTattoo(self.currTattoo)
