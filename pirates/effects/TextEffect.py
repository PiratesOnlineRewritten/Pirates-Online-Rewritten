from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PLocalizer
from pandac.PandaModules import *
from otp.otpbase import OTPRender
from pirates.piratesbase import Freebooter
from pirates.piratesbase import PiratesGlobals
from pirates.inventory import ItemGlobals
from pirates.inventory import ItemConstants
import random
import weakref
MOD_TYPE_MULTIPLE = 0
MOD_TYPE_MULTIPLE_COMPACT = 1
MOD_TYPE_SEQUENTIAL = 2
MOD_TYPE_SEQUENTIAL_CONTINUOUS = 3
MOD_TYPE_SEQUENTIAL_COMPACT = 4
MOD_TYPE_TOTAL = 5
MOD_BASICPENALTY = 0
MOD_CREWBONUS = 1
MOD_2XPBONUS = 2
MOD_HOLIDAYBONUS = 3
MOD_POTIONBONUS = 4

def genText(value, type, modType=MOD_TYPE_MULTIPLE, modifiers={}, effects={}):
    if value < 0:
        finalText = '%s'
        baseVal = value
    else:
        if type == 4:
            finalText = '+%s ' + PLocalizer.EXP
            baseVal = value
        else:
            if type == 5:
                finalText = PLocalizer.ChatPanelQuestCompletedMsg + '\n +%s ' + PLocalizer.EXP
                baseVal = value
            else:
                if type == 7:
                    finalText = '+%s ' + PLocalizer.PVPInfamySea
                    baseVal = value
                else:
                    if type == 8:
                        finalText = '+%s ' + PLocalizer.PVPInfamyLand
                        baseVal = value
                    else:
                        if type == 9:
                            finalText = '+%s ' + PLocalizer.PVPSalvage
                            baseVal = value
                        else:
                            finalText = '+%s'
                            baseVal = value
                        if ItemConstants.CRITICAL in effects:
                            finalText += '!'
                        mods = []
                        basicPenalty = 0
                        crewBonus = 0
                        doubleXPBonus = 0
                        holidayBonus = 0
                        potionBonus = 0
                        modtypes = modifiers.keys()
                        if MOD_HOLIDAYBONUS in modtypes:
                            holidayBonus = modifiers.get(MOD_HOLIDAYBONUS)
                            baseVal -= holidayBonus
                        if MOD_2XPBONUS in modtypes:
                            doubleXPBonus = modifiers.get(MOD_2XPBONUS)
                            baseVal -= doubleXPBonus
                        if MOD_POTIONBONUS in modtypes:
                            potionBonus = modifiers.get(MOD_POTIONBONUS)
                            baseVal -= potionBonus
                        if MOD_CREWBONUS in modtypes:
                            crewBonus = modifiers.get(MOD_CREWBONUS)
                            baseVal -= crewBonus
                        if MOD_BASICPENALTY in modtypes:
                            basicPenalty = modifiers.get(MOD_BASICPENALTY)
                            baseVal += basicPenalty
                        if basicPenalty > 0:
                            mods.append(TextEffect.TextEffectMod(0, -1 * basicPenalty, PLocalizer.EXP_Nerf, modType))
                    if crewBonus > 0:
                        mods.append(TextEffect.TextEffectMod(0, crewBonus, PLocalizer.CrewBonus, modType))
                if doubleXPBonus > 0:
                    mods.append(TextEffect.TextEffectMod(0, doubleXPBonus, PLocalizer.DoubleRepBonus, modType))
            if holidayBonus > 0:
                mods.append(TextEffect.TextEffectMod(0, holidayBonus, PLocalizer.HolidayBonus, modType))
        if potionBonus > 0:
            mods.append(TextEffect.TextEffectMod(0, potionBonus, PLocalizer.PotionBonus, modType))
    return (finalText, baseVal, mods)


def genColor(number, type, npc, effects):
    if type == 1:
        r = 1.0
        g = 1.0
        b = 0
        a = 1
    elif type == 2:
        r = 1.0
        g = 0.5
        b = 0
        a = 1
    elif type == 3:
        if npc:
            r = 0.3
            g = 0.0
            b = 1.0
            a = 1
        else:
            r = 0.5
            g = 0.0
            b = 1.0
            a = 1
    elif type == 4:
        r = 1.0
        g = 1.0
        b = 1.0
        a = 1
    elif type == 5:
        r = 0.8
        g = 1.0
        b = 0.8
        a = 1
    elif type == 7:
        r = 0.8
        g = 0.2
        b = 0.0
        a = 1
    elif type == 8:
        r = 1.0
        g = 0.4
        b = 0.1
        a = 1
    elif type == 9:
        r = 0.0
        g = 0.9
        b = 0.0
        a = 1
    elif type == 10:
        r = 0.6
        g = 0.6
        b = 0.95
        a = 1
    elif number < 0:
        if ItemGlobals.CRITICAL in effects:
            r = 0.9
            g = 0.7
            b = 0.3
            a = 1
        elif npc:
            r = 0.9
            g = 0.1
            b = 0.1
            a = 1
        else:
            r = 0.9
            g = 0.3
            b = 0.1
            a = 1
    elif npc:
        r = 0
        g = 0.9
        b = 0
        a = 1
    else:
        r = 0.1
        g = 0.9
        b = 0.2
        a = 1
    return (r, g, b, a)


