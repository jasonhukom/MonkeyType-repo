import sys, tty, termios, time, os

# --- setup for reading one key at a time ---
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# --- ANSI color codes ---
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# --- the text to type ---
text = "monkey type test"
typed = ""

os.system("clear")
print("Type this:\n")
print(text + "\n")

print("Start typing...")

start = None
for i in range(len(text)):
    ch = getch()
    if start is None:
        start = time.time()

    # backspace support
    if ch == "\x7f":  # delete key
        if typed:
            typed = typed[:-1]
        continue

    typed += ch

    # clear line and reprint live coloring
    sys.stdout.write("\033[2K\r")  # clear current line
    for j, c in enumerate(text):
        if j < len(typed):
            if typed[j] == c:
                sys.stdout.write(GREEN + c + RESET)
            else:
                sys.stdout.write(RED + c + RESET)
        else:
            sys.stdout.write(c)
    sys.stdout.flush()

    end = time.time()

    elapsed = end - start if start else 0
correct = sum(1 for a, b in zip(typed, text) if a == b)
accuracy = correct / len(text) * 100

wpm = 

print(f"\n\n✅ Accuracy: {accuracy:.1f}%")
print(f"⚡ Speed: {wpm:.1f} WPM")
