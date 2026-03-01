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
    # Render wymaga portu z ich zmiennej środowiskowej
    render_port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=render_port)

# --- 2. KLASA SERWERA BRAWL STARS ---
class Server:
    Clients = {"ClientCounts": 0, "Clients": {}}
    ThreadCount = 0

    def __init__(self, ip: str, port: int):
        self.server = socket.socket()
        self.port = port
        self.ip = ip

    def start(self):
        try:
            from Utils.Config import Config
            if not os.path.exists('./config.json'):
                Config.create_config(self)
        except Exception:
            pass

        try:
            self.server.bind((self.ip, self.port))
            self.server.listen()
            print(f'[INFO] Serwer Gry BS slucha na porcie: {self.port}', flush=True)
            
            while True:
                client, address = self.server.accept()
                print(f'[INFO] Nowe polaczenie z IP: {address[0]}', flush=True)
                ClientThread(client, address).start()
                Server.ThreadCount += 1
        except Exception as e:
            print(f"[ERROR] Problem z socketem gry: {e}", flush=True)

# --- 3. KLASA OBSLUGI GRACZA ---
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
            if not s: break
            data += s
        return data

    def run(self):
        try:
            from Packets.LogicMessageFactory import packets
            while True:
                header = self.client.recv(7)
                if len(header) > 0:
                    packet_id = int.from_bytes(header[:2], 'big')
                    length = int.from_bytes(header[2:5], 'big')
                    data = self.recvall(length)
                    if packet_id in packets:
                        print(f'[INFO] Odebrano pakiet: {packet_id}', flush=True)
                        message = packets[packet_id](self.client, self.player, data)
                        message.decode()
                        message.process()
                else: break
        except Exception:
            pass
        finally:
            self.client.close()
            Server.ThreadCount -= 1

# --- 4. URUCHAMIANIE ---
if __name__ == '__main__':
    # Startujemy Flask (dla Rendera)
    threading.Thread(target=run_flask, daemon=True).start()

    # Startujemy NGROK (Twój Bypass na 20%)
    try:
        # TWOJ NOWY POPRAWNY TOKEN
        token = "3AM2SpEOAUVGCESIAosveMU6VOI_7DE7kndmAhkC4KwFXCFFh"
        ngrok.set_auth_token(token)
        
        # Otwieramy tunel TCP
        tunnel = ngrok.connect(9339, "tcp")
        
        print("\n" + "="*50, flush=True)
        print(f"BYPASS AKTYWNY!", flush=True)
        print(f"ADRES DO GRY: {tunnel.public_url}", flush=True)
        print("="*50 + "\n", flush=True)
    except Exception as e:
        print(f"[NGROK ERROR] Blad tunelu: {e}", flush=True)

    # Startujemy serwer gry
    bs_server = Server('0.0.0.0', 9339)
    bs_server.start()