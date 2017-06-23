from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ShipFrameSelect import ShipFrameSelect
from pirates.piratesgui.ShipSnapshot import ShipSnapshot
from pirates.ship import ShipUpgradeGlobals

class ShipFrameShopping(ShipFrameSelect):

    def __init__(self, parent, **kw):
        optiondefs = (('mode', 'repair', None), )
        self.defineoptions(kw, optiondefs)
        ShipFrameSelect.__init__(self, parent, **kw)
        self.initialiseoptions(ShipFrameShopping)
        return None

    def enableStatsOV(self, shipOV):
        self.snapShot = ShipSnapshot(self, shipOV, pos=self['snapShotPos'])
        typeStr = PLocalizer.YourShip
        if shipOV.state not in ('Off', ):
            self.button['state'] = DGG.DISABLED
        else:
            self.button['state'] = DGG.NORMAL
        if shipOV.Hp <= 0:
            self['shipColorScale'] = VBase4(1, 0.4, 0.4, 1)
        if self['mode'] == 'repair':
            self.button['text'] = PLocalizer.InteractRepair
            if shipOV.Hp == shipOV.maxHp:
                self.button['state'] = DGG.DISABLED
        elif self['mode'] == 'sell':
            self.button['text'] = PLocalizer.InteractSellShips
        elif self['mode'] == 'overhaul':
            self.button['text'] = PLocalizer.InteractOverhaul
        elif self['mode'] == 'upgrade':
            self.button['text'] = PLocalizer.InteractUpgrade
            if shipOV.shipClass not in ShipUpgradeGlobals.HULLS_THAT_CAN_UPGRADE:
                self.button['state'] = DGG.DISABLED
                self.button['text'] = PLocalizer.InteractNoUpgrade