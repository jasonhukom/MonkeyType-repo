# Speed Test (Monkeytype-style typing test for the terminal)

A small terminal typing test built with Python and [rich](https://github.com/Textualize/rich).
It clears your screen, shows a passage (in Bahasa Indonesia / English school topics), and colors
it as you type. When you finish, it shows your **accuracy** and **speed (WPM)**.

## How it works

| What you see | Meaning |
|---|---|
| Gray text | Not typed yet |
| Green letter | Correct letter |
| Red letter | Wrong letter (it replaces the original letter; a wrong space shows as `_`) |

- **Backspace** goes back one character and turns it gray again.
- Arrow keys and other special keys are ignored.
- The test **ends automatically** when you type the last character.
- Press **Enter** or **Ctrl+C** to stop early.

## Project layout

```
speed-test/
├── linux/       speed-test.py + run.sh    (Linux / macOS)
├── windows/     speed-test.py + run.ps1   (Windows / PowerShell)
├── requirements.txt
├── .gitignore
└── README.md
```

Requires **Python 3.9 or newer**.

## Linux / macOS

Quick start (creates a virtual environment and installs `rich` for you):

```bash
cd linux
./run.sh
```

Manual setup:

```bash
cd linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
python speed-test.py
```

## Windows (PowerShell)

Quick start:

```powershell
cd windows
.\run.ps1
```

If PowerShell says scripts are disabled, run it like this instead:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

Manual setup:

```powershell
cd windows
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
python speed-test.py
```

For the best colors, use Windows Terminal (it works in the classic PowerShell window too).

## How the score is calculated

- **Accuracy** = correctly typed characters / total characters x 100
- **Speed** = (accuracy / average word length) / minutes taken

The timer starts when the passage appears and includes the 1-second "Loading results" screen.

## Editing the passages

Add or change passages in the `materials()` function at the bottom of `speed-test.py`.
Use normal keyboard characters only (avoid copy-pasted non-breaking spaces, which cannot be typed).

## Publishing to GitHub

The included `.gitignore` keeps your virtual environment (`.venv/`), Python caches and editor files out of the repo.

```bash
git init
git add .
git commit -m "Add typing speed test"
```
