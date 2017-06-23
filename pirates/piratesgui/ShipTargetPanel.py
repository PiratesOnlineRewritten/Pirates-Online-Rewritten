from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiTray
from pirates.uberdog import UberDogGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.battle import EnemyGlobals
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesTimer
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui.ShipArmorGui import ShipArmorGui

class ShipTargetPanel(GuiTray.GuiTray):
    Width = PiratesGuiGlobals.ShipTargetPanelWidth
    Height = PiratesGuiGlobals.ShipTargetPanelHeight

    def __init__(self, ship):
        GuiTray.GuiTray.__init__(self, None, self.Width, self.Height)
        self.ship = ship
        self.shipDisplay = None
        self.hpMeter = None
        self.speedMeter = None
        self.nameBox = None
        self.classBox = None
        self.timer = None
        self.boardingButton = None
        self.initialiseoptions(ShipTargetPanel)
        self.armorGui = None
        self.createGui()
        return

    def createGui(self):
        self.shipcard = loader.loadModel('models/gui/ship_battle')
        tex = self.shipcard.find('**/ship_battle_speed_bar*')
        self.hpFrame = DirectFrame(parent=self, pos=(0.269, 0, -0.005), relief=None, image=tex, image_scale=(0.3,
                                                                                                             1,
                                                                                                             0.6))
        self.hpMeter = DirectWaitBar(parent=self.hpFrame, relief=DGG.RAISED, borderWidth=(0.002,
                                                                                          0.002), range=self.ship.maxHp, value=self.ship.Hp, frameColor=(0,
                                                                                                                                                         0,
                                                                                                                                                         0,
                                                                                                                                                         1), barColor=(0.1,
                                                                                                                                                                       0.7,
                                                                                                                                                                       0.1,
                                                                                                                                                                       1), frameSize=(-0.27, 0.131, -0.01, 0.01), pos=(0.069,
                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                       0.0), text=PLocalizer.Hull, text_scale=PiratesGuiGlobals.TextScaleLarge * 0.75, text_align=TextNode.ALeft, text_pos=(0.16, -0.012), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                                                                           1), text_font=PiratesGlobals.getInterfaceFont())
        self.spFrame = DirectFrame(parent=self, pos=(0.266, 0, -0.03), relief=None, image=tex, image_scale=(0.3,
                                                                                                            1,
                                                                                                            0.52))
        self.speedMeter = DirectWaitBar(parent=self.spFrame, relief=DGG.RAISED, borderWidth=(0.002,
                                                                                             0.002), range=self.ship.maxSp, value=self.ship.Sp, frameColor=(0,
                                                                                                                                                            0,
                                                                                                                                                            0,
                                                                                                                                                            1), barColor=(0.7,
                                                                                                                                                                          0.7,
                                                                                                                                                                          0.1,
                                                                                                                                                                          1), frameSize=(-0.27, 0.132, -0.008, 0.008), pos=(0.069,
                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                            0.0), text=PLocalizer.Speed, text_scale=PiratesGuiGlobals.TextScaleLarge * 0.75, text_align=TextNode.ALeft, text_pos=(0.16, -0.008), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                                                                                                                                                 1), text_font=PiratesGlobals.getInterfaceFont())
        tex = self.shipcard.find('**/ship_battle_dish02*')
        self.nameBox = DirectFrame(parent=self, relief=None, text=self.ship.getName(), text_align=TextNode.ALeft, text_scale=0.045, text_pos=(0.075, -0.085), text_fg=(1,
                                                                                                                                                                       0,
                                                                                                                                                                       0,
                                                                                                                                                                       1), text_shadow=(0,
                                                                                                                                                                                        0,
                                                                                                                                                                                        0,
                                                                                                                                                                                        1), text_font=PiratesGlobals.getInterfaceFont())
        color = EnemyGlobals.getShipNametagColor(self.ship.getTeam())
        self.nameBox['text_fg'] = color
        if self.ship.getSiegeTeam():
            gui = loader.loadModel('models/gui/toplevel_gui')
            if self.ship.getSiegeTeam() == 1:
                flagPath = '**/ship_pvp_icon_french'
            else:
                flagPath = '**/ship_pvp_icon_spanish'
            flag = gui.find(flagPath)
            flag.setScale(0.05)
        else:
            flagPath = EnemyGlobals.getTeamIconModelPath(self.ship.getTeam())
            flagModel = loader.loadModel('models/gui/flag_icons')
            if flagPath:
                flag = flagModel.find(flagPath)
                flag.setScale(0.25)
        if flagPath:
            flag.flattenStrong()
            flag.reparentTo(self.nameBox)
            flag.setPos(0.11, 0, 0.055)
        self.armorGui = ShipArmorGui(self, pos=(0.0, 0.0, 0.0), scale=0.7)
        return

    def destroy(self):
        self.ignoreAll()
        self.destroyGui()
        GuiTray.GuiTray.destroy(self)

    def destroyGui(self):
        if self.shipDisplay:
            self.shipDisplay.removeNode()
            self.shipDisplay = None
        if self.hpMeter:
            self.hpMeter.removeNode()
            self.hpMeter = None
        if self.speedMeter:
            self.speedMeter.removeNode()
            self.speedMeter = None
        if self.nameBox:
            self.nameBox.removeNode()
            self.nameBox = None
        if self.classBox:
            self.classBox.removeNode()
            self.classBox = None
        if self.timer:
            self.timer.destroy()
            self.timer = None
        if self.boardingButton:
            self.boardingButton.removeNode()
            self.boardingButton = None
        return

    def setTimer(self, time):
        if not self.timer:
            self.timer = PiratesTimer.PiratesTimer(showMinutes=1, alarmTime=10)
            self.timer.setScale(0.75)
            self.timer.reparentTo(self)
        self.timer.setTime(time)

    def stopTimer(self):
        if self.timer:
            self.timer.destroy()
            self.timer = None
        return

    def setArmorStatus(self, location, status):
        self.armorGui.setArmorStatus(location, status)