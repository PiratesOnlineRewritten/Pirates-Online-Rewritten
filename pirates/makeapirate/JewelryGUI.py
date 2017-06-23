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
import JewelryGlobals
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
jewelry_keys = [
 'LEar', 'REar', 'LBrow', 'RBrow', 'Nose', 'Mouth', 'LHand', 'RHand']

class JewelryGUI(DirectFrame, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('JewelryGUI')

    def __init__(self, main=None):
        self.main = main
        self.parent = main.bookModel
        self.avatar = main.avatar
        self.mode = None
        self.shownMale = None
        self.shownFemale = None
        self.zoneTabs = []
        self.zoneFrames = []
        self.load()
        return

    def enter(self):
        self.notify.debug('enter')
        self.show()
        if self.mode == None:
            self.load()
            self.mode = -1
        return

    def exit(self):
        self.hide()

    def save(self):
        if self.mode == -1:
            pass
        self.saveDNA()

    def load(self):
        self.loadTabs()
        self.setupButtons()

    def assignAvatar(self, avatar):
        self.avatar = avatar

    def loadTabs(self):
        self.zone1Tab = DirectButton(parent=self.parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='L Ear', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone1_Tab], pos=(-0.97, 0, 1.02))
        self.zone1Tab.hide()
        self.zoneTabs.append(self.zone1Tab)
        self.zone2Tab = DirectButton(parent=self.parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='R Ear', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone2_Tab], pos=(-0.72, 0, 1.02))
        self.zone2Tab.hide()
        self.zoneTabs.append(self.zone2Tab)
        self.zone3Tab = DirectButton(parent=self.parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='L Brow', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone3_Tab], pos=(-0.47, 0, 1.02))
        self.zone3Tab.hide()
        self.zoneTabs.append(self.zone3Tab)
        self.zone4Tab = DirectButton(parent=self.parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='R Brow', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone4_Tab], pos=(-0.22, 0, 1.02))
        self.zone4Tab.hide()
        self.zoneTabs.append(self.zone4Tab)
        self.zone5Tab = DirectButton(parent=self.parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='Nose', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone5_Tab], pos=(0.03,
                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                          1.02))
        self.zone5Tab.hide()
        self.zoneTabs.append(self.zone5Tab)
        self.zone6Tab = DirectButton(parent=self.parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='Mouth', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone6_Tab], pos=(0.28,
                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                           1.02))
        self.zone6Tab.hide()
        self.zoneTabs.append(self.zone6Tab)
        self.zone7Tab = DirectButton(parent=self.parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='L Hand', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone7_Tab], pos=(0.53,
                                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                                            1.02))
        self.zone7Tab.hide()
        self.zoneTabs.append(self.zone7Tab)
        self.zone8Tab = DirectButton(parent=self.parent, relief=DGG.RAISED, frameSize=(-0.13, 0.13, -0.04, 0.04), borderWidth=(0.008,
                                                                                                                               0.008), text='R Hand', text_scale=0.07, text_align=TextNode.ACenter, text_pos=(0, -0.015), command=self.setMode, extraArgs=[Zone8_Tab], pos=(0.78,
                                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                                            1.02))
        self.zone8Tab.hide()
        self.zoneTabs.append(self.zone8Tab)

    def unload(self):
        del self.main
        del self.parent
        del self.avatar

    def setMode(self, mode, updateAnyways=0):
        messenger.send('wakeup')
        if not updateAnyways:
            if self.mode == mode:
                return
            else:
                self.mode = mode
        self.currTattoo = mode
        for i in range(0, len(self.zoneTabs)):
            self.zoneTabs[i]['state'] = DGG.NORMAL
            self.zoneTabs[i]['relief'] = DGG.RAISED
            self.zoneFrames[i].hide()

        self.zoneTabs[mode]['state'] = DGG.DISABLED
        self.zoneTabs[mode]['relief'] = DGG.SUNKEN
        self.zoneFrames[mode].show()
        if mode < Zone7_Tab:
            self.main.pgsZoom['value'] = 1.0
        else:
            self.main.pgsZoom['value'] = 0.5
        if mode in [Zone1_Tab, Zone7_Tab]:
            self.main.pgsRotate['value'] = -0.3
        elif mode in [Zone2_Tab, Zone8_Tab]:
            self.main.pgsRotate['value'] = 0.3
        else:
            self.main.pgsRotate['value'] = 0.0
        self.reparentCommonGui(mode)

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
        for i in range(0, len(self.zoneTabs)):
            self.zoneTabs[i]['state'] = DGG.NORMAL
            self.zoneTabs[i].hide()
            self.zoneFrames[i].hide()

        self.saveDNA()

    def setupButtons(self):
        self.zone1Frame = DirectFrame(parent=self.parent, relief=DGG.FLAT, pos=(0.0,
                                                                                0,
                                                                                0.7))
        self.zone1Frame.hide()
        self.zoneFrames.append(self.zone1Frame)
        self.jewelry1Picker = CharGuiPicker(self.main, parent=self.zone1Frame, text=PLocalizer.ShapeJewelryLEarFrameTitle, nextCommand=Functor(self.handleNextJewelry, jewelry_keys[Zone1_Tab]), backCommand=Functor(self.handleLastJewelry, jewelry_keys[Zone1_Tab]))
        self.jewelry1Picker.setPos(0, 0, -0.5)
        self.zone2Frame = DirectFrame(parent=self.parent, relief=DGG.FLAT, pos=(0.0,
                                                                                0,
                                                                                0.7))
        self.zone2Frame.hide()
        self.zoneFrames.append(self.zone2Frame)
        self.jewelry2Picker = CharGuiPicker(self.main, parent=self.zone2Frame, text=PLocalizer.ShapeJewelryREarFrameTitle, nextCommand=Functor(self.handleNextJewelry, jewelry_keys[Zone2_Tab]), backCommand=Functor(self.handleLastJewelry, jewelry_keys[Zone2_Tab]))
        self.jewelry2Picker.setPos(0, 0, -0.5)
        self.zone3Frame = DirectFrame(parent=self.parent, relief=DGG.FLAT, pos=(0.0,
                                                                                0,
                                                                                0.7))
        self.zone3Frame.hide()
        self.zoneFrames.append(self.zone3Frame)
        self.jewelry3Picker = CharGuiPicker(self.main, parent=self.zone3Frame, text=PLocalizer.ShapeJewelryLBrowFrameTitle, nextCommand=Functor(self.handleNextJewelry, jewelry_keys[Zone3_Tab]), backCommand=Functor(self.handleLastJewelry, jewelry_keys[Zone3_Tab]))
        self.jewelry3Picker.setPos(0, 0, -0.5)
        self.zone4Frame = DirectFrame(parent=self.parent, relief=DGG.FLAT, pos=(0.0,
                                                                                0,
                                                                                0.7))
        self.zone4Frame.hide()
        self.zoneFrames.append(self.zone4Frame)
        self.jewelry4Picker = CharGuiPicker(self.main, parent=self.zone4Frame, text=PLocalizer.ShapeJewelryRBrowFrameTitle, nextCommand=Functor(self.handleNextJewelry, jewelry_keys[Zone4_Tab]), backCommand=Functor(self.handleLastJewelry, jewelry_keys[Zone4_Tab]))
        self.jewelry4Picker.setPos(0, 0, -0.5)
        self.zone5Frame = DirectFrame(parent=self.parent, relief=DGG.FLAT, pos=(0.0,
                                                                                0,
                                                                                0.7))
        self.zone5Frame.hide()
        self.zoneFrames.append(self.zone5Frame)
        self.jewelry5Picker = CharGuiPicker(self.main, parent=self.zone5Frame, text=PLocalizer.ShapeJewelryNoseFrameTitle, nextCommand=Functor(self.handleNextJewelry, jewelry_keys[Zone5_Tab]), backCommand=Functor(self.handleLastJewelry, jewelry_keys[Zone5_Tab]))
        self.jewelry5Picker.setPos(0, 0, -0.5)
        self.zone6Frame = DirectFrame(parent=self.parent, relief=DGG.FLAT, pos=(0.0,
                                                                                0,
                                                                                0.7))
        self.zone6Frame.hide()
        self.zoneFrames.append(self.zone6Frame)
        self.jewelry6Picker = CharGuiPicker(self.main, parent=self.zone6Frame, text=PLocalizer.ShapeJewelryMouthFrameTitle, nextCommand=Functor(self.handleNextJewelry, jewelry_keys[Zone6_Tab]), backCommand=Functor(self.handleLastJewelry, jewelry_keys[Zone6_Tab]))
        self.jewelry6Picker.setPos(0, 0, -0.5)
        self.zone7Frame = DirectFrame(parent=self.parent, relief=DGG.FLAT, pos=(0.0,
                                                                                0,
                                                                                0.7))
        self.zone7Frame.hide()
        self.zoneFrames.append(self.zone7Frame)
        self.jewelry7Picker = CharGuiPicker(self.main, parent=self.zone7Frame, text=PLocalizer.ShapeJewelryLHandFrameTitle, nextCommand=Functor(self.handleNextJewelry, jewelry_keys[Zone7_Tab]), backCommand=Functor(self.handleLastJewelry, jewelry_keys[Zone7_Tab]))
        self.jewelry7Picker.setPos(0, 0, -0.5)
        self.zone8Frame = DirectFrame(parent=self.parent, relief=DGG.FLAT, pos=(0.0,
                                                                                0,
                                                                                0.7))
        self.zone8Frame.hide()
        self.zoneFrames.append(self.zone8Frame)
        self.jewelry8Picker = CharGuiPicker(self.main, parent=self.zone8Frame, text=PLocalizer.ShapeJewelryRHandFrameTitle, nextCommand=Functor(self.handleNextJewelry, jewelry_keys[Zone8_Tab]), backCommand=Functor(self.handleLastJewelry, jewelry_keys[Zone8_Tab]))
        self.jewelry8Picker.setPos(0, 0, -0.5)
        self.loadColorGUI()

    def loadColorGUI(self):
        self.primaryColorFrame = DirectFrame(parent=self.zone1Frame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_pos=(0, 0, -0.3), image_scale=(2.43,
                                                                                                                                                                           1.6,
                                                                                                                                                                           1.6), text='Pirmary Color', text_fg=(1,
                                                                                                                                                                                                                1,
                                                                                                                                                                                                                1,
                                                                                                                                                                                                                1), text_scale=0.18, text_pos=(0, -0.05), pos=(0, 0, -0.8), scale=0.7)
        self.primaryColorButtons = []
        xOffset = -0.8
        yOffset = -0.3
        for i in range(0, len(HumanDNA.jewelryColors)):
            if i and i % 9 == 0:
                xOffset = -0.5
                yOffset -= 0.3
            jewelryColor = HumanDNA.jewelryColors[i]
            if jewelryColor is None:
                jewelryColor = VBase4(0, 0, 0, 1)
            self.primaryColorButtons.append(DirectButton(parent=self.primaryColorFrame, relief=DGG.RAISED, pos=(xOffset, 0, yOffset), frameSize=(-0.1, 0.1, -0.1, 0.1), borderWidth=(0.008,
                                                                                                                                                                                     0.008), frameColor=jewelryColor, command=self.handleSetPrimaryColor, extraArgs=[i]))
            xOffset += 0.2

        self.secondaryColorFrame = DirectFrame(parent=self.zone1Frame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_pos=(0, 0, -0.3), image_scale=(2.43,
                                                                                                                                                                             1.6,
                                                                                                                                                                             1.6), text='Secondary Color', text_fg=(1,
                                                                                                                                                                                                                    1,
                                                                                                                                                                                                                    1,
                                                                                                                                                                                                                    1), text_scale=0.18, text_pos=(0, -0.05), pos=(0,
                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                   -1.4), scale=0.7)
        self.secondaryColorButtons = []
        xOffset = -0.8
        yOffset = -0.3
        for i in range(0, len(HumanDNA.jewelryColors)):
            if i and i % 9 == 0:
                xOffset = -0.5
                yOffset -= 0.3
            jewelryColor = HumanDNA.jewelryColors[i]
            if jewelryColor is None:
                jewelryColor = VBase4(0, 0, 0, 1)
            self.secondaryColorButtons.append(DirectButton(parent=self.secondaryColorFrame, relief=DGG.RAISED, pos=(xOffset, 0, yOffset), frameSize=(-0.1, 0.1, -0.1, 0.1), borderWidth=(0.008,
                                                                                                                                                                                         0.008), frameColor=jewelryColor, command=self.handleSetSecondaryColor, extraArgs=[i]))
            xOffset += 0.2

        return

    def reset(self):
        self.avatar.hideAllJewelry()
        self.saveDNA()

    def saveDNA(self):
        self.avatar.pirate.setJewelryZone1(self.avatar.currentJewelry['LEar'][0], self.avatar.currentJewelry['LEar'][1], self.avatar.currentJewelry['LEar'][2])
        self.avatar.pirate.setJewelryZone2(self.avatar.currentJewelry['REar'][0], self.avatar.currentJewelry['REar'][1], self.avatar.currentJewelry['REar'][2])
        self.avatar.pirate.setJewelryZone3(self.avatar.currentJewelry['LBrow'][0], self.avatar.currentJewelry['LBrow'][1], self.avatar.currentJewelry['LBrow'][2])
        self.avatar.pirate.setJewelryZone4(self.avatar.currentJewelry['RBrow'][0], self.avatar.currentJewelry['RBrow'][1], self.avatar.currentJewelry['RBrow'][2])
        self.avatar.pirate.setJewelryZone5(self.avatar.currentJewelry['Nose'][0], self.avatar.currentJewelry['Nose'][1], self.avatar.currentJewelry['Nose'][2])
        self.avatar.pirate.setJewelryZone6(self.avatar.currentJewelry['Mouth'][0], self.avatar.currentJewelry['Mouth'][1], self.avatar.currentJewelry['Mouth'][2])
        self.avatar.pirate.setJewelryZone7(self.avatar.currentJewelry['LHand'][0], self.avatar.currentJewelry['LHand'][1], self.avatar.currentJewelry['LHand'][2])
        self.avatar.pirate.setJewelryZone8(self.avatar.currentJewelry['RHand'][0], self.avatar.currentJewelry['RHand'][1], self.avatar.currentJewelry['RHand'][2])

    def randomPick(self):
        pass

    def reparentCommonGui(self, mode):
        self.primaryColorFrame.reparentTo(self.zoneFrames[mode])
        self.secondaryColorFrame.reparentTo(self.zoneFrames[mode])
        for i in range(0, len(self.primaryColorButtons)):
            self.primaryColorButtons[i]['relief'] = DGG.RAISED

        for i in range(0, len(self.secondaryColorButtons)):
            self.secondaryColorButtons[i]['relief'] = DGG.RAISED

    def handleNextJewelry(self, key):
        self.avatar.handleJewelryOptions(key, True)
        print self.avatar.currentJewelry

    def handleLastJewelry(self, key):
        self.avatar.handleJewelryOptions(key, False)

    def handleSetPrimaryColor(self, colorIdx):
        for i in range(0, len(self.primaryColorButtons)):
            self.primaryColorButtons[i]['relief'] = DGG.RAISED

        self.primaryColorButtons[colorIdx]['relief'] = DGG.SUNKEN
        primaryColor = HumanDNA.jewelryColors[colorIdx]
        if primaryColor:
            key = jewelry_keys[self.mode]
            idx = self.avatar.currentJewelry[key][0]
            self.avatar.jewelrySets[key][idx][0].setColor(primaryColor)
            self.avatar.currentJewelry[key][1] = colorIdx

    def handleSetSecondaryColor(self, colorIdx):
        for i in range(0, len(self.secondaryColorButtons)):
            self.secondaryColorButtons[i]['relief'] = DGG.RAISED

        self.secondaryColorButtons[colorIdx]['relief'] = DGG.SUNKEN
        secondaryColor = HumanDNA.jewelryColors[colorIdx]
        if secondaryColor:
            key = jewelry_keys[self.mode]
            idx = self.avatar.currentJewelry[key][0]
            self.avatar.jewelrySets[key][idx][1].setColor(secondaryColor)
            self.avatar.currentJewelry[key][2] = colorIdx