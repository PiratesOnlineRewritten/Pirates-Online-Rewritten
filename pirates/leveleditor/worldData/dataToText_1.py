import direct
import sys
dataFileName = sys.argv[1]
dataModule = dataFileName.split('.py')[0]
textFileName = dataModule + '.txt'
print 'Parsing %s.py --> %s\n' % (dataModule, textFileName)
exec 'from pirates.leveleditor.worldData.%s import *' % dataModule
lines = []
for mainUid in objectStruct['Objects']:
    mainObj = objectStruct['Objects'][mainUid]
    lines.append('Name:\t%s\t%s\nType:\t%s\n\n' % (mainObj['Name'], mainUid, mainObj['Type']))

def printObjects(obj):
    for uid in obj['Objects']:
        object = obj['Objects'][uid]
        line = ''
        if object['Type'] == 'Player Spawn Node':
            pass
        elif object['Type'] == 'Spawn Node':
            line = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (dataModule, obj['Type'], uid, object['Type'], object['Spawnables'], object['Team'], object['Min Population'], `(object['Pos'])`)
        elif object['Type'] == 'Object Spawn Node':
            line = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (dataModule, obj['Type'], uid, object['Type'], object['Spawnables'], object['SpawnDelay'], object['startingDepth'], `(object['Pos'])`)
        elif object['Type'] == 'Searchable Container':
            line = '%s\t%s\t%s\t%s\t%s\t%s\t\t%s\n' % (dataModule, obj['Type'], uid, object['Type'], object['type'], object['searchTime'], `(object['Pos'])`)
        elif object['Type'] == 'Townsperson':
            line = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (dataModule, obj['Type'], uid, object['Type'], object['Category'], object['Start State'], object['Team'], `(object['Pos'])`)
        elif 'Objects' in object:
            printObjects(object)
        lines.append(line)


lines.append('\n')
for mainUid in objectStruct['Objects']:
    mainObj = objectStruct['Objects'][mainUid]
    printObjects(mainObj)

textFile = file(textFileName, 'w')
textFile.writelines(lines)
textFile.close()