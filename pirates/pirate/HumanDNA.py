from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from pirates.makeapirate import ClothingGlobals
from pirates.pirate import BodyDefs
from pirates.inventory.ItemConstants import DYE_COLORS
from otp.speedchat import ColorSpace
from pirates.piratesbase import PiratesGlobals

notify = directNotify.newCategory('HumanDNA')
LAYER1_CLOTHES = 1
LAYER2_CLOTHES = 2
LAYER3_CLOTHES = 3
ClothesMaxMAPColor = 21
pirateModelTypes = [
 'sf', 'ms', 'mi', 'tp', 'tm']
pirateHeadTypes = [
 'a', 'b', 'c', 'd', 'e']
availableHairColors = [
 0, 1, 2, 3, 4, 5, 6, 7]
hairColors = [VBase4(141 / 255.0, 106 / 255.0, 41 / 255.0, 255 / 255.0), VBase4(78 / 255.0, 57 / 255.0, 24 / 255.0, 255 / 255.0), VBase4(255 / 255.0, 214 / 255.0, 125 / 255.0, 255 / 255.0), VBase4(200 / 255.0, 153 / 255.0, 73 / 255.0, 255 / 255.0), VBase4(133 / 255.0, 58 / 255.0, 33 / 255.0, 255 / 255.0), VBase4(86 / 255.0, 34 / 255.0, 0 / 255.0, 255 / 255.0), VBase4(41 / 255.0, 41 / 255.0, 41 / 255.0, 255 / 255.0), VBase4(187 / 255.0, 187 / 255.0, 187 / 255.0, 255 / 255.0), VBase4(0 / 255.0, 128 / 255.0, 0 / 255.0, 255 / 255.0)]
hatColorsOld = [
 [
  VBase4(255 / 255.0, 255 / 255.0, 255 / 255.0, 255 / 255.0), VBase4(194 / 255.0, 210 / 255.0, 222 / 255.0, 255 / 255.0), VBase4(255 / 255.0, 233 / 255.0, 198 / 255.0, 255 / 255.0), VBase4(208 / 255.0, 213 / 255.0, 152 / 255.0, 255 / 255.0), VBase4(164 / 255.0, 99 / 255.0, 60 / 255.0, 255 / 255.0), VBase4(196 / 255.0, 144 / 255.0, 147 / 255.0, 255 / 255.0), VBase4(189 / 255.0, 181 / 255.0, 197 / 255.0, 255 / 255.0), VBase4(167 / 255.0, 167 / 255.0, 167 / 255.0, 255 / 255.0), VBase4(146 / 255.0, 177 / 255.0, 188 / 255.0, 255 / 255.0), VBase4(226 / 255.0, 198 / 255.0, 137 / 255.0, 255 / 255.0), VBase4(155 / 255.0, 159 / 255.0, 107 / 255.0, 255 / 255.0), VBase4(148 / 255.0, 112 / 255.0, 72 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 75 / 255.0, 80 / 255.0, 255 / 255.0), VBase4(152 / 255.0, 145 / 255.0, 159 / 255.0, 255 / 255.0), VBase4(94 / 255.0, 94 / 255.0, 94 / 255.0, 255 / 255.0), VBase4(83 / 255.0, 108 / 255.0, 135 / 255.0, 255 / 255.0), VBase4(161 / 255.0, 133 / 255.0, 72 / 255.0, 255 / 255.0), VBase4(106 / 255.0, 121 / 255.0, 96 / 255.0, 255 / 255.0), VBase4(101 / 255.0, 68 / 255.0, 32 / 255.0, 255 / 255.0), VBase4(110 / 255.0, 43 / 255.0, 47 / 255.0, 255 / 255.0), VBase4(115 / 255.0, 105 / 255.0, 126 / 255.0, 255 / 255.0), VBase4(220 / 255.0, 111 / 255.0, 45 / 255.0, 255 / 255.0), VBase4(250 / 255.0, 208 / 255.0, 117 / 255.0, 255 / 255.0), VBase4(59 / 255.0, 178 / 255.0, 220 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 113 / 255.0, 207 / 255.0, 255 / 255.0), VBase4(87 / 255.0, 141 / 255.0, 88 / 255.0, 255 / 255.0), VBase4(190 / 255.0, 67 / 255.0, 128 / 255.0, 255 / 255.0), VBase4(46 / 255.0, 190 / 255.0, 68 / 255.0, 255 / 255.0), VBase4(70 / 255.0, 126 / 255.0, 219 / 255.0, 255 / 255.0), VBase4(201 / 255.0, 14 / 255.0, 14 / 255.0, 255 / 255.0), VBase4(21 / 255.0, 22 / 255.0, 24 / 255.0, 255 / 255.0)], [VBase4(255 / 255.0, 255 / 255.0, 255 / 255.0, 255 / 255.0), VBase4(194 / 255.0, 210 / 255.0, 222 / 255.0, 255 / 255.0), VBase4(255 / 255.0, 233 / 255.0, 198 / 255.0, 255 / 255.0), VBase4(206 / 255.0, 231 / 255.0, 153 / 255.0, 255 / 255.0), VBase4(252 / 255.0, 190 / 255.0, 171 / 255.0, 255 / 255.0), VBase4(196 / 255.0, 144 / 255.0, 147 / 255.0, 255 / 255.0), VBase4(226 / 255.0, 203 / 255.0, 249 / 255.0, 255 / 255.0), VBase4(167 / 255.0, 167 / 255.0, 167 / 255.0, 255 / 255.0), VBase4(133 / 255.0, 208 / 255.0, 222 / 255.0, 255 / 255.0), VBase4(203 / 255.0, 177 / 255.0, 122 / 255.0, 255 / 255.0), VBase4(150 / 255.0, 173 / 255.0, 100 / 255.0, 255 / 255.0), VBase4(237 / 255.0, 188 / 255.0, 216 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 75 / 255.0, 80 / 255.0, 255 / 255.0), VBase4(185 / 255.0, 167 / 255.0, 203 / 255.0, 255 / 255.0), VBase4(94 / 255.0, 94 / 255.0, 94 / 255.0, 255 / 255.0), VBase4(72 / 255.0, 146 / 255.0, 159 / 255.0, 255 / 255.0), VBase4(101 / 255.0, 68 / 255.0, 32 / 255.0, 255 / 255.0), VBase4(106 / 255.0, 121 / 255.0, 96 / 255.0, 255 / 255.0), VBase4(195 / 255.0, 100 / 255.0, 154 / 255.0, 255 / 255.0), VBase4(110 / 255.0, 43 / 255.0, 47 / 255.0, 255 / 255.0), VBase4(148 / 255.0, 127 / 255.0, 171 / 255.0, 255 / 255.0), VBase4(220 / 255.0, 111 / 255.0, 45 / 255.0, 255 / 255.0), VBase4(250 / 255.0, 208 / 255.0, 117 / 255.0, 255 / 255.0), VBase4(59 / 255.0, 178 / 255.0, 220 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 113 / 255.0, 207 / 255.0, 255 / 255.0), VBase4(87 / 255.0, 141 / 255.0, 88 / 255.0, 255 / 255.0), VBase4(190 / 255.0, 67 / 255.0, 128 / 255.0, 255 / 255.0), VBase4(46 / 255.0, 190 / 255.0, 68 / 255.0, 255 / 255.0), VBase4(70 / 255.0, 126 / 255.0, 219 / 255.0, 255 / 255.0), VBase4(201 / 255.0, 14 / 255.0, 14 / 255.0, 255 / 255.0), VBase4(21 / 255.0, 22 / 255.0, 24 / 255.0, 255 / 255.0)]]
skinColors = [
 VBase4(229 / 255.0, 186 / 255.0, 142 / 255.0, 255 / 255.0), VBase4(228 / 255.0, 191 / 255.0, 139 / 255.0, 255 / 255.0), VBase4(230 / 255.0, 194 / 255.0, 178 / 255.0, 255 / 255.0), VBase4(227 / 255.0, 198 / 255.0, 191 / 255.0, 255 / 255.0), VBase4(171 / 255.0, 121 / 255.0, 86 / 255.0, 255 / 255.0), VBase4(181 / 255.0, 149 / 255.0, 111 / 255.0, 255 / 255.0), VBase4(175 / 255.0, 145 / 255.0, 104 / 255.0, 255 / 255.0), VBase4(182 / 255.0, 130 / 255.0, 106 / 255.0, 255 / 255.0), VBase4(183 / 255.0, 150 / 255.0, 142 / 255.0, 255 / 255.0), VBase4(142 / 255.0, 97 / 255.0, 64 / 255.0, 255 / 255.0), VBase4(151 / 255.0, 104 / 255.0, 87 / 255.0, 255 / 255.0), VBase4(147 / 255.0, 123 / 255.0, 86 / 255.0, 255 / 255.0), VBase4(151 / 255.0, 104 / 255.0, 87 / 255.0, 255 / 255.0), VBase4(161 / 255.0, 126 / 255.0, 115 / 255.0, 255 / 255.0), VBase4(108 / 255.0, 71 / 255.0, 44 / 255.0, 255 / 255.0), VBase4(101 / 255.0, 80 / 255.0, 62 / 255.0, 255 / 255.0), VBase4(98 / 255.0, 79 / 255.0, 51 / 255.0, 255 / 255.0), VBase4(93 / 255.0, 63 / 255.0, 47 / 255.0, 255 / 255.0), VBase4(139 / 255.0, 110 / 255.0, 99 / 255.0, 255 / 255.0), VBase4(81 / 255.0, 59 / 255.0, 44 / 255.0, 255 / 255.0)]
crazySkinColors = [
 VBase4(0 / 255.0, 255 / 255.0, 128 / 255.0, 255 / 255.0), VBase4(128 / 255.0, 0 / 255.0, 255 / 255.0, 255 / 255.0), VBase4(128 / 255.0, 255 / 255.0, 255 / 255.0, 255 / 255.0), VBase4(0 / 255.0, 206 / 255.0, 209 / 255.0, 255 / 255.0), VBase4(255 / 255.0, 0 / 255.0, 255 / 255.0, 255 / 255.0), VBase4(255 / 255.0, 255 / 255.0, 0 / 255.0, 255 / 255.0), VBase4(255 / 255.0, 0 / 255.0, 0 / 255.0, 255 / 255.0), VBase4(0 / 255.0, 0 / 255.0, 255 / 255.0, 255 / 255.0), VBase4(0 / 255.0, 255 / 255.0, 0 / 255.0, 255 / 255.0)]
crazySkinColorRarities = [
 15, 30, 45, 56, 67, 78, 85, 92, 100]

def getRandomCrazySkinColor():
    randRoll = random.randint(0, 99)
    numColors = len(crazySkinColors)
    for i in range(numColors):
        if randRoll < crazySkinColorRarities[i]:
            return i

    return 0


jewelryColors = [
 None, VBase4(255 / 255.0, 215 / 255.0, 0 / 255.0, 255 / 255.0), VBase4(192 / 255.0, 192 / 255.0, 192 / 255.0, 255 / 255.0), VBase4(176 / 255.0, 23 / 255.0, 31 / 255.0, 255 / 255.0), VBase4(128 / 255.0, 0 / 255.0, 128 / 255.0, 255 / 255.0), VBase4(39 / 255.0, 64 / 255.0, 139 / 255.0, 255 / 255.0), VBase4(0 / 255.0, 206 / 255.0, 209 / 255.0, 255 / 255.0), VBase4(0 / 255.0, 201 / 255.0, 87 / 255.0, 255 / 255.0), VBase4(30 / 255.0, 30 / 255.0, 30 / 255.0, 255 / 255.0)]
