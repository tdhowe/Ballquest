import math
import cairo

#def draw_shield(cr):
    

def draw_rectangle(cr, x, y, width, height, corner_radius, line_width):
    radius = corner_radius;
    degrees = math.pi / 180.0;

    cr.save()
    cr.translate(x, y)
    cr.move_to(radius, 0)
    cr.arc (width - radius, radius, radius, -90 * degrees, 0 * degrees)
    cr.arc (width - radius, height - radius, radius, 0 * degrees, 90 * degrees)
    cr.arc (radius, height - radius, radius, 90 * degrees, 180 * degrees)
    cr.arc (radius, radius, radius, 180 * degrees, 270 * degrees)
    cr.set_source_rgb(0,0,0)
    cr.set_line_width (line_width)
    cr.stroke()
    cr.restore()


def main():
    width, height = 750, 1050

    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context (surface)

    cr.set_source_rgb(1.0, 0.9, 0.9)
    cr.rectangle (0, 0, width, height) # Rectangle(x0, y0, x1, y1)
    cr.fill()

    # Buffer space around the image
    buffer = 4
    corner_radius = 12
    line_width = 4
    padding = 15
    
    # Draw the border line around the card
    border_w = width - 2 * buffer
    border_h = height - 2 * buffer
    draw_rectangle(cr, buffer, buffer, border_w, border_h, corner_radius, line_width)
    
    # Draw the header box for the text
    header_x = buffer + padding
    header_y = buffer
    header_w = width * 6 / 8
    header_h = height / 10
    draw_rectangle(cr, header_x, header_y, header_w, header_h, corner_radius, line_width)

    # Draw the box that will hold the image
    imagebox_x = header_x
    imagebox_y = header_y + header_h + buffer + padding
    imagebox_w = header_w
    imagebox_h = height * 3 / 5 - header_h
    draw_rectangle(cr, imagebox_x, imagebox_y, imagebox_w, imagebox_h, corner_radius, line_width)

    surface.write_to_png ("example.png") # Output to PNG

main()
