from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

import curses
import curses.textpad
import keyboard

screen = curses.initscr()
curses.echo()

while True:
    if(keyboard.is_pressed("ctrl+e")):
        break
    
    screen.clear()
    insert = curses.textpad.Textbox(screen, insert_mode=True)
    text = insert.edit()
    screen.refresh()

curses.endwin