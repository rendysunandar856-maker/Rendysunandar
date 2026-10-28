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


# === CYBERSECURITY TOOLS ===
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

        if pilih == "1":
            try:
                data = input("IP/CIDR (contoh 192.168.1.0/24): ").strip()
                net = ipaddress.ip_network(data, strict=False)
                print("Network :", net.network_address)
                print("Netmask :", net.netmask)
                print("Broadcast:", net.broadcast_address)
                print("Jumlah alamat:", net.num_addresses)
            except ValueError as e:
                print("Input tidak valid:", e)

        elif pilih == "2":
            host = input("Domain: ").strip()
            if not host or "/" in host or " " in host:
                print("Domain tidak valid.")
                continue
            try:
                hasil = socket.getaddrinfo(host, None)
                for ip in sorted({x[4][0] for x in hasil}):
                    print("IP:", ip)
            except (socket.gaierror, OSError) as e:
                print("DNS gagal:", e)

        elif pilih == "3":
            url = input("URL situs milikmu/lab: ").strip()
            if "://" not in url:
                url = "https://" + url
            parsed = urlparse(url)

            if parsed.scheme not in ("http", "https") or not parsed.hostname:
                print("URL tidak valid.")
                continue

            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "RendySigma/1.0"}
                )
                with urllib.request.urlopen(req, timeout=8) as r:
                    print("HTTP status:", r.status)
                    for nama in (
                        "Strict-Transport-Security",
                        "Content-Security-Policy",
                        "X-Content-Type-Options",
                        "X-Frame-Options",
                        "Referrer-Policy",
                    ):
                        print(nama + ":", r.headers.get(nama, "Tidak ditemukan"))
            except Exception as e:
                print("Pemeriksaan gagal:", e)

        elif pilih == "4":
            host = input("Domain (tanpa https://): ").strip()
            if not host or "/" in host or " " in host:
                print("Domain tidak valid.")
                continue
            try:
                context = ssl.create_default_context()
                with socket.create_connection((host, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=host) as tls:
                        cert = tls.getpeercert()
                        print("Versi TLS:", tls.version())
                        print("Subjek:", cert.get("subject"))
                        print("Penerbit:", cert.get("issuer"))
                        print("Berlaku sampai:", cert.get("notAfter"))
            except Exception as e:
                print("Pemeriksaan TLS gagal:", e)

        elif pilih == "5":
            print("Gunakan hanya perangkat sendiri atau lab yang berizin.")
            host = input("IP/domain lab: ").strip()
            try:
                port = int(input("Port TCP (1-65535): ").strip())
                if not host or "/" in host or " " in host:
                    raise ValueError("Host tidak valid")
                if not 1 <= port <= 65535:
                    raise ValueError("Port harus 1 sampai 65535")

                with socket.create_connection((host, port), timeout=3):
                    print(f"Port {port}/TCP dapat dihubungi.")
            except (ValueError, OSError) as e:
                print("Koneksi gagal:", e)

        elif pilih == "6":
            path = input("Lokasi file zip/7z: ").strip()
            wordlist = input("Lokasi file wordlist: ").strip()
            try:
                import zipfile

                if not path.endswith(('.zip', '.7z')):
                    print("Pastikan ekstensi file adalah .zip atau .7z")
                    continue

                with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                    passwords = [line.strip() for line in f if line.strip()]

                print(f"Mulai crack file: {path} dengan {len(passwords)} kemungkinan password...")
                found = False

                if path.endswith('.zip'):
                    zip_file = zipfile.ZipFile(path)
                    for pwd in passwords:
                        try:
                            zip_file.extractall(pwd=pwd.encode('utf-8'))
                            print(f"Password ditemukan: {pwd}")
                            found = True
                            break
                        except RuntimeError:
                            continue
                else:
                    print("Format .7z memerlukan modul py7zr atau 7z command line tool.")
                    print("Mencoba menggunakan 7z command line tool...")
                    import subprocess
                    for pwd in passwords:
                        try:
                            result = subprocess.run(
                                ["7z", "t", "-p" + pwd, path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                timeout=2
                            )
                            if "No errors" in result.stderr.decode() or result.returncode == 0:
                                print(f"Password ditemukan: {pwd}")
                                found = True
                                break
                        except Exception:
                            continue

                if not found:
                    print("Password tidak ditemukan dalam wordlist.")
            except Exception as e:
                print("Gagal melakukan crack:", e)

        elif pilih == "7":
            path = input("Lokasi file log: ").strip()
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    lines = f.readlines()
                print("Total baris:", len(lines))
                for
