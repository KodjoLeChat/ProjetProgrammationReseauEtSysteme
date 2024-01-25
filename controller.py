import subprocess
import re
import time

def capture_and_print_subnet():
    command = ["sudo","./ip_clear"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

    # List to store the captured IP addresses
    captured_ips = set()

    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                match = re.match(r'IP Address: (\S+)', output)
                if match:
                    ip_address = match.group(1)
                    if ip_address not in captured_ips:
                        print(ip_address)
                        captured_ips.add(ip_address)
            time.sleep(1)  # Adjust the sleep duration as needed
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C to exit the loop gracefully

    process.terminate()
    process.wait()

    return list(captured_ips)

if __name__ == "__main__":
    captured_ips = capture_and_print_subnet()
    print("Captured IPs in Python script:", captured_ips)
