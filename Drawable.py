import cairo
from enum import Enum

class Color(Enum):
    BROWN = 'Brown'
    BLUE = 'Blue'
    RED = 'Red'
    PURPLE = 'Purple'

    # Get the RGB color associated with this color enum
    def get_rgb(self):        
        rgb = {
            Color.BROWN : [0.64, 0.5, 0.34],
            Color.BLUE : [0.5, 0.7, 0.9],
            Color.RED : [1, 0.61, 0.61],
            Color.PURPLE : [0.84, 0.72, 1.0]
        }[self]

        return rgb

class Drawable:
    # Do nothing in the base class
    def draw(self, cr):
        pass

    # Get the x,y dimensions of the actual drawable object.
    # For instance, text will not be the given width, height
    def get_size(self, cr):
        return 0, 0

class DrawableImage(Drawable):
    def __init__(self, width, height, image):
        self.image_surface = cairo.ImageSurface.create_from_png(image)
        self.w = width
        self.h = height

        # calculate proportional scaling
        self.img_height = self.image_surface.get_height()
        self.img_width = self.image_surface.get_width()
        width_ratio = float(self.w) / float(self.img_width)
        height_ratio = float(self.h) / float(self.img_height)
        self.scale_xy = min(height_ratio, width_ratio)

    def draw(self, cr):
        # scale image and add it
        cr.save()
        cr.translate(-self.img_width / 2 * self.scale_xy, -self.img_height / 2 * self.scale_xy)
        cr.scale(self.scale_xy, self.scale_xy)
        cr.set_source_surface(self.image_surface)

        cr.paint()
        cr.restore()
    
    def get_size(self, cr):
        return self.img_width * self.scale_xy, self.img_height * self.scale_xy

class DrawableText(Drawable):
    def __init__(self, text, bold = False, italic = False, font = "Constantia", fontsize = 20):
        self.text = text
        self.bold = bold
        self.italic = italic
        self.font = font
        self.fontsize = fontsize
    
    # Apply the font for this drawable to the current cairo context
    def __apply_font(self, cr):
        slant = cairo.FONT_SLANT_ITALIC if self.italic else cairo.FONT_SLANT_NORMAL
        weight = cairo.FONT_WEIGHT_BOLD if self.bold else cairo.FONT_WEIGHT_NORMAL
        cr.select_font_face(self.font, slant, weight)
        cr.set_font_size(self.fontsize)
        cr.set_source_rgb(0, 0, 0)

    def draw(self, cr):
        cr.save()
        self.__apply_font(cr)
        cr.show_text(self.text)
        cr.restore()

    def get_size(self, cr):
        cr.save()
        self.__apply_font(cr)
        word_size = cr.text_extents(self.text)
        font_size = cr.font_extents()
        cr.restore()
        return word_size.x_advance, font_size[2]
    
class DrawableShield(Drawable):
    def __init__(self, width, height, color, white_fill = True):
        self.color = color
        self.w = width
        self.h = height
        self.white_fill = white_fill
        self.line_width = 0.005
        
    def get_size(self, cr):
        return self.w, self.h

    def draw(self, cr):
        cr.save()
        cr.translate(self.w / 2, self.h)
        cr.scale(self.w / 2, -self.h)

        # Fill with white, then draw the outline
        for fill in [True, False]:
            cr.move_to(0,0)

            self.__draw_shield_geometry(cr)

            if (fill):
                if self.white_fill: cr.set_source_rgb(1, 1, 1)
                else:
                    rgb = self.color.get_rgb() 
                    cr.set_source_rgb(rgb[0], rgb[1], rgb[2])
                cr.fill()
            else:
                cr.set_source_rgb(0, 0, 0)
                cr.set_line_width(self.line_width)
                cr.stroke()

        cr.restore()

    # Shield Geometry is dependent on color
    def __draw_shield_geometry(self, cr):
        if (self.color is Color.BROWN):
            cr.curve_to(.55, .1, 0.9, .4, 1, 0.83)
            cr.curve_to(0.4, 1.04, -0.4, 1.04, -1, 0.83)
            cr.curve_to(-0.9, .4, -.55, .1, 0, 0) 
        if (self.color is Color.RED):
            cr.curve_to(.55, .1, 0.9, .4, 1, 0.97)
            cr.line_to(0, 0.85)
            cr.line_to(-1, 0.97)
            cr.curve_to(-0.9, .4, -.55, .1, 0, 0)
        if (self.color is Color.BLUE):
            cr.curve_to(.55, .1, 0.9, .4, 1, 0.75)
            cr.line_to(0.4, 1)
            #cr.curve_to(0.75, 0.8, 0.6, 0.86, 0.4, 1)
            cr.line_to(-0.4, 1)
            #cr.curve_to(-0.6, 0.86, -0.75, 0.8, -1, 0.75)     
            cr.line_to(-1, 0.75)
            cr.curve_to(-0.9, .4, -.55, .1, 0, 0)
        if (self.color is Color.PURPLE):
            cr.curve_to(.55, .1, 0.9, .4, 1, 0.85)
            cr.curve_to(0.72, 0.8, 0.33, 0.85, 0, 1)
            cr.curve_to(-0.353, 0.85, -0.72, 0.8, -1, 0.85)
            cr.curve_to(-0.9, .4, -.55, .1, 0, 0)

class DrawableAppealMatch(Drawable):
    # Create a new drawable "<color> match <cnt>" icon.
    # The width and height represent the size of the
    # individual shields in the match display
    def __init__(self, width, height, color, match_cnt):
        self.color = color
        self.w = width
        self.h = height
        self.match_cnt = match_cnt
        
    def get_size(self, cr):
        return self.w, self.h

    def draw(self, cr):
        cr.save()
        shield = DrawableShield(self.w, self.h, self.color, False)
        shield.line_width = 0.04
        text = DrawableText(str(self.match_cnt))
        text.fontsize = self.w * 2 / 3
        text.bold = True
        text_size = text.get_size(cr)

        curx, cury = cr.get_current_point()
        cr.translate(curx, cury - self.h * 3 / 4)
        shield.draw(cr)

        cr.translate(self.w / 2 - text_size[0] / 2, self.h / 2 + text_size[1] / 8)

        text.draw(cr)

        cr.restore()
