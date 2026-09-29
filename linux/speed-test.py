from rich.console import Console
from rich.text import Text
import sys, os, time, random, select

if os.name == "nt":
    print("This is the Linux/macOS version. Windows users: use the 'windows' folder instead.")
    sys.exit(1)

import termios, tty

console = Console()

UNTYPED_STYLE = "grey50"
BACKSPACE_KEYS = ("\x7f", "\x08")


def getch():
    """Read one key press. Returns None on EOF, '' for keys to ignore (arrows etc.).
    The terminal must already be in cbreak mode (see main)."""
    fd = sys.stdin.fileno()
    data = os.read(fd, 1)
    if data == b"\x1b":
        # Escape sequence (arrow keys, Home, End...): swallow the rest of it
        while select.select([fd], [], [], 0.02)[0]:
            os.read(fd, 32)
        return ""
    if data == b"":
        return None
    try:
        return data.decode()
    except UnicodeDecodeError:
        return ""


def clear():
    console.clear()


def main():
    clear()
    text_list = materials()
    fix_text = randomize_text(text_list)
    users_typed = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)  # no echo, key-by-key input, and no lost keys while redrawing
    start = time.time()
    texts = Text(fix_text, style=UNTYPED_STYLE)
    list_of_character = [Text()]
    while True:
        try:
            clear()

            console.print(Text.assemble(*list_of_character) + texts[len(users_typed):])

            character = getch()

            # EOF, Ctrl+C, Ctrl+D or Enter -> finish
            if character is None or character in ("\x03", "\x04", "\r", "\n"):
                break

            # Backspace: go back one character, it turns gray again
            if character in BACKSPACE_KEYS:
                if users_typed:
                    users_typed = users_typed[:-1]
                    list_of_character.pop()
                continue

            # Ignore other control keys / unknown keys
            if not character or not character.isprintable():
                continue

            users_typed += character
            expected_char = fix_text[len(users_typed) - 1]
            if character == expected_char:
                list_of_character.append(Text(character, style="green"))
            else:
                # a wrong space would be invisible, so show an underscore instead
                shown = "_" if character == " " else character
                list_of_character.append(Text(shown, style="red"))

            # typed the whole text -> finish
            if len(users_typed) >= len(fix_text):
                break

        except (EOFError, KeyboardInterrupt):
            break

    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    sys.stdout.flush()
    clear()
    wait_seconds("Loading results ", 1)
    end = time.time()
    len_time = check_len_of_time(start, end)
    correct = check_correction(users_typed, fix_text)
    accuracy = (correct / len(fix_text)) * 100
    average = word_len_finder(fix_text)
    # total words / number of minutes
    wpm = (accuracy / average) / (len_time / 60)
    print(f"\n\nAccuracy: {accuracy:.1f}%")
    print(f"Speed: {wpm:.1f} WPM")


def wait_seconds(prompt_i_seconds, num):
    for i in range(num):
        print(f"\r{prompt_i_seconds}in {i} seconds...")
        time.sleep(1)
        clear()

def randomize_text(your_list):
    return random.choice(your_list)

def check_len_of_time(start_time, end_time):
    return end_time - start_time if start_time else 0

def check_correction(word1, word2):
    return sum(1 for a, b in zip(word1, word2) if a == b)

def word_len_finder(sentence):
    words = sentence.split()
    lenlist = []
    for word in words:
        lenlist.append(len(word))
    return sum(lenlist) / len(lenlist) 

def materials():
    return [
        "Algoritma adalah langkah-langkah logis untuk menyelesaikan suatu masalah dalam pemrograman. Flowchart digunakan untuk menggambarkan alur logika dari algoritma agar lebih mudah dipahami. Variabel berfungsi menyimpan data seperti angka atau teks yang akan digunakan dalam program. Bahasa pemrograman seperti Python membantu siswa memahami konsep perulangan, percabangan, dan fungsi. Pemahaman tentang etika digital dan keamanan data sangat penting di era teknologi saat ini.",
        "Bilangan real terdiri atas bilangan rasional dan irasional yang digunakan dalam berbagai operasi hitung. Himpunan menjadi dasar dalam memahami relasi dan fungsi yang menghubungkan satu nilai dengan nilai lainnya. Logaritma merupakan kebalikan dari eksponen yang digunakan untuk menyelesaikan persoalan pertumbuhan atau peluruhan. Persamaan linear dua variabel sering digunakan untuk menyelesaikan masalah sehari-hari seperti perbandingan harga atau kecepatan. Konsep gradien membantu kita memahami kemiringan suatu garis pada grafik.",
        "Teks laporan hasil observasi adalah teks yang menyampaikan informasi faktual berdasarkan hasil pengamatan suatu objek. Struktur teks ini terdiri atas pernyataan umum, deskripsi bagian, dan deskripsi manfaat. Teks anekdot digunakan untuk menyampaikan kritik sosial dengan cara yang lucu dan menghibur. Prosa merupakan karya sastra berbentuk naratif yang menggambarkan tokoh, latar, serta alur cerita secara bebas. Kalimat efektif dan penggunaan ejaan yang tepat menjadi kunci agar informasi tersampaikan dengan baik.",
        "Atom merupakan partikel paling kecil yang menyusun zat, sedangkan molekul adalah gabungan dari dua atau lebih atom. Energi dapat berubah bentuk dari energi potensial menjadi energi kinetik ketika benda bergerak. Ekosistem terdiri dari komponen biotik dan abiotik yang saling berinteraksi untuk menjaga keseimbangan alam. Fotosintesis merupakan proses tumbuhan hijau mengubah cahaya matahari menjadi energi kimia. Pengukuran besaran seperti massa, waktu, dan suhu penting untuk memahami fenomena ilmiah.",
        "Simple Present Tense digunakan untuk menyatakan kebiasaan atau fakta umum, contohnya She studies every day. Simple Past Tense digunakan untuk menceritakan kejadian yang sudah terjadi, seperti They played football yesterday. Recount text adalah teks yang menceritakan kembali pengalaman masa lalu dengan urutan peristiwa yang jelas. Vocabulary atau kosakata menjadi dasar penting dalam berbicara dan menulis dalam bahasa Inggris. Pronunciation atau pelafalan perlu diperhatikan agar komunikasi lebih jelas, dan kemampuan reading, listening, speaking, serta writing harus dilatih secara seimbang."
    ]

if __name__ == "__main__":
    main()
