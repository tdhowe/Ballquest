import math
import cairo
import string
from Drawable import *
from enum import Enum

def sanitize_filename(filename):
    valid_chars = "-_.()/%s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename.strip() if c in valid_chars)

def draw_rectangle(cr, x, y, width, height, 
                   rounded = True, corner_radius = 15,
                   line_width = 3,
                   fill = False, fill_color = [1, 1, 1]):

    radius = corner_radius
    degrees = math.pi / 180.0

    cr.save()
    cr.translate(x, y)

    if rounded:
        cr.move_to(radius, 0)
        cr.arc(width - radius, radius, radius, -90 * degrees, 0 * degrees)
        cr.arc(width - radius, height - radius, radius, 0 * degrees, 90 * degrees)
        cr.arc(radius, height - radius, radius, 90 * degrees, 180 * degrees)
        cr.arc(radius, radius, radius, 180 * degrees, 270 * degrees)
    else:
        cr.rectangle(0, 0, width, height)
        
    cr.set_line_width(line_width)

    if fill:
        cr.set_source_rgb(fill_color[0], fill_color[1], fill_color[2])
        cr.fill()
    else:
        cr.set_source_rgb(0,0,0)
        cr.stroke()

    cr.restore()

class ImagePanel:
    shield_padding = 10 # Padding around the shield image
    height = 0
    width = 0
    corner_radius = 0
    line_width = 3

    def __init__(self, color, image):
        self.color = color
        self.image = sanitize_filename(image)

    def __draw_shield(self, cr, x, y):
        cr.save()

        width = ImagePanel.width - ImagePanel.shield_padding * 2
        height = ImagePanel.height - ImagePanel.shield_padding * 2

        x = x + ImagePanel.shield_padding
        y = y + ImagePanel.shield_padding

        shield = DrawableShield(width, height, self.color)
        # The coordinate space is defined as 0,0 at the center-bottom
        # of the ImagePanel.  Positive Y is up (we invert the scale so this is the case).
        # The bezier curve is determined by which color shield we are trying to draw.
        cr.translate(x, y)
        shield.draw(cr)

        cr.restore()

    def draw(self, cr, x, y):
        rgb = self.color.get_rgb()

        # Fill in the background
        draw_rectangle(cr, x,  y, 
            ImagePanel.width, ImagePanel.height, 
            corner_radius = ImagePanel.corner_radius, line_width = ImagePanel.line_width,
            fill = True, fill_color = rgb)
        
        # Draw the outline
        draw_rectangle(cr, x,  y, 
            ImagePanel.width, ImagePanel.height, 
            corner_radius = ImagePanel.corner_radius, line_width = ImagePanel.line_width)

        # draw the shield background
        self.__draw_shield(cr, x, y)

        # draw the image
        img_x = x + ImagePanel.width / 2
        img_y = y + ImagePanel.height / 2
        cr.save()
        img = DrawableImage(ImagePanel.width / 2, ImagePanel.height / 2, self.image)
        cr.translate(img_x, img_y)
        img.draw(cr)
        cr.restore()

class TextRegion:

    # A text region is defined from the upper-left corner of the box with a given width and height
    # Words will automatically wrap around the width
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = "Constantia"
        self.bold = False
        self.italic = False
        self.horizontal_center = False
        self.vertical_center = False
        self.__last_pos = [x, y]
        self.fontsize = 20

    def new_line(self, cr):
        if self.horizontal_center or self.vertical_center: return

        # Select the font
        self.__set_font(cr)

        font_size = cr.font_extents()

        x = self.x
        y = self.__last_pos[1] + font_size[2] * 5 / 4

        self.__last_pos = [x, y]
        return x, y

    def __set_font(self, cr):
        # Set up the look of the text
        slant = cairo.FONT_SLANT_ITALIC if self.italic else cairo.FONT_SLANT_NORMAL
        weight = cairo.FONT_WEIGHT_BOLD if self.bold else cairo.FONT_WEIGHT_NORMAL
        cr.select_font_face(self.font, slant, weight)
        cr.set_font_size(self.fontsize)
        cr.set_source_rgb(0, 0, 0)

    # Draw the text with the configured font.  If centered is set to true,
    # no wrapping will be done, and the text will be drawn centered
    # horizontally and vertically within the region.
    def draw_text(self, cr, text):
        cr.save()
        self.__set_font(cr)


        if self.vertical_center or self.horizontal_center:
            item = DrawableText(text, self.bold, self.italic, self.font, self.fontsize)
            self.__draw_item(cr, item)
        else:
            self.__draw_text(cr, text)

        cr.restore()

    def draw_item(self, cr, drawable):
        cr.save()
        self.__set_font(cr)

        self.__draw_item(cr, drawable)

        cr.restore()

    def get_current_position(self):
        return self.__last_pos[0], self.__last_pos[1]

    # Draw the text and wrap around to the next line if necessary
    def __draw_text(self, cr, text):
        x, y = self.get_current_position()

        # Use text to get the drawn width
        text_size = cr.text_extents(text)

        # Use font to make sure we are vertically centered
        font_size = cr.font_extents()

        y_centering = font_size[2] / 4
        y += y_centering

        # Split into words so we can wrap around the box if needed
        for word in text.split(' '):
            word_size = cr.text_extents(word)

            if x + word_size.x_advance > self.x + self.width:
                # Word will need to be wrapped
                x, y = self.new_line(cr)
            
            cr.move_to(x, y)
            cr.show_text(word + " ")
            x, y = cr.get_current_point()

        self.__last_pos[0] = x
        self.__last_pos[1] = y - y_centering
            
    def __draw_item(self, cr, drawable):
        x, y = self.get_current_position()

        # Use text to get the drawn width
        w, h = drawable.get_size(cr)

        if self.horizontal_center:
            x = (x + self.x + self.width) / 2 - w / 2
        if self.vertical_center:
            y = (y + self.y + self.height) / 2
        
        y_centering = h / 4
        y += y_centering
        
        # Move to the to the start of the text string
        cr.move_to(x, y)

        drawable.draw(cr)

        curx, cury = cr.get_current_point()
        if self.horizontal_center: x = self.x
        else: x = curx

        if not self.vertical_center:
            # Update the y location for the next write
            y = cury + h

        self.__last_pos[0] = x
        self.__last_pos[1] = y - y_centering

class StatBox:
    box_width = 0
    box_height = 0
    padding = 0
    header_font_size = 24
    value_font_size = 38

    def __init__(self, header_text, value_text):
        self.header_text = header_text
        self.value_text = value_text

    def draw(self, cr, x, y, line_width):
        pad = StatBox.padding
        text_region = TextRegion(x + pad, y + pad, StatBox.box_width - pad * 2, StatBox.box_height - pad * 2)

        # Draw the box outline first
        cr.rectangle(x, y, StatBox.box_width, StatBox.box_height)
        cr.set_source_rgb(0,0,0)
        cr.set_line_width (line_width)
        cr.stroke()

        # Now draw the header text
        text_region.bold = True
        text_region.horizontal_center = True
        text_region.vertical_center = False        
        text_region.fontsize = self.header_font_size
        text_region.draw_text(cr, self.header_text)

        # Finally draw the value
        if "match" in self.value_text.lower():
            # If we are drawing a match value, we need a different drawable object
            parsed = self.value_text.split(" ")
            color = Color[parsed[0].upper()]
            match_cnt = int(parsed[2])

            size = self.value_font_size * 3 / 2

            value = DrawableAppealMatch(size, size, color, match_cnt)
        elif "/" in self.value_text:
            parsed = self.value_text.split("/")
            cnt = int(parsed[0])
            t = SpecialType[parsed[1].upper()]
            size = self.value_font_size * 3 / 2

            value = DrawableMultipleAppeal(text_region.width, text_region.height - size, cnt, t)
            value.fontsize = self.value_font_size

        else:
            # Draw the text directly
            value = DrawableText(self.value_text)
            value.fontsize = self.value_font_size

        text_region.vertical_center = True
        text_region.draw_item(cr, value)

class Card:
    width = 750 # Width of the card
    height = 1050 # Height of the card
    buffer = 4 # Thickness of the black line around the card
    corner_radius = 15 # Radius of rounded rectangles
    line_width = 3 # Thickness of the lines
    padding = 12 # Space between boxes
    box_w = 130 # Width of the stat boxes on the right side of the card
    out_folder = "gen/"
    desc_text_size = 30
    desc_h = 70

    def __init__(self, name, color, slot):
        self.stats = []
        self.types = []
        self.name = name
        self.slot = slot
        self.imagebox = ImagePanel(color, "Images/" + name + ".png")
        self.text = ""
        self.flavor_text = ""

    def __draw_boxes(self, cr):
        box_num = 0
        for box in self.stats:
            box.draw(cr, 0, box_num * StatBox.box_height, Card.line_width)
            box_num += 1

    def __draw_detail_text(self, cr, x, y, width, height):
        font_size = 36
        padding = 30
        text = self.text
        flavor = self.flavor_text

        text_region = TextRegion(x + padding, y + padding * 2, width - padding * 2, height - padding * 3)
        text_region.fontsize = font_size

        if len(text) > 0:
            words = text.split(' ')
            keyword_cnt = text.count(':')
            
            # First part of detail text will be the keyword if it is present
            bold = keyword_cnt > 0

            for word in words:
                text_region.bold = bold
                text_region.draw_text(cr, word)

                # End of keyword, stop bolding until sentence end
                if ":" in word:
                    bold = False
                    keyword_cnt -= 1

                # At sentence end, resume bolding for the next word
                if "." in word:
                    bold = keyword_cnt > 0
            
            text_region.new_line(cr)
                
        if len(flavor) > 0:
            text_region.italic = True
            text_region.fontsize = 30
            text_region.draw_text(cr, flavor)

    def __draw_header_text(self, cr, x, y, width, height):
        draw_rectangle(cr, x, y, width, height, corner_radius = Card.corner_radius, line_width = Card.line_width)

        header_txt = TextRegion(x, y, width, height)
        header_txt.bold = True
        header_txt.vertical_center = True
        header_txt.horizontal_center = True
        header_txt.fontsize = 42
        header_txt.draw_text(cr, self.name)

    def __draw_slot_indicator(self, cr, x, y, size):
        squares = {
            Slot.HEAD : [[False, True, False], [False, False, False], [False, False, False]],
            Slot.CHEST : [[False, False, False], [False, True, False], [False, False, False]],
            Slot.FEET : [[False, False, False], [False, False, False], [False, True, False]],
            Slot.WEAPON : [[False, False, False], [True, False, True], [False, False, False]],
            Slot.BACK : [[True, False, False], [False, False, False], [False, False, False]],
            Slot.TRINKET : [[False, False, True], [False, False, False], [True, False, True]],
        }[self.slot]
        
        slot_size = size / 3
        lw = Card.line_width

        for row in range(len(squares)):
            for col in range(len(squares[row])):
                slot_x = x + col * slot_size
                slot_y = y + row * slot_size
                draw_rectangle(cr, slot_x, slot_y, slot_size, slot_size, rounded = False, fill = False, line_width = lw)

                if squares[row][col]:
                    # Fill the square with black
                    fill_x = slot_x + lw
                    fill_y = slot_y + lw
                    fill_sz = slot_size - lw * 2

                    draw_rectangle(cr, fill_x, fill_y, fill_sz, fill_sz, rounded = False, fill = True, fill_color = [0, 0, 0], line_width = lw)

        draw_rectangle(cr, x, y, size, size, rounded = False, fill = False)

    # Create the description string.
    # The string will be comma separated if 3 or more descriptors,
    # and the second to last word will be "and"
    def __get_desc_str(self):
        desc = []        
        for t in self.types:
            desc.append(t.value)

        noun = self.imagebox.color.value + " " + self.slot.value

        adj_cnt = len(desc)

        if adj_cnt is 0:
            return noun
        elif adj_cnt is 1:
            description = desc[0]
        elif adj_cnt is 2:
            description = desc[0] + " and " + desc[1]
        else:
            description = desc[0]
            for i in range(adj_cnt - 2):
                description += ", "
                description += desc[i]
            
            description += ", and " + desc[adj_cnt - 1]

        return description + " " + noun

    def __draw_description_text(self, cr, x, y, width, height):
        # First draw the description box
        draw_rectangle(cr, x, y, width, height)

        # Then the icons
        img_size = 50
        images = [t.get_image(img_size) for t in self.types]

        cr.save()

        cr.translate(x + Card.padding * 3, y + height / 2)

        for img in images:
            img.draw(cr)
            cr.translate(img_size, 0)

        cr.translate(-Card.padding, -height / 2 + Card.padding)

        # Draw the description text
        desc_txt = TextRegion(0, 0, width - Card.padding * 2, height - Card.padding * 2)
        desc_txt.bold = False
        desc_txt.vertical_center = True
        desc_txt.horizontal_center = False
        desc_txt.fontsize = Card.desc_text_size
        desc_txt.draw_text(cr, self.__get_desc_str())

        cr.restore()

    # Add a stat with the given name (such as "Price") and value (such as "3")
    def add_stat(self, name, value):
        if len(self.stats) >= 5:
            raise Exception("Too many stats for item '" + self.name + "'")
        self.stats.append(StatBox(name, value))

    def add_type(self, t):
        self.types.append(t)

    # Set the description text
    def set_text(self, text):
        self.text = text
    
    # Set the flavor text (shown in italics below the description)
    def set_flavor_text(self, flavor_text):
        self.flavor_text = flavor_text

    # Generate the card in the output folder based on current settings
    def create_card(self,):
        w = Card.width
        h = Card.height

        surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context (surface)

        # Fill the background with black
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle (0, 0, w, h)
        cr.fill()

        # Draw the border line around the card
        border_w = w - 2 * Card.buffer
        border_h = h - 2 * Card.buffer
        draw_rectangle(cr, Card.buffer, Card.buffer, border_w, border_h, corner_radius = 2, line_width = Card.line_width, fill = True)
        
        # Draw the header box for the text
        header_x = Card.padding
        header_y = Card.padding
        header_w = w - Card.padding * 2 - Card.box_w
        header_h = h / 14
        self.__draw_header_text(cr, header_x, header_y, header_w, header_h)
           
        # Set up layout for all image panels
        ImagePanel.width = header_w
        ImagePanel.height = h * 4 / 7
        ImagePanel.corner_radius = Card.corner_radius
        ImagePanel.shield_padding = Card.padding
        ImagePanel.line_width = Card.line_width    
        
        imagebox_x = header_x
        imagebox_y = header_y + header_h + Card.padding
        self.imagebox.draw(cr, imagebox_x, imagebox_y)
        
        # Draw the boxes on the right side of the card
        cr.save()
        box_h = (imagebox_y + ImagePanel.height + Card.padding) / 6
        cr.translate(w - Card.box_w, 0)

        StatBox.box_width = Card.box_w
        StatBox.box_height = box_h
        StatBox.padding = 20

        self.__draw_boxes(cr)

        # We want the indicator box to be below all the stats and centered in the column
        indicator_y = box_h * 5 + Card.padding
        indicator_size = box_h - Card.padding * 2
        self.__draw_slot_indicator(cr, Card.box_w - indicator_size - Card.padding * 2, indicator_y, indicator_size)

        cr.restore()


        # Draw the description box below the image
        descbox_x = imagebox_x
        descbox_y = imagebox_y + ImagePanel.height + Card.padding
        descbox_w = w - Card.padding * 2
        descbox_h = Card.desc_h

        self.__draw_description_text(cr, descbox_x, descbox_y, descbox_w, descbox_h)

        # Draw the detailed text box at the bottom
        detail_x = descbox_x
        detail_y = descbox_y + descbox_h + Card.padding
        detail_w = descbox_w
        detail_h = h - detail_y - Card.padding
        draw_rectangle(cr, detail_x, detail_y, detail_w, detail_h, corner_radius = Card.corner_radius, line_width = Card.line_width)

        # Move to the upper left corner where the text will start
        self.__draw_detail_text(cr, detail_x, detail_y, detail_w, detail_h)

        output_name = Card.out_folder + sanitize_filename(self.name) + ".png"
        # Write to output
        surface.write_to_png(output_name)
