import pyglet
import ctypes

from map import Map

# Scaling fix for Windows
try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception as e:
    print(f"Could not set DPI awareness: {e}")

# ------------------------

class GameWindow:
    state = 'menu'
    tile_size = 70

    difficulty_array = [
        ('easy', (0, 100, 0, 255)),
        ('medium', (255, 100, 0, 255)),
        ('hard', (255, 0, 0, 255)),
        ('extreme', (0, 0, 255, 255))
    ]
    current_difficulty_index = 0

    def __init__(self):
        self.labels = []
        self.tiles = []
        self.map = None
        self.game = pyglet.graphics.Batch()
        self.overlay_rect = None
        self.restart_label = None
        self.result_label = None

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
        width, height, bombs = self.get_game_settings(
            self.difficulty_array[self.current_difficulty_index][0])

        self.map = Map(width, height)
        self.map.add_bombs(bombs)

        window.set_size(width * self.tile_size, height * self.tile_size)

        self.state = 'game'

        # Reset tiles and labels
        self.tiles = []
        self.labels = []

        # Reset the game batch
        self.game = pyglet.graphics.Batch()

        for y in range(self.map.height):
            tile_row = []
            label_row = []
            for x in range(self.map.width):
                y_position = (self.map.height - y - 1) * self.tile_size
                tile = pyglet.shapes.Rectangle(
                    x=x * self.tile_size,
                    y=y_position,
                    width=self.tile_size,
                    height=self.tile_size,
                    color=(200, 200, 200, 255),
                    batch=self.game
                )
                tile_row.append(tile)
                label_row.append(None)  # Placeholder for labels
            self.tiles.append(tile_row)
            self.labels.append(label_row)

        # Create overlay elements
        window_width, window_height = window.get_size()

        # Create the overlay rectangle
        self.overlay_rect = pyglet.shapes.Rectangle(
            x=0,
            y=0,
            width=window_width,
            height=window_height,
            color=(255, 255, 255),
            batch=self.game
        )
        self.overlay_rect.opacity = 0  # Fully transparent

        # Create the restart label
        self.restart_label = pyglet.text.Label(
            text='Click anywhere to restart',
            font_name='Cascadia Mono',
            font_size=24,
            x=window_width / 2,
            y=window_height / 2 - 30,
            anchor_x='center',
            anchor_y='center',
            color=(0, 0, 0, 0),
            batch=self.game
        )

        # Create the result label ("You Win"/"You Lose")
        self.result_label = pyglet.text.Label(
            text='',  # Text will be set when the game ends
            font_name='Cascadia Mono',
            font_size=48,
            x=window_width / 2,
            y=window_height / 2 + 30,
            anchor_x='center',
            anchor_y='center',
            color=(0, 0, 0, 0),
            batch=self.game
        )

    def reset_game(self):
        # Reset game variables
        self.state = 'menu'
        self.map = None
        # Delete tiles and labels
        for row in self.tiles:
            for tile in row:
                tile.delete()
        self.tiles = []
        for row in self.labels:
            for label in row:
                if label:
                    label.delete()
        self.labels = []
        # Reset the game batch
        self.game = pyglet.graphics.Batch()
        # Overlay elements will be recreated in start_game()

# ------------------------

# Initialize variables
minesweeper = GameWindow()

# Create the game window
window = pyglet.window.Window(800, 600)
window.set_caption('Minesweeper')

# ------------------------

# Create the menu
menu = pyglet.graphics.Batch()

menu_bg = pyglet.shapes.Rectangle(
    x=0, y=0, width=window.width, height=window.height,
    color=(255, 255, 255, 255), batch=menu)

menu_title = pyglet.text.Label(
    'Minesweeper', font_name='Cascadia Mono', font_size=65,
    color=(0, 0, 0, 255), x=window.width // 2, y=500,
    anchor_x='center', anchor_y='top', batch=menu)

menu_difficulty_label = pyglet.text.Label(
    'Difficulty:', font_name='Cascadia Mono', font_size=18,
    color=(0, 0, 0, 255), x=window.width // 2, y=300,
    anchor_x='center', anchor_y='top', batch=menu)

menu_difficulty_text_hitbox = pyglet.shapes.Rectangle(
    x=window.width // 4, y=180, width=window.width // 2, height=80,
    color=(0, 0, 0, 50), batch=menu)

menu_difficulty_text = pyglet.text.Label(
    'EASY', font_name='Cascadia Mono', font_size=36,
    color=(0, 100, 0, 255), x=window.width // 2, y=250,
    anchor_x='center', anchor_y='top', batch=menu)

# Create the play button
menu_play_button_bg = pyglet.shapes.Rectangle(
    x=window.width // 2, y=55, width=100, height=100,
    color=(255, 255, 255, 0), batch=menu)
menu_play_button_bg.anchor_x = 50

menu_play_button = pyglet.shapes.Triangle(
    x=window.width // 2, y=100,
    x2=window.width // 2, y2=170,
    x3=window.width // 2 + 55, y3=135,
    color=(0, 100, 0, 255), batch=menu)
menu_play_button.anchor_position = 23, 30

# ------------------------

