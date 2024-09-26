import pyglet
from map import Map


class GameWindow:
    def __init__(self, root):
        pass

    def _get_game_settings(self, difficulty):

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

    def _open_menu(self):
        # add buttons for difficulty
        pass


    def _open_game(self, difficulty):

        tile_size = 50

        width, height, bombs = self._get_game_settings(difficulty)

        minesweeper = Map(width, height)
        minesweeper.add_bombs(bombs)

        # create the game window




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
