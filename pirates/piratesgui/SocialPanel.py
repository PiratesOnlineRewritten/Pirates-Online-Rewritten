from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import DialogButton
from pirates.piratesgui import PiratesInfo
from pirates.piratesbase import PLocalizer

class SocialPanel(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, parent=NodePath(), relief=None, state=DGG.NORMAL, frameSize=(0.0, PiratesGuiGlobals.SocialPageWidth, 0.0, PiratesGuiGlobals.SocialPageHeight - PiratesGuiGlobals.GridCell))
        self.initialiseoptions(SocialPanel)
        self.setBin('gui-fixed', -1)
        guic = loader.loadModel('models/gui/chat_frame_c')
        cm = CardMaker('bg')
        cm.setColor(0.0, 0, 0, 0.7)
        cm.setFrame(-2.5, 1.95, -1.45, 4.9)
        self.bg = self.attachNewNode(cm.generate())
        self.bg.setColor(0, 0, 0, 0.7)
        self.bg.setTransparency(1)
        self.bg.flattenStrong()
        guic.find('**/pPlane8').copyTo(self.bg)
        guic.find('**/pPlane9').copyTo(self.bg)
        guic.find('**/pPlane10').copyTo(self.bg)
        guic.find('**/pPlane26').copyTo(self.bg)
        guic.find('**/pPlane27').copyTo(self.bg)
        self.bg.setScale(0.145, 1.0, 0.14)
        self.bg.setPos(0.27, 0.0, 0.21)
        buttonGeom = NodePath('Close')
        guic.find('**/pPlane30').copyTo(buttonGeom)
        guic.find('**/pPlane31').copyTo(buttonGeom)
        guic.find('**/pPlane32').copyTo(buttonGeom)
        buttonGeom.flattenStrong()
        self.tCloseButton = DirectButton(parent=self, relief=None, frameColor=(1, 1,
                                                                               1,
                                                                               1), pad=(-0.02, -0.02), borderWidth=(0,
                                                                                                                    0), geom=buttonGeom, pos=(0.145, 0, -0.095), scale=0.2, rolloverSound=None, command=self.hide)
        self.currPageIndex = None
        self.currPageTabIndex = None
        self.pages = []
        self.pageTabs = []
        self.pageTabFrame = DirectFrame(parent=self, relief=None, pos=(PiratesGuiGlobals.BorderWidth[0], 0, PiratesGuiGlobals.BorderWidth[0]))
        self.accept('press-wheel_up-%s' % self.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.guiId, self.mouseWheelDown)
        return

    def mouseWheelUp(self, task=None):
        messenger.send('socailPanelWheelUp')

    def mouseWheelDown(self, task=None):
        messenger.send('socailPanelWheelDown')

    def destroy(self):
        self.pages = []
        self.pageTabs = []
        self.ignoreAll()
        DirectFrame.destroy(self)

    def addPage(self, page):
        page.reparentTo(self)
        page.hide()
        self.pages.append(page)
        self.addPageTab(page)

    def addPageTab(self, page):

        def goToPage():
            messenger.send('wakeup')
            self.setPage(page)

        tabIndex = len(self.pageTabs)
        xOffset = -0.01 + tabIndex * 0.158
        charGui = loader.loadModel('models/gui/toplevel_gui')
        buttonImage = (charGui.find('**/generic_button'), charGui.find('**/generic_button_down'), charGui.find('**/generic_button_over'), charGui.find('**/generic_button_disabled'))
        pageTab = DirectButton(parent=self.pageTabFrame, relief=None, image=buttonImage, image_scale=(0.158,
                                                                                                      1.0,
                                                                                                      0.18), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=page.title, text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(xOffset, 0, 0.035), command=goToPage)
        self.pageTabs.append(pageTab)
        charGui.removeNode()
        return

    def removePage(self, page):
        page.detachNode()
        self.pages.remove(page)

    def setPage(self, page):
        if self.currPageIndex is not None:
            self.pages[self.currPageIndex].hide()
        self.currPageIndex = self.pages.index(page)
        self.setPageTabIndex(self.currPageIndex)
        page.show()
        return

    def setPageTabIndex(self, pageTabIndex):
        for pageButton in self.pageTabs:
            pageButton['image_color'] = Vec4(0.63, 0.63, 0.63, 1)
            pageButton['image1_color'] = Vec4(0.4, 0.4, 0.4, 1)
            pageButton['image2_color'] = Vec4(0.9, 0.9, 0.9, 1)
            pageButton['image3_color'] = Vec4(0.4, 0.4, 0.4, 1)

        self.currPageTabIndex = pageTabIndex
        self.pageTabs[self.currPageTabIndex]['image_color'] = Vec4(0.82, 0.82, 0.82, 1)
        self.pageTabs[self.currPageTabIndex]['image1_color'] = Vec4(0.4, 0.4, 0.4, 1)
        self.pageTabs[self.currPageTabIndex]['image2_color'] = Vec4(0.9, 0.9, 0.9, 1)
        self.pageTabs[self.currPageTabIndex]['image3_color'] = Vec4(0.4, 0.4, 0.4, 1)

    def getCurPage(self):
        return self.pages[self.currPageIndex]

    def __pageChange(self, offset):
        if self.currPageIndex is not None:
            self.pages[self.currPageIndex].hide()
        self.currPageIndex = self.currPageIndex + offset
        self.currPageIndex = max(self.currPageIndex, 0)
        self.currPageIndex = min(self.currPageIndex, len(self.pages) - 1)
        self.setPageTabIndex(self.currPageIndex)
        page = self.pages[self.currPageIndex]
        page.show()
        return

    def updateAll(self):
        for page in self.pages:
            page.membersList.updateAll()

    def updateAvOnAll(self, avId):
        for page in self.pages:
            page.membersList.updateAv(avId)

    def b_help(self):
        self.confirmBox = PiratesInfo.PiratesInfo(PLocalizer.SocialPanelHelpTitle, PLocalizer.SocialPanelHelpContents)

    def show(self):
        if localAvatar.getAllowSocialPanel():
            DirectFrame.show(self)
            self.pages[self.currPageIndex].hide()
            self.pages[self.currPageIndex].show()