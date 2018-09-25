from otp.nametag.ClickablePopup import *
from otp.nametag.MarginPopup import *


class WhisperPopup(ClickablePopup, MarginPopup):
    WTNormal = 0
    WTQuickTalker = 1
    WTSystem = 2
    WTBattleSOS = 3
    WTEmote = 4
    WTToontownBoardingGroup = 5

    def __init__(self, text, font, type):
        ClickablePopup.__init__(self)
        MarginPopup.__init__(self)

        self.text = text
        self.font = font
        self.type = type

        self.np_balloon = None
        self.avname = ''
        self.region = None
        self.mouse_watcher = None
        self.manager = None

        # self.setCullCallback()
        self.cbNode = CallbackNode(self.getName() + '-cbNode')
        self.cbNode.setCullCallback(PythonCallbackObject(self.cullCallback))
        self.addChild(self.cbNode)

        self.time = 0
        self.culled = False
        self.clickable = False
        self.avid = 0
        self.is_player = False
        self.is_player_id = None
        self._state = 3
        self.objcode = 0

    def setClickable(self, avatar_name, avatar_id, is_player_id=False):
        self.clickable = True
        self.avname = avatar_name
        self.avid = avatar_id
        self.is_player_id = is_player_id
        self._state = 0

    def click(self):
        messenger.send('clickedWhisper', [self.avid, self.is_player])

    def considerVisible(self):
        if self.clickable and self.visible and self.mouse_watcher != NametagGlobals._mouse_watcher:
            return False

        if self.seq != NametagGlobals._margin_prop_seq:
            self.seq = NametagGlobals._margin_prop_seq
            self.updateContents()

        return True

    def manage(self, manager):
        self.manager = manager
        manager.managePopup(self)

    def unmanage(self, manager):
        manager.unmanagePopup(self)
        del self.manager

    def cullCallback(self, *args):
        if not self.culled:
            self.culled = True
            self.time = globalClock.getFrameTime()

    def setVisible(self, value):
        MarginPopup.setVisible(self, value)
        self.updateContents()

        if self.clickable:
            if self.region:
                if self.visible:
                    self.mouse_watcher = NametagGlobals._mouse_watcher
                    self.mouse_watcher.addRegion(self.region)

                elif self.mouse_watcher:
                    self.mouse_watcher.removeRegion(self.region)
                    self.mouse_watcher = None

    def setRegion(self, frame, sort):
        if self.region:
            self.region.setFrame(frame)

        else:
            self.region = self._createRegion(frame)

        self.region.setSort(sort)

    def updateContents(self):
        if self.np_balloon:
            self.np_balloon.removeNode()
            self.np_balloon = None

        if self.visible:
            self.generateText(NametagGlobals._speech_balloon_2d, self.text, self.font)

    def generateText(self, balloon, text, font):
        text_color = NametagGlobals.getWhisperFg(self.type, self._state)
        balloon_color = NametagGlobals.getWhisperBg(self.type, self._state)
        balloon_color[3] = max(balloon_color[3], NametagGlobals._min_2d_alpha)
        balloon_color[3] = min(balloon_color[3], NametagGlobals._max_2d_alpha)

        balloon_result = balloon.generate(text, font, 8.0, text_color, balloon_color,
                                          False, False, 0, None, False, False, None)

        self.np_balloon = self.np.attachNewNode(balloon_result)

        v34 = self.cell_width * 0.22222222
        v35 = balloon.text_height * balloon.hscale * 0.5
        v57 = -balloon.hscale * 5.5
        v16 = -(NametagGlobals._balloon_text_origin[2] + v35)

        v64 = Mat4(v34, 0, 0, 0,
                   0, v34, 0, 0,
                   0, 0, v34, 0,
                   v57 * v34, 0, v16 * v34, 1.0)

        self.np_balloon.setMat(v64)

        reducer = SceneGraphReducer()
        reducer.applyAttribs(self.np_balloon.node())

        if self.clickable:
            v22 = self.np.getNetTransform().getMat()
            v39, _, v41 = v22.xformPoint(Point3(v57 * v34, 0.0, v16 * v34))
            v27, _, v28 = v22.xformPoint(Point3(-v57 * v34, 0.0, -v16 * v34))
            self.setRegion(Vec4(v39, v27, v41, v28), 0)

    def setObjectCode(self, objcode):
        self.objcode = objcode

    def getObjectCode(self):
        return self.objcode

    def getScore(self):
        result = 2000

        if self.culled:
            elapsed = globalClock.getFrameTime() - self.time
            result -= elapsed * 200

            # moved from considerManage:
            if elapsed > 15.0:
                self.unmanage(self.manager)

        return result
