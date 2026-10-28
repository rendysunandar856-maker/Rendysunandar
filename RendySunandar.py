
#!/usr/bin/env python3
# Ren.sigma - Network Security Edition
# Gunakan hanya pada sistem, jaringan, dan file yang kamu punya izin
# untuk menguji atau menganalisis.

import os
import re
import ssl
import sys
import json
import math
import socket
import hashlib
import ipaddress
import platform
import urllib.request
import urllib.error
from datetime import datetime
from urllib.parse import urlparse

VERSION = "2.0"
IMAGE_URL = (
    "https://raw.githubusercontent.com/rendysunandar856-maker/"
    "Rendysunandar/main/anime_baru.jpg"
)

R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
W = "\033[97m"
RESET = "\033[0m"


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def pause():
    input(f"\n{Y}Tekan Enter untuk kembali...{RESET}")


def banner():
    print(f"{C}")
    print(r"""
 ____                 _
|  _ \ ___ _ __   ___(_) __ _ _ __ ___   __ _
| |_) / _ \ '_ \ / __| |/ _` | '_ ` _ \ / _` |
|  _ <  __/ | | | (__| | (_| | | | | | | (_| |
|_| \_\___|_| |_|\___|_|\__, |_| |_| |_|\__,_|
                        |___/
    """)
    print(f"{W}        Ren.sigma Network Security Edition {VERSION}{RESET}")

    # Opsional: tampilkan gambar GitHub jika Pillow tersedia.
    try:
        from io import BytesIO
        from PIL import Image

        req = urllib.request.Request(
            IMAGE_URL, headers={"User-Agent": "RenSigma/2.0"}
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            image_data = response.read(2_000_000)

        image = Image.open(BytesIO(image_data)).convert("RGB")
        image.thumbnail((48, 20))
        chars = " .:-=+*#%@"
        pixels = list(image.getdata())
        width, height = image.size

        for y in range(height):
            line = ""
            for x in range(width):
                rr, gg, bb = pixels[y * width + x]
                brightness = int((rr * 0.299 + gg * 0.587 + bb * 0.114) / 256 * len(chars))
                brightness = min(brightness, len(chars) - 1)
                line += f"\033[38;2;{rr};{gg};{bb}m{chars[brightness]}{RESET}"
            print(line)
    except Exception:
        pass

    print(f"{C}" + "-" * 48 + RESET)


def ask(prompt):
    return input(f"{Y}{prompt}{RESET}").strip()


def valid_domain(value):
    value = value.strip()
    if "://" in value:
        value = urlparse(value).hostname or ""
    value = value.rstrip(".")
    if not value or len(value) > 253 or " " in value:
        raise ValueError("Domain tidak valid.")
    return value


# 1. IP & Subnet Calculator
def subnet_calculator():
    print(f"\n{C}=== IP & SUBNET CALCULATOR ==={RESET}")
    try:
        network = ipaddress.ip_network(ask("IP/CIDR (contoh 192.168.1.10/24): "), strict=False)
        print("Network       :", network.network_address)
        print("Netmask       :", network.netmask)
        print("Broadcast     :", network.broadcast_address)
        print("Prefix        :", network.prefixlen)
        print("Total alamat  :", network.num_addresses)
        if network.version == 4:
            print("Host usable   :", max(0, network.num_addresses - 2)
                  if network.prefixlen < 31 else network.num_addresses)
            print("Wildcard mask :", ipaddress.IPv4Address(int(network.hostmask)))
    except ValueError as exc:
        print(f"{R}Input tidak valid: {exc}{RESET}")


# 2. DNS Lookup
def dns_lookup():
    print(f"\n{C}=== DNS LOOKUP ==={RESET}")
    try:
        host = valid_domain(ask("Domain: "))
        results = socket.getaddrinfo(host, None)
        addresses = sorted({result[4][0] for result in results})
        for address in addresses:
            print(f"{G}{address}{RESET}")
        if not addresses:
            print("Tidak ada alamat ditemukan.")
    except (ValueError, socket.gaierror, OSError) as exc:
        print(f"{R}Lookup gagal: {exc}{RESET}")


# 3. WHOIS Lookup (server WHOIS publik, koneksi baca saja)
def whois_lookup():
    print(f"\n{C}=== WHOIS LOOKUP ==={RESET}")
    try:
        domain = valid_domain(ask("Domain (contoh example.com): "))
        if "." not in domain or domain.startswith("-"):
            print("Masukkan nama domain yang valid.")
            return

        with socket.create_connection(("whois.iana.org", 43), timeout=6) as sock:
            sock.sendall((domain + "\r\n").encode())
            chunks = []
            while True:
                part = sock.recv(4096)
                if not part:
                    break
                chunks.append(part)
                if sum(map(len, chunks)) > 100_000:
                    break

        response = b"".join(chunks).decode("utf-8", errors="replace")
        refer = re.search(r"(?im)^refer:\s*(\S+)", response)
        server = refer.group(1) if refer else None

        if server:
            with socket.create_connection((server, 43), timeout=6) as sock:
                sock.sendall((domain + "\r\n").encode())
                chunks = []
                total = 0
                while total < 100_000:
                    part = sock.recv(min(4096, 100_000 - total))
                    if not part:
                        break
                    chunks.append(part)
                    total += len(part)
            response = b"".join(chunks).decode("utf-8", errors="replace")

        print(response[:12000] or "Tidak ada data WHOIS.")
    except (ValueError, OSError) as exc:
        print(f"{R}WHOIS gagal: {exc}{RESET}")


# Helper HTTP: hanya GET/OPTIONS/HEAD, tidak mengirim kredensial
def http_request(url, method="GET"):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("URL harus diawali http:// atau https://")
    if parsed.username or parsed.password:
        raise ValueError("Jangan masukkan kredensial ke dalam URL.")

    req = urllib.request.Request(
        url,
        method=method,
        headers={"User-Agent": "RenSigma-Defensive-Audit/2.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            return response.status, response.headers, response.read(200_000)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers, exc.read(20_000)


# 4. HTTP Method Checker
def http_method_checker():
    print(f"\n{C}=== HTTP METHOD CHECKER ==={RESET}")
    try:
        url = ask("URL milik sendiri/lab: ")
        status, headers, _ = http_request(url, "OPTIONS")
        print("HTTP status:", status)
        allowed = headers.get("Allow")
        if allowed:
            print("Allow:", allowed)
        else:
            print("Server tidak mengirim header Allow.")
            print("Hasil ini tidak membuktikan metode tertentu diizinkan atau ditolak.")
    except (ValueError, OSError, urllib.error.URLError) as exc:
        print(f"{R}Request gagal: {exc}{RESET}")


# 5. Security Headers Analyzer
def headers_analyzer():
    print(f"\n{C}=== SECURITY HEADERS ANALYZER ==={RESET}")
    checks = {
        "Strict-Transport-Security": "Membantu menerapkan HTTPS",
        "Content-Security-Policy": "Membatasi sumber konten",
        "X-Content-Type-Options": "Mencegah MIME sniffing",
        "X-Frame-Options": "Perlindungan framing lama",
        "Referrer-Policy": "Mengatur informasi referrer",
        "Permissions-Policy": "Mengatur akses fitur browser",
    }
    try:
        url = ask("URL situs milik sendiri/lab: ")
        status, headers, _ = http_request(url, "GET")
        print("HTTP status:", status)
        for name, description in checks.items():
            value = headers.get(name)
            if value:
                print(f"{G}[ADA]{RESET} {name}: {value}")
            else:
                print(f"{Y}[BELUM TERLIHAT]{RESET} {name} — {description}")
        print("\nCatatan: hasil ini pemeriksaan awal, bukan bukti kerentanan.")
    except (ValueError, OSError, urllib.error.URLError) as exc:
        print(f"{R}Analisis gagal: {exc}{RESET}")


# 6. TLS Certificate Inspector
def certificate_inspector():
    print(f"\n{C}=== CERTIFICATE INSPECTOR ==={RESET}")
    try:
        host = valid_domain(ask("Hostname HTTPS: "))
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=7) as raw:
            with context.wrap_socket(raw, server_hostname=host) as secure:
                cert = secure.getpeercert()
                print("TLS version :", secure.version())
                print("Cipher      :", secure.cipher())
                print("Subject     :", cert.get("subject"))
                print("Issuer      :", cert.get("issuer"))
                expiry = cert.get("notAfter")
                print("Expires     :", expiry or "Tidak tersedia")
                if expiry:
                    expires_at = datetime.strptime(expiry, "%b %d %H:%M:%S %Y %Z")
                    remaining = (expires_at - datetime.utcnow()).days
                    print("Sisa hari   :", remaining)
    except (ValueError, OSError, ssl.SSLError) as exc:
        print(f"{R}Pemeriksaan gagal: {exc}{RESET}")


# 7. Local Network Scanner — hanya subnet kecil yang diizinkan
def local_network_scanner():
    print(f"\n{C}=== LOCAL NETWORK SCANNER ==={RESET}")
    print("Gunakan hanya pada jaringan milik sendiri atau lab berizin.")
    try:
        network = ipaddress.ip_network(ask("Subnet IPv4 (contoh 192.168.1.0/24): "), strict=False)
        if network.version != 4 or network.num_addresses > 256:
            print("Dibatasi ke subnet IPv4 dengan maksimal 256 alamat.")
            return
        port_text = ask("TCP port yang ingin diperiksa (contoh 80): ")
        port = int(port_text)
        if not 1 <= port <= 65535:
            print("Port harus antara 1 dan 65535.")
            return

        found = 0
        for ip in network.hosts():
            try:
                with socket.create_connection((str(ip), port), timeout=0.25):
                    print(f"{G}[RESPON]{RESET} {ip}:{port}")
                    found += 1
            except OSError:
                pass
        print(f"Selesai. Perangkat merespons pada port {port}: {found}")
        print("Perangkat yang tidak merespons port tersebut bisa saja tetap aktif.")
    except (ValueError, OSError) as exc:
        print(f"{R}Input/scan gagal: {exc}{RESET}")


# 8. PCAP Analyzer — memakai Scapy bila sudah dipasang
def pcap_analyzer():
    print(f"\n{C}=== PCAP ANALYZER ==={RESET}")
    path = ask("Lokasi file .pcap/.pcapng milik sendiri: ")
    if not os.path.isfile(path):
        print("File tidak ditemukan.")
        return
    if not path.lower().endswith((".pcap", ".pcapng")):
        print("Pilih file .pcap atau .pcapng.")
        return
    try:
        from scapy.utils import PcapReader
        from collections import Counter
        protocols = Counter()
        sources = Counter()
        destinations = Counter()
        count = 0

        with PcapReader(path) as reader:
            for packet in reader:
                count += 1
                if packet.haslayer("IP"):
                    ip = packet["IP"]
                    sources[ip.src] += 1
                    destinations[ip.dst] += 1
                    if packet.haslayer("TCP"):
                        protocols["TCP"] += 1
                    elif packet.haslayer("UDP"):
                        protocols["UDP"] += 1
                    elif packet.haslayer("ICMP"):
                        protocols["ICMP"] += 1
                    else:
                        protocols["IP lainnya"] += 1
                elif packet.haslayer("IPv6"):
                    protocols["IPv6"] += 1
                else:
                    protocols["Non-IP/lainnya"] += 1

        print("Total paket:", count)
        print("Protokol:", dict(protocols))
        print("Top IP sumber:", sources.most_common(10))
        print("Top IP tujuan:", destinations.most_common(10))
    except ImportError:
        print("Scapy belum terpasang.")
        print("Coba: pip install scapy")
    except Exception as exc:
        print(f"{R}Gagal membaca PCAP: {exc}{RESET}")


# 9. Log Analyzer
def log_analyzer():
    print(f"\n{C}=== LOG ANALYZER ==={RESET}")
    path = ask("Lokasi file log teks milik sendiri: ")
    if not os.path.isfile(path):
        print("File tidak ditemukan.")
        return

    patterns = {
        "failed": re.compile(r"failed|failure|invalid password|authentication error", re.I),
        "denied": re.compile(r"denied|forbidden|blocked|unauthorized", re.I),
        "error": re.compile(r"\berror\b|exception|critical", re.I),
        "timeout": re.compile(r"timeout|timed out|connection reset", re.I),
    }
    totals = {name: 0 for name in patterns}
    matches = []

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as file:
            for line_number, line in enumerate(file, 1):
                for name, pattern in patterns.items():
                    if pattern.search(line):
                        totals[name] += 1
                        if len(matches) < 30:
                            matches.append((line_number, name, line.strip()[:240]))
                        break

        print("Ringkasan:")
        for name, total in totals.items():
            print(f"  {name}: {total}")
        print("\nContoh baris yang cocok:")
        for number, category, line in matches:
            print(f"[baris {number}] [{category}] {line}")
        print("\nPola ini hanya indikator awal; periksa konteks sebelum menyimpulkan.")
    except OSError as exc:
        print(f"{R}Gagal membaca log: {exc}{RESET}")


# 10. SHA-256 File Integrity Checker
def hash_checker():
    print(f"\n{C}=== SHA-256 HASH CHECKER ==={RESET}")
    path = ask("Lokasi file: ")
    if not os.path.isfile(path):
        print("File tidak ditemukan.")
        return

    digest = hashlib.sha256()
    try:
        with open(path, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        actual = digest.hexdigest()
        print("SHA-256:", actual)

        expected = ask("SHA-256 pembanding (kosongkan untuk melewati): ").lower()
        if expected:
            if re.fullmatch(r"[0-9a-f]{64}", expected) is None:
                print("Format SHA-256 harus terdiri dari 64 karakter heksadesimal.")
            elif actual == expected:
                print(f"{G}HASH COCOK{RESET}")
            else:
                print(f"{R}HASH BERBEDA{RESET}")
    except OSError as exc:
        print(f"{R}Gagal membaca file: {exc}{RESET}")


# 11. Password Strength Auditor — lokal, tanpa koneksi internet
def password_auditor():
    print(f"\n{C}=== PASSWORD STRENGTH AUDITOR ==={RESET}")
    print("Pemeriksaan dilakukan lokal. Jangan gunakan kata sandi asli.")
    password = ask("Masukkan kata sandi contoh: ")
    if not password:
        print("Input kosong.")
        return

    score = 0
    score += 1 if len(password) >= 12 else 0
    score += 1 if len(password) >= 16 else 0
    score += 1 if re.search(r"[a-z]", password) else 0
    score += 1 if re.search(r"[A-Z]", password) else 0
    score += 1 if re.search(r"\d", password) else 0
    score += 1 if re.search(r"[^A-Za-z0-9]", password) else 0

    if password.lower() in {"password", "password123", "admin", "qwerty123"}:
        score = 0

    if score <= 2:
        rating = "Lemah"
    elif score <= 4:
        rating = "Sedang"
    else:
        rating = "Lebih kuat"

    print("Panjang:", len(password))
    print("Skor indikator:", score, "/ 6")
    print("Penilaian sederhana:", rating)
    print("Gunakan kata sandi unik dan panjang; aktifkan MFA jika tersedia.")
    print("Ini bukan pengukuran entropi atau jaminan keamanan.")


# 12. Network Information
def network_info():
    print(f"\n{C}=== NETWORK / SYSTEM INFO ==={RESET}")
    print("Hostname :", socket.gethostname())
    print("OS       :", platform.system(), platform.release())
    print("Python   :", platform.python_version())
    print("Arsitektur:", platform.machine())
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("192.0.2.1", 80))
            print("IP lokal :", sock.getsockname()[0])
    except OSError:
        print("IP lokal : tidak dapat ditentukan")


def main():
    while True:
        clear()
        banner()
        print(f"""
{W}[1]{RESET} IP & Subnet Calculator
{W}[2]{RESET} DNS Lookup
{W}[3]{RESET} WHOIS Lookup
{W}[4]{RESET} HTTP Method Checker
{W}[5]{RESET} Security Headers Analyzer
{W}[6]{RESET} TLS Certificate Inspector
{W}[7]{RESET} Local Network Scanner
{W}[8]{RESET} PCAP Analyzer
{W}[9]{RESET} Log Analyzer
{W}[10]{RESET} SHA-256 Hash Checker
{W}[11]{RESET} Password Strength Auditor
{W}[12]{RESET} Network / System Info
{R}[0]{RESET} Keluar
""")
        choice = ask("Ren.sigma > ")

        actions = {
            "1": subnet_calculator,
            "2": dns_lookup,
            "3": whois_lookup,
            "4": http_method_checker,
            "5": headers_analyzer,
            "6": certificate_inspector,
            "7": local_network_scanner,
            "8": pcap_analyzer,
            "9": log_analyzer,
            "10": hash_checker,
            "11": password_auditor,
            "12": network_info,
        }

        if choice == "0":
            print(f"{G}Ren.sigma ditutup. Sampai jumpa!{RESET}")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except KeyboardInterrupt:
                print("\nDibatalkan.")
            except Exception as exc:
                print(f"{R}Terjadi kesalahan: {exc}{RESET}")
            pause()
        else:
            print(f"{R}Pilihan tidak valid.{RESET}")
            pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeluar.")

