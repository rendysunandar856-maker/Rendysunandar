
from PIL import Image, ImageOps, ImageEnhance
import os
import shutil
import urllib.request
from io import BytesIO
import sys
import socket
import platform
import subprocess

# === AMBIL GAMBAR LANGSUNG DARI GITHUB ===
IMAGE_URL = "https://raw.githubusercontent.com/rendysunandar856-maker/Rendysunandar/main/anime_baru.jpg"
chars = "@%#*+=-:. "

try:
    with urllib.request.urlopen(IMAGE_URL, timeout=15) as response:
        image_data = response.read()

    with Image.open(BytesIO(image_data)) as source:
        img = ImageOps.exif_transpose(source).convert("RGB")
except Exception as e:
    print("Gagal mengambil gambar dari GitHub:", e)
    sys.exit(1)

# === UKURAN GAMBAR ===
cols = shutil.get_terminal_size((80, 24)).columns
width = min(max(cols - 2, 60), 100)
height = max(1, int(img.height / img.width * width * 0.48))

img = img.resize((width, height), Image.Resampling.LANCZOS)
img = ImageEnhance.Contrast(img).enhance(1.4)
img = ImageEnhance.Color(img).enhance(1.2)

gray = ImageOps.autocontrast(ImageOps.grayscale(img), cutoff=1)
rgb = list(img.getdata())
levels = list(gray.getdata())

C = "\033[96m"
B = "\033[1;96m"
D = "\033[34m"
R = "\033[0m"

print()

RED = "\033[91m"
RESET = "\033[0m"

# === BANNER ===
try:
    result = subprocess.run(
        ["figlet", "-f", "slant", "Rendy Sunandar"],
        capture_output=True, text=True, timeout=3
    )
    banner = result.stdout.rstrip() if result.returncode == 0 else "Rendy Sunandar"
except (FileNotFoundError, subprocess.SubprocessError):
    banner = "Rendy Sunandar"

print(RED + banner + RESET)
print(RED + "       KELAS 11 TKJ" + RESET)
print(RED + "  ┌──────────────────────────────┐" + RESET)
print(RED + "  │  SYSTEM  : TERMUX ANDROID     │" + RESET)
print(RED + "  │  STATUS  : ONLINE             │" + RESET)
print(RED + "  │  NETWORK : READY              │" + RESET)
print(RED + "  │  SKILL   : NETWORKING         │" + RESET)
print(RED + "  └──────────────────────────────┘" + RESET)
print()

# === CETAK GAMBAR ASCII BERWARNA ===
for y in range(height):
    line = []
    for x in range(width):
        i = y * width + x
        r, g, b = rgb[i]
        v = levels[i]
        index = min(v * len(chars) // 256, len(chars) - 1)

        if v > 242:
            line.append(" ")
        else:
            line.append(
                f"\033[38;2;{r};{g};{b}m{chars[index]}\033[0m"
            )

    print("".join(line))

# === MENU INTERAKTIF RENDY SUNANDAR ===
MERAH = "\033[91m"
RESET = "\033[0m"

def judul():
    merah = "\033[91m"
    oranye = "\033[38;5;208m"
    reset = "\033[0m"

    try:
        r = subprocess.run(
            ["figlet", "-f", "big", "RENDY"],
            capture_output=True, text=True, timeout=3
        )
        atas = r.stdout.rstrip() if r.returncode == 0 else "RENDY"
    except (FileNotFoundError, subprocess.SubprocessError):
        atas = "RENDY"

    try:
        r = subprocess.run(
            ["figlet", "-f", "big", "SUNANDAR"],
            capture_output=True, text=True, timeout=3
        )
        bawah = r.stdout.rstrip() if r.returncode == 0 else "SUNANDAR"
    except (FileNotFoundError, subprocess.SubprocessError):
        bawah = "SUNANDAR"

    print()
    print(oranye + atas + reset)
    print(merah + bawah + reset)
    print(oranye + "================================" + reset)
    print(merah + "           MENU UTAMA" + reset)
    print(oranye + "================================" + reset)

def menu():
    while True:
        judul()
        print("\033[38;5;208m[1] INFORMASI SISTEM ANDROID/TERMUX\033[0m")
        print("\033[91m[2] CEK KONEKSI INTERNET\033[0m")
        print("\033[38;5;208m[3] INFORMASI JARINGAN DAN IP\033[0m")
        print("\033[91m[4] TOOLS PYTHON\033[0m")
        print("\033[38;5;208m[5] PROFIL RENDY SUNANDAR\033[0m")
        print("\033[91m[0] KELUAR DARI MENU\033[0m")
        print("================================" + RESET)

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            print(MERAH + "\n--- INFORMASI SISTEM ---")
            print("Sistem :", platform.system())
            print("Versi  :", platform.release())
            print("Python :", platform.python_version())
            print("Mesin  :", platform.machine())
            print("Termux :", os.environ.get("PREFIX", "Tidak terdeteksi"))
            print(RESET)

        elif pilihan == "2":
            print(MERAH + "\nMemeriksa koneksi internet...")
            try:
                req = urllib.request.Request(
                    "https://www.google.com",
                    method="HEAD",
                    headers={"User-Agent": "TermuxMenu/1.0"}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    print("Internet: TERHUBUNG")
                    print("HTTP status:", response.status)
            except Exception:
                print("Internet tidak terjangkau atau pemeriksaan gagal.")
                print("Periksa Wi-Fi/data seluler kamu.")
            print(RESET)

        elif pilihan == "3":
            print(MERAH + "\n--- INFORMASI JARINGAN ---")
            try:
                host = socket.gethostname()
                ip = socket.gethostbyname(host)
                print("Hostname :", host)
                print("IP lokal :", ip)
                print("Catatan  : IP bisa berupa alamat loopback.")
            except OSError as e:
                print("Tidak dapat membaca informasi jaringan:", e)
            print(RESET)

        elif pilihan == "4":
            print(MERAH + "\n--- TOOLS PYTHON ---")
            print("1. Versi Python")
            print("2. Versi pip")
            sub = input("Pilih tools (1/2): ").strip()

            if sub == "1":
                print(sys.version)
            elif sub == "2":
                subprocess.run(
                    [sys.executable, "-m", "pip", "--version"]
                )
            else:
                print("Pilihan tidak tersedia.")
            print(RESET)

        elif pilihan == "5":
            print(MERAH + "\n--- PROFIL ---")
            print("Nama     : Rendy Sunandar")
            print("Lingkup  : Android dan Termux")
            print("Minat    : Python dan networking")
            print(RESET)

        elif pilihan == "0":
            print(MERAH + "Keluar dari menu. Sampai jumpa!" + RESET)
            break

        else:
            print(MERAH + "Pilihan tidak tersedia." + RESET)

        input("\nTekan Enter untuk kembali ke menu...")

try:
    menu()
except (KeyboardInterrupt, EOFError):
    print("\nMenu ditutup.")
    

