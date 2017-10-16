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

    # Shield Geometry is dependent on color
    def __draw_shield_geometry(self, cr):
        if (self.color is Color.BROWN):
            cr.curve_to(.55, .1, 0.9, .4, 1, 0.85)
            cr.curve_to(0.4, 1.04, -0.4, 1.04, -1, 0.85)
            cr.curve_to(-0.9, .4, -.55, .1, 0, 0) 
        if (self.color is Color.RED):
            cr.curve_to(.55, .1, 0.9, .4, 1, 0.97)
            cr.line_to(0, 0.85)
            cr.line_to(-1, 0.97)
            cr.curve_to(-0.9, .4, -.55, .1, 0, 0)
        if (self.color is Color.BLUE):
            cr.curve_to(.55, .1, 0.9, .4, 1, 0.75)
            cr.curve_to(0.75, 0.8, 0.6, 0.86, 0.4, 1)
            cr.line_to(-0.4, 1)
            cr.curve_to(-0.6, 0.86, -0.75, 0.8, -1, 0.75)
            cr.curve_to(-0.9, .4, -.55, .1, 0, 0)
        if (self.color is Color.PURPLE):
            cr.curve_to(.55, .1, 0.9, .4, 1, 0.85)
            cr.curve_to(0.72, 0.8, 0.33, 0.85, 0, 1)
            cr.curve_to(-0.353, 0.85, -0.72, 0.8, -1, 0.85)
            cr.curve_to(-0.9, .4, -.55, .1, 0, 0)

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

            self.__draw_shield_geometry(cr)

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
            Color.BROWN : [0.64, 0.5, 0.34],
            Color.BLUE : [0.5, 0.7, 0.9],
            Color.RED : [1, 0.61, 0.61],
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

class Card:
    width = 750 # Width of the card
    height = 1050 # Height of the card
    buffer = 4 # Thickness of the black line around the card
    corner_radius = 15 # Radius of the rounded corners
    line_width = 3 # Thickness of the lines
    padding = 12 # Space between boxes
    box_w = 130 # Width of the stat boxes on the right side of the card
    out_folder = "gen/"

    def __init__(self, name, description, color, image):
        self.stats = []
        self.name = name
        self.description = description
        self.imagebox = ImagePanel(color, image)

    def __draw_boxes(self, cr):
        box_num = 0
        for box in self.stats:
            box.draw(cr, 0, box_num * StatBox.box_height, Card.line_width)
            box_num += 1

    def add_stat(self, name, value):
        self.stats.append(StatBox(name, value))

    def create_card(self,):
        w = Card.width
        h = Card.height
        box_w = 130

        surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context (surface)

        # Fill the background with black
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle (0, 0, w, h)
        cr.fill()

        # Draw the border line around the card
        border_w = w - 2 * Card.buffer
        border_h = h - 2 * Card.buffer
        draw_rounded_rectangle(cr, Card.buffer, Card.buffer, border_w, border_h, 0, Card.line_width, True)
        
        # Draw the header box for the text
        header_x = Card.padding
        header_y = Card.padding
        header_w = w - box_w - Card.padding * 2
        header_h = h / 11
        draw_rounded_rectangle(cr, header_x, header_y, header_w, header_h, Card.corner_radius, Card.line_width)
        draw_text(cr, header_x + header_w / 2, header_y + header_h / 2, 42, self.name)
           
        # Set up layout for all image panels
        ImagePanel.width = header_w
        ImagePanel.height = h * 2 / 3 - header_h
        ImagePanel.corner_radius = Card.corner_radius
        ImagePanel.shield_padding = Card.padding
        ImagePanel.line_width = Card.line_width    
        
        imagebox_x = header_x
        imagebox_y = header_y + header_h + Card.padding
        self.imagebox.draw(cr, imagebox_x, imagebox_y)
        
        # Draw the boxes on the right side of the card
        cr.save()
        box_h = (imagebox_y + ImagePanel.height) / 6
        cr.translate(w - box_w, 0)

        StatBox.box_width = box_w
        StatBox.box_height = box_h
        StatBox.padding = 20

        self.__draw_boxes(cr)
        cr.restore()

        # Draw the description box at the bottom
        descbox_x = imagebox_x
        descbox_y = imagebox_y + ImagePanel.height + Card.padding
        descbox_w = w - Card.padding * 2
        descbox_h = h - descbox_y - Card.padding
        draw_rounded_rectangle(cr, descbox_x, descbox_y, descbox_w, descbox_h, Card.corner_radius, Card.line_width)


        output_name = Card.out_folder + self.name.replace(" ", "_") + ".png"
        # Write to output
        surface.write_to_png(output_name)


def main():
    brown_card = Card("Test Brown Card", "This is a brown card for testing. Lorem Ipsum Sin Dolor", Color.BROWN, "")
    red_card = Card("Test Red Card", "This is a red card for testing. Lorem Ipsum Sin Dolor", Color.RED, "")
    blue_card = Card("Test Blue Card", "This is a blue card for testing. Lorem Ipsum Sin Dolor", Color.BLUE, "")
    purple_card = Card("Test Purple Card", "This is a purple card for testing. Lorem Ipsum Sin Dolor", Color.PURPLE, "")

    brown_card.add_stat("Price", "2")
    red_card.add_stat("Price", "3")
    blue_card.add_stat("Price", "3")
    purple_card.add_stat("Price", "4")

    brown_card.add_stat("Appeal", "-4")
    red_card.add_stat("Appeal", "3")
    blue_card.add_stat("Appeal", "3")
    purple_card.add_stat("Appeal", "4")

    brown_card.add_stat("Priority", "0")
    red_card.add_stat("Priority", "2")
    blue_card.add_stat("Priority", "2")
    purple_card.add_stat("Priority", "-3")

    brown_card.add_stat("HP", "8")
    red_card.add_stat("HP", "6")
    blue_card.add_stat("HP", "6")
    purple_card.add_stat("HP", "4")
    
    brown_card.add_stat("Damage", "2s")
    red_card.add_stat("Damage", "6b")
    blue_card.add_stat("Damage", "6s/4b")
    purple_card.add_stat("Damage", "4m")

    brown_card.add_stat("Capacity", "1")
    red_card.add_stat("Capacity", "2")
    blue_card.add_stat("Capacity", "3")
    purple_card.add_stat("Capacity", "4")

    brown_card.create_card();
    red_card.create_card();
    blue_card.create_card();
    purple_card.create_card();


main()