clothesTopColorsOld = [
 [
  VBase4(255 / 255.0, 255 / 255.0, 255 / 255.0, 255 / 255.0), VBase4(194 / 255.0, 210 / 255.0, 222 / 255.0, 255 / 255.0), VBase4(255 / 255.0, 233 / 255.0, 198 / 255.0, 255 / 255.0), VBase4(208 / 255.0, 213 / 255.0, 152 / 255.0, 255 / 255.0), VBase4(164 / 255.0, 99 / 255.0, 60 / 255.0, 255 / 255.0), VBase4(196 / 255.0, 144 / 255.0, 147 / 255.0, 255 / 255.0), VBase4(189 / 255.0, 181 / 255.0, 197 / 255.0, 255 / 255.0), VBase4(167 / 255.0, 167 / 255.0, 167 / 255.0, 255 / 255.0), VBase4(146 / 255.0, 177 / 255.0, 188 / 255.0, 255 / 255.0), VBase4(226 / 255.0, 198 / 255.0, 137 / 255.0, 255 / 255.0), VBase4(155 / 255.0, 159 / 255.0, 107 / 255.0, 255 / 255.0), VBase4(148 / 255.0, 112 / 255.0, 72 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 75 / 255.0, 80 / 255.0, 255 / 255.0), VBase4(152 / 255.0, 145 / 255.0, 159 / 255.0, 255 / 255.0), VBase4(94 / 255.0, 94 / 255.0, 94 / 255.0, 255 / 255.0), VBase4(83 / 255.0, 108 / 255.0, 135 / 255.0, 255 / 255.0), VBase4(161 / 255.0, 133 / 255.0, 72 / 255.0, 255 / 255.0), VBase4(106 / 255.0, 121 / 255.0, 96 / 255.0, 255 / 255.0), VBase4(101 / 255.0, 68 / 255.0, 32 / 255.0, 255 / 255.0), VBase4(110 / 255.0, 43 / 255.0, 47 / 255.0, 255 / 255.0), VBase4(115 / 255.0, 105 / 255.0, 126 / 255.0, 255 / 255.0), VBase4(220 / 255.0, 111 / 255.0, 45 / 255.0, 255 / 255.0), VBase4(250 / 255.0, 208 / 255.0, 117 / 255.0, 255 / 255.0), VBase4(59 / 255.0, 178 / 255.0, 220 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 113 / 255.0, 207 / 255.0, 255 / 255.0), VBase4(87 / 255.0, 141 / 255.0, 88 / 255.0, 255 / 255.0), VBase4(190 / 255.0, 67 / 255.0, 128 / 255.0, 255 / 255.0), VBase4(46 / 255.0, 190 / 255.0, 68 / 255.0, 255 / 255.0), VBase4(70 / 255.0, 126 / 255.0, 219 / 255.0, 255 / 255.0), VBase4(201 / 255.0, 14 / 255.0, 14 / 255.0, 255 / 255.0), VBase4(21 / 255.0, 22 / 255.0, 24 / 255.0, 255 / 255.0)], [VBase4(255 / 255.0, 255 / 255.0, 255 / 255.0, 255 / 255.0), VBase4(194 / 255.0, 210 / 255.0, 222 / 255.0, 255 / 255.0), VBase4(255 / 255.0, 233 / 255.0, 198 / 255.0, 255 / 255.0), VBase4(206 / 255.0, 231 / 255.0, 153 / 255.0, 255 / 255.0), VBase4(252 / 255.0, 190 / 255.0, 171 / 255.0, 255 / 255.0), VBase4(196 / 255.0, 144 / 255.0, 147 / 255.0, 255 / 255.0), VBase4(226 / 255.0, 203 / 255.0, 249 / 255.0, 255 / 255.0), VBase4(167 / 255.0, 167 / 255.0, 167 / 255.0, 255 / 255.0), VBase4(133 / 255.0, 208 / 255.0, 222 / 255.0, 255 / 255.0), VBase4(203 / 255.0, 177 / 255.0, 122 / 255.0, 255 / 255.0), VBase4(150 / 255.0, 173 / 255.0, 100 / 255.0, 255 / 255.0), VBase4(237 / 255.0, 188 / 255.0, 216 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 75 / 255.0, 80 / 255.0, 255 / 255.0), VBase4(185 / 255.0, 167 / 255.0, 203 / 255.0, 255 / 255.0), VBase4(94 / 255.0, 94 / 255.0, 94 / 255.0, 255 / 255.0), VBase4(72 / 255.0, 146 / 255.0, 159 / 255.0, 255 / 255.0), VBase4(101 / 255.0, 68 / 255.0, 32 / 255.0, 255 / 255.0), VBase4(106 / 255.0, 121 / 255.0, 96 / 255.0, 255 / 255.0), VBase4(195 / 255.0, 100 / 255.0, 154 / 255.0, 255 / 255.0), VBase4(110 / 255.0, 43 / 255.0, 47 / 255.0, 255 / 255.0), VBase4(148 / 255.0, 127 / 255.0, 171 / 255.0, 255 / 255.0), VBase4(220 / 255.0, 111 / 255.0, 45 / 255.0, 255 / 255.0), VBase4(250 / 255.0, 208 / 255.0, 117 / 255.0, 255 / 255.0), VBase4(59 / 255.0, 178 / 255.0, 220 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 113 / 255.0, 207 / 255.0, 255 / 255.0), VBase4(87 / 255.0, 141 / 255.0, 88 / 255.0, 255 / 255.0), VBase4(190 / 255.0, 67 / 255.0, 128 / 255.0, 255 / 255.0), VBase4(46 / 255.0, 190 / 255.0, 68 / 255.0, 255 / 255.0), VBase4(70 / 255.0, 126 / 255.0, 219 / 255.0, 255 / 255.0), VBase4(201 / 255.0, 14 / 255.0, 14 / 255.0, 255 / 255.0), VBase4(21 / 255.0, 22 / 255.0, 24 / 255.0, 255 / 255.0)]]
clothesBotColorsOld = [
 [
  VBase4(255 / 255.0, 255 / 255.0, 255 / 255.0, 255 / 255.0), VBase4(194 / 255.0, 210 / 255.0, 222 / 255.0, 255 / 255.0), VBase4(255 / 255.0, 233 / 255.0, 198 / 255.0, 255 / 255.0), VBase4(208 / 255.0, 213 / 255.0, 152 / 255.0, 255 / 255.0), VBase4(164 / 255.0, 99 / 255.0, 60 / 255.0, 255 / 255.0), VBase4(196 / 255.0, 144 / 255.0, 147 / 255.0, 255 / 255.0), VBase4(189 / 255.0, 181 / 255.0, 197 / 255.0, 255 / 255.0), VBase4(146 / 255.0, 177 / 255.0, 188 / 255.0, 255 / 255.0), VBase4(107 / 255.0, 107 / 255.0, 107 / 255.0, 255 / 255.0), VBase4(203 / 255.0, 177 / 255.0, 122 / 255.0, 255 / 255.0), VBase4(155 / 255.0, 159 / 255.0, 107 / 255.0, 255 / 255.0), VBase4(148 / 255.0, 112 / 255.0, 72 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 75 / 255.0, 80 / 255.0, 255 / 255.0), VBase4(152 / 255.0, 145 / 255.0, 159 / 255.0, 255 / 255.0), VBase4(83 / 255.0, 108 / 255.0, 135 / 255.0, 255 / 255.0), VBase4(41 / 255.0, 50 / 255.0, 60 / 255.0, 255 / 255.0), VBase4(178 / 255.0, 147 / 255.0, 80 / 255.0, 255 / 255.0), VBase4(106 / 255.0, 121 / 255.0, 96 / 255.0, 255 / 255.0), VBase4(101 / 255.0, 68 / 255.0, 32 / 255.0, 255 / 255.0), VBase4(110 / 255.0, 43 / 255.0, 47 / 255.0, 255 / 255.0), VBase4(115 / 255.0, 105 / 255.0, 126 / 255.0, 255 / 255.0), VBase4(220 / 255.0, 111 / 255.0, 45 / 255.0, 255 / 255.0), VBase4(250 / 255.0, 208 / 255.0, 117 / 255.0, 255 / 255.0), VBase4(59 / 255.0, 178 / 255.0, 220 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 113 / 255.0, 207 / 255.0, 255 / 255.0), VBase4(87 / 255.0, 141 / 255.0, 88 / 255.0, 255 / 255.0), VBase4(190 / 255.0, 67 / 255.0, 128 / 255.0, 255 / 255.0), VBase4(46 / 255.0, 190 / 255.0, 68 / 255.0, 255 / 255.0), VBase4(70 / 255.0, 126 / 255.0, 219 / 255.0, 255 / 255.0), VBase4(201 / 255.0, 14 / 255.0, 14 / 255.0, 255 / 255.0), VBase4(21 / 255.0, 22 / 255.0, 24 / 255.0, 255 / 255.0)], [VBase4(255 / 255.0, 255 / 255.0, 255 / 255.0, 255 / 255.0), VBase4(194 / 255.0, 210 / 255.0, 222 / 255.0, 255 / 255.0), VBase4(255 / 255.0, 233 / 255.0, 198 / 255.0, 255 / 255.0), VBase4(206 / 255.0, 231 / 255.0, 153 / 255.0, 255 / 255.0), VBase4(252 / 255.0, 190 / 255.0, 171 / 255.0, 255 / 255.0), VBase4(196 / 255.0, 144 / 255.0, 147 / 255.0, 255 / 255.0), VBase4(226 / 255.0, 203 / 255.0, 249 / 255.0, 255 / 255.0), VBase4(167 / 255.0, 167 / 255.0, 167 / 255.0, 255 / 255.0), VBase4(133 / 255.0, 208 / 255.0, 222 / 255.0, 255 / 255.0), VBase4(203 / 255.0, 177 / 255.0, 122 / 255.0, 255 / 255.0), VBase4(150 / 255.0, 173 / 255.0, 100 / 255.0, 255 / 255.0), VBase4(237 / 255.0, 188 / 255.0, 216 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 75 / 255.0, 80 / 255.0, 255 / 255.0), VBase4(185 / 255.0, 167 / 255.0, 203 / 255.0, 255 / 255.0), VBase4(94 / 255.0, 94 / 255.0, 94 / 255.0, 255 / 255.0), VBase4(72 / 255.0, 146 / 255.0, 159 / 255.0, 255 / 255.0), VBase4(101 / 255.0, 68 / 255.0, 32 / 255.0, 255 / 255.0), VBase4(106 / 255.0, 121 / 255.0, 96 / 255.0, 255 / 255.0), VBase4(195 / 255.0, 100 / 255.0, 154 / 255.0, 255 / 255.0), VBase4(110 / 255.0, 43 / 255.0, 47 / 255.0, 255 / 255.0), VBase4(148 / 255.0, 127 / 255.0, 171 / 255.0, 255 / 255.0), VBase4(220 / 255.0, 111 / 255.0, 45 / 255.0, 255 / 255.0), VBase4(250 / 255.0, 208 / 255.0, 117 / 255.0, 255 / 255.0), VBase4(59 / 255.0, 178 / 255.0, 220 / 255.0, 255 / 255.0), VBase4(158 / 255.0, 113 / 255.0, 207 / 255.0, 255 / 255.0), VBase4(87 / 255.0, 141 / 255.0, 88 / 255.0, 255 / 255.0), VBase4(190 / 255.0, 67 / 255.0, 128 / 255.0, 255 / 255.0), VBase4(46 / 255.0, 190 / 255.0, 68 / 255.0, 255 / 255.0), VBase4(70 / 255.0, 126 / 255.0, 219 / 255.0, 255 / 255.0), VBase4(201 / 255.0, 14 / 255.0, 14 / 255.0, 255 / 255.0), VBase4(21 / 255.0, 22 / 255.0, 24 / 255.0, 255 / 255.0)]]

