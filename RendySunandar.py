
from PIL import Image, ImageOps, ImageEnhance
import shutil
import urllib.request
import urllib.error
from io import BytesIO
import sys
import socket
import subprocess
from urllib.parse import urlparse

# === KONFIGURASI ===
IMAGE_URL = (
    "https://raw.githubusercontent.com/"
    "rendysunandar856-maker/Rendysunandar/main/anime_baru.jpg"
)
CHARS = "@%#*+=-:. "

RED = "\033[91m"
RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MERAH = RED


# === BANNER GAMBAR ===
def tampilkan_gambar():
    try:
        with urllib.request.urlopen(IMAGE_URL, timeout=15) as response:
            image_data = response.read()

        with Image.open(BytesIO(image_data)) as source:
            img = ImageOps.exif_transpose(source).convert("RGB")

        cols = shutil.get_terminal_size((80, 24)).columns
        width = min(max(cols - 2, 60), 100)
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
                v = levels[i]
                index = min(
                    v * len(CHARS) // 256,
                    len(CHARS) - 1
                )

                if v > 242:
                    line.append(" ")
                else:
                    line.append(
                        f"\033[38;2;{r};{g};{b}m"
                        f"{CHARS[index]}\033[0m"
                    )
            print("".join(line))

    except Exception as e:
        print(f"{YELLOW}Gambar tidak bisa dimuat: {e}{RESET}")


# === JUDUL ===
def judul():
    print()
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

    print(f"\033[38;5;208m{atas}{RESET}")
    print(f"{RED}{bawah}{RESET}")
    print(f"{CYAN}{'=' * 32}{RESET}")
    print(f"{RED}          MENU UTAMA{RESET}")
    print(f"{CYAN}{'=' * 32}{RESET}")


# === VALIDASI URL ===
def minta_url(prompt):
    url = input(prompt).strip()
    if not url:
        print(f"{RED}URL tidak boleh kosong.{RESET}")
        return None

    if not url.startswith(("https://", "http://")):
        url = "https://" + url

    parsed = urlparse(url)
    if not parsed.hostname:
        print(f"{RED}Format URL tidak valid.{RESET}")
        return None

    return url


# === PORT SCANNER ===
def port_scanner():
    print(f"{RED}\n--- PORT SCANNER ---{RESET}")
    target = input("IP/hostname perangkat milikmu: ").strip()

    if not target:
        print("Target kosong!")
        return

    try:
        socket.getaddrinfo(target, None)
    except socket.gaierror:
        print(f"{RED}Hostname tidak ditemukan.{RESET}")
        return

    print(f"{CYAN}Memeriksa port umum pada {target}...{RESET}")
    ports = [21, 22, 25, 53, 80, 110, 143, 443, 445, 3306, 8080]

    for port in ports:
        try:
            with socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            ) as sock:
                sock.settimeout(0.7)
                if sock.connect_ex((target, port)) == 0:
                    print(f"{GREEN}[TERBUKA] Port {port}{RESET}")
        except (socket.error, OSError):
            continue

    print(f"{YELLOW}Pemeriksaan selesai.{RESET}")


# === HTTP SECURITY HEADERS ===
def check_headers():
    print(f"{RED}\n--- HTTP HEADER SECURITY CHECK ---{RESET}")
    url = minta_url("URL website milikmu/lab berizin: ")
    if not url:
        return

    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "RenSigma/1.0"}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            headers = response.headers

            print(f"\n{GREEN}Status HTTP: {response.status}{RESET}")
            for key, value in headers.items():
                print(f"{CYAN}{key}:{RESET} {value}")

            checks = {
                "Strict-Transport-Security": "HSTS",
                "X-Frame-Options": "Perlindungan framing",
                "X-Content-Type-Options": "Perlindungan MIME",
                "Content-Security-Policy": "CSP",
            }

            print(f"\n{YELLOW}Analisis header:{RESET}")
            for header, desc in checks.items():
                if header in headers:
                    print(f"{GREEN}[ADA] {desc}{RESET}")
                else:
                    print(f"{RED}[BELUM ADA] {desc}{RESET}")

    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"{RED}Gagal memeriksa URL: {e}{RESET}")


# === DIRECTORY FINDER ===
def dir_finder():
    print(f"{RED}\n--- DIRECTORY FINDER ---{RESET}")
    url = minta_url("URL website milikmu/lab berizin: ")
    if not url:
        return

    dirs = [
        "/",
        "/robots.txt",
        "/sitemap.xml",
        "/login",
        "/admin",
    ]

    print(f"{CYAN}Memeriksa path publik pada {url}...{RESET}")

    for path in dirs:
        target_url = url.rstrip("/") + path
        req = urllib.request.Request(
            target_url,
            method="HEAD",
            headers={"User-Agent": "RenSigma/1.0"},
        )

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                print(
                    f"{GREEN}[{response.status}] "
                    f"{target_url}{RESET}"
                )
        except urllib.error.HTTPError as e:
            print(f"{YELLOW}[{e.code}] {target_url}{RESET}")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            print(f"{RED}Gagal: {target_url} — {e}{RESET}")

    print(f"{YELLOW}Pemeriksaan selesai.{RESET}")


# === DEMO LOGIN LOKAL ===
def login_demo():
    print(f"{RED}\n--- LOGIN SECURITY DEMO ---{RESET}")
    print("Demo lokal: tidak mengirim permintaan ke website.")
    print("Tujuan: memahami pentingnya password yang kuat.")

    password = input("Masukkan password contoh: ")
    if len(password) >= 12:
        print(f"{GREEN}Panjang password cukup baik.{RESET}")
    else:
        print(
            f"{YELLOW}Gunakan password lebih panjang "
            f"dan unik.{RESET}"
        )


# === MENU UTAMA ===
def menu():
    while True:
        judul()
        print("1. Port Scanner")
        print("2. HTTP Security Headers")
        print("3. Directory Finder")
        print("4. Login Security Demo")
        print("0. Keluar")

        pilihan = input(f"\n{CYAN}Pilih menu: {RESET}").strip()

        if pilihan == "1":
            port_scanner()
        elif pilihan == "2":
            check_headers()
        elif pilihan == "3":
            dir_finder()
        elif pilihan == "4":
            login_demo()
        elif pilihan == "0":
            print(f"{GREEN}Terima kasih sudah menggunakan RenSigma.{RESET}")
            break
        else:
            print(f"{RED}Pilihan tidak valid.{RESET}")

        input("\nTekan Enter untuk kembali ke menu...")


# === JALANKAN PROGRAM ===
if __name__ == "__main__":
    print(f"{RED}Rendy Sunandar | Kelas 11 TKJ{RESET}")
    print("SYSTEM: TERMUX ANDROID")
    print("STATUS: ONLINE")
    print("NETWORK: READY")
    print()

    tampilkan_gambar()
    menu()
