from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesbase import PLocalizer

class Tab(BorderFrame):

    def __init__(self, tabBar, name, **kw):
        optiondefs = (
         (
          'state', DGG.DISABLED, None), ('command', None, self.setCommand), ('extraArgs', [], self.setExtraArgs), ('name', name, None), ('mouseEntered', None, None), ('mouseLeft', None, None), ('selected', False, self.setSelected), ('textMayChange', 1, None))
        self.defineoptions(kw, optiondefs)
        BorderFrame.__init__(self, parent=NodePath(), **kw)
        self.initialiseoptions(Tab)
        self.setName(str(name))
        self.tabBar = tabBar
        self.invisibleButton = DirectButton(parent=self, relief=1, frameColor=(1.0,
                                                                               0.0,
                                                                               1.0,
                                                                               0), frameSize=self.getInnerFrameSize(), rolloverSound=None, command=self['command'], extraArgs=self['extraArgs'], textMayChange=1)
        self.invisibleButton.bind(DGG.ENTER, self.mouseEntered)
        self.invisibleButton.bind(DGG.EXIT, self.mouseLeft)
        return

    def destroy(self):
        self.tabBar = None
        self.invisibleButton = None
        BorderFrame.destroy(self)
        return

    def setTabBar(self, tabBar):
        self.tabBar = tabBar

    def setCommand(self):
        if hasattr(self, 'invisibleButton'):

            def command(*args, **kwargs):
                if self.tabBar:
                    self.tabBar.selectTab(self['name'])
                if self['command']:
                    self['command'](*args, **kwargs)

            self.invisibleButton['command'] = command

    def setExtraArgs(self):
        if hasattr(self, 'invisibleButton'):
            self.invisibleButton['extraArgs'] = self['extraArgs']

    def __resetButton(self):
        if hasattr(self, 'invisibleButton'):
            self.invisibleButton['frameSize'] = self.getInnerFrameSize()

    def setPos(self, *args, **kwargs):
        BorderFrame.setPos(self, *args, **kwargs)
        self.__resetButton()

    def setScale(self, *args, **kwargs):
        BorderFrame.setScale(self, *args, **kwargs)
        self.__resetButton()

    def setFrameSize(self, *args, **kwargs):
        BorderFrame.setFrameSize(self, *args, **kwargs)
        self.__resetButton()

    def mouseEntered(self, pt):
        if self['mouseEntered']:
            self['mouseEntered']()

    def mouseLeft(self, pt):
        if self['mouseLeft']:
            self['mouseLeft']()

    def setSelected(self):
        if self['selected']:
            self.mouseEntered(None)
        else:
            self.mouseLeft(None)
        return


class LeftTab(Tab):

    def __init__(self, tabBar, name, **kw):
        Tab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(LeftTab)
        self.guiComponents['right'].setColor(0, 0, 0, 1)
        self.guiComponents['right'].setTransparency(0, 1)
        self.guiComponents['background'].setColor(0, 0, 0, 1)
        self.guiComponents['background'].setTransparency(0, 1)
        self.guiComponents['background'].setTextureOff(1)
        self.resetDecorations()


class TopTab(Tab):

    def __init__(self, tabBar, name, **kw):
        Tab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(TopTab)
        self.guiComponents['bottom'].setColor(0, 0, 0, 1)
        self.guiComponents['bottom'].setTransparency(0, 1)
        self.guiComponents['background'].setColor(0, 0, 0, 1)
        self.guiComponents['background'].setTransparency(0, 1)
        self.resetDecorations()


class TabBar(DirectFrame):

    def __init__(self, backParent, frontParent, parent=None, offset=0, **kw):
        optiondefs = (('relief', None, None), ('state', DGG.DISABLED, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(TabBar)
        self.bParent = backParent
        self.fParent = frontParent
        self.offset = offset
        self.tabs = {}
        self.tabOrder = []
        self.activeIndex = 0
        self.setOffset(self.offset)
        return

    def setOffset(self, offset):
        self.offset = offset
        self.refreshTabs()

    def destroy(self):
        for tab in self.tabs.itervalues():
            tab.destroy()

        self.bParent = None
        self.fParent = None
        return

    def addTab(self, name, pos=-1, **kw):
        self.removeTab(name, False)
        if pos < 0:
            pos = len(self.tabOrder)
        self.tabs[name] = self.makeTab(name, **kw)
        self.tabs[name].setTabBar(self)
        self.tabOrder.insert(pos, name)
        self.refreshTabs()
        return self.tabs[name]

    def refreshTabs(self):
        pass

    def makeTab(self, name, **kw):
        pass

    def selectTab(self, name):
        try:
            self.activeIndex = self.tabOrder.index(name)
            self.refreshTabs()
            for tab in self.tabs.itervalues():
                tab['selected'] = False

            activeName = self.tabOrder[self.activeIndex]
            activeTab = self.tabs.get(activeName)
            if activeTab:
                activeTab['selected'] = True
        except ValueError:
            pass
        except IndexError:
            pass

    def getTab(self, name):
        return self.tabs.get(name)

    def getOrder(self):
        return self.tabOrder

    def removeTab(self, name, refresh=True):
        needRefresh = False
        if name in self.tabOrder:
            self.tabOrder.remove(name)
            needRefresh = True
        tab = self.tabs.pop(name, None)
        if tab:
            tab.destroy()
            needRefresh = True
        if refresh and needRefresh:
            self.refreshTabs()
        return

    def stash(self):
        DirectFrame.stash(self)
        for tab in self.tabs.itervalues():
            tab.stash()

    def unstash(self):
        DirectFrame.unstash(self)
        for tab in self.tabs.itervalues():
            tab.unstash()