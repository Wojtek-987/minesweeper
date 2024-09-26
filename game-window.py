import pyglet
import ctypes

from map import Map


# scaling fix for Windows
try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception as e:
    print(f"Could not set DPI awareness: {e}")


# ------------------------


class GameWindow:
    state = 'menu'
    tile_size = 70

    difficulty_array = [('easy', (0, 255, 0, 255)), ('medium', (255, 100, 0, 255)), ('hard', (255, 0, 0, 255)), ('extreme', (0, 0, 255, 255))]
    current_difficulty_index = 0

    def __init__(self):
        self.map = None

    def get_game_settings(self, difficulty):
        width = 0
        height = 0
        bombs = 0

        if difficulty == 'easy':
            width = 7
            height = 7
            bombs = 7
        elif difficulty == 'medium':
            width = 10
            height = 10
            bombs = 15
        elif difficulty == 'hard':
            width = 10
            height = 15
            bombs = 25
        elif difficulty == 'extreme':
            width = 10
            height = 15
            bombs = 35

        return width, height, bombs

    def start_game(self):

        width, height, bombs = self.get_game_settings(self.difficulty_array[self.current_difficulty_index][0])

        self.map = Map(width, height)
        self.map.add_bombs(bombs)

        window.set_size(width * self.tile_size, (height + 2) * self.tile_size)

        self.state = 'game'


# ------------------------


# init vars
minesweeper = GameWindow()


# create the game window
window = pyglet.window.Window(800, 600)
window.set_caption('Minesweeper')


# ------------------------


# create the menu
menu = pyglet.graphics.Batch()

menu_bg = pyglet.shapes.Rectangle(x=0, y=0, width=window.width, height=window.height, color=(255, 255, 255, 255), batch=menu)

menu_title = pyglet.text.Label('Minesweeper', font_name='Cascadia Mono', font_size=65, color=(0, 0, 0, 255), x=window.width // 2, y=500, anchor_x='center', anchor_y='top', batch=menu)

menu_difficulty_label = pyglet.text.Label('Difficulty:', font_name='Cascadia Mono', font_size=18, color=(0, 0, 0, 255), x=window.width // 2, y=300, anchor_x='center', anchor_y='top', batch=menu)

menu_difficulty_text_hitbox = pyglet.shapes.Rectangle(x=window.width // 4, y=180, width=window.width // 2, height=80, color=(0, 0, 0, 50), batch=menu)
menu_difficulty_text = pyglet.text.Label('EASY', font_name='Cascadia Mono', font_size=36, color=(0, 255, 0, 255), x=window.width // 2, y=250, anchor_x='center', anchor_y='top', batch=menu)

# create the play button

menu_play_button_bg = pyglet.shapes.Rectangle(x=window.width // 2, y=55, width=100, height=100, color=(255, 255, 255, 0), batch=menu)
menu_play_button_bg.anchor_x = 50

menu_play_button = pyglet.shapes.Triangle(x=window.width // 2, y=100, x2=window.width // 2, y2=170, x3=window.width // 2 + 55, y3=135, color=(0, 255, 0, 255), batch=menu)
menu_play_button.anchor_position = 23, 30


# ------------------------


# create game view
game = pyglet.graphics.Batch()


# ------------------------


# mouse events
@window.event
def on_mouse_motion(x, y, dx, dy):
    if (x, y) in menu_play_button_bg:
        menu_play_button_bg.color = (100, 100, 100, 100)
    else:
        menu_play_button_bg.color = (255, 255, 255, 0)


@window.event
def on_mouse_press(x, y, button, modifiers):
    if (x, y) in menu_difficulty_text_hitbox:
        minesweeper.current_difficulty_index = (minesweeper.current_difficulty_index + 1) % len(minesweeper.difficulty_array)
        menu_difficulty_text.text = minesweeper.difficulty_array[minesweeper.current_difficulty_index][0].upper()
        menu_difficulty_text.color = minesweeper.difficulty_array[minesweeper.current_difficulty_index][1]

    if (x, y) in menu_play_button_bg:
        minesweeper.start_game()


# ------------------------


# draw the window
@window.event
def on_draw():
    window.clear()
    if minesweeper.state == 'menu':
        menu.draw()
    else:
        game.draw()


pyglet.app.run()

# initialize the game variables
#
#             if game_map.uncovered[y][x] == 'v':
#                 if game_map.map[y][x] == -1:
#                     spacing = ''
#
#                 print('[' + spacing + str(game_map.map[y][x]), ']', end='')
#
#             elif game_map.uncovered[y][x] == 'f':
#                 if game_map.map[y][x] == -1:
#                     spacing = ''
#
#                 print('[ # ]', end='')
#
#             elif game_map.uncovered[y][x] == 'h':
#                 print('[ - ]', end='')
#

#     if game_map.uncover(int(x), int(y)) == 'bomb':
#         print('You lost!')
#         break
#
#     game_map.uncover(int(x), int(y))
#     game_map.place_flag(int(x), int(y))