class TextEffect():

    class TextEffectMod():

        def __init__(self, index, modValue, reason, type=0):
            self.modValue = modValue
            self.reason = reason
            self.index = index
            self.type = type

    def __init__(self, textGenerator, type, targetObj, scale, startPos, duration, text, baseVal, mods, finishCallback=None, destPos=None, textColor=(1, 1, 1, 1)):
        self.textGenerator = textGenerator
        self.textNode = None
        self.type = type
        self.startPos = startPos
        self.destPos = destPos
        self.duration = duration
        self.textLine1 = TextNode('HpTextGenerator')
        self.targetObj = targetObj
        self.staticText = text
        self.baseVal = baseVal
        self.textColor = textColor
        self.mods = mods
        self.scale = scale
        self.textNodes = []
        self.textIvals = []
        self.textModNodes = []
        self.textModIvals = []
        self.hpText = None
        self.start()
        self.finishCallbackRef = weakref.ref(finishCallback)
        return

    def genTextNode(self, parent, satellite=False):
        if satellite == False and self.hpText:
            self.hpText.removeNode()
        self.textNode = self.textGenerator.generate()
        hpText = parent.attachNewNode(self.textNode)
        if satellite == False:
            self.hpText = hpText
        if satellite:
            hpText.setScale(self.scale * 0.7)
        else:
            hpText.setScale(self.scale)
        hpText.setBillboardPointEye(3.0)
        hpText.setBin('fixed', 100)
        hpText.setDepthWrite(0)
        hpText.setFogOff()
        hpText.setLightOff()
        hpText.setPos(0, 0, 2.0)
        OTPRender.renderReflection(False, hpText, 'p_text_effect', None)
        return hpText

    def start(self):
        if self.type == 4:
            hpTextDummy = render.attachNewNode('hpTextDummy')
            hpTextDummy.setPos(render, self.targetObj.getPos(render))
        else:
            hpTextDummy = self.targetObj.attachNewNode('hpTextDummy')
        origColor = self.textColor
        self.textGenerator.setTextColor(*origColor)
        self.genTextNode(hpTextDummy)
        if self.destPos:
            hpTextDummy.setPos(self.targetObj, self.destPos[0], self.destPos[1], self.destPos[2])
            destPos = hpTextDummy.getPos()
        if self.startPos:
            hpTextDummy.setPos(self.targetObj, self.startPos[0], self.startPos[1], self.startPos[2])
        else:
            hpTextDummy.setPos(self, 0, 0, self.targetObj.height * 0.666)
        hpTextDummy.headsUp(base.camera)
        hpTextDummy.setH(hpTextDummy.getH() + 180)
        tgtColor = Vec4(origColor[0], origColor[1], origColor[2], 0)
        if not self.destPos:
            destPos = Point3(hpTextDummy.getX(), hpTextDummy.getY(), hpTextDummy.getZ() + 3 * self.scale)
        numberMoveUp = hpTextDummy.posInterval(self.duration, destPos)
        fadeOut = hpTextDummy.colorScaleInterval(self.duration * 0.333, tgtColor, startColorScale=Vec4(*origColor))
        trackParallel = Parallel(numberMoveUp)
        numMods = len(self.mods)
        origModDelay = self.duration * 0.8 / (numMods + 1)
        modDelay = origModDelay * 0.5
        for mod in self.mods:
            nextModDelay = modDelay + origModDelay
            trackParallel.append(Sequence(Wait(modDelay), Func(self.playMod, hpTextDummy, mod, origModDelay)))
            modDelay = nextModDelay

        trackParallel.append(Sequence(Wait(self.duration * 0.666), fadeOut))
        track = Sequence(trackParallel, Func(self.finish, hpTextDummy))
        track.start()
        self.textNodes.append(hpTextDummy)
        self.textIvals.append(track)

    def playMod(self, parent, mod, fadeDelay):
        self.textGenerator.setText(self.staticText % str(self.baseVal + mod.modValue))
        self.baseVal += mod.modValue
        origColor = self.textColor
        self.textGenerator.setTextColor(*origColor)
        parentText = self.genTextNode(parent)
        parentBounds = parentText.getTightBounds()
        parentHeight = parentBounds[1].getZ() - parentBounds[0].getZ()
        sign = ''
        if mod.modValue > 0:
            sign = '+'
        finalText = sign + str(mod.modValue) + ' ' + mod.reason
        finalText = '( ' + finalText + ' )'
        self.textGenerator.setText(finalText)
        self.textGenerator.setTextColor(*self.textColor)
        modText = self.genTextNode(parent, True)
        prevTextModPos = None
        if mod.type == MOD_TYPE_SEQUENTIAL or mod.type == MOD_TYPE_SEQUENTIAL_CONTINUOUS:
            for currTextModNode in self.textModNodes:
                if mod.type == MOD_TYPE_SEQUENTIAL_CONTINUOUS:
                    prevTextModPos = currTextModNode.getPos()
                currTextModNode.removeNode()

            self.textModNodes = []
            for currTextModIval in self.textModIvals:
                currTextModIval.finish()

            self.textModIvals = []
        if mod.type == MOD_TYPE_SEQUENTIAL_COMPACT or mod.type == MOD_TYPE_MULTIPLE_COMPACT:
            zLoc = 1.9 - parentHeight + self.scale * 0.5
            modText.setPos(0, -0.1, zLoc)
            origColor = self.textColor
            origColorX = origColor[0]
            origColorY = origColor[1]
            origColorZ = origColor[2]
            startColor = Vec4(origColorX, origColorY, origColorZ, 0.5)
            tgtColor = Vec4(origColorX, origColorY, origColorZ, 0)
            modText.setColorScale(tgtColor)
            fullTrack = Parallel()
            if mod.type == MOD_TYPE_MULTIPLE_COMPACT:
                startPos = modText.getPos()
                finalPos = Point3(startPos.getX(), startPos.getY(), startPos.getZ() - 9 * self.scale)
                fullTrack.append(modText.posInterval(14.0, finalPos))
                fullTrack.append(Sequence(Wait(fadeDelay), modText.colorScaleInterval(3.0, tgtColor, startColorScale=startColor)))
            modTextFade = Sequence(modText.colorScaleInterval(0.5, origColor, startColorScale=tgtColor))
            if mod.type != MOD_TYPE_MULTIPLE_COMPACT:
                modTextFade.append(Wait(fadeDelay - 0.15 - 0.5))
                modTextFade.append(modText.colorScaleInterval(0.15, tgtColor, startColorScale=origColor))
            fullTrack.append(modTextFade)
            fullTrack.start()
            self.textModIvals.append(fullTrack)
        else:
            modText.setPos(2 * (self.scale * 1.25), -0.1, 2 + self.scale * 0.9)
            if prevTextModPos:
                startPos = modText.getPos()
                modText.setPos(prevTextModPos)
            else:
                startPos = modText.getPos()
            finalPos = Point3(startPos.getX() + 2, startPos.getY(), startPos.getZ() + 8 * self.scale)
            origColor = self.textColor
            origColorX = origColor[0]
            origColorY = origColor[1]
            origColorZ = origColor[2]
            startColor = Vec4(origColorX, origColorY, origColorZ, 0.5)
            tgtColor = Vec4(origColorX, origColorY, origColorZ, 0)
            modTextMove = Parallel(modText.posInterval(14.0, finalPos), Sequence(Wait(fadeDelay), modText.colorScaleInterval(3.0, tgtColor, startColorScale=startColor)))
            modTextMove.start()
            self.textModIvals.append(modTextMove)
        self.textModNodes.append(modText)
        return

    def pause(self):
        for currIval in self.textIvals:
            currIval.pause()

        for currIval in self.textModIvals:
            currIval.pause()

    def resume(self):
        for currIval in self.textIvals:
            currIval.resume()

        for currIval in self.textModIvals:
            currIval.resume()

    def finish(self, textNode=None):
        if textNode:
            index = self.textNodes.index(textNode)
            self.textIvals[index].finish()
            self.textIvals[index] = None
            self.textNodes[index].removeNode()
            self.textNodes[index] = None
            finishCallback = self.finishCallbackRef()
            if finishCallback:
                finishCallback()
        return


def genTextEffect(targetObj, textGenerator, number, bonus, isNpc, cleanupCallback, startPos, destPos=None, scale=1.0, modifiers={}, effects=[]):
    textGenerator.setFont(PiratesGlobals.getPirateOutlineFont())
    text, baseVal, mods = genText(number, bonus, MOD_TYPE_MULTIPLE, modifiers, effects)
    duration = 2.0 + len(mods)
    textGenerator.setText(text % str(baseVal))
    textGenerator.clearShadow()
    textGenerator.setAlign(TextNode.ACenter)
    color = genColor(number, bonus, isNpc, effects)
    newEffect = TextEffect(textGenerator, bonus, targetObj, scale, startPos, duration, text, baseVal, mods, cleanupCallback, destPos, color)
    return newEffect