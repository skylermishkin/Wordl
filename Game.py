import Tkinter as tk
import time
import random

from Board import *
from Player import *
from Hand import *
from Tile import *


class Game(tk.Frame):
    """

    """




    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title("Grid Manager")

        for r in range(6):
            self.master.rowconfigure(r, weight=1)
        for c in range(5):
            self.master.columnconfigure(c, weight=1)
            tk.Button(master, text="Button {0}".format(c)).grid(row=6, column=c, sticky='ew')

        Frame1 = tk.Frame(master, bg="red", width=100, height=100)
        Frame1.grid(row=0, column=0, rowspan=3, columnspan=2, sticky='wens')
        Frame2 = tk.Frame(master, bg="blue", width=100, height=100)
        Frame2.grid(row=3, column=0, rowspan=3, columnspan=2, sticky='wens')
        Frame3 = tk.Frame(master, bg="green", width=300, height=200)
        Frame3.grid(row=0, column=2, rowspan=6, columnspan=3, sticky='wens')

    def start(self):
        root = tk.Tk()
        board = Board(root)
        board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        player1 = tk.PhotoImage(data=imagedata)
        board.addpiece("player1", player1, 1, 1)
        root.mainloop()
