from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
MSG_CAT_DEFAULT = 0
MSG_CAT_THREAT_LEVEL = 1
MSG_CAT_NO_PORT = 2
MSG_CAT_TELL_PORT = 3
MSG_CAT_ANNOUNCE_ATTACK = 4
MSG_CAT_SUNK_SHIP = 5
MSG_CAT_SHORE_CLOSE = 6
MSG_CAT_PURCHASE = 7
MSG_CAT_PURCHASE_FAILED = 8
MSG_CAT_LOOT_WARNING = 9
MMH_QUEUE = 0
MMH_FIRST = 1
MMH_LAST = 2
MMH_COMBINE = 3
MessageOptions = {MSG_CAT_DEFAULT: {'text_fg': PiratesGuiGlobals.TextFG1,'text_shadow': (0, 0, 0, 1),'text_font': PiratesGlobals.getPirateOutlineFont(),'text_scale': 0.05,'showBorder?': True,'messageTime': 7.0,'multiMessageHandling': MMH_FIRST,'messagePrefix': '','priority': 0},MSG_CAT_THREAT_LEVEL: {'text_fg': PiratesGuiGlobals.TextFG1,'text_shadow': (0, 0, 0, 1),'text_font': PiratesGlobals.getPirateOutlineFont(),'text_scale': 0.05,'showBorder?': True,'messageTime': 7.0,'multiMessageHandling': MMH_FIRST,'messagePrefix': '','priority': 0},MSG_CAT_NO_PORT: {'text_fg': PiratesGuiGlobals.TextFG6,'text_shadow': (0, 0, 0, 1),'text_font': PiratesGlobals.getPirateOutlineFont(),'text_scale': 0.05,'showBorder?': True,'messageTime': 1.0,'multiMessageHandling': MMH_FIRST,'messagePrefix': '','priority': 0},MSG_CAT_TELL_PORT: {'text_fg': PiratesGuiGlobals.TextFG1,'text_shadow': (0, 0, 0, 1),'text_font': PiratesGlobals.getPirateOutlineFont(),'text_scale': 0.05,'showBorder?': True,'messageTime': 7.0,'multiMessageHandling': MMH_FIRST,'messagePrefix': '','priority': 0},MSG_CAT_ANNOUNCE_ATTACK: {'text_fg': PiratesGuiGlobals.TextFG1,'text_shadow': (0, 0, 0, 1),'text_font': PiratesGlobals.getPirateOutlineFont(),'text_scale': 0.05,'showBorder?': False,'messageTime': 7.0,'multiMessageHandling': MMH_FIRST,'messagePrefix': '','priority': 0},MSG_CAT_SUNK_SHIP: {'text_fg': PiratesGuiGlobals.TextFG1,'text_shadow': (0, 0, 0, 1),'text_font': PiratesGlobals.getPirateOutlineFont(),'text_scale': 0.05,'showBorder?': False,'messageTime': 7.0,'multiMessageHandling': MMH_FIRST,'messagePrefix': '','priority': 0},MSG_CAT_SHORE_CLOSE: {'text_fg': PiratesGuiGlobals.TextFG6,'text_shadow': (0, 0, 0, 1),'text_font': PiratesGlobals.getPirateOutlineFont(),'text_scale': 0.05,'showBorder?': True,'messageTime': 1.0,'multiMessageHandling': MMH_FIRST,'messagePrefix': '','priority': -1},MSG_CAT_PURCHASE: {'text_fg': PiratesGuiGlobals.TextFG1,'text_shadow': (0, 0, 0, 1),'text_font': PiratesGlobals.getPirateOutlineFont(),'text_scale': 0.05,'showBorder?': True,'messageTime': 3.0,'multiMessageHandling': MMH_FIRST,'messagePrefix': '','priority': 0},MSG_CAT_PURCHASE_FAILED: {'text_fg': PiratesGuiGlobals.TextFG6,'text_shadow': (0, 0, 0, 1),'text_font': PiratesGlobals.getPirateOutlineFont(),'text_scale': 0.05,'showBorder?': True,'messageTime': 3.0,'multiMessageHandling': MMH_FIRST,'messagePrefix': '','priority': 0},MSG_CAT_LOOT_WARNING: {'text_fg': PiratesGuiGlobals.TextFG6,'text_shadow': (0, 0, 0, 1),'text_font': PiratesGlobals.getPirateOutlineFont(),'text_scale': 0.05,'showBorder?': True,'messageTime': 6.0,'multiMessageHandling': MMH_LAST,'messagePrefix': '','priority': 0}}