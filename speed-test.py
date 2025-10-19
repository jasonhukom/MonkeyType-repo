from rich.console import Console
from rich.text import Text
from rich.live import Live
import sys, os, time, termios, tty, getpass, random

os_name = os.name
console = Console()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def clear():
    os.system("clear")

def main():
    clear()
    text_list = materials()
    fix_text = randomize_text(text_list)
    users_typed = ""
    print(fix_text)
    wait_seconds("Starting", 3)
    clear()
    start = time.time()
    print(fix_text)
    
    for index, character in enumerate(fix_text):
        try:    
            characters_input_by_user = getch()

            if characters_input_by_user == "\x7f" or characters_input_by_user == "\x08":
                if users_typed:
                    users_typed = users_typed[0:-1]
                    clear()
                    text = colour_change(fix_text, None, len(users_typed) - 1)
                console.print(text)
                continue

            users_typed += characters_input_by_user
            
            clear()

            text = fix_text
            print(users_typed)
            if users_typed[index] == character:
                text = colour_change(fix_text, "green", len(users_typed))
            else:
                text = colour_change(fix_text, "red", len(users_typed))    
            console.print(f"{text}")
            
        except EOFError:
            break
        except IndexError:
            pass
            
    sys.stdout.flush()
    clear()
    wait_seconds("Loading results", 1)
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
        

def colour_change(text, colour, length):
    text_in_rich = Text(text)
    text_in_rich.stylize(colour, 0, length)
    return text_in_rich

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
        "Algoritma adalah langkah-langkah logis untuk menyelesaikan suatu masalah dalam pemrograman. Flowchart digunakan untuk menggambarkan alur logika dari algoritma agar lebih mudah dipahami. Variabel berfungsi menyimpan data seperti angka atau teks yang akan digunakan dalam program. Bahasa pemrograman seperti Python membantu siswa memahami konsep perulangan, percabangan, dan fungsi. Pemahaman tentang etika digital dan keamanan data sangat penting di era teknologi saat ini.",
        "Bilangan real terdiri atas bilangan rasional dan irasional yang digunakan dalam berbagai operasi hitung. Himpunan menjadi dasar dalam memahami relasi dan fungsi yang menghubungkan satu nilai dengan nilai lainnya. Logaritma merupakan kebalikan dari eksponen yang digunakan untuk menyelesaikan persoalan pertumbuhan atau peluruhan. Persamaan linear dua variabel sering digunakan untuk menyelesaikan masalah sehari-hari seperti perbandingan harga atau kecepatan. Konsep gradien membantu kita memahami kemiringan suatu garis pada grafik.",
        "Teks laporan hasil observasi adalah teks yang menyampaikan informasi faktual berdasarkan hasil pengamatan suatu objek. Struktur teks ini terdiri atas pernyataan umum, deskripsi bagian, dan deskripsi manfaat. Teks anekdot digunakan untuk menyampaikan kritik sosial dengan cara yang lucu dan menghibur. Prosa merupakan karya sastra berbentuk naratif yang menggambarkan tokoh, latar, serta alur cerita secara bebas. Kalimat efektif dan penggunaan ejaan yang tepat menjadi kunci agar informasi tersampaikan dengan baik.",
        "Atom merupakan partikel paling kecil yang menyusun zat, sedangkan molekul adalah gabungan dari dua atau lebih atom. Energi dapat berubah bentuk dari energi potensial menjadi energi kinetik ketika benda bergerak. Ekosistem terdiri dari komponen biotik dan abiotik yang saling berinteraksi untuk menjaga keseimbangan alam. Fotosintesis merupakan proses tumbuhan hijau mengubah cahaya matahari menjadi energi kimia. Pengukuran besaran seperti massa, waktu, dan suhu penting untuk memahami fenomena ilmiah.",
        "Simple Present Tense digunakan untuk menyatakan kebiasaan atau fakta umum, contohnya She studies every day. Simple Past Tense digunakan untuk menceritakan kejadian yang sudah terjadi, seperti They played football yesterday. Recount text adalah teks yang menceritakan kembali pengalaman masa lalu dengan urutan peristiwa yang jelas. Vocabulary atau kosakata menjadi dasar penting dalam berbicara dan menulis dalam bahasa Inggris. Pronunciation atau pelafalan perlu diperhatikan agar komunikasi lebih jelas, dan kemampuan reading, listening, speaking, serta writing harus dilatih secara seimbang."
    ]

if __name__ == "__main__":
    if os_name == 'nt':
        result = input("This program might not work with your OS. Are you sure to continue?").lower()
        match result:
            case 'y':
                main()
            case 'n':
                sys.exit()
    elif os_name == 'posix':
        main()