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

        self.canvas.focus_set()
        # utility listeners - always on
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<Tab>', self._toggle_players_visibility)
        self._mousey = 0
        self._mousex = 0
        self.highlighting = False

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
                              px_x=(BOARD_WIDTH - 2) * self.twidth + LR_PAD,
                              px_y=3 * self.theight + TB_PAD,
                              width=1 * self.twidth,
                              height=6 * self.theight)
        self.d4 = Dice(sides=4)
        self.d4set = [Dice(sides=4,
                           canvas=self.canvas,
                           pxcoord=self.dice_grid.position_pxcoords[_],
                           grid=self.dice_grid,
                           freeze=True) for _ in range(NUM_D4)]
        self.d6 = Dice(sides=6)
        self.d6set = [Dice(sides=6,
                           canvas=self.canvas,
                           grid_pos=_,
                           grid=self.dice_grid,
                           freeze=True) for _ in range(NUM_D6)]
        self.d8 = Dice(sides=8)
        self.d8set = None
        self.d20 = Dice(sides=20)
        # canvas objects
        self.board = Board(self.canvas, self.grid,
                           width=BOARD_WIDTH, height=BOARD_HEIGHT,
                           tb_pad=TB_PAD, lr_pad=LR_PAD)
        self.players = []  # [[player, pos], ...]
        player_colors = ["yellow", "brown", "white", "grey"]
        for i in range(self.num_players):
            p = Player(self.canvas,
                       pxcoord=self.grid.pxcoord_from_coord((i, 0)),
                       grid=self.grid,
                       diameter=self.theight*0.5,
                       color=player_colors[i],
                       name="Player{}".format(i+1))
            p.is_active = True if i is 0 else False
            self.players.append([p, i])

        self.board.setup()
        self.board.create()
        for p in self.players:
            player = p[0]
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
        for p in self.players:
            player = p[0]
            if player.is_active:
                p[1] += 1
                p[1] = self.grid.sanitized_path_pos(p[1])
                x, y = self.grid.pxcoord_from_coord(self.grid.coord_from_path_pos(p[1]))
                player.move(x, y)

    def _move_player_down(self, event):
        print("Moving player down")
        for p in self.players:
            player = p[0]
            if player.is_active:
                p[1] -= 1
                p[1] = self.grid.sanitized_path_pos(p[1])
                x, y = self.grid.pxcoord_from_coord(self.grid.coord_from_path_pos(p[1]))
                player.move(x, y)

    def _collect_tile(self, event):
        for p in self.players:
            player = p[0]
            if player.is_active:
                for pos in self.board.tile_map:
                    if pos == p[1]:
                        print("Collecting {} tile.".format(self.board.tile_map[pos].text))
                        player.add_to_hand(self.board.tile_map[pos].text)
                        self.board.tile_map[pos].reroll()

    def _on_click(self, event):
        self._mousex, self._mousey = event.x, event.y
        # print("Click: {}, {}".format(self._mousex, self._mousey))
        if self.highlighting:
            # TODO: look for both dice and tiles to highlight
            grid_pos = self.dice_grid.position_snapped_to_grid((self._mousex, self._mousey))
            if grid_pos is not None:
                for die in self.d6set:
                    if die.grid_pos == grid_pos:
                        die.highlight()
                        # find tiles to highlight
                    else:  # make sure to unhighlight others
                        if die.highlighted:
                            die.unhighlight()

    def _toggle_players_visibility(self, event):
        print("Toggled player visibility")
        for p in self.players:
            player = p[0]
            player.toggle_visibility()

    def update(self):
        # control phases/stages, visibilities (like dice) and listeners
        if self.stage is None:  # initialize
            for die in self.d4set:
                die.reveal()
            self.stage = "determining_power"
            print("############DETERMINE POWERS############")
            print("{} begin your rolls".format(self.players[0][0].name))  # TODO better GUI visual

        if self.stage is "determining_power":
            self.power_determination()

        if self.stage is "collecting":
            self.collection()

        if self.stage is "finalizing":
            pass

        for p in self.players:
            player = p[0]
            player.update()
        self.canvas.update()

    def power_determination(self):
        """
        Regulates the game state while in the Power Determination phase.
        Will prompt each player to make their power rolls and trigger the collection phase once complete.
        """
        for i, p in enumerate(self.players):
            player = p[0]
            if player.is_active:
                if player.num_words is None:
                    if self._all_dice_rolled(self.d4set):
                        player.num_words = sum([die.value for die in self.d4set])
                        for die in self.d4set:
                            die.hide()
                            die.value = "#"
                        self.d8set = [Dice(sides=8,
                                           canvas=self.canvas,
                                           pxcoord=self.dice_grid.position_pxcoords[_],
                                           grid=self.dice_grid,
                                           freeze=True) for _ in range(player.num_words)]
                        for die in self.d8set:
                            die.reveal()
                else:  # Determine word lengths
                    if self._all_dice_rolled(self.d8set):
                        player.word_lengths = [die.value for die in self.d8set]
                        player.determine_power()
                        print("{} has {} power".format(player.name, player.power))
                        for die in self.d8set:
                            die.hide()
                        self.d8set = None
                        player.is_active = False
                        if i + 1 < len(self.players):
                            self.players[i+1][0].is_active = True
                            # TODO: make better GUI visual
                            print("{} begin your rolls".format(self.players[i+1][0].name))
                            for die in self.d4set:
                                die.reveal()
                                die.frozen = False
                        else:  # start back at player 1
                            self.players[0][0].is_active = True
                            # TODO better GUI visuals
                            print("############COLLECTION PHASE############")
                            self.stage = "collecting"
                            print("{} begin your turn".format(self.players[0][0].name))
                            for die in self.d6set:
                                die.reveal()

    def collection(self):
        """
        Regulates game state while in the collection phase.
        Will control player turns and their order. Prompts the active player for their rolls,
        then their moves, and finally for them to end their turn.
        """
        for i, p in enumerate(self.players):
            player = p[0]
            if player.is_active:
                if self._all_dice_rolled(self.d6set):
                    self.highlighting = True
                    # check highlighted tiles
                    # highlight board positions
                    pass  # TODO do move cascade

    def finalization(self):
        """
        Regullates game state while in the finalization phase.
        Will initiate a timer for each player to do any last re-arrangements of their hand, then
        scores up points.
        """
        # TODO
        pass

    @staticmethod
    def _all_dice_rolled(dice):
        for die in dice:
            if not die.frozen:
                return False
        return True

    @staticmethod
    def _num_dice_hidden(dice):
        result = 0
        for die in dice:
            result += 1 if die._hidden else 0