def printColors():
    print '** Skin Colors:'
    for color in skinColors:
        outVal = [
         int(color.getX() * 256), int(color.getY() * 256), int(color.getZ() * 256)]
        print str(outVal)

    print '\n ** Jewelry Colors:'
    for color in jewelryColors:
        try:
            outVal = [
             int(color.getX() * 256), int(color.getY() * 256), int(color.getZ() * 256)]
        except:
            pass

        print str(outVal)

    print '\n ** Hair Colors:'
    for color in hairColors:
        outVal = [
         int(color.getX() * 256), int(color.getY() * 256), int(color.getZ() * 256)]
        print str(outVal)

    print '\n ** Male Hat Colors:'
    for color in hatColors[0]:
        outVal = [
         int(color.getX() * 256), int(color.getY() * 256), int(color.getZ() * 256)]
        print str(outVal)

    print '\n ** Female Hat Colors:'
    for color in hatColors[1]:
        outVal = [
         int(color.getX() * 256), int(color.getY() * 256), int(color.getZ() * 256)]
        print str(outVal)

    print '\n ** Male Top Colors:'
    for color in clothesTopColors[0]:
        outVal = [
         int(color.getX() * 256), int(color.getY() * 256), int(color.getZ() * 256)]
        print str(outVal)

    print '\n ** Female Top Colors:'
    for color in clothesTopColors[1]:
        outVal = [
         int(color.getX() * 256), int(color.getY() * 256), int(color.getZ() * 256)]
        print str(outVal)

    print '\n ** Male Bottom Colors:'
    for color in clothesBotColors[0]:
        outVal = [
         int(color.getX() * 256), int(color.getY() * 256), int(color.getZ() * 256)]
        print str(outVal)

    print '\n ** Female Bottom Colors:'
    for color in clothesBotColors[1]:
        outVal = [
         int(color.getX() * 256), int(color.getY() * 256), int(color.getZ() * 256)]
        print str(outVal)


class PirateEyes():

    def __init__(self, color=0):
        self.color = color

    def copy(self, other):
        self.color = other.color

    def __str__(self):
        string = 'color %s' % self.color
        return string


class PirateHair():

    def __init__(self, hair=0, beard=0, mustache=0, color=0):
        self.hair = hair
        self.beard = beard
        self.mustache = mustache
        self.color = color
        self.highlight = 0

    def copy(self, other):
        self.hair = other.hair
        self.beard = other.beard
        self.mustache = other.mustache
        self.color = other.color
        self.highlight = other.highlight

    def __str__(self):
        string = 'style %s, beard %s, mustache %s, color %s, highlight %s' % (self.hair, self.beard, self.mustache, self.color, self.highlight)
        return string


class PirateHead():

    def __init__(self):
        self.headWidth = 0.0
        self.headHeight = 0.0
        self.headRoundness = 0.0
        self.jawWidth = 0.0
        self.jawLength = 0.0
        self.jawRoundness = 0.0
        self.jawChinSize = 0.0
        self.jawAngle = 0.0
        self.texture = 0
        self.mouthWidth = 0.0
        self.mouthLipThickness = 0.0
        self.mouthFrown = 0.0
        self.cheekBoneHeight = 0.0
        self.cheekBoneWidth = 0.0
        self.cheekFat = 0.0
        self.teeth = 0
        self.browWidth = 0.0
        self.browProtruding = 0.0
        self.browAngle = 0.0
        self.browHeight = 0.0
        self.eyeCorner = 0.0
        self.eyeOpeningSize = 0.0
        self.eyeBulge = 0.0
        self.eyes = PirateEyes()
        self.noseBridgeWidth = 0.0
        self.noseNostrilWidth = 0.0
        self.noseLength = 0.0
        self.noseBump = 0.0
        self.noseNostrilHeight = 0.0
        self.noseNostrilAngle = 0.0
        self.noseNostrilIndent = 0.0
        self.noseBridgeBroke = 0.0
        self.noseNostrilBroke = 0.0
        self.earScale = 0.0
        self.earFlapAngle = 0.0
        self.earPosition = 0.0
        self.earLobe = 0.0
        self.hair = PirateHair()

    def copy(self, other):
        self.headWidth = other.headWidth
        self.headHeight = other.headHeight
        self.headRoundness = other.headRoundness
        self.jawWidth = other.jawWidth
        self.jawLength = other.jawLength
        self.jawRoundness = other.jawRoundness
        self.jawChinSize = other.jawChinSize
        self.jawAngle = other.jawAngle
        self.texture = other.texture
        self.mouthWidth = other.mouthWidth
        self.mouthLipThickness = other.mouthLipThickness
        self.mouthFrown = other.mouthFrown
        self.cheekBoneHeight = other.cheekBoneHeight
        self.cheekBoneWidth = other.cheekBoneWidth
        self.cheekFat = other.cheekFat
        self.teeth = other.teeth
        self.browWidth = other.browWidth
        self.browProtruding = other.browProtruding
        self.browAngle = other.browAngle
        self.browHeight = other.browHeight
        self.eyeCorner = other.eyeCorner
        self.eyeOpeningSize = other.eyeOpeningSize
        self.eyeBulge = other.eyeBulge
        self.eyes.copy(other.eyes)
        self.noseBridgeWidth = other.noseBridgeWidth
        self.noseNostrilWidth = other.noseNostrilWidth
        self.noseLength = other.noseLength
        self.noseBump = other.noseBump
        self.noseNostrilHeight = other.noseNostrilHeight
        self.noseNostrilAngle = other.noseNostrilAngle
        self.noseNostrilIndent = other.noseNostrilIndent
        self.noseBridgeBroke = other.noseBridgeBroke
        self.noseNostrilBroke = other.noseNostrilBroke
        self.earScale = other.earScale
        self.earFlapAngle = other.earFlapAngle
        self.earPosition = other.earPosition
        self.earLobe = other.earLobe
        self.hair.copy(other.hair)

    def __str__(self):
        string = '--shape--\n\t' + 'headWidth %s, headHeight %s, headRoundness %s\n\t' % (self.headWidth, self.headHeight, self.headRoundness) + 'jawWidth %s, jawChinSize %s, jawAngle %s, jawLength %s\n\t' % (self.jawWidth, self.jawChinSize, self.jawAngle, self.jawLength) + 'face %s\n\t' % self.texture + '--mouth--\n\t' + 'mouthWidth %s, mouthLipThickness %s, \n\t' % (self.mouthWidth, self.mouthLipThickness) + 'cheekFat %s, teeth %s\n\t' % (self.cheekFat, self.teeth) + '--eyes--\n\t' + 'browProtruding %s\n\t' % self.browProtruding + 'eyeCorner %s, eyeOpeningSize  %s, eyeSpace %s\n\t' % (self.eyeCorner, self.eyeOpeningSize, self.eyeBulge) + 'eye %s\n\t' % self.eyes + '--nose--\n\t' + 'noseBridgeWidth %s, noseNostrilWidth %s, noseLength %s, noseBump %s\n\t' % (self.noseBridgeWidth, self.noseNostrilWidth, self.noseLength, self.noseBump) + 'noseNostrilHeight %s, noseNostrilAngle %s, noseNostrilIndent %s\n\t' % (self.noseNostrilHeight, self.noseNostrilAngle, self.noseNostrilIndent) + 'noseBridgeBroke %s, noseNostrilBroke %s\n\t' % (self.noseBridgeBroke, self.noseNostrilBroke) + '--ear--\n\t' + 'earScale %s, earFlapAngle %s, earPosition %s\n\t' % (self.earScale, self.earFlapAngle, self.earPosition) + '--hair--\n\t' + '%s\n\t' % self.hair
        return string


class PirateBody():

    def __init__(self, shape=0, height=0.0, color=0):
        self.shape = shape
        self.height = height
        self.headSize = 0.0
        self.color = color
        self.skin = 0

    def copy(self, other):
        self.shape = other.shape
        self.height = other.height
        self.headSize = other.headSize
        self.color = other.color
        self.skin = other.skin

    def __str__(self):
        string = 'shape %s, height %s, headSize %s, skintone %s, skinTexture %s' % (self.shape, self.height, self.headSize, self.color, self.skin)
        return string


class PirateClothes():

    def __init__(self, top=0, bot=0, shoe=0, color=0):
        self.shirt = top
        self.vest = 0
        self.coat = 0
        self.pant = bot
        self.belt = 0
        self.sock = 0
        self.shoe = shoe
        self.hat = 0
        self.shirtTexture = 0
        self.vestTexture = 0
        self.coatTexture = 0
        self.pantTexture = 0
        self.beltTexture = 0
        self.sockTexture = 0
        self.shoeTexture = 0
        self.hatTexture = 0
        self.shirtColor = color
        self.vestColor = 0
        self.coatColor = 0
        self.pantColor = color
        self.sashColor = 0
        self.shoeColor = 0
        self.hatColor = 0

    def copy(self, other):
        self.shirt = other.shirt
        self.vest = other.vest
        self.coat = other.coat
        self.pant = other.pant
        self.belt = other.belt
        self.sock = other.sock
        self.shoe = other.shoe
        self.hat = other.hat
        self.shirtTexture = other.shirtTexture
        self.vestTexture = other.vestTexture
        self.coatTexture = other.coatTexture
        self.pantTexture = other.pantTexture
        self.beltTexture = other.beltTexture
        self.sockTexture = other.sockTexture
        self.shoeTexture = other.shoeTexture
        self.hatTexture = other.hatTexture
        self.shirtColor = other.shirtColor
        self.vestColor = other.vestColor
        self.coatColor = other.coatColor
        self.pantColor = other.pantColor
        self.sashColor = other.sashColor
        self.shoeColor = other.shoeColor
        self.hatColor = other.hatColor

    def __str__(self):
        string = 'shirt %s:%s:%s, vest %s:%s:%s, coat %s:%s:%s, pant %s:%s:%s,%s, belt %s:%s:%s, hat %s:%s:%s, sock %s:%s, shoe %s:%s' % (self.shirt, self.shirtTexture, self.shirtColor, self.vest, self.vestTexture, self.vestColor, self.coat, self.coatTexture, self.coatColor, self.pant, self.pantTexture, self.pantColor, self.shoeColor, self.belt, self.beltTexture, self.sashColor, self.hat, self.hatTexture, self.hatColor, self.sock, self.sockTexture, self.shoe, self.shoeTexture)
        return string


