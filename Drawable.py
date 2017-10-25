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
    def __init__(self, text):
        self.text = text

    def draw(self, cr):
        cr.save()
        cr.show_text(self.text)
        cr.restore()

    def get_size(self, cr):
        word_size = cr.text_extents(self.text)
        font_size = cr.font_extents()
        return word_size.x_advance, font_size[2]
    
class DrawableShield(Drawable):
    def __init__(self, width, height, color, white_fill = True):
        self.color = color
        self.w = width
        self.h = height
        self.white_fill = white_fill
        
    def get_size(self, cr):
        return self.w, self.h

    def draw(self, cr):
        cr.save()
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
                cr.set_line_width(0.005)
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