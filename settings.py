# Global settings and data for the game
WIDTH = 1000
HEIGHT = 600

POWER_LENGTHS = {1: range(2,12),
                 2: range(12,17),
                 3: range(17,22),
                 4: range(22,27),
                 5: range(27,33),
                 6: range(33,65)}

RANK_COLORS = {0: "blue",
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
