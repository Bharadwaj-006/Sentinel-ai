from scapy.all import sniff, IP
import sqlite3
from datetime import datetime

# connect database
conn = sqlite3.connect("attacks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attacks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ip TEXT,
attack_type TEXT,
timestamp TEXT
)
""")

packet_count = {}

def detect_packet(packet):

    if packet.haslayer(IP):

        ip = packet[IP].src

        # ignore external internet servers
        if not ip.startswith("10.") and not ip.startswith("192.168"):
            return

        packet_count[ip] = packet_count.get(ip, 0) + 1

        # trigger alert if packet burst detected
        if packet_count[ip] > 50:

            print(f"🚨 ATTACK DETECTED from {ip}")

            cursor.execute(
                "INSERT INTO attacks (ip, attack_type, timestamp) VALUES (?, ?, ?)",
                (ip, "Suspicious Traffic", str(datetime.now()))
            )

            conn.commit()

            packet_count[ip] = 0


def start_sniff():

    print("Monitoring network traffic...")
    sniff(prn=detect_packet, iface="en0", store=False)


start_sniff()
