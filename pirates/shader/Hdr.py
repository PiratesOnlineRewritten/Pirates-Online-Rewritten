from pandac.PandaModules import *
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
from pirates.shader.Blur import *

class Hdr():

    def __init__(self, display_width=1024, display_height=1024, glow=1, glow_glitter=1, dynamic_exposure=1):
        base.hdr = None
        base.main_rtt = None
        self.success = 0
        enable_post_processing = 1
        enable = enable_post_processing
        if base.options:
            enable = 0
            if base.options.shader:
                if base.win and base.win.getGsg() and base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20:
                    if base.options.hdr:
                        enable = enable_post_processing
        attrib = DepthTestAttrib.make(RenderAttrib.MLessEqual)
        render.setAttrib(attrib)
        width = display_width
        height = display_height
        base.post_processing = enable
        activeDisplayRegion = None
        if enable:
            dr = base.win.getActiveDisplayRegion(0)
            if dr:
                activeDisplayRegion = dr
                order = 50
                format = 0

                def createCallback():
                    camera = base.cam
                    camera_parent = camera.getParent()
                    main_camera = Camera(camera.node())
                    main_camera.setCameraMask(OTPRender.EnviroCameraBitmask | OTPRender.MainCameraBitmask)
                    main_camera_node = camera_parent.attachNewNode(main_camera)
                    main_rtt = base.main_rtt
                    mbuffer = main_rtt.getTextureBuffer()
                    if mbuffer:
                        display_region = mbuffer.makeDisplayRegion()
                        display_region.setCamera(main_camera_node)
                        card = mbuffer.getTextureCard()
                        if base.post_processing:
                            parent = None
                        else:
                            parent = render2d
                            card.reparentTo(parent)
                        camera.node().setScene(render)
                        main_rtt.saveCamera(main_camera_node)
                    return

                dependency_array = DependencyArray(createCallback)
                base.dependency_array = dependency_array
                main_rtt = RenderToTexture('main', width, height, order, format, dependency_array=dependency_array)
                base.main_rtt = main_rtt
                mbuffer = main_rtt.getTextureBuffer()
                if mbuffer:
                    dependency_array.enable(True)
                    dependency_array.checkDependencies()
                if base.main_rtt.created:
                    dr.setActive(0)
                else:
                    base.main_rtt.delete()
                    base.main_rtt = None
        source_rtt = base.main_rtt
        if source_rtt:
            base.glow = None
            if base.post_processing and glow:
                scene = render
                camera = base.cam
                add = 0
                order = 51
                base.glow = Glow(width, height, source_rtt, scene, camera, add=add, order=order, glitter=glow_glitter)
                if base.glow.success:
                    pass
                else:
                    base.glow.delete()
                    base.glow = None
            if base.post_processing:
                width = 512
                height = 512
                luminance = 1
                add = 0
                order = 60
                hdr = 1
                hdr_output = 1
                add_glow = 0
                glow_rtt = 0
                average = dynamic_exposure
                if base.glow:
                    add_glow = 1
                    glow_rtt = base.glow.glow_rtt
                if base.main_rtt:
                    base.hdr = Blur(width, height, source_rtt, luminance=luminance, add=add, order=order, hdr=hdr, hdr_output=hdr_output, add_glow=add_glow, glow_rtt=glow_rtt, average=average)
                    if base.hdr.success:
                        if base.glow:
                            base.glow.hdr = base.hdr
                        self.success = 1
                        c = 0.58
                        NametagGlobals.setBalloonModulationColor(VBase4(c, c, c, 1.0))
                    else:
                        if base.glow:
                            base.glow.delete()
                            base.glow = None
                        base.hdr.delete()
                        base.hdr = None
                        base.main_rtt.delete()
                        base.main_rtt = None
                        if activeDisplayRegion:
                            activeDisplayRegion.setActive(1)
        elif base.post_processing:
            if activeDisplayRegion:
                activeDisplayRegion.setActive(1)
        return