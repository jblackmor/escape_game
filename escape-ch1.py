# Escape - A Python Adventure
# by Sean McManus / www.sean.co.uk
# Art by Rafael Pimenta
# Typed in by Jason R Blackmor

WIDTH = 800
HEIGHT = 600
TITLE = "Escape - a Python Adventure"

# this will place the game window in the middle of my third monitor [must be at top of script file]
### comment out lines 12-24 to let pygame zero choose a default location
import os
from screeninfo import get_monitors

# dynamically calculate the center position of the current monitor
def get_window_position():
    # assuming the third monitor is the current one (index 2)
    monitor = get_monitors()[0]  # adjust index if needed
    center_x = monitor.x + (monitor.width - WIDTH) // 2
    center_y = monitor.y + (monitor.height - HEIGHT) // 2
    return f"{center_x},{center_y}"

# print(get_window_position())   # 4400,240 for current monitor setup
os.environ['SDL_VIDEO_WINDOW_POS'] = get_window_position()


## game can be ran with: pgzrun <filename.py>
### comment out `import pgzrun` & `pgzrun.go()` [last line of script] if you go with this approach
import pgzrun

player_x = 600
player_y = 350

def draw():
    screen.blit(images.backdrop, (0, 0))
    screen.blit(images.mars, (50,50))
    screen.blit(images.astronaut, (player_x, player_y))
    screen.blit(images.ship, (550, 300))
   
def game_loop():
    global player_x, player_y
    if keyboard.right:
        player_x += 5
    elif keyboard.left:
        player_x -= 5
    elif keyboard.up:
        player_y -= 5
    elif keyboard.down:
        player_y += 5

clock.schedule_interval(game_loop, 0.03)

pgzrun.go()