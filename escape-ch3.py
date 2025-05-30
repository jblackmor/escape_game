# Escape - A Python Adventure
# by Sean McManus / www.sean.co.uk
# Art by Rafael Pimenta
# Typed in by Jason R Blackmor

WIDTH = 800
HEIGHT = 800
TITLE = "Escape - a Python Adventure"

# this will place the game window in the middle of my third monitor [must be at top of script file]
### comment out lines 12-24 to let pygame zero choose a default location
import os
from screeninfo import get_monitors

# dynamically calculate the center position of the current monitor
def get_window_position():
    # assuming the third monitor is the current one (index 2)
    monitor = get_monitors()[0] #[2]  # adjust index if needed
    center_x = monitor.x + (monitor.width - WIDTH) // 2
    center_y = monitor.y + (monitor.height - HEIGHT) // 2
    return f"{center_x},{center_y}"

# print(get_window_position())   # 4400,240 for current monitor setup
os.environ['SDL_VIDEO_WINDOW_POS'] = get_window_position()


## game can be ran with: pgzrun <filename.py>
### comment out `import pgzrun` & `pgzrun.go()` [last line of script] if you go with this approach
import pgzrun

DEMO_OBJECTS = [images.floor, images.pillar]

top_left_x = 100
top_left_y = 150

room_height = 7
room_width = 5

room_map = [ [1, 1, 1, 1, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 1, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 1, 1, 1, 1]
           ]

def draw():
    for y in range(room_height):
        for x in range(room_width):
            image_to_draw = DEMO_OBJECTS[room_map[y][x]]
            screen.blit(image_to_draw, (top_left_x + (x*30), top_left_y + (y*30) - image_to_draw.get_height()))

# room_map = [ [1, 1, 1, 1, 1],
#              [1, 0, 0, 0, 1],
#              [1, 0, 1, 0, 1],
#              [1, 0, 0, 0, 1],
#              [1, 0, 0, 0, 1],
#              [1, 0, 0, 0, 1],
#              [1, 1, 1, 1, 1]
#            ]

# for y in range(7):
#     print(room_map[y])
# print()


# for y in range(7):
#     for x in range(5):
#         print(room_map[y][x], end="")  # can add one space in 'end' for a little more spaced out legibility
#     print()


pgzrun.go()