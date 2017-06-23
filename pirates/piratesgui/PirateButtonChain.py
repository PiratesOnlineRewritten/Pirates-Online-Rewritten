from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import StateData
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPGlobals
from otp.friends.FriendInfo import FriendInfo
from pirates.piratesbase import Freebooter
import GuiButton

class PirateButtonChain():

    def __init__(self, width, parent, fromBottom=False):
        self.fromBottom = fromBottom
        self.width = width
        self.baseFrame = DirectFrame(parent=parent, relief=None)
        self.load()
        return

    def load(self):
        self.buttonCount = 0
        self.buttonIndex = 0
        self.buttonList = []
        gui = loader.loadModel('models/gui/avatar_chooser_rope')
        topPanel = gui.find('**/avatar_c_A_top')
        topPanelOver = gui.find('**/avatar_c_A_top_over')
        self.topButton = (
         topPanel, topPanel, topPanelOver, topPanel)
        middlePanel = gui.find('**/avatar_c_A_middle')
        middlePanelOver = gui.find('**/avatar_c_A_middle_over')
        self.middleButton = (middlePanel, middlePanel, middlePanelOver, middlePanel)
        bottomPanel = gui.find('**/avatar_c_A_bottom')
        bottomPanelOver = gui.find('**/avatar_c_A_bottom_over')
        self.bottomButton = (
         bottomPanel, bottomPanel, bottomPanelOver, bottomPanel)
        self.iScale = 0.25
        self.gScale = (self.width * 0.65, 0.0, 0.28)
        self.tPos = (0.0, -0.015, 0.0)
        self.tBPos = (0.0, 0.025, 0.0)
        self.iPos = (
         0.1, 0, -0.0)
        self.offX = self.width * 0.5
        self.topZ = 0.08
        self.midZ = 0.075
        self.endZ = 0.11
        self.startZ = -0.03

    def show(self):
        self.baseFrame.show()

    def hide(self):
        self.baseFrame.hide()

    def destroy(self):
        self.buttonList = []
        self.baseFrame.destroy()

    def setPos(self, x, y, z):
        self.baseFrame.setPos(x, y, z)

    def premakeButton(self, inText, inCommand, extra=None, textPos=None):
        if not hasattr(self, 'buttonQueue'):
            self.buttonQueue = []
        if not textPos:
            buttonTextPos = self.tPos
        else:
            xLoc = self.tPos[0] + textPos[0]
            yLoc = self.tPos[1] + textPos[1]
            zLoc = self.tPos[2] + textPos[2]
            buttonTextPos = (xLoc, yLoc, zLoc)
        preformButton = DirectButton(parent=self.baseFrame, relief=None, text=inText, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=buttonTextPos, text_align=TextNode.ACenter, text0_fg=PiratesGuiGlobals.TextFG2, text1_fg=PiratesGuiGlobals.TextFG3, text2_fg=PiratesGuiGlobals.TextFG1, text3_fg=PiratesGuiGlobals.TextFG9, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, command=inCommand, geom=self.middleButton, geom_scale=self.gScale, geom0_color=(1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   1), geom1_color=(1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    1), geom2_color=(1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     1), geom3_color=(0.5,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      0.5,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      0.5,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      1))
        self.buttonList.append(preformButton)
        self.buttonQueue.append((inText, inCommand))
        self.buttonIndex += 1
        return preformButton

    def makeButtons(self):
        if self.fromBottom:
            self.startZ += self.midZ * len(self.buttonQueue)
        for index in range(0, len(self.buttonQueue)):
            isLast = False
            if index == len(self.buttonQueue) - 1:
                isLast = True
            self.createButtons(self.buttonQueue[index][0], self.buttonQueue[index][1], isLast)

        self.buttonQueue = []

    def getButton(self, index):
        return self.buttonList[index]

    def createButtons(self, inText, inCommand, inLast=False):
        formingButton = self.buttonList[self.buttonCount]
        if self.buttonCount == 0:
            formingButton.setPos(self.offX, 0, self.startZ)
            formingButton['geom'] = self.topButton
        elif inLast and not self.fromBottom:
            formingButton.setPos(self.offX, 0, self.startZ - (self.topZ + self.midZ * (self.buttonCount - 2) + self.endZ))
            formingButton['geom'] = self.bottomButton
            formingButton['text_pos'] = self.tBPos
        else:
            formingButton.setPos(self.offX, 0, self.startZ - (self.topZ + self.midZ * (self.buttonCount - 1)))
            formingButton['geom'] = self.middleButton
        formingButton.resetFrameSize()
        self.buttonCount += 1

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.topZ + self.midZ * (self.buttonCount - 2) + self.endZ