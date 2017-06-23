from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
import random
from pirates.inventory import ItemGlobals
RBROW = 0
LBROW = 1
LEAR = 2
REAR = 3
NOSE = 4
MOUTH = 5
LHAND = 6
RHAND = 7
JewelryTypes = [
 RBROW, LBROW, LEAR, REAR, NOSE, MOUTH, LHAND, RHAND]
JewelryOptionStrings = {RBROW: 'RBrow',LBROW: 'LBrow',LEAR: 'LEar',REAR: 'REar',NOSE: 'Nose',MOUTH: 'Mouth',LHAND: 'LHand',RHAND: 'RHand'}
PERLA_ALODIA_QUEST_A = 0
DAJIN_MING_QUEST_A = 1
JEWELER_SMITTY_QUEST_A = 2
PERLA_ALODIA_QUEST_B = 3
DAJIN_MING_QUEST_B = 4
JEWELER_SMITTY_QUEST_B = 5
questDrops = {PERLA_ALODIA_QUEST_A: [ItemGlobals.RUBY_LIP_RING, ItemGlobals.RUBY_LIP_RING],PERLA_ALODIA_QUEST_B: [ItemGlobals.RUBY_AND_AMETHYST_EAR_STUD_AND_RING, ItemGlobals.RUBY_AND_AMETHYST_EAR_STUD_AND_RING],DAJIN_MING_QUEST_A: [ItemGlobals.ONYX_LARGE_EAR_LOOP, ItemGlobals.ONYX_LARGE_EAR_LOOP],JEWELER_SMITTY_QUEST_A: [ItemGlobals.SAPPHIRE_BROW_RING, ItemGlobals.SAPPHIRE_BROW_RING],DAJIN_MING_QUEST_B: [ItemGlobals.EMERALD_DOUBLE_NOSE_SPIKE, ItemGlobals.EMERALD_DOUBLE_NOSE_SPIKE],JEWELER_SMITTY_QUEST_B: [ItemGlobals.TURQUOISE_BROW_SPIKE, ItemGlobals.TURQUOISE_BROW_SPIKE]}
quest_items = [
 ItemGlobals.RUBY_LIP_RING, ItemGlobals.ONYX_LARGE_EAR_LOOP, ItemGlobals.SAPPHIRE_BROW_RING, ItemGlobals.EMERALD_DOUBLE_NOSE_SPIKE, ItemGlobals.TURQUOISE_BROW_SPIKE]

def isQuestDrop(id):
    if id in quest_items:
        return True
    else:
        return False