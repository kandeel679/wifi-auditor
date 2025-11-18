import subprocess
import platform
import ipaddress
import socket
import threading
import time
import speedtest
from datetime import datetime
from queue import Queue
from colorama import Fore, Style, init

# Initialize color output
init(autoreset=True)

class WiFiSecurityAnalyzer:
    def __init__(self):
        self.os_type = platform.system()
        self.report_log = []
        self.live_hosts = []
        
    def log(self, message, level="INFO"):
        """Helper to print and store logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if level == "INFO":
            print(f"[{timestamp}] {Fore.GREEN}[INFO]{Style.RESET_ALL} {message}")
        elif level == "ALERT":
            print(f"[{timestamp}] {Fore.RED}[ALERT]{Style.RESET_ALL} {message}")
        elif level == "DATA":
            print(f"[{timestamp}] {Fore.CYAN}[DATA]{Style.RESET_ALL} {message}")
        
        self.report_log.append(f"[{timestamp}] [{level}] {message}")

    def get_local_ip(self):
        """Finds the local IP address and Subnet"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Doesn't allow actual connection, just helps determine interface
            s.connect(('8.8.8.8', 1))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = '127.0.0.1'
        finally:
            s.close()
        return local_ip

    def site_survey(self):
        """
        PHASE 1: Site Survey
        Uses OS commands to see what wifi networks are around.
        This replaces 'Monitor Mode' by using the standard Wi-Fi card scan.
        """
        self.log("Starting Site Survey (Visible Networks)...")
        try:
            if self.os_type == "Windows":
                # Windows command to show networks with signal strength and BSSID
                cmd = ["netsh", "wlan", "show", "networks", "mode=bssid"]
            else:
                # Linux command (requires nmcli)
                cmd = ["nmcli", "dev", "wifi"]
            
            output = subprocess.check_output(cmd, universal_newlines=True)
            
            # Basic parsing to look for open networks
            if "Open" in output or "insecure" in output.lower():
                self.log("Found potentially insecure/open networks in range!", "ALERT")
            
            self.log(f"\n--- RAW SURVEY DATA ---\n{output}\n-----------------------", "DATA")
            
        except Exception as e:
            self.log(f"Error running site survey: {e}", "ALERT")

    def ping_host(self, ip):
        """Helper function to ping a single host"""
        # -n 1 for Windows, -c 1 for Linux
        param = '-n' if self.os_type == 'Windows' else '-c'
        command = ['ping', param, '1', str(ip)]
        
        # Suppress output to keep console clean
        response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if response == 0:
            return True
        return False

    def network_scan(self):
        """
        PHASE 2: Network Scanning / Host Discovery
        Scans the current subnet for other devices.
        """
        local_ip = self.get_local_ip()
        self.log(f"Your IP is: {local_ip}")
        
        # Assume /24 subnet for simplicity
        network_prefix = '.'.join(local_ip.split('.')[:-1])
        self.log(f"Scanning subnet: {network_prefix}.0/24 for active devices...")
        
        lock = threading.Lock()
        
        def scan_worker(ip_end):
            target_ip = f"{network_prefix}.{ip_end}"
            if self.ping_host(target_ip):
                with lock:
                    try:
                        # Try to resolve hostname
                        hostname = socket.gethostbyaddr(target_ip)[0]
                    except:
                        hostname = "Unknown"
                    
                    self.log(f"Host Found: {target_ip} ({hostname})", "INFO")
                    self.live_hosts.append((target_ip, hostname))

        # Using threads to make the scan faster
        threads = []
        for i in range(1, 255):
            t = threading.Thread(target=scan_worker, args=(i,))
            threads.append(t)
            t.start()
            # Slight delay to prevent flooding network card
            time.sleep(0.01) 
        
        for t in threads:
            t.join()

        self.log(f"Scan Complete. Found {len(self.live_hosts)} devices.")

    def performance_analysis(self):
        """
        PHASE 3: Performance Analysis
        Checks internet bandwidth to identify bottlenecks.
        """
        self.log("Starting Performance Analysis (Bandwidth Test)...")
        self.log("Please wait, this takes about 20 seconds...", "INFO")
        
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            
            download_speed = st.download() / 1_000_000 # Convert to Mbps
            upload_speed = st.upload() / 1_000_000 # Convert to Mbps
            ping = st.results.ping
            
            self.log(f"Download: {download_speed:.2f} Mbps", "DATA")
            self.log(f"Upload:   {upload_speed:.2f} Mbps", "DATA")
            self.log(f"Latency:  {ping} ms", "DATA")
            
            if download_speed < 5:
                self.log("Bandwidth is critically low! Potential bottleneck or interference.", "ALERT")
                
        except Exception as e:
            self.log(f"Could not run speedtest: {e}", "ALERT")

    def save_report(self):
        filename = f"Wifi_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as f:
            for line in self.report_log:
                f.write(line + "\n")
        print(f"\n{Fore.YELLOW}Report saved to {filename}{Style.RESET_ALL}")

if __name__ == "__main__":
    tool = WiFiSecurityAnalyzer()
    
    print(f"{Fore.YELLOW}=== Wi-Fi Security & Performance Analyzer ==={Style.RESET_ALL}")
    print("Mode: Internal Auditor (Managed Mode)\n")
    
    # 1. Run Site Survey
    tool.site_survey()
    print("-" * 30)
    
    # 2. Run Network Scan
    tool.network_scan()
    print("-" * 30)
    
    # 3. Run Performance Test
    tool.performance_analysis()
    print("-" * 30)
    
    # 4. Save Data
    tool.save_report()