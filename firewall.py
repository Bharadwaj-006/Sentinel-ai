import os

def block_ip(ip):
    print(f"Blocking IP: {ip}")
    command = f"sudo pfctl -t blocked_ips -T add {ip}"
    os.system(command)
