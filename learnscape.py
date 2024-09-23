#!/usr/bin/env python3

#
# Author: Sean O'Beirne
# Date: 9-22-2024
# File: learnscape.py
# Usage: python3 learnscape
#

#
# Visualize various computer science elements
#


import curses
from curses.textpad import rectangle

import random

import subprocess, os, sys

import time

import logging

# Configure logging
logging.basicConfig(filename= f"{__file__}/../debug.log", level=logging.DEBUG, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

stdscr = curses.initscr()


curses.start_color()
curses.use_default_colors()

# Define colors
def hex_to_rgb(hexstring):
    r = int(int(hexstring[0:2], 16) * 1000 / 255)
    g = int(int(hexstring[2:4], 16) * 1000 / 255)
    b = int(int(hexstring[4:6], 16) * 1000 / 255)
    return (r, g, b)

green = hex_to_rgb("29ad2b")
brown = hex_to_rgb("896018")
white = hex_to_rgb("ffffff")
black = hex_to_rgb("000000")

tn_bg = hex_to_rgb("24283b")
tn_bg_dark = hex_to_rgb("1f2335")
tn_bg_highlight = hex_to_rgb("292e42")
tn_blue = hex_to_rgb("7aa2f7")
tn_blue0 = hex_to_rgb("3d59a1")
tn_blue1 = hex_to_rgb("2ac3de")
tn_blue2 = hex_to_rgb("0db9d7")
tn_blue5 = hex_to_rgb("89ddff")
tn_blue6 = hex_to_rgb("b4f9f8")
tn_blue7 = hex_to_rgb("394b70")
tn_comment = hex_to_rgb("565f89")
tn_cyan = hex_to_rgb("7dcfff")
tn_dark3 = hex_to_rgb("545c7e")
tn_dark5 = hex_to_rgb("737aa2")
tn_fg = hex_to_rgb("c0caf5")
tn_fg_dark = hex_to_rgb("a9b1d6")
tn_fg_gutter = hex_to_rgb("3b4261")
tn_green = hex_to_rgb("9ece6a")
tn_green1 = hex_to_rgb("73daca")
tn_green2 = hex_to_rgb("41a6b5")
tn_magenta = hex_to_rgb("bb9af7")
tn_magenta2 = hex_to_rgb("ff007c")
tn_orange = hex_to_rgb("ff9e64")
tn_purple = hex_to_rgb("9d7cd8")
tn_red = hex_to_rgb("f7768e")
tn_red1 = hex_to_rgb("db4b4b")
tn_teal = hex_to_rgb("1abc9c")
tn_terminal_black = hex_to_rgb("414868")
tn_yellow = hex_to_rgb("e0af68")
tn_git_add = hex_to_rgb("449dab")
tn_git_change = hex_to_rgb("6183bb")
tn_git_delete = hex_to_rgb("914c54")



COLOR_BLACK = 0
COLOR_RED = 1
COLOR_GREEN = 2
COLOR_ORANGE = 3
COLOR_BLUE = 4
COLOR_MAGENTA = 5
COLOR_CYAN = 6
COLOR_WHITE = 7
COLOR_DARK_GREY = 8
COLOR_LIGHT_RED = 9
COLOR_LIGHT_GREEN = 10
COLOR_YELLOW = 11
COLOR_LIGHT_BLUE = 12
COLOR_PURPLE = 13
COLOR_BROWN = 14
COLOR_DIM_WHITE = 15

# RGB values (0-1000 scale)
color_definitions = {
    COLOR_BLACK: black,
    COLOR_RED: tn_red1,
    COLOR_GREEN: green,
    COLOR_ORANGE: tn_orange,
    COLOR_BLUE: tn_blue0,
    COLOR_MAGENTA: tn_magenta2,
    COLOR_CYAN: tn_cyan,
    COLOR_WHITE: white,
    COLOR_DARK_GREY: tn_dark5,
    COLOR_LIGHT_RED: tn_red,
    COLOR_LIGHT_GREEN: tn_green,
    COLOR_YELLOW: tn_yellow,
    COLOR_LIGHT_BLUE: tn_blue,
    COLOR_PURPLE: tn_purple,
    COLOR_BROWN: brown,
    COLOR_DIM_WHITE: tn_fg,
}



# Initialize 16 colors
def init_16_colors():
    curses.start_color()
    
    if curses.can_change_color():
        for color, rgb in color_definitions.items():
            curses.init_color(color, *rgb)
    
    # Define color pairs using custom color numbers
    curses.init_pair(1, COLOR_BLACK, COLOR_BLACK)
    curses.init_pair(2, COLOR_RED, COLOR_BLACK)
    curses.init_pair(3, COLOR_GREEN, COLOR_BLACK)
    curses.init_pair(4, COLOR_ORANGE, COLOR_BLACK)
    curses.init_pair(5, COLOR_BLUE, COLOR_BLACK)
    curses.init_pair(6, COLOR_MAGENTA, COLOR_BLACK)
    curses.init_pair(7, COLOR_CYAN, COLOR_BLACK)
    curses.init_pair(8, COLOR_WHITE, COLOR_BLACK)
    curses.init_pair(9, COLOR_DARK_GREY, COLOR_BLACK)
    curses.init_pair(10, COLOR_LIGHT_RED, COLOR_BLACK)
    curses.init_pair(11, COLOR_LIGHT_GREEN, COLOR_BLACK)
    curses.init_pair(12, COLOR_YELLOW, COLOR_BLACK)
    curses.init_pair(13, COLOR_LIGHT_BLUE, COLOR_BLACK)
    curses.init_pair(14, COLOR_PURPLE, COLOR_BLACK)
    curses.init_pair(15, COLOR_BROWN, COLOR_BLACK)
    curses.init_pair(16, COLOR_DIM_WHITE, COLOR_RED)

init_16_colors()

BLACK = curses.color_pair(1)
RED = curses.color_pair(2)
GREEN = curses.color_pair(3)
ORANGE = curses.color_pair(4)
BLUE = curses.color_pair(5)
MAGENTA = curses.color_pair(6)
CYAN = curses.color_pair(7)
WHITE = curses.color_pair(8)
DARK_GREY = curses.color_pair(9)
LIGHT_RED = curses.color_pair(10)
LIGHT_GREEN = curses.color_pair(11)
YELLOW = curses.color_pair(12)
LIGHT_BLUE = curses.color_pair(13)
PURPLE = curses.color_pair(14)
BROWN = curses.color_pair(15)
DIM_WHITE = curses.color_pair(16)




HEADER = [
r"""  ,--.                             ,---.                            """, 
r"""  |  |   ,---. ,--,--,--.--,--,--,'   .-' ,---.,--,--.,---. ,---.   """, 
r"""  |  |  | .-. ' ,-.  |  .--|      `.  `-.| .--' ,-.  | .-. | .-. :  """, 
r"""  |  '--\   --\ '-'  |  |  |  ||  .-'    \ `--\ '-'  | '-' \   --.  """, 
r"""  `-----'`----'`--`--`--'  `--''--`-----' `---'`--`--|  |-' `----'  """, 
]

# Box drawing characters
V  = '│'
H  = '─'
TL = '╭'
TR = '╮'
BL = '╰'
BR = '╯'
# horizup = '┴'
# horizdown = '┬'
# vertleft =  '┤'
# vertright = '├'
# verthoriz = '┼'

BORDER_COLOR = PURPLE

running = True

wins = []
CTRLPANEL_I = 0
STATUSPANEL_I = 1
TITLEPANEL_I = 2
MENUPANEL_I = 3
OPTIONSPANEL_I = 4

actions = {}



def draw():
    # Clear screen
    stdscr.clear()

    # Turn off cursor blinking and echoing
    curses.curs_set(0)
    curses.noecho()
    curses.set_escdelay(1)

    stdscr.bkgd(' ', WHITE)



def draw_win(win: curses.window, borders=True, ascii=False, color=WHITE):
    height, width = win.getmaxyx()
    h = height - 1
    w = width - 2
    if borders:
        for i in range(1, w):
            win.addch(0, i, H, BORDER_COLOR)
            win.addch(h, i, H, BORDER_COLOR)
        for i in range(1, h):
            win.addch(i, 0, V, BORDER_COLOR)
            win.addch(i, w, V, BORDER_COLOR)
        win.addch(0, 0, TL, BORDER_COLOR)
        win.addch(h, 0, BL, BORDER_COLOR)
        win.addch(0, w, TR, BORDER_COLOR)
        win.addch(h, w, BR, BORDER_COLOR)
    if ascii:
        for i, line in enumerate(HEADER):
            win.addstr(i+1, 1, line, color)


def draw_wins(height, width):
    # bottom-left control panel
    ctrlpanel_height = 6
    ctrlpanel_width = 15
    ctrlpanel_y = height - ctrlpanel_height
    ctrlpanel_x = 0
    ctrlpanel = curses.newwin(ctrlpanel_height, ctrlpanel_width, ctrlpanel_y, ctrlpanel_x)
    ctrlpanel.bkgd(WHITE)
    ctrlpanel_text = [
        "p - pause",
        "r - reset",
        "? - help",
        "q - quit"
    ]
    for i in range(len(ctrlpanel_text)):
        ctrlpanel.addstr(i+1, 2, ctrlpanel_text[i])
    draw_win(ctrlpanel)
    wins.append(ctrlpanel)

    # bottom status bar
    statuspanel_height = 4
    statuspanel_width = width - ctrlpanel_width - 2
    statuspanel_y = height - statuspanel_height
    statuspanel_x = ctrlpanel_width + 1
    statuspanel = curses.newwin(statuspanel_height, statuspanel_width, statuspanel_y, statuspanel_x)
    statuspanel.bkgd(WHITE)
    statuspanel_text = [
        "p - pause",
        "r - reset",
    ]
    for i, line in enumerate(statuspanel_text):
        x = (statuspanel_width-1) // 2 - len(line) // 2
        statuspanel.addstr(i+1, x, line)
    draw_win(statuspanel)
    wins.append(statuspanel)

    # top left title
    titlepanel_height = 7
    titlepanel_width = 71
    titlepanel_y = 0
    titlepanel_x = 0
    titlepanel = curses.newwin(titlepanel_height, titlepanel_width, titlepanel_y, titlepanel_x)
    titlepanel.bkgd(WHITE)
    draw_win(titlepanel, ascii=True, color=YELLOW)
    wins.append(titlepanel)

    # center main menu
    menupanel_height = 25
    menupanel_width = 52
    menupanel_y = 8
    menupanel_x = width // 2 - menupanel_width // 2 - 20
    menupanel = curses.newwin(menupanel_height, menupanel_width, menupanel_y, menupanel_x)
    menupanel.bkgd(WHITE)
    menupanel_text = [
        "1 - scheduler algorithms",
        "2 - memory management",
        "3 - deadlock",
        # "4 - ",
        # "5 - ",
    ]
    for i, line in enumerate(menupanel_text):
        x = (menupanel_width-1) // 2 - len(line) // 2
        menupanel.addstr(i+1, x, line)
    draw_win(menupanel)
    wins.append(menupanel)

    # right options maybe?
    optionspanel_height = 34
    optionspanel_width = 40
    optionspanel_y = 0
    optionspanel_x = width - optionspanel_width
    optionspanel = curses.newwin(optionspanel_height, optionspanel_width, optionspanel_y, optionspanel_x)
    optionspanel.bkgd(WHITE)
    optionspanel_text = [
        # "p - pause",
        # "r - reset",
        # "? - help",
        # "q - quit"
    ]
    for i in range(len(optionspanel_text)):
        optionspanel.addstr(i+1, 2, optionspanel_text[i])
    draw_win(optionspanel)
    wins.append(optionspanel)

def refresh():
    stdscr.refresh()
    for win in wins:
        win.refresh()

def update_status_last_key(key):
    wins[STATUSPANEL_I].addstr(1, 2, f"last key: {key}")


def show_help(height, width):
    helppanel_height = 10
    helppanel_width = 20
    helppanel_y = height - 6 - helppanel_height
    helppanel_x = 0
    helppanel = curses.newwin(helppanel_height, helppanel_width, helppanel_y, helppanel_x)
    helppanel.bkgd(WHITE)
    helppanel_text = [

        "p - pause",
        "r - reset",
        "? - help", 
        "q - quit"
    ]
    for i in range(len(helppanel_text)):
        helppanel.addstr(i+1, 2, helppanel_text[i])
    draw_win(helppanel)
    helppanel.refresh()
    key = stdscr.getkey()
    helppanel.erase()
    helppanel.bkgd(' ', WHITE)
    helppanel.refresh()
    del helppanel
    return key


def main(stdscr):
    draw()
    height, width = stdscr.getmaxyx()
    x, y = 0, 0
    draw_wins(height, width)

    global running
    # Main loop
    while running:
        refresh()
        key = stdscr.getkey()
        if key == '?':
            update_status_last_key(key)
            refresh()
            key = show_help(height, width)
        elif key == 'r':
            pass
        elif key == 'q' or key == '\x1b':
            running = False
        elif key == ' ':
            refresh()
            continue
        else:
            log.error(f"Invalid key {key}")
        update_status_last_key(key)
        log.info(f"keypress: {key}")

    log.info("Quitting...")



if __name__ == "__main__":
    curses.wrapper(main)