class HumanDNA(AvatarDNA.AvatarDNA):

    def __init__(self, gender='m', bodyIndex=None):
        self.type = 'pirate'
        self.tutorial = 0
        self.name = ''
        self.gender = gender
        if bodyIndex == None:
            if BodyDefs.BodyChoiceGenderDict.get(self.gender):
                bodyIndex = BodyDefs.BodyChoiceGenderDict[self.gender][2]
            else:
                bodyIndex = 2
        self.body = PirateBody(bodyIndex)
        self.head = PirateHead()
        self.clothes = PirateClothes()
        self.tattooChest = [
         0, 0.0, 0.0, 1, 0, 0]
        self.tattooZone2 = [0, 0.0, 0.0, 1, 0, 0]
        self.tattooZone3 = [0, 0.0, 0.0, 1, 0, 0]
        self.tattooZone4 = [0, 0.0, 0.0, 1, 0, 0]
        self.tattooZone5 = [0, 0.0, 0.0, 1, 0, 0]
        self.tattooZone6 = [0, 0.0, 0.0, 1, 0, 0]
        self.tattooZone7 = [0, 0.0, 0.0, 1, 0, 0]
        self.tattooZone8 = [0, 0.0, 0.0, 1, 0, 0]
        self.jewelryZone1 = [
         0, 0, 0]
        self.jewelryZone2 = [0, 0, 0]
        self.jewelryZone3 = [0, 0, 0]
        self.jewelryZone4 = [0, 0, 0]
        self.jewelryZone5 = [0, 0, 0]
        self.jewelryZone6 = [0, 0, 0]
        self.jewelryZone7 = [0, 0, 0]
        self.jewelryZone8 = [0, 0, 0]
        return

    def makeMakeAPirate(self):
        if self.gender == 'm':
            self.clothes.shirt = 4
            self.clothes.shirtTexture = 1
            self.clothes.shirtColor = 0
            self.clothes.pant = 0
            self.clothes.pantTexture = 1
            self.clothes.pantColor = 14
            self.clothes.shoe = 1
            self.head.hair.hair = 2
            self.head.hair.color = 1
            self.clothes.hat = 0
            self.clothes.coat = 0
            self.clothes.coatColor = 1
            self.clothes.belt = 1
        elif self.gender == 'f':
            self.clothes.shirt = 0
            self.clothes.shirtTexture = 0
            self.clothes.shirtColor = 0
            self.clothes.pant = 0
            self.clothes.pantColor = 0
            self.clothes.vest = 0
            self.clothes.belt = 1
            self.clothes.shoe = 1
            self.head.hair.hair = 14
            self.head.hair.color = 1
            self.head.mouthLipThickness = 0.25
            self.head.browProtruding = 0.858
            self.head.cheekFat = 0.18
        elif self.gender == 'n':
            self.clothes.coat = 3
            self.clothes.coatColor = 0
            self.clothes.pant = 4
            self.clothes.pantColor = 0
            self.clothes.sock = 0
            self.clothes.shoe = 3
            self.head.hair.hair = 1
            self.clothes.hat = 3
            self.clothes.hatColor = 0
            self.head.texture = 0

    def copy(self, other):
        self.type = other.type
        self.tutorial = other.tutorial
        self.name = other.name
        self.gender = other.gender
        self.body.copy(other.body)
        self.head.copy(other.head)
        self.clothes.copy(other.clothes)
        self.tattooChest = other.tattooChest
        self.tattooZone2 = other.tattooZone2
        self.tattooZone3 = other.tattooZone3
        self.tattooZone4 = other.tattooZone4
        self.tattooZone5 = other.tattooZone5
        self.tattooZone6 = other.tattooZone6
        self.tattooZone7 = other.tattooZone7
        self.tattooZone8 = other.tattooZone8
        self.jewelryZone1 = other.jewelryZone1
        self.jewelryZone2 = other.jewelryZone2
        self.jewelryZone3 = other.jewelryZone3
        self.jewelryZone4 = other.jewelryZone4
        self.jewelryZone5 = other.jewelryZone5
        self.jewelryZone6 = other.jewelryZone6
        self.jewelryZone7 = other.jewelryZone7
        self.jewelryZone8 = other.jewelryZone8

    def __str__(self):
        string = 'type = %s\n' % self.type + 'name = %s\n' % self.name + 'tutorial = %s\n' % self.tutorial + 'gender = %s\n' % self.gender + 'head = %s\n' % self.head + 'body = %s\n' % self.body + 'clothes = %s\n' % self.clothes
        return string

    def saveAsNPCDict(self):
        d = {}
        d[HumanDNA.setTutorial] = self.tutorial
        d[HumanDNA.setName] = self.name
        d[HumanDNA.setGender] = self.gender
        d[HumanDNA.setBodyShape] = self.body.shape
        d[HumanDNA.setBodyHeight] = self.body.height
        d[HumanDNA.setBodyColor] = self.body.color
        d[HumanDNA.setBodySkin] = self.body.skin
        d[HumanDNA.setHeadSize] = self.body.headSize
        d[HumanDNA.setHeadWidth] = self.head.headWidth
        d[HumanDNA.setHeadHeight] = self.head.headHeight
        d[HumanDNA.setHeadRoundness] = self.head.headRoundness
        d[HumanDNA.setJawWidth] = self.head.jawWidth
        d[HumanDNA.setJawRoundness] = self.head.jawRoundness
        d[HumanDNA.setJawChinSize] = self.head.jawChinSize
        d[HumanDNA.setJawAngle] = self.head.jawAngle
        d[HumanDNA.setJawLength] = self.head.jawLength
        d[HumanDNA.setMouthWidth] = self.head.mouthWidth
        d[HumanDNA.setMouthLipThickness] = self.head.mouthLipThickness
        d[HumanDNA.setMouthFrown] = self.head.mouthFrown
        d[HumanDNA.setCheekBoneHeight] = self.head.cheekBoneHeight
        d[HumanDNA.setCheekBoneWidth] = self.head.cheekBoneWidth
        d[HumanDNA.setCheekFat] = self.head.cheekFat
        d[HumanDNA.setBrowWidth] = self.head.browWidth
        d[HumanDNA.setBrowProtruding] = self.head.browProtruding
        d[HumanDNA.setBrowAngle] = self.head.browAngle
        d[HumanDNA.setBrowHeight] = self.head.browHeight
        d[HumanDNA.setEyeCorner] = self.head.eyeCorner
        d[HumanDNA.setEyeOpeningSize] = self.head.eyeOpeningSize
        d[HumanDNA.setEyeBulge] = self.head.eyeBulge
        d[HumanDNA.setNoseBridgeWidth] = self.head.noseBridgeWidth
        d[HumanDNA.setNoseNostrilWidth] = self.head.noseNostrilWidth
        d[HumanDNA.setNoseLength] = self.head.noseLength
        d[HumanDNA.setNoseBump] = self.head.noseBump
        d[HumanDNA.setNoseNostrilHeight] = self.head.noseNostrilHeight
        d[HumanDNA.setNoseNostrilAngle] = self.head.noseNostrilAngle
        d[HumanDNA.setNoseNostrilIndent] = self.head.noseNostrilIndent
        d[HumanDNA.setNoseBridgeBroke] = self.head.noseBridgeBroke
        d[HumanDNA.setNoseNostrilBroke] = self.head.noseNostrilBroke
        d[HumanDNA.setEarScale] = self.head.earScale
        d[HumanDNA.setEarFlapAngle] = self.head.earFlapAngle
        d[HumanDNA.setEarPosition] = self.head.earPosition
        d[HumanDNA.setEarLobe] = self.head.earLobe
        d[HumanDNA.setHeadTexture] = self.head.texture
        d[HumanDNA.setHairHair] = self.head.hair.hair
        d[HumanDNA.setHairBeard] = self.head.hair.beard
        d[HumanDNA.setHairMustache] = self.head.hair.mustache
        d[HumanDNA.setHairColor] = self.head.hair.color
        d[HumanDNA.setHighLightColor] = self.head.hair.highlight
        d[HumanDNA.setEyesColor] = self.head.eyes.color
        d[HumanDNA.setClothesHat] = (self.clothes.hat, self.clothes.hatTexture)
        d[HumanDNA.setClothesShirt] = (self.clothes.shirt, self.clothes.shirtTexture)
        d[HumanDNA.setClothesPant] = (self.clothes.pant, self.clothes.pantTexture)
        d[HumanDNA.setClothesSock] = (self.clothes.sock, self.clothes.sockTexture)
        d[HumanDNA.setClothesShoe] = (self.clothes.shoe, self.clothes.shoeTexture)
        d[HumanDNA.setClothesVest] = (self.clothes.vest, self.clothes.vestTexture)
        d[HumanDNA.setClothesCoat] = (self.clothes.coat, self.clothes.coatTexture)
        d[HumanDNA.setClothesBelt] = (self.clothes.belt, self.clothes.beltTexture)
        d[HumanDNA.setClothesTopColor] = (self.clothes.shirtColor, self.clothes.vestColor, self.clothes.coatColor)
        d[HumanDNA.setClothesBotColor] = (self.clothes.pantColor, self.clothes.sashColor, self.clothes.shoeColor)
        d[HumanDNA.setTattooChest] = (self.tattooChest[0], self.tattooChest[1], self.tattooChest[2], self.tattooChest[3], self.tattooChest[4], self.tattooChest[5])
        d[HumanDNA.setTattooZone2] = (self.tattooZone2[0], self.tattooZone2[1], self.tattooZone2[2], self.tattooZone2[3], self.tattooZone2[4], self.tattooZone2[5])
        d[HumanDNA.setTattooZone3] = (self.tattooZone3[0], self.tattooZone3[1], self.tattooZone3[2], self.tattooZone3[3], self.tattooZone3[4], self.tattooZone3[5])
        d[HumanDNA.setTattooZone4] = (self.tattooZone4[0], self.tattooZone4[1], self.tattooZone4[2], self.tattooZone4[3], self.tattooZone4[4], self.tattooZone4[5])
        d[HumanDNA.setTattooZone5] = (self.tattooZone5[0], self.tattooZone5[1], self.tattooZone5[2], self.tattooZone5[3], self.tattooZone5[4], self.tattooZone5[5])
        d[HumanDNA.setTattooZone6] = (self.tattooZone6[0], self.tattooZone6[1], self.tattooZone6[2], self.tattooZone6[3], self.tattooZone6[4], self.tattooZone6[5])
        d[HumanDNA.setTattooZone7] = (self.tattooZone7[0], self.tattooZone7[1], self.tattooZone7[2], self.tattooZone7[3], self.tattooZone7[4], self.tattooZone7[5])
        d[HumanDNA.setTattooZone8] = (self.tattooZone8[0], self.tattooZone8[1], self.tattooZone8[2], self.tattooZone8[3], self.tattooZone8[4], self.tattooZone8[5])
        d[HumanDNA.setJewelryZone1] = (self.jewelryZone1[0], self.jewelryZone1[1], self.jewelryZone1[2])
        d[HumanDNA.setJewelryZone2] = (self.jewelryZone2[0], self.jewelryZone2[1], self.jewelryZone2[2])
        d[HumanDNA.setJewelryZone3] = (self.jewelryZone3[0], self.jewelryZone3[1], self.jewelryZone3[2])
        d[HumanDNA.setJewelryZone4] = (self.jewelryZone4[0], self.jewelryZone4[1], self.jewelryZone4[2])
        d[HumanDNA.setJewelryZone5] = (self.jewelryZone5[0], self.jewelryZone5[1], self.jewelryZone5[2])
        d[HumanDNA.setJewelryZone6] = (self.jewelryZone6[0], self.jewelryZone6[1], self.jewelryZone6[2])
        d[HumanDNA.setJewelryZone7] = (self.jewelryZone7[0], self.jewelryZone7[1], self.jewelryZone7[2])
        d[HumanDNA.setJewelryZone8] = (self.jewelryZone8[0], self.jewelryZone8[1], self.jewelryZone8[2])
        return d

    def loadFromNPCDict(self, npcDict):
        for f in npcDict.keys():
            if isinstance(npcDict[f], tuple):
                val = npcDict[f]
                exec 'f(self, ' + str(val)[1:]
            else:
                f(self, npcDict[f])

    def setTattooChest(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.tattooChest = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def setTattooZone2(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.tattooZone2 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def setTattooZone3(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.tattooZone3 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def setTattooZone4(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.tattooZone4 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def setTattooZone5(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.tattooZone5 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def setTattooZone6(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.tattooZone6 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def setTattooZone7(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.tattooZone7 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def setTattooZone8(self, tattoo, offsetX, offsetY, scale, rotate, color):
        self.tattooZone8 = [
         tattoo, offsetX, offsetY, scale, rotate, color]

    def setJewelryZone1(self, idx, primaryColor=0, secondaryColor=0):
        self.jewelryZone1 = [idx, primaryColor, secondaryColor]

    def setJewelryZone2(self, idx, primaryColor=0, secondaryColor=0):
        self.jewelryZone2 = [idx, primaryColor, secondaryColor]

    def setJewelryZone3(self, idx, primaryColor=0, secondaryColor=0):
        self.jewelryZone3 = [idx, primaryColor, secondaryColor]

    def setJewelryZone4(self, idx, primaryColor=0, secondaryColor=0):
        self.jewelryZone4 = [idx, primaryColor, secondaryColor]

    def setJewelryZone5(self, idx, primaryColor=0, secondaryColor=0):
        self.jewelryZone5 = [idx, primaryColor, secondaryColor]

    def setJewelryZone6(self, idx, primaryColor=0, secondaryColor=0):
        self.jewelryZone6 = [idx, primaryColor, secondaryColor]

    def setJewelryZone7(self, idx, primaryColor=0, secondaryColor=0):
        self.jewelryZone7 = [idx, primaryColor, secondaryColor]

    def setJewelryZone8(self, idx, primaryColor=0, secondaryColor=0):
        self.jewelryZone8 = [idx, primaryColor, secondaryColor]

    def setTutorial(self, val):
        self.tutorial = val

    def setName(self, val):
        self.name = val

    def setGender(self, val):
        self.gender = val

    def setBodyShape(self, val):
        self.body.shape = val

    def setBodyHeight(self, val):
        self.body.height = val

    def setBodyColor(self, val):
        self.body.color = val

    def setBodySkin(self, val):
        self.body.skin = val

    def setHeadSize(self, val):
        self.body.headSize = val

    def setHeadWidth(self, val):
        self.head.headWidth = val

    def setHeadHeight(self, val):
        self.head.headHeight = val

    def setHeadRoundness(self, val):
        self.head.headRoundness = val

    def setJawWidth(self, val):
        self.head.jawWidth = val

    def setJawRoundness(self, val):
        self.head.jawRoundness = val

    def setJawChinSize(self, val):
        self.head.jawChinSize = val

    def setJawAngle(self, val):
        self.head.jawAngle = val

    def setJawLength(self, val):
        self.head.jawLength = val

    def setMouthWidth(self, val):
        self.head.mouthWidth = val

    def setMouthLipThickness(self, val):
        self.head.mouthLipThickness = val

    def setMouthFrown(self, val):
        self.head.mouthFrown = val

    def setCheekBoneHeight(self, val):
        self.head.cheekBoneHeight = val

    def setCheekBoneWidth(self, val):
        self.head.cheekBoneWidth = val

    def setCheekFat(self, val):
        self.head.cheekFat = val

    def setBrowWidth(self, val):
        self.head.browWidth = val

    def setBrowProtruding(self, val):
        self.head.browProtruding = val

    def setBrowAngle(self, val):
        self.head.browAngle = val

    def setBrowHeight(self, val):
        self.head.browHeight = val

    def setEyeCorner(self, val):
        self.head.eyeCorner = val

    def setEyeOpeningSize(self, val):
        self.head.eyeOpeningSize = val

    def setEyeBulge(self, val):
        self.head.eyeBulge = val

    def setNoseBridgeWidth(self, val):
        self.head.noseBridgeWidth = val

    def setNoseNostrilWidth(self, val):
        self.head.noseNostrilWidth = val

    def setNoseLength(self, val):
        self.head.noseLength = val

    def setNoseBump(self, val):
        self.head.noseBump = val

    def setNoseNostrilHeight(self, val):
        self.head.noseNostrilHeight = val

    def setNoseNostrilAngle(self, val):
        self.head.noseNostrilAngle = val

    def setNoseNostrilIndent(self, val):
        self.head.noseNostrilIndent = val

    def setNoseBridgeBroke(self, val):
        self.head.noseBridgeBroke = val

    def setNoseNostrilBroke(self, val):
        self.head.noseNostrilBroke = val

    def setEarScale(self, val):
        self.head.earScale = val

    def setEarFlapAngle(self, val):
        self.head.earFlapAngle = val

    def setEarPosition(self, val):
        self.head.earPosition = val

    def setEarLobe(self, val):
        self.head.earLobe = val

    def setHeadTexture(self, val):
        self.head.texture = val

    def setHairHair(self, val):
        self.head.hair.hair = val

    def setHairBeard(self, val):
        self.head.hair.beard = val

    def setHairMustache(self, val):
        self.head.hair.mustache = val

    def setHairColor(self, val):
        self.head.hair.color = val

    def setHighLightColor(self, val):
        self.head.hair.highlight = val

    def setHat(self, val):
        self.clothes.hat = val

    def setHatIdx(self, val):
        self.clothes.hat = val

    def setHatColor(self, val):
        self.clothes.hatColor = val

    def setEyesColor(self, val):
        self.head.eyes.color = val

    def setClothesByType(self, type, val1, val2, val3):
        if type == 'HAT':
            self.clothes.hat = val1
            self.clothes.hatTexture = val2
            if val3 >= 0:
                self.clothes.hatColor = val3
        elif type == 'SHIRT':
            self.clothes.shirt = val1
            self.clothes.shirtTexture = val2
            if val3 >= 0:
                self.clothes.shirtColor = val3
        elif type == 'VEST':
            self.clothes.vest = val1
            self.clothes.vestTexture = val2
            if val3 >= 0:
                self.clothes.vestColor = val3
        elif type == 'COAT':
            self.clothes.coat = val1
            self.clothes.coatTexture = val2
            if val3 >= 0:
                self.clothes.coatColor = val3
        elif type == 'PANT':
            self.clothes.pant = val1
            self.clothes.pantTexture = val2
            if val3 >= 0:
                self.clothes.pantColor = val3
        elif type == 'BELT':
            self.clothes.belt = val1
            self.clothes.beltTexture = val2
            if val3 >= 0:
                self.clothes.sashColor = val3
        elif type == 'SHOE':
            self.clothes.shoe = val1
            self.clothes.shoeTexture = val2
            if val3 >= 0:
                self.clothes.shoeColor = val3

    def setClothesShirt(self, val1, val2=0):
        self.clothes.shirt = val1
        self.clothes.shirtTexture = val2

    def setClothesPant(self, val1, val2=0):
        self.clothes.pant = val1
        self.clothes.pantTexture = val2

    def setClothesHat(self, val1, val2=0):
        self.clothes.hat = val1
        self.clothes.hatTexture = val2

    def setHatTexture(self, val):
        self.clothes.hatTexture = val

    def setClothesSock(self, val1, val2=0):
        self.clothes.sock = val1
        self.clothes.sockTexture = val2

    def setClothesShoe(self, val1, val2=0):
        self.clothes.shoe = val1
        self.clothes.shoeTexture = val2

    def setClothesVest(self, val1, val2=0):
        self.clothes.vest = val1
        self.clothes.vestTexture = val2

    def setClothesCoat(self, val1, val2=0):
        self.clothes.coat = val1
        self.clothes.coatTexture = val2

    def setClothesBelt(self, val1, val2=0):
        self.clothes.belt = val1
        self.clothes.beltTexture = val2

    def setClothesTopColor(self, val1, val2, val3):
        self.clothes.shirtColor = val1
        self.clothes.vestColor = val2
        self.clothes.coatColor = val3

    def setClothesBotColor(self, val1, val2, val3):
        self.clothes.pantColor = val1
        self.clothes.sashColor = val2
        self.clothes.shoeColor = val3

    def getTattooChest(self):
        return self.tattooChest

    def getTattooZone2(self):
        return self.tattooZone2

    def getTattooZone3(self):
        return self.tattooZone3

    def getTattooZone4(self):
        return self.tattooZone4

    def getTattooZone5(self):
        return self.tattooZone5

    def getTattooZone6(self):
        return self.tattooZone6

    def getTattooZone7(self):
        return self.tattooZone7

    def getTattooZone8(self):
        return self.tattooZone8

    def getJewelryZone1(self):
        return self.jewelryZone1

    def getJewelryZone2(self):
        return self.jewelryZone2

    def getJewelryZone3(self):
        return self.jewelryZone3

    def getJewelryZone4(self):
        return self.jewelryZone4

    def getJewelryZone5(self):
        return self.jewelryZone5

    def getJewelryZone6(self):
        return self.jewelryZone6

    def getJewelryZone7(self):
        return self.jewelryZone7

    def getJewelryZone8(self):
        return self.jewelryZone8

    def getTutorial(self):
        if base.config.GetBool('ignore-teleport-requirements', False):
            return PiratesGlobals.TUT_GOT_COMPASS

        return self.tutorial

    def getDNAName(self):
        return self.name

    def getGender(self):
        return self.gender

    def getBodyShape(self):
        return self.body.shape

    def getBodyHeight(self):
        return self.body.height

    def getBodyColor(self):
        return self.body.color

    def getBodySkin(self):
        return self.body.skin

    def getHeadSize(self):
        return self.body.headSize

    def getHeadWidth(self):
        return self.head.headWidth

    def getHeadHeight(self):
        return self.head.headHeight

    def getHeadRoundness(self):
        return self.head.headRoundness

    def getJawWidth(self):
        return self.head.jawWidth

    def getJawRoundness(self):
        return self.head.jawRoundness

    def getJawChinSize(self):
        return self.head.jawChinSize

    def getJawAngle(self):
        return self.head.jawAngle

    def getJawLength(self):
        return self.head.jawLength

    def getMouthWidth(self):
        return self.head.mouthWidth

    def getMouthLipThickness(self):
        return self.head.mouthLipThickness

    def getMouthFrown(self):
        return self.head.mouthFrown

    def getCheekBoneHeight(self):
        return self.head.cheekBoneHeight

    def getCheekBoneWidth(self):
        return self.head.cheekBoneWidth

    def getCheekFat(self):
        return self.head.cheekFat

    def getBrowWidth(self):
        return self.head.browWidth

    def getBrowProtruding(self):
        return self.head.browProtruding

    def getBrowAngle(self):
        return self.head.browAngle

    def getBrowHeight(self):
        return self.head.browHeight

    def getEyeCorner(self):
        return self.head.eyeCorner

    def getEyeOpeningSize(self):
        return self.head.eyeOpeningSize

    def getEyeBulge(self):
        return self.head.eyeBulge

    def getNoseBridgeWidth(self):
        return self.head.noseBridgeWidth

    def getNoseNostrilWidth(self):
        return self.head.noseNostrilWidth

    def getNoseLength(self):
        return self.head.noseLength

    def getNoseBump(self):
        return self.head.noseBump

    def getNoseNostrilHeight(self):
        return self.head.noseNostrilHeight

    def getNoseNostrilAngle(self):
        return self.head.noseNostrilAngle

    def getNoseNostrilIndent(self):
        return self.head.noseNostrilIndent

    def getNoseBridgeBroke(self):
        return self.head.noseBridgeBroke

    def getNoseNostrilBroke(self):
        return self.head.noseNostrilBroke

    def getEarScale(self):
        return self.head.earScale

    def getEarFlapAngle(self):
        return self.head.earFlapAngle

    def getEarPosition(self):
        return self.head.earPosition

    def getEarLobe(self):
        return self.head.earLobe

    def getHeadTexture(self):
        return self.head.texture

    def getHairHair(self):
        return self.head.hair.hair

    def getHairBeard(self):
        return self.head.hair.beard

    def getHairMustache(self):
        return self.head.hair.mustache

    def getHairColor(self):
        return self.head.hair.color

    def getHighLightColor(self):
        return self.head.hair.highlight

    def getHatIdx(self):
        return self.clothes.hat

    def getHat(self):
        return self.clothes.hat

    def getHatTexture(self):
        return self.clothes.hatTexture

    def getHatColor(self):
        return self.clothes.hatColor

    def getEyesColor(self):
        return self.head.eyes.color

    def verifyClothing(self, type, modelId, texId):
        if (
         self.gender, type, modelId, texId) in ClothingGlobals.quickConfirmSet:
            return [modelId, texId]
        elif self.gender == 'm' or self.gender == 'f':
            return [0, 0]
        else:
            return [
             modelId, texId]

    def getClothesShirt(self):
        return self.verifyClothing('SHIRT', self.clothes.shirt, self.clothes.shirtTexture)

    def getClothesPant(self):
        return self.verifyClothing('PANT', self.clothes.pant, self.clothes.pantTexture)

    def getClothesHat(self):
        return self.verifyClothing('HAT', self.clothes.hat, self.clothes.hatTexture)

    def getClothesSock(self):
        return [
         self.clothes.sock, self.clothes.sockTexture]

    def getClothesShoe(self):
        return self.verifyClothing('SHOE', self.clothes.shoe, self.clothes.shoeTexture)

    def getClothesVest(self):
        return self.verifyClothing('VEST', self.clothes.vest, self.clothes.vestTexture)

    def getClothesCoat(self):
        return self.verifyClothing('COAT', self.clothes.coat, self.clothes.coatTexture)

    def getClothesBelt(self):
        return self.verifyClothing('BELT', self.clothes.belt, self.clothes.beltTexture)

    def getClothesTopColor(self):
        return [
         self.clothes.shirtColor, self.clothes.vestColor, self.clothes.coatColor]

    def getClothesBotColor(self):
        return [
         self.clothes.pantColor, self.clothes.sashColor, self.clothes.shoeColor]

    def defaultColor(self):
        return 0

    def __defaultColors(self):
        self.hairColor = 1
        self.hairColor = 2
        self.skinColor = 0

    def setNPCType(self):
        self.type = 'npc'

    def getType(self):
        return self.type

    def getBuild(self):
        if self.model[0] == 'sf':
            return 'short fat'
        elif self.model[0] == 'ms':
            return 'medium skinny'
        elif self.model[0] == 'mi':
            return 'medium ideal'
        elif self.model[0] == 'tp':
            return 'tall pear'
        elif self.model[0] == 'tm':
            return 'tall muscular'
        else:
            notify.error('unknown modelStyle: ', self.model[0])

    def getGender(self):
        return self.gender

    def lookupHairColor(self):
        try:
            return hairColors[self.head.hair.color]
        except:
            return hairColors[0]

    def lookupHatColor(self):
        idx = 0
        if self.gender == 'f':
            idx = 1
        try:
            return DYE_COLORS[self.color.hatColor]
        except:
            return DYE_COLORS[0]

    def lookupClothesTopColor(self):
        idx = 0
        if self.gender == 'f':
            idx = 1
        try:
            return [
             DYE_COLORS[self.clothes.shirtColor], DYE_COLORS[self.clothes.vestColor], DYE_COLORS[self.clothes.coatColor]]
        except:
            return [
             DYE_COLORS[0], DYE_COLORS[5], DYE_COLORS[10]]

    def lookupClothesBotColor(self):
        idx = 0
        if self.gender == 'f':
            idx = 1
        try:
            return [
             DYE_COLORS[self.clothes.pantColor], DYE_COLORS[self.clothes.sashColor], DYE_COLORS[self.clothes.shoeColor]]
        except:
            return [
             DYE_COLORS[0], DYE_COLORS[7], DYE_COLORS[12]]

    def getHairBaseColor(self):
        try:
            return hairColors[self.getHairColor()]
        except:
            return hairColors[0]

    def getHairHighLightColor(self):
        try:
            return hairHighLightColors[self.getHighLightColor()]
        except:
            return hairHighLightColors[0]

    def getSkinColor(self):
        try:
            return skinColors[self.body.color]
        except:
            return skinColors[0]

    def getColor(self, index):
        try:
            return hairColors[index]
        except:
            return hairColors[0]

    def tossAValue(self, random, clip=0.5, negative=True):
        value = 0.0
        value = random.random()
        if value > clip:
            value = clip
        if negative:
            toss = random.choice([0, 1])
            if toss:
                value = -value
        return value

    def makeNPCPirate(self, seed=None, gender='m'):
        if seed:
            randomGen = random.Random()
            randomGen.seed(seed)
        else:
            randomGen = random
        colors = range(len(DYE_COLORS))
        self.gender = randomGen.choice(['m', 'f'])
        if self.gender == 'm':
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesMale)
            self.body.color = 0
            self.clothes.shirt = 6
            self.clothes.shirtColor = randomGen.choice(colors)
            self.clothes.pant = 1
            self.clothes.pantColor = randomGen.choice(colors)
            self.clothes.sock = 0
            self.clothes.shoe = 1
            self.clothes.belt = 0
            self.clothes.coat = randomGen.choice(range(3))
            self.clothes.coatColor = randomGen.choice(colors)
            self.head.texture = 0
            self.clothes.hat = randomGen.choice(range(5))
            self.head.hair.hair = randomGen.choice([1, 2, 3, 4, 5, 6])
            self.head.hair.beard = randomGen.choice(range(11))
            self.head.hair.mustache = randomGen.choice([0, 1, 2, 4])
            self.head.hair.color = randomGen.choice(range(5))
        else:
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesFemale)
            self.body.color = 0
            self.clothes.shirt = randomGen.choice([3, 4, 5])
            self.clothes.shirtColor = randomGen.choice(colors)
            self.clothes.pant = randomGen.choice([0, 2])
            self.clothes.pantColor = randomGen.choice(colors)
            self.clothes.sock = 0
            self.clothes.shoe = randomGen.choice([1, 2, 3, 4])
            self.clothes.belt = 0
            self.clothes.coat = randomGen.choice(range(3))
            self.clothes.coatColor = randomGen.choice(colors)
            self.clothes.hat = randomGen.choice(range(5))
            self.clothes.hatColor = randomGen.choice(colors)
            self.head.hair.hair = randomGen.choice(range(16))
            self.head.hair.color = randomGen.choice(range(5))

    def makeNPCGhost(self, seed=None, gender='m', wantConquistadorHat=False):
        if seed:
            randomGen = random.Random()
            randomGen.seed(seed)
        else:
            randomGen = random
        colors = range(len(DYE_COLORS))
        self.gender = randomGen.choice(['m', 'm', 'f'])
        if self.gender == 'm':
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesMale)
            self.body.color = 0
            self.clothes.shirt = 6
            self.clothes.shirtColor = randomGen.choice(colors)
            self.clothes.pant = 1
            self.clothes.pantColor = randomGen.choice(colors)
            self.clothes.sock = 0
            self.clothes.shoe = 1
            self.clothes.belt = 0
            self.clothes.coat = randomGen.choice(range(3))
            self.clothes.coatColor = randomGen.choice(colors)
            self.head.texture = 0
            if wantConquistadorHat:
                self.clothes.hat = 20
            else:
                self.clothes.hat = randomGen.choice(range(5))
            self.head.hair.hair = randomGen.choice([1, 2, 3, 4, 5, 6])
            self.head.hair.beard = randomGen.choice(range(11))
            self.head.hair.mustache = randomGen.choice([0, 1, 2, 4])
            self.head.hair.color = randomGen.choice(range(5))
        else:
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesFemale)
            self.body.color = 0
            self.clothes.shirt = randomGen.choice([3, 4, 5])
            self.clothes.shirtColor = randomGen.choice(colors)
            self.clothes.pant = randomGen.choice([0, 2])
            self.clothes.pantColor = randomGen.choice(colors)
            self.clothes.sock = 0
            self.clothes.shoe = randomGen.choice([1, 2, 3, 4])
            self.clothes.belt = 0
            self.clothes.coat = randomGen.choice(range(3))
            self.clothes.coatColor = randomGen.choice(colors)
            if wantConquistadorHat:
                self.clothes.hat = 17
            self.head.hair.hair = randomGen.choice(range(16))
            self.head.hair.color = randomGen.choice(range(5))

    def makeNPCZombie(self, seed=None, gender='m'):
        if seed:
            randomGen = random.Random()
            randomGen.seed(seed)
        else:
            randomGen = random
        colors = [0, 0, 0, 0, 0, 0, 0, 0, 7, 14, 30, 35, 36, 44]
        self.gender = randomGen.choice(['m', 'm', 'f'])
        if self.gender == 'm':
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesMale)
            self.body.color = 0
            self.clothes.shirt = 6
            self.clothes.shirtColor = randomGen.choice(colors)
            self.clothes.pant = 1
            self.clothes.pantColor = randomGen.choice(colors)
            self.clothes.sock = 0
            self.clothes.shoe = 1
            self.clothes.belt = 0
            self.clothes.coat = randomGen.choice(range(3))
            self.clothes.coatColor = randomGen.choice(colors)
            self.head.texture = 0
            self.clothes.hat = randomGen.choice(range(5))
            self.head.hair.hair = randomGen.choice([1, 2, 3, 4, 5, 6])
            self.head.hair.beard = randomGen.choice(range(11))
            self.head.hair.mustache = randomGen.choice([0, 1, 2, 4])
            self.head.hair.color = randomGen.choice(range(5))
        else:
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesFemale)
            self.body.color = 0
            self.clothes.shirt = randomGen.choice([3, 4, 5])
            self.clothes.shirtColor = randomGen.choice(colors)
            self.clothes.pant = randomGen.choice([0, 2])
            self.clothes.pantColor = randomGen.choice(colors)
            self.clothes.sock = 0
            self.clothes.shoe = randomGen.choice([1, 2, 3, 4])
            self.clothes.belt = 0
            self.clothes.coat = randomGen.choice(range(3))
            self.clothes.coatColor = randomGen.choice(colors)
            self.head.hair.hair = randomGen.choice(range(16))
            self.head.hair.color = randomGen.choice(range(5))

    def makeNPCBountyHunter(self, seed=None, gender='m'):
        if seed:
            randomGen = random.Random()
            randomGen.seed(seed)
        else:
            randomGen = random
        colors = [0, 0, 0, 0, 0, 0, 0, 0, 7, 14, 30, 35, 36, 44]
        self.gender = randomGen.choice(['m', 'm', 'f'])
        if self.gender == 'm':
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesMale)
            self.body.color = 0
            self.clothes.shirt = 6
            self.clothes.shirtColor = randomGen.choice(colors)
            self.clothes.pant = 1
            self.clothes.pantColor = randomGen.choice(colors)
            self.clothes.sock = 0
            self.clothes.shoe = 1
            self.clothes.belt = 0
            self.clothes.coat = randomGen.choice(range(3))
            self.clothes.coatColor = randomGen.choice(colors)
            self.head.texture = 0
            self.clothes.hat = randomGen.choice([15, 17, 18])
            self.head.hair.hair = randomGen.choice([1, 2, 3, 4, 5, 6])
            self.head.hair.beard = randomGen.choice(range(11))
            self.head.hair.mustache = randomGen.choice([0, 1, 2, 4])
            self.head.hair.color = randomGen.choice(range(5))
        else:
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesFemale)
            self.body.color = 0
            self.clothes.shirt = randomGen.choice([3, 4, 5])
            self.clothes.shirtColor = randomGen.choice(colors)
            self.clothes.pant = randomGen.choice([0, 2])
            self.clothes.pantColor = randomGen.choice(colors)
            self.clothes.sock = 0
            self.clothes.shoe = randomGen.choice([1, 2, 3, 4])
            self.clothes.belt = 0
            self.clothes.coat = randomGen.choice(range(3))
            self.clothes.coatColor = randomGen.choice(colors)
            self.clothes.hat = randomGen.choice([12, 14, 15])
            self.head.hair.hair = randomGen.choice(range(16))
            self.head.hair.color = randomGen.choice(range(5))

    def makeNPCTownfolk(self, seed=None, gender='m'):
        if seed:
            randomGen = random.Random()
            randomGen.seed(seed)
        else:
            randomGen = random
        colors = range(len(DYE_COLORS))
        self.gender = gender
        if self.gender == 'm':
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesMale)
            self.body.color = 0
            self.clothes.shirt = 6
            self.clothes.shirtColor = randomGen.choice(colors)
            self.clothes.pant = 1
            self.clothes.pantColor = randomGen.choice(colors)
            self.clothes.sock = 0
            self.clothes.shoe = 1
            self.clothes.belt = 0
            self.clothes.coat = randomGen.choice(range(3))
            self.clothes.coatColor = randomGen.choice(colors)
            self.head.texture = 0
            self.clothes.hat = randomGen.choice([15, 17, 18])
            self.head.hair.hair = randomGen.choice([1, 2, 3, 4, 5, 6])
            self.head.hair.beard = randomGen.choice(range(11))
            self.head.hair.mustache = randomGen.choice([0, 1, 2, 4])
            self.head.hair.color = randomGen.choice(range(5))
        else:
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesFemale)
            self.body.color = 0
            self.clothes.shirt = randomGen.choice([3, 4, 5])
            self.clothes.shirtColor = randomGen.choice(colors)
            self.clothes.pant = randomGen.choice([0, 2])
            self.clothes.pantColor = randomGen.choice(colors)
            self.clothes.sock = 0
            self.clothes.shoe = randomGen.choice([1, 2, 3, 4])
            self.clothes.belt = 0
            self.clothes.coat = randomGen.choice(range(3))
            self.clothes.coatColor = randomGen.choice(colors)
            self.clothes.hat = randomGen.choice([12, 14, 15])
            self.head.hair.hair = randomGen.choice(range(16))
            self.head.hair.color = randomGen.choice(range(5))

    def makeNPCDealer(self, seed=None, gender='m'):
        if seed:
            randomGen = random.Random()
            randomGen.seed(seed)
        else:
            randomGen = random
        self.gender = gender
        if self.gender == 'm':
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesMale)
            self.body.color = randomGen.choice([0, 7])
            self.clothes.shirt = 6
            self.clothes.vest = 0
            self.clothes.pant = 1
            self.clothes.sock = 0
            self.clothes.shoe = 2
            self.clothes.belt = 1
            self.head.texture = 0
            self.head.hair.hair = randomGen.choice([1, 2, 3, 4, 5, 6])
            self.head.hair.beard = randomGen.choice(range(11))
            self.head.hair.mustache = randomGen.choice([0, 1, 2, 4])
            self.head.hair.color = randomGen.choice(range(5))
        else:
            self.body.shape = randomGen.choice(BodyDefs.BodyChoicesFemale)
            self.body.color = randomGen.choice([0, 7])
            self.clothes.shirt = 6
            self.clothes.vest = 0
            self.clothes.pant = 1
            self.clothes.sock = 0
            self.clothes.shoe = 2
            self.clothes.belt = 1
            self.head.hair.hair = randomGen.choice(range(16))
            self.head.hair.color = randomGen.choice(range(5))

    def makeNPCNavySailor(self, seed=None, gender='m'):
        if seed:
            randomGen = random.Random()
            randomGen.seed(seed)
        else:
            randomGen = random
        self.gender = 'n'
        self.body.color = randomGen.choice([0, 2, 3, 5, 8])
        self.body.shape = randomGen.choice(BodyDefs.BodyChoicesNeutral)
        self.body.height = randomGen.choice([-0.3, 0.0, 0.3, 0.6])
        self.body.headSize = -0.3 + randomGen.random() * 0.6
        self.clothes.shirt = 0
        self.clothes.shirtTexture = 0
        self.clothes.vest = 0
        self.clothes.coat = 3
        self.clothes.coatColor = 0
        self.clothes.pant = 4
        self.clothes.pantTexture = 0
        self.clothes.pantColor = 0
        self.clothes.sock = 0
        self.clothes.shoe = 3
        self.clothes.belt = 0
        self.head.texture = randomGen.choice([0, 1, 4])
        self.head.jawWidth = self.tossAValue(randomGen, 1.0)
        self.head.jawLength = self.tossAValue(randomGen, 1.0)
        self.head.jawChinSize = self.tossAValue(randomGen, 1.0)
        self.head.jawAngle = self.tossAValue(randomGen, 1.0)
        self.head.cheekFat = self.tossAValue(randomGen, 1.0)
        self.head.browProtruding = self.tossAValue(randomGen, 1.0, False)
        self.head.eyeBulge = self.tossAValue(randomGen, 1.0)
        self.head.noseBridgeWidth = self.tossAValue(randomGen, 1.0)
        self.head.noseNostrilWidth = self.tossAValue(randomGen, 1.0)
        self.head.noseLength = self.tossAValue(randomGen, 1.0)
        self.head.noseBump = self.tossAValue(randomGen)
        self.head.noseNostrilHeight = self.tossAValue(randomGen, 1.0)
        self.head.noseNostrilAngle = self.tossAValue(randomGen, 1.0)
        self.head.earScale = self.tossAValue(randomGen)
        self.head.earFlapAngle = self.tossAValue(randomGen)
        self.head.earPosition = self.tossAValue(randomGen)
        self.head.hair.hair = randomGen.choice([1, 9])
        self.head.hair.beard = randomGen.choice([0, 7, 9])
        self.head.hair.mustache = randomGen.choice([0, 1, 2])
        self.head.hair.color = randomGen.choice([0, 1, 2, 3, 4, 5, 6, 7])
        self.head.eyes.color = randomGen.choice([0, 1, 2, 3, 4, 5])
        self.clothes.hat = 3
        self.clothes.hatColor = 0

    def makeNPCIndiaNavySailor(self, seed=None, gender='m'):
        if seed:
            randomGen = random.Random()
            randomGen.seed(seed)
        else:
            randomGen = random
        self.head.hair.hair = 1
        self.gender = 'n'
        self.body.color = randomGen.choice([0, 2, 3, 5, 8])
        self.body.shape = randomGen.choice(BodyDefs.BodyChoicesNeutral)
        self.body.height = randomGen.choice([0.0, 0.3, 0.6])
        self.body.headSize = -0.3 + randomGen.random() * 0.6
        self.clothes.shirt = 0
        self.clothes.vest = 0
        self.clothes.coat = 4
        self.clothes.coatColor = 0
        self.clothes.pant = 5
        self.clothes.pantColor = 0
        self.clothes.sock = 0
        self.clothes.shoe = 4
        self.clothes.belt = 0
        self.head.texture = randomGen.choice([0, 1, 4])
        self.head.jawWidth = self.tossAValue(randomGen, 1.0)
        self.head.jawLength = self.tossAValue(randomGen, 1.0)
        self.head.jawChinSize = self.tossAValue(randomGen, 1.0)
        self.head.jawAngle = self.tossAValue(randomGen, 1.0)
        self.head.cheekFat = self.tossAValue(randomGen, 1.0)
        self.head.browProtruding = self.tossAValue(randomGen, 1.0, False)
        self.head.eyeBulge = self.tossAValue(randomGen, 1.0)
        self.head.noseBridgeWidth = self.tossAValue(randomGen, 1.0)
        self.head.noseNostrilWidth = self.tossAValue(randomGen, 1.0)
        self.head.noseLength = self.tossAValue(randomGen, 1.0)
        self.head.noseBump = self.tossAValue(randomGen)
        self.head.noseNostrilHeight = self.tossAValue(randomGen, 1.0)
        self.head.noseNostrilAngle = self.tossAValue(randomGen, 1.0)
        self.head.earScale = self.tossAValue(randomGen)
        self.head.earFlapAngle = self.tossAValue(randomGen)
        self.head.earPosition = self.tossAValue(randomGen)
        self.head.hair.hair = randomGen.choice([1, 9])
        self.head.hair.beard = randomGen.choice([0, 7, 9])
        self.head.hair.mustache = randomGen.choice([0, 1, 2])
        self.head.hair.color = randomGen.choice([0, 1, 2, 3, 4, 5, 6, 7])
        self.head.eyes.color = randomGen.choice([0, 1, 2, 3, 4, 5])
        self.clothes.hat = 4
        self.clothes.hatColor = 0

    def makeLeadingMan(self):
        self.gender = 'm'
        self.height = 0.8
        self.head.headWidth = 0
        self.head.headHeight = 0
        self.head.headRoundness = 0
        self.head.mouthFrown = 0.36
        self.body.shape = BodyDefs.BodyChoicesMale[2]
        self.body.color = 4
        self.clothes.shirt = 6
        self.clothes.shirtColor = 0
        self.clothes.pant = 1
        self.clothes.pantColor = 11
        self.clothes.sock = 0
        self.clothes.shoe = 2
        self.clothes.belt = 0
        self.clothes.coat = 2
        self.clothes.coatColor = 14
        self.clothes.vest = 0
        self.clothes.vestColor = 12
        self.head.eyes.color = 0
        self.head.texture = 0
        self.clothes.hat = 0
        self.clothes.hatColor = 4
        self.head.hair.hair = 6
        self.head.hair.beard = 5
        self.head.hair.mustache = 4
        self.head.hair.color = 2

    def makeNetString(self):
        dg = PyDatagram()

        # Gender
        dg.addUint8(self.gender == 'm')

        # Body
        dg.addUint8(self.body.shape)
        dg.addFloat64(self.body.height)
        dg.addUint8(self.body.color)
        dg.addUint8(self.body.skin)

        # Head
        dg.addFloat64(self.body.headSize)
        dg.addFloat64(self.head.headWidth)
        dg.addFloat64(self.head.headHeight)
        dg.addFloat64(self.head.headRoundness)

        # Jaw
        dg.addFloat64(self.head.jawWidth)
        dg.addFloat64(self.head.jawRoundness)
        dg.addFloat64(self.head.jawChinSize)
        dg.addFloat64(self.head.jawAngle)
        dg.addFloat64(self.head.jawLength)

        # Mouth
        dg.addFloat64(self.head.mouthWidth)
        dg.addFloat64(self.head.mouthLipThickness)
        dg.addFloat64(self.head.mouthFrown)

        # Cheek
        dg.addFloat64(self.head.cheekBoneHeight)
        dg.addFloat64(self.head.cheekBoneWidth)
        dg.addFloat64(self.head.cheekFat)

        # Brow
        dg.addFloat64(self.head.browWidth)
        dg.addFloat64(self.head.browProtruding)
        dg.addFloat64(self.head.browAngle)
        dg.addFloat64(self.head.browHeight)

        # Eye
        dg.addFloat64(self.head.eyeCorner)
        dg.addFloat64(self.head.eyeOpeningSize)
        dg.addFloat64(self.head.eyeBulge)

        # Nose
        dg.addFloat64(self.head.noseBridgeWidth)
        dg.addFloat64(self.head.noseNostrilWidth)
        dg.addFloat64(self.head.noseLength)
        dg.addFloat64(self.head.noseBump)
        dg.addFloat64(self.head.noseNostrilHeight)
        dg.addFloat64(self.head.noseNostrilAngle)
        dg.addFloat64(self.head.noseNostrilIndent)
        dg.addFloat64(self.head.noseBridgeBroke)
        dg.addFloat64(self.head.noseNostrilBroke)

        # Ear
        dg.addFloat64(self.head.earScale)
        dg.addFloat64(self.head.earFlapAngle)
        dg.addFloat64(self.head.earPosition)
        dg.addFloat64(self.head.earLobe)

        # Hair
        dg.addUint8(self.head.texture)
        dg.addUint8(self.head.hair.hair)
        dg.addUint8(self.head.hair.beard)
        dg.addUint8(self.head.hair.mustache)
        dg.addUint8(self.head.hair.color)
        dg.addUint8(self.head.hair.highlight)

        # Eye 2
        dg.addUint8(self.head.eyes.color)

        # Clothes
        dg.addUint8(self.clothes.hat)
        dg.addUint8(self.clothes.hatTexture)
        dg.addUint8(self.clothes.shirt)
        dg.addUint8(self.clothes.shirtTexture)
        dg.addUint8(self.clothes.pant)
        dg.addUint8(self.clothes.pantTexture)
        dg.addUint8(self.clothes.sock)
        dg.addUint8(self.clothes.sockTexture)
        dg.addUint8(self.clothes.shoe)
        dg.addUint8(self.clothes.shoeTexture)
        dg.addUint8(self.clothes.vest)
        dg.addUint8(self.clothes.vestTexture)
        dg.addUint8(self.clothes.coat)
        dg.addUint8(self.clothes.coatTexture)
        dg.addUint8(self.clothes.belt)
        dg.addUint8(self.clothes.beltTexture)

        # Clothes color
        dg.addUint8(self.clothes.shirtColor)
        dg.addUint8(self.clothes.vestColor)
        dg.addUint8(self.clothes.coatColor)
        dg.addUint8(self.clothes.pantColor)
        dg.addUint8(self.clothes.sashColor)
        dg.addUint8(self.clothes.shoeColor)

        # Tattoo
        dg.addUint8(self.tattooChest[0])
        dg.addFloat64(self.tattooChest[1])
        dg.addFloat64(self.tattooChest[2])
        dg.addUint8(self.tattooChest[3])
        dg.addUint8(self.tattooChest[4])
        dg.addUint8(self.tattooChest[5])
        dg.addUint8(self.tattooZone2[0])
        dg.addFloat64(self.tattooZone2[1])
        dg.addFloat64(self.tattooZone2[2])
        dg.addUint8(self.tattooZone2[3])
        dg.addUint8(self.tattooZone2[4])
        dg.addUint8(self.tattooZone2[5])
        dg.addUint8(self.tattooZone3[0])
        dg.addFloat64(self.tattooZone3[1])
        dg.addFloat64(self.tattooZone3[2])
        dg.addUint8(self.tattooZone3[3])
        dg.addUint8(self.tattooZone3[4])
        dg.addUint8(self.tattooZone3[5])
        dg.addUint8(self.tattooZone4[0])
        dg.addFloat64(self.tattooZone4[1])
        dg.addFloat64(self.tattooZone4[2])
        dg.addUint8(self.tattooZone4[3])
        dg.addUint8(self.tattooZone4[4])
        dg.addUint8(self.tattooZone4[5])
        dg.addUint8(self.tattooZone5[0])
        dg.addFloat64(self.tattooZone5[1])
        dg.addFloat64(self.tattooZone5[2])
        dg.addUint8(self.tattooZone5[3])
        dg.addUint8(self.tattooZone5[4])
        dg.addUint8(self.tattooZone5[5])
        dg.addUint8(self.tattooZone6[0])
        dg.addFloat64(self.tattooZone6[1])
        dg.addFloat64(self.tattooZone6[2])
        dg.addUint8(self.tattooZone6[3])
        dg.addUint8(self.tattooZone6[4])
        dg.addUint8(self.tattooZone6[5])
        dg.addUint8(self.tattooZone7[0])
        dg.addFloat64(self.tattooZone7[1])
        dg.addFloat64(self.tattooZone7[2])
        dg.addUint8(self.tattooZone7[3])
        dg.addUint8(self.tattooZone7[4])
        dg.addUint8(self.tattooZone7[5])
        dg.addUint8(self.tattooZone8[0])
        dg.addFloat64(self.tattooZone8[1])
        dg.addFloat64(self.tattooZone8[2])
        dg.addUint8(self.tattooZone8[3])
        dg.addUint8(self.tattooZone8[4])
        dg.addUint8(self.tattooZone8[5])

        # Jewelry
        dg.addUint8(self.jewelryZone1[0])
        dg.addUint8(self.jewelryZone1[1])
        dg.addUint8(self.jewelryZone1[2])
        dg.addUint8(self.jewelryZone2[0])
        dg.addUint8(self.jewelryZone2[1])
        dg.addUint8(self.jewelryZone2[2])
        dg.addUint8(self.jewelryZone3[0])
        dg.addUint8(self.jewelryZone3[1])
        dg.addUint8(self.jewelryZone3[2])
        dg.addUint8(self.jewelryZone4[0])
        dg.addUint8(self.jewelryZone4[1])
        dg.addUint8(self.jewelryZone4[2])
        dg.addUint8(self.jewelryZone5[0])
        dg.addUint8(self.jewelryZone5[1])
        dg.addUint8(self.jewelryZone5[2])
        dg.addUint8(self.jewelryZone6[0])
        dg.addUint8(self.jewelryZone6[1])
        dg.addUint8(self.jewelryZone6[2])
        dg.addUint8(self.jewelryZone7[0])
        dg.addUint8(self.jewelryZone7[1])
        dg.addUint8(self.jewelryZone7[2])
        dg.addUint8(self.jewelryZone8[0])
        dg.addUint8(self.jewelryZone8[1])
        dg.addUint8(self.jewelryZone8[2])
        return dg.getMessage()

    def makeFromNetString(self, netString):
        dg = PyDatagram(netString)
        dgi = PyDatagramIterator(dg)

        # Gender
        self.setGender('m' if dgi.getUint8() else 'f')

        # Body
        self.setBodyShape(dgi.getUint8())
        self.setBodyHeight(dgi.getFloat64())
        self.setBodyColor(dgi.getUint8())
        self.setBodySkin(dgi.getUint8())

        # Head
        self.setHeadSize(dgi.getFloat64())
        self.setHeadWidth(dgi.getFloat64())
        self.setHeadHeight(dgi.getFloat64())
        self.setHeadRoundness(dgi.getFloat64())

        # Jaw
        self.setJawWidth(dgi.getFloat64())
        self.setJawRoundness(dgi.getFloat64())
        self.setJawChinSize(dgi.getFloat64())
        self.setJawAngle(dgi.getFloat64())
        self.setJawLength(dgi.getFloat64())

        # Mouth
        self.setMouthWidth(dgi.getFloat64())
        self.setMouthLipThickness(dgi.getFloat64())
        self.setMouthFrown(dgi.getFloat64())

        # Cheek
        self.setCheekBoneHeight(dgi.getFloat64())
        self.setCheekBoneWidth(dgi.getFloat64())
        self.setCheekFat(dgi.getFloat64())

        # Brow
        self.setBrowWidth(dgi.getFloat64())
        self.setBrowProtruding(dgi.getFloat64())
        self.setBrowAngle(dgi.getFloat64())
        self.setBrowHeight(dgi.getFloat64())

        # Eye
        self.setEyeCorner(dgi.getFloat64())
        self.setEyeOpeningSize(dgi.getFloat64())
        self.setEyeBulge(dgi.getFloat64())

        # Nose
        self.setNoseBridgeWidth(dgi.getFloat64())
        self.setNoseNostrilWidth(dgi.getFloat64())
        self.setNoseLength(dgi.getFloat64())
        self.setNoseBump(dgi.getFloat64())
        self.setNoseNostrilHeight(dgi.getFloat64())
        self.setNoseNostrilAngle(dgi.getFloat64())
        self.setNoseNostrilIndent(dgi.getFloat64())
        self.setNoseBridgeBroke(dgi.getFloat64())
        self.setNoseNostrilBroke(dgi.getFloat64())

        # Ear
        self.setEarScale(dgi.getFloat64())
        self.setEarFlapAngle(dgi.getFloat64())
        self.setEarPosition(dgi.getFloat64())
        self.setEarLobe(dgi.getFloat64())

        # Hair
        self.setHeadTexture(dgi.getUint8())
        self.setHairHair(dgi.getUint8())
        self.setHairBeard(dgi.getUint8())
        self.setHairMustache(dgi.getUint8())
        self.setHairColor(dgi.getUint8())
        self.setHighLightColor(dgi.getUint8())

        # Eye 2
        self.setEyesColor(dgi.getUint8())

        # Clothes
        self.setClothesHat(dgi.getUint8(), dgi.getUint8())
        self.setClothesShirt(dgi.getUint8(), dgi.getUint8())
        self.setClothesPant(dgi.getUint8(), dgi.getUint8())
        self.setClothesSock(dgi.getUint8(), dgi.getUint8())
        self.setClothesShoe(dgi.getUint8(), dgi.getUint8())
        self.setClothesVest(dgi.getUint8(), dgi.getUint8())
        self.setClothesCoat(dgi.getUint8(), dgi.getUint8())
        self.setClothesBelt(dgi.getUint8(), dgi.getUint8())

        # Clothes color
        self.setClothesTopColor(dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setClothesBotColor(dgi.getUint8(), dgi.getUint8(), dgi.getUint8())

        # Tattoo
        self.setTattooChest(dgi.getUint8(), dgi.getFloat64(), dgi.getFloat64(), dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setTattooZone2(dgi.getUint8(), dgi.getFloat64(), dgi.getFloat64(), dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setTattooZone3(dgi.getUint8(), dgi.getFloat64(), dgi.getFloat64(), dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setTattooZone4(dgi.getUint8(), dgi.getFloat64(), dgi.getFloat64(), dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setTattooZone5(dgi.getUint8(), dgi.getFloat64(), dgi.getFloat64(), dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setTattooZone6(dgi.getUint8(), dgi.getFloat64(), dgi.getFloat64(), dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setTattooZone7(dgi.getUint8(), dgi.getFloat64(), dgi.getFloat64(), dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setTattooZone8(dgi.getUint8(), dgi.getFloat64(), dgi.getFloat64(), dgi.getUint8(), dgi.getUint8(), dgi.getUint8())

        # Jewelry
        self.setJewelryZone1(dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setJewelryZone2(dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setJewelryZone3(dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setJewelryZone4(dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setJewelryZone5(dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setJewelryZone6(dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setJewelryZone7(dgi.getUint8(), dgi.getUint8(), dgi.getUint8())
        self.setJewelryZone8(dgi.getUint8(), dgi.getUint8(), dgi.getUint8())

        assert dgi.getRemainingSize() == 0

    @classmethod
    def isValidNetString(cls, netString):
        return len(netString) == len(cls().makeNetString())