# Mouse events
@window.event
def on_mouse_motion(x, y, dx, dy):
    if minesweeper.state == 'menu':
        if (x, y) in menu_play_button_bg:
            menu_play_button_bg.color = (100, 100, 100, 100)
        else:
            menu_play_button_bg.color = (255, 255, 255, 0)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if minesweeper.state == 'menu':
        if (x, y) in menu_difficulty_text_hitbox:
            minesweeper.current_difficulty_index = (
                minesweeper.current_difficulty_index + 1
            ) % len(minesweeper.difficulty_array)
            menu_difficulty_text.text = (
                minesweeper.difficulty_array[
                    minesweeper.current_difficulty_index][0].upper())
            menu_difficulty_text.color = (
                minesweeper.difficulty_array[
                    minesweeper.current_difficulty_index][1])

        if (x, y) in menu_play_button_bg:
            minesweeper.start_game()

    elif minesweeper.state == 'game':
        grid_x = int(x // minesweeper.tile_size)
        grid_y = int(y // minesweeper.tile_size)
        grid_y = minesweeper.map.height - grid_y - 1

        if 0 <= grid_x < minesweeper.map.width and 0 <= grid_y < minesweeper.map.height:

            if button == pyglet.window.mouse.LEFT:
                result = minesweeper.map.uncover(grid_x, grid_y)
                update_tiles()

                # Handle game over
                if result == 'bomb':
                    reveal_all_bombs()
                    # Schedule game over state change after 1 second
                    pyglet.clock.schedule_once(set_game_over_state, 1.0)
                else:
                    if check_win():
                        pyglet.clock.schedule_once(set_win_state, 0.0)

            elif button == pyglet.window.mouse.RIGHT:
                # Place or remove a flag
                minesweeper.map.place_flag(grid_x, grid_y)
                update_tiles()

                if check_win():
                    pyglet.clock.schedule_once(set_win_state, 0.0)

    elif minesweeper.state in ['game_over', 'win']:
        # Restart the game
        minesweeper.reset_game()
        window.set_size(800, 600)

def update_tiles():
    # Existing code to update tiles and labels
    for y in range(minesweeper.map.height):
        for x in range(minesweeper.map.width):
            tile = minesweeper.tiles[y][x]
            status = minesweeper.map.uncovered[y][x]
            cell_value = minesweeper.map.map[y][x]

            # Update tile color based on status
            if status == 'h':
                tile.color = (200, 200, 200, 255)  # Hidden
                # Remove label if it exists
                if minesweeper.labels[y][x]:
                    minesweeper.labels[y][x].delete()
                    minesweeper.labels[y][x] = None
            elif status == 'v':
                if cell_value == -1:
                    # Uncovered bomb
                    tile.color = (0, 0, 0, 255)  # Black tile for bomb
                    # Remove label if it exists
                    if minesweeper.labels[y][x]:
                        minesweeper.labels[y][x].delete()
                        minesweeper.labels[y][x] = None
                else:
                    tile.color = (150, 150, 150, 255)  # Uncovered non-bomb tile
                    # Create or update label
                    if cell_value > 0:
                        if minesweeper.labels[y][x] is None:
                            # Assign colors based on the number
                            number_colors = {
                                1: (0, 0, 255, 255),      # Blue
                                2: (0, 128, 0, 255),      # Green
                                3: (255, 0, 0, 255),      # Red
                                4: (0, 0, 128, 255),      # Dark Blue
                                5: (128, 0, 0, 255),      # Dark Red
                                6: (0, 128, 128, 255),    # Teal
                                7: (0, 0, 0, 255),        # Black
                                8: (128, 128, 128, 255)   # Gray
                            }
                            color = number_colors.get(cell_value, (0, 0, 0, 255))  # Default to black
                            number_label = pyglet.text.Label(
                                text=str(cell_value),
                                font_name='Cascadia Mono',
                                font_size=24,
                                x=tile.x + minesweeper.tile_size / 2,
                                y=tile.y + minesweeper.tile_size / 2,
                                anchor_x='center',
                                anchor_y='center',
                                color=color,
                                batch=minesweeper.game
                            )
                            minesweeper.labels[y][x] = number_label
                    else:
                        # Remove label if cell is zero
                        if minesweeper.labels[y][x]:
                            minesweeper.labels[y][x].delete()
                            minesweeper.labels[y][x] = None
            elif status == 'f':
                tile.color = (255, 0, 0, 255)  # Flagged
                # Remove label if it exists
                if minesweeper.labels[y][x]:
                    minesweeper.labels[y][x].delete()
                    minesweeper.labels[y][x] = None

def check_win():
    for y in range(minesweeper.map.height):
        for x in range(minesweeper.map.width):
            cell_value = minesweeper.map.map[y][x]
            status = minesweeper.map.uncovered[y][x]
            if cell_value != -1 and status != 'v':
                # Found a non-bomb tile that's not uncovered yet
                return False
    return True

def reveal_all_bombs():
    for y in range(minesweeper.map.height):
        for x in range(minesweeper.map.width):
            if minesweeper.map.map[y][x] == -1:
                minesweeper.map.uncovered[y][x] = 'v'
    update_tiles()

def set_game_over_state(dt):
    minesweeper.state = 'game_over'
    # Make overlay elements visible
    minesweeper.overlay_rect.opacity = 200
    minesweeper.restart_label.color = (0, 0, 0, 255)
    # Set result label to "You Lose!" in red
    minesweeper.result_label.text = 'You Lose!'
    minesweeper.result_label.color = (255, 0, 0, 255)
    update_tiles()

def set_win_state(dt):
    minesweeper.state = 'win'
    # Make overlay elements visible
    minesweeper.overlay_rect.opacity = 200
    minesweeper.restart_label.color = (0, 0, 0, 255)
    # Set result label to "You Win!" in green
    minesweeper.result_label.text = 'You Win!'
    minesweeper.result_label.color = (0, 100, 0, 255)
    update_tiles()

# ------------------------

# Draw the window
@window.event
def on_draw():
    window.clear()
    if minesweeper.state == 'menu':
        menu.draw()
    else:
        minesweeper.game.draw()

pyglet.app.run()
