import math

from panda3d.core import *

from otp.nametag import NametagGlobals
from otp.nametag.MarginPopup import MarginPopup
from otp.nametag.Nametag import Nametag
from otp.nametag.NametagConstants import *


class Nametag2d(Nametag, MarginPopup):

    def __init__(self):
        Nametag.__init__(self, 8.0)
        MarginPopup.__init__(self)

        self.copied_np = None
        self.attached_np = None
        self.arrow = None
        self.unknown_np = None

        # self.setCullCallback()
        self.cbNode = CallbackNode(self.getName() + '-cbNode')
        self.cbNode.setCullCallback(PythonCallbackObject(self.cullCallback))
        self.addChild(self.cbNode)

        self.setName('unnamed')

        self.contents = 3
        self.chat_contents = 0
        self.updateContents()
        self.on = NametagGlobals._master_arrows_on
        self.seq2d = 0

        self.trans_vec = Vec3(0, 0, 0)

    def setVisible(self, value):
        self.visible = value
        self.updateContents()

    def manage(self, manager):
        self.updateContents()
        manager.managePopup(self)

    def unmanage(self, manager):
        Nametag.unmanage(self, manager)
        manager.unmanagePopup(self)

    def setObjectCode(self, objcode):
        if self.group:
            self.group.setObjectCode(objcode)

    def getObjectCode(self):
        if self.group:
            return self.group.getObjectCode()

        return 0

    def getScore(self):
        if self.group:
            return 1000 - self.getDistance2()

        return 0

    def getDistance2(self):
        if self.avatar:
            np = self.avatar

        else:
            np = self.group.getAvatar()

        if np.isEmpty():
            return 0

        return np.getPos(NametagGlobals._toon).lengthSquared()

    def considerVisible(self):
        from NametagGroup import NametagGroup

        v2 = 0
        do_update = True
        if self.on != NametagGlobals._master_arrows_on:
            self.on = NametagGlobals._master_arrows_on
            v2 = 1

        if self.seq2d == NametagGlobals._margin_prop_seq:
            if not v2:
                do_update = False

        else:
            self.seq2d = NametagGlobals._margin_prop_seq

        if do_update:
            self.updateContents()

        if not self.chat_contents:
            return 0

        result = self.group.nametag3d_flag != 2
        if NametagGlobals._onscreen_chat_forced and self.chat_contents & (Nametag.CSpeech | Nametag.CThought):
            result = 1

        self.group.setNametag3dFlag(0)
        if result and self.group.getColorCode() in (NametagGroup.CCToonBuilding,
                                                      NametagGroup.CCSuitBuilding,
                                                      NametagGroup.CCHouseBuilding):
            return self.getDistance2() < 1600

        return result

    def updateContents(self):
        self.stopFlash()
        if self.group:
            self.setName(self.group.getName())

        else:
            self.setName('unnamed')

        if self.copied_np:
            self.copied_np.removeNode()

        if self.attached_np:
            self.attached_np.removeNode()

        if self.arrow:
            self.arrow.removeNode()

        if self.unknown_np:
            self.unknown_np.removeNode()

        self.chat_contents = self.determineContents()
        if not NametagGlobals._master_arrows_on:
            self.chat_contents = self.chat_contents & ~1

        if self.visible and self.isGroupManaged():
            v10 = self.chat_contents
            if v10 & Nametag.CSpeech:
                self.generateChat(NametagGlobals._speech_balloon_2d)

            elif v10 & Nametag.CThought:
                self.generateChat(NametagGlobals._thought_balloon_2d)

            elif v10 & Nametag.CName:
                self.generateName()

    def frameCallback(self):
        if self.visible and self.popup_region:
            self.seq = self.group.region_seq

        if self.group:
            self.group.updateRegions()

    def rotateArrow(self):
        if not self.arrow:
            return

        if self.avatar:
            np = self.avatar

        else:
            np = self.group.getAvatar()

        if not np:
            return

        relpos = np.getPos(NametagGlobals._camera) - NametagGlobals._toon.getPos(NametagGlobals._camera)
        hpr = Vec3(0, 0, -math.atan2(relpos[1], relpos[0]) * 180 / math.pi)
        scale = Vec3(0.5, 0.5, 0.5)
        shear = Vec3(0, 0, 0)

        temp_mat_3 = Mat3()
        composeMatrix(temp_mat_3, scale, shear, hpr)
        arrow_mat = Mat4(temp_mat_3, self.trans_vec)
        self.arrow.setMat(arrow_mat)

    def generateName(self):
        v4 = self.getState()
        v84 = NametagGlobals.getNameFg(self.group.getColorCode(), v4)
        v75 = NametagGlobals.getNameBg(self.group.getColorCode(), v4)
        v75[3] = max(v75[3], NametagGlobals._min_2d_alpha)
        v75[3] = min(v75[3], NametagGlobals._max_2d_alpha)

        v67 = NametagGlobals._card_pad[3] + self.group.name_frame[3]
        v68 = self.group.name_frame[2] - NametagGlobals._card_pad[2]

        wordwrap = self.group.getNameWordwrap()
        v17 = self.cell_width / wordwrap * 2.0
        v66 = 0.333 * (1.0 / v17) - (v68 + v67) * 0.5
        v18 = min(1.0 / v17 - v67, v66)

        v69 = Mat4(v17, 0, 0, 0,
                   0, v17, 0, 0,
                   0, 0, v17, 0,
                   0, 0, v18 * v17, 1.0)
        a3 = v69

        if v75[3] != 0.0:
            card = CardMaker('nametag')
            card.setFrame(self.group.name_frame[0] - NametagGlobals._card_pad[0],
                          self.group.name_frame[1] + NametagGlobals._card_pad[1],
                          v68, v67)
            card.setColor(v75)
            if NametagGlobals._nametag_card:
                card.setSourceGeometry(NametagGlobals._nametag_card.node(),
                                       NametagGlobals._nametag_card_frame)

            self.attached_np = self.np.attachNewNode(card.generate())
            self.attached_np.setMat(v69)
            if v75[3] != 1.0:
                self.attached_np.setTransparency(1)

            if self.has_draw_order:
                bin = config.GetString('nametag-fixed-bin', 'fixed')
                self.attached_np.setBin(bin, self.draw_order)

        self.copied_np = self.group.copyNameTo(self.np)
        self.copied_np.setMat(a3)
        if self.has_draw_order:
            bin = config.GetString('nametag-fixed-bin', 'fixed')
            self.copied_np.setBin(bin, self.draw_order)

        self.copied_np.setColor(v84)
        if v84[3] != 1.0:
            self.copied_np.setTransparency(1)

        reducer = SceneGraphReducer()
        reducer.applyAttribs(self.copied_np.node())
        reducer.applyAttribs(self.attached_np.node())

        if NametagGlobals._arrow_model:
            self.arrow = NametagGlobals._arrow_model.copyTo(self.np)
            if self.has_draw_order:
                bin = config.GetString('nametag-fixed-bin', 'fixed')
                self.arrow.setBin(bin, self.draw_order)

            self.trans_vec = a3.xformPoint(Point3(0, 0, v68 - 1.0))

            color = NametagGlobals.getArrowColor(self.group.getColorCode())
            self.arrow.setColor(color)
            if color[3] != 1.0:
                self.arrow.setTransparency(1)

            self.rotateArrow()

        elif self.arrow:
            self.arrow.removeNode()

        v69 = self.np.getNetTransform().getMat()
        v69 = a3 * v69

        v77 = v69.xformPoint(Point3(self.group.name_frame[0] - NametagGlobals._card_pad[0], 0, v68))
        v80 = v69.xformPoint(Point3(self.group.name_frame[1] + NametagGlobals._card_pad[1], 0, v67))

        frame = Vec4(v77[0], v80[0], v77[2], v80[2])
        self.setRegion(frame, 0)

    def generateChat(self, balloon):
        v5 = self.getState()
        text_color = NametagGlobals.getChatFg(self.group.getColorCode(), v5)
        balloon_color = NametagGlobals.getChatBg(self.group.getColorCode(), v5)

        if self.group.chat_flags & CFQuicktalker:
            balloon_color = self.group.getQtColor()

        balloon_color[3] = max(balloon_color[3], NametagGlobals._min_2d_alpha)
        balloon_color[3] = min(balloon_color[3], NametagGlobals._max_2d_alpha)

        text = self.group.getChat()
        if self.group.name:
            text = '%s: %s' % (self.group.name, text)

        has_page_button = False
        has_quit_button = False
        if not self.group.has_timeout:
            has_page_button = self.group.chat_flags & CFPageButton
            if self.group.getPageNumber() >= self.group.getNumChatPages() - 1:
                if self.group.chat_flags & CFQuitButton:
                    has_page_button = False
                    has_quit_button = True

        page_button = None
        if has_page_button:
            page_button = NametagGlobals.getPageButton(v5)

        elif has_quit_button:
            page_button = NametagGlobals.getQuitButton(v5)

        reversed = self.group.chat_flags & CFReversed
        new_button = [None]
        balloon_result = balloon.generate(text, self.group.getChatFont(), self.wordwrap,
                                          text_color, balloon_color, False,
                                          self.has_draw_order, self.draw_order,
                                          page_button, self.group.willHaveButton(),
                                          reversed, new_button)

        self.unknown_np = self.np.attachNewNode(balloon_result)

        v88 = 8.0  # XXX THIS IS A GUESS
        v49 = 2 * self.cell_width
        a6 = v49 / (v88 + 1.0)
        v50 = balloon.text_height * balloon.hscale
        v85 = balloon.hscale * 5.0
        v88 = v50 * 0.5
        v113 = -(balloon.hscale * 0.5 + v85)
        v51 = -(NametagGlobals._balloon_text_origin[2] + v88)
        v118 = Mat4(a6, 0, 0, 0,
                    0, a6, 0, 0,
                    0, 0, a6, 0,
                    v113 * a6, 0, v51 * a6, 1.0)

        self.unknown_np.setMat(v118)

        reducer = SceneGraphReducer()
        reducer.applyAttribs(self.unknown_np.node())

        v66 = self.np.getNetTransform().getMat()

        # XXX THE LINES BELOW ARE A GUESS
        v67 = v113 * a6
        v68 = v51 * a6
        v94 = v66.xformPoint(Point3(v67, 0.0, v68))
        v97 = v66.xformPoint(Point3(-v67, 0.0, -v68))

        frame = Vec4(v94[0], v97[0], v94[2], v97[2])
        self.setRegion(frame, 0)

    def cullCallback(self, *args):
        self.rotateArrow()
        if self.visible and self.popup_region:
            self.seq = self.group.getRegionSeq()
