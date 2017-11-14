from panda3d.core import *

class ChatBalloon:
    TEXT_SHIFT = (0.1, -0.05, 1.1)
    TEXT_SHIFT_REVERSED = -0.05
    TEXT_SHIFT_PROP = 0.08
    NATIVE_WIDTH = 10.0
    MIN_WIDTH = 2.5
    MIN_HEIGHT = 1
    BUBBLE_PADDING = 0.3
    BUBBLE_PADDING_PROP = 0.05
    BUTTON_SCALE = 6
    BUTTON_SHIFT = (-0.2, 0, 0.6)
    FRAME_SHIFT = (0.2, 1.4)

    def __init__(self, model):
        self.model = model

    def generate(self, text, font, textColor=(0,0,0,1), balloonColor=(1,1,1,1),
                 wordWrap = 10.0, button=None, reversed=False):

        root = NodePath('balloon')

        # Add balloon geometry:
        balloon = self.model.copyTo(root)
        top = balloon.find('**/top')
        middle = balloon.find('**/middle')
        bottom = balloon.find('**/bottom')

        balloon.setColor(balloonColor)
        if balloonColor[3] < 1.0:
            balloon.setTransparency(1)

        # Render the text into a TextNode, using the font:
        t = root.attachNewNode(TextNode('text'))
        t.node().setFont(font)
        t.node().setWordwrap(wordWrap)
        t.node().setText(text)
        t.node().setTextColor(textColor)

        width, height = t.node().getWidth(), t.node().getHeight()

        # Turn off depth write for the text: The place in the depth buffer is
        # held by the chat bubble anyway, and the text renders after the bubble
        # so there's no risk of the bubble overwriting the text's pixels.
        t.setAttrib(DepthWriteAttrib.make(0))
        t.setPos(self.TEXT_SHIFT)
        t.setX(t, self.TEXT_SHIFT_PROP*width)
        t.setZ(t, height)

        if reversed:
            # The nametag code wants the text on the left side of the axis,
            # rather than on the right side. Therefore, we move the text to the
            # opposite side:
            t.setX(self.TEXT_SHIFT_REVERSED - self.TEXT_SHIFT_PROP*width - width)

        # Give the chat bubble a button, if one is requested:
        if button:
            np = button.copyTo(root)
            np.setPos(t, width, 0, -height)
            np.setPos(np, self.BUTTON_SHIFT)
            np.setScale(self.BUTTON_SCALE)

        # Set a minimum width and height for short or empty messages
        if width < self.MIN_WIDTH:
            width = self.MIN_WIDTH
            if reversed:
                t.setX(t, -width/2.0)
            else:
                t.setX(t, width/2.0)
            t.node().setAlign(TextNode.ACenter)

        if height < self.MIN_HEIGHT:
            height = self.MIN_HEIGHT
            t.setX(t, height/2.0)
            t.node().setAlign(TextNode.ACenter)

        # Set the balloon's size:
        width *= 1+self.BUBBLE_PADDING_PROP
        width += self.BUBBLE_PADDING
        balloon.setSx(width/self.NATIVE_WIDTH)
        if reversed:
            balloon.setSx(-balloon.getSx())
            balloon.setTwoSided(True) # Render the backface of the balloon
        middle.setSz(height)
        top.setZ(top, height-1)

        # Calculate the frame occupied by the balloon:
        left, bottom = self.FRAME_SHIFT
        if reversed:
            left = -left - width
        frame = (left, left+width, bottom, bottom+height+1)

        return root, frame
