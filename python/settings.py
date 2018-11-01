import json
import glob


# Global settings and data for the game
WIDTH = 1400
HEIGHT = 800

LR_PAD = 50
TB_PAD = 50

BOARD_WIDTH = 18
BOARD_HEIGHT = 10

HAND_WIDTH = 8
HAND_HEIGHT = 10

NUM_D6 = 6
NUM_D4 = 2

HIGHLIGHT_WIDTH = 7

PROMPT_GRIDPOS = 13 + (BOARD_WIDTH-1) * 2

PLAYERSTAT_GRIDPOS = 15 + (BOARD_WIDTH-1) * 4

POWER_LENGTHS = {1: range(2,12),
                 2: range(12,17),
                 3: range(17,22),
                 4: range(22,27),
                 5: range(27,33),
                 6: range(33,65)}

RANK_COLOR = {0: "blue",
               1: "green",
               2: "red",
               3: "black",
               4: "purple"}

RANK_LETTERS = {0: {"A", "E"},
                1: {"I", "L", "O", "N", "S", "R", "T"},
                2: {"C", "D", "G", "H", "M", "P", "U"},
                3: {"B", "F", "K", "W", "Y"},
                4: {"J", "Q", "V", "X", "Z"}}

LETTER_RANK = {letter: rank for rank in RANK_LETTERS for letter in RANK_LETTERS[rank]}

RANK_POP = {0: 2,
            1: 4,
            2: 4,
            3: 2,
            4: 2}

RANK_WEIGHT = {0: float(RANK_POP[0]) / sum(RANK_POP.values()),
               1: float(RANK_POP[1]) / sum(RANK_POP.values()),
               2: float(RANK_POP[2]) / sum(RANK_POP.values()),
               3: float(RANK_POP[3]) / sum(RANK_POP.values()),
               4: float(RANK_POP[4]) / sum(RANK_POP.values())}

DICTIONARY_RELPATH = glob.glob("./Enable_dictionary.txt")[0]
DICTIONARY = []
with open(DICTIONARY_RELPATH, "r") as f:
    for line in f:
        DICTIONARY.append(line.rstrip())


'''
self.max_grid = Grid(HAND_WIDTH, HAND_HEIGHT,
                     px_x=2 * self.grid.twidth + LR_PAD,
                     px_y=2 * self.grid.theight + TB_PAD,
                     width=int(BOARD_WIDTH / 3) * self.grid.twidth,
                     height=int(BOARD_HEIGHT - 4) * self.grid.theight)

self.min_grid = Grid(HAND_WIDTH, HAND_HEIGHT,
                     px_x=(2 + HAND_WIDTH) * self.grid.twidth + LR_PAD,
                     px_y=(2 + HAND_HEIGHT) * self.grid.theight + TB_PAD,
                     width=self.grid.twidth,
                     height=self.grid.theight)
'''
