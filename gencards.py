import math
import cairo

#def draw_shield(cr):
    

def draw_rectangle(cr, x, y, width, height, corner_radius, line_width):
    radius = corner_radius;
    degrees = math.pi / 180.0;

    cr.move_to(x + radius, y)
    cr.arc (x + width - radius, y + radius, radius, -90 * degrees, 0 * degrees);
    cr.arc (x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees);
    cr.arc (x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees);
    cr.arc (x + radius, y + radius, radius, 180 * degrees, 270 * degrees);
    cr.set_source_rgb(0,0,0)
    cr.set_line_width (line_width);
    cr.stroke ();

def main():
    WIDTH, HEIGHT = 750, 1050

    ratio = WIDTH / HEIGHT

    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    cr = cairo.Context (surface)

    cr.set_source_rgb(1.0, 0.8, 0.8)
    cr.rectangle (0, 0, WIDTH, HEIGHT) # Rectangle(x0, y0, x1, y1)
    cr.fill()

    # Buffer space around the image
    border = 5
    corner_radius = 12
    
    #cr, x, y, width, height, corner_radius, line_width
    rect_w = WIDTH - 2 * border
    rect_h = HEIGHT - 2 * border
    draw_rectangle(cr, border, border, rect_w, rect_h, corner_radius, 4)
    
    mid_x = rect_w / 8
    
    draw_rectangle(cr, mid_x, border, mid_x * 6, 100, corner_radius, 4)

    #draw_shield(ctx)

    surface.write_to_png ("example.png") # Output to PNG

main()
