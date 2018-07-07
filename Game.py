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

        # stages can be {"determining_power", "collecting", "finalizing"}
        self.stage = None
        self.pending_rolls = False
        self.pending_moves = False

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
        self.dice_grid = Grid(1, 8,
                              px_x=12 * self.twidth + LR_PAD,
                              px_y=(BOARD_HEIGHT - HAND_HEIGHT + 2) * self.theight + TB_PAD,
                              width=1 * self.twidth,
                              height=6 * self.theight)
        self.d4 = Dice(sides=4)
        self.d4set = [Dice(sides=4,
                           canvas=self.canvas,
                           pxcoord=self.dice_grid.pxcoord_from_coord(self.dice_grid.coord_from_pos(_)),
                           grid=self.dice_grid,
                           freeze=True) for _ in range(NUM_D4)]
        self.d6 = Dice(sides=6)
        self.d6set = [Dice(sides=6,
                           canvas=self.canvas,
                           pxcoord=self.dice_grid.pxcoord_from_coord(self.dice_grid.coord_from_pos(_)),
                           grid=self.dice_grid,
                           freeze=True) for _ in range(NUM_D6)]
        self.d8 = Dice(sides=8)
        self.d8set = None
        self.d20 = Dice(sides=20)
        # canvas objects
        self.board = Board(self.canvas, self.grid,
                           width=BOARD_WIDTH, height=BOARD_HEIGHT,
                           tb_pad=TB_PAD, lr_pad=LR_PAD)
        self.players = {}  # {Player: pos, ...}
        for i in range(self.num_players):
            p = Player(self.canvas,
                       pxcoord=self.grid.pxcoord_from_coord((i, 0)),
                       grid=self.grid,
                       diameter=self.theight*0.5)
            p.is_active = True if i is 0 else False
            self.players[p] = i

        self.board.setup()
        self.board.create()
        for player in self.players:
            player.reveal()

    def _start_listeners(self, groups={"movement", "pickup"}):
        """

        :param groups: {"movement", "pickup"}
        :return:
        """
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
        """

        :param groups: {"movement", "pickup"}
        :return:
        """
        if "movement" in groups:
            # simple player movement
            self.canvas.bind("<Up>", self._ignore)
            self.canvas.bind("<Down>", self._ignore)
        if "pickup" in groups:
            # simple tile pickup
            self.canvas.bind("<space>", self._ignore)
        if "rolling" in groups:
            pass  # TODO

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
                player.move(x, y)

    def _move_player_down(self, event):
        print("Moving player down")
        for player in self.players:
            if player.is_active:
                self.players[player] -= 1
                self.players[player] = self.grid.sanitized_path_pos(self.players[player])
                x, y = self.grid.pxcoord_from_coord(self.grid.coord_from_path_pos(self.players[player]))
                player.move(x, y)

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

    def update(self):
        # TODO control phases/stages, visibilities (like dice) and listeners
        if self.stage is None:
            for die in self.d4set:
                die.reveal()
            self.pending_rolls = True
            self.stage = "determining_power"
            print("############DETERMINE POWERS############")

        if self.stage is "determining_power":
            self.power_determination()

        elif self.stage is "collecting":
            if not self.pending_moves:
                for die in self.d6set:
                    die.reveal()
                    die.frozen = False
                self.pending_rolls = True
                self._start_listeners({"movement", "pickup"})
            self.collection()

        for player in self.players:
            player.hand.update()
        self.canvas.update()

    def power_determination(self):
        all_determined = True
        for player, pos in sorted(self.players.iteritems()):  # this should keep it in order right? :eek:
            # TODO visual prompt for specific player
            if player.num_words is None:
                all_determined = False
                all_rolled = True
                for die in self.d4set:
                    if not die.frozen:
                        all_rolled = False
                        break
                if all_rolled:
                    player.num_words = sum([die.value for die in self.d4set])
                    for die in self.d4set:
                        die.frozen = False
            elif player.word_lengths is None:
                all_determined = False
                all_rolled = True
                # !!!! hide and reveal in this scope will iterate every game frame :(
                for die in self.d4set:
                    die.hide()
                if self.d8set is None:
                    self.d8set = [Dice(sides=8,
                               canvas=self.canvas,
                               pxcoord=self.dice_grid.pxcoord_from_coord(self.dice_grid.coord_from_pos(_)),
                               grid=self.dice_grid,
                               freeze=True) for _ in range(player.num_words)]
                for die in self.d8set:
                    die.reveal()
                    if not die.frozen:
                        all_rolled = False
                if all_rolled:
                    player.word_lengths = []
                    for die in self.d8set:
                        player.word_lengths.append(die.value)
                        die.hide()
                    player.power = player.determine_power(player.word_lengths)
                    print("Player has {} power".format(player.power))
                    self.d8set = None
        if all_determined:
            print("############COLLECTION PHASE############")
            self.stage = "collecting"
            self.pending_rolls = False

    def collection(self):
        # TODO
        # wait for rolls
        # for move in range power
        #   wait for die highlight, and highlight the positions
        #   wait for position selection, and move player and collect
        if self.pending_rolls:
            all_rolled = True
            for die in self.d6set:
                if not die.frozen:
                    all_rolled = False
            if all_rolled:
                self.pending_rolls = False
                self.pending_moves = True
        if self.pending_moves:
            moves_taken = 0
            
