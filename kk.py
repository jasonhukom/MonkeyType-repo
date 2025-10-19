from rich.console import Console
from rich.text import Text
import sys, termios, tty

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

text = "hello world"

for i, c in enumerate(text):
    ch = getch()
    if ch == text:
        texts = Text(text)
        texts.stylize("green", )
console = Console()
text = Text("lol")
text.stylize("red", 0, 1) 
console.print(text)
