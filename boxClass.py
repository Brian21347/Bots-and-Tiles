from enum import Enum
from vector import Vector2d
import pygame
from typing import Any


class Justification(Enum):
    topleft = 0
    midtop = 1
    topright = 2

    midleft = 3
    center = 4
    midright = 5

    bottomleft = 6
    midbottom = 7
    bottomright = 8


class OverflowingOptions(Enum):
    resize_text = 0
    resize_box_down = 1
    resize_box_right = 2
    allow_overflow = 3



class DrawnFrom(Enum):
    topleft = 0
    midtop = 1
    topright = 2

    midleft = 3
    center = 4
    midright = 5

    bottomleft = 6
    midbottom = 7
    bottomright = 8


class Box:
    """
    A class for a box which will be displayed on a screen. An image and a message text can be added to the box to be
    displayed along with it
    """

    # box defaults
    background_color: str | tuple = 'light gray'  # background color for the box
    border_size: int = 0  # the size of the border
    border_color: str = background_color  # the color of the border
    fill_in_border: bool = False  # whether the center of the boarder will be filled in or not
    margin: int = 10  # how much margin there is from the text to the edge of the box
    corner_rounding: int = margin  # the radius of the corners of the box if it was to be rounded
    hovered_over_color: str | tuple = 'light green'  # the color the box is filled when hovered over or clicked on
    # TODO: better explanation for "box_draw_from"
    box_draw_from: 'DrawnFrom' = DrawnFrom.center  # the location of the box which is at the drawn position

    # images
    image_path: str = ''  # if there is an image, then it will be displayed behind the text
    resize_image: bool = True  # scale down the image so that it will fit in the box
    center_image: bool = True  # centers the image; or, the top left of the image is positioned as the top left of the box
    keep_proportion: bool = True  # keeps the image in proportion when scaled
    blending_type: int = pygame.BLEND_RGBA_MAX  # how the image is blended to the background,
    # should the image be lighter than the background, select BLEND_RGBA_MIN
    # should the image be darker than the background, select BLEND_RGBA_MAX

    # text defaults
    text_color: str | tuple = 'black'  # the default color of the text in the box if it is not changed by tags
    text_size: int = 12  # the default size of the text in the box if it is not changed by tags
    text_font: str | None = None  # the default font used for the box if it is not changed by tags
    text_wrap: bool = True  # wrapping the text in the box to the nearest space; or, no wrapping
    text_justification: 'Justification' = Justification.center  # how the text is justified
    # changes the text/box if text overflows
    if_overflowing_text: 'OverflowingOptions' = OverflowingOptions.resize_box_down
    # changes the box to fit the text, based off of the settings in "if_overflowing_text"
    resize_box_to_text: bool = if_overflowing_text == OverflowingOptions.resize_box_down or \
        if_overflowing_text == OverflowingOptions.resize_box_right

    __hovered_over = False  # is the box hovered over
    __selected = False  # is the box selected
    __text_by_line = None  # the text after it has been interpreted
    __images_by_line = None  # the images of the text after it has been rendered

    def __init__(self, disp_surf: pygame.surface.Surface, pos_func, size_func, text) -> None:
        """
        :param disp_surf: surface on which the box is drawn on
        :param pos_func: callback function for the location of the top left corner of the box,
                    screen width and height are inputted
        :param size_func: callback function for the size of the box, screen width and height are inputted
        :param text: the text in the box, can be formatted through tags. Tags are denoted with angle brackets ("<>"),
                    between a tag specifying properties and an end tag, the default properties of the text will be changed
                    accordingly. The properties of tags can be specified using this notation (order does not matter):
                        PROPERTY:VALUE
                    Please note that if the text was to be bolded or italicized, there would be no colon then VALUE.
                    Properties that can be specified are:
                        - size (s), the size of the text
                        - font (f), the font of the text
                        - color (c), the color of the text
                        - bold (b), whether the text is bolded or not
                        - italic (i), whether the text is italicized or not
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

    def change_attrs(self, **kwargs) -> 'Box':
        # TODO: add the description of "box_drawn_from" and the type for it too
        """
        Function for changing the attributes of the box object, format is ATTRIBUTE: VALUE
        positive_or_zero: int | float >= 0
        positive: int | float > 0
        color: str | tuple[PoZ, PoZ, PoZ] | tuple[PoZ, PoZ, PoZ, PoZ]
        Attributes are:
            background_color (color): background color for the box
            border_size (positive_or_zero): the size of the border
            border_color (str): the color of the border, will only take into effect if border_size is not 0
            fill_in_border (bool): whether the center of the boarder will be filled in or not
            margin (positive_or_zero): how much margin there is from the text to the edge of the box
            corner_rounding (positive_or_zero): the radius of the corners of the box if it was to be rounded
            hovered_over_color (color): the color the box is filled when hovered over or clicked on

            image_path (str): if there is an image, then it will be displayed behind the text
            resize_image (bool): scale down the image so that it will fit in the box
            center_image (bool): centers the image; or, the top left of the image is positioned as the top left of the box
            keep_proportion (bool): keeps the image in proportion when scaled
            blending_type (int): how the image is blended to the background, should the image be lighter than the
                                 background, select BLEND_RGBA_MIN should the image be darker than the background,
                                 select BLEND_RGBA_MAX

            text_color (color): the default color of the text in the box if it is not changed by tags
            text_size (positive): the default size of the text in the box if it is not changed by tags
            text_font (str | None): the default font used for the box if it is not changed by tags
            text_wrap (bool): wrapping the text in the box to the nearest space; or, no wrapping
            text_justification (`Justification`): how the text is justified
            if_overflowing_text ('OverflowingOptions'): OverflowingOptions.resize_box_down  # how overflow will be handled
            resize_box_to_text (bool): changes the box to fit the text, based off of the settings in "if_overflowing_text"
        """
        colors = {str: 'True', tuple: '(len(value) == 3 or len(value) == 4) and all([PoZ(n) for n in value])'}
        positive_or_zero = {int: 'value >= 0', float: 'value >= 0'}
        positive = {int: 'value > 0', float: 'value > 0'}
        ints = {int: 'True'}
        bools = {bool: 'True'}
        strings = {str: 'True'}
        justification = {Justification: 'True'}
        overflowing_options = {OverflowingOptions: 'True'}
        attributes = {
            # attributes regarding the box itself
            'background_color': colors,
            'border_size': positive_or_zero,
            'border_color': colors,
            'fill_in_border': bools,
            'margin': positive_or_zero,
            'corner_rounding': positive_or_zero,
            'hovered_over_color': colors,

            # attributes regarding image
            'image_path': strings,
            'resize_image': bools,
            'center_image': bools,
            'keep_proportion': bools,
            'blending_type': ints,

            # attributes regarding text
            'text_color': colors,
            'text_size': positive,
            'text_font': strings,
            'text_wrap': bools,
            'text_justification': justification,
            'if_overflowing_text': overflowing_options,
            'resize_box_to_text': bools,
        }

        for key_value_pair in kwargs.items():
            key, value = key_value_pair
            if key not in attributes:
                raise AttributeError(f'"{key}" is not an attribute of the class Box')
            if type(value) not in attributes[key]:
                raise ValueError(f'"{value}" is not a valid value for the attribute "{key}"')
            if not eval(attributes[key][type(value)]):
                raise ValueError(f'"{value}" is not a valid value for the attribute "{key}"')
            self.__setattr__(key, value)
        return self

    def update(self, event: pygame.event.Event) -> Any:
        """
        :param event: pygame event
        :return: `return_when_clicked` if clicked; otherwise, return nothing
        """
        # handling the screen changing sizes
        if event.type == pygame.VIDEORESIZE:
            self.disp_size = self.disp_surf.get_size()

            # recalculating values
            self.pos = self.__pos_func(*self.disp_size)
            self.size = self.__size_func(*self.disp_size)
            self.rect = pygame.rect.Rect(list(self.pos), list(self.size))
            self.__images_by_line = self.convert_text_to_images()
            self.overflow()

        # handling clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__hovered_over:
                self.__selected = not self.__selected
                return self.return_when_clicked
            else:
                self.__selected = False

        self.hovered_over()  # this method could change how the box is drawn

        # the methods are called in this order so that the box is behind the image and both are behind the text
        self.draw_box()
        self.draw_img()
        self.draw_text()

    def draw_box(self) -> None:
        """Draws the box on the display surface."""
        # changes the box's color if the box is selected/hovered over
        if (self.fill_in_border and self.border_size) or not self.border_size:
            color = self.hovered_over_color if self.__hovered_over or self.__selected else self.background_color
            pygame.draw.rect(self.disp_surf, color, self.rect, 0, self.corner_rounding)
        if self.border_size:
            pygame.draw.rect(self.disp_surf, self.border_color, self.rect, self.border_size, self.corner_rounding)

    def hovered_over(self) -> None:
        """Sets `__hovered_over` to True if the box is hovered over and false otherwise."""
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):  # the mouse curser is on the box if it was not rounded

            # if there is no rounding, the curser is on the circle
            if not self.corner_rounding:
                self.__hovered_over = True
                return

            # if the cursor's x or y value is not within a corner which is being rounded
            rounding = min(self.corner_rounding / 1, self.rect.width / 2, self.rect.height / 2)
            if abs(self.rect.centerx - pos[0]) < (self.rect.width / 2 - rounding) or \
                    abs(self.rect.centery - pos[1]) < (self.rect.height / 2 - rounding):
                self.__hovered_over = True
                return

            # finding reference point (it is the center of the closest circle (they are in the corners of the box))
            if pos[0] > self.rect.centerx:
                if pos[1] > self.rect.centery:  # bottom right
                    reference_point = self.rect.bottomright[0] - rounding, self.rect.bottomright[1] - rounding
                else:  # top right
                    reference_point = self.rect.topright[0] - rounding, self.rect.topright[1] + rounding
            else:
                if pos[1] > self.rect.centery:  # bottom left
                    reference_point = self.rect.bottomleft[0] + rounding, self.rect.bottomleft[1] - rounding
                else:  # top left
                    reference_point = self.rect.topleft[0] + rounding, self.rect.topleft[1] + rounding

            # using distance to the center of the closest circle to determine if the curser is in the circle, making it
            # inside the box
            dist_to_reference_point = ((reference_point[0] - pos[0]) ** 2 + (reference_point[1] - pos[1]) ** 2) ** .5
            self.__hovered_over = dist_to_reference_point < rounding
        else:
            self.__hovered_over = False

    def draw_img(self) -> None:
        """Draws the image on the display surface."""
        if self.image_path:
            image = pygame.image.load(self.image_path)  # retrieving
            if self.resize_image:
                if self.keep_proportion:
                    scale_up = min(
                        (self.rect.width - self.margin) / image.get_width(),
                        (self.rect.height - self.margin) / image.get_height()
                    )
                    image = pygame.transform.scale(image, image.get_rect().scale_by(scale_up, scale_up).size)
                else:
                    display_area = self.rect.width - self.margin, self.rect.height - self.margin
                    image = pygame.transform.scale(image, display_area)  # scaling image
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

    def draw_text(self) -> None:
        """Draws the text on the display surface."""

        if self.__text_by_line is None:
            self.__text_by_line = self.interpret_text()
        if self.__images_by_line is None:
            self.__images_by_line = self.convert_text_to_images()
            self.overflow()

        top_justification = [Justification.topleft, Justification.midtop, Justification.topright]
        mid_ver_justification = [Justification.midleft, Justification.midright, Justification.center]

        left_justification = [Justification.topleft, Justification.midleft, Justification.bottomleft]
        mid_hor_justification = [Justification.midtop, Justification.center, Justification.midbottom]

        # total height of the text
        total_image_height = sum(max(image.get_height() for image in line) for line in self.__images_by_line)

        # handling the height offset between the lines:
        if self.text_justification in top_justification:
            vertical_offset = 0
        elif self.text_justification in mid_ver_justification:
            vertical_offset = (total_image_height * (1 / len(self.__images_by_line) - 1)) / 2
        else:  # justification is bottom left, right, or middle
            vertical_offset = -total_image_height + max(image.get_height() for image in self.__images_by_line[-1])

        for i, line in enumerate(self.__images_by_line):
            total_image_width = sum(image.get_width() for image in line)
            if self.text_justification in left_justification:
                horizontal_offset = 0
            elif self.text_justification in mid_hor_justification:
                horizontal_offset = (-total_image_width + line[0].get_width()) / 2
            else:  # justification is top right, middle right, bottom right
                horizontal_offset = -total_image_width + line[0].get_width()

            for j, image in enumerate(line):
                # used to center the text within its line
                if self.text_justification in top_justification:
                    addition = (max(img.get_height() for img in line) - image.get_height()) / 2
                elif self.text_justification in mid_ver_justification:
                    addition = 0
                else:
                    addition = -(max(img.get_height() for img in line) - image.get_height()) / 2
                blit_pos = self.justify_text(image, vertical_offset + addition, horizontal_offset)

                # handling width
                if j < len(line) - 1:
                    if self.text_justification in left_justification:
                        horizontal_offset += image.get_width()
                    elif self.text_justification in mid_hor_justification:
                        horizontal_offset += (image.get_width() + line[j + 1].get_width()) / 2
                    else:  # justification is top right, middle right, bottom right
                        horizontal_offset += line[j + 1].get_width()

                # drawing the text
                self.disp_surf.blit(image, blit_pos)

            # handling height
            if i < len(self.__images_by_line) - 1:
                if self.text_justification in top_justification:
                    vertical_offset += max(image.get_height() for image in line)
                elif self.text_justification in mid_ver_justification:
                    vertical_offset += (max(image.get_height() for image in line) +
                                        max(image.get_height() for image in self.__images_by_line[i + 1])) / 2
                else:
                    vertical_offset += max(image.get_height() for image in self.__images_by_line[i + 1])

    def convert_text_to_images(self) -> list[list[pygame.surface.Surface]]:
        """
        Converts text with its properties into images of the text.

        :returns: A list of lines which have images of the text
        """

        lines: list[list[pygame.surface.Surface]] = []
        for line in self.__text_by_line:
            used_space = 0  # space already taken up in each line (0 for a new line, >0 for a continuation)

            if not self.text_wrap:
                lines.append([self.render_text(*text_and_properties) for text_and_properties in line])
                continue

            for text_and_properties in line:
                # looping while there is leftover on each line after wrapping
                # if there is a continuation, only allow wrapping by word                    ˅˅˅˅˅˅˅˅˅˅˅˅˅˅
                while (image_and_leftover := self.wrap_text(text_and_properties, used_space, not used_space))[1]:
                    # in the loop, is the image of the rendered text which can fit in the text box
                    # and the text that was left over and needs to be placed in another line

                    image, leftover = image_and_leftover  # image and leftover text

                    if image is None:  # go to the next line, the text cannot be wrapped by word
                        if not used_space:
                            return [
                                [self.render_text('Sorry,', self.default_properties)],
                                [self.render_text('window', self.default_properties)],
                                [self.render_text('is too', self.default_properties)],
                                [self.render_text('small', self.default_properties)]
                            ]
                        used_space = 0
                        continue

                    text_and_properties = (leftover.strip(' '), text_and_properties[1])

                    if used_space == 0:  # if this is on a new line, display the image in the next line
                        lines.append([image])
                    else:  # if this is a continuation of the previous line, display the image on the previous line
                        lines[-1].append(image)
                        used_space = 0  # the program moves to a new line

                if image_and_leftover[0].get_width() == 0:  # image is of ' ', skip it
                    continue

                # if this was a continuation of the previous line, add the image to the previous line
                if used_space:
                    lines[-1].append(image_and_leftover[0])

                # this was not a continuation of the previous line, add the image to a new line
                else:
                    lines.append([image_and_leftover[0]])
                used_space += image_and_leftover[0].get_width()  # the program continues from this line

        return lines

    def overflow(self) -> None:
        # checking if text does not overflow:
        if self.if_overflowing_text is OverflowingOptions.allow_overflow:
            return
        height_of_lines = sum(max(image.get_height() for image in line) for line in self.__images_by_line)
        if not self.resize_box_to_text and height_of_lines <= self.rect.height - 2 * self.margin:
            return

        # handling overflow:
        # TODO: resize_text needs to be further tested and have it's speed improved
        if self.if_overflowing_text == OverflowingOptions.resize_text:
            # need to increment/decrement the sizes of text so that it fits in the box
            # if the size of the text is 1, then end the decrementing and state that the text cannot be displayed
            print(self.__text_by_line)

            target = self.rect.height - 2 * self.margin

            if height_of_lines == target:  # nothing needs to be resized
                return
            while height_of_lines < target:  # text needs to be resized up
                for line in self.__text_by_line:
                    for text_and_properties in line:
                        text_and_properties[1]['s'] += 1
                lines = self.convert_text_to_images()
                self.__images_by_line = lines
                height_of_lines = sum(max(image.get_height() for image in line) for line in lines)
            while height_of_lines > target:  # text needs to be resized down
                for line in self.__text_by_line:
                    for text_and_properties in line:
                        if text_and_properties[1]['s'] <= 1:
                            self.__images_by_line = self.error_message
                            return
                        text_and_properties[1]['s'] -= 1
                lines = self.convert_text_to_images()
                self.__images_by_line = lines
                height_of_lines = sum(max(image.get_height() for image in line) for line in lines)
        elif self.if_overflowing_text == OverflowingOptions.resize_box_down:
            self.rect.height = height_of_lines + 2 * self.margin
        else:  # resize box to the right
            # TODO: change the width of the box according to the text
            self.rect.width *= height_of_lines / (self.rect.height - 2 * self.margin)
            self.convert_text_to_images()

    def justify_text(self, image: pygame.surface.Surface, vertical_offset: int | float, horizontal_offset: int | float) \
            -> pygame.rect.Rect:
        """Returns the position to display the text."""
        left = self.rect.left + self.margin + horizontal_offset
        mid_horizontal = self.rect.centerx + horizontal_offset
        right = self.rect.right - self.margin + horizontal_offset

        top = self.rect.top + self.margin + vertical_offset
        mid_vertical = self.rect.centery + vertical_offset
        bottom = self.rect.bottom - self.margin + vertical_offset

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

    def wrap_text(self, text_and_properties: list[str, dict], used_space: int | float, char_wrap: bool = True) \
            -> tuple[None | pygame.surface.Surface, str]:

        text, properties = text_and_properties
        leftover = ''

        while (image := self.render_text(text, properties)).get_width() > self.line_length() - used_space:
            if len(text) == 1:
                return None, text
            i = text.rfind(' ')
            if i == -1 or i == 0:
                if not char_wrap:
                    return None, text
                i = len(text) - 1
            leftover = text[i:] + leftover
            text = text[:i]

        return image, leftover

    def line_length(self, position: None | Vector2d = None, width: None | int = None) -> int | float:
        # TODO: additional logic is needed to calculate the length of a line on a curved box
        return self.rect.width - 2 * self.margin

    @staticmethod
    def render_text(text: str, properties: dict[str, int | bool | str]) -> pygame.surface.Surface:
        """Renders text."""
        font = pygame.font.SysFont(properties['f'], properties['s'], bold=properties['b'], italic=properties['i'])
        return font.render(text, True, properties['c'])

    def interpret_text(self) -> list[list[list[str, dict], ], ] | list:
        # noinspection GrazieInspection
        """
        Interprets `self.text`, changing properties of text between tags and separating `self.text` into different
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
        default_properties = self.default_properties

        # removing unwanted whitespaces:
        i = 0
        processed_text = ''
        while i < len(self.text):
            if self.text[i] == '<':
                starting_i = i
                i += 1
                while self.text[i] in ' \n':
                    i += 1
                if self.text[i] != '>':
                    processed_text += self.text[starting_i: i + 1]
                i += 1
                continue
            processed_text += self.text[i]
            i += 1
        self.text = processed_text

        text_segments: list[list[str, dict], ] = [  # splitting the text up and adding default properties to them
            [text_segment, default_properties.copy()] for text_segment in self.text.split('\n')
        ]
        # list of lines containing text segments and properties
        text_by_line: list[list[list[str, dict], ], ] | list = []
        # for tags that cover multiple lines, properties are "continued"
        continued_properties = default_properties.copy()

        # each loop processes a line
        for text_segment, segment_properties in text_segments:  # `text_segment`: str, `segment_properties`: dict
            text_by_line.append([])  # adding a new line
            add_processed_text = lambda processed_text: text_by_line[-1].append(processed_text)  # helper function

            # each loop processes a tag
            while text_segment.count('<') > 0 and text_segment.count('>') > 0:

                tag_start = text_segment.find('<')
                tag_end = text_segment.find('>')
                tag_contents = text_segment[tag_start + 1:tag_end].lower().replace(' ', '')

                # adding the text before tags to `interpreted_text` and removing processed segments of it:
                # the text before an ending tag has its properties continued
                # the text before a starting tag has default properties
                text_before_properties = continued_properties if tag_contents == '/' else default_properties
                if tag_start != 0:  # has text before the tag
                    add_processed_text([text_segment[:tag_start], text_before_properties])
                text_segment = text_segment[tag_end + 1:]  # remove the tag and anything before it (it was processed)
                if tag_contents == '/':
                    continue  # end tags have no properties to process, so continue

                # setting segment properties to the correct values:
                for key_value_pair in tag_contents.split(','):  # `key_value_pair` is a string like this: 's:20'
                    key, _, value = key_value_pair.partition(':')  # `key` = 's', `value` = '20'
                    key = key[0]
                    if key == 'b' or key == 'i':
                        value = True  # bold or italic
                    elif key == 's': value = int(value)  # size
                    else:
                        value = value.replace('-', ' ')  # color or font
                    segment_properties[key] = value

                # adding the text inside the tags to `interpreted_text`:
                text = text_segment[:text_segment.find('</>')] if '</>' in text_segment else text_segment  # text to add
                add_processed_text([text, segment_properties])
                if '</>' in text_segment:  # there is an end tag
                    text_segment = text_segment[text_segment.find('</>')+3:]  # removing processed values
                    segment_properties = default_properties.copy()  # resetting `segment_properties`
                    continue

                # there is not an end tag
                continued_properties = segment_properties.copy()  # continuing `segment_properties`
                text_segment = ''  # all values processed, reset `text_segment`

            if text_segment:  # adding all unprocessed values
                if continued_properties != default_properties:
                    add_processed_text([text_segment, continued_properties])
                else:
                    add_processed_text([text_segment, default_properties])
        return text_by_line

    @property
    def error_message(self) -> list[list[pygame.surface.Surface,],]:
        return [
                [self.render_text('Sorry,', self.default_properties)],
                [self.render_text('window', self.default_properties)],
                [self.render_text('is too', self.default_properties)],
                [self.render_text('small', self.default_properties)]
            ]

    @property
    def default_properties(self) -> dict[str, bool | str | int | None]:
        return {  # the default properties of text
                'b': False,  # bold  bool
                'i': False,  # italic  bool
                'c': self.text_color,  # color  str
                'f': self.text_font,  # font  str
                's': self.text_size  # size  int
            }


def test():
    string = '''UC<     c      : green,        s: 20, f: arial, b>Yes</>UC<c:blue>BLUE</>UC
<            >UC<c:blue>BLUE</>UC<S:20,f:      ARIAL, I>This means <
             >you agree</>UC<c:blue>BLUE</>UC
<            >UC<c:blue>BLUE</>UC<i>ITALIC</>UC
<            ><c:blue>BLUE\nBLUE\nBLUE</>'''
    default = {'b': False, 'i': False, 'c': 'black', 'f': None, 's': 12}
    box = Box(pygame.surface.Surface([10, 10]), lambda x, y: (0,0), lambda x, y: (0,0), string)
    text_by_line = box.interpret_text()
    for line in text_by_line:
        for tp in line:
            to_print = {}
            text, properties = tp
            for k, v in properties.items():
                if properties[k] != default[k]:
                    to_print[k] = v
            print(text, to_print, end='/')
        print()


if __name__ == '__main__':
    test()
