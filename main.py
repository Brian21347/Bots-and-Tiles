from boxClass import Box, Justification, OverflowingOptions
from screeenClass import Screen
import pygame
from sys import exit

pygame.init()
pygame.display.set_caption('Bots and Tiles')

# pygame objects
screen = pygame.display.set_mode([500, 500], pygame.RESIZABLE)
clock = pygame.time.Clock()

# UI objects
intro_screen = Screen(
    box1=
    Box(screen, lambda x, y: (x / 2, y / 2), lambda x, y: (x / 2.5, y / 2.5), '<s: 40,b>Bots and Tiles</>')
    .change_attrs(background_color='gray', corner_rounding=25, text_justification=Justification.center,
                  border_size=1, border_color='black', if_overflowing_text=OverflowingOptions.resize_box_down,
                  fill_in_border=True),
    # TODO: allow boxes to access information about other boxes, eg their height
    box2=
    Box(screen, lambda x, y: (x / 2, y / 2 + 100), lambda x, y: (x / 5, y / 5), '<s: 28>Play</>')
    .change_attrs(background_color='gray', corner_rounding=25, text_justification=Justification.center,
                  border_size=1, border_color='black', if_overflowing_text=OverflowingOptions.resize_box_down,
                  fill_in_border=True),
)
game_screen = Screen()
# box = Box(screen, lambda x, y: (x / 10, y / 10), lambda x, y: (x / 2, y / 2),
#           '<c:red,s:40,b,i>This_is_a_string </><c:blue>to test '
#           '\nhow text is disp-\nlayed with the `Box` class</>'
#           )
# box.change_attrs(
#     background_color='light green', hovered_over_color='green', corner_rounding=50,
#     text_justification=Justification.center, text_size=28, border_size=1, border_color='black',
#     fill_in_border=True, resize_box_to_text=True,
#     if_overflowing_text=OverflowingOptions.resize_box_down
# )

# constants
FRAME_RATE = 24
BACKGROUND_COLOR = 'light gray'


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            update_screen(event)
        clock.tick(FRAME_RATE)


def update_screen(event):
    screen.fill(BACKGROUND_COLOR)

    # box.update(event)
    val = intro_screen.update(event)
    if len(val):  # TODO: more logic for which box was pressed
        intro_screen.hide()
        game_screen.show()

    pygame.display.update()


if __name__ == '__main__':
    main()
