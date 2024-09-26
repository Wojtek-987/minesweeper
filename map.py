import random


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for _ in range(self.width)] for _ in range(self.height)]
        # h - hidden, v - visible, f - flag
        self.uncovered = [['h' for _ in range(self.width)] for _ in range(self.height)]
        self.bomb_list = []

    def add_bombs(self, quantity):
        for _ in range(quantity):
            self._place_bomb()

        self._update_numbers()

    def _place_bomb(self):
        random_x = random.randrange(0, self.width)
        random_y = random.randrange(0, self.height)
        if self.map[random_y][random_x] != -1:
            self.map[random_y][random_x] = -1
            self.bomb_list.append((random_y, random_x))
        else:
            self._place_bomb()

    def _update_numbers(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] != -1:
                    # check for boundaries:

                    # top
                    if y > 0:
                        if self.map[y - 1][x] == -1:
                            self.map[y][x] += 1

                    # top right
                    if x < self.width - 1 and y > 0:
                        if self.map[y - 1][x + 1] == -1:
                            self.map[y][x] += 1

                    # right
                    if x < self.width - 1:
                        if self.map[y][x + 1] == -1:
                            self.map[y][x] += 1

                    # bottom right
                    if x < self.width - 1 and y < self.height - 1:
                        if self.map[y + 1][x + 1] == -1:
                            self.map[y][x] += 1

                    # bottom
                    if y < self.height - 1:
                        if self.map[y + 1][x] == -1:
                            self.map[y][x] += 1

                    # bottom left
                    if x > 0 and y < self.height - 1:
                        if self.map[y + 1][x - 1] == -1:
                            self.map[y][x] += 1

                    # left
                    if x > 0:
                        if self.map[y][x - 1] == -1:
                            self.map[y][x] += 1

                    # top left
                    if x > 0 and y > 0:
                        if self.map[y - 1][x - 1] == -1:
                            self.map[y][x] += 1

    def uncover(self, x, y):
        # if out of bounds
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return 'passed'

        # if is uncovered or flag
        if self.uncovered[y][x] in ['v', 'f']:
            return 'passed'

        self.uncovered[y][x] = 'v'

        # if is bomb
        if self.map[y][x] == -1:
            return 'bomb'

        # uncover neighbouring empty cells recursively
        self._ripple(x, y)

        return 'uncovered'

    def _ripple(self, x, y):
        # if cell is not empty, break recursion
        if self.map[y][x] != 0:
            return

        directions = [
            (0, -1),  # top
            (1, 0),  # right
            (0, 1),  # bottom
            (-1, 0),  # left
        ]

        # Check adjacent cells
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                if self.uncovered[new_y][new_x] == 'h':
                    self.uncover(new_x, new_y)

    def place_flag(self, x, y):
        self.uncovered[y][x] = 'f'
