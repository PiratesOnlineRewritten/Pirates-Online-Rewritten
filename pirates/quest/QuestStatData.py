

class QuestStatData():
    EnemyDefeatTime = 0.00833333
    ShipDefeatTime = 0.05
    VoyageTime = 0.11666666
    PokerGoldTime = 0.02
    GoldTime = 0.02
    TreasureTime = 0.01666666
    VisitTime = 0.01666666
    Tasks = {}
    Enemies = {}
    Misc = {}

    def incrementTasks(self, name, count=1):
        if not self.Tasks.has_key(name):
            self.Tasks[name] = count
        else:
            self.Tasks[name] = self.Tasks[name] + count

    def incrementEnemies(self, name, count=1):
        if not self.Enemies.has_key(name):
            self.Enemies[name] = count
        else:
            self.Enemies[name] = self.Enemies[name] + count

    def incrementMisc(self, name, count=1):
        if not self.Misc.has_key(name):
            self.Misc[name] = count
        else:
            self.Misc[name] = self.Misc[name] + count

    def computeTime(self):
        self.totalEnemyTime = self.Misc.get('totalEnemies') * self.EnemyDefeatTime
        self.totalShipTime = self.Misc.get('totalShips') * self.ShipDefeatTime
        self.totalQuestFightTime = self.totalEnemyTime + self.totalShipTime
        self.totalVoyageTime = self.Misc.get('voyages') * self.VoyageTime
        self.pokerGoldTime = self.Misc.get('poker-gold') * self.PokerGoldTime
        self.goldTime = self.Misc.get('gold') * self.GoldTime - self.pokerGoldTime
        self.treasureTime = self.Misc.get('treasures') * self.TreasureTime
        self.visitTime = self.Misc.get('visits') * self.VisitTime
        self.totalTime = self.totalQuestFightTime + self.totalVoyageTime + self.goldTime + self.TreasureTime + self.visitTime

    def __repr__(self):
        self.computeTime()
        argStr = ''
        for name, value in self.Tasks.items():
            argStr += '%s=%s,' % (name, repr(self.Tasks[name]))

        for name, value in self.Enemies.items():
            argStr += '%s=%s,' % (name, repr(self.Enemies[name]))

        for name, value in self.Misc.items():
            argStr += '%s=%s,' % (name, repr(self.Misc[name]))

        argStr += 'totalEnemyFightTime=%s,' % self.totalEnemyTime
        argStr += 'totalShipFightTime=%s,' % self.totalShipTime
        argStr += 'totalQuestFightTime=%s,' % self.totalQuestFightTime
        argStr += 'totalVoyageTime=%s,' % self.totalVoyageTime
        argStr += 'pokerTime=%s,' % self.pokerGoldTime
        argStr += 'goldTime=%s,' % self.goldTime
        argStr += 'treasureTime=%s,' % self.treasureTime
        argStr += 'visitTime=%s,' % self.visitTime
        argStr += 'totalTime=%s,' % self.totalTime
        return '%s(%s)' % (self.__class__.__name__, argStr)