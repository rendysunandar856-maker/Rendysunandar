from PIL import Image, ImageOps, ImageEnhance
import os
import shutil
import urllib.request
from io import BytesIO
import sys
import socket
import platform
import subprocess
import ssl
import hashlib
import ipaddress
from urllib.parse import urlparse
import zipfile
import itertools
import string

# === AMBIL GAMBAR DARI GITHUB ===
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

RED = "\033[91m"
RESET = "\033[0m"
MERAH = RED

print()

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


# === JUDUL MENU ===
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


# === FUNGSI EKSTRAK ===
def extract_archive():
    path = input("Masukkan path file archive (.zip atau .7z): ").strip()
    out_dir = input("Folder tujuan ekstrak (kosongkan untuk folder sama): ").strip()
    
    if not out_dir:
        out_dir = os.path.dirname(path) if os.path.dirname(path) else "."
    
    if path.endswith(".zip"):
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(out_dir)
            print(MERAH + f"[+] Ekstrak ZIP berhasil ke: {out_dir}" + RESET)
        except Exception as e:
            print(f"Gagal ekstrak zip: {e}")
    
    elif path.endswith(".7z"):
        try:
            result = subprocess.run(
                ["7z", "x", f"-o{out_dir}/", path, "-y"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                print(MERAH + f"[+] Ekstrak 7Z berhasil ke: {out_dir}" + RESET)
            else:
                print(f"Gagal ekstrak 7z: {result.stderr}")
        except FileNotFoundError:
            print("Perintah '7z' tidak ditemukan. Install dulu: pkg install p7zip")
        except Exception as e:
            print(f"Gagal ekstrak 7z: {e}")
    else:
        print("Format file tidak didukung (hanya .zip dan .7z).")


# === FUNGSI CRACK PASSWORD ===
def crack_archive():
    print("\n" + MERAH + "=== CRACK PASSWORD ARCHIVE ===" + RESET)
    print("[1] Crack .ZIP (Brute-force/Dict)")
    print("[2] Crack .7Z (Menggunakan p7zip)")
    print("[0] Kembali")
    
    mode = input("Pilih mode (1/2/0): ").strip()
    
    if mode == "1":
        path = input("Masukkan path file .zip: ").strip()
        method = input("Gunakan file kata sandi (dic) atau brute-force angka? (dic/brute): ").strip().lower()
        
        if method == "dic":
            dic_path = input("Masukkan path file dictionary: ").strip()
            try:
                with open(dic_path, 'r', encoding='utf-8', errors='ignore') as f:
                    words = [line.strip() for line in f]
            except Exception as e:
                print(f"Gagal membaca dictionary: {e}")
                return

            found = False
            print("Memulai pencarian...")
            for pwd in words:
                try:
                    with zipfile.ZipFile(path, 'r') as zf:
                        zf.extractall(pwd=pwd.encode('utf-8'))
                    print(MERAH + f"\n[+] PASSWORD DITEMUKAN: {pwd}" + RESET)
                    found = True
                    break
                except (RuntimeError, Exception):
                    continue
            
            if not found:
                print("Password tidak ditemukan dalam dictionary.")

        elif method == "brute":
            print("Memulai brute-force angka 4 digit (0000-9999)...")
            chars = string.digits
            found = False
            
            for attempt in itertools.product(chars, repeat=4):
                pwd = "".join(attempt)
                try:
                    with zipfile.ZipFile(path, 'r') as zf:
                        zf.extractall(pwd=pwd.encode('utf-8'))
                    print(MERAH + f"\n[+] PASSWORD DITEMUKAN: {pwd}" + RESET)
                    found = True
                    break
                except (RuntimeError, Exception):
                    continue
            
            if not found:
                print("Password tidak ditemukan dalam range 4 digit.")

        else:
            print("Pilihan metode tidak valid.")

    elif mode == "2":
        path = input("Masukkan path file .7z: ").strip()
        dic_path = input("Masukkan path file dictionary: ").strip()
        
        try:
            with open(dic_path, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f]
            
            print("Mulai crack .7z...")
            found = False
            for pwd in words:
                cmd = ["7z", "t", f"-p{pwd}", path, "-y"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
                
                if result.returncode == 0:
                    print(MERAH + f"\n[+] PASSWORD DITEMUKAN: {pwd}" + RESET)
                    found = True
                    break
            
            if not found:
                print("Password tidak ditemukan dalam dictionary.")
                
        except FileNotFoundError:
            print("Perintah '7z' tidak ditemukan. Install dulu: pkg install p7zip")
        except Exception as e:
            print(f"Error saat crack: {e}")

    elif mode == "0":
        return
    else:
        print("Pilihan tidak valid.")


# === CYBERSECURITY TOOLS ===
def cybersecurity_tools():
    while True:
        print("\n" + MERAH + "=== CYBERSECURITY TOOLS ===" + RESET)
        print("[1] Kalkulator subnet")
        print("[2] DNS lookup")
        print("[3] Pemeriksaan header HTTP")
        print("[4] Pemeriksaan sertifikat TLS")
        print("[5] Cek satu port TCP (lab berizin)")
        print("[6] Hitung SHA-256 file")
        print("[7] Analisis log lokal")
        print("[8] Informasi lingkungan Python")
        print("[9] Ekstrak Zip/7z")
        print("[10] Crack Password Zip/7z")
        print("[0] Kembali ke
