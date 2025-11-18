# 📡 Wi-Fi Security & Performance Analyzer (Prototype)

### 🔍 Overview
**Wi-Fi Security Analyzer** is a Python-based network assessment tool designed to audit wireless networks from the perspective of a connected client ("Internal Auditor"). 

Unlike traditional hacking tools that require hardware-dependent **Monitor Mode**, this tool operates entirely in **Managed Mode**. It utilizes active scanning, system-level calls, and bandwidth stress-testing to fulfill security availability requirements, detect bottlenecks, and map connected devices.

This project demonstrates how to perform a **Site Survey**, **Vulnerability Check**, and **Performance Analysis** using standard hardware constraints.

### 🚀 Key Features
* **Site Survey & Spectrum Analysis:** Scans the local environment for visible SSIDs, signal strength (RSSI), and encryption standards to identify channel interference and insecure networks.
* **Active Host Discovery:** Performs a multi-threaded IP ping sweep (subnet scan) to identify all live devices connected to the network (IoT, mobile, workstations).
* **Performance & Bottleneck Detection:** Integrates `speedtest-cli` to measure real-time latency, upload, and download throughput to identify network degradation.
* **Automated Reporting:** Generates a timestamped text log (`.txt`) of the audit, suitable for creating Wi-Fi area maps or compliance reports.
* **Cross-Platform Compatibility:** Detects the OS (Windows/Linux) and adjusts system commands (`netsh` vs `nmcli`) automatically.

### 🛠️ How It Works
This tool bypasses the need for raw packet capture (Monitor Mode) by utilizing the **Post-Connection** attack surface:
1. **Reconnaissance:** Queries the OS network interface to scrape visible BSSID data.
2. **Enumeration:** Uses the `socket` and `subprocess` libraries to map the `/24` subnet.
3. **Availability Testing:** Stresses the network connection to ensure it meets availability standards.

### 📦 Prerequisites
* Python 3.x
* Network connection (Wi-Fi)

### ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/wifi-security-analyzer.git](https://github.com/YOUR_USERNAME/wifi-security-analyzer.git)
   cd wifi-security-analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install speedtest-cli colorama
   ```

3. **Run the tool:**
   ```bash
   python wifi_auditor.py
   ```

### ⚠️ Disclaimer
*This tool is for educational purposes and authorized network auditing only. Ensure you have permission to scan the network you are connected to.*
