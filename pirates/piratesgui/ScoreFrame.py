from pirates.piratesgui.SheetFrame import SheetFrame

class ScoreFrame(SheetFrame):

    def __init__(self, w, h, holder, team, **kw):
        self.team = team
        title = holder.getTeamName(self.team)
        SheetFrame.__init__(self, w, h, title, holder, **kw)
        self.initialiseoptions(ScoreFrame)
        self.scoreChanged = False

    def getItemList(self):
        return self.holder.getItemList(self.team)

    def _handleItemChange(self):
        self.scoreChanged = True

    def show(self):
        if self.scoreChanged:
            self.scoreChanged = False
            self.redraw()
        SheetFrame.show(self)