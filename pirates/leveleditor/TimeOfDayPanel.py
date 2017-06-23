import pprint
from direct.showbase.TkGlobal import *
from direct.tkwidgets.AppShell import *
from direct.tkwidgets import Dial
from direct.tkwidgets import Floater
from direct.tkwidgets import Slider
from direct.tkwidgets import VectorWidgets
from direct.tkwidgets import Valuator
import tkColorChooser
from direct.directtools.DirectUtil import getTkColorString
import Pmw
from direct.gui import DirectGuiGlobals as DGG
from pirates.piratesbase import PLocalizer as PL
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TODGlobals
from pandac.PandaModules import *
from Tkinter import *

class TimeOfDayPanel(AppShell):
    appname = 'Time Of Day Panel'
    appversion = '1.1'
    copyright = 'Copyright 2006 Walt Disney Interactive Media Group.' + ' All Rights Reserved'
    contactname = 'Pirates Team - DIMG'
    contactphone = ''
    contactemail = ''
    frameWidth = 690
    frameHeight = 800
    usecommandarea = 0
    usestatusarea = 0

    def __init__(self, todMgr, parent=None, **kw):
        self.todMgr = todMgr
        self.editor = None
        self.selectedCycleDuration = -1
        self.uncommitedColor = Vec4(255.0, 0.0, 0.0, 255.0)
        self.changedColor = Vec4(0.0, 255.0, 255.0, 255.0)
        self.defaultColor = Vec4(255.0, 255.0, 255.0, 255.0)
        self.changesEnabled = 0
        self.holdFogColor = None
        self.holdFogExp = None
        self.holdLinearRanges = None
        self.holdAmbientColor = None
        self.holdDirectionColor = None
        self.holdBackColor = None
        self.holdSunDirection = None
        self.accept('timeOfDayChange', self.updateTod)
        self.accept('environmentChanged', self.updateEnv)
        self.accept('TOD_Setting_Change', self.checkButtonsForChange)
        self.accept('TOD_CYCLE_CHANGE', self.updateCycleType)
        DGG.INITOPT = Pmw.INITOPT
        optiondefs = (('title', self.appname, None),)
        self.defineoptions(kw, optiondefs)
        AppShell.__init__(self, parent)
        self.initialiseoptions(TimeOfDayPanel)
        return

    def setEditor(self, editor):
        self.editor = editor
        self.checkButtonsForChange()

    def onDestroy(self, event):
        if self.editor:
            self.editor.TODPanel = None
            self.editor.TODPanelLoaded = False
        self.ignoreAll()
        AppShell.onDestroy(self, event)
        return

    def getTkColorFromVec4(self, v, mult=255):
        return getTkColorString([int(v[0] * mult), int(v[1] * mult), int(v[2] * mult)])

    def createInterface(self):
        interior = self.interior()
        todFrame = Frame(interior, borderwidth=4, relief='raised')
        todButtonFrame = Frame(todFrame, borderwidth=2, relief='sunken')
        printButton = Button(todButtonFrame, text='PRINT', command=self.printSettings)
        texToggle = Button(todButtonFrame, text='Toggle Textures', command=base.toggleTexture)
        saveChanges = Button(todButtonFrame, text='Insert Change', command=self.saveChanges)
        self.saveChanges = saveChanges
        self.saveChanges['state'] = 'disabled'
        removeChanges = Button(todButtonFrame, text='Clear to Environment Setting', command=self.clearChanges)
        self.removeChanges = removeChanges
        self.removeChanges['state'] = 'disabled'
        undoChanges = Button(todButtonFrame, text='Undo Change', command=self.undoChanges)
        self.undoChanges = undoChanges
        self.environmetVar = IntVar()
        self.environmetVar.set(self.todMgr.environment)
        environmentFrame = Frame(todFrame, borderwidth=2, relief='sunken')
        for environmentId in TODGlobals.ENVIRONMENT_NAMES:
            name = TODGlobals.ENVIRONMENT_NAMES[environmentId]
            button = Radiobutton(environmentFrame, text=name, variable=self.environmetVar, value=environmentId, command=self.changeEnvironment)
            button.pack(side=LEFT, fill=X, expand=0)

        todCycleTypeFrame = Frame(todFrame, borderwidth=2, relief='sunken')
        self.cycleTypeVar = IntVar()
        self.cycleTypeVar.set(self.todMgr.cycleType)
        self.cycleTypeDict = {}
        for idKey in TODGlobals.CYCLE_NAMES:
            name = TODGlobals.CYCLE_NAMES[idKey]
            self.cycleTypeDict[idKey] = Radiobutton(todCycleTypeFrame, text=name, variable=self.cycleTypeVar, value=idKey, command=self.commandChangeTodCycle)

        for buttonKey in self.cycleTypeDict:
            button = self.cycleTypeDict[buttonKey]
            button.pack(side=LEFT, fill=X, expand=0)

        self.todStateFrame = Frame(todFrame, borderwidth=2, relief='sunken')
        self.todVar = IntVar()
        self.todVar.set(self.todMgr.currentState)
        todCycleId = self.todMgr.cycleType
        todCycleList = TODGlobals.CycleStateTimeList[todCycleId]
        self.todButtonDict = {}
        self.makeTODButtons()
        for buttonKey in self.todButtonDict:
            button = self.todButtonDict[buttonKey]
            button.pack(side=LEFT, fill=X, expand=0)

        todCycleFrame = Frame(todFrame, borderwidth=2, relief='sunken')
        self.cycleDurationVar = IntVar()
        todCycle0 = Radiobutton(todCycleFrame, text='Off(edit)', variable=self.cycleDurationVar, value=0, command=self.commandChangeTodSpeed)
        todCycle1 = Radiobutton(todCycleFrame, text='30 sec', variable=self.cycleDurationVar, value=120, command=self.commandChangeTodSpeed)
        todCycle2 = Radiobutton(todCycleFrame, text='2 min', variable=self.cycleDurationVar, value=30, command=self.commandChangeTodSpeed)
        todCycle3 = Radiobutton(todCycleFrame, text='10 min', variable=self.cycleDurationVar, value=6, command=self.commandChangeTodSpeed)
        todCycle4 = Radiobutton(todCycleFrame, text='1 hour', variable=self.cycleDurationVar, value=1, command=self.commandChangeTodSpeed)
        self.cycleDurationVar.set(int(self.todMgr.cycleSpeed))
        envInfo = Label(todFrame, text='Environment- -DataOnly- is the working set', borderwidth=2, anchor=W, font=('MS Sans Serif',
                                                                                                                    9))
        todInfo = Label(todFrame, text='TOD- White is Default, Blue is Saved, Red is changed but not saved', borderwidth=2, anchor=W, font=('MS Sans Serif',
                                                                                                                                            9))
        cycleInfo = Label(todFrame, text='Cycle', borderwidth=2, anchor=W, font=('MS Sans Serif',
                                                                                 9))
        durationInfo = Label(todFrame, text='Duration- Select Off to Edit', borderwidth=2, anchor=W, font=('MS Sans Serif',
                                                                                                           9))
        todCycle0.pack(side=LEFT, fill=X, expand=0)
        todCycle1.pack(side=LEFT, fill=X, expand=0)
        todCycle2.pack(side=LEFT, fill=X, expand=0)
        todCycle3.pack(side=LEFT, fill=X, expand=0)
        todCycle4.pack(side=LEFT, fill=X, expand=0)
        todButtonFrame.pack(side=TOP, fill=X, expand=0)
        printButton.pack(fill=X, expand=0)
        texToggle.pack(fill=X, expand=0)
        saveChanges.pack(fill=X, expand=0)
        undoChanges.pack(fill=X, expand=0)
        removeChanges.pack(fill=X, expand=0)
        envInfo.pack(fill=X, expand=0)
        environmentFrame.pack(fill=X, expand=0)
        cycleInfo.pack(fill=X, expand=0)
        todCycleTypeFrame.pack(fill=X, expand=0)
        todInfo.pack(side=TOP, fill=X, expand=0)
        self.todStateFrame.pack(fill=X, expand=0)
        durationInfo.pack(side=TOP, fill=X, expand=0)
        todCycleFrame.pack(fill=X, expand=0)
        todFrame.pack(fill=X, expand=0, pady=4)
        initialFogColor = self.todMgr.fog.getColor()
        controlFrame = Frame(interior, borderwidth=2, relief='raised')
        otherFrame = Frame(controlFrame, borderwidth=2, relief='raised')
        skyFrame = Frame(interior, borderwidth=2, relief='raised')
        skyLabel = Label(skyFrame, text='Select Sky', font=('MS Sans Serif', 11))
        self.todSkyTypeVar = IntVar()
        self.todSkyTypeVar.set(int(self.todMgr.skyGroup.lastSky))
        skyListFrame = Frame(interior, borderwidth=2, relief='raised')
        for key in TODGlobals.SKY_NAMES:
            name = TODGlobals.SKY_NAMES[key]
            skyTypeButton = Radiobutton(skyListFrame, text=name, variable=self.todSkyTypeVar, value=key, command=self.changeSky)
            skyTypeButton.pack(side=LEFT, fill=X, expand=0)

        otherFrame.pack(side=RIGHT, fill=NONE, expand=0, pady=4)
        fogFrame = Frame(otherFrame, borderwidth=2, relief='raised')
        fogLabelFrame = Frame(fogFrame, borderwidth=2, relief='sunken')
        fogControlFrame = Frame(fogFrame, borderwidth=2, relief='sunken')
        self.fogTopLabel = Label(fogLabelFrame, text='FOG ', font=('MS Sans Serif',
                                                                   11))
        fogTypeFrame = Frame(fogControlFrame, borderwidth=2, relief='raised')
        self.fogTypeVar = IntVar()
        self.fogTypeVar.set(self.todMgr.fogType)
        self.fogOff = Radiobutton(fogTypeFrame, text='Off', variable=self.fogTypeVar, value=TODGlobals.FOG_OFF, command=self.setFogType)
        self.fogExp = Radiobutton(fogTypeFrame, text='Exponent', variable=self.fogTypeVar, value=TODGlobals.FOG_EXP, command=self.setFogType)
        self.fogLinear = Radiobutton(fogTypeFrame, text='Linear', variable=self.fogTypeVar, value=TODGlobals.FOG_LINEAR, command=self.setFogType)
        self.fogLabel = Label(fogLabelFrame, text='\n ', font=('MS Sans Serif', 11))
        self.fogLabel['bg'] = self.getTkColorFromVec4(initialFogColor)
        self.fogColor = Valuator.ValuatorGroup(parent=fogControlFrame, dim=3, labels=['R', 'G', 'B'], value=[int(initialFogColor[0] * 1.0), int(initialFogColor[1] * 1.0), int(initialFogColor[2] * 1.0)], type='slider', valuator_style='mini', valuator_min=0, valuator_max=1.0, valuator_resolution=0.01)
        self.fogColor['command'] = self.setFogColorVec

        def popupFogColorPicker():
            baseColor = self.todMgr.getFogColor()
            initColor = self.clipLightValue(baseColor * 255.0, 255.0)
            color = tkColorChooser.askcolor(parent=interior, initialcolor=(initColor[0], initColor[1], initColor[2]))
            if color[0] is not None:
                self.fogColor.set((round(color[0][0] / 255.0, 2), round(color[0][1] / 255.0, 2), round(color[0][2] / 255.0, 2)))
            return

        pButton = Button(fogLabelFrame, text='Popup Color Picker', command=popupFogColorPicker)
        initialRange = self.todMgr.fog.getExpDensity()
        self.fogRangeFrame = Frame(fogControlFrame)
        self.fogRange = Valuator.ValuatorGroup(parent=self.fogRangeFrame, dim=1, labels=['Range'], value=[initialRange], type='slider', valuator_style='mini', min=0.0, max=0.01, numDigits=6, resolution=1e-06)
        self.fogRange['command'] = self.setFogRangeVec
        initialOnSet = self.todMgr.linearFog.getLinearOnsetPoint()
        initialPeak = self.todMgr.linearFog.getLinearOpaquePoint()
        self.fogLinearRange = Valuator.ValuatorGroup(parent=self.fogRangeFrame, dim=2, labels=['OnSet', 'Peak'], value=[initialOnSet[1], initialPeak[1]], type='slider', valuator_style='mini', min=0.0, max=1000.0, numDigits=0, resolution=1.0)
        self.fogLinearRange['command'] = self.setFogLinearRange
        initialSunDirection = self.todMgr.skyGroup.getSunTrueAngle()
        sunFrame = Frame(otherFrame, borderwidth=2, relief='raised')
        self.sunDirectionLabel = Label(sunFrame, text='Sun Direction', font=('MS Sans Serif',
                                                                             11))
        self.sunDirection = Valuator.ValuatorGroup(parent=sunFrame, dim=3, labels=['Heading (Sunrise Direction)', 'Pitch (Tilt)', 'Roll (Rise and Set)'], value=[int(initialSunDirection[0] * 360), int(initialSunDirection[1] * 360), int(initialSunDirection[2] * 360)], type='slider', valuator_style='mini', valuator_min=0, valuator_max=360, valuator_resolution=1)
        self.sunDirection['command'] = self.setSunDirection

        def pointSunDown():
            self.sunDirection.set((0, 0, 270))

        def pointSunUp():
            self.sunDirection.set((0, 0, 90))

        sunDown = Button(sunFrame, text='Sun at Top', command=pointSunDown)
        sunUp = Button(sunFrame, text='Sun at Bottom', command=pointSunUp)
        self.sunDirectionLabel.pack(side=TOP, fill=X, expand=0, pady=4)
        self.sunDirection.pack(side=TOP, fill=X, expand=0, pady=4)
        sunDown.pack(side=TOP, fill=X, expand=0, pady=4)
        sunUp.pack(side=TOP, fill=X, expand=0, pady=4)
        controlFrame.pack(side=TOP, fill=X, expand=0, pady=4)
        skyFrame.pack(side=TOP, fill=X, expand=0, pady=4)
        skyLabel.pack(side=TOP, fill=X, expand=0)
        skyListFrame.pack(side=TOP, fill=X, expand=0)
        fogLabelFrame.pack(side=LEFT, fill=X, expand=0)
        fogControlFrame.pack(side=RIGHT, fill=X, expand=1)
        self.fogTopLabel.pack(side=TOP, fill=X, expand=1)
        fogTypeFrame.pack(side=TOP, fill=X, expand=1)
        self.fogOff.pack(side=RIGHT, fill=X, expand=1)
        self.fogExp.pack(side=RIGHT, fill=X, expand=1)
        self.fogLinear.pack(side=RIGHT, fill=X, expand=1)
        self.fogLabel.pack(side=TOP, fill=X, expand=1)
        pButton.pack(side=BOTTOM, fill=X, expand=0)
        self.fogColor.pack(fill=X, expand=0)
        self.fogRangeFrame.pack(fill=X, expand=0)
        self.fogRange.pack(fill=X, expand=0)
        fogFrame.pack(side=TOP, fill=X, expand=0, pady=4)
        sunFrame.pack(side=TOP, fill=X, expand=0, pady=4)
        initialAmbientColor = self.todMgr.alight.node().getColor()
        lightingFrame = Frame(controlFrame, borderwidth=2, relief='raised')
        ambientFrame = Frame(lightingFrame, borderwidth=2, relief='raised')
        ambientControlFrame = Frame(ambientFrame, borderwidth=2, relief='sunken')
        ambientLabelFrame = Frame(ambientFrame, borderwidth=2, relief='sunken')
        self.ambientLabel = Label(ambientLabelFrame, text='\n ', font=('MS Sans Serif',
                                                                       11))
        self.ambientLabel['bg'] = self.getTkColorFromVec4(self.clipLightValue(initialAmbientColor * 1.0, 1.0))
        self.ambientSwitchVar = IntVar()
        self.ambientSwitch = Checkbutton(ambientLabelFrame, text='Fill Light', variable=self.ambientSwitchVar, command=self.switchAmbient)
        self.ambientColor = Valuator.ValuatorGroup(parent=ambientControlFrame, dim=3, labels=['R', 'G', 'B'], value=[int(initialAmbientColor[0] * 1.0), int(initialAmbientColor[1] * 1.0), int(initialAmbientColor[2] * 1.0)], type='slider', valuator_style='mini', valuator_min=0, valuator_max=1.0, valuator_resolution=0.01)
        self.ambientColor['command'] = self.setAmbientColorVec

        def popupAmbientColorPicker():
            baseColor = self.todMgr.getFillLightColor()
            initColor = self.clipLightValue(baseColor * 255.0, 255.0)
            color = tkColorChooser.askcolor(parent=interior, initialcolor=(initColor[0], initColor[1], initColor[2]))
            if color[0] is not None:
                self.ambientColor.set((round(color[0][0] / 255.0, 2), round(color[0][1] / 255.0, 2), round(color[0][2] / 255.0, 2)))
            return

        pButton = Button(ambientLabelFrame, text='Popup Color Picker', command=popupAmbientColorPicker)
        ambientLabelFrame.pack(side=LEFT, fill=X, expand=0)
        ambientControlFrame.pack(side=RIGHT, fill=X, expand=1)
        self.ambientSwitch.pack(side=TOP, fill=X, expand=1)
        self.ambientLabel.pack(side=TOP, fill=X, expand=1)
        pButton.pack(side=BOTTOM, fill=X, expand=0)
        self.ambientColor.pack(fill=X, expand=0)
        lightingFrame.pack(side=LEFT, fill=NONE, expand=0, pady=4)
        if self.todMgr.dlight:
            initialDirectionalColor = self.todMgr.getFrontLightColor()
        else:
            initialDirectionalColor = Vec4(0, 0, 0, 1)
        directionalFrame = Frame(lightingFrame, borderwidth=2, relief='raised')
        directionalControlFrame = Frame(directionalFrame, borderwidth=2, relief='sunken')
        directionalLabelFrame = Frame(directionalFrame, borderwidth=2, relief='sunken')
        self.directionalLabel = Label(directionalLabelFrame, text='FRONT LIGHT\n ', font=('MS Sans Serif',
                                                                                          11))
        self.directionalLabel['bg'] = self.getTkColorFromVec4(self.clipLightValue(initialDirectionalColor * 0.5, 1.0))
        self.frontSwitchVar = IntVar()
        self.frontSwitch = Checkbutton(directionalLabelFrame, text='Front Light', variable=self.frontSwitchVar, command=self.switchFront)
        self.directionalColor = Valuator.ValuatorGroup(parent=directionalControlFrame, dim=3, labels=['R', 'G', 'B'], value=[int(initialDirectionalColor[0] * 1.0), int(initialDirectionalColor[1] * 1.0), int(initialDirectionalColor[2] * 1.0)], type='slider', valuator_style='mini', valuator_min=0, valuator_max=2.0, valuator_resolution=0.01)
        self.directionalColor['command'] = self.setDirectionalColorVec

        def popupDirectionalColorPicker():
            baseColor = self.todMgr.getFrontLightColor()
            initColor = self.clipLightValue(baseColor * 127.5, 255.0)
            color = tkColorChooser.askcolor(parent=interior, initialcolor=(initColor[0], initColor[1], initColor[2]))
            if color[0] is not None:
                self.directionalColor.set((round(color[0][0] / 127.5, 2), round(color[0][1] / 127.5, 2), round(color[0][2] / 127.5, 2)))
            return

        pButton = Button(directionalLabelFrame, text='Popup Color Picker', command=popupDirectionalColorPicker)
        directionalLabelFrame.pack(side=LEFT, fill=X, expand=0)
        directionalControlFrame.pack(side=RIGHT, fill=X, expand=1)
        self.frontSwitch.pack(side=TOP, fill=X, expand=1)
        self.directionalLabel.pack(side=TOP, fill=X, expand=1)
        pButton.pack(side=BOTTOM, fill=X, expand=0)
        self.directionalColor.pack(fill=X, expand=0)
        if self.todMgr.shadowLight:
            initialBackLightColor = self.todMgr.getBackLightColor()
        else:
            initialBackLightColor = Vec4(0, 0, 0, 1)
        backLightFrame = Frame(lightingFrame, borderwidth=2, relief='raised')
        backLightControlFrame = Frame(backLightFrame, borderwidth=2, relief='sunken')
        backLightLabelFrame = Frame(backLightFrame, borderwidth=2, relief='sunken')
        self.backLightLabel = Label(backLightLabelFrame, text='BACK LIGHT\n ', font=('MS Sans Serif',
                                                                                     11))
        self.backLightLabel['bg'] = self.getTkColorFromVec4(self.clipLightValue(initialBackLightColor * 0.5, 1.0))
        self.backSwitchVar = IntVar()
        self.backSwitch = Checkbutton(backLightLabelFrame, text='Back Light', variable=self.backSwitchVar, command=self.switchBack)
        self.backLightColor = Valuator.ValuatorGroup(parent=backLightControlFrame, dim=3, labels=['R', 'G', 'B'], value=[int(initialBackLightColor[0] * 1.0), int(initialBackLightColor[1] * 1.0), int(initialBackLightColor[2] * 1.0)], type='slider', valuator_style='mini', valuator_min=0, valuator_max=2.0, valuator_resolution=0.01)
        self.backLightColor['command'] = self.setBackColorVec

        def popupBackColorPicker():
            baseColor = self.todMgr.getBackLightColor()
            initColor = self.clipLightValue(baseColor * 127.5, 255.0)
            color = tkColorChooser.askcolor(parent=interior, initialcolor=(initColor[0], initColor[1], initColor[2]))
            if color[0] is not None:
                self.backLightColor.set((round(color[0][0] / 127.5, 2), round(color[0][1] / 127.5, 2), round(color[0][2] / 127.5, 2)))
            return

        pButton = Button(backLightLabelFrame, text='Popup Color Picker', command=popupBackColorPicker)
        backLightLabelFrame.pack(side=LEFT, fill=X, expand=0)
        backLightControlFrame.pack(side=RIGHT, fill=X, expand=1)
        self.backSwitch.pack(side=TOP, fill=X, expand=1)
        self.backLightLabel.pack(side=TOP, fill=X, expand=1)
        pButton.pack(side=BOTTOM, fill=X, expand=0)
        self.backLightColor.pack(fill=X, expand=0)
        directionalFrame.pack(side=TOP, fill=X, expand=0, pady=4)
        ambientFrame.pack(side=TOP, fill=X, expand=0, pady=4)
        backLightFrame.pack(side=TOP, fill=X, expand=0, pady=4)
        self.postCreateInterface()

    def postCreateInterface(self):
        self.cycleDurationVar.set(int(self.todMgr.cycleSpeed))
        self.selectedCycleDuration = self.todMgr.cycleSpeed
        if self.todMgr.cycleDuration == 0:
            self.holdData()
        self.setEnableDisable()
        self.checkButtonsForChange()

    def makeTODButtons(self):
        for buttonKey in self.todButtonDict:
            button = self.todButtonDict[buttonKey]
            button.pack_forget()

        self.todButtonDict = {}
        todCycleId = self.todMgr.cycleType
        todCycleList = TODGlobals.CycleStateTimeList[todCycleId]
        for todCycleState in todCycleList:
            timeId = todCycleState[0]
            timeName = TODGlobals.StateDict[timeId]
            newButton = Radiobutton(self.todStateFrame, text=timeName, variable=self.todVar, value=timeId, command=self.commandChangeTod)
            self.todButtonDict[timeId] = newButton
            newButton.pack(side=LEFT, fill=X, expand=0)

    def setEnableDisable(self):
        cycleDuration = self.todMgr.cycleSpeed
        if cycleDuration > 0.0 or self.todMgr.currentState != self.todVar.get():
            self.ambientLabel['text'] = 'DISABLED\n '
            self.directionalLabel['text'] = 'DISABLED\n '
            self.backLightLabel['text'] = 'DISABLED\n '
            self.fogLabel['text'] = 'DISABLED\n '
            self.saveChanges['state'] = 'disabled'
            self.changesEnabled = 0
            self.holdFogColor = None
            self.holdFogExp = None
            self.holdLinearRanges = None
            self.holdAmbientColor = None
            self.holdDirectionColor = None
            self.holdBackColor = None
        else:
            if cycleDuration == -1.0:
                self.ambientLabel['text'] = '\n '
                self.directionalLabel['text'] = '\n '
                self.backLightLabel['text'] = '\n '
                self.fogLabel['text'] = 'DISABLED\n '
                self.saveChanges['state'] = 'disabled'
                self.changesEnabled = 0
                self.holdFogColor = None
                self.holdFogExp = None
                self.holdLinearRanges = None
                self.holdAmbientColor = None
                self.holdDirectionColor = None
                self.holdBackColor = None
            else:
                self.ambientLabel['text'] = '\n '
                self.directionalLabel['text'] = '\n '
                self.backLightLabel['text'] = '\n '
                self.fogLabel['text'] = '\n '
                self.changesEnabled = 1
            if self.selectedCycleDuration != 0 or self.holdFogColor == None:
                self.changesEnabled = 0
                self.saveChanges['state'] = 'disabled'
            if self.changesEnabled:
                self.frontSwitch['state'] = 'normal'
                self.ambientSwitch['state'] = 'normal'
                self.backSwitch['state'] = 'normal'
            else:
                self.frontSwitch['state'] = 'disabled'
                self.ambientSwitch['state'] = 'disabled'
                self.backSwitch['state'] = 'disabled'
            if self.todMgr.fogMask:
                self.fogTopLabel['text'] = 'FOG -hidden-'
            self.fogTopLabel['text'] = 'FOG'
        return

    def checkButtonsForChange(self):
        changedColor = Vec4(0.0, 255.0, 255.0, 255.0)
        defaultColor = Vec4(255.0, 255.0, 255.0, 255.0)
        if self.editor:
            alteredTODs = self.todMgr.listAlteredTODs(TODGlobals.ENV_DATAFILE)
        else:
            alteredTODs = self.todMgr.listAlteredTODs(self.todMgr.environment)
        for key in self.todButtonDict:
            button = self.todButtonDict[key]
            text = TODGlobals.StateDict.get(key)
            if text:
                if text in alteredTODs:
                    button['bg'] = getTkColorString(self.changedColor)
                else:
                    button['bg'] = getTkColorString(self.defaultColor)

        frontSwitch = self.todMgr.lightSwitch[0]
        ambientSwitch = self.todMgr.lightSwitch[1]
        backSwitch = self.todMgr.lightSwitch[2]
        self.frontSwitchVar.set(frontSwitch)
        self.ambientSwitchVar.set(ambientSwitch)
        self.backSwitchVar.set(backSwitch)
        self.fogTypeVar.set(self.todMgr.fogType)
        self.todSkyTypeVar.set(int(self.todMgr.skyGroup.lastSky))
        alteredTODs = self.todMgr.listAlteredTODs(self.todMgr.environment)
        alteredTime = 0
        stateId = self.todMgr.currentState
        for entry in alteredTODs:
            if entry == stateId:
                alteredTime = 1

        if alteredTime and self.selectedCycleDuration == 0 or 1:
            self.removeChanges['state'] = 'normal'
        else:
            self.removeChanges['state'] = 'disabled'

    def updateTod(self, stateId, stateDuration, elapsedTime, transitionTime):
        self.todVar.set(stateId)
        self.holdData()
        self.setEnableDisable()
        self.checkButtonsForChange()
        self.repackFog()

    def holdData(self):
        holdChanges = self.changesEnabled
        self.changesEnabled = 1
        stateId = self.todMgr.currentState
        fogColor = TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'FogColor')
        fogRange = TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'FogExp')
        linearFogOnSet = self.todMgr.linearFog.getLinearOnsetPoint()
        linearFogPeak = self.todMgr.linearFog.getLinearOpaquePoint()
        ambientColor = TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'AmbientColor')
        self.fogColor.set((fogColor[0], fogColor[1], fogColor[2]))
        self.fogRange.set((fogRange,))
        self.ambientColor.set((ambientColor[0], ambientColor[1], ambientColor[2]))
        self.fogLinearRange.set((linearFogOnSet[1], linearFogPeak[1]))
        sunDirection = self.todMgr.skyGroup.boundSunAngle(TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'Direction'))
        self.sunDirection.set((sunDirection[0], sunDirection[1], sunDirection[2]))
        directionalColor = None
        if self.todMgr.dlight:
            directionalColor = TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'FrontColor')
            self.holdDirectionColor = directionalColor
            self.directionalColor.set((directionalColor[0], directionalColor[1], directionalColor[2]))
        backLightColor = None
        if self.todMgr.shadowLight:
            backLightColor = TODGlobals.getTodEnvSetting(stateId, self.todMgr.environment, 'BackColor')
            self.holdBackColor = backLightColor
            self.backLightColor.set((backLightColor[0], backLightColor[1], backLightColor[2]))
        if self.selectedCycleDuration == 0:
            pass
        self.holdFogColor = fogColor
        self.holdFogExp = fogRange
        self.holdLinearRanges = (linearFogOnSet[1], linearFogPeak[1])
        self.holdAmbientColor = ambientColor
        self.holdDirectionColor = directionalColor
        self.holdBackColor = backLightColor
        self.holdSunDirection = sunDirection
        self.changesEnabled = holdChanges
        return

    def updateEnv(self):
        self.environmetVar.set(self.todMgr.environment)

    def changeEnvironment(self):
        environmentId = self.environmetVar.get()
        self.todMgr.setEnvironment(environmentId)
        if self.editor:
            if self.editor.panel.environmentMenu:
                name = TODGlobals.ENVIRONMENT_NAMES[environmentId]
                itemList = list(self.editor.panel.environmentMenu._list.get())
                self.editor.panel.environmentMenu.selectitem(itemList.index(name))
                self.editor.panel.selectPropertyVal(name, 'Environment', self.editor.panel.areaObjInfo, None, None, isVisAttrib=False, skipVisUpdate=True, skipCvsEdit=False, skipCallback=True, fromUI=False)
        return

    def commandChangeTodCycle(self):
        cycle = self.cycleTypeVar.get()
        cycleName = TODGlobals.CYCLE_NAMES[cycle]
        initialStateId = TODGlobals.CycleStateTimeList[cycle][0][0]
        stateName = TODGlobals.StateDict[initialStateId]
        self.changeTODCycleType(cycle, initialStateId)
        self.setEnableDisable()
        self.checkButtonsForChange()

    def updateCycleType(self):
        self.cycleDurationVar.set(int(self.todMgr.cycleSpeed))
        self.makeTODButtons()

    def changeTODCycleType(self, cycleType, initialStateId):
        magicWord = '~todCycle %s %s' % (cycleType, initialStateId)
        messenger.send('magicWord', [magicWord])
        if self.editor:
            self.todMgr.cycleType = cycleType
            self.makeTODButtons()
            self.commandChangeTod()

    def commandChangeTod(self):
        tod = self.todVar.get()
        startHour = TODGlobals.getStateBeginTime(self.todMgr.cycleType, tod)
        if startHour == None:
            startHour = 0.0
        todStartHour = (startHour + TODGlobals.getStateTransitionTime(self.todMgr.cycleType, tod)) * PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY
        cycleDuration = self.cycleDurationVar.get()
        self.changeTod(cycleDuration, todStartHour)
        self.setEnableDisable()
        self.checkButtonsForChange()
        return

    def commandChangeTodSpeed(self):
        tod = self.todVar.get()
        todStartHour = TODGlobals.getStateBeginTime(self.todMgr.cycleType, tod)
        cycleDuration = self.cycleDurationVar.get()
        self.changeTod(cycleDuration)
        self.setEnableDisable()
        self.checkButtonsForChange()

    def commandChangeTodOff(self):
        tod = self.todVar.get()
        todStartHour = TODGlobals.getStateBeginTime(self.todMgr.cycleType, tod)
        cycleDuration = self.cycleDurationVar.get()
        self.selectedCycleDuration = -1
        self.changeTod(self.todMgr.cycleSpeed, todStartHour)

    def changeTod(self, cycleSpeed, desiredTime = None):
        magicSpeed = max(cycleSpeed, 0)
        if desiredTime == None:
            desiredTime = self.todMgr.getCurrentIngameTime()

        magicWord = '~tod %s %s' % (desiredTime, magicSpeed)
        messenger.send('magicWord', [magicWord])
        self.selectedCycleDuration = cycleSpeed
        if self.editor:
            self.editor.panel.skyState.set(self.todVar.get())
            if desiredTime != None:
                self.todMgr.cycleSpeed = cycleSpeed
                self.todMgr.setDesiredTime(desiredTime)

            self.editor.changeTimeOfDay()
        elif self.editor and self.editor.TODPanelLoaded:
            self.editor.objectMgr.currEditedObjInfo.setTodModified(True)

        self.editor.disableTOD(fromTODPanel = True)
        self.setEnableDisable()
        self.checkButtonsForChange()

    def setSunDirection(self, direction):
        if not self.changesEnabled:
            return
        todState = self.todVar.get()
        newDirection = Vec3(direction[0], direction[1], direction[2])
        direction = newDirection
        self.todMgr.skyGroup.setSunTrueAngle(direction)
        if self.holdSunDirection != direction:
            if self.holdSunDirection != None:
                button = self.todButtonDict.get(todState)
                if button:
                    button['bg'] = getTkColorString(self.uncommitedColor)
            self.holdSunDirection = direction
            self.saveChanges['state'] = 'normal'
            if self.editor and self.editor.TODPanelLoaded:
                self.editor.objectMgr.currEditedObjInfo.setTodModified(True)
        return

    def setFogColorVec(self, color):
        if not self.changesEnabled:
            return
        vColor = Vec4(color[0] / 1.0, color[1] / 1.0, color[2] / 1.0, 0)
        iColor = [int(vColor[0] * 255.0), int(vColor[1] * 255.0), int(vColor[2] * 255.0)]
        todState = self.todVar.get()
        self.todMgr.setFogColor(vColor)
        self.fogLabel['bg'] = getTkColorString(iColor)
        if self.holdFogColor != vColor:
            if self.holdFogColor != None:
                button = self.todButtonDict.get(todState)
                if button:
                    button['bg'] = getTkColorString(self.uncommitedColor)
            self.holdFogColor = vColor
            self.saveChanges['state'] = 'normal'
            if self.editor and self.editor.TODPanelLoaded:
                self.editor.objectMgr.currEditedObjInfo.setTodModified(True)
        return

    def setFogRangeVec(self, range):
        if not self.changesEnabled:
            return
        self.todMgr.setFogExpDensity(range[0])
        todState = self.todVar.get()
        if self.holdFogExp != range[0]:
            if self.holdFogExp != None:
                button = self.todButtonDict.get(todState)
                if button:
                    button['bg'] = getTkColorString(self.uncommitedColor)
            self.holdFogExp = range[0]
            self.saveChanges['state'] = 'normal'
            if self.editor and self.editor.TODPanelLoaded:
                self.editor.objectMgr.currEditedObjInfo.setTodModified(True)
        return

    def setFogLinearRange(self, range):
        if not self.changesEnabled:
            return
        self.todMgr.setLinearFogOnset(range[0])
        self.todMgr.setLinearFogPeak(range[1])
        todState = self.todVar.get()
        if self.holdLinearRanges != (range[0], range[1]):
            if self.holdLinearRanges != None:
                button = self.todButtonDict.get(todState)
                if button:
                    button['bg'] = getTkColorString(self.uncommitedColor)
            self.holdLinearRanges = (
             range[0], range[1])
            self.saveChanges['state'] = 'normal'
            if self.editor and self.editor.TODPanelLoaded:
                if not self.editor.switchingToDrive:
                    self.todMgr.linearFog.setLinearRange(range[0], range[1])
                self.editor.objectMgr.currEditedObjInfo.setTodModified(True)
        return

    def setAmbientColorVec(self, color):
        if not self.changesEnabled:
            return
        vColor = Vec4(color[0] / 1.0, color[1] / 1.0, color[2] / 1.0, 1)
        iColor = [int(vColor[0] * 255.0), int(vColor[1] * 255.0), int(vColor[2] * 255.0)]
        self.todMgr.setFillLightColor(vColor)
        self.ambientLabel['bg'] = getTkColorString(iColor)
        todState = self.todVar.get()
        if self.holdAmbientColor != vColor:
            if self.holdAmbientColor != None:
                button = self.todButtonDict.get(todState)
                if button:
                    button['bg'] = getTkColorString(self.uncommitedColor)
            self.holdAmbientColor = vColor
            self.saveChanges['state'] = 'normal'
            if self.holdDirectionColor:
                self.todMgr.setFrontLightColor(self.holdDirectionColor)
            if self.holdBackColor:
                self.todMgr.setBackLightColor(self.holdBackColor)
            if self.editor and self.editor.TODPanelLoaded:
                self.editor.objectMgr.currEditedObjInfo.setTodModified(True)
            self.ambientLabel['text'] = '\n%.4s | %.4s | %.4s' % (vColor[0], vColor[1], vColor[2])
        return

    def setDirectionalColorVec(self, color):
        if not self.changesEnabled:
            return
        vColor = Vec4(color[0] / 1.0, color[1] / 1.0, color[2] / 1.0, 1)
        iColor = [int(vColor[0] * 127.5), int(vColor[1] * 127.5), int(vColor[2] * 127.5)]
        if self.todMgr.dlight:
            self.todMgr.setFrontLightColor(vColor)
        self.directionalLabel['bg'] = getTkColorString(self.clipLightValue(iColor))
        todState = self.todVar.get()
        if self.holdDirectionColor != vColor:
            if self.holdDirectionColor != None:
                button = self.todButtonDict.get(todState)
                if button:
                    button['bg'] = getTkColorString(self.uncommitedColor)
            self.holdDirectionColor = vColor
            self.saveChanges['state'] = 'normal'
            if self.editor and self.editor.TODPanelLoaded:
                self.editor.objectMgr.currEditedObjInfo.setTodModified(True)
            self.directionalLabel['text'] = '\n%.4s | %.4s | %.4s' % (vColor[0], vColor[1], vColor[2])
        return

    def setBackColorVec(self, color):
        if not self.changesEnabled:
            return
        vColor = Vec4(color[0] / 1.0, color[1] / 1.0, color[2] / 1.0, 1)
        iColor = [int(vColor[0] * 127.5), int(vColor[1] * 127.5), int(vColor[2] * 127.5)]
        if self.todMgr.shadowLight:
            self.todMgr.setBackLightColor(vColor)
        self.backLightLabel['bg'] = getTkColorString(self.clipLightValue(iColor))
        todState = self.todVar.get()
        if self.holdBackColor != vColor:
            if self.holdBackColor != None:
                button = self.todButtonDict.get(todState)
                if button:
                    button['bg'] = getTkColorString(self.uncommitedColor)
            self.holdBackColor = vColor
            self.saveChanges['state'] = 'normal'
            if self.editor and self.editor.TODPanelLoaded:
                self.editor.objectMgr.currEditedObjInfo.setTodModified(True)
            self.backLightLabel['text'] = '\n%.4s | %.4s | %.4s' % (vColor[0], vColor[1], vColor[2])
        return

    def switchAmbient(self):
        if not self.changesEnabled:
            return
        ambientSwitch = self.ambientSwitchVar.get()
        lightSwitch = self.todMgr.lightSwitch
        newSwitch = [lightSwitch[0], ambientSwitch, lightSwitch[2]]
        todState = self.todVar.get()
        if lightSwitch != newSwitch:
            button = self.todButtonDict.get(todState)
            if button:
                button['bg'] = getTkColorString(self.uncommitedColor)
            self.saveChanges['state'] = 'normal'
            self.todMgr.setLightSwitch(newSwitch)

    def switchFront(self):
        if not self.changesEnabled:
            return
        frontSwitch = self.frontSwitchVar.get()
        lightSwitch = self.todMgr.lightSwitch
        newSwitch = [frontSwitch, lightSwitch[1], lightSwitch[2]]
        todState = self.todVar.get()
        if lightSwitch != newSwitch:
            button = self.todButtonDict.get(todState)
            if button:
                button['bg'] = getTkColorString(self.uncommitedColor)
            self.saveChanges['state'] = 'normal'
            self.todMgr.setLightSwitch(newSwitch)

    def switchBack(self):
        if not self.changesEnabled:
            return
        backSwitch = self.backSwitchVar.get()
        lightSwitch = self.todMgr.lightSwitch
        newSwitch = [lightSwitch[0], lightSwitch[1], backSwitch]
        todState = self.todVar.get()
        if lightSwitch != newSwitch:
            button = self.todButtonDict.get(todState)
            if button:
                button['bg'] = getTkColorString(self.uncommitedColor)
            self.saveChanges['state'] = 'normal'
            self.todMgr.setLightSwitch(newSwitch)

    def changeSky(self):
        if not self.changesEnabled:
            return
        newSkyValue = self.todSkyTypeVar.get()
        skyValue = self.todMgr.skyGroup.lastSky
        todState = self.todVar.get()
        if skyValue != newSkyValue:
            button = self.todButtonDict.get(todState)
            if button:
                button['bg'] = getTkColorString(self.uncommitedColor)
            self.saveChanges['state'] = 'normal'
            self.todMgr.setSkyType(newSkyValue)

    def setFogType(self):
        if not self.changesEnabled:
            return
        newFogType = self.fogTypeVar.get()
        fogType = self.todMgr.fogType
        todState = self.todVar.get()
        if fogType != newFogType:
            button = self.todButtonDict.get(todState)
            if button:
                button['bg'] = getTkColorString(self.uncommitedColor)
            self.saveChanges['state'] = 'normal'
            self.todMgr.setFogType(newFogType)
            self.repackFog()

    def repackFog(self):
        if self.todMgr.fogType == TODGlobals.FOG_LINEAR:
            self.fogRange.pack_forget()
            self.fogLinearRange.pack(fill=BOTH, expand=1, pady=4)
        elif self.todMgr.fogType == TODGlobals.FOG_EXP:
            self.fogRange.pack(fill=BOTH, expand=1, pady=4)
            self.fogLinearRange.pack_forget()
        else:
            self.fogRange.pack_forget()
            self.fogLinearRange.pack_forget()

    def saveChanges(self):
        fogType = self.fogTypeVar.get()
        lightswitch = [bool(self.frontSwitchVar.get()) * 1, bool(self.ambientSwitchVar.get()) * 1, bool(self.backSwitchVar.get()) * 1]
        skyType = self.todSkyTypeVar.get()
        if self.holdFogColor != None and self.holdFogExp != None and self.holdLinearRanges != None and self.holdAmbientColor != None and self.holdDirectionColor != None and self.holdBackColor != None and self.holdSunDirection != None:
            settingDict = {}
            settingDict['Direction'] = self.holdSunDirection
            settingDict['FrontColor'] = self.holdDirectionColor
            settingDict['BackColor'] = self.holdBackColor
            settingDict['AmbientColor'] = self.holdAmbientColor
            settingDict['FogColor'] = self.holdFogColor
            settingDict['FogExp'] = self.holdFogExp
            settingDict['FogLinearRange'] = self.holdLinearRanges
            settingDict['LightSwitch'] = lightswitch
            settingDict['FogType'] = fogType
            settingDict['SkyType'] = skyType
            if self.editor:
                self.todMgr.insertTODSettingDict(TODGlobals.ENV_DATAFILE, self.todMgr.currentState, settingDict)
            else:
                self.todMgr.insertTODSettingDict(self.todMgr.environment, self.todMgr.currentState, settingDict)
        else:
            import pdb
            pdb.set_trace()
        self.holdFogColor = None
        self.holdFogExp = None
        self.holdLinearRanges = None
        self.holdAmbientColor = None
        self.holdDirectionColor = None
        self.holdBackColor = None
        self.holdSunDirection = None
        self.changeTod(self.todMgr.cycleSpeed, self.todMgr.getCurrentIngameTime())
        self.checkButtonsForChange()
        self.setEnableDisable()
        return

    def clearChanges(self):
        todName = TODGlobals.StateDict.get(self.todVar.get())
        if todName:
            if self.editor:
                self.todMgr.revertTODChange(TODGlobals.ENV_DATAFILE, todName)
            else:
                self.todMgr.revertTODChange(self.todMgr.environment, todName)
        self.holdFogColor = None
        self.holdFogExp = None
        self.holdLinearRanges = None
        self.holdAmbientColor = None
        self.holdDirectionColor = None
        self.holdBackColor = None
        self.holdSunDirection = None
        self.changeTod(self.todMgr.cycleSpeed, self.todMgr.getCurrentIngameTime())
        self.checkButtonsForChange()
        self.setEnableDisable()
        return

    def undoChanges(self):
        self.changeTod(self.todMgr.cycleSpeed, self.todMgr.getCurrentIngameTime())

    def clipLightValue(self, color, clipValue=255.0):
        vColor = Vec4(color[0], color[1], color[2], 1)
        if vColor[0] > clipValue:
            vColor[0] = clipValue
        if vColor[1] > clipValue:
            vColor[1] = clipValue
        if vColor[2] > clipValue:
            vColor[2] = clipValue
        if vColor[0] < 0.0:
            vColor[0] = 0.0
        if vColor[1] < 0.0:
            vColor[1] = 0.0
        if vColor[2] < 0.0:
            vColor[2] = 0.0
        return vColor

    def printSettings(self):
        if self.editor:
            print self.todMgr.getEnviroDictString(environment=TODGlobals.ENV_DATAFILE, tabs=1, heading="'TodSettings' :")
            print ''
            print self.todMgr.listAlteredTODs(TODGlobals.ENV_DATAFILE)
        else:
            f = open('NewTODData.py', 'w')
            importString1 = 'from pandac.PandaModules import Point3, VBase3, Vec4, Vec3\n'
            importString2 = 'from pirates.piratesbase.TODDefs import *\n'
            f.write(importString1)
            f.write(importString2)
            for environment in TODGlobals.ENVIRONMENT_ID_SETTING_DICT:
                if environment == TODGlobals.ENV_DATAFILE:
                    pass
                else:
                    envHeading = '%s = ' % TODGlobals.ENVIRONMENT_ID_SETTING_DICT[environment]
                    outString = self.todMgr.getEnviroDictString(environment=environment, tabs=0, heading=envHeading)
                    f.write('\n')
                    print outString
                    f.write(outString)

            f.write('\n')
            f.close()
