
import socket
import ssl
import urllib.request
import urllib.error
import platform
import os
import ipaddress
from datetime import datetime, timezone
from urllib.parse import urlparse

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def heading(title):
    print(f"\n{RED}--- {title} ---{RESET}")


def pause():
    input(f"\n{YELLOW}Tekan Enter untuk kembali...{RESET}")


def network_info():
    heading("INFORMASI JARINGAN")
    print("Hostname :", socket.gethostname())
    print("Sistem   :", platform.system(), platform.release())
    print("Python   :", platform.python_version())
    print("Arsitektur:", platform.machine())
    print("Termux   :", os.environ.get("PREFIX", "Tidak terdeteksi"))

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("192.0.2.1", 80))
            print("IP lokal :", s.getsockname()[0])
    except OSError as e:
        print("IP lokal tidak terdeteksi:", e)


def dns_lookup():
    heading("DNS LOOKUP")
    host = input("Domain (contoh: example.com): ").strip()

    if not host or "/" in host or " " in host:
        print("Masukkan domain saja.")
        return

    try:
        results = socket.getaddrinfo(host, None)
        addresses = sorted({item[4][0] for item in results})
        for address in addresses:
            print(f"{GREEN}{address}{RESET}")
    except socket.gaierror as e:
        print(f"{RED}DNS lookup gagal: {e}{RESET}")


def port_checker():
    heading("PORT CHECKER")
    host = input("IP/hostname perangkat milikmu atau lab: ").strip()

    try:
        port = int(input("Port (1-65535): "))
        if not host or not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        print("Host atau nomor port tidak valid.")
        return

    try:
        with socket.create_connection((host, port), timeout=3):
            print(f"{GREEN}Port {port} dapat dihubungi.{RESET}")
    except (OSError, socket.timeout) as e:
        print(f"{YELLOW}Port tidak dapat dihubungi: {e}{RESET}")


def connection_test():
    heading("CONNECTION TEST")
    host = input("Host milik sendiri/lab: ").strip()

    if not host:
        print("Host kosong.")
        return

    try:
        port = int(input("Port (contoh 443): "))
        if not 1 <= port <= 65535:
            raise ValueError

        start = datetime.now().timestamp()
        with socket.create_connection((host, port), timeout=5):
            elapsed = (datetime.now().timestamp() - start) * 1000

        print(f"{GREEN}Koneksi berhasil: {elapsed:.1f} ms{RESET}")
    except ValueError:
        print("Nomor port tidak valid.")
    except OSError as e:
        print(f"{YELLOW}Koneksi gagal: {e}{RESET}")


def http_security_check():
    heading("HTTP SECURITY CHECK")
    url = input("URL website milikmu/lab: ").strip()

    if not url:
        print("URL kosong.")
        return

    if not url.startswith(("https://", "http://")):
        url = "https://" + url

    if not urlparse(url).hostname:
        print("Format URL tidak valid.")
        return

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "RenSigma-NetworkAudit/1.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            headers = response.headers
            print("HTTP Status:", response.status)

            checks = {
                "Strict-Transport-Security": "HSTS",
                "Content-Security-Policy": "CSP",
                "X-Content-Type-Options": "MIME protection",
                "X-Frame-Options": "Framing protection",
                "Referrer-Policy": "Referrer policy",
            }

            for header, label in checks.items():
                if header in headers:
                    print(f"{GREEN}[ADA] {label}{RESET}")
                else:
                    print(f"{YELLOW}[PERLU DIPERIKSA] {label}{RESET}")

    except urllib.error.HTTPError as e:
        print("HTTP Status:", e.code, e.reason)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"{RED}Pemeriksaan gagal: {e}{RESET}")


def ssl_tls_checker():
    heading("SSL/TLS CERTIFICATE CHECK")
    host = input("Hostname HTTPS milik sendiri/lab: ").strip()

    if not host or "/" in host:
        print("Masukkan hostname saja, contoh: example.com")
        return

    try:
        context = ssl.create_default_context()

        with socket.create_connection((host, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as tls:
                cert = tls.getpeercert()

                print("TLS Version:", tls.version())
                cipher = tls.cipher()
                print("Cipher     :", cipher[0] if cipher else "Tidak diketahui")
                print("Subject    :", cert.get("subject"))
                print("Issuer     :", cert.get("issuer"))

                expiry = cert.get("notAfter")
                if expiry:
                    expiry_dt = datetime.strptime(
                        expiry, "%b %d %H:%M:%S %Y %Z"
                    ).replace(tzinfo=timezone.utc)

                    print("Kedaluwarsa:", expiry_dt.isoformat())
                    if expiry_dt > datetime.now(timezone.utc):
                        print(f"{GREEN}Sertifikat masih berlaku.{RESET}")
                    else:
                        print(f"{RED}Sertifikat kedaluwarsa.{RESET}")

    except (ssl.SSLError, OSError, ValueError) as e:
        print(f"{RED}Pemeriksaan TLS gagal: {e}{RESET}")


def lan_discovery():
    heading("LAN DISCOVERY")
    print("Hanya gunakan pada jaringan lokal milik sendiri/lab.")

    subnet = input("Subnet IPv4 (contoh 192.168.1.0/24): ").strip()

    try:
        network = ipaddress.ip_network(subnet, strict=False)

        if not isinstance(network, ipaddress.IPv4Network):
            print("Hanya mendukung IPv4.")
            return

        if network.num_addresses > 256:
            print("Batasi subnet hingga maksimal 256 alamat.")
            return

    except ValueError:
        print("Format subnet tidak valid.")
        return

    print(f"{CYAN}Memeriksa port TCP 80 pada {network}...{RESET}")
    print("Perangkat tanpa port 80 terbuka mungkin tidak terdeteksi.")

    found = 0

    for ip in network.hosts():
        try:
            with socket.create_connection((str(ip), 80), timeout=0.15):
                print(f"{GREEN}[HTTP aktif] {ip}{RESET}")
                found += 1
        except OSError:
            pass

    print(f"Pemeriksaan selesai. Respons ditemukan: {found}")


def main_menu():
    actions = {
        "1": ("Informasi jaringan", network_info),
        "2": ("DNS Lookup", dns_lookup),
        "3": ("Port Checker", port_checker),
        "4": ("Connection Test", connection_test),
        "5": ("HTTP Security Check", http_security_check),
        "6": ("SSL/TLS Checker", ssl_tls_checker),
        "7": ("LAN Discovery", lan_discovery),
    }

    while True:
        print(f"\n{CYAN}╔══════════════════════════════════╗")
        print("║       REN.SIGMA CYBER TOOLS      ║")
        print("╚══════════════════════════════════╝" + RESET)

        for number, (name, _) in actions.items():
            print(f"[{number}] {name}")

        print("[0] Keluar")
        choice = input(f"\n{YELLOW}Pilih menu: {RESET}").strip()

        if choice == "0":
            print(f"{GREEN}Ren.sigma ditutup. Sampai jumpa!{RESET}")
            break

        if choice not in actions:
            print(f"{RED}Pilihan tidak tersedia.{RESET}")
            continue

        try:
            actions[choice][1]()
        except (KeyboardInterrupt, EOFError):
            print("\nKembali ke menu.")

        pause()


if __name__ == "__main__":
    try:
        main_menu()
    except (KeyboardInterrupt, EOFError):
        print("\nRen.sigma ditutup.")
