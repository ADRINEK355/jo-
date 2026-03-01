import socket
import time
import os
import threading
from threading import Thread
from flask import Flask
from pyngrok import ngrok

# --- 1. KONFIGURACJA FLASK (Oszukujemy Rendera, że jesteśmy stroną WWW) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Serwer Brawl Stars jest LIVE na Renderze przez Ngrok!"

def run_flask():
    # Render wymaga, abyśmy słuchali na porcie z ich zmiennej środowiskowej
    render_port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=render_port)

# --- 2. KLASA SERWERA BRAWL STARS (Twoja logika gry) ---
class Server:
    Clients = {"ClientCounts": 0, "Clients": {}}
    ThreadCount = 0

    def __init__(self, ip: str, port: int):
        self.server = socket.socket()
        self.port = port
        self.ip = ip

    def start(self):
        # Próba załadowania konfiguracji (jeśli masz foldery Utils/Config)
        try:
            from Utils.Config import Config
            if not os.path.exists('./config.json'):
                print("[INFO] Tworzenie pliku config.json...", flush=True)
                Config.create_config(self)
        except Exception:
            pass

        # Bindowanie serwera gry
        try:
            self.server.bind((self.ip, self.port))
            print(f'[INFO] Serwer Gry BS słucha na porcie: {self.port}', flush=True)
            
            while True:
                self.server.listen()
                client, address = self.server.accept()
                print(f'[INFO] Nowe połączenie z IP: {address[0]}', flush=True)
                ClientThread(client, address).start()
                Server.ThreadCount += 1
        except Exception as e:
            print(f"[ERROR] Problem z socketem gry: {e}", flush=True)

# --- 3. KLASA OBSŁUGI GRACZA ---
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
        except Exception:
            pass

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
        except Exception:
            return

        try:
            while True:
                header = self.client.recv(7)
                if len(header) > 0:
                    packet_id = int.from_bytes(header[:2], 'big')
                    length = int.from_bytes(header[2:5], 'big')
                    data = self.recvall(length)

                    if packet_id in packets:
                        print(f'[INFO] Pakiet odebrany: {packet_id}', flush=True)
                        message = packets[packet_id](self.client, self.player, data)
                        message.decode()
                        message.process()
                else:
                    break
        except Exception:
            pass
        finally:
            self.client.close()
            Server.ThreadCount -= 1

# --- 4. URUCHAMIANIE WSZYSTKIEGO ---
if __name__ == '__main__':
    # A. Startujemy Flaska w osobnym wątku (wymagane przez Render)
    threading.Thread(target=run_flask, daemon=True).start()

    # B. Uruchamiamy NGROK (Twój Bypass na 20%)
    try:
        # TWÓJ TOKEN: 5M57D5G5WPCNRJ3XP4DOIUHGROLAPK2E
        ngrok.set_auth_token("5M57D5G5WPCNRJ3XP4DOIUHGROLAPK2E")
        
        # Tworzymy tunel TCP na port gry 9339
        tunnel = ngrok.connect(9339, "tcp")
        
        print("\n" + "="*50, flush=True)
        print(f"BYPASS AKTYWNY!", flush=True)
        print(f"ADRES DO GRY: {tunnel.public_url}", flush=True)
        print("="*50 + "\n", flush=True)
    except Exception as e:
        print(f"[NGROK ERROR] Nie udało się odpalić tunelu: {e}", flush=True)

    # C. Startujemy serwer gry na porcie 9339 (Lokalnie wewnątrz Rendera)
    bs_server = Server('0.0.0.0', 9339)
    bs_server.start()