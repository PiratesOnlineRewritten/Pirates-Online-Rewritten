from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals

class TextPrinter(DirectObject.DirectObject):

    def __init__(self):
        DirectObject.DirectObject.__init__(self)
        self.event = None
        self.sfx = None
        self.text = DirectLabel(parent=aspect2d, relief=None, text='', text_align=TextNode.ACenter, text_scale=0.06, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0, 0, -0.9), text_font=PiratesGlobals.getPirateOutlineFont(), sortOrder=80, state=DGG.DISABLED)
        self.text.hide()
        self.fader = None
        self.subtitleParent = render2d.attachNewNode(PGTop('subtitleParent'))
        self.subtitleParent.node().setMouseWatcher(base.mouseWatcherNode)
        return

    def destroy(self):
        self.ignoreAll()
        if self.fader:
            self.fader.finish()
            self.fader = None
        if self.sfx:
            self.sfx.stop()
            self.sfx = None
        self.text.destroy()
        del self.text
        self.subtitleParent.removeNode()
        taskMgr.remove('clearSubtitleTask')
        return

    def clearText(self):
        self.event = None
        self.text['text'] = ''
        self.text['text_fg'] = PiratesGuiGlobals.TextFG2
        self.text.wrtReparentTo(aspect2d)
        self.text.hide()
        if self.sfx:
            self.sfx.stop()
            self.sfx = None
        self.ignore('enter')
        self.ignore('mouse1')
        return

    def showText(self, text, color=None, sfx=None, timeout=False):
        self.text['text'] = text
        self.text.show()
        if self.text.isHidden():
            self.text.wrtReparentTo(self.subtitleParent)
        self.event = None
        if color:
            self.text['text_fg'] = color
        if sfx:
            if self.sfx:
                self.sfx.stop()
            self.sfx = sfx
            base.playSfx(sfx)
        if timeout:
            chatTimeout = 10
            taskMgr.doMethodLater(chatTimeout, self.clearText, 'clearSubtitleTask', extraArgs=[])
        return

    def fadeInText(self, text, color=None, sfx=None):
        self.text['text'] = text
        self.text.show()
        if self.text.isHidden():
            self.text.wrtReparentTo(self.subtitleParent)
        self.event = None
        if sfx:
            if self.sfx:
                self.sfx.stop()
            self.sfx = sfx
            base.playSfx(sfx)
        if self.fader:
            self.fader.finish()
            self.fader = None
        if color:
            self.text['text_fg'] = color
        self.fader = LerpFunctionInterval(self.text.setAlphaScale, fromData=0, toData=1, duration=1.0)
        self.fader.start()
        return

    def fadeOutText(self):
        self.event = None
        if self.sfx:
            self.sfx.stop()
            self.sfx = None
        self.ignore('enter')
        self.ignore('mouse1')
        if self.fader:
            self.fader.finish()
            self.fader = None
        fadeOut = LerpFunctionInterval(self.text.setAlphaScale, fromData=1, toData=0, duration=1.0)

        def restoreColor():
            self.text['text_fg'] = PiratesGuiGlobals.TextFG2
            self.text.wrtReparentTo(aspect2d)

        self.fader = Sequence(fadeOut, Func(self.text.hide), Func(restoreColor))
        self.fader.start()
        return