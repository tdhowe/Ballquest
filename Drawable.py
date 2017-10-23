import cairo

class Drawable:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    # Do nothing in the base class
    def draw(self, cr):
        pass

class DrawableImage(Drawable):
    def __init__(self, x, y, width, height, image):
        super(DrawableImage, self).__init__(x, y, width, height)
        self.image = image

    def draw(self, cr):
        image_surface = cairo.ImageSurface.create_from_png(self.image)

        # calculate proportional scaling
        img_height = image_surface.get_height()
        img_width = image_surface.get_width()
        width_ratio = float(self.w) / float(img_width)
        height_ratio = float(self.h) / float(img_height)
        scale_xy = min(height_ratio, width_ratio)

        # scale image and add it
        cr.save()
        cr.translate(self.x - (img_width / 2) * scale_xy, self.y - (img_height / 2) * scale_xy)
        cr.scale(scale_xy, scale_xy)
        cr.set_source_surface(image_surface)

        cr.paint()
        cr.restore()
