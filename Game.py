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
        self.twidth = int(float(self.cwidth - LR_PAD * 2) / BOARD_WIDTH)
        self.theight = int(float(self.cheight - TB_PAD * 2) / BOARD_HEIGHT)
        self.grid = Grid(BOARD_WIDTH, BOARD_HEIGHT,
                         px_x=LR_PAD,
                         px_y=TB_PAD,
                         width=self.twidth * BOARD_WIDTH,
                         height=self.theight * BOARD_HEIGHT)
        self.dice_grid = Grid(1, 8,
                              px_x=(BOARD_WIDTH - 3) * self.twidth + LR_PAD,
                              px_y=2 * self.theight + TB_PAD,
                              width=self.twidth,
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
        self.active_dice = self.d4set
        # canvas objects
        self.board = Board(self.canvas, self.grid,
                           width=BOARD_WIDTH, height=BOARD_HEIGHT,
                           tb_pad=TB_PAD, lr_pad=LR_PAD)
        self.players = []  # [[player, pos], ...]
        player_colors = ["yellow", "brown", "white", "grey"]
        for i in range(self.num_players):
            p = Player(self.canvas,
                       grid_pos=i,
                       grid=self.grid,
                       diameter=self.theight*0.5,
                       color=player_colors[i],
                       name="Player{}".format(i+1))
            p.is_active = True if i is 0 else False
            self.players.append([p, i])
        self._prompt_box = None
        self._stat_box = None

        self._prompt_text = ""

        self.board.setup()
        self.board.create()
        for p in self.players:
            p[0].reveal()

    def _collect_tile(self, event=None):
        for p in self.players:
            player = p[0]
            if player.is_active:
                for pos in self.board.tile_map:
                    if pos == p[1]:
                        print("Collecting {} tile.".format(self.board.tile_map[pos].text))
                        player.add_to_hand(self.board.tile_map[pos].text)
                        self.board.tile_map[pos].reroll()

    def _use_move(self, path_pos):
        for p in self.players:
            player = p[0]
            if player.is_active:
                p[1] = self.grid.sanitized_path_pos(path_pos)
                x, y = self.grid.pxcoord_from_path_pos(p[1])
                player.move(x, y)
                self._collect_tile()
                for die in self.d6set:
                    if die.highlighted:
                        die.unhighlight()
                        self.board.unhighlight()
                        die.hide()
                        player.hide()
                        player.reveal()
            player.hide()
            player.reveal()

    def _on_click(self, event):
        self._mousex, self._mousey = event.x, event.y
        # print("Click: {}, {}".format(self._mousex, self._mousey))
        if self.highlighting:  # highlight path positions for the active player
            dice_pos = self.dice_grid.position_from_pxcoord((self._mousex, self._mousey))
            board_pos = self.grid.path_pos_from_pxcoord((self._mousex, self._mousey))
            print("Clicked dice {}, board {}".format(dice_pos, board_pos))
            if dice_pos is not None:
                for die in self.d6set:
                    reached_positions = self.__reached_path_positions(die.value)
                    if die.grid_pos == dice_pos and not die.is_hidden():
                        die.highlight()
                        self.board.highlight(reached_positions)
                    else:  # make sure to un-highlight
                        if die.highlighted:
                            die.unhighlight()
                            self.board.unhighlight(reached_positions)
                for p in self.players:
                    p[0].hide()
                    p[0].reveal()
            elif board_pos is not None:
                reached_positions = []
                for die in self.d6set:
                    if die.highlighted:
                        reached_positions = self.__reached_path_positions(die.value)
                if board_pos in reached_positions:
                    self._use_move(board_pos)
        else:  # roll dice
            dice_pos = self.dice_grid.position_from_pxcoord((self._mousex, self._mousey))
            if dice_pos is not None:
                for die in self.active_dice:
                    die.roll()

    def __reached_path_positions(self, dist):
        """The positions on the board path reached from the active player by the dist.

        :param dist:
        :return int, int: forward and reverse positions on the path
        """
        for p in self.players:
            if p[0].is_active:
                return (self.grid.sanitized_path_pos(p[0].grid_pos + dist),
                        self.grid.sanitized_path_pos(p[0].grid_pos - dist))

    def _toggle_players_visibility(self, event=None):
        print("Toggled player visibility")
        for p in self.players:
            player = p[0]
            player.toggle_visibility()

    def update(self):
        # control phases/stages, visibilities (like dice) and listeners
        self.canvas.update_idletasks()
        if self.stage is None:  # initialize
            for die in self.d4set:
                die.reveal()
            self.stage = "determining_power"
            print("\n###############\nDETERMINE POWERS\n###############\n")
            print("{} begin your rolls".format(self.players[0][0].name))
            self._prompt_text = "{}'s roll".format(self.players[0][0].name)

        if self.stage is "determining_power":
            self.power_determination()

        if self.stage is "collecting":
            self.collection()

        if self.stage is "finalizing":
            self.finalization()

        for p in self.players:
            player = p[0]
            player.update()
            player.hand.update()
        self._prompt(show_player_stats=False if (self.stage is None or self.stage is "determining_power") else True)
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
                    if self._all_dice_rolled():
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
                        self.active_dice = self.d8set
                else:  # Determine word lengths
                    if self._all_dice_rolled():
                        player.word_lengths = sorted([die.value for die in self.d8set], reverse=True)
                        player.determine_power()
                        player.update()
                        print("{} has {} power".format(player.name, player.power))
                        for die in self.d8set:
                            die.hide()
                        self.d8set = None
                        player.is_active = False
                        if i + 1 < len(self.players):
                            self.players[i+1][0].is_active = True
                            print("\n{} begin your rolls".format(self.players[i+1][0].name))
                            self._prompt_text = "{}'s roll".format(self.players[i+1][0].name)
                            for die in self.d4set:
                                die.reveal()
                                die.frozen = False
                            self.active_dice = self.d4set
                        else:  # start back at player 1
                            self.players[0][0].is_active = True
                            self.players[0][0].hand.reveal()
                            print("\n###############\nCOLLECTION PHASE\n###############\n")
                            self.stage = "collecting"
                            print("\n{} begin your turn".format(self.players[0][0].name))
                            self._prompt_text = "{}'s turn".format(self.players[0][0].name)
                            for die in self.d6set:
                                die.reveal()
                            self.active_dice = self.d6set
                break

    def collection(self):
        """
        Regulates game state while in the collection phase.
        Will control player turns and their order. Prompts the active player for their rolls,
        then their moves, and finally for them to end their turn.
        """
        for i, p in enumerate(self.players):
            player = p[0]
            if player.is_active:
                #player.maximize_hand()  # TODO
                if self._all_dice_rolled():
                    self.highlighting = True
                if self._all_moves_used():
                    self.highlighting = False
                    player.is_active = False
                    player.hand.hide()
                    player.update()
                    #player.minimize_hand()  # TODO
                    if i + 1 < len(self.players):
                        print("{} start your turn".format(self.players[i+1][0].name))
                        self._prompt_text = "{}'s turn".format(self.players[i+1][0].name)
                        self.players[i+1][0].is_active = True
                        self.players[i + 1][0].hand.reveal()
                        self.players[i + 1][0].update()
                        # self.players[i + 1][0].maximize_hand()  # TODO
                    else:
                        print("{} start your turn".format(self.players[0][0].name))
                        self._prompt_text = "{}'s turn".format(self.players[0][0].name)
                        self.players[0][0].is_active = True
                        self.players[0][0].hand.reveal()
                        self.players[0][0].update()
                        # self.players[0][0].maximize_hand()  # TODO
                    for die in self.d6set:
                        die.highlighted = False
                        die.frozen = False
                        die.value = "#"
                        die.hide()
                        die.reveal()
                break

    def finalization(self):
        """
        Regullates game state while in the finalization phase.
        Will initiate a timer for each player to do any last re-arrangements of their hand, then
        scores up points.
        """
        # TODO
        pass

    def _all_moves_used(self):
        for p in self.players:
            player = p[0]
            if player.is_active:
                break
        moves_used = 0
        for die in self.d6set:
            if die.is_hidden():
                moves_used += 1
        if moves_used == player.power:
            return True
        return False

    def _all_dice_rolled(self):
        for die in self.active_dice:
            if not die.frozen:
                return False
        return True

    @staticmethod
    def _num_dice_hidden(dice):
        result = 0
        for die in dice:
            result += 1 if die.is_hidden() else 0
        return result

    def _prompt(self, text=None, show_player_stats=True):
        if text is not None:
            self._prompt_text = text

        # clear old canvas items
        if self._prompt_box is not None:
            self.canvas.delete(self._prompt_box)
            self.canvas.delete(self._stat_box)

        # get active player
        for p in self.players:
            if p[0].is_active:
                active_player = p[0]
                break

        # Game phase prompt
        self._prompt_box = self.canvas.create_text(*self.grid.position_pxcoords[PROMPT_GRIDPOS],
                                                   text=self._prompt_text,
                                                   font="Comic {} bold".format(int(self.grid.theight / 2)),
                                                   fill="black")

        if show_player_stats:
            moves = "NA" if self.active_dice is not self.d6set else active_player.power - self._num_dice_hidden(self.d6set)
            # player stat box
            self._stat_box = self.canvas.create_text(*self.grid.position_pxcoords[PLAYERSTAT_GRIDPOS],
                                 text="Power: {}  Moves: {}\nWord lengths: {}".format(active_player.power,
                                                                                      moves,
                                                                                      active_player.word_lengths),
                                 font="Comic {} bold".format(int(self.grid.theight / 3)),
                                 fill="black")
