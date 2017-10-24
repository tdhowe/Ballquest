import cairo

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
    