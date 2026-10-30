<img width="1920" height="918" alt="Screenshot_2026-10-31_00_14_51" src="https://github.com/user-attachments/assets/c66c37b2-ffa4-44e3-8fe9-01eef19ad77d" />

# WEBCHECK
WebCheck is an advanced command-line threat intelligence and fraud verification tool designed for Kali Linux and NetHunter. It inspects domain age, SSL security, WHOIS records, and Abuse.ch malware blacklists—all 100% anonymized and securely routed through the Tor network to protect your real IP.
cat << 'EOF' > README.md
# 🌐 WEBCHECK

<p align="center">
  <img src="https://img.shields.io/badge/OS-Kali%20Linux%20%7C%20NetHunter-blue?style=for-the-badge&logo=kalilinux" alt="Kali Linux" />
  <img src="https://img.shields.io/badge/Language-Python%203-yellow?style=for-the-badge&logo=python" alt="Python 3" />
  <img src="https://img.shields.io/badge/Privacy-Tor%20Network-purple?style=for-the-badge&logo=torbrowser" alt="Tor Network" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

> **WebCheck** is an advanced command-line threat intelligence and fraud verification tool built for **Kali Linux** and **Kali NetHunter**. It performs automated domain risk scoring, SSL inspection, WHOIS auditing, and malware blacklist checks—all 100% anonymized and securely routed through the Tor network to protect your public IP.

---

## ⚡ Features

- **🔒 3-Tier Tor Identity Verification:** Verifies SOCKS5 listener, checks official Tor consensus, and retrieves exit node country/ISP metadata before launching targets.
- **🛡 Anti-DNS Leak & Anonymity:** Enforces remote DNS resolution over SOCKS5 (`socks5h://`) so your local IP address is never exposed.
- **🚨 Threat Intelligence Feeds:** Queries live blacklists (such as Abuse.ch / URLhaus) for active phishing, C2, and malware host reports.
- **🔍 Domain Trust & Risk Heuristics:** Automatically calculates domain age, flags brand-new disposable scam domains (< 90 days), and evaluates high-risk TLDs.
- **📜 SSL & Telemetry Inspection:** Examines SSL handshakes, HTTP response codes, and server headers securely over encrypted circuits.

---

## 📦 System Requirements

Before running WebCheck, ensure your environment meets the following requirements:

- **OS:** Kali Linux, NetHunter, Termux, or any Debian-based Linux distribution
- **Python:** Python 3.8 or higher
- **Service:** Tor service daemon installed and active

### 📌 Python Dependencies
- `requests`
- `PySocks`
- `urllib3`

---

## 🚀 Installation & Setup

Copy and paste the following commands to clone the repository, install dependencies, and install `webcheck` globally:

```bash
# 1. Clone the repository
git clone git@github.com:whoami136/WEBCHECK.git
cd WEBCHECK

# 2. Install required Python packages
pip install -r requirements.txt --break-system-packages

# 3. Make the tool executable and link it globally
chmod +x webcheck.py
sudo cp webcheck.py /usr/bin/webcheck
ln -s /usr/bin/webcheck ~/webcheck
sudo systemctl start tor
webcheck {LINK}
