from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.audio import SoundGlobals
from pirates.effects import FireworkGlobals
from pirates.effects.FireworkGlobals import *
from pirates.effects.Firework import Firework
from pirates.ai import HolidayGlobals
from pirates.piratesbase import TODDefs
import random
colors = [
 Vec4(1, 1, 1, 1), Vec4(1, 0.1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), Vec4(0.3, 1, 0.3, 1), Vec4(0.2, 0.2, 1, 1), Vec4(1, 1, 0.1, 1), Vec4(1, 0.5, 0.1, 1), Vec4(1, 0.1, 1, 1), Vec4(0.1, 1, 1, 1), Vec4(0.1, 0.5, 1, 1)]

class FireworkShow(NodePath):

    def __init__(self, showType):
        NodePath.__init__(self, 'FireworkShow')
        self.showType = showType
        self.sectionIvals = []
        self.fireworks = []

        def r():
            return random.randint(8, 12) / 10.0

        def rV():
            return Vec3(random.randint(-120, 120), random.randint(-120, 120), random.randint(400, 600))

        def rP():
            return Point3(random.randint(-300, 300), random.randint(-50, 50), 0)

        def rS():
            return 0.75 + random.random() / 2.0

        def rC():
            return random.choice(colors)

        def rT():
            return random.randint(12, 20) / 10.0

        def rD():
            return random.randint(1, 20) / 10.0

        self.showData = {HolidayGlobals.FOURTHOFJULY: [[FireworkType.BasicPeony, Vec3(0, 0, 450), Point3(0, 0, 0), 1.0, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 1), 2.0, 3.0], [FireworkType.BasicPeony, Vec3(-60, 20, 550), Point3(-120, 0, 0), 0.8, Vec4(1, 1, 0, 1), -1, 1.8, 0.2], [FireworkType.BasicPeony, Vec3(30, -20, 470), Point3(120, 0, 0), 0.8, rC(), -1, 1.8, 2.5], [FireworkType.AdvancedPeony, Vec3(-120, 20, 500), Point3(-200, 0, 0), 1.0, Vec4(1, 0, 0, 1), -1, rT(), 0.25], [FireworkType.AdvancedPeony, Vec3(0, 0, 500), Point3(0, 0, 0), 1.0, Vec4(0, 1, 0, 1), -1, rT(), 0.25], [FireworkType.AdvancedPeony, Vec3(120, -20, 500), Point3(200, 0, 0), 1.0, Vec4(0.1, 0.1, 1, 1), -1, rT(), 2.5], [FireworkType.BasicPeony, Vec3(-50, 50, 450) * r(), Point3(0, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.AdvancedPeony, Vec3(50, -50, 450) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.BasicPeony, Vec3(-100, 0, 450) * r(), Point3(-200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.AdvancedPeony, Vec3(100, 50, 450) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.BasicPeony, Vec3(100, -50, 450) * r(), Point3(-200, 0, 0), 1.0, rC(), -1, rT(), 1.5], [FireworkType.DiademPeony, Vec3(0, 0, 450) * r(), Point3(0, 0, 0), 1.1, rC(), -1, rT(), 3.0], [FireworkType.AmericanFlag, None, Point3(0, 0, 0), 1.0, None, None, None, 4.0], [FireworkType.GlowFlare, Vec3(-100, 0, 500), Point3(-400, 0, 0), 1.25, Vec4(1, 1, 1, 1), -1, 3.0, 0.0], [FireworkType.GlowFlare, Vec3(100, 0, 500), Point3(400, 0, 0), 1.25, Vec4(1, 1, 1, 1), -1, 3.0, 0.5], [FireworkType.GlowFlare, Vec3(-50, 0, 500), Point3(-250, 0, 0), 1.25, Vec4(0, 1, 0, 1), -1, 3.0, 0.0], [FireworkType.GlowFlare, Vec3(50, 0, 500), Point3(250, 0, 0), 1.25, Vec4(0, 1, 0, 1), -1, 3.0, 0.5], [FireworkType.GlowFlare, Vec3(-25, 0, 500), Point3(-100, 0, 0), 1.25, Vec4(1, 0, 0, 1), -1, 3.0, 0.0], [FireworkType.GlowFlare, Vec3(25, 0, 500), Point3(100, 0, 0), 1.25, Vec4(1, 0, 0, 1), -1, 3.0, 1.0], [FireworkType.DiademChrysanthemum, Vec3(0, 0, 550), Point3(0, 0, 0), 1.25, Vec4(1, 1, 1, 1), -1, 1.5, 2.0], [FireworkType.Ring, Vec3(-100, 50, 500) * r(), Point3(-200, 0, 0), 1.0, rC(), -1, rT(), 0.5], [FireworkType.Ring, Vec3(100, -50, 500) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), 1.5], [FireworkType.Ring, Vec3(0, 0, 550), Point3(0, 50, 0), 1.0, rC(), -1, rT(), 1.5], [FireworkType.Saturn, Vec3(-250, 50, 450), Point3(200, 0, 0), 1.0, rC(), rC(), 1.7, 0.5], [FireworkType.Saturn, Vec3(250, -50, 450), Point3(-200, 0, 0), 1.0, rC(), rC(), 1.7, 1.5], [FireworkType.BasicPeony, Vec3(-150, 100, 500) * r(), Point3(-200, 0, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.AdvancedPeony, Vec3(-50, 100, 500) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.BasicPeony, Vec3(-150, -100, 500) * r(), Point3(0, 50, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.Chrysanthemum, Vec3(175, 100, 500) * r(), Point3(220, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.Ring, Vec3(-75, -100, 500) * r(), Point3(-220, 0, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicPeony, Vec3(0, 100, 500) * r(), Point3(0, 0, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.AdvancedPeony, Vec3(75, 100, 500) * r(), Point3(-200, 0, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicPeony, Vec3(150, 100, 500) * r(), Point3(0, 0, 0), 1.0, rC(), rC(), rT(), rD()], [FireworkType.Chrysanthemum, Vec3(-100, 100, 500) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), 3.0], [FireworkType.Mickey, None, Point3(0, 0, 0), 1.0, rC(), -1, None, 3.0], [FireworkType.Bees, Vec3(0, 0, 550), Point3(0, 0, 0), 1.2, rC(), -1, 1.7, 2.0], [FireworkType.Bees, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.Bees, Vec3(-100, 50, 500) * r(), Point3(-200, 50, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.Bees, Vec3(-50, 0, 500) * r(), Point3(0, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.Bees, Vec3(100, -50, 500) * r(), Point3(200, 0, 0), 1.0, rC(), -1, rT(), rD()], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.AdvancedPeony, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.Bees, rV(), rP(), 1.0, rC(), -1, rT(), rD()], [FireworkType.AdvancedPeony, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.Ring, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.Ring, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.Bees, rV(), rP(), 1.0, rC(), -1, rT(), rD()], [FireworkType.DiademPeony, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.Ring, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.Bees, rV(), rP(), 1.0, rC(), -1, rT(), rD()], [FireworkType.Saturn, rV(), rP(), 1.0, rC(), rC(), rT(), rD()], [FireworkType.Chrysanthemum, rV(), rP(), 1.0, rC(), rC(), rT(), 3.5], [FireworkType.PalmTree, Vec3(-150, 50, 300), rP(), 1.0, Vec4(0, 1, 0, 1), rC(), 1.75, 2.0], [FireworkType.PalmTree, Vec3(160, 50, 320), rP(), 1.0, Vec4(0, 1, 0, 1), rC(), 1.75, 2.0], [FireworkType.Bees, rV(), rP(), 1.0, rC(), -1, rT(), 2.0], [FireworkType.PalmTree, Vec3(-150, -50, 350), Point3(-250, 0, 0), 1.2, Vec4(0, 1, 0, 1), rC(), 1.75, 2.0], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.75], [FireworkType.Bees, rV(), rP(), 1.0, rC(), -1, rT(), 0.5], [FireworkType.AdvancedPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.Ring, rV(), rP(), 1.0, rC(), rC(), rT(), 0.3], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.5], [FireworkType.Ring, rV(), rP(), 1.0, rC(), rC(), rT(), 0.25], [FireworkType.Bees, rV(), rP(), 1.0, rC(), -1, rT(), 0.5], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.Ring, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.AdvancedPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.6], [FireworkType.DiademPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.5], [FireworkType.AdvancedPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.6], [FireworkType.Ring, rV(), rP(), 1.0, rC(), rC(), rT(), 0.3], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.3], [FireworkType.Bees, rV(), rP(), 1.0, rC(), -1, rT(), 0.6], [FireworkType.AdvancedPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.5], [FireworkType.Ring, rV(), rP(), 1.0, rC(), rC(), rT(), 0.5], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.Ring, rV(), rP(), 1.0, rC(), rC(), rT(), 0.3], [FireworkType.Bees, rV(), rP(), 1.0, rC(), -1, rT(), 0.4], [FireworkType.BasicPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.4], [FireworkType.AdvancedPeony, rV(), rP(), 1.0, rC(), rC(), rT(), 0.5], [FireworkType.Saturn, rV(), rP(), 1.0, rC(), rC(), rT(), 0.6], [FireworkType.Chrysanthemum, rV(), rP(), 1.0, rC(), rC(), rT(), 2.5], [FireworkType.PirateSkull, None, Point3(0, 0, 0), 1.0, Vec4(1, 1, 1, 1), -1, None, 2.0]],HolidayGlobals.NEWYEARS: [[FireworkType.BasicPeony, Vec3(0, 0, 460), Point3(0, 0, 0), 1.0, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 1), 2.5, 0.75], [FireworkType.BasicPeony, Vec3(-75, 0, 450), Point3(-250, 0, 0), 1.0, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 1), 2.3, 3.1], [FireworkType.BasicPeony, Vec3(120, 0, 600), Point3(100, 0, 0), 1.0, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 1), 1.25, 1.7], [FireworkType.BasicPeony, Vec3(-25, 0, 480), Point3(-350, 0, 0), 1.0, Vec4(0.2, 1, 0.2, 1), Vec4(1, 1, 1, 1), 1.5, 0.2], [FireworkType.BasicPeony, Vec3(25, 0, 500), Point3(350, 0, 0), 1.0, Vec4(1, 0.2, 0.2, 1), Vec4(1, 1, 1, 1), 1.5, 1.6], [FireworkType.BasicPeony, Vec3(-50, 0, 500), Point3(-150, 0, 0), 1.0, Vec4(1, 0.2, 0.2, 1), Vec4(1, 1, 1, 1), 1.25, 0.2], [FireworkType.BasicPeony, Vec3(50, 0, 550), Point3(150, 0, 0), 1.0, Vec4(0.2, 1, 0.2, 1), Vec4(1, 1, 1, 1), 1.25, 1.5], [FireworkType.AdvancedPeony, Vec3(0, 0, 700), Point3(0, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.0, 0.4], [FireworkType.BasicPeony, Vec3(100, 0, 520), Point3(300, 0, 0), 1.1, rC(), Vec4(1, 1, 1, 1), 1.2, 0.0], [FireworkType.BasicPeony, Vec3(-100, 0, 500), Point3(-300, 0, 0), 1.1, rC(), Vec4(1, 1, 1, 1), 1.2, 1.75], [FireworkType.PalmTree, Vec3(100, 0, 350), Point3(-300, 0, 0), 1.2, Vec4(0.1, 1, 0.1, 1), rC(), 1.8, 0.5], [FireworkType.PalmTree, Vec3(-150, 0, 350), Point3(-350, 0, 0), 1.1, Vec4(0.1, 1, 0.1, 1), rC(), 1.75, 2.8], [FireworkType.BasicPeony, Vec3(100, 0, 450), Point3(350, 0, 0), 1.0, rC(), Vec4(1, 1, 1, 1), 2.2, 0.25], [FireworkType.BasicPeony, Vec3(-100, 0, 500), Point3(50, 0, 0), 1.0, rC(), Vec4(1, 1, 1, 1), 2.2, 0.25], [FireworkType.AdvancedPeony, Vec3(0, 0, 400), Point3(200, 0, 0), 1.15, rC(), Vec4(1, 1, 1, 1), 2.8, 2.5], [FireworkType.Chrysanthemum, Vec3(-25, 0, 500), Point3(-150, 0, 0), 1.5, Vec4(1, 1, 0.1, 1), Vec4(1, 1, 1, 1), 1.6, 2.35], [FireworkType.GlowFlare, Vec3(150, 0, 620), Point3(-500, 0, 0), 1.0, Vec4(1, 0.1, 0.1, 1), Vec4(1, 0.1, 0.1, 1), 2.2, 0.5], [FireworkType.GlowFlare, Vec3(150, 0, 620), Point3(-300, 0, 0), 1.0, Vec4(0.1, 1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), 2.2, 0.6], [FireworkType.GlowFlare, Vec3(150, 0, 620), Point3(-100, 0, 0), 1.0, Vec4(0.1, 0.1, 1, 1), Vec4(0.1, 0.1, 1, 1), 2.2, 0.5], [FireworkType.GlowFlare, Vec3(-150, 0, 620), Point3(100, 0, 0), 1.0, Vec4(1, 0.1, 0.1, 1), Vec4(1, 0.1, 0.1, 1), 2.2, 0.6], [FireworkType.GlowFlare, Vec3(-150, 0, 620), Point3(300, 0, 0), 1.0, Vec4(0.1, 1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), 2.2, 0.5], [FireworkType.GlowFlare, Vec3(-150, 0, 620), Point3(500, 0, 0), 1.0, Vec4(0.1, 0.1, 1, 1), Vec4(0.1, 0.1, 1, 1), 2.2, 0.5], [FireworkType.Chrysanthemum, Vec3(-50, 0, 400), Point3(-200, 0, 0), 1.2, Vec4(1, 0.5, 0.2, 1), Vec4(1, 1, 1, 1), 2.5, 0.0], [FireworkType.GlowFlare, Vec3(250, 0, 350), Point3(-500, 0, 0), 1.0, Vec4(1, 1, 0.1, 1), Vec4(1, 1, 0.1, 1), 2.2, 0.0], [FireworkType.GlowFlare, Vec3(-250, 0, 350), Point3(500, 0, 0), 1.0, Vec4(1, 1, 0.1, 1), Vec4(1, 1, 0.1, 1), 2.2, 0.5], [FireworkType.Chrysanthemum, Vec3(50, 0, 440), Point3(200, 0, 0), 1.2, Vec4(1, 0.5, 0.2, 1), Vec4(1, 1, 1, 1), 2.0, 1.5], [FireworkType.BasicPeony, Vec3(50, 0, 500), Point3(200, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.5, 0.5], [FireworkType.BasicPeony, Vec3(-80, 0, 500), Point3(-200, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.5, 0.5], [FireworkType.BasicPeony, Vec3(50, 0, 550), Point3(350, 0, 0), 1.1, rC(), Vec4(1, 1, 1, 1), 1.5, 0.5], [FireworkType.DiademPeony, Vec3(0, 0, 600), Point3(0, 0, 0), 1.3, Vec4(0.1, 0.1, 1, 1), Vec4(1, 1, 0.1, 1), 1.3, 0.5], [FireworkType.BasicPeony, Vec3(-100, 0, 750), Point3(-350, 0, 0), 1.1, rC(), Vec4(1, 1, 1, 1), 1.0, 0.2], [FireworkType.BasicPeony, Vec3(40, 0, 550), Point3(400, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.25, 0.5], [FireworkType.BasicPeony, Vec3(0, 0, 550), Point3(-400, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.25, 0.5], [FireworkType.Chrysanthemum, Vec3(-100, 0, 550), Point3(-300, 0, 0), 1.0, rC(), Vec4(1, 1, 1, 1), 1.3, 0.0], [FireworkType.Chrysanthemum, Vec3(100, 0, 550), Point3(300, 0, 0), 1.0, rC(), Vec4(1, 1, 1, 1), 1.3, 0.5], [FireworkType.DiademChrysanthemum, Vec3(-10, 0, 600), Point3(0, 0, 0), 1.3, Vec4(1, 0.1, 0.1, 1), Vec4(1, 1, 0.1, 1), 1.3, 1.9], [FireworkType.Bees, Vec3(-100, 0, 650), Point3(-350, 0, 0), 1.3, rC(), Vec4(1, 1, 1, 1), 1.2, 2.2], [FireworkType.Bees, Vec3(100, 0, 600), Point3(-250, 0, 0), 1.3, rC(), Vec4(1, 1, 1, 1), 1.2, 2.2], [FireworkType.Chrysanthemum, Vec3(25, 0, 480), Point3(250, 0, 0), 1.3, rC(), Vec4(1, 1, 1, 1), 2.3, 0.3], [FireworkType.Bees, Vec3(-100, 0, 500), Point3(100, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 1.3, 0.0], [FireworkType.Bees, Vec3(150, 0, 500), Point3(350, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 1.3, 3.25], [FireworkType.GlowFlare, Vec3(-150, 0, 400), Point3(0, 0, 0), 0.5, Vec4(0.1, 1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), 1.5, 0.0], [FireworkType.GlowFlare, Vec3(150, 0, 400), Point3(0, 0, 0), 0.5, Vec4(0.1, 1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), 1.5, 0.75], [FireworkType.GlowFlare, Vec3(0, 0, 480), Point3(0, 0, 0), 0.75, Vec4(0.1, 1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), 1.75, 0.0], [FireworkType.DiademChrysanthemum, Vec3(0, 0, 450), Point3(0, 0, 0), 1.25, rC(), Vec4(1, 1, 0.1, 1), 1.25, 2.5], [FireworkType.DiademPeony, Vec3(50, 0, 450), Point3(300, 0, 0), 1.2, rC(), rC(), 1.75, 0.75], [FireworkType.Ring, Vec3(75, 0, 500), Point3(150, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.75, 0.5], [FireworkType.DiademPeony, Vec3(-50, 0, 450), Point3(-300, 0, 0), 1.2, rC(), rC(), 1.75, 0.5], [FireworkType.Ring, Vec3(-75, 0, 500), Point3(-150, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.75, 1.25], [FireworkType.Saturn, Vec3(0, 0, 450), Point3(0, 0, 0), 1.2, rC(), rC(), 1.3, 3.3], [FireworkType.BasicPeony, Vec3(-25, 0, 300), Point3(-400, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 3.1, 0.2], [FireworkType.BasicPeony, Vec3(-10, 0, 400), Point3(-200, 0, 0), 1.15, rC(), Vec4(1, 1, 1, 1), 2.7, 0.2], [FireworkType.BasicPeony, Vec3(0, 0, 500), Point3(0, 0, 0), 1.1, rC(), Vec4(1, 1, 1, 1), 2.3, 0.2], [FireworkType.BasicPeony, Vec3(10, 0, 600), Point3(200, 0, 0), 1.05, rC(), Vec4(1, 1, 1, 1), 1.9, 0.2], [FireworkType.BasicPeony, Vec3(25, 0, 700), Point3(400, 0, 0), 1.0, rC(), Vec4(1, 1, 1, 1), 1.5, 0.6], [FireworkType.Saturn, Vec3(75, 0, 300), Point3(250, 0, 0), 1.25, Vec4(0.1, 1, 0.1, 1), Vec4(1, 1, 0.1, 1), 2.25, 2.5], [FireworkType.DiademChrysanthemum, Vec3(-25, 0, 550), Point3(0, 0, 0), 1.4, rC(), rC(), 1.3, 1.5], [FireworkType.BasicPeony, Vec3(-150, 0, 450), Point3(-400, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(-100, 0, 550), Point3(-300, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.Chrysanthemum, Vec3(-50, 0, 450), Point3(-200, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.BasicPeony, Vec3(-25, 0, 550), Point3(-100, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(0, 0, 450), Point3(0, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.Chrysanthemum, Vec3(25, 0, 550), Point3(100, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.BasicPeony, Vec3(50, 0, 450), Point3(200, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(100, 0, 550), Point3(300, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.Chrysanthemum, Vec3(150, 0, 450), Point3(400, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.BasicPeony, Vec3(50, 0, 400), Point3(300, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(25, 0, 500), Point3(200, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.Chrysanthemum, Vec3(0, 0, 400), Point3(100, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.BasicPeony, Vec3(-25, 0, 500), Point3(0, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(-50, 0, 400), Point3(-100, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.Chrysanthemum, Vec3(-100, 0, 500), Point3(-200, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.BasicPeony, Vec3(-150, 0, 400), Point3(-300, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(-200, 0, 500), Point3(-400, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25]],HolidayGlobals.MARDIGRAS: [[FireworkType.BasicPeony, Vec3(0, 0, 460), Point3(0, 0, 0), 1.0, Vec4(1, 0.2, 1, 1), Vec4(1, 1, 1, 1), 2.5, 0.75], [FireworkType.BasicPeony, Vec3(-75, 0, 450), Point3(-250, 0, 0), 1.0, Vec4(0.2, 1, 0.2, 1), Vec4(1, 1, 1, 1), 2.3, 3.1], [FireworkType.BasicPeony, Vec3(120, 0, 600), Point3(100, 0, 0), 1.0, Vec4(1, 0.2, 0.2, 1), Vec4(1, 1, 1, 1), 1.25, 1.7], [FireworkType.BasicPeony, Vec3(-25, 0, 480), Point3(-350, 0, 0), 1.0, Vec4(0.2, 1, 0.2, 1), Vec4(1, 1, 1, 1), 1.5, 0.2], [FireworkType.BasicPeony, Vec3(25, 0, 500), Point3(350, 0, 0), 1.0, Vec4(1, 0.2, 0.2, 1), Vec4(1, 1, 1, 1), 1.5, 1.6], [FireworkType.BasicPeony, Vec3(-50, 0, 500), Point3(-150, 0, 0), 1.0, Vec4(1, 0.2, 0.2, 1), Vec4(1, 1, 1, 1), 1.25, 0.2], [FireworkType.BasicPeony, Vec3(50, 0, 550), Point3(150, 0, 0), 1.0, Vec4(0.2, 1, 0.2, 1), Vec4(1, 1, 1, 1), 1.25, 1.5], [FireworkType.AdvancedPeony, Vec3(0, 0, 700), Point3(0, 0, 0), 1.2, Vec4(1, 0.2, 1, 1), Vec4(1, 1, 1, 1), 1.0, 0.4], [FireworkType.BasicPeony, Vec3(100, 0, 520), Point3(300, 0, 0), 1.1, Vec4(0.2, 1, 0.2, 1), Vec4(1, 1, 1, 1), 1.2, 0.0], [FireworkType.BasicPeony, Vec3(-100, 0, 500), Point3(-300, 0, 0), 1.1, Vec4(1, 0.2, 0.2, 1), Vec4(1, 1, 1, 1), 1.2, 1.75], [FireworkType.PalmTree, Vec3(100, 0, 350), Point3(-300, 0, 0), 1.2, Vec4(0.1, 1, 0.1, 1), Vec4(1, 0.1, 1, 1), 1.8, 0.5], [FireworkType.PalmTree, Vec3(-150, 0, 350), Point3(-350, 0, 0), 1.1, Vec4(0.1, 1, 0.1, 1), Vec4(1, 0.1, 1, 1), 1.75, 2.8], [FireworkType.BasicPeony, Vec3(100, 0, 450), Point3(350, 0, 0), 1.0, rC(), Vec4(1, 1, 1, 1), 2.2, 0.25], [FireworkType.BasicPeony, Vec3(-100, 0, 500), Point3(50, 0, 0), 1.0, rC(), Vec4(1, 1, 1, 1), 2.2, 0.25], [FireworkType.AdvancedPeony, Vec3(0, 0, 400), Point3(200, 0, 0), 1.15, rC(), Vec4(1, 1, 1, 1), 2.8, 2.5], [FireworkType.Chrysanthemum, Vec3(-25, 0, 500), Point3(-150, 0, 0), 1.5, Vec4(1, 0.1, 1, 1), Vec4(1, 1, 1, 1), 1.6, 2.35], [FireworkType.GlowFlare, Vec3(150, 0, 620), Point3(-500, 0, 0), 1.0, Vec4(1, 0.1, 0.1, 1), Vec4(1, 0.1, 0.1, 1), 2.2, 0.5], [FireworkType.GlowFlare, Vec3(150, 0, 620), Point3(-300, 0, 0), 1.0, Vec4(0.1, 1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), 2.2, 0.6], [FireworkType.GlowFlare, Vec3(150, 0, 620), Point3(-100, 0, 0), 1.0, Vec4(1, 0.1, 1, 1), Vec4(1, 0.1, 1, 1), 2.2, 0.5], [FireworkType.GlowFlare, Vec3(-150, 0, 620), Point3(100, 0, 0), 1.0, Vec4(1, 0.1, 0.1, 1), Vec4(1, 0.1, 0.1, 1), 2.2, 0.6], [FireworkType.GlowFlare, Vec3(-150, 0, 620), Point3(300, 0, 0), 1.0, Vec4(0.1, 1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), 2.2, 0.5], [FireworkType.GlowFlare, Vec3(-150, 0, 620), Point3(500, 0, 0), 1.0, Vec4(1, 0.1, 1, 1), Vec4(1, 0.1, 1, 1), 2.2, 0.5], [FireworkType.Chrysanthemum, Vec3(-50, 0, 400), Point3(-200, 0, 0), 1.2, Vec4(1, 0.5, 0.2, 1), Vec4(1, 1, 1, 1), 2.5, 0.0], [FireworkType.GlowFlare, Vec3(250, 0, 350), Point3(-500, 0, 0), 1.0, Vec4(1, 1, 0.1, 1), Vec4(1, 1, 0.1, 1), 2.2, 0.0], [FireworkType.GlowFlare, Vec3(-250, 0, 350), Point3(500, 0, 0), 1.0, Vec4(1, 1, 0.1, 1), Vec4(1, 1, 0.1, 1), 2.2, 0.5], [FireworkType.Chrysanthemum, Vec3(50, 0, 440), Point3(200, 0, 0), 1.2, Vec4(1, 0.5, 0.2, 1), Vec4(1, 1, 1, 1), 2.0, 1.5], [FireworkType.BasicPeony, Vec3(50, 0, 500), Point3(200, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.5, 0.5], [FireworkType.BasicPeony, Vec3(-80, 0, 500), Point3(-200, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.5, 0.5], [FireworkType.BasicPeony, Vec3(50, 0, 550), Point3(350, 0, 0), 1.1, rC(), Vec4(1, 1, 1, 1), 1.5, 0.5], [FireworkType.DiademPeony, Vec3(0, 0, 600), Point3(0, 0, 0), 1.3, Vec4(0.1, 0.1, 1, 1), Vec4(1, 1, 0.1, 1), 1.3, 0.5], [FireworkType.BasicPeony, Vec3(-100, 0, 750), Point3(-350, 0, 0), 1.1, rC(), Vec4(1, 1, 1, 1), 1.0, 0.2], [FireworkType.BasicPeony, Vec3(40, 0, 550), Point3(400, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.25, 0.5], [FireworkType.BasicPeony, Vec3(0, 0, 550), Point3(-400, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.25, 0.5], [FireworkType.Chrysanthemum, Vec3(-100, 0, 550), Point3(-300, 0, 0), 1.0, rC(), Vec4(1, 1, 1, 1), 1.3, 0.0], [FireworkType.Chrysanthemum, Vec3(100, 0, 550), Point3(300, 0, 0), 1.0, rC(), Vec4(1, 1, 1, 1), 1.3, 0.5], [FireworkType.DiademChrysanthemum, Vec3(-10, 0, 600), Point3(0, 0, 0), 1.3, Vec4(1, 0.1, 0.1, 1), Vec4(1, 1, 0.1, 1), 1.3, 1.9], [FireworkType.Bees, Vec3(-100, 0, 650), Point3(-350, 0, 0), 1.3, Vec4(1, 0.1, 1, 1), Vec4(1, 1, 1, 1), 1.2, 2.2], [FireworkType.Bees, Vec3(100, 0, 600), Point3(-250, 0, 0), 1.3, Vec4(1, 1, 0.1, 1), Vec4(1, 1, 1, 1), 1.2, 2.2], [FireworkType.Chrysanthemum, Vec3(25, 0, 480), Point3(250, 0, 0), 1.3, rC(), Vec4(1, 1, 1, 1), 2.3, 0.3], [FireworkType.Bees, Vec3(-100, 0, 500), Point3(100, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 1.3, 0.0], [FireworkType.Bees, Vec3(150, 0, 500), Point3(350, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 1.3, 3.25], [FireworkType.GlowFlare, Vec3(-150, 0, 400), Point3(0, 0, 0), 0.5, Vec4(0.1, 1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), 1.5, 0.0], [FireworkType.GlowFlare, Vec3(150, 0, 400), Point3(0, 0, 0), 0.5, Vec4(0.1, 1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), 1.5, 0.75], [FireworkType.GlowFlare, Vec3(0, 0, 480), Point3(0, 0, 0), 0.75, Vec4(0.1, 1, 0.1, 1), Vec4(0.1, 1, 0.1, 1), 1.75, 0.0], [FireworkType.DiademChrysanthemum, Vec3(0, 0, 450), Point3(0, 0, 0), 1.25, rC(), Vec4(1, 1, 0.1, 1), 1.25, 2.5], [FireworkType.DiademPeony, Vec3(50, 0, 450), Point3(300, 0, 0), 1.2, rC(), rC(), 1.75, 0.75], [FireworkType.Ring, Vec3(75, 0, 500), Point3(150, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.75, 0.5], [FireworkType.DiademPeony, Vec3(-50, 0, 450), Point3(-300, 0, 0), 1.2, rC(), rC(), 1.75, 0.5], [FireworkType.Ring, Vec3(-75, 0, 500), Point3(-150, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 1.75, 1.25], [FireworkType.Saturn, Vec3(0, 0, 450), Point3(0, 0, 0), 1.2, rC(), rC(), 1.3, 3.3], [FireworkType.BasicPeony, Vec3(-25, 0, 300), Point3(-400, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 3.1, 0.2], [FireworkType.BasicPeony, Vec3(-10, 0, 400), Point3(-200, 0, 0), 1.15, rC(), Vec4(1, 1, 1, 1), 2.7, 0.2], [FireworkType.BasicPeony, Vec3(0, 0, 500), Point3(0, 0, 0), 1.1, rC(), Vec4(1, 1, 1, 1), 2.3, 0.2], [FireworkType.BasicPeony, Vec3(10, 0, 600), Point3(200, 0, 0), 1.05, rC(), Vec4(1, 1, 1, 1), 1.9, 0.2], [FireworkType.BasicPeony, Vec3(25, 0, 700), Point3(400, 0, 0), 1.0, rC(), Vec4(1, 1, 1, 1), 1.5, 0.6], [FireworkType.Saturn, Vec3(75, 0, 300), Point3(250, 0, 0), 1.25, Vec4(0.1, 1, 0.1, 1), Vec4(1, 1, 0.1, 1), 2.25, 2.5], [FireworkType.DiademChrysanthemum, Vec3(-25, 0, 550), Point3(0, 0, 0), 1.4, rC(), rC(), 1.3, 1.5], [FireworkType.BasicPeony, Vec3(-150, 0, 450), Point3(-400, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(-100, 0, 550), Point3(-300, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.Chrysanthemum, Vec3(-50, 0, 450), Point3(-200, 0, 0), 1.2, Vec4(1, 0.1, 1, 1), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.BasicPeony, Vec3(-25, 0, 550), Point3(-100, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(0, 0, 450), Point3(0, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.Chrysanthemum, Vec3(25, 0, 550), Point3(100, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.BasicPeony, Vec3(50, 0, 450), Point3(200, 0, 0), 1.2, Vec4(1, 0.1, 1, 1), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(100, 0, 550), Point3(300, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.Chrysanthemum, Vec3(150, 0, 450), Point3(400, 0, 0), 1.2, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.BasicPeony, Vec3(50, 0, 400), Point3(300, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(25, 0, 500), Point3(200, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.Chrysanthemum, Vec3(0, 0, 400), Point3(100, 0, 0), 1.25, Vec4(1, 0.2, 1, 1), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.BasicPeony, Vec3(-25, 0, 500), Point3(0, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(-50, 0, 400), Point3(-100, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.Chrysanthemum, Vec3(-100, 0, 500), Point3(-200, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.BasicPeony, Vec3(-150, 0, 400), Point3(-300, 0, 0), 1.25, rC(), Vec4(1, 1, 1, 1), 2.0, 0.25], [FireworkType.AdvancedPeony, Vec3(-200, 0, 500), Point3(-400, 0, 0), 1.25, Vec4(1, 0.2, 1, 1), Vec4(1, 1, 1, 1), 2.0, 0.25]]}
        self.sectionData = {HolidayGlobals.FOURTHOFJULY: [(0, 34), (34, 95)],HolidayGlobals.NEWYEARS: [(0, 77)],HolidayGlobals.MARDIGRAS: [(0, 77)]}
        self.showMusic = {HolidayGlobals.NEWYEARS: SoundGlobals.MUSIC_FIREWORKS,HolidayGlobals.MARDIGRAS: SoundGlobals.MUSIC_FIREWORKS}
        del r
        del rV
        del rP
        del rS
        del rC
        del rT
        del rD
        self.delaySectionStart = None
        self.curSection = None
        self.curOffset = 0.0
        return None

    def beginSection(self, startIndex, endIndex, offset):
        taskMgr.remove('beginSection' + str(startIndex) + str(endIndex))
        sectionIval = Parallel()
        time = 2.0
        showMusic = self.showMusic.get(self.showType)
        if showMusic:
            base.musicMgr.load(showMusic, looping=False)
            musicOffset = self.getDuration(0, startIndex) - self.getDuration(startIndex, startIndex) + offset
            volume = 0.8
            if not self.wantFireworkSounds():
                volume = 0.0
            sectionIval.append(Func(base.musicMgr.request, showMusic, priority=2, looping=False, volume=volume))
            sectionIval.append(Func(base.musicMgr.offsetMusic, musicOffset))
        sectionData = self.showData.get(self.showType)[startIndex:endIndex]
        for fireworkInfo in sectionData:
            typeId = fireworkInfo[0]
            velocity = fireworkInfo[1]
            pos = fireworkInfo[2]
            scale = fireworkInfo[3]
            color1 = fireworkInfo[4]
            color2 = fireworkInfo[5]
            if color2 == -1:
                color2 = color1
            trailDur = fireworkInfo[6]
            delay = fireworkInfo[7]
            firework = Firework(typeId, velocity, scale, color1, color2, trailDur)
            firework.reparentTo(self)
            firework.setPos(pos)
            self.fireworks.append(firework)
            sectionIval.append(Sequence(Wait(time), firework.generateFireworkIval()))
            time += delay

        if endIndex == len(self.showData.get(self.showType)):
            sectionIval.append(Sequence(Wait(time), Func(self.cleanupShow)))
        self.sectionIvals.append(sectionIval)
        self.curSection = sectionIval
        self.curOffset = offset
        self.delaySectionStart = FrameDelayedCall('delaySectionStart', self.startCurSection, frames=24)

    def startCurSection(self):
        self.curSection.start(self.curOffset)

    def begin(self, timestamp):
        time = 0.0
        for section in self.sectionData.get(self.showType):
            startIndex = section[0]
            endIndex = section[1]
            sectionDur = self.getDuration(startIndex, endIndex)
            if timestamp < sectionDur:
                timestamp = max(0.0, timestamp)
                taskMgr.doMethodLater(time, self.beginSection, 'beginSection' + str(startIndex) + str(endIndex), extraArgs=[startIndex, endIndex, timestamp])
                time = time + sectionDur - timestamp
            timestamp -= sectionDur

    def getDuration(self, startIndex=0, endIndex=None):
        duration = 0.0
        if endIndex == None:
            endIndex = len(self.showData.get(self.showType))
        for firework in self.showData.get(self.showType)[startIndex:endIndex]:
            duration += firework[7]

        return duration

    def isPlaying(self):
        for ival in self.sectionIvals:
            if ival.isPlaying():
                return True

        return False

    def cleanupShow(self):
        if self.delaySectionStart:
            self.delaySectionStart.destroy()
        showMusic = self.showMusic.get(self.showType)
        if showMusic:
            base.musicMgr.requestFadeOut(showMusic)
        for section in self.sectionData.get(self.showType):
            startIndex = section[0]
            endIndex = section[1]
            taskMgr.remove('beginSection' + str(startIndex) + str(endIndex))

        for ival in self.sectionIvals:
            ival.pause()
            ival = None

        self.sectionIvals = []
        for firework in self.fireworks:
            firework.cleanup()
            firework = None

        self.fireworks = []
        return

    def wantFireworkSounds(self):
        return localAvatar.getGameState() != 'Cutscene' and base.cr.timeOfDayManager.environment not in [TODDefs.ENV_CAVE, TODDefs.ENV_LAVACAVE, TODDefs.ENV_INTERIOR]