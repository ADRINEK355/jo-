import logging
import socket
import time
import os
import threading
from threading import Thread

# --- SEKCJA BOTA DISCORD ---
# Wejdź na Discord Developer Portal, stwórz bota i wklej jego TOKEN poniżej
TOKEN = 'MTQ2NjE1MzgxMDY5NDI0NjUxMw.GYmMwf.z6gMFFfRFO_SaTC_tQOoqx9v2wKlE818dZncWI' 

import discord
from discord.ext import commands

# Konfiguracja bota
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 BOT DISCORD ONLINE: {bot.user}')
    await bot.change_presence(activity=discord.Game(name="Brawlix v2 | !status"))

@bot.command()
async def status(ctx):
    # Pokazuje status serwera na Discordzie
    await ctx.send(f"✅ **Serwer Brawlix v26 jest ONLINE!**\n👥 Aktywni gracze: {Server.ThreadCount}\n🏆 Admin Adix wbił właśnie kolejną 35 rangę!")

@bot.command()
async def news(ctx):
    await ctx.send("📢 **NEWS:** 8 Marca wielki event: **Bazar Tary!** Nowe skiny dla Emz i Jessie!")

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
        # Importy z Twoich plików Logic
        try:
            from Logic.Device import Device
            from Logic.Player import Players
            self.device = Device(self.client)
            self.player = Players(self.device)
        except ImportError:
            print("[ERROR] Nie znaleziono folderu Logic (Device.py / Player.py)!")

    def recvall(self, length: int):
        data = b''
        while len(data) < length:
            s = self.client.recv(length)
            if not s:
                break
            data += s
        return data

    def run(self):
        # Import bazy pakietów
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

                # Rozłączanie przy braku aktywności (10 sekund)
                if time.time() - last_packet > 10:
                    print(f"[INFO] IP {self.address[0]} rozłączone (timeout).")
                    self.client.close()
                    Server.ThreadCount -= 1
                    break
        except Exception:
            self.client.close()
            Server.ThreadCount -= 1

# --- URUCHAMIANIE WSZYSTKIEGO ---
if __name__ == '__main__':
    # 1. Odpalamy serwer Brawl Stars w tle (osobny wątek)
    bs_server = Server('0.0.0.0', 9339)
    server_thread = threading.Thread(target=bs_server.start)
    server_thread.daemon = True
    server_thread.start()

    # 2. Odpalamy bota Discord (to trzyma skrypt przy życiu)
    if TOKEN != 'TUTAJ_WKLEJ_TWOJ_TOKEN_BOTA':
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"❌ Błąd bota Discord: {e}")
            # Jeśli bot nie działa, serwer i tak będzie działał dzięki tej pętli:
            while True:
                time.sleep(1)
    else:
        print("⚠️ Nie wkleiłeś TOKENU bota! Serwer BS działa, ale bot Discord jest wyłączony.")
        while True:
            time.sleep(1)