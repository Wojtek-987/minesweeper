from map import Map

# create the window

# display menu

# initialize the game variables
game_map = Map(10, 5)
game_map.add_bombs(10)



# display the game in the window
while True:
    for y in range(5):
        for x in range(10):

            spacing = ' '

            if game_map.uncovered[y][x] == 'v':
                if game_map.map[y][x] == -1:
                    spacing = ''

                print('[' + spacing + str(game_map.map[y][x]), ']', end='')

            elif game_map.uncovered[y][x] == 'f':
                if game_map.map[y][x] == -1:
                    spacing = ''

                print('[ # ]', end='')

            elif game_map.uncovered[y][x] == 'h':
                print('[ - ]', end='')

        print()

    x = input('x: ')
    y = input('y: ')
    if game_map.uncover(int(x), int(y)) == 'bomb':
        print('You lost!')
        break

    game_map.uncover(int(x), int(y))
    # game_map.place_flag(int(x), int(y))
