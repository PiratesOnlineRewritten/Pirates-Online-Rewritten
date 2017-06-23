from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PiratesTimer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.ship import ShipMeter
from pirates.ship import ShipUpgradeGlobals
from pirates.ship import ShipGlobals

class ShipSnapshot(DirectFrame):
    PrivateerRepairOnLaunch = base.config.GetBool('privateer-repair-on-launch', 0)

    def __init__(self, parent, shipOV=None, siegeTeam=0, shipName='', shipClass=0, mastInfo=[], hp=0, maxHp=0, sp=0, maxSp=0, cargo=0, maxCargo=0, crew=0, maxCrew=0, time=0, **kw):
        if ShipSnapshot.PrivateerRepairOnLaunch and siegeTeam:
            hp = maxHp
            sp = maxSp
        optiondefs = (
         ('relief', None, None), ('shipOV', shipOV, None), ('siegeTeam', siegeTeam, None), ('shipName', shipName, None), ('shipClass', shipClass, None), ('mastInfo', mastInfo, None), ('hp', hp, None), ('maxHp', maxHp, None), ('sp', sp, None), ('maxSp', maxSp, None), ('cargo', cargo, None), ('maxCargo', maxCargo, None), ('crew', crew, None), ('crewNames', [], self.setCrewNames), ('maxCrew', maxCrew, None), ('time', time, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(ShipSnapshot)
        self.frameBox = None
        self.nameBox = None
        self.hpFrame = None
        self.hpMeter = None
        self.spFrame = None
        self.spMeter = None
        self.cargoMeter = None
        self.cargoLabel = None
        self.crewMeter = None
        self.crewLabel = None
        self.timer = None
        self.shipIcon = None
        self.loadGUI()
        return

    def destroy(self):
        if self.shipIcon:
            self.shipIcon.destroy()
            self.shipIcon = None
        self.frameBox = None
        self.nameBox = None
        self.hpFrame = None
        self.hpMeter = None
        self.spFrame = None
        self.spMeter = None
        self.cargoMeter = None
        self.cargoLabel = None
        self.crewMeter = None
        self.crewLabel = None
        self.timer = None
        self.shipIcon = None
        DirectFrame.destroy(self)
        return

    def loadGUI(self):
        shipcard = loader.loadModel('models/gui/ship_battle')
        tex = shipcard.find('**/ship_battle_speed_bar*')
        self.hpFrame = DirectFrame(parent=self, state=DGG.DISABLED, relief=None, image=tex, image_scale=(0.23,
                                                                                                         1,
                                                                                                         0.5), pos=(0.4,
                                                                                                                    0,
                                                                                                                    0.31), scale=1.2)
        if self['shipOV']:
            hp, maxHp = self['shipOV'].Hp, self['shipOV'].maxHp
            sp, maxSp = self['shipOV'].Sp, self['shipOV'].maxSp
            if ShipSnapshot.PrivateerRepairOnLaunch and self['siegeTeam'] and self['shipOV'].state == 'Off':
                hp = maxHp
                sp = maxSp
        else:
            hp, maxHp = self['hp'], self['maxHp']
            sp, maxSp = self['sp'], self['maxSp']
        hpFraction = max(0, float(hp) / float(maxHp)) * 100.0
        spFraction = max(0, float(sp) / float(maxSp)) * 100.0
        if hpFraction >= 0.5:
            barColor = (0.1, 0.7, 0.1, 1)
        else:
            if hpFraction >= 0.25:
                barColor = (1.0, 1.0, 0.1, 1)
            else:
                barColor = (1.0, 0.0, 0.0, 1)
            self.hpMeter = DirectWaitBar(parent=self.hpFrame, state=DGG.DISABLED, relief=DGG.RAISED, borderWidth=(0.002,
                                                                                                                  0.002), range=100.0, value=hpFraction, frameColor=(0,
                                                                                                                                                                     0,
                                                                                                                                                                     0,
                                                                                                                                                                     1), barColor=barColor, frameSize=(-0.222, 0.084, -0.009, 0.009), pos=(0.069,
                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                           0.001), text=PLocalizer.Hull, text_scale=PiratesGuiGlobals.TextScaleLarge * 0.75, text_align=TextNode.ARight, text_pos=(-0.25, -0.008), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                                                                                                                   1), text_font=PiratesGlobals.getInterfaceFont())
            self.spFrame = DirectFrame(parent=self, state=DGG.DISABLED, relief=None, image=tex, image_scale=(0.23,
                                                                                                             1,
                                                                                                             0.5), pos=(0.4,
                                                                                                                        0,
                                                                                                                        0.26), scale=1.2)
            self.spMeter = DirectWaitBar(parent=self.spFrame, state=DGG.DISABLED, relief=DGG.RAISED, borderWidth=(0.002,
                                                                                                                  0.002), range=100.0, value=spFraction, frameColor=(0,
                                                                                                                                                                     0,
                                                                                                                                                                     0,
                                                                                                                                                                     1), barColor=(0.7,
                                                                                                                                                                                   0.7,
                                                                                                                                                                                   0.1,
                                                                                                                                                                                   1), frameSize=(-0.222, 0.084, -0.009, 0.009), pos=(0.069,
                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                      0.001), text=PLocalizer.Speed, text_scale=PiratesGuiGlobals.TextScaleLarge * 0.75, text_align=TextNode.ARight, text_pos=(-0.25, -0.008), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                                                                                                                                                                               1), text_font=PiratesGlobals.getInterfaceFont())
            cargoTex = shipcard.find('**/ship_battle_dish02*')
            if self['shipOV']:
                cargo, maxCargo = len(self['shipOV'].cargo), self['shipOV'].maxCargo
            else:
                cargo, maxCargo = self['cargo'], self['maxCargo']
            self.cargoMeter = GuiButton.GuiButton(parent=self, state=DGG.DISABLED, relief=None, helpText=PLocalizer.CargoIconHelp2, helpPos=(0.1,
                                                                                                                                             0,
                                                                                                                                             0.15), image=cargoTex, image_scale=0.32, text='%d/%d' % (cargo, maxCargo), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_pos=(0.0, -0.03), text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getInterfaceFont(), pos=(0.263,
                                                                                                                                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                                                                                                                                              0.17))
            self.cargoLabel = DirectLabel(parent=self.cargoMeter, relief=None, state=DGG.DISABLED, text=PLocalizer.Cargo, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.0,
                                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                                       0.015))
            if self['shipOV']:
                crew, maxCrew = self['shipOV'].crewCount, self['shipOV'].maxCrew
            else:
                crew, maxCrew = self['crew'], self['maxCrew']
            self.crewMeter = GuiButton.GuiButton(parent=self, state=DGG.DISABLED, relief=None, helpText=PLocalizer.CrewIconHelp, helpPos=(-0.1, 0, 0.15), image=cargoTex, image_scale=0.32, text='%d/%d' % (crew, maxCrew), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_pos=(0.0, -0.03), text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getInterfaceFont(), pos=(0.402,
                                                                                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                                                                                  0.17))
            self.crewLabel = DirectLabel(parent=self.crewMeter, relief=None, state=DGG.DISABLED, text=PLocalizer.Crew, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.0,
                                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                                    0.015))
            if self['shipOV']:
                time = self['shipOV'].getTimeLeft()
            else:
                time = self['time']
            self.timer = PiratesTimer.PiratesTimer(showMinutes=True, mode=None, titleText='', titleFg='', infoText='', cancelText='', cancelCallback=None)
            self.timer.setFontColor(PiratesGuiGlobals.TextFG2)
            self.timer.reparentTo(self)
            self.timer.setScale(0.55)
            self.timer.setPos(0.54, 0, 0.17)
            if time:
                self.timer.unstash()
                self.timer.countdown(time)
            self.timer.stash()
            self.timer.timerExpired()
        return

    def loadShipIcon(self):
        self.shipIcon = ShipMeter.ShipMeter(0, self['shipClass'], self['mastInfo'])
        self.shipIcon.reparentTo(self)
        self.shipIcon.setDepthTest(1)
        self.shipIcon.setDepthWrite(1)
        self.shipIcon.setPos(0, 0, 0.17)
        self.shipIcon.setHpr(-60, 12, 15)
        self.shipIcon.setScale(0.42)

    def setCustomization(self, customHull, customRigging, customPattern, customLogo):
        shipTypeInfo = ShipGlobals.getShipConfig(self['shipClass'])
        shipHullInfo = ShipUpgradeGlobals.HULL_TYPES.get(customHull)
        cargoMult = shipHullInfo['Cargo']
        if self['shipOV']:
            cargo = len(self['shipOV'].cargo)
            maxCargo = shipTypeInfo['maxCargo']
        else:
            cargo = self['cargo']
            maxCargo = shipTypeInfo['maxCargo']
        self.cargoMeter['text'] = '%d/%d' % (cargo, maxCargo * cargoMult)

    def setCrewNames(self):
        if hasattr(self, 'crewMeter'):
            if self['crewNames']:
                PLocalizer.KnownCrew = 'Recognized'
                self.crewMeter['helpText'] = '%s\n-\n%s:\n%s' % (PLocalizer.CrewIconHelp, PLocalizer.KnownCrew, '\n'.join(self['crewNames']))
            else:
                self.crewMeter['helpText'] = PLocalizer.CrewIconHelp