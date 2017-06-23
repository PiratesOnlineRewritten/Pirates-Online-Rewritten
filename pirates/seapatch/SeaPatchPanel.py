from pandac.PandaModules import *
from direct.tkwidgets.AppShell import *
from direct.showbase.TkGlobal import *
from tkFileDialog import *
from tkSimpleDialog import askstring
import os
from direct.tkwidgets import Dial
from direct.tkwidgets import Floater
from direct.tkwidgets import Slider
from direct.tkwidgets import VectorWidgets

class SeaPatchPanel(AppShell):
    appversion = '1.0'
    appname = 'SeaPatch Panel'
    frameWidth = 500
    frameHeight = 600
    padx = 0
    pady = 0
    usecommandarea = 0
    usestatusarea = 0
    patch = None
    selected_wave = 0

    def __init__(self, **kw):
        taskMgr.remove('tkLoop')
        spawnTkLoop()
        DGG.INITOPT = Pmw_INITOPT
        optiondefs = (
         (
          'title', self.appname, None),)
        self.defineoptions(kw, optiondefs)
        AppShell.__init__(self)
        self.initialiseoptions(SeaPatchPanel)
        return

    def appInit(self):
        self.widgetDict = {}
        self.variableDict = {}

    def createInterface(self):
        interior = self.interior()
        mainFrame = Frame(interior)
        mainFrame.pack()
        fileMenu = self.menuBar.component('File-menu')
        fileMenu.insert_command(fileMenu.index('Quit'), label='Save Params', command=self.saveWave)
        fileMenu.insert_command(fileMenu.index('Quit'), label='Load Params', command=self.loadWave)
        self.mainNotebook = Pmw.NoteBook(interior)
        self.mainNotebook.pack(fill=BOTH, expand=1)
        geomPage = self.mainNotebook.add('Geometry')
        UVPage = self.mainNotebook.add('UVs')
        shadingPage = self.mainNotebook.add('Shading')
        multiwavePage = self.mainNotebook.add('Multiwave')
        geomFloaterDefs = (
         (
          'Geom', 'Speed', 'Global control of wave speed', self.setOverallSpeed, 0.0, 0.0001), ('Geom', 'Radius', 'Outer Boundary at which wave will completely fade out in amplitude', self.setRadius, 0.0, 0.1), ('Geom', 'Threshold', 'Inner Boundary at which wave will start to fade out its amplitude', self.setThreshold, 0.0, 0.1), ('Geom', 'Height Damping', 'Damp the Bobbing for all floating objects', self.setHDamping, 0.01, 0.01), ('Geom', 'Normal Damping', 'Damp the Rocking for all floating objects', self.setNDamping, 0.01, 0.01))
        shadingFloaterDefs = (
         (
          'Shading', 'Red High', 'Red Value of the High color', self.setHighColorR, 0.0, 0.1), ('Shading', 'Blue High', 'Blue Value of the High color', self.setHighColorB, 0.0, 0.1), ('Shading', 'Green High', 'Green Value of the High color', self.setHighColorG, 0.0, 0.1), ('Shading', 'Alpha High', 'Alpha Value of the High color', self.setHighColorA, 0.0, 0.1), ('Shading', 'Red Low', 'Red Value of the Low color', self.setLowColorR, 0.0, 0.1), ('Shading', 'Blue Low', 'Blue Value of the Low color', self.setLowColorB, 0.0, 0.1), ('Shading', 'Green Low', 'Green Value of the Low color', self.setLowColorG, 0.0, 0.1), ('Shading', 'Alpha Low', 'Alpha Value of the Low color', self.setLowColorA, 0.0, 0.1))
        UVFloaterDefs = (
         (
          'UV', 'UScale', 'Set the U divisor for UV computation', self.setUScale, 0.1, 0.1), ('UV', 'VScale', 'Set the V divisor for UV computation', self.setVScale, 0.1, 0.1), ('UV', 'USpeed', 'The rate at which the texture slides at rest', self.setUSpeed, -100.0, 0.0001), ('UV', 'VSpeed', 'The rate at which the texture slides at rest', self.setVSpeed, -100.0, 0.0001))
        multiwaveFloaterDefs = (
         (
          'MWave', 'Amplitude', 'Amplitude of the waves', self.setMAmplitude, 0.0, 0.01), ('MWave', 'Wavelength', 'Wavelength', self.setMWavelength, -1000.0, 0.0001), ('MWave', 'Speed', 'Speed', self.setMSpeed, 0.01, 0.01), ('MWave', 'WaveDirX', 'Wave X Direction', self.setWaveXDir, -100, 0.01), ('MWave', 'WaveDirY', 'Wave Y Direction', self.setWaveYDir, -100, 0.01), ('MWave', 'Choppiness', 'Wave Choppy Factor', self.setChoppyK, 0.01, 0.01))
        self.createFloaters(geomPage, geomFloaterDefs)
        self.createFloaters(UVPage, UVFloaterDefs)
        self.createFloaters(shadingPage, shadingFloaterDefs)
        self.createOptionMenu(multiwavePage, 'Multiwave', 'Wave Number', 'Select wave number', ('1',
                                                                                                '2',
                                                                                                '3',
                                                                                                '4',
                                                                                                '5',
                                                                                                '6'), self.selectWave)
        self.createCheckbutton(multiwavePage, 'Multiwave', 'Enable', 'Turn On-Off this particular wave', self.switchWaves, 1)
        self.createOptionMenu(multiwavePage, 'Multiwave', 'Wave Target', "Specify the wave's target", ('Height (Z)',
                                                                                                       'U',
                                                                                                       'V'), self.selectWaveTarget)
        self.createOptionMenu(multiwavePage, 'Multiwave', 'Wave Func', "Specify the wave's function", ('Sin',
                                                                                                       'Noise'), self.selectWaveFunc)
        self.createCheckbutton(geomPage, 'Geom', 'WireFrame', 'Toggle WireFrame', self.toggleWF, 0)
        self.createFloaters(multiwavePage, multiwaveFloaterDefs)

    def setPatch(self, patch_var):
        self.patch = patch_var
        self.updateWidgets()

    def updateWidgets(self):
        speed = self.patch.patch.getOverallSpeed()
        self.getWidget('Geom', 'Speed').set(speed, 0)
        radius = self.patch.patch.getRadius()
        self.getWidget('Geom', 'Radius').set(radius, 0)
        threshold = self.patch.patch.getThreshold()
        self.getWidget('Geom', 'Threshold').set(threshold, 0)
        hcolor = self.patch.patch.getHighColor()
        self.getWidget('Shading', 'Red High').set(hcolor[0], 0)
        self.getWidget('Shading', 'Blue High').set(hcolor[1], 0)
        self.getWidget('Shading', 'Green High').set(hcolor[2], 0)
        self.getWidget('Shading', 'Alpha High').set(hcolor[3], 0)
        lcolor = self.patch.patch.getLowColor()
        self.getWidget('Shading', 'Red Low').set(lcolor[0], 0)
        self.getWidget('Shading', 'Blue Low').set(lcolor[1], 0)
        self.getWidget('Shading', 'Green Low').set(lcolor[2], 0)
        self.getWidget('Shading', 'Alpha Low').set(lcolor[3], 0)
        uvscale = self.patch.patch.getUvScale()
        pus = self.patch.patch.getUvSpeed()
        self.getWidget('UV', 'USpeed').set(pus[0], 0)
        self.getWidget('UV', 'VSpeed').set(pus[1], 0)
        self.getWidget('UV', 'UScale').set(uvscale[0], 0)
        self.getWidget('UV', 'VScale').set(uvscale[1], 0)
        wamplitude = self.patch.patch.getWaveAmplitude(self.selected_wave)
        wlength = self.patch.patch.getWaveLength(self.selected_wave)
        wspeed = self.patch.patch.getWaveSpeed(self.selected_wave)
        wenabled = self.patch.patch.isWaveEnabled(self.selected_wave)
        if wenabled == 1:
            self.getWidget('Multiwave', 'Enable').select()
        elif wenabled == 0:
            self.getWidget('Multiwave', 'Enable').deselect()
        self.getWidget('MWave', 'Amplitude').set(wamplitude, 0)
        self.getWidget('MWave', 'Wavelength').set(wlength, 0)
        self.getWidget('MWave', 'Speed').set(wspeed, 0)
        wd = self.patch.patch.getWaveDirection(self.selected_wave)
        k = self.patch.patch.getChoppyK(self.selected_wave)
        self.getWidget('MWave', 'WaveDirX').set(wd[0], 0)
        self.getWidget('MWave', 'WaveDirY').set(wd[1], 0)
        self.getWidget('MWave', 'Choppiness').set(k, 0)
        hd = self.patch.patch.getHeightDamper()
        nd = self.patch.patch.getNormalDamper()
        self.getWidget('Geom', 'Height Damping').set(hd, 0)
        self.getWidget('Geom', 'Normal Damping').set(nd, 0)
        wttext = 'unknown'
        wt = self.patch.patch.getWaveTarget(self.selected_wave)
        if wt == SeaPatchRoot.WTZ:
            wttext = 'Height (Z)'
        else:
            if wt == SeaPatchRoot.WTU:
                wttext = 'U'
            elif wt == SeaPatchRoot.WTV:
                wttext = 'V'
            self.getVariable('Multiwave', 'Wave Target').set(wttext)
            wftext = 'unknown'
            wf = self.patch.patch.getWaveFunc(self.selected_wave)
            if wf == SeaPatchRoot.WFSin:
                wftext = 'Sin'
            elif wf == SeaPatchRoot.WFNoise:
                wftext = 'Noise'
        self.getVariable('Multiwave', 'Wave Func').set(wftext)

    def setWavelengthFalloffStart(self, value):
        self.patch.patch.setWavelengthFalloffStart(value)

    def setWavelengthFalloffEnd(self, value):
        self.patch.patch.setWavelengthFalloffEnd(value)

    def selectWaveTarget(self, target):
        if target == 'Height (Z)':
            self.patch.patch.setWaveTarget(self.selected_wave, SeaPatchRoot.WTZ)
        elif target == 'U':
            self.patch.patch.setWaveTarget(self.selected_wave, SeaPatchRoot.WTU)
        elif target == 'V':
            self.patch.patch.setWaveTarget(self.selected_wave, SeaPatchRoot.WTV)

    def selectWaveFunc(self, func):
        if func == 'Sin':
            self.patch.patch.setWaveFunc(self.selected_wave, SeaPatchRoot.WFSin)
        elif func == 'Noise':
            self.patch.patch.setWaveFunc(self.selected_wave, SeaPatchRoot.WFNoise)

    def selectWave(self, type):
        self.selected_wave = int(type) - 1
        self.updateWidgets()

    def toggleUVScaling(self):
        pass

    def toggleNoise(self):
        if self.getVariable('UV', 'UV Noise').get() == 1:
            self.patch.patch.enableNoiseUv()
        elif self.getVariable('UV', 'UV Noise').get() == 0:
            self.patch.patch.disableNoiseUv()

    def switchWaves(self):
        if self.getVariable('Multiwave', 'Enable').get() == 1:
            self.patch.patch.enableWave(self.selected_wave)
        elif self.getVariable('Multiwave', 'Enable').get() == 0:
            self.patch.patch.disableWave(self.selected_wave)

    def loadWave(self):
        fileName = askopenfilename(filetypes=[('SPF', 'spf')], title='Open SeaPatch File')
        if not fileName:
            return
        self.patch.loadSeaPatchFile(fileName)
        self.updateWidgets()

    def saveWave(self):
        fileName = asksaveasfilename(filetypes=[('SPF', 'spf')], title='Save SeaPatch File')
        if not fileName:
            return
        out_file = open(fileName + '.spf', 'w')
        self.patch.saveSeaPatchFile(fileName)

    def setUSlide(self, value):
        self.patch.patch.setUSlide(value)

    def setVSlide(self, value):
        self.patch.patch.setVSlide(value)

    def setColorIn(self, value):
        self.patch.patch.setColorIn(value)

    def setColorOut(self, value):
        self.patch.patch.setColorOut(value)

    def setHDamping(self, value):
        self.patch.patch.setHeightDamper(value)

    def setNDamping(self, value):
        self.patch.patch.setNormalDamper(value)

    def setHighColorR(self, value):
        c = self.patch.patch.getHighColor()
        self.patch.patch.setHighColor(Vec4(value, c[1], c[2], c[3]))

    def setHighColorG(self, value):
        c = self.patch.patch.getHighColor()
        self.patch.patch.setHighColor(Vec4(c[0], value, c[2], c[3]))

    def setHighColorB(self, value):
        c = self.patch.patch.getHighColor()
        self.patch.patch.setHighColor(Vec4(c[0], c[1], value, c[3]))

    def setHighColorA(self, value):
        c = self.patch.patch.getHighColor()
        self.patch.patch.setHighColor(Vec4(c[0], c[1], c[2], value))

    def setLowColorR(self, value):
        c = self.patch.patch.getLowColor()
        self.patch.patch.setLowColor(Vec4(value, c[1], c[2], c[3]))

    def setLowColorG(self, value):
        c = self.patch.patch.getLowColor()
        self.patch.patch.setLowColor(Vec4(c[0], value, c[2], c[3]))

    def setLowColorB(self, value):
        c = self.patch.patch.getLowColor()
        self.patch.patch.setLowColor(Vec4(c[0], c[1], value, c[3]))

    def setLowColorA(self, value):
        c = self.patch.patch.getLowColor()
        self.patch.patch.setLowColor(Vec4(c[0], c[1], c[2], value))

    def setUScale(self, value):
        uvScale = self.patch.patch.getUvScale()
        self.patch.patch.setUvScale(VBase2(value, uvScale[1]))

    def setVScale(self, value):
        uvScale = self.patch.patch.getUvScale()
        self.patch.patch.setUvScale(VBase2(uvScale[0], value))

    def setUSpeed(self, value):
        pm = self.patch.patch.getUvSpeed()
        self.patch.patch.setUvSpeed(Vec2(value, pm[1]))

    def setVSpeed(self, value):
        pm = self.patch.patch.getUvSpeed()
        self.patch.patch.setUvSpeed(Vec2(pm[0], value))

    def setMAmplitude(self, value):
        self.patch.patch.setWaveAmplitude(self.selected_wave, value)

    def setMWavelength(self, value):
        self.patch.patch.setWaveLength(self.selected_wave, value)

    def setMSpeed(self, value):
        self.patch.patch.setWaveSpeed(self.selected_wave, value)

    def setOverallSpeed(self, value):
        self.patch.patch.setOverallSpeed(value)

    def setRadius(self, value):
        self.patch.patch.setRadius(value)

    def setThreshold(self, value):
        self.patch.patch.setThreshold(value)

    def setChoppyK(self, value):
        self.patch.patch.setChoppyK(self.selected_wave, value)

    def setWaveXDir(self, value):
        wd = self.patch.patch.getWaveDirection(self.selected_wave)
        self.patch.patch.setWaveDirection(self.selected_wave, Vec2(value, wd[1]))

    def setWaveYDir(self, value):
        wd = self.patch.patch.getWaveDirection(self.selected_wave)
        self.patch.patch.setWaveDirection(self.selected_wave, Vec2(wd[0], value))

    def toggleWF(self):
        base.toggleWireframe()

    def SetIt(self):
        pass

    def createCheckbutton(self, parent, category, text, balloonHelp, command, initialState, side='top'):
        bool = BooleanVar()
        bool.set(initialState)
        widget = Checkbutton(parent, text=text, anchor=W, variable=bool)
        widget['command'] = command
        widget.pack(fill=X, side=side)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        self.variableDict[category + '-' + text] = bool
        return widget

    def createRadiobutton(self, parent, side, category, text, balloonHelp, variable, value, command):
        widget = Radiobutton(parent, text=text, anchor=W, variable=variable, value=value)
        widget['command'] = command
        widget.pack(side=side, fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createFloaters(self, parent, widgetDefinitions):
        widgets = []
        for category, label, balloonHelp, command, min, resolution in widgetDefinitions:
            widgets.append(self.createFloater(parent, category, label, balloonHelp, command, min, resolution))

        return widgets

    def createFloater(self, parent, category, text, balloonHelp, command=None, min=0.0, resolution=None, numDigits=4, **kw):
        kw['text'] = text
        kw['min'] = min
        kw['resolution'] = resolution
        kw['numDigits'] = numDigits
        widget = apply(Floater.Floater, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createAngleDial(self, parent, category, text, balloonHelp, command=None, **kw):
        kw['text'] = text
        kw['style'] = 'mini'
        widget = apply(Dial.AngleDial, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createSlider(self, parent, category, text, balloonHelp, command=None, min=0.0, max=1.0, resolution=0.001, **kw):
        kw['text'] = text
        kw['min'] = min
        kw['max'] = max
        kw['resolution'] = resolution
        widget = apply(Slider.Slider, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createVector2Entry(self, parent, category, text, balloonHelp, command=None, **kw):
        kw['text'] = text
        widget = apply(VectorWidgets.Vector2Entry, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createVector3Entry(self, parent, category, text, balloonHelp, command=None, **kw):
        kw['text'] = text
        widget = apply(VectorWidgets.Vector3Entry, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createColorEntry(self, parent, category, text, balloonHelp, command=None, **kw):
        kw['text'] = text
        widget = apply(VectorWidgets.ColorEntry, (parent,), kw)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def createOptionMenu(self, parent, category, text, balloonHelp, items, command):
        optionVar = StringVar()
        if len(items) > 0:
            optionVar.set(items[0])
        widget = Pmw.OptionMenu(parent, labelpos=W, label_text=text, label_width=12, menu_tearoff=1, menubutton_textvariable=optionVar, items=items)
        widget['command'] = command
        widget.pack(fill=X)
        self.bind(widget.component('menubutton'), balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        self.variableDict[category + '-' + text] = optionVar
        return optionVar

    def createComboBox(self, parent, category, text, balloonHelp, items, command, history=0):
        widget = Pmw.ComboBox(parent, labelpos=W, label_text=text, label_anchor='w', label_width=12, entry_width=16, history=history, scrolledlist_items=items)
        widget.configure(entryfield_entry_state='disabled')
        if len(items) > 0:
            widget.selectitem(items[0])
        widget['selectioncommand'] = command
        widget.pack(side='left', expand=0)
        self.bind(widget, balloonHelp)
        self.widgetDict[category + '-' + text] = widget
        return widget

    def getWidget(self, category, text):
        return self.widgetDict[category + '-' + text]

    def getVariable(self, category, text):
        return self.variableDict[category + '-' + text]