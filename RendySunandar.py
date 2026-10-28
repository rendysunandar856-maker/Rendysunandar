from PIL import Image, ImageOps, ImageEnhance
import os
import shutil
import urllib.request
from io import BytesIO
import sys
import socket
import platform
import subprocess
import threading
import queue
import time
from urllib.parse import urlparse

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
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"

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
print(RED + "  │  SKILL   : NETWORKING/HACKING │" + RESET)
print(RED + "  └──────────────────────────────┐" + RESET)
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
            line.append(f"\033[38;2;{r};{g};{b}m{chars[index]}\033[0m")
    print("".join(line))

# === MENU INTERAKTIF RENDY SUNANDAR ===
MERAH = "\033[91m"

def judul():
    merah = "\033[91m"
    oranye = "\033[38;5;208m"
    reset = "\033[0m"

    try:
        r = subprocess.run(["figlet", "-f", "big", "RENDY"], capture_output=True, text=True, timeout=3)
        atas = r.stdout.rstrip() if r.returncode == 0 else "RENDY"
    except:
        atas = "RENDY"

    try:
        r = subprocess.run(["figlet", "-f", "big", "SUNANDAR"], capture_output=True, text=True, timeout=3)
        bawah = r.stdout.rstrip() if r.returncode == 0 else "SUNANDAR"
    except:
        bawah = "SUNANDAR"

    print()
    print(oranye + atas + reset)
    print(merah + bawah + reset)
    print(oranye + "================================" + reset)
    print(merah + "           MENU UTAMA" + reset)
    print(oranye + "================================" + reset)

# === FUNGSI TOOLS HACK WEBSITE ===
def port_scanner():
    print(MERAH + "\n--- PORT SCANNER ---\n")
    target = input("Masukkan IP/Hostname Target: ").strip()
    if not target:
        print("Target kosong!")
        return

    print(f"{YELLOW}Memindai port pada {target}...{RESET}")
    open_ports = []
    
    # Memindai port umum (1-1024)
    for port in range(1, 1025):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"{GREEN}[+] Port {port} Terbuka{RESET}")
                open_ports.append(port)
            sock.close()
        except socket.error:
            pass
            
    if not open_ports:
        print(f"{RED}[-] Tidak ada port terbuka pada rentang 1-1024.{RESET}")

def check_headers():
    print(MERAH + "\n--- HTTP HEADER SECURITY CHECK ---\n")
    url = input("Masukkan URL (contoh: https://example.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "RenSigma/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            headers = dict(response.getheaders())
            print(f"\n{GREEN}[+] Header Response dari {url}:{RESET}")
            for key, value in headers.items():
                print(f"{CYAN}{key}:{RESET} {value}")
            
            # Cek keamanan dasar
            security_headers = {
                "Strict-Transport-Security": "HSTS",
                "X-Frame-Options": "Clickjacking Protection",
                "X-Content-Type-Options": "MIME Sniffing Protection",
                "Content-Security-Policy": "CSP"
            }
            
            print(f"\n{YELLOW}[!] Analisis Keamanan:{RESET}")
            found = 0
            for header, desc in security_headers.items():
                if header in headers:
                    print(f"{GREEN}✓ {desc} ({header}) Ditemukan{RESET}")
                    found += 1
                else:
                    print(f"{RED}✗ {desc} ({header}) Hilang{RESET}")
            
            if found == 0:
                print("\n{RED}Peringatan: Website memiliki keamanan header yang sangat lemah.{RESET}")
                
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")

def simple_bruteforce():
    print(MERAH + "\n--- SIMPLE LOGIN BRUTE FORCE (DEMO) ---\n")
    print("Peringatan: Gunakan pada target yang memiliki izin!")
    url = input("Masukkan URL Login (POST): ").strip()
    if not url.startswith("http"):
        url = "https://" + url
    
    username_field = input("Nama field username (default: username): ").strip() or "username"
    password_field = input("Nama field password (default: password): ").strip() or "password"
    
    # Daftar kata sandi sederhana untuk demo
    passwords = ["admin", "123456", "password", "root", "test", "admin123"]
    
    print(f"\n{CYAN}Memulai brute-force pada {url}...{RESET}")
    print(f"User field: {username_field} | Pass field: {password_field}\n")
    
    for pwd in passwords:
        try:
            data = {username_field: "admin", password_field: pwd}
            encoded_data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request(url, data=encoded_data, method="POST")
            req.add_header("User-Agent", "RenSigma/1.0")
            
            with urllib.request.urlopen(req, timeout=5) as response:
                # Logika sederhana: jika status 302 (redirect) atau response kecil, dianggap sukses
                if response.status == 302 or len(response.read()) < 100:
                    print(f"{GREEN}[+] Kemungkinan Sukses! Password: {pwd}{RESET}")
                    return
        except Exception:
            pass
        print(f"\r{YELLOW}Mencoba: {pwd}...", end="")
    
    print(f"\n{RED}Brute-force selesai. Tidak menemukan password dalam daftar.{RESET}")

def dir_finder():
    print(MERAH + "\n--- DIRECTORY FINDER ---\n")
    url = input("Masukkan URL (contoh: https://target.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url
    
    # Daftar direktori umum
    dirs = ["/admin", "/login", "/wp-admin", "/phpmyadmin", "/config", "/backup", "/.git", "/.env"]
    
    print(f"{CYAN}Mencari direktori pada {url}...{RESET}")
    for d in dirs:
        try:
            target_url = url.rstrip("/") + d
            req = urllib.request.Request(target_url, method="HEAD")
            req.add_header("User-Agent", "RenSigma/1.0")
