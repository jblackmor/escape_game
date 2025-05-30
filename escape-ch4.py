# Escape - A Python Adventure
# by Sean McManus / www.sean.co.uk
# Art by Rafael Pimenta
# Typed in by Jason R Blackmor

###################################
##  VARIABLES / CONSTANTS, pt I  ##
###################################
WIDTH = 800
HEIGHT = 800
TITLE = "Escape - a Python Adventure"

PLAYER_NAME = 'Jason'
FRIEND1_NAME = 'Dan'
FRIEND2_NAME = 'TayTay'

# this will place the game window in the middle of my third monitor [must be at top of script file]
### comment out lines 19-31 to let pygame zero choose a default location
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

####################################
##  VARIABLES / CONSTANTS, pt II  ##
####################################
DEMO_OBJECTS = [images.floor, images.pillar, images.soil]

current_room = 31  # start room = 31

top_left_x = 100
top_left_y = 150

###########
##  MAP  ##
###########

MAP_WIDTH = 5
MAP_HEIGHT = 10
MAP_SIZE = MAP_WIDTH * MAP_HEIGHT

GAME_MAP = [['Room 0 - where unused objects are kept', 0, 0, False, False]]

outdoor_rooms = range(1,26)
for planetsectors in range(1,26):  # rooms 1 to 25 are generated here [sectors of soil on the planet surface outside of the space station]
    GAME_MAP.append(['The dusty planet surface', 13, 13, True, True])

GAME_MAP += [
        #["room name/description", height (top to bottom, not floor to ceiling), width (left to right), top exit? (boolean), right exit? (boolean)]
        ["The airlock", 13, 5, True, False], # room 26
        ["The engineering lab", 13, 13, False, False], # room 27
        ["Poodle Mission Control", 9, 13, False, True], # room 28
        ["The viewing gallery", 9, 15, False, False], # room 29
        ["The crew's bathroom", 5, 5, False, False], # room 30
        ["The airlock entry bay", 7, 11, True, True], # room 31
        ["Left elbow room", 9, 7, True, False], # room 32
        ["Right elbow room", 7, 13, True, True], # room 33
        ["The science lab", 13, 13, False, True], # room 34
        ["The greenhouse", 13, 13, True, False], # room 35
        [PLAYER_NAME + "'s sleeping quarters", 9, 11, False, False], # room 36
        ["West corridor", 15, 5, True, True], # room 37
        ["The briefing room", 7, 13, False, True], # room 38
        ["The crew's community room", 11, 13, True, False], # room 39
        ["Main Mission Control", 14, 14, False, False], # room 40
        ["The sick bay", 12, 7, True, False], # room 41
        ["West corridor", 9, 7, True, False], # room 42
        ["Utilities control room", 9, 9, False, True], # room 43
        ["Systems engineering bay", 9, 11, False, False], # room 44
        ["Security portal to Mission Control", 7, 7, True, False], # room 45
        [FRIEND1_NAME + "'s sleeping quarters", 9, 11, True, True], # room 46
        [FRIEND2_NAME + "'s sleeping quarters", 9, 11, True, True], # room 47
        ["The pipeworks", 13, 11, True, False], # room 48
        ["The chief scientist's office", 9, 7, True, True], # room 49
        ["The robot workshop", 9, 11, True, False] # room 50
        ]

# simple sanity check on map above to check data entry
assert len(GAME_MAP)-1 == MAP_SIZE, "Map size and GAME_MAP don't match"


################
##  MAKE MAP  ##
################

def get_floor_type():
    if current_room in outdoor_rooms:
        return 2  # soil
    else:
        return 0  # tiled floor

def generate_map():
# this function makes the map for the current room, using room data, scenery data and prop data
    global room_map, room_width, room_height, room_name, hazard_map
    global top_left_x, top_left_y, wall_transparency_frame
    room_data = GAME_MAP[current_room]
    room_name = room_data[0]
    room_height = room_data[1]
    room_width = room_data[2]

    floor_type = get_floor_type()
    if current_room in range(1,21):
        bottom_edge = 2  # soil
        side_edge = 2  # soil
    if current_room in range(21,26):
        bottom_edge = 1  # wall
        side_edge = 2  # soil
    if current_room > 25:
        bottom_edge = 1  # wall
        side_edge = 1  # wall

    # create top line of room map
    room_map = [[side_edge] * room_width]
    # add middle lines of room map (wall, floor to fill width, wall)
    for y in range(room_height - 2):
        room_map.append([side_edge] + [floor_type]*(room_width - 2) + [side_edge])
    # add bottom line of room map
    room_map.append([bottom_edge] * room_width)

    # add doorways
    middle_row = int(room_height / 2)
    middle_column = int(room_width / 2)

    if room_data[4]:  # if right exit exists in room
        room_map[middle_row][room_width - 1] = floor_type
        room_map[middle_row + 1][room_width - 1] = floor_type
        room_map[middle_row - 1][room_width - 1] = floor_type
   
    if current_room % MAP_WIDTH != 1:  # if room is NOT on left side of map
        room_to_left = GAME_MAP[current_room - 1]
        # if room on the left has a right exit, add a left exit to the current room
        if room_to_left[4]:
            room_map[middle_row][0] = floor_type
            room_map[middle_row + 1][0] = floor_type
            room_map[middle_row - 1][0] = floor_type
       
    if room_data[3]:  # if top exit exists in room
        room_map[0][middle_column] = floor_type
        room_map[0][middle_column + 1] = floor_type
        room_map[0][middle_column - 1] = floor_type

    if current_room <= MAP_SIZE - MAP_WIDTH:  # if room is NOT on bottom row
        room_below = GAME_MAP[current_room + MAP_WIDTH]
        # if room below has a top exit, add a bottom exit to the current room
        if room_below[3]:
            room_map[room_height - 1][middle_column] = floor_type
            room_map[room_height - 1][middle_column + 1] = floor_type
            room_map[room_height - 1][middle_column - 1] = floor_type
   

################
##  EXPLORER  ##
################

def draw():
    global room_height, room_width, room_map
    generate_map()
    screen.clear()

    for y in range(room_height):
        for x in range(room_width):
            image_to_draw = DEMO_OBJECTS[room_map[y][x]]
            screen.blit(image_to_draw, (top_left_x + (x*30), top_left_y + (y*30) - image_to_draw.get_height()))

def movement():
    global current_room
    old_room = current_room

    if keyboard.left:
        current_room -= 1
    if keyboard.right:
        current_room += 1
    if keyboard.up:
        current_room -= MAP_WIDTH
    if keyboard.down:
        current_room += MAP_WIDTH

    if current_room > 50:
        current_room = 50
    if current_room < 1:
        current_room = 1

    if current_room != old_room:
        print("Entering room: " + str(current_room))

clock.schedule_interval(movement, 0.1)

pgzrun.go()