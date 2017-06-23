from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.fsm import FSM
from direct.task import Task
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
import BattleAvatarGameFSM

class BattleNPCGameFSM(BattleAvatarGameFSM.BattleAvatarGameFSM):

    def __init__(self, av):
        BattleAvatarGameFSM.BattleAvatarGameFSM.__init__(self, av, 'BattleNPCFSM')

    def enterAttackChase(self, extraArgs=[]):
        self.av.motionFSM.on()

    def exitAttackChase(self):
        self.av.motionFSM.off()

    def enterFollow(self, extraArgs=[]):
        self.av.motionFSM.on()

    def exitFollow(self):
        self.av.motionFSM.off()

    def enterRetreat(self, extraArgs=[]):
        self.av.motionFSM.on()

    def exitRetreat(self):
        if self.av.motionFSM.state != 'Off':
            self.av.motionFSM.off()

    def enterInteract(self, extraArgs=[]):
        animState = 'LandRoam'
        self.av.motionFSM.setAnimInfo(self.av.getAnimInfo(animState))

    def exitInteract(self):
        pass

    def enterBattle(self, extraArgs=[]):
        BattleAvatarGameFSM.BattleAvatarGameFSM.enterBattle(self, extraArgs)
        self.av.battleFX(1)

    def exitBattle(self):
        BattleAvatarGameFSM.BattleAvatarGameFSM.exitBattle(self)
        self.av.battleFX(0)

    def enterPatrol(self, extraArgs=[]):
        self.demand('LandRoam')

    def enterPathFollow(self, extraArgs=[]):
        self.demand('LandRoam')

    def enterIdle(self, extraArgs=[]):
        self.demand('LandRoam')

    def enterDeath(self, extraArgs=[]):
        BattleAvatarGameFSM.BattleAvatarGameFSM.enterDeath(self, extraArgs)
        messenger.send(self.av.uniqueName(PiratesGlobals.AVATAR_DEFEAT_MSG))
        messenger.send(self.av.uniqueName(PiratesGlobals.AVATAR_DEATH_MSG))

    def enterBreakCombat(self, extraArgs=[]):
        self.av.showHpString(PLocalizer.Disengage, 0, 5, 0.5)

    def filterBreakCombat(self, request, args=[]):
        if request == 'advance':
            return 'LandRoam'
        if request == 'Battle':
            return
        return self.defaultFilter(request, args)

    def exitBreakCombat(self):
        pass

    def destroy(self):
        if hasattr(self, 'fadeOutIval'):
            self.fadeOutIval.pause()
            del self.fadeOutIval

    def enterFadeOut(self, args=[]):
        if self.av is None:
            return
        if self.av.motionFSM:
            self.av.motionFSM.off()
        self.av.stashBattleCollisions()
        parentGA = self.av.getParentObj()
        npcDoId = self.av.getDoId()
        if base.localAvatar.guiMgr.targetStatusTray.doId == npcDoId:
            base.localAvatar.guiMgr.targetStatusTray.hide()
        if hasattr(self, 'fadeOutIval'):
            self.fadeOutIval.pause()
            del self.fadeOutIval
        nameText = self.av.getNameText()
        if nameText is None:
            return
        self.fadeOutIval = Sequence(Func(self.av.setTransparency, TransparencyAttrib.MAlpha), Func(self.av.setAlphaScale, 1.0), Func(nameText.setAlphaScale, 1.0), Parallel(LerpFunctionInterval(self.av.setAlphaScale, 3.0, fromData=1.0, toData=0.0, blendType='easeInOut'), LerpFunctionInterval(nameText.setAlphaScale, 3.0, fromData=1.0, toData=0.0, blendType='easeInOut')), Func(self.av.hide), Func(nameText.hide), Func(parentGA.sendUpdate, 'requestNPCRemoval', [npcDoId]))
        self.fadeOutIval.start()
        return