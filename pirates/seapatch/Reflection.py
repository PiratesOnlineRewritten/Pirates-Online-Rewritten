from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from otp.otpbase import OTPRender

class Reflection(DirectObject):
    global_reflection = None

    @classmethod
    def getGlobalReflection(self):
        return Reflection.global_reflection

    @classmethod
    def getSkyOnly(self):
        try:
            return base.options.reflection == 1
        except:
            return base.config.GetBool('want-water-reflection-show-through-only', False)

    @classmethod
    def initialize(self, parent):
        if not Reflection.global_reflection:
            buffer_width = 512
            buffer_height = 512
            Reflection.global_reflection = Reflection('reflection', buffer_width, buffer_height, parent, Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
            Reflection.global_reflection.lock = True

    @classmethod
    def uninitialize(self):
        reflection = Reflection.global_reflection
        if reflection:
            reflection.lock = False
            reflection.delete()
        Reflection.global_reflection = None
        return

    def __init__(self, name, width, height, parent, plane=Plane(Vec3(0, 0, 1), Point3(0, 0, 0))):
        DirectObject.__init__(self)
        self.lock = False
        self.parent = parent
        self.plane = plane
        self.name = name
        self.width = width
        self.height = height
        self.reflection_state = True
        self.card_created = False
        self.reflection_card_node_path = None
        self.black_clear_color = VBase4(0.0, 0.0, 0.0, 0.0)
        self.clear_color = self.black_clear_color
        self.reflection_texture = Texture('reflection_buffer')
        if self.reflection_texture:
            self.reflection_texture.setWrapU(Texture.WMClamp)
            self.reflection_texture.setWrapV(Texture.WMClamp)
        p = PNMImage(1, 1, 4)
        p.fill(0, 0, 0)
        p.alphaFill(0)
        t = Texture('black')
        t.load(p)
        t.setKeepRamImage(1)
        t.setCompression(t.CMOff)
        self.black_reflection_texture = t
        self.plane_node = PlaneNode('reflection_plane_' + self.name)
        self.plane_node.setPlane(self.plane)
        self.clip_plane = plane
        self.clip_plane_node = PlaneNode('clip_plane_' + self.name)
        self.clip_plane_node.setPlane(self.clip_plane)
        self.reflection_root = parent.attachNewNode('reflection_root_' + self.name)
        self.reflection_plane_node_path = self.reflection_root.attachNewNode(self.plane_node)
        self.clip_plane_node_path = self.reflection_root.attachNewNode(self.clip_plane_node)
        self.reflection_camera = Camera('reflection_camera_' + self.name)
        self.reflection_camera.setInitialState(RenderState.make(CullFaceAttrib.makeReverse(), ClipPlaneAttrib.make().addOnPlane(self.clip_plane_node_path)))
        self.reflection_camera_node_path = self.reflection_plane_node_path.attachNewNode(self.reflection_camera)
        self.reflection_camera.setCameraMask(OTPRender.ReflectionCameraBitmask)
        self.reflectShowThroughOnly(False)
        self.reflection_buffer = None
        self.__createBuffer()
        self.accept('close_main_window', self.__destroyBuffer)
        self.accept('open_main_window', self.__createBuffer)
        self.accept('texture_state_changed', self.__createBuffer)
        return

    def __destroyBuffer(self):
        if self.reflection_buffer:
            base.graphicsEngine.removeWindow(self.reflection_buffer)
            self.reflection_buffer = None
        return

    def __createBuffer(self):
        self.__destroyBuffer()
        if not base.win.getGsg():
            return
        self.reflection_buffer = base.win.makeTextureBuffer('reflection_buffer' + self.name, self.width, self.height, tex=self.reflection_texture)
        if self.reflection_buffer:
            self.reflection_buffer.setSort(40)
            self.reflection_buffer.setClearColor(self.black_clear_color)
            self.display_region = self.reflection_buffer.makeDisplayRegion()
            self.display_region.setCamera(self.reflection_camera_node_path)
            if base.main_rtt:
                base.graphicsEngine.openWindows()
                self.reflection_buffer.setInverted(0)
            self.enable(self.reflection_state)
        else:
            self.display_region = None
            self.enable(False)
        return

    def createCard(self, bin_name, bin_priority):
        if self.card_created == False:
            reflection_card = CardMaker('reflection_card')
            reflection_card.setFrame(-1.0, 1.0, -1.0, 1.0)
            if self.reflection_texture:
                use_render = True
                if use_render:
                    reflection_card.clearSourceGeometry()
                    reflection_card.setHasUvs(True)
                    geom_node = GeomNode('reflection_card')
                    array = GeomVertexArrayFormat()
                    array.addColumn(InternalName.getVertex(), 4, Geom.NTFloat32, Geom.CClipPoint)
                    array.addColumn(InternalName.getColor(), 4, Geom.NTFloat32, Geom.CColor)
                    array.addColumn(InternalName.getTexcoord(), 2, Geom.NTFloat32, Geom.CTexcoord)
                    format = GeomVertexFormat()
                    format.addArray(array)
                    self.format = GeomVertexFormat.registerFormat(format)
                    vertex_data = GeomVertexData('reflection_card', self.format, Geom.UHStatic)
                    vertex_writer = GeomVertexWriter(vertex_data, 'vertex')
                    color_writer = GeomVertexWriter(vertex_data, 'color')
                    texture_writer = GeomVertexWriter(vertex_data, 'texcoord')
                    triangles = GeomTriangles(Geom.UHStatic)
                    w = 1.0
                    h = 1.0
                    z = 0.0
                    hw = 1.0
                    v0 = Vec4(-w, -h, z, hw)
                    v1 = Vec4(w, -h, z, hw)
                    v2 = Vec4(-w, h, z, hw)
                    v3 = Vec4(w, h, z, hw)
                    c0 = Vec4(1.0, 1.0, 1.0, 1.0)
                    c1 = c0
                    c2 = c0
                    c3 = c0
                    t0 = Vec2(0.0, 0.0)
                    t1 = Vec2(1.0, 0.0)
                    t2 = Vec2(0.0, 1.0)
                    t3 = Vec2(1.0, 1.0)
                    vertex_writer.addData3f(v0[0], v0[1], v0[2])
                    vertex_writer.addData3f(v1[0], v1[1], v1[2])
                    vertex_writer.addData3f(v2[0], v2[1], v2[2])
                    vertex_writer.addData3f(v3[0], v3[1], v3[2])
                    color_writer.addData4f(c0[0], c0[1], c0[2], c0[3])
                    color_writer.addData4f(c1[0], c1[1], c1[2], c1[3])
                    color_writer.addData4f(c2[0], c2[1], c2[2], c2[3])
                    color_writer.addData4f(c3[0], c3[1], c3[2], c3[3])
                    texture_writer.addData2f(t0[0], t0[1])
                    texture_writer.addData2f(t1[0], t1[1])
                    texture_writer.addData2f(t2[0], t2[1])
                    texture_writer.addData2f(t3[0], t3[1])
                    vertex_index = 0
                    triangles.addVertex(vertex_index + 0)
                    triangles.addVertex(vertex_index + 1)
                    triangles.addVertex(vertex_index + 2)
                    triangles.closePrimitive()
                    triangles.addVertex(vertex_index + 1)
                    triangles.addVertex(vertex_index + 3)
                    triangles.addVertex(vertex_index + 2)
                    triangles.closePrimitive()
                    geometry = Geom(vertex_data)
                    geometry.addPrimitive(triangles)
                    geom_node.addGeom(geometry)
                    geometry_node = geom_node
                    reflection_card.setSourceGeometry(geometry_node, Vec4(-1.0, 1.0, -1.0, 1.0))
                reflection_card_node_path = NodePath(reflection_card.generate())
                reflection_card_node_path.setTexture(self.reflection_texture, 1)
                reflection_card_node_path.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOne, ColorBlendAttrib.OOneMinusIncomingColor))
                reflection_card_node_path.setDepthTest(0)
                reflection_card_node_path.setDepthWrite(0)
                reflection_card_node_path.setLightOff()
                reflection_card_node_path.node().setBounds(OmniBoundingVolume())
                reflection_card_node_path.node().setFinal(1)
                mask = 4294967295L
                stencil = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, mask, mask)
                reflection_card_node_path.setAttrib(stencil)
                reflection_card_node_path.setBin(bin_name, bin_priority)
                if use_render:
                    reflection_card_node_path.hide(BitMask32.lowerOn(31))
                    reflection_card_node_path.showThrough(OTPRender.EnviroCameraBitmask)
                    reflection_card_node_path.reparentTo(render)
                else:
                    reflection_card_node_path.reparentTo(render2d)
                self.reflection_card_node_path = reflection_card_node_path
                self.card_created = True

    def setCardReflectionFactor(self, scale):
        pass

    def setLens(self, lens):
        self.lens = lens

    def setClearColor(self, clear_color):
        self.clear_color = clear_color

    def setPlanes(self, plane, clip_plane):
        self.plane = plane
        self.clip_plane = clip_plane
        self.plane_node.setPlane(self.plane)
        self.clip_plane_node.setPlane(self.clip_plane)

    def enable(self, enable):
        if not base.useStencils:
            enable = False
        if enable:
            if self.reflection_buffer != None:
                self.reflection_buffer.setActive(True)
            if self.reflection_card_node_path:
                self.reflection_card_node_path.unstash()
            self.reflection_state = True
        else:
            if self.reflection_buffer != None:
                self.reflection_buffer.setActive(False)
            if self.reflection_card_node_path:
                self.reflection_card_node_path.stash()
            self.reflection_state = False
        return

    def update_reflection(self, lens, reference_node, supports_sky_only=True, sky_only=False):
        if True:
            self.reflection_camera_node_path.node().setLens(lens)
        else:
            near = lens.getNear()
            far = lens.getFar()
            fov = lens.getFov()
            reflection_lens = self.reflection_camera_node_path.node().getLens()
            reflection_lens.setNear(near)
            reflection_lens.setFar(far)
            reflection_lens.setFov(fov)
        if self.reflection_buffer:
            if self.reflection_state:
                self.reflection_buffer.setClearColor(self.clear_color)
            else:
                self.reflection_buffer.setClearColor(self.black_clear_color)
        state = self.reflection_state
        if supports_sky_only == False:
            self.enable(state)
        self.reflection_state = state
        reference_matrix = reference_node.getMat(self.reflection_plane_node_path)
        reflection_matrix = self.plane.getReflectionMat()
        matrix = reference_matrix * reflection_matrix
        self.reflection_camera_node_path.setMat(matrix)

    def update_reflectuion_no_shader(self):
        if self.reflection_card_node_path:
            if self.reflection_state:
                self.reflection_card_node_path.unstash()
            else:
                self.reflection_card_node_path.stash()

    def delete(self):
        if not self.lock:
            if self.reflection_card_node_path:
                self.reflection_card_node_path.removeNode()
            self.reflection_camera_node_path.removeNode()
            self.clip_plane_node_path.removeNode()
            self.reflection_plane_node_path.removeNode()
            self.reflection_root.removeNode()
            self.reflection_buffer.clearRenderTextures()
            self.reflection_buffer.removeAllDisplayRegions()
            self.display_region = None
            self.__destroyBuffer()
            self.ignore('close_main_window')
            self.ignore('open_main_window')
            self.ignore('texture_state_changed')
        return

    def reflectShowThroughOnly(self, reflect_show_through_only):
        if reflect_show_through_only:
            self.reflection_camera.setCameraMask(OTPRender.SkyReflectionCameraBitmask)
            render.hide(OTPRender.ReflectionCameraBitmask | OTPRender.SkyReflectionCameraBitmask)
        else:
            self.reflection_camera.setCameraMask(OTPRender.ReflectionCameraBitmask)
            render.show(OTPRender.ReflectionCameraBitmask | OTPRender.SkyReflectionCameraBitmask)
        self.reflect_show_through_only = reflect_show_through_only