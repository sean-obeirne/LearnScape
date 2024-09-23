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


stdscr = curses.initscr()
import colors as c

import logging

# Configure logging
logging.basicConfig(filename= f"{__file__}/../debug.log", level=logging.DEBUG, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)





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

BORDER_COLOR = c.DARK_GREY

running = True

wins = {}

actions = {}

MODES = {
    1: "mainmenu",
    2: "simulation",
    3: "paused",
}
mode = "mainmenu"

SIMULATIONS = {
    1: "scheduler",
    2: "memory management",
    3: "deadlock",
}

simulation = ""



def draw():
    # Clear screen
    stdscr.clear()

    # Turn off cursor blinking and echoing
    curses.curs_set(0)
    curses.noecho()
    curses.set_escdelay(1)

    stdscr.bkgd(' ', c.WHITE)



def draw_win(win: curses.window, borders=True, ascii=False, color=c.WHITE, border_color=BORDER_COLOR):
    height, width = win.getmaxyx()
    h = height - 1
    w = width - 2
    if borders:
        for i in range(1, w):
            win.addch(0, i, H, border_color)
            win.addch(h, i, H, border_color)
        for i in range(1, h):
            win.addch(i, 0, V, border_color)
            win.addch(i, w, V, border_color)
        win.addch(0, 0, TL, border_color)
        win.addch(h, 0, BL, border_color)
        win.addch(0, w, TR, border_color)
        win.addch(h, w, BR, border_color)
    if ascii:
        for i, line in enumerate(HEADER):
            win.addstr(i+1, 1, line, color)


def draw_wins(height, width):
    # clear first
    for win in wins:
        wins[win].erase()
        wins[win].bkgd(' ', c.WHITE)
        refresh()

    # bottom-left control panel
    name = "ctrlpanel"
    ctrlpanel_height = 6
    ctrlpanel_width = 15
    ctrlpanel_y = height - ctrlpanel_height
    ctrlpanel_x = 0
    ctrlpanel = curses.newwin(ctrlpanel_height, ctrlpanel_width, ctrlpanel_y, ctrlpanel_x)
    ctrlpanel.bkgd(c.WHITE)
    ctrlpanel_text = [
        "p - pause",
        "r - reset",
        "? - help",
        "q - quit"
    ]
    for i in range(len(ctrlpanel_text)):
        ctrlpanel.addstr(i+1, 2, ctrlpanel_text[i])
    draw_win(ctrlpanel)
    wins[name] = ctrlpanel

    # bottom status bar
    name = "statuspanel"
    statuspanel_height = 4
    statuspanel_width = width - ctrlpanel_width - 2
    statuspanel_y = height - statuspanel_height
    statuspanel_x = ctrlpanel_width + 1
    statuspanel = curses.newwin(statuspanel_height, statuspanel_width, statuspanel_y, statuspanel_x)
    statuspanel.bkgd(c.WHITE)
    statuspanel_text = [
    ]
    statuspanel.addstr(2, 2, f"mode: {mode}")
    for i, line in enumerate(statuspanel_text):
        x = (statuspanel_width-1) // 2 - len(line) // 2
        statuspanel.addstr(i+1, x, line)
    draw_win(statuspanel)
    wins[name] = statuspanel

    # right options
    name = "optionspanel"
    optionspanel_height = 34
    optionspanel_width = 30
    optionspanel_y = 0
    optionspanel_x = width - optionspanel_width
    optionspanel = curses.newwin(optionspanel_height, optionspanel_width, optionspanel_y, optionspanel_x)
    optionspanel.bkgd(c.WHITE)
    optionspanel_text = [
        # "p - pause",
        # "r - reset",
        # "? - help",
        # "q - quit"
    ]
    optionspanel.addstr(1, 2, f"Options:", c.YELLOW)
    for i in range(len(optionspanel_text)):
        optionspanel.addstr(i+1, 2, optionspanel_text[i])
    draw_win(optionspanel, border_color=c.DIM_WHITE)
    wins[name] = optionspanel

    # main centered panel for simulation
    name = "mainpanel"
    mainpanel_height = height - statuspanel_height - 4
    mainpanel_width = statuspanel_width - optionspanel_width - 1
    mainpanel_y = 4
    mainpanel_x = ctrlpanel_width + 1
    mainpanel = curses.newwin(mainpanel_height, mainpanel_width, mainpanel_y, mainpanel_x)
    mainpanel.bkgd(c.WHITE)
    mainpanel_text = [
    ]
    for i, line in enumerate(mainpanel_text):
        x = (mainpanel_width-1) // 2 - len(line) // 2
        mainpanel.addstr(i+1, x, line)
    draw_win(mainpanel, border_color=c.DIM_WHITE)
    wins[name] = mainpanel

    # top left title
    if mode == "mainmenu":
        name = "titlepanel"
        titlepanel_height = 7
        titlepanel_width = 71
        titlepanel_y = 0
        titlepanel_x = 0
        titlepanel = curses.newwin(titlepanel_height, titlepanel_width, titlepanel_y, titlepanel_x)
        titlepanel.bkgd(c.WHITE)
        draw_win(titlepanel, ascii=True, color=c.LIGHT_RED, border_color=c.PURPLE)
        wins[name] = titlepanel

    # center main menu
    if mode == "mainmenu":
        name = "menupanel"
        menupanel_height = 25
        menupanel_width = 52
        menupanel_y = 8
        menupanel_x = width // 2 - menupanel_width // 2 + statuspanel_x // 2
        menupanel = curses.newwin(menupanel_height, menupanel_width, menupanel_y, menupanel_x)
        menupanel.bkgd(c.WHITE)
        menupanel_text = [
            "",
            "Welcome!",
            "Which concept would you like to visualize?",
            "",
            "1 - scheduler algorithms",
            "2 - memory management",
            "3 - deadlock",
            # "4 - ",
            # "5 - ",
        ]
        for i, line in enumerate(menupanel_text):
            x = (menupanel_width-1) // 2 - len(line) // 2
            if len(line) > 0 and line[0].isdigit():
                menupanel.addstr(i+1, x, line.split(" ")[0], c.LIGHT_GREEN)
                x += 1
                menupanel.addstr(i+1, x, line[1:], c.YELLOW if i < 3 else c.WHITE)
            else:
                menupanel.addstr(i+1, x, line, c.YELLOW if i < 3 else c.WHITE)
        draw_win(menupanel, border_color=c.PURPLE)
        wins[name] = menupanel


def refresh():
    stdscr.refresh()
    for win in wins:
        wins[win].refresh()

def update_status_last_key(key):
    wins["statuspanel"].addstr(1, 2, f"last key: {key}")


def show_help(height, width):
    helppanel_height = 10
    helppanel_width = 20
    helppanel_y = height - 6 - helppanel_height
    helppanel_x = 0
    helppanel = curses.newwin(helppanel_height, helppanel_width, helppanel_y, helppanel_x)
    helppanel.bkgd(c.WHITE)
    helppanel_text = [
        "p - pause",
        "r - reset",
        "? - help", 
        "q - quit"
    ]
    for i in range(len(helppanel_text)):
        helppanel.addstr(i+1, 2, helppanel_text[i])
    draw_win(helppanel, border_color=c.LIGHT_RED)
    helppanel.refresh()
    key = stdscr.getkey()
    helppanel.erase()
    helppanel.bkgd(' ', c.WHITE)
    helppanel.refresh()
    del helppanel
    draw_wins(height, width)
    return key


def main(stdscr):
    draw()
    height, width = stdscr.getmaxyx()
    x, y = 0, 0
    global mode
    mode = MODES[1]

    draw_wins(height, width)


    global running
    # Main loop
    while running:
        refresh()
        key: str = stdscr.getkey()
        if key.isdigit():
            mode = MODES[2]
            simulation = SIMULATIONS[int(key)]
            draw_wins(height, width)
        elif key == '?':
            update_status_last_key(key)
            refresh()
            key = show_help(height, width)
        elif key == 'r':
            pass
        elif key == 'q' or key == '\x1b':
            if mode == MODES[2]:
                mode = MODES[1]
                draw_wins(height, width)
            else:
                running = False
        elif key == ' ':
            refresh()
            continue
        else:
            log.error(f"Invalid key {key}")
        update_status_last_key(key)
        log.info(f"keypress: {key}, in mode: {mode}")

    log.info("Quitting...")



if __name__ == "__main__":
    curses.wrapper(main)

