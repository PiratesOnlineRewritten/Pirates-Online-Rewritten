from pirates.piratesgui import NonPayerPanel
from pirates.piratesbase import PLocalizer

class StayTunedPanel(NonPayerPanel.NonPayerPanel):

    def configurePanel(self):
        self.NUM_IMAGES = 0
        piccard = loader.loadModel('models/textureCards/velvetpics')
        self.gameImage = [
         (
          piccard.find('**/vr_combat'), piccard.find('**/vr_quest'))]
        self.gameCaption = [
         (
          PLocalizer.VR_Cap_StayTuned1, PLocalizer.VR_Cap_StayTuned2)]
        self.gameHeader = [
         PLocalizer.VR_Head_StayTuned1]
        self.gameDescript = [
         PLocalizer.VR_StayTuned1]

    def __init__(self, w=9.0, h=6.0):
        NonPayerPanel.NonPayerPanel.__init__(self, w, h, False)
        self.upgradeButton['command'] = self.hide
        self.upgradeButton['text'] = PLocalizer.lClose
        self.clickHereButton.hide()
        self.titleText['text'] = PLocalizer.VR_StayTuned
        self.scrollRight.hide()
        self.scrollLeft.hide()
        self.underText.setZ(2.75)
        self.fullText.setZ(2.67)