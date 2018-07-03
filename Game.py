from Board import *
from Player import *
from Grid import *
from Dice import *
from settings import *


class Game(object):
    def __init__(self, canvas, num_players=1, *args, **kwargs):
        """ctor

        :param canvas:
        :param numplayers:
        :param args:
        :param kwargs:
        """
        self.canvas = canvas
        self.num_players = num_players

        self.d4 = Dice(sides=4)
        self.d4set = [Dice(sides=4) for _ in range(NUM_D4)]
        self.d6 = Dice(sides=6)
        self.d6set = [Dice(sides=6) for _ in range(NUM_D6)]
        self.d8 = Dice(sides=8)
        self.d20 = Dice(sides=20)

        # stages can be {"determining_power", "collecting", "finalizing"}
        self.stage = "determining_power"
        self.pending_user_input = False

        self.canvas.focus_set()
        # utility listeners - always on
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<Tab>', self._toggle_players_visibility)
        self._mousey = 0
        self._mousex = 0

        self.cwidth = self.canvas.winfo_reqwidth()
        self.cheight = self.canvas.winfo_reqheight()
        self.twidth = (self.cwidth - LR_PAD * 2) / (BOARD_WIDTH + 1)
        self.theight = (self.cheight - TB_PAD * 2) / (BOARD_HEIGHT + 2)
        self.grid = Grid(BOARD_WIDTH, BOARD_HEIGHT,
                         px_x=LR_PAD,
                         px_y=self.theight + TB_PAD,
                         width=self.twidth * BOARD_WIDTH,
                         height=self.theight * BOARD_HEIGHT)
        # canvas objects
        self.board = Board(self.canvas, self.grid,
                           width=BOARD_WIDTH, height=BOARD_HEIGHT,
                           tb_pad=TB_PAD, lr_pad=LR_PAD,)
        self.players = {}
        for i in range(self.num_players):
            p = Player(self.canvas,
                       coords=self.grid.pxcoord_from_coord((i, 0)),
                       diameter=self.theight*0.5)
            p.is_active = True if i is 0 else False
            self.players[p] = i

        self.board.setup()
        self.board.create()
        for player in self.players:
            player.create()

        self._start_listeners()

    def update(self):
        for player in self.players:
            player.hand.update()
        self.canvas.after(10)
        self.canvas.update()

    def _start_listeners(self, groups={"movement", "pickup"}):
        if "movement" in groups:
            # simple player movement
            self.canvas.bind("<Up>", self._move_player_up)
            self.canvas.bind("<Down>", self._move_player_down)
        if "pickup" in groups:
            # simple tile pickup
            self.canvas.bind("<space>", self._collect_tile)
        if "rolling" in groups:
            pass # TODO

    def _kill_listeners(self,  groups={"movement", "pickup"}):
        if "movement" in groups:
            # simple player movement
            self.canvas.bind("<Up>", self._ignore)
            self.canvas.bind("<Down>", self._ignore)
        if "pickup" in groups:
            # simple tile pickup
            self.canvas.bind("<space>", self._ignore)
        if "rolling" in groups:
            pass # TODO

    @staticmethod
    def _ignore(self, event):
        # for "killing" listeners
        pass

    def _move_player_up(self, event):
        print("Moving player up")
        for player in self.players:
            if player.is_active:
                self.players[player] += 1
                self.players[player] = self.grid.sanitized_path_pos(self.players[player])
                x, y = self.grid.pxcoord_from_coord(self.grid.coord_from_path_pos(self.players[player]))
                player.move(x - player.coords[0], y - player.coords[1])

    def _move_player_down(self, event):
        print("Moving player down")
        for player in self.players:
            if player.is_active:
                self.players[player] -= 1
                self.players[player] = self.grid.sanitized_path_pos(self.players[player])
                x, y = self.grid.pxcoord_from_coord(self.grid.coord_from_path_pos(self.players[player]))
                player.move(x - player.coords[0], y - player.coords[1])

    def _collect_tile(self, event):
        for player in self.players:
            if player.is_active:
                for pos in self.board.tile_map:
                    if pos == self.players[player]:
                        print("Collecting {} tile.".format(self.board.tile_map[pos].text))
                        player.add_to_hand(self.board.tile_map[pos].text)
                        self.board.tile_map[pos].reroll()

    def _on_click(self, event):
        self._mousex, self._mousey = event.x, event.y
        print("Click: {}, {}".format(self._mousex, self._mousey))

    def _toggle_players_visibility(self, event):
        print("Toggled player visibility")
        for player in self.players:
            player.toggle_visibility()

    def prompt_power_rolls(self):
        # TODO
        pass
