import time
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.actor import Actor
from direct.task import Task
from direct.showbase.PythonUtil import report
from pirates.npc import Skeleton
from pirates.pirate import Pirate
from pirates.pirate import HumanDNA
from pirates.quest import QuestParser
from pirates.makeapirate import MakeAPirate
from pirates.piratesbase import PiratesGlobals
from pirates.instance import DistributedInstanceBase
from pirates.cutscene import CutsceneData
from pirates.piratesbase import TimeOfDayManager

class DistributedPiratesTutorialWorld(DistributedInstanceBase.DistributedInstanceBase):
    notify = directNotify.newCategory('DistributedPiratesTutorialWorld')