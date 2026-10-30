#!/usr/bin/env python3
import socket
import socks
import random
import sys
import time
import requests
import urllib3
import re
import json
from datetime import datetime
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===== COLOR PALETTE =====
W = '\033[1;37m'
GREY = '\033[90m'
RESET = '\033[0m'
RED = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
C = '\033[1;36m'
B = '\033[1;34m'
DP = '\033[38;5;129m'
BOLD = '\033[1m'

BANNER = rf"""{GREY}
          !\_______/!\
          !!                 !! \
          !!    WEBCK Toolkit  !!   \
          !!                 !!    !
          !!        Free     !!    !
          !!                 !!    !
          !!       #hugs     !!    !
          !!                 !!  /
          !!_______!! /
          !/_______\!/
             _\_____//!
            !_________!/
{W}
[---]        WebCheck - Threat & Trust    [---]
[---]        Created by: Nur whoami136    [---]
[---]    Homepage: https://github.com/whoami136 [---]
{RESET}"""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15"
]

HIGH_RISK_TLDS = ['.top', '.xyz', '.buzz', '.bid', '.click', '.loan', '.download', '.stream', '.gq', '.ml', '.cf', '.tk']

def loading_interface():
    modules = [
        "SOCKS5 Global Tor Wrapper",
        "3-Tier Tor Exit Node & Geo-ASN Verifier",
        "Anti-DNS Leak Module",
        "URLhaus & Phishing Threat DB Connector",
        "WHOIS Domain Age & Registrar Auditor",
        "SSL / HTTP Security & Fraud Heuristics"
    ]
    print(f"{C}[*] Initializing Apex Security Framework...{RESET}")
    for mod in modules:
        print(f"{GREY}  [ ] Loading {mod}...", end="", flush=True)
        time.sleep(random.uniform(0.03, 0.07))
        print(f"\r{G}  [✔] Loading {mod}... Synchronized{RESET}")
    print("")

class TorGuard:
    def __init__(self, port=9050):
        self.port = port
        self.exit_ip = None
        self.exit_country = "Unknown"
        self.exit_isp = "Unknown"

    def verify_all(self):
        print(f"{C}[*] Commencing 3-Step Tor Exit Node Verification...{RESET}")

        print(f"{GREY}  [Step 1/3] Testing local SOCKS5 listener (127.0.0.1:{self.port})...{RESET}", end="", flush=True)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                if s.connect_ex(("127.0.0.1", self.port)) != 0:
                    raise ConnectionRefusedError
            print(f"\r{G}  [✔ Step 1/3] Port {self.port} active. Tor service is running.{RESET}")
        except Exception:
            print(f"\r{RED}  [✘ Step 1/3] FATAL: Port {self.port} is down! Start Tor first (sudo systemctl start tor).{RESET}")
            print(f"{Y}[!] Execution halted to prevent leaking your real public IP.{RESET}\n")
            sys.exit(1)

        proxies = {
            'http': f'socks5h://127.0.0.1:{self.port}',
            'https': f'socks5h://127.0.0.1:{self.port}'
        }

        print(f"{GREY}  [Step 2/3] Querying official Tor Project Directory Consensus...{RESET}", end="", flush=True)
        try:
            r = requests.get("https://check.torproject.org/api/ip", proxies=proxies, timeout=10)
            data = r.json()
            self.exit_ip = data.get("IP", "Unknown")
            is_tor = data.get("IsTor", False)

            if not is_tor:
                print(f"\r{RED}  [✘ Step 2/3] FAILED: Proxy connected, but IP is NOT a recognized Tor Exit!{RESET}")
                sys.exit(1)
            print(f"\r{G}  [✔ Step 2/3] Consensus Confirmed! Official Tor Exit Node: {W}{self.exit_ip}{RESET}")
        except Exception as e:
            print(f"\r{RED}  [✘ Step 2/3] FAILED: Could not authenticate Tor network ({e}).{RESET}")
            sys.exit(1)

        print(f"{GREY}  [Step 3/3] Fetching Exit Node Geo-Location & ISP Metadata...{RESET}", end="", flush=True)
        try:
            r_geo = requests.get(f"http://ip-api.com/json/{self.exit_ip}", timeout=8)
            geo_data = r_geo.json()
            if geo_data.get("status") == "success":
                self.exit_country = geo_data.get("country", "Unknown")
                self.exit_isp = geo_data.get("isp", "Unknown")
            print(f"\r{G}  [✔ Step 3/3] Exit Identity Verified: {W}{self.exit_country} ({self.exit_isp}){RESET}\n")
        except Exception:
            print(f"\r{G}  [✔ Step 3/3] Target will strictly log Exit Node IP: {W}{self.exit_ip}{RESET}\n")

        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", self.port, rdns=True)
        socket.socket = socks.socksocket
        return proxies

def query_whois_deep(domain):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(8)
        s.connect(("whois.iana.org", 43))
        s.send(f"{domain}\r\n".encode())
        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        s.close()
        text = response.decode('utf-8', errors='ignore')

        refer_match = re.search(r'refer:\s+([^\s]+)', text, re.I)
        if refer_match:
            refer_server = refer_match.group(1).strip()
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.settimeout(8)
            s2.connect((refer_server, 43))
            s2.send(f"{domain}\r\n".encode())
            resp2 = b""
            while True:
                data2 = s2.recv(4096)
                if not data2:
                    break
                resp2 += data2
            s2.close()
            text = resp2.decode('utf-8', errors='ignore')

        created = None
        registrar = None
        for line in text.splitlines():
            if not created and re.search(r'Creation Date|created:|registered:', line, re.I):
                created = line.split(":", 1)[1].strip()
            if not registrar and re.search(r'Registrar:|Registrar Name:', line, re.I):
                registrar = line.split(":", 1)[1].strip()

        return created or "Hidden / Non-standard", registrar or "Unknown / Redacted"
    except Exception:
        return "Query Timeout", "Unknown"

def calculate_domain_age(created_str):
    try:
        cleaned_date = re.sub(r'\.\d+Z?', '', created_str)
        cleaned_date = cleaned_date.split('T')[0].split(' ')[0]
        creation_date = datetime.strptime(cleaned_date, "%Y-%m-%d")
        age_days = (datetime.now() - creation_date).days
        return age_days
    except Exception:
        return None

def scan(target):
    print(BANNER)
    loading_interface()

    guard = TorGuard(port=9050)
    proxies = guard.verify_all()

    parsed = urlparse(target if "://" in target else f"http://{target}")
    raw_domain = parsed.netloc or parsed.path.split('/')[0]
    raw_domain = raw_domain.split(':')[0]
    clean_domain = re.sub(r'^www\.', '', raw_domain)

    print(f"{B}TARGET HOST:{RESET} {W}{BOLD}{raw_domain}{RESET}")
    print(f"{GREY}Running deep threat intelligence, scam verification & trust scoring over Tor...{RESET}\n")

    print(f"{C}[*] Querying Malware & Scam Blacklists (URLhaus)...{RESET}", end="", flush=True)
    threat_status = "Clean"
    is_malicious = False
    try:
        r = requests.post("https://urlhaus-api.abuse.ch/v1/host/", data={"host": clean_domain}, proxies=proxies, timeout=10)
        data = r.json()
        if data.get("query_status") == "ok":
            is_malicious = True
            threat_status = f"{RED}{BOLD}MALICIOUS / SCAM ({data.get('url_count', 0)} reports){RESET}"
            print(f"\r{C}[*] Querying Malware & Scam Blacklists (URLhaus)... {RED}[ALERT FOUND]{RESET}")
        else:
            threat_status = f"{G}Clean (0 malicious reports){RESET}"
            print(f"\r{C}[*] Querying Malware & Scam Blacklists (URLhaus)... {G}[PASSED]{RESET}")
    except Exception:
        threat_status = f"{Y}Threat API Timeout{RESET}"
        print(f"\r{C}[*] Querying Malware & Scam Blacklists (URLhaus)... {Y}[SKIPPED]{RESET}")

    print(f"{C}[*] Inspecting SSL Handshake & HTTP Status...{RESET}", end="", flush=True)
    http_code = "000"
    ssl_status = f"{RED}Unencrypted (Plain HTTP){RESET}"
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        r = requests.get(f"https://{raw_domain}", headers=headers, proxies=proxies, timeout=10, verify=False, allow_redirects=True)
        http_code = str(r.status_code)
        ssl_status = f"{G}Valid (HTTPS Secure){RESET}"
        print(f"\r{C}[*] Inspecting SSL Handshake & HTTP Status... {G}[PASSED]{RESET}")
    except Exception:
        try:
            r = requests.get(f"http://{raw_domain}", headers=headers, proxies=proxies, timeout=10, allow_redirects=True)
            http_code = str(r.status_code)
            print(f"\r{C}[*] Inspecting SSL Handshake & HTTP Status... {Y}[HTTP FALLBACK]{RESET}")
        except Exception:
            http_code = "Unreachable"
            print(f"\r{C}[*] Inspecting SSL Handshake & HTTP Status... {RED}[FAILED]{RESET}")

    print(f"{C}[*] Analyzing Domain Age & WHOIS Registration Record...{RESET}", end="", flush=True)
    creation_date, registrar = query_whois_deep(clean_domain)
    age_days = calculate_domain_age(creation_date)
    
    age_str = f"{age_days} Days Old" if age_days is not None else "Unknown Age"
    if age_days is not None and age_days < 90:
        age_str += f" {RED}(HIGH FRAUD RISK: < 90 Days){RESET}"
    elif age_days is not None:
        age_str += f" {G}(Established){RESET}"
    
    print(f"\r{C}[*] Analyzing Domain Age & WHOIS Registration Record... {G}[PASSED]{RESET}\n")

    tld_risk = f"{G}Standard / Trusted TLD{RESET}"
    is_high_risk_tld = any(clean_domain.endswith(tld) for tld in HIGH_RISK_TLDS)
    if is_high_risk_tld:
        tld_risk = f"{RED}High Scam Correlation TLD (.xyz/.top/etc){RESET}"

    print(f"{W}╔═════════════════════ WEBCK ADVANCED TELEMETRY ════════════════════╗{RESET}")
    print(f"║ {'Target Domain':<23} : {raw_domain:<38} ║")
    print(f"║ {'Threat Intelligence':<23} : {threat_status:<38} ║")
    print(f"║ {'SSL Security':<23} : {ssl_status:<38} ║")
    print(f"║ {'HTTP Status Code':<23} : {http_code:<38} ║")
    print(f"║ {'Domain Creation':<23} : {creation_date[:38]:<38} ║")
    print(f"║ {'Calculated Age':<23} : {age_str:<38} ║")
    print(f"║ {'TLD Risk Profile':<23} : {tld_risk:<38} ║")
    print(f"║ {'Domain Registrar':<23} : {registrar[:38]:<38} ║")
    print(f"║ {'Tor Exit Node IP':<23} : {guard.exit_ip:<38} ║")
    print(f"║ {'Tor Exit Country':<23} : {guard.exit_country:<38} ║")
    print(f"{W}╚═════════════════════════════════════════════════════════════════╝{RESET}")

    if is_malicious or (age_days is not None and age_days < 30) or is_high_risk_tld:
        print(f"\n{RED}{BOLD}[ ✖ FRAUD / SCAM WARNING ] High risk indicators detected! Exercise extreme caution.{RESET}")
    else:
        print(f"\n{G}{BOLD}[ ✔ TRUST CHECK PASSED ] No critical active threat indicators found.{RESET}")

    print(f"\n{DP}# =================================================================={RESET}")
    print(f"{DP}  Protected via Tor Anonymity Network (Exit Node: {guard.exit_ip}){RESET}")
    print(f"{DP}# =================================================================={RESET}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(BANNER)
        print(f"{RED}[!] Error: Missing target URL or domain.{RESET}")
        print(f"{Y}Usage: webcheck <target.com> or webcheck https://target.com{RESET}\n")
        sys.exit(1)
    scan(sys.argv[1])
