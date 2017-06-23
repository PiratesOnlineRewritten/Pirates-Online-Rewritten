from direct.distributed.ClockDelta import globalClockDelta
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TODGlobals
import time

class TimeOfDayManagerBase():
    from direct.directnotify import DirectNotifyGlobal
    notify = DirectNotifyGlobal.directNotify.newCategory('TimeOfDayManagerBase')

    def __init__(self):
        self.timeOfDayMethodList = []
        self.waitingMethod = None
        self.timeOfDayToggleList = []
        self.toggleOnDict = {}
        self.waitingToggle = None
        self.togglesOn = 0
        return

    def printNumbers(self, num1, num2):
        print 'Print Numbers %s %s' % (num1, num2)

    def printTime(self, index=None):
        print 'Print Index %s Time %s' % (index, self.getCurrentIngameTime())

    def addthingy(self):
        self.addTimeOfDayMethod(12.0, 'noonthing', self.printNumbers, (42, 69))

    def addTMs(self):
        self.addTimeOfDayMethod(12.0, 'one', self.printTime, (1, ))
        self.addTimeOfDayMethod(12.0, 'two', self.printTime, (2, ))
        self.addTimeOfDayMethod(12.0, 'three', self.printTime, (3, ))
        self.addTimeOfDayMethod(12.0, 'four', self.printTime, (4, ))
        self.addTimeOfDayMethod(19.0, 'a', self.printTime, (5, ))
        self.addTimeOfDayMethod(19.0, 'b', self.printTime, (6, ))
        self.addTimeOfDayMethod(19.0, 'c', self.printTime, (7, ))
        self.addTimeOfDayMethod(19.0, 'd', self.printTime, (8, ))

    def addTT(self):
        self.addTimeOfDayToggle('day-night', 8.0, 20.0, self.printTime, ('day', ), self.printTime, ('night', ))
        self.addTimeOfDayToggle('midday', 12.0, 0.0, self.printTime, [1], self.printTime, [2])

    def queryTimeOfDayToggle(self, uniqueName):
        for toggle in self.timeOfDayToggleList:
            if toggle[0] == uniqueName:
                return True

        return False

    def addTimeOfDayToggle(self, uniqueName, startTime, endTime, startMethod=None, startArgs=[], endMethod=None, endArgs=[]):
        returnVal = 1
        returnFlip = 0
        if endTime < startTime:
            holdTime = startTime
            startTime = endTime
            endTime = holdTime
            holdMethod = startMethod
            startMethod = endMethod
            endMethod = holdMethod
            holdArgs = startArgs
            startArgs = endArgs
            endArgs = holdArgs
            returnFlip = 1
        skipAdds = False
        for toggle in self.timeOfDayToggleList:
            if toggle[0] == uniqueName:
                skipAdds = True
                break

        currentInGameTime = self.getCurrentIngameTime()
        if currentInGameTime >= startTime and currentInGameTime < endTime:
            if returnFlip:
                returnVal = 0
            else:
                returnVal = 1
        elif returnFlip:
            returnVal = 1
        else:
            returnVal = 0
        if self.togglesOn and not skipAdds:
            self.timeOfDayToggleList.append([uniqueName, startTime, endTime, startMethod, startArgs, endMethod, endArgs])
            toggleOn = 0
            if currentInGameTime >= startTime and currentInGameTime < endTime:
                toggleOn = 1
                startMethod(*startArgs)
            else:
                endMethod(*endArgs)
            self.toggleOnDict[uniqueName] = toggleOn
            self.processTimeOfDayToggles()
        return returnVal

    def checkTimeOfDayToggle(self, nameToCheck):
        for toggle in self.timeOfDayToggleList:
            if toggle[0] == nameToCheck:
                return 1

        return 0

    def removeTimeOfDayToggle(self, nameToRemove):
        removeList = []
        for toggle in self.timeOfDayToggleList:
            if toggle[0] == nameToRemove:
                removeList.append(toggle)

        for toggle in removeList:
            self.timeOfDayToggleList.remove(toggle)
            del self.toggleOnDict[toggle[0]]

    def startTodToggles(self):
        self.togglesOn = 1
        self.processTimeOfDayToggles()

    def processTimeOfDayToggles(self, task=None):
        currentInGameTime = self.getCurrentIngameTime()
        if not self.togglesOn:
            return
        taskMgr.remove('timeOfDayToggles')
        self.doTimeOfDayToggles(currentInGameTime)
        self.waitForNextToggle(currentInGameTime)
        if task:
            return task.done

    def doTimeOfDayToggles(self, currentInGameTime=None):
        if currentInGameTime == None:
            currentInGameTime = self.getCurrentIngameTime()
        for toggle in self.timeOfDayToggleList:
            toggleStart = toggle[1]
            toggleEnd = toggle[2]
            toggleOn = self.toggleOnDict[toggle[0]]
            if currentInGameTime >= toggleStart:
                if currentInGameTime < toggleEnd:
                    method = toggle[3]
                    toggleArgs = toggle[4]
                    toggleOn or method(*toggleArgs)
                    self.toggleOnDict[toggle[0]] = 1
            else:
                method = toggle[5]
                toggleArgs = toggle[6]
                if toggleOn:
                    method(*toggleArgs)
                    self.toggleOnDict[toggle[0]] = 0

        return

    def waitForNextToggle(self, currentInGameTime=None):
        if currentInGameTime == None:
            currentInGameTime = self.getCurrentIngameTime()
        nextToggleTime = None
        shortestWait = None
        for toggle in self.timeOfDayToggleList:
            startToggle = toggle[1]
            if currentInGameTime > startToggle:
                timeToToggle = PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY + startToggle
            else:
                timeToToggle = startToggle
            if timeToToggle < 0.0:
                pass
            if nextToggleTime == None or nextToggleTime > timeToToggle:
                nextToggleTime = timeToToggle
            endToggle = toggle[2]
            if currentInGameTime > endToggle:
                timeToToggle = PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY + endToggle
            else:
                timeToToggle = endToggle
            if timeToToggle < 0.0:
                set_trace()
            if nextToggleTime == None or nextToggleTime > timeToToggle:
                nextToggleTime = timeToToggle
            if nextToggleTime != None:
                cycleSpeed = self.cycleSpeed
                if cycleSpeed <= 0:
                    cycleSpeed = 1
                REALSECONDS_PER_GAMEDAY = PiratesGlobals.TOD_REALSECONDS_PER_GAMEDAY / cycleSpeed
                REALSECONDS_PER_GAMEHOUR = float(REALSECONDS_PER_GAMEDAY / PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY)
                timeDiff = nextToggleTime - currentInGameTime
                waitTime = timeDiff * REALSECONDS_PER_GAMEHOUR
                if waitTime < 0:
                    pass
                if shortestWait == None or waitTime < shortestWait:
                    shortestWait = waitTime

        if shortestWait != None:
            taskMgr.doMethodLater(shortestWait + 0.5, self.processTimeOfDayToggles, 'timeOfDayToggles')
        return

    def addTimeOfDayMethod(self, time, uniqueName, method, extraArgs=None):
        timeIndex = 0
        methodTuple = (time, uniqueName, method, extraArgs)
        for entry in self.timeOfDayMethodList:
            if entry[1] == uniqueName:
                pass

        self.timeOfDayMethodList.append(methodTuple)
        sortedList = sorted(self.timeOfDayMethodList, key=lambda methodTuple: methodTuple[timeIndex])
        self.timeOfDayMethodList = sortedList
        indexWaiting = None
        if self.waitingMethod in self.timeOfDayMethodList:
            indexWaiting = self.timeOfDayMethodList.index(self.waitingMethod)
            indexAdded = self.timeOfDayMethodList.index(methodTuple)
            if indexAdded == indexWaiting + 1 or indexAdded == len(self.timeOfDayMethodList) - 1 and indexWaiting == 0:
                self.restartTimeOfDayMethod()
        else:
            self.restartTimeOfDayMethod()
        return

    def gameHoursToRealSeconds(self, hours):
        cycleSpeed = self.cycleSpeed
        if cycleSpeed <= 0:
            cycleSpeed = 1
        REALSECONDS_PER_GAMEDAY = PiratesGlobals.TOD_REALSECONDS_PER_GAMEDAY / cycleSpeed
        REALSECONDS_PER_GAMEHOUR = float(REALSECONDS_PER_GAMEDAY / PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY)
        return float(hours) * float(REALSECONDS_PER_GAMEHOUR)

    def restartTimeOfDayMethod(self):
        taskMgr.remove('timeOfDayMethod')
        cycleSpeed = self.cycleSpeed
        if cycleSpeed <= 0:
            cycleSpeed = 1
        REALSECONDS_PER_GAMEDAY = PiratesGlobals.TOD_REALSECONDS_PER_GAMEDAY / cycleSpeed
        REALSECONDS_PER_GAMEHOUR = float(REALSECONDS_PER_GAMEDAY / PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY)
        currentInGameTime = self.getCurrentIngameTime()
        nextMethod = None
        timeToNextMethod = None
        if not self.timeOfDayMethodList or len(self.timeOfDayMethodList) == 0:
            return
        for method in self.timeOfDayMethodList:
            methodTime = method[0]
            timeToMethod = methodTime - currentInGameTime
            if timeToMethod < 0.0:
                timeToMethod += 24.0
            timeToMethod %= 24.0
            if not nextMethod or timeToNextMethod > timeToMethod:
                nextMethod = method
                timeToNextMethod = timeToMethod

        self.waitingMethod = nextMethod
        waitTime = timeToNextMethod * REALSECONDS_PER_GAMEHOUR
        taskMgr.doMethodLater(waitTime, self.processTODMethod, 'timeOfDayMethod')
        return

    def processTODMethod(self, task=None):
        indexWaiting = self.timeOfDayMethodList.index(self.waitingMethod)
        methodToProcess = self.waitingMethod[2]
        methodArgs = self.waitingMethod[3]
        testIndex = indexWaiting
        sizeOfTasks = len(self.timeOfDayMethodList)
        firstWaiting = self.waitingMethod
        if testIndex <= sizeOfTasks - 1:
            for index in range(testIndex, sizeOfTasks):
                method = self.timeOfDayMethodList[index]
                if method[0] == self.waitingMethod[0]:
                    methodToProcess = method[2]
                    methodArgs = method[3]
                    if methodArgs == None:
                        methodToProcess()
                    else:
                        methodToProcess(*methodArgs)
                    self.waitingMethod = method

        self.restartTimeOfDayMethod()
        return task.done

    def removeTimeOfDayMethod(self, uniqueName):
        needRestart = 0
        if self.waitingMethod and self.waitingMethod[1] == uniqueName:
            needRestart = 1
            self.waitingMethod = None
            self.restartTimeOfDayMethod()
        removeList = []
        for methodTuple in self.timeOfDayMethodList:
            if methodTuple[1] == uniqueName:
                removeList.append(methodTuple)

        for tupleToRemove in removeList:
            self.timeOfDayMethodList.remove(tupleToRemove)

        if needRestart:
            self.restartTimeOfDayMethod()
        return