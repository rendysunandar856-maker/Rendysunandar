
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

# =========================================
# REN.SIGMA - RENDY SUNANDAR
# =========================================

IMAGE_URL = "https://raw.githubusercontent.com/rendysunandar856-maker/Rendysunandar/main/anime_baru.jpg"

RED = "\033[91m"
ORANGE = "\033[38;5;208m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
MERAH = RED
CHARS = "@%#*+=-:. "


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
    print(RED + "       KELAS 11 TKJ" + RESET)
    print(RED + "  ┌──────────────────────────────┐" + RESET)
    print(RED + "  │  SYSTEM  : TERMUX ANDROID     │" + RESET)
    print(RED + "  │  STATUS  : READY              │" + RESET)
    print(RED + "  │  NETWORK : READY              │" + RESET)
    print(RED + "  │  SKILL   : NETWORKING         │" + RESET)
    print(RED + "  └──────────────────────────────┘" + RESET)
    print()


def judul():
    print()
    print(ORANGE + figlet("RENDY", "big") + RESET)
    print(RED + figlet("SUNANDAR", "big") + RESET)
    print(ORANGE + "================================" + RESET)
    print(RED + "           MENU UTAMA" + RESET)
    print(ORANGE + "================================" + RESET)


def jeda():
    input("\nTekan Enter untuk melanjutkan...")


# =========================================
# 1. INFORMASI SISTEM
# =========================================

def system_info():
    print("\n" + RED + "=== INFORMASI SISTEM ===" + RESET)
    print("Sistem       :", platform.system())
    print("Versi        :", platform.release())
    print("Arsitektur   :", platform.machine())
    print("Platform     :", platform.platform())
    print("Versi Python :", sys.version)
    print("Direktori    :", os.getcwd())
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
# PEMULIHAN PASSWORD ARSIP MILIK SENDIRI
# =========================================

def crack_archive():
    print("\n" + RED + "=== PEMULIHAN PASSWORD ARSIP ===" + RESET)
    print("Gunakan hanya pada arsip milikmu sendiri.")
    print("[1] Periksa password ZIP dari wordlist")
    print("[2] Periksa password 7Z dari wordlist")
    print("[0] Kembali")

    mode = input("Pilih mode: ").strip()

    if mode == "0":
        return

    if mode not in ("1", "2"):
        print("Pilihan tidak valid.")
        return

    path = input("Lokasi file arsip: ").strip()
    wordlist = input("Lokasi file wordlist: ").strip()

    if not os.path.isfile(path):
        print("File arsip tidak ditemukan.")
        return

    if not os.path.isfile(wordlist):
        print("File wordlist tidak ditemukan.")
        return

    if mode == "1":
        if not path.lower().endswith(".zip"):
            print("File harus berformat ZIP.")
            return

        try:
            with zipfile.ZipFile(path, "r") as archive:
                members = [
                    item for item in archive.infolist()
                    if not item.is_dir()
                ]

                encrypted = [
                    item for item in members
                    if item.flag_bits & 1
                ]

                if not encrypted:
                    print("Tidak ditemukan file ZIP terenkripsi.")
                    return

                print(
                    "Arsip terenkripsi ditemukan. "
                    "Gunakan perangkat pemulihan tepercaya "
                    "untuk arsip milikmu."
                )
                print("Jumlah file terenkripsi:", len(encrypted))

        except (OSError, zipfile.BadZipFile) as e:
            print("Gagal membaca ZIP:", e)

    elif mode == "2":
        if not path.lower().endswith(".7z"):
            print("File harus berformat 7Z.")
            return

        print(
            "Pemulihan 7Z tidak dijalankan otomatis oleh program ini. "
            "Pastikan arsip milikmu dan gunakan alat pemulihan tepercaya."
        )


# =========================================
# CYBERSECURITY TOOLS
# =========================================

def cybersecurity_tools():
    while True:
        print("\n" + MERAH + "=== CYBERSECURITY TOOLS ===" + RESET)
        print("[1] Kalkulator subnet")
        print("[2] DNS lookup")
        print("[3] Pemeriksaan header HTTP")
        print("[4] Pemeriksaan sertifikat TLS")
        print("[5] Cek satu port TCP (lab berizin)")
        print("[6] Crack ZIP/7Z Password")
        print("[7] Analisis log lokal")
        print("[8] Informasi lingkungan Python")
        print("[0] Kembali ke menu utama")

        pilih = input("Pilih tools: ").strip()

        try:
            if pilih == "1":
                data = input(
                    "IP/CIDR (contoh 192.168.1.0/24): "
                ).strip()

                net = ipaddress.ip_network(data, strict=False)
                print("Network :", net.network_address)
                print("Netmask :", net.netmask)
                print("Broadcast:", net.broadcast_address)
                print("Jumlah alamat:", net.num_addresses)

                if net.num_addresses > 2:
                    print("Host awal:", net.network_address + 1)
                    print("Host akhir:", net.broadcast_address - 1)

            elif pilih == "2":
                host = input("Domain: ").strip()

                if not host or "/" in host or " " in host:
                    print("Domain tidak valid.")
                    continue

                hasil = socket.getaddrinfo(host, None)
                addresses = sorted({item[4][0] for item in hasil})

                for address in addresses:
                    print("IP:", address)

            elif pilih == "3":
                url = input("URL situs milikmu/lab: ").strip()

                if "://" not in url:
                    url = "https://" + url

                parsed = urlparse(url)

                if (
                    parsed.scheme not in ("http", "https")
                    or not parsed.hostname
                ):
                    print("URL tidak valid.")
                    continue

                request = urllib.request.Request(
                    url,
                    headers={"User-Agent": "RendySigma/1.0"}
                )

                with urllib.request.urlopen(request, timeout=8) as response:
                    print("HTTP status:", response.status)

                    for name in (
                        "Strict-Transport-Security",
                        "Content-Security-Policy",
                        "X-Content-Type-Options",
                        "X-Frame-Options",
                        "Referrer-Policy",
                    ):
                        print(
                            name + ":",
                            response.headers.get(name, "Tidak ditemukan")
                        )

            elif pilih == "4":
                host = input("Domain (tanpa https://): ").strip()

                if not host or "/" in host or " " in host:
                    print("Domain tidak valid.")
                    continue

                context = ssl.create_default_context()

                with socket.create_connection(
                    (host, 443), timeout=5
                ) as sock:
                    with context.wrap_socket(
                        sock, server_hostname=host
                    ) as tls:
                        cert = tls.getpeercert()
                        print("Versi TLS:", tls.version())
                        print("Subjek:", cert.get("subject"))
                        print("Penerbit:", cert.get("issuer"))
                        print("Berlaku sampai:", cert.get("notAfter"))

            elif pilih == "5":
                print("Gunakan hanya perangkat sendiri atau lab berizin.")
                host = input("IP/domain lab: ").strip()
                port = int(input("Port TCP (1-65535): ").strip())

                if not host or "/" in host or " " in host:
                    print("Host tidak valid.")
                    continue

                if not 1 <= port <= 65535:
                    print("Port tidak valid.")
                    continue

                with socket.create_connection((host, port), timeout=3):
                    print(f"Port {port}/TCP dapat dihubungi.")

            elif pilih == "6":
                crack_archive()

            elif pilih == "7":
                path = input("Lokasi file log: ").strip()
                keywords = (
                    "error", "failed", "warning", "denied", "critical"
                )

                with open(
                    path, "r", encoding="utf-8", errors="replace"
                ) as file:
                    found = 0

                    for number, line in enumerate(file, 1):
                        if any(word in line.lower() for word in keywords):
                            print(f"{number}: {line.rstrip()}")
                            found += 1

                            if found >= 100:
                                print("Hasil dibatasi hingga 100 baris.")
                                break

                    if found == 0:
                        print("Tidak ditemukan baris yang cocok.")

            elif pilih == "8":
                print("Python:", sys.version)
                print("Sistem:", platform.platform())
                print("Arsitektur:", platform.machine())
                print("Executable:", sys.executable)

            elif pilih == "0":
                return

            else:
                print("Pilihan tidak valid.")
                continue

        except (OSError, ValueError, socket.gaierror, ssl.SSLError) as e:
            print("Terjadi kesalahan:", e)
        except Exception as e:
            print("Tools gagal dijalankan:", e)

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
        else:
            print("Pilihan tidak valid.")

        jeda()


# =========================================
# PROFIL
# =========================================

def profil():
    print("\n" + RED + "=== PROFIL ===" + RESET)
    print("Nama       : Rendy Sunandar")
    print("Kelas      : 11 TKJ")
    print("Project    : Ren.sigma")
    print("Fokus      : Networking")
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
