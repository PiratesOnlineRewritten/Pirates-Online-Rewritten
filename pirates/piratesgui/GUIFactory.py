from direct.gui.DirectGui import DirectLabel, DirectButton
from pandac.PandaModules import NodePath, TextNode
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PLocalizer
BUTTON_PREFIX = 'button'
STATIC_PREFIX = 'static'
SPRITE_PREFIX = 'sprite'
SEQUENCE_PREFIX = 'sequence'
TEXT_PREFIX = 'text'
LOCATOR_PREFIX = 'locator'
GROUP_PREFIX = 'group'
SCALE_MULTIPLIER = 1.0
TEXT_MULTIPLIER = 0.06
notify = DirectNotifyGlobal.directNotify.newCategory('GUIFactory')

def destroyDirectGUIDict(dict):
    for key in dict:
        if hasattr(dict[key], 'destroy'):
            dict[key].destroy()
        dict[key].removeNode()

    dict.clear()


def generateElements(nodePath, parent):
    elements = _parseChildren(nodePath, parent)
    return elements


def generateButtons(nodePath, parent, **kw):
    return _generateType(nodePath, parent, 'button', **kw)


def generateText(nodePath, parent):
    return _generateType(nodePath, parent, 'text')


def generateStaticElements(nodePath, parent):
    return _generateType(nodePath, parent, 'static')


def _generateType(nodePath, parent, type, **kw):
    elements = _parseChildren(nodePath, parent, elementTypes=[type], **kw)
    if type in elements:
        return elements[type]
    else:
        return {}


def _parseChildren(nodePath, parent, elements={}, elementTypes=None, **kw):
    for i in range(nodePath.getNumChildren()):
        _parseNodePath(nodePath.getChild(i), parent, elements, elementTypes, **kw)

    return elements


def _parseNodePath(nodePath, parent, elements={}, elementTypes=None, **kw):
    prefix = nodePath.getName().split('_')[0]
    notify.debug('parsing %s with prefix %s' % (nodePath.getName(), prefix))
    if elementTypes is None:
        canCreate = prefix in PREFIX_TO_CREATE_CALL
    else:
        canCreate = prefix in PREFIX_TO_CREATE_CALL and prefix in elementTypes
    if canCreate:
        nameAndElement = PREFIX_TO_CREATE_CALL[prefix](nodePath, parent, **kw)
        if prefix not in elements:
            elements[prefix] = {}
        elements[prefix][nameAndElement[0]] = nameAndElement[1]
    else:
        notify.debug('no rule to create element with prefix %s' % prefix)
    return elements


def _parseText(nodePath, parent):
    notify.debug('creating %s' % nodePath.getName()[len(TEXT_PREFIX) + 1:])
    label = DirectLabel(parent=parent, relief=None, text=nodePath.getName()[len(TEXT_PREFIX) + 1:], text_align=TextNode.ACenter, text_scale=0.1, sortOrder=50)
    label.setPos(nodePath.getPos() * SCALE_MULTIPLIER)
    return (
     nodePath.getName()[len(TEXT_PREFIX) + 1:], label)


def _parseStatic(nodePath, parent):
    notify.debug('creating %s' % nodePath.getName()[len(STATIC_PREFIX) + 1:])
    element = NodePath(nodePath.getName()[len(STATIC_PREFIX) + 1:])
    element.reparentTo(parent)
    nodePath.copyTo(element)
    element.setScale(SCALE_MULTIPLIER)
    element.setPos(0, 0, 0)
    return (
     nodePath.getName()[len(STATIC_PREFIX) + 1:], element)


def _parseButton(nodePath, parent, **kw):
    notify.debug('creating %s' % nodePath.getName()[len(BUTTON_PREFIX) + 1:])
    game = nodePath.getName()[len(BUTTON_PREFIX) + 1:]
    text = PLocalizer.Minigame_Repair_Names[game]
    button = _createButton(nodePath=nodePath, parent=parent, canReposition=True, helpText=text, helpPos=(0.0, 0.0, -0.175), helpOpaque=1, helpCenterAlign=True, command=None, extraArgs=[0], **kw)
    return (
     nodePath.getName()[len(BUTTON_PREFIX) + 1:], button)


def _createButton(nodePath, parent, **kw):
    buttonClass = kw.get('buttonClass', DirectButton)
    if 'buttonClass' in kw:
        del kw['buttonClass']
    textLocator = nodePath.find('text_button')
    if textLocator.isEmpty():
        textPos = (0.0, 0.0)
    else:
        textPos = (
         textLocator.getX(), textLocator.getZ())
    args = {}
    args['parent'] = parent
    args['image'] = (nodePath.find('**/idle'), nodePath.find('**/down'), nodePath.find('**/over'), nodePath.find('**/disabled'))
    args['text_pos'] = textPos
    args['text_scale'] = TEXT_MULTIPLIER
    args['relief'] = None
    if 'passNodePathToButton' in kw:
        if kw['passNodePathToButton']:
            args['nodePath'] = nodePath
        del kw['passNodePathToButton']
    for key in kw:
        args[key] = kw[key]

    b = buttonClass(**args)
    b.setScale(SCALE_MULTIPLIER)
    b.setPos(nodePath.getPos() * SCALE_MULTIPLIER)
    return b


PREFIX_TO_CREATE_CALL = {BUTTON_PREFIX: _parseButton,STATIC_PREFIX: _parseStatic,SPRITE_PREFIX: _parseStatic,SEQUENCE_PREFIX: _parseStatic,TEXT_PREFIX: _parseText,LOCATOR_PREFIX: _parseStatic}