from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiTray
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui import ReputationMeterDial
from pirates.piratesgui import StatusTray
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import VitaeMeter

class GameGui(DirectButton):

    def __init__(self, parent, **kw):
        gui = loader.loadModel('models/gui/toplevel_gui')
        DirectButton.__init__(self, parent=NodePath(), **kw)
        self.initialiseoptions(GameGui)
        self.repMeter = ReputationMeterDial.ReputationMeterDial(InventoryType.OverallRep, width=0.56)
        self.repMeter.reparentTo(self)
        self.repMeter.setPos(0.425, 0, 0.19)
        self.keyFrame = gui.find('**/main_gui_game_gui_base').copyTo(self)
        self.keyFrame.setPos(0.75, 0, 0.185)
        self.keyFrame.setScale(0.6)
        self.repMeter.categoryLabel.wrtReparentTo(self)
        self.repMeter.levelCapScroll.wrtReparentTo(self)
        self.repMeter.levelCapIcon.wrtReparentTo(self)
        self.statusTray = StatusTray.StatusTray(parent=self, state=DGG.DISABLED)
        self.statusTray.flattenStrong()
        self.statusTray.statusEffectsPanel.setPos(0.34, 0, 0.14)
        self.statusTray.statusEffectsPanel.setScale(0.8)
        self.statusTray.setPos(0.36, 0, 0.17)
        self.statusTray.hpLabel.show()
        self.statusTray.hpMeter.component('text0').show()
        self.statusTray.voodooLabel.show()
        self.statusTray.voodooMeter.component('text0').show()
        self.voodooModMeter = None
        self.hpModMeter = None
        self.repMeter.levelLabel.wrtReparentTo(self)
        self.repMeter.valueLabel.wrtReparentTo(self)
        self.vitaeMeter = VitaeMeter.VitaeMeter(parent=self.statusTray, state=DGG.DISABLED, relief=None, pos=(0.85,
                                                                                                              0,
                                                                                                              0.1), scale=0.82)
        self.clamps = self.attachNewNode('clamps')
        clamp = gui.find('**/groggy_clamp').copyTo(NodePath(''))
        clamp.reparentTo(self.clamps, sort=2)
        clamp.setPos(0.96, 0, 0.135)
        clamp.setScale(0.8)
        clamp = gui.find('**/*clamp').copyTo(NodePath(''))
        clamp.reparentTo(self.clamps, sort=2)
        clamp.setPos(0.96, 0, 0.235)
        clamp.setScale(0.8)
        self.clamps.hide()
        meterGui = loader.loadModel('models/textureCards/dialmeter')
        self.glow = OnscreenImage(parent=self, image=meterGui.find('**/dialmeter_full'), scale=0.58, color=(0.996,
                                                                                                            0.957,
                                                                                                            0.51,
                                                                                                            0.67), pos=(0.425,
                                                                                                                        0,
                                                                                                                        0.19))
        self.glow2 = OnscreenImage(parent=self, image=meterGui.find('**/dialmeter_full'), scale=0.45, color=(0.996,
                                                                                                             0.957,
                                                                                                             0.51,
                                                                                                             0.67), pos=(0.425,
                                                                                                                         0,
                                                                                                                         0.19))
        self.glow.hide()
        self.glow.setBin('gui-fixed', -2)
        self.glow2.hide()
        self.glow2.setBin('gui-fixed', -2)
        self.setBin('gui-fixed', -1)
        meterGui.removeNode()
        self.bind(DGG.ENTER, self.turnHighlightOn)
        self.bind(DGG.EXIT, self.turnHighlightOff)
        self.createHealthAlert()
        self.haTask = None
        self.reparentTo(parent or aspect2d)
        return

    def createHealthAlert(self):
        if hasattr(self, 'healthAlertIval'):
            self.healthAlertIval.finish()
            del self.healthAlertIval
        self.healthAlertIval = Sequence(LerpColorScaleInterval(self.keyFrame, 0.25, Vec4(1.0, 0.3, 0.3, 1.0), blendType='easeIn'), LerpColorScaleInterval(self.keyFrame, 0.25, Vec4(1.0, 1.0, 1.0, 1.0), blendType='easeOut'), Func(self.keyFrame.clearColorScale))
        self.healthAlertRate = 1.0

    def updateHealthAlert(self, task):
        if not hasattr(base, 'localAvatar') or not base.localAvatar or not localAvatar.isGenerated():
            return task.done
        hpFraction = float(base.localAvatar.hp) / float(base.localAvatar.maxHp)
        if hpFraction > 0.4:
            self.stopHealthAlert()
            return task.done
        self.healthAlertRate = 1.0 - hpFraction * 2.0
        if not self.healthAlertIval.isPlaying():
            self.healthAlertIval.start(playRate=self.healthAlertRate)
        return task.cont

    def startHealthAlert(self):
        if not self.haTask:
            self.haTask = taskMgr.add(self.updateHealthAlert, 'updateHealthAlert')

    def stopHealthAlert(self):
        if self.haTask:
            taskMgr.remove(self.haTask)
            self.haTask = None
        return

    def destroy(self):
        self.stopHealthAlert()
        if hasattr(self, 'moveUpIval'):
            self.moveUpIval.finish()
            del self.moveUpIval
        if hasattr(self, 'scaleDown'):
            self.scaleDown.finish()
            del self.scaleDown
        if hasattr(self, 'fadeOut'):
            self.fadeOut.finish()
            del self.fadeOut
        if hasattr(self, 'track'):
            self.track.finish()
            del self.track
        if hasattr(self, 'healthAlertIval'):
            self.healthAlertIval.finish()
            del self.healthAlertIval
        if self.hpModMeter:
            self.hpModMeter.destroy()
            self.hpModMeter = None
        if self.voodooModMeter:
            self.voodooModMeter.destroy()
            self.voodooModMeter = None
        self.clamps = None
        DirectButton.destroy(self)
        return

    def hide(self):
        DirectButton.hide(self)
        self.vitaeMeter.hide()
        self.statusTray.updateHp(localAvatar.getHp(), localAvatar.getMaxHp())
        self.statusTray.updateVoodoo(localAvatar.getMojo(), localAvatar.getMaxMojo())

    def show(self):
        DirectButton.show(self)
        self.vitaeMeter.show()
        inv = localAvatar.getInventory()
        if inv:
            vtLevel = inv.getStackQuantity(InventoryType.Vitae_Level)
            vtCost = inv.getStackQuantity(InventoryType.Vitae_Cost)
            vtLeft = inv.getStackQuantity(InventoryType.Vitae_Left)
            self.updateVitae(vtLevel, vtCost, vtLeft)

    def updateVitae(self, level, cost, left):
        self.vitaeMeter.update(level, cost, left)
        if level > 0:
            self.vitaeMeter.show()
            self.showClamps()
        else:
            self.vitaeMeter.hide()
            self.hideClamps()

    def createExpAlert(self, amount, duration, position, posChange):
        textGenerator = TextNode('textGenerator')
        if amount < 0:
            textGenerator.setText(str(amount))
        else:
            textGenerator.setText('+' + str(amount) + ' ' + PLocalizer.Reputation)
        textGenerator.setFont(PiratesGlobals.getPirateOutlineFont())
        textGenerator.clearShadow()
        textGenerator.setAlign(TextNode.ACenter)
        textGenerator.setTextColor(1.0, 1.0, 1.0, 1.0)
        textScale = 0.075
        newTextNode = textGenerator.generate()
        newTextDummy = render2d.attachNewNode(newTextNode)
        newTextDummy.setPos(render2d, position)
        newTextDummy.setHpr(render2d, 0.0, 0.0, 0.0)
        newTextDummy.setScale(textScale)
        newTextDummy.setBin('gui-popup', 0)
        if hasattr(self, 'moveUpIval'):
            self.moveUpIval.finish()
            del self.moveUpIval
        if hasattr(self, 'scaleDown'):
            self.scaleDown.finish()
            del self.scaleDown
        if hasattr(self, 'fadeOut'):
            self.fadeOut.finish()
            del self.fadeOut
        if hasattr(self, 'track'):
            self.track.finish()
            del self.track
        self.moveUpIval = newTextDummy.posInterval(duration, position + posChange)
        self.scaleDown = newTextDummy.scaleInterval(duration * 0.75, textScale * 0.7, blendType='easeInOut')
        self.fadeOut = newTextDummy.colorScaleInterval(duration * 0.25, Vec4(0, 0, 0, 0))
        self.track = Sequence(Parallel(self.moveUpIval, Sequence(Wait(0.25), self.scaleDown), Sequence(Wait(0.75), self.fadeOut)), Func(self.removeExpAlert, newTextDummy))
        self.track.start()

    def removeExpAlert(self, alert):
        if alert:
            alert.removeNode()
            alert = None
        return

    def createLevelUpAlert(self, duration, position, posChange):
        textGenerator = TextNode('textGenerator')
        textGenerator.setText(PLocalizer.LevelUp)
        textGenerator.setFont(PiratesGlobals.getPirateOutlineFont())
        textGenerator.clearShadow()
        textGenerator.setAlign(TextNode.ACenter)
        textGenerator.setTextColor(1.0, 1.0, 1.0, 1.0)
        textScale = 0.075
        newTextNode = textGenerator.generate()
        newTextDummy = render2d.attachNewNode(newTextNode)
        newTextDummy.setPos(render2d, position)
        newTextDummy.setHpr(render2d, 0.0, 0.0, 0.0)
        newTextDummy.setScale(textScale)
        newTextDummy.setBin('gui-popup', 0)
        if hasattr(self, 'moveUpIval'):
            self.moveUpIval.finish()
            del self.moveUpIval
        if hasattr(self, 'scaleDown'):
            self.scaleDown.finish()
            del self.scaleDown
        if hasattr(self, 'fadeOut'):
            self.fadeOut.finish()
            del self.fadeOut
        if hasattr(self, 'track'):
            self.track.finish()
            del self.track
        self.moveUpIval = newTextDummy.posInterval(duration, position + posChange)
        self.scaleDown = newTextDummy.scaleInterval(duration * 0.75, textScale * 0.7, blendType='easeInOut')
        self.fadeOut = newTextDummy.colorScaleInterval(duration * 0.25, Vec4(0, 0, 0, 0))
        self.track = Sequence(Parallel(self.moveUpIval, Sequence(Wait(0.25), self.scaleDown), Sequence(Wait(0.75), self.fadeOut)), Func(self.removeExpAlert, newTextDummy))
        self.track.start()

    def showClamps(self):
        self.clamps.show()

    def hideClamps(self):
        self.clamps.hide()

    def turnHighlightOn(self, event=None):
        self.glow.show()
        self.glow2.show()

    def turnHighlightOff(self, event=None):
        self.glow.hide()
        self.glow2.hide()