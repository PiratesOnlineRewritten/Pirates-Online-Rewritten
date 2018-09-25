from panda3d.core import *


class PopupHandle:

    def __init__(self, popup):
        self.popup = popup  # 12
        self.cell = -1  # 16
        self.wants_visible = False  # 20
        self.score = 0  # 24
        self.objcode = id(self)  # 28
        popup.setObjectCode(self.objcode)


class MarginCell:

    def __init__(self):
        self.mat = Mat4()  # 0
        self.cell_width = 0  # 64
        self.popup = None  # 68
        self.np = None  # 72
        self.visible = False  # 84
        self.objcode = 0  # 88
        self.time = 0  # 96


class MarginManager(PandaNode):

    def __init__(self):
        PandaNode.__init__(self, 'margins')

        # self.setCullCallback()
        self.cbNode = CallbackNode(self.getName() + '-cbNode')
        self.cbNode.setCullCallback(PythonCallbackObject(self.cullCallback))
        self.addChild(self.cbNode)

        self.cells = []
        self.popups = {}  # MarginPopup*: PopupHandle
        self.code_map = {}  # code: MarginPopup*
        self.num_available = 0

    def addGridCell(self, a2, a3, a4, a5, a6, a7):
        v7 = (a5 - a4) * 0.16666667
        v8 = (a7 - a6) * 0.16666667
        v15 = v7 * a2 + a4
        v9 = a3 * v8 + a6
        v10 = v9 + v8 - 0.01
        v11 = v9 + 0.01
        v12 = v15 + v7 - 0.01
        v13 = v15 + 0.01
        return self.addCell(v13, v12, v11, v10)

    def addCell(self, left, right, bottom, top):
        v5 = (top - bottom) * 0.5
        v19 = Vec3(v5, 0, 0)
        scale = Vec3(v5, v5, v5)
        shear = Vec3(0, 0, 0)
        trans = Vec3((left + right) * 0.5, 0, (bottom + top) * 0.5)

        v18 = len(self.cells)
        v9 = MarginCell()
        self.cells.append(v9)
        v9.available = True

        mat3 = Mat3()
        composeMatrix(mat3, scale, shear, Vec3(0, 0, 0), 0)
        v9.mat = Mat4(mat3, trans)

        v9.cell_width = (right - left) * 0.5 / v19[0]
        v9.np = None
        v9.popup = None
        v9.objcode = 0
        v9.time = 0.0

        self.num_available += 1
        return v18

    def setCellAvailable(self, a2, a3):
        v5 = self.cells[a2]
        if v5.available:
            self.num_available -= 1

        v5.available = a3
        if v5.available:
            self.num_available += 1

        if v5.np:
            self.hide(a2)
            v5.popup = None
            v5.objcode = 0

    def getCellAvailable(self, a2):
        return self.cells[a2].available

    def cullCallback(self, *args):
        self.update()

    def managePopup(self, a2):
        a2.setManaged(True)
        self.popups[a2] = PopupHandle(a2)
        self.code_map[a2.getObjectCode()] = a2

    def unmanagePopup(self, a2):
        v9 = self.popups.get(a2)
        if v9:
            if v9.cell >= 0:
                self.hide(v9.cell)
                v9.cell = -1

            a2.setManaged(False)
            del self.popups[a2]
            del self.code_map[v9.objcode]

    def hide(self, a2):
        cell = self.cells[a2]
        cell.np.removeNode()
        cell.time = globalClock.getFrameTime()
        if cell.popup:
            cell.popup.setVisible(False)

    def show(self, popup, cell_index):
        v12 = self.cells[cell_index]
        v12.popup = popup
        v12.objcode = popup.getObjectCode()
        v12.np = NodePath.anyPath(self).attachNewNode(popup)
        v12.np.setMat(v12.mat)
        self.popups[popup].cell = cell_index
        popup.cell_width = v12.cell_width
        popup.setVisible(True)

    def chooseCell(self, a2, a3):
        now = globalClock.getFrameTime()
        objcode = a2.getObjectCode()

        for cell in a3:
            v7 = self.cells[cell]
            if (v7.popup == a2 or v7.objcode == objcode) and (now - v7.time) <= 30.0:
                result = cell
                break

        else:
            for cell in a3[::-1][1:]:  # Iterate backwards, skip last item
                v10 = self.cells[cell]
                if (not v10.popup) or (now - v10.time) > 30.0:
                    result = cell
                    break

            else:
                result = a3[-1]

        a3.remove(result)
        return result

    def showVisibleNoConflict(self):
        cells = []
        for i, cell in enumerate(self.cells):
            if cell.available and not cell.np:
                cells.append(i)

        for handle in self.popups.values():
            v7 = handle.popup
            if handle.wants_visible and not v7.isVisible():
                v8 = self.chooseCell(v7, cells)
                self.show(v7, v8)

    def showVisibleResolveConflict(self):
        v4 = []

        for handle in self.popups.values():
            score = 0
            if handle.wants_visible:
                score = handle.score

            v4.append((handle, -score))

        v4 = sorted(v4, key=lambda a: a[-1])
        for handle in v4[self.num_available:]:
            if handle[0].popup.isVisible():
                self.hide(handle[0].cell)
                handle[0].cell = -1

        cells = []
        for i, cell in enumerate(self.cells):
            if cell.available and not cell.np:
                cells.append(i)

        for handle in v4[:self.num_available]:
            v7 = handle[0].popup
            if handle[0].wants_visible and not v7.isVisible():
                v8 = self.chooseCell(v7, cells)
                self.show(v7, v8)

    def update(self):
        num_want_visible = 0

        for handle in self.popups.values():
            popup = handle.popup
            handle.wants_visible = popup.considerVisible()
            if handle.wants_visible and handle.objcode:
                handle.score = popup.getScore()
                num_want_visible += 1

            elif popup.isVisible():
                self.hide(handle.cell)
                handle.cell = -1

        if num_want_visible > self.num_available:
            self.showVisibleResolveConflict()

        else:
            self.showVisibleNoConflict()

        for popup in self.popups:
            popup.frameCallback()
