import math
import cairo
from enum import Enum

class Color(Enum):
    BROWN = 0
    BLUE = 1
    RED = 2
    PURPLE = 3

class ImagePanel:
    shield_padding = 10 # Padding around the shield image
    height = 0
    width = 0
    corner_radius = 0
    line_width = 3

    def __init__(self, color, image):
        self.color = color
        self.image = image

    def draw_shield(self, cr, x, y):
        cr.save()

        width = ImagePanel.width - ImagePanel.shield_padding * 2
        height = ImagePanel.height - ImagePanel.shield_padding * 2

        x = x + width / 2 + ImagePanel.shield_padding
        y = y + height + ImagePanel.shield_padding

        # The coordinate space is defined as 0,0 at the center-bottom
        # of the ImagePanel.  Positive Y is up (we invert the scale so this is the case).
        # The bezier curve is determined by which color shield we are trying to draw.
        cr.translate(x, y)
        cr.scale(width / 2, -height)

        # Fill with white, then draw the outline
        for fill in [True, False]:
            cr.move_to(0,0)
            cr.curve_to(.55, .1, 0.9, .4, 1, 0.75)
            cr.curve_to(0.7, 0.7, 0.35, 0.8, 0, 1)
            cr.curve_to(-0.35, 0.8, -0.7, 0.7, -1, 0.75)
            cr.curve_to(-0.9, .4, -.55, .1, 0, 0)

            if (fill):
                cr.set_source_rgb(1, 1, 1)
                cr.fill()
            else:
                cr.set_source_rgb(0, 0, 0)
                cr.set_line_width(0.005)
                cr.stroke()

        cr.restore()

    def draw(self, cr, x, y):
        rgb = {
            Color.BROWN : [1, 0.5, 0.5],
            Color.BLUE : [1, 0.5, 0.5],
            Color.RED : [1, 0.5, 0.5],
            Color.PURPLE : [0.84, 0.72, 1.0]
        }[self.color]

        # Fill in the background
        draw_rounded_rectangle(cr, x,  y, 
            ImagePanel.width, ImagePanel.height, ImagePanel.corner_radius, ImagePanel.line_width,
            True, rgb)
        
        # Draw the outline
        draw_rounded_rectangle(cr, x,  y, 
            ImagePanel.width, ImagePanel.height, ImagePanel.corner_radius, ImagePanel.line_width)

        # draw the shield background
        self.draw_shield(cr, x, y)

def draw_text(cr, x, y, font_size, text, horiz_center = True, bold = False, italic = False):
    cr.save()
    cr.translate(x, y)
    cr.set_source_rgb(0,0,0)

    slant = cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL
    weight = cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL

    cr.select_font_face("Wasco Sans", slant, weight)
    cr.set_font_size(font_size)
    text_size = cr.text_extents(text)

    text_x = 0;
    if (horiz_center):
        text_x = -text_size[2] / 2
    cr.move_to(text_x, text_size[3]/3)
    cr.show_text(text)
    cr.restore()

def draw_rounded_rectangle(cr, x, y, width, height, corner_radius, line_width, fill = False, fill_color = [1, 1, 1]):
    radius = corner_radius;
    degrees = math.pi / 180.0;

    cr.save()
    cr.translate(x, y)
    cr.move_to(radius, 0)
    cr.arc (width - radius, radius, radius, -90 * degrees, 0 * degrees)
    cr.arc (width - radius, height - radius, radius, 0 * degrees, 90 * degrees)
    cr.arc (radius, height - radius, radius, 90 * degrees, 180 * degrees)
    cr.arc (radius, radius, radius, 180 * degrees, 270 * degrees)
    cr.set_line_width (line_width)

    if (fill):
        cr.set_source_rgb(fill_color[0], fill_color[1], fill_color[2])
        cr.fill()
    else:
        cr.set_source_rgb(0,0,0)
        cr.stroke()

    cr.restore()

class StatBox:
    box_width = 0
    box_height = 0
    padding = 0
    header_font_size = 20
    value_font_size = 32

    def __init__(self, header_text, value_text):
        self.header_text = header_text
        self.value_text = value_text

    def draw(self, cr, x, y, line_width):
        # Draw the box outline first
        cr.rectangle(x, y, StatBox.box_width, StatBox.box_height)
        cr.set_source_rgb(0,0,0)
        cr.set_line_width (line_width)
        cr.stroke()

        # Now draw the header text
        draw_text(cr, StatBox.box_width / 2, y + StatBox.padding, StatBox.header_font_size, self.header_text)

        # Finally draw the value
        draw_text(cr, StatBox.box_width / 2, y + StatBox.padding + StatBox.box_height / 2, StatBox.value_font_size, self.value_text)


def draw_boxes(cr, line_width, boxes):
    box_num = 0
    for box in boxes:
        box.draw(cr, 0, box_num * StatBox.box_height, line_width)
        box_num += 1

def main():
    width, height = 750, 1050

    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context (surface)

    buffer = 4 # Thickness of the black line around the card
    corner_radius = 15 # Radius of the rounded corners
    line_width = 3 # Thickness of the lines
    padding = 12 # Space between boxes
    box_w = 130 # Width of the stat boxes on the right side of the card

    # Fill the background with black
    cr.set_source_rgb(0, 0, 0)
    cr.rectangle (0, 0, width, height)
    cr.fill()
    
    # Draw the border line around the card
    border_w = width - 2 * buffer
    border_h = height - 2 * buffer
    draw_rounded_rectangle(cr, buffer, buffer, border_w, border_h, 0, line_width, True)
    
    # Draw the header box for the text
    header_x = padding
    header_y = padding
    header_w = width - box_w - padding * 2
    header_h = height / 11
    draw_rounded_rectangle(cr, header_x, header_y, header_w, header_h, corner_radius, line_width)
    draw_text(cr, header_x + header_w / 2, header_y + header_h / 2, 42, "ASDEBVFXEWGRXCTED")

    # Draw the box that will hold the image
    ImagePanel.width = header_w
    ImagePanel.height = height * 2 / 3 - header_h
    ImagePanel.corner_radius = corner_radius
    ImagePanel.shield_padding = buffer
    ImagePanel.line_width = line_width    
    
    imagebox_x = header_x
    imagebox_y = header_y + header_h + padding

    panel = ImagePanel(Color.PURPLE, "")
    panel.draw(cr, imagebox_x, imagebox_y)


    # Draw the boxes on the right side of the card
    cr.save()
    box_w = 130
    box_h = (imagebox_y + ImagePanel.height) / 6
    cr.translate(width - box_w, 0)

    StatBox.box_width = box_w
    StatBox.box_height = box_h
    StatBox.padding = 20

    boxes = []
    boxes.append(StatBox("testheader1", "994"))
    boxes.append(StatBox("testheader2", "995"))
    boxes.append(StatBox("testheader3", "996"))
    boxes.append(StatBox("testheader4", "997"))
    boxes.append(StatBox("testheader5", "998"))
    boxes.append(StatBox("testheader6", "999"))

    draw_boxes(cr, line_width, boxes)
    cr.restore()

    # Draw the description box at the bottom
    descbox_x = imagebox_x
    descbox_y = imagebox_y + ImagePanel.height + padding
    descbox_w = width - padding * 2
    descbox_h = height - descbox_y - padding
    draw_rounded_rectangle(cr, descbox_x, descbox_y, descbox_w, descbox_h, corner_radius, line_width)

    surface.write_to_png ("example.png") # Output to PNG

main()
