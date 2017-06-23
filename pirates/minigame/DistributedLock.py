from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.task.Task import Task
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.minigame import LockGUI
from pirates.minigame import LockGlobals
from pirates.piratesbase import PLocalizer
from pirates.distributed import DistributedInteractive
from pirates.interact import InteractiveBase
from pirates.interact import InteractionManager
from pirates.pirate import HumanDNA

class DistributedLock(DistributedInteractive.DistributedInteractive):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLock')

    def __init__(self, cr):
        print 'DistributedLock:__init__'
        NodePath.__init__(self, 'DistributedLock')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        self.isDoor = 0

    def generate(self):
        print 'DistributedLock:generate'
        DistributedInteractive.DistributedInteractive.generate(self)
        self.setName(self.uniqueName('DistributedLock'))
        self.loadModel()
        self.setInteractOptions(proximityText=PLocalizer.InteractLock, sphereScale=12, diskRadius=12)
        self.reparentTo(render)

    def loadModel(self):
        self.table = loader.loadModel('models/props/treasureChest')
        self.table.setScale(0.5, 0.5, 0.5)
        self.table.reparentTo(self)

    def requestInteraction(self, avId, interactType=0):
        base.localAvatar.motionFSM.off()
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        base.localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def disable(self):
        print 'DistributedLock:disable'
        DistributedInteractive.DistributedInteractive.disable(self)

    def delete(self):
        print 'DistributedLock:delete'
        DistributedInteractive.DistributedInteractive.delete(self)
        del self.table
        self.removeNode()

    def getTableModel(self):
        print 'DistributedLock:getTableModel'
        table = loader.loadModel('models/props/treasureChest')
        table.setScale(0.5, 0.5, 0.5)
        return table

    def guiCallback(self, action):
        print 'DistributedLock:guiCallback'
        if action == LockGlobals.LGUI_EXIT:
            self.d_requestExit()
        elif action == LockGlobals.LGUI_MECHLEFT:
            self.gui.adjustMechanism(-1)
        elif action == LockGlobals.LGUI_MECHRIGHT:
            self.gui.adjustMechanism(1)
        elif action == LockGlobals.LGUI_TRYLOCK:
            self.gui.tryLock()
        else:
            self.notify.error('guiCallback: unknown action: %s' % action)

    def localAvatarSatDown(self, avId, difficulty):
        print 'DistributedLock:localAvatarSatDown'
        self.gui = LockGUI.LockGUI(self, avId, difficulty)
        camera.setPosHpr(self, 0, -5, 4, 0, -30, 0)
        base.camLens.setMinFov(55)
        self.accept('escape', self.guiCallback, extraArgs=[LockGlobals.LGUI_EXIT])
        self.accept('arrow_left', self.guiCallback, extraArgs=[LockGlobals.LGUI_MECHLEFT])
        self.accept('arrow_right', self.guiCallback, extraArgs=[LockGlobals.LGUI_MECHRIGHT])
        self.accept('space', self.guiCallback, extraArgs=[LockGlobals.LGUI_TRYLOCK])
        taskMgr.add(self.movePick, 'lockpick')
        self.acceptInteraction()

    def localAvatarGotUp(self):
        print 'DistributedLock:localAvatarGotUp'
        self.ignore('escape')
        self.ignore('arrow_left')
        self.ignore('arrow_right')
        self.ignore('space')
        self.gui.destroy()
        del self.gui
        taskMgr.remove('lockpick')

    def movePick(self, task):
        self.gui.lockHeartbeat()
        return Task.cont

    def d_requestExit(self):
        print 'DistributedLock:d_requestExit'
        self.sendUpdate('requestExit', [])

    def lockSolved(self, name):
        print 'DistributedLock:lockSolved'
        self.gui.lockOpen(name)

    def requestSeatResponse(self, answer):
        print 'DistributedLock:requestSeatResponse'
        if answer == 1:
            self.localAvatarSatDown()
            localAvatar.b_setGameState('ParlorGame')
        elif answer == 2:
            self.localAvatarGotUp()
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
        else:
            localAvatar.motionFSM.on()

    def setOpen(self, open):
        if open:
            if 'gui' in vars(self):
                self.gui.toolState = LockGlobals.LSTATE_OPEN
            self.finalOpen()

    def finalOpen(self):
        self.chestLid = self.table.find('**/top')
        lidopener = LerpHprInterval(self.chestLid, 1, Vec3(0, -40, 0))
        lidopener.start()
        self.setAllowInteract(False)