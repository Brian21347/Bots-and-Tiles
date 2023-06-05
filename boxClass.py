from enum import Enum
from vector import Vector2d
import pygame


class Justification(Enum):
    topleft = 0   ; midtop = 1   ; topright = 2
    midleft = 3   ; center = 4   ; midright = 5
    bottomleft = 6; midbottom = 7; bottomright = 8
class OverflowingOptions(Enum): resize_text = 0; resize_box_down = 1; resize_box_right = 2; allow_overflow = 3


class Box:
    """
    A class for a box which will be displayed on a screen. An image and a message text can be added to the box to be
    displayed along with it
    """
    # TODO: make a function for changing the atributes of the box

    # box defalts
    background_color: str | tuple  = 'light gray'  # background color for the box
    border_size: int = 0  # the size of the border
    # TODO: implement the boarder_color and fill_in_border atributes of the box
    border_color: str = background_color  # the color of the border
    fill_in_border: bool = False  # whether the center of the boarder will be filled in or not
    margin: int = 10  # how much margin there is from the text to the edge of the box
    corner_rounding: int = margin  # the radius of the corners of the box if it was to be rounded
    hovered_over_color: str | tuple = 'light green'  # the color the box is filled when hovered over or clicked on

    # images
    image_path: str = ''  # if there is an image, then it will be displayed behind the text
    resize_image: bool = True  # scale down the image so that it will fit in the box
    center_image: bool = True  # centers the image; or, the topleft of the image is positioned as the topleft of the box
    # TODO: implement the keep_proportion atribute of the box
    keep_proportion: bool = True

    # text defalts
    text_color: str | tuple  = 'black'  # the defalt color of the text in the box if it is not changed by tags
    text_size: int = 12  # the defalt size of the text in the box if it is not changed by tags
    text_font: str | None = None  # the defalt font used for the box if it is not changed by tags
    text_wrap: bool = True  # wraping the text in the box to the nearest space; or, no wraping
    text_justification: 'Justification' = Justification.center  # how the text is justified
    # TODO: implment the if_overflowing_text atribute of the box
    if_overflowing_text: 'OverflowingOptions' = OverflowingOptions.resize_box_down

    __hovered_over = False  # is the box hovered over
    __selected = False  # is the box selected
    __text_by_line = None  # the text after it has been interpreted
    __images_by_line = None  # the images of the text after it has been rendered

    def __init__(self, disp_surf: pygame.surface.Surface, pos_func, size_func, text):
        """
        :param disp_surf: surface on which the box is drawn on
        :param pos_func: callback function for the location of the topleft corner of the box,
                    screen width and heigh are inputed
        :param size_func: callback function for the size of the box, screen width and heigh are inputed
        :param text: the text in the box, can be formated through tags. Tags are denoted with angle brackets ("<>"),
                    between a tag specifing properties and an end tag, the defult properties of the text will be changed
                    accordingly. The properties of tags can be specified using this notation (order does not matter):
                        PROPERTY:VALUE
                    Please note that if the text was to be bolded or italized, there would be no colon then VALUE.
                    Properties that can be specified are:
                        - size (s), the size of the text
                        - font (f), the font of the text
                        - color (c), the color of the text
                        - bold (b), whether the text is bolded or not
                        - italic (i), whether the text is italized or not
                    An example would be <s:20,c:blue,f:arial,b,i>text</>
        """
        self.disp_surf = disp_surf
        self.disp_size = disp_surf.get_size()
        self.text = str(text)
        self.return_when_clicked = self  # value returned when the box is clicked on

        # `__pos_func` and `__size_func` are functions that are used to calculate the position and size of the box
        self.__pos_func = pos_func
        self.__size_func = size_func

        # `pos`, `size`, and `rect` calculated using `__pos_func` and `__size_func`
        self.pos: 'Vector2d' = self.__pos_func(*self.disp_size)
        self.size: 'Vector2d' = self.__size_func(*self.disp_size)
        self.rect = pygame.rect.Rect(list(self.pos), list(self.size))

    def update(self, event: pygame.event.Event):
        """
        :param event: pygame event
        :return: `return_when_clicked` if clicked; otherwise, return nothign
        """
        # handeling the screen changing sizes
        if event.type == pygame.VIDEORESIZE:
            self.disp_size = self.disp_surf.get_size()

            # recalculating values
            self.pos = self.__pos_func(*self.disp_size)
            self.size = self.__size_func(*self.disp_size)
            self.rect = pygame.rect.Rect(list(self.pos), list(self.size))
            self.__images_by_line = self.convert_text_to_images()

        # handeling clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__hovered_over:
                self.__selected = not self.__selected
                return self.return_when_clicked
            else: self.__selected = False

        self.hovered_over()  # this method could change how the box is drawn

        # the methods are called in this order so that the box is behind the image and both are behind the text
        self.draw_box()
        self.draw_img()
        self.draw_text()

    def draw_box(self):
        """Draws the box on the display surface."""
        # changes the box's color if the box is selected/hovered over
        color = self.hovered_over_color if self.__hovered_over or self.__selected else self.background_color
        pygame.draw.rect(self.disp_surf, color, self.rect, self.border_size, self.corner_rounding)

    def draw_img(self):
        """Draws the image on the display surface."""
        if self.image_path:
            image = pygame.image.load(self.image_path)  # retreving image
            if self.resize_image: image = pygame.transform.scale(image, self.rect.size)  # scaling image
            image_size = image.get_size()  # getting size
            image = image.convert_alpha()  # removing transparent parts of image

            # the position of the image (centering it or putting it on the top left)
            pos = (self.rect.center[0] - image_size[0]/2 + 1, self.rect.center[1] - image_size[1]/2 + 1) \
                if self.center_image else self.rect.topleft

            # rounding the corners of the image if it is resized
            if self.corner_rounding and self.resize_image:
                pygame.draw.rect(self.disp_surf, 'black', (*pos, *image_size), border_radius=self.corner_rounding)
            flag = pygame.BLEND_RGBA_MAX if self.resize_image else 0
            self.disp_surf.blit(image, pos, None, flag)

    def hovered_over(self):
        """Sets `__hovered_over` to True if the box is hovered over and false otherwise."""
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):  # the mouse curser is on the box if it was not rounded

            # if there is no rounding, the curser is on the circle
            if not self.corner_rounding:
                self.__hovered_over = True
                return

            # if the curser's x or y value is not within a corner which is being rounded
            rounding = min(self.corner_rounding / 1, self.rect.width / 2, self.rect.height / 2)
            if abs(self.rect.centerx - pos[0]) < (self.rect.width / 2 - rounding) or \
                    abs(self.rect.centery - pos[1]) < (self.rect.height / 2 - rounding):
                self.__hovered_over = True
                return

            # finding refrence point (it is the center of the closest circle (they are in the corners of the box))
            if pos[0] > self.rect.centerx:
                if pos[1] > self.rect.centery:  # bottom right
                    refrence_point = self.rect.bottomright[0] - rounding, self.rect.bottomright[1] - rounding
                else:  # top right
                    refrence_point = self.rect.topright[0] - rounding, self.rect.topright[1] + rounding
            else:
                if pos[1] > self.rect.centery:  # bottom left
                    refrence_point = self.rect.bottomleft[0] + rounding, self.rect.bottomleft[1] - rounding
                else:  # top left
                    refrence_point = self.rect.topleft[0] + rounding, self.rect.topleft[1] + rounding

            # using distance to the center of the closest circle to determine if the curser is in the circle, making it
            # inside the box
            dist_to_refrence_point = ((refrence_point[0] - pos[0]) ** 2 + (refrence_point[1] - pos[1]) ** 2) ** .5
            self.__hovered_over = dist_to_refrence_point < rounding
        else:
            self.__hovered_over = False

    def draw_text(self):
        """Draws the text on the display surface."""

        if self.__text_by_line is None: self.__text_by_line = self.interpret_text()
        if self.__images_by_line is None: self.__images_by_line = self.convert_text_to_images()

        # total height of the text
        total_image_height = sum(max(image.get_height() for image in line) for line in self.__images_by_line)

        # handeling the height offset between the lines:
        if self.text_justification in [Justification.topleft, Justification.midtop, Justification.topright]:
            vertical_offset = 0
        elif self.text_justification in [Justification.midleft, Justification.midright, Justification.center]:
            vertical_offset = (total_image_height * (-1 + 1 / len(self.__images_by_line))) / 2
        else:  # justification is bottom left, right, or middle
            vertical_offset = -total_image_height + max(image.get_height() for image in self.__images_by_line[-1])

        for line in self.__images_by_line:
            if self.text_justification in [Justification.topleft, Justification.midleft, Justification.bottomleft]:
                horizontal_offset = 0
            elif self.text_justification in [Justification.midtop, Justification.center, Justification.midbottom]:
                horizontal_offset = -sum(image.get_width() for image in line) / 2
            else:  # justification is top right, middle right, bottom right
                horizontal_offset = -sum(image.get_width() for image in line) + line[-1].get_width()

            for image in line:
                # justification
                addition = (max(img.get_height() for img in line) - image.get_height()) / 2  # used to center the text within its line
                blit_pos = self.justify_text(image, vertical_offset + addition, horizontal_offset)

                # handeling width
                horizontal_offset += image.get_width()

                # drawing the text
                self.disp_surf.blit(image, blit_pos)

            # handeling height
            vertical_offset += max(image.get_height() for image in line if line)

    def convert_text_to_images(self) -> list[list[pygame.surface.Surface]]:
        """
        Converts text with its properties into images of the text.

        :returns: A list of lines which have images of the text
        """

        lines: list[list[pygame.surface.Surface]] = []
        for line in self.__text_by_line:
            used_space = 0  # space already taken up in each line (0 for a new line, >0 for a continuation)
            for text_and_properties in line:
                if not self.text_wrap:
                    lines.append([self.render_text(*text_and_properties)])
                    continue

                # looping while there is leftover on each line after wrapping
                # if there is a continuation, only allow wrapping by word                    ˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅
                while (image_and_leftover := self.wrap_text(text_and_properties, used_space, not bool(used_space)))[1]:
                    # in the loop, is the image of the rendered text which can fit in the text box
                    # and the text that was left over and needs to be placed in another line

                    image, leftover = image_and_leftover  # image and leftover text

                    if image is None: used_space = 0; continue  # go to the next line, the text cannot be wrapped by word

                    text_and_properties = (leftover.strip(' '), text_and_properties[1])

                    if used_space == 0:  # if this is on a new line, display the image in the next line
                        lines.append([image])
                    else:  # if this is a continuation of the previous line, display the image on the previous line
                        lines[-1].append(image)
                        used_space = 0  # the program moves to a new line

                if image_and_leftover[0].get_width() == 0: continue  # image is of ' ', skip it

                # if this was a continuation of the previous line, add the image to the previous line
                if used_space: lines[-1].append(image_and_leftover[0])

                # this was not a continuation of the previous line, add the image to a new line
                else: lines.append([image_and_leftover[0]])
                used_space += image_and_leftover[0].get_width()  # the program continues from this line

        # handeling overflow:
        # TODO: implement overflow
        if self.if_overflowing_text == OverflowingOptions.resize_text:
            pass
        elif self.if_overflowing_text == OverflowingOptions.resize_box_down:
            pass
        else:  # resize box to the right
            pass

        return lines

    def justify_text(self, image, vertical_offset, horizontal_offset):
        """Returns the position to display the text."""
        left = self.rect.left + self.margin + horizontal_offset
        mid_horizontal = self.rect.centerx + horizontal_offset
        right = self.rect.right - self.margin + horizontal_offset

        top = self.rect.top + self.margin + vertical_offset
        mid_vertical = self.rect.centery + vertical_offset
        bottom = self.rect.bottom - self.margin + horizontal_offset

        justification_to_position = {
            Justification.topleft: image.get_rect(topleft=(left, top)),
            Justification.midtop: image.get_rect(midtop=(mid_horizontal, top)),
            Justification.topright: image.get_rect(topright=(right, top)),

            Justification.midleft: image.get_rect(midleft=(left, mid_vertical)),
            Justification.center: image.get_rect(center=(mid_horizontal, mid_vertical)),
            Justification.midright: image.get_rect(midright=(right, mid_vertical)),

            Justification.bottomleft: image.get_rect(bottomleft=(left, bottom)),
            Justification.midbottom: image.get_rect(midbottom=(mid_horizontal, bottom)),
            Justification.bottomright: image.get_rect(bottomright=(right, bottom)),
        }
        return justification_to_position[self.text_justification]

    def wrap_text(self, text_and_properties, used_space, char_wrap=True) -> tuple[None | pygame.surface.Surface, str]:

        text, properties = text_and_properties
        leftover = ''

        while (image := self.render_text(text, properties)).get_width() > self.line_length() - used_space:
            i = text.rfind(' ')
            if i == -1 or i == 0:
                if not char_wrap: return None, text
                i = len(text) - 1
            leftover = text[i:] + leftover
            text = text[:i]

        return image, leftover

    def line_length(self, position=None, width=None):
        # TODO: additional logic is needed to calculate the length of a line on a curved box
        return self.rect.width - self.margin

    @staticmethod
    def render_text(text, properties):
        """Renders text."""
        font = pygame.font.SysFont(properties['f'], properties['s'], bold=properties['b'], italic=properties['i'])
        return font.render(text, True, properties['c'])

    def interpret_text(self):
        """
        Interprets `self.text`, changing properties of text between tags and sepreating `self.text` into different
        lines. Tags are denoted with angle brackets "<>" with the properties being denoted using the below format:
            PROPERTY:VALUE (special cases are with the properties bold and italic)
        ex.
        - "<c: green, s: 20, f: arial, b>Yes</>\n<S:20,f: arial, I>This means you agree</>"

          (Yes; color is green, size is 20, font is arial, bolded)
          (This means you agree; size is 20, font is arial, italic)

        - '''UC<     c      : green,        s: 20, f: arial, b>Yes</>UC<c:blue>BLUE</>UC
<            >UC<c:blue>BLUE</>UC<S:20,f:      ARIAL, I>This means <
             >you agree</>UC<c:blue>BLUE</>UC
<            >UC<c:blue>BLUE</>UC<i>ITALIC</>UC'''

          UC(Yes; color is green, size is 20, font is arial, bolded)UC(BLUE; color is blue)UC
          UC(BLUE; color is BLUE)UC(This means you agree; size is 20, font is arial, italic)UC(BLUE; color is blue)UC
          UC(BLUE; color is blue)UC(ITALIC; italic)UC
        """
        defult_properties = {  # the defult properties of text
                'b': False,  # bold  bool
                'i': False,  # italic  bool
                'c': self.text_color,  # color  str
                'f': self.text_font,  # font  str
                's': self.text_size  # size  int
            }

        # removing unwanted whitespaces:
        i = 0
        processed_text = ''
        while i < len(self.text):
            if self.text[i] == '<':
                starting_i = i
                i += 1
                while self.text[i] in ' \n': i += 1
                if self.text[i] != '>': processed_text += self.text[starting_i: i + 1]
                i += 1
                continue
            processed_text += self.text[i]
            i += 1
        self.text = processed_text

        text_segments: list[list[str, dict],] = [  # splitting the text up and adding defult properties to them
            [text_segment, defult_properties.copy()] for text_segment in self.text.split('\n')
        ]
        text_by_line: list[list[list[str, dict],],] | list = []  # list of lines containing text segments and properties
        continued_properties = defult_properties.copy()  # for tags that cover multiple lines, properties are "continued"

        # each loop processes a line
        for text_segment, segment_properties in text_segments:  # `text_segment`: str, `segment_properties`: dict
            text_by_line.append([])  # adding a new line
            add_proccessed_text = lambda proccessed_text: text_by_line[-1].append(proccessed_text)  # helper function

            # each loop processes a tag
            while text_segment.count('<') > 0 and text_segment.count('>') > 0:

                tag_start = text_segment.find('<')
                tag_end = text_segment.find('>')
                tag_contents = text_segment[tag_start + 1:tag_end].lower().replace(' ', '')

                # adding the text before tags to `interpreted_text` and removing processed segments of it:
                # the text before an ending tag has its properties continued
                # the text before a starting tag has defult properties
                text_before_properties = continued_properties if tag_contents == '/' else defult_properties
                if tag_start != 0:  # has text before the tag
                    add_proccessed_text([text_segment[:tag_start], text_before_properties])
                text_segment = text_segment[tag_end + 1:]  # remove the tag and anything before it (it was proccessed)
                if tag_contents == '/': continue  # end tags have no properties to process, so continue

                # setting segment properties to the correct values:
                for key_value_pair in tag_contents.split(','):  # `key_value_pair` is a string like this: 's:20'
                    key, _, value = key_value_pair.partition(':')  # `key` = 's', `value` = '20'
                    key = key[0]
                    if key == 'b' or key == 'i': value = True  # bold or italic
                    elif key == 's': value = int(value)  # size
                    else: value = value.replace('-', ' ')  # color or font
                    segment_properties[key] = value

                # adding the text inside the tags to `interpreted_text`:
                text = text_segment[:text_segment.find('</>')] if '</>' in text_segment else text_segment  # text to add
                add_proccessed_text([text, segment_properties])
                if '</>' in text_segment:  # there is an end tag
                    text_segment = text_segment[text_segment.find('</>')+3:]  # removing processed values
                    segment_properties = defult_properties.copy()  # resetting `segment_properties`
                    continue

                # there is not an end tag
                continued_properties = segment_properties.copy()  # continuing `segment_properties`
                text_segment = ''  # all values processed, reset `text_segment`

            if text_segment:  # adding all unprocessed values
                add_proccessed_text([text_segment, defult_properties])
        return text_by_line
