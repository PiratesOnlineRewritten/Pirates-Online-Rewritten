from direct.showbase.PythonUtil import ParamObj

class QuestTaskState(ParamObj):

    class ParamSet(ParamObj.ParamSet):
        Params = {'taskType': None,'progress': 0,'goal': 1,'bonusProgress': 0,'bonusGoal': 0,'attempts': 0,'enemyType': None,'faction': None,'hull': None,'containersSearched': None}

    def acquire(self):
        if not hasattr(self, '_refcount'):
            self._refcount = 0
        self._refcount += 1

    def release(self):
        self._refcount -= 1
        if self._refcount <= 0:
            self.destroy()

    def handleParamChange(self, params):
        self.modified = True

    def isModified(self):
        return getattr(self, 'modified', False)

    def resetModified(self):
        self.modified = False

    def handleProgress(self, num=1):
        if not self.isComplete():
            self.setProgress(max(0, min(self.progress + num, self.goal)))

    def handleProgressBonus(self, num=1):
        if not self.isComplete(bonus=True):
            self.setBonusProgress(max(0, min(self.bonusProgress + num, self.bonusGoal)))

    def forceComplete(self):
        self.setProgress(self.goal)

    def resetProgress(self):
        self.setProgress(0)

    def isComplete(self, bonus=False):
        if bonus:
            return self.bonusProgress >= self.bonusGoal
        else:
            return self.progress >= self.goal

    def hasSearchedContainer(self, containerId):
        return self.containersSearched is not None and containerId in self.containersSearched

    def searchedContainer(self, containerId):
        if self.containersSearched is None:
            self.containersSearched = []
        elif containerId in self.containersSearched:
            return False
        self.containersSearched.append(containerId)
        return True