import random
import copy


class Game():

    def __init__(self, debug=False):
        self.game_finished = False
        self.debug = debug
        self.bombs = 10
        self.GRID_SIZE = 6
        self.coordinates = [  # this represents the real board
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]

        self.SYMBOL_TABLE = {
            0: "~",  # empty space
            1: "~",  # hidden sub
            2: "X",  # hit sub
            3: "o"  # missed shot
        }
        self.LETTER_TO_NUM = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5
        }

        self.NUM_SUBS = 5
        self.hit_subs = 0

        # maybe won't use this
        self.VALID_LETTERS = ["a", "b", "c", "d", "e", "f"]
        self.VALID_NUMBERS = [1, 2, 3, 4, 5, 6]

    def _generate_board_view(self, coordinates):
        # should generate it programatically
        return f"""
                   |   | A | B | C | D | E | F |
                   | 1 | {self.SYMBOL_TABLE[coordinates[0][0]]} | {self.SYMBOL_TABLE[coordinates[0][1]]} | {self.SYMBOL_TABLE[coordinates[0][2]]} | {self.SYMBOL_TABLE[coordinates[0][3]]} | {self.SYMBOL_TABLE[coordinates[0][4]]} | {self.SYMBOL_TABLE[coordinates[0][5]]} |
                   | 2 | {self.SYMBOL_TABLE[coordinates[1][0]]} | {self.SYMBOL_TABLE[coordinates[1][1]]} | {self.SYMBOL_TABLE[coordinates[1][2]]} | {self.SYMBOL_TABLE[coordinates[1][3]]} | {self.SYMBOL_TABLE[coordinates[1][4]]} | {self.SYMBOL_TABLE[coordinates[1][5]]} |
                   | 3 | {self.SYMBOL_TABLE[coordinates[2][0]]} | {self.SYMBOL_TABLE[coordinates[2][1]]} | {self.SYMBOL_TABLE[coordinates[2][2]]} | {self.SYMBOL_TABLE[coordinates[2][3]]} | {self.SYMBOL_TABLE[coordinates[2][4]]} | {self.SYMBOL_TABLE[coordinates[2][5]]} |
                   | 4 | {self.SYMBOL_TABLE[coordinates[3][0]]} | {self.SYMBOL_TABLE[coordinates[3][1]]} | {self.SYMBOL_TABLE[coordinates[3][2]]} | {self.SYMBOL_TABLE[coordinates[3][3]]} | {self.SYMBOL_TABLE[coordinates[3][4]]} | {self.SYMBOL_TABLE[coordinates[3][5]]} |
                   | 5 | {self.SYMBOL_TABLE[coordinates[4][0]]} | {self.SYMBOL_TABLE[coordinates[4][1]]} | {self.SYMBOL_TABLE[coordinates[4][2]]} | {self.SYMBOL_TABLE[coordinates[4][3]]} | {self.SYMBOL_TABLE[coordinates[4][4]]} | {self.SYMBOL_TABLE[coordinates[4][5]]} |
                   | 6 | {self.SYMBOL_TABLE[coordinates[5][0]]} | {self.SYMBOL_TABLE[coordinates[5][1]]} | {self.SYMBOL_TABLE[coordinates[5][2]]} | {self.SYMBOL_TABLE[coordinates[5][3]]} | {self.SYMBOL_TABLE[coordinates[5][4]]} | {self.SYMBOL_TABLE[coordinates[5][5]]} |
        """

    def _has_remaining_bombs(self):
        return self.bombs > 0

    def _update_bombs(self):
        self.bombs -= 1

    def _get_bomb_position(self):
        return input(f"X = hit\no = miss\nBOMBS LEFT ({self.bombs})\nSCORE: {self.hit_subs}\nEnter bombing coordinates: \n ")

    def _place_submarines(self):

        subs_set = set()
        while len(subs_set) < self.NUM_SUBS:  # this might repeat values
            row, column = self._convert_value_to_cords(random.randint(0, 35))
            self.coordinates[row][column] = 1
            # this exists to populate the set and stop the while loop
            subs_set.add((row, column))

    def _convert_value_to_cords(self, value: int) -> tuple:
        row = value % self.GRID_SIZE
        column = value // self.GRID_SIZE
        return row, column

    def _convert_input_to_coords(self, input: str) -> tuple:
        return int(input[0]) - 1, self.LETTER_TO_NUM[input[1].lower()]

    def _register_missed_shot(self, coords):
        self.coordinates[coords[0]][coords[1]] = 3

    def _register_hit(self, coords):
        self.coordinates[coords[0]][coords[1]] = 2
        self.hit_subs += 1

    def _process_bombing(self, coords):
        hit_spot = self.coordinates[coords[0]][coords[1]]
        if hit_spot == 0:
            self._register_missed_shot(coords)

        elif hit_spot == 1:
            self._register_hit(coords)

        self.bombs -= 1

    def _lost_game(self):
        return self.bombs <= 0

    def _won_game(self):
        return self.hit_subs >= self.NUM_SUBS

    def _game_turn(self):
        if self.debug:
            print(self.coordinates)
        while not self.game_finished:
            print(self._generate_board_view(self.coordinates))
            attack = self._get_bomb_position()
            coords = self._convert_input_to_coords(attack)
            self._process_bombing(coords)
            if self._won_game():
                print("YOU WON!")
                break
            elif self._lost_game():
                print("YOU LOST")
                break

    def run(self):
        self._place_submarines()
        self._game_turn()


if __name__ == "__main__":
    game = Game(debug=True)
    game.run()
