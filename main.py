import logging
import socket
import time
import os
import threading
from threading import Thread

# --- KLASA SERWERA BRAWL STARS ---
class Server:
    Clients = {"ClientCounts": 0, "Clients": {}}
    ThreadCount = 0

    def __init__(self, ip: str, port: int):
        self.server = socket.socket()
        self.port = port
        self.ip = ip

    def start(self):
        # Próba załadowania konfiguracji
        try:
            from Utils.Config import Config
            if not os.path.exists('./config.json'):
                print("[INFO] Tworzenie pliku config.json...")
                Config.create_config(self)
        except ImportError:
            print("[WARNING] Folder Utils/Config.py nie został znaleziony!")

        # Bindowanie serwera
        try:
            self.server.bind((self.ip, self.port))
            print(f'[INFO] Serwer Brawl Stars ruszył! Ip: {self.ip}, Port: {self.port}')
            
            while True:
                self.server.listen()
                client, address = self.server.accept()
                print(f'[INFO] Nowe połączenie z IP: {address[0]}')
                ClientThread(client, address).start()
                Server.ThreadCount += 1
        except Exception as e:
            print(f"[ERROR] Nie można odpalić serwera: {e}")

# --- KLASA OBSŁUGI GRACZA ---
class ClientThread(Thread):
    def __init__(self, client, address):
        super().__init__()
        self.client = client
        self.address = address
        try:
            from Logic.Device import Device
            from Logic.Player import Players
            self.device = Device(self.client)
            self.player = Players(self.device)
        except ImportError:
            print("[ERROR] Nie znaleziono folderu Logic!")

    def recvall(self, length: int):
        data = b''
        while len(data) < length:
            s = self.client.recv(length)
            if not s:
                break
            data += s
        return data

    def run(self):
        try:
            from Packets.LogicMessageFactory import packets
        except ImportError:
            print("[ERROR] Nie znaleziono folderu Packets!")
            return

        last_packet = time.time()
        try:
            while True:
                header = self.client.recv(7)
                if len(header) > 0:
                    last_packet = time.time()
                    packet_id = int.from_bytes(header[:2], 'big')
                    length = int.from_bytes(header[2:5], 'big')
                    data = self.recvall(length)

                    if packet_id in packets:
                        print(f'[INFO] Odebrano pakiet Id: {packet_id}')
                        message = packets[packet_id](self.client, self.player, data)
                        message.decode()
                        message.process()
                    else:
                        print(f'[INFO] Pakiet nieznany: {packet_id}')

                if time.time() - last_packet > 10:
                    self.client.close()
                    Server.ThreadCount -= 1
                    break
        except Exception:
            self.client.close()
            Server.ThreadCount -= 1

# --- URUCHAMIANIE ---
if __name__ == '__main__':
    # Serwer rusza na porcie 9339 (lub takim, jaki przydzieli hosting)
    # Na Renderze warto sprawdzić zmienną środowiskową PORT
    port = int(os.environ.get("PORT", 9339))
    bs_server = Server('0.0.0.0', port)
    print(f"[SYSTEM] Startowanie na porcie: {port}")
    bs_server.start()