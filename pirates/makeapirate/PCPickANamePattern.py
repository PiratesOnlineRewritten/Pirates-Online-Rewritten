from direct.showbase.PythonUtil import listToItem2index
from otp.namepanel.PickANamePattern import PickANamePatternTwoPartLastName
from pirates.piratesbase.PiratesGlobals import maleNames, femaleNames, lastNamePrefixesCapped

class PCPickANamePattern(PickANamePatternTwoPartLastName):
    NameParts = None

    def _getNameParts(self, gender):
        if PCPickANamePattern.NameParts is None:
            PCPickANamePattern.NameParts = {}
            maleNameParts = []
            for nameList in maleNames:
                maleNameParts.append(listToItem2index(nameList))

            femaleNameParts = []
            for nameList in femaleNames:
                femaleNameParts.append(listToItem2index(nameList))

            PCPickANamePattern.NameParts['m'] = maleNameParts
            PCPickANamePattern.NameParts['f'] = femaleNameParts
        return PCPickANamePattern.NameParts[gender]

    def _getLastNameCapPrefixes(self):
        return lastNamePrefixesCapped