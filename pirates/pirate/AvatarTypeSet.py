from pirates.pirate.AvatarType import AvatarType

class AvatarTypeSet(AvatarType):

    def __init__(self, strings, *avatarTypes):
        self._strings = strings
        self._sortedTypes = makeList(avatarTypes)
        self._sortedTypes.sort()

    def getAvatarTypes(self):
        return self._sortedTypes

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if len(self._avatarTypes) != len(other._avatarTypes):
            return False
        return self._sortedTypes == other._sortedTypes

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return True
        if len(self._avatarTypes) != len(other._avatarTypes):
            return True
        return self._sortedTypes != other._sortedTypes

    def __cmp__(self, other):
        return hash(self) - hash(other)(self.faction, self.track, self.id)

    def isA(self, other):
        for type in self._sortedTypes:
            if not type.isA(other):
                return False

        return True

    def _contains(self, other):
        for type in self._sortedTypes:
            if other.isA(type):
                return True

        return False

    def getName(self):
        return self._strings[0]

    def getStrings(self):
        return self._strings[1]

    def __hash__(self):
        h = hash(tuple(self._sortedTypes))
        if hasattr(self, '_hash'):
            if h != self._hash:
                raise 'inconsistent AvatarType hash values: %s, %s' % (h, self._hash)
        else:
            self._hash = h
        return h

    def __str__(self):
        return 'AvatarTypeSet(%s)' % self.getName()

    def __repr__(self):
        return 'AvatarTypeSet%s' % self._sortedTypes