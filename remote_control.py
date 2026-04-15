import telebot
import os
import subprocess
import time
import pyperclip
import threading
import requests
import datetime

# ===== Telegram Config =====
AUTHORIZED_USER_ID = Your_chat_id_here
TOKEN = "Your_bot_token_here"
bot = telebot.TeleBot(TOKEN)
location_sent = False
# ===== Network Photo Capture =====
IMAGE_PATH = "/home/shubham/intruder_photos/intruder.jpg"
DELAY = 7  # seconds after network detected

def capture_photo():
    folder = "/home/shubham/intruder_photos"

    if not os.path.exists(folder):
        os.makedirs(folder)

    timestamp = int(time.time())
    image_path = f"{folder}/intruder_{timestamp}.jpg"

    command = f"fswebcam -d /dev/video0 -r 1280x720 --no-banner {image_path}"
    os.system(command)

    print("Saved photo:", image_path)

def send_all_saved_photos():
    folder = "/home/shubham/intruder_photos"

    if not os.path.exists(folder):
        return

    for file in os.listdir(folder):
        if file.endswith(".jpg"):
            path = os.path.join(folder, file)

            try:
                with open(path, "rb") as photo:
                    bot.send_photo(AUTHORIZED_USER_ID, photo)

                os.remove(path)

            except Exception as e:
                print("Failed to send:", file)

def internet_available():
    try:
        requests.get("https://api.telegram.org", timeout=5)
        return True
    except:
        return False

def auto_send_photos():
    global location_sent

    while True:
        if internet_available():
            send_all_saved_photos()
            send_saved_ssid()
        time.sleep(30)

# ===== Audio Recording =====
def record_audio():
    audio_path = "/home/shubham/audio_test.mp3"
    os.system(f"ffmpeg -f pulse -i default -t 15 -y {audio_path}")
    with open(audio_path, "rb") as audio:
        bot.send_audio(AUTHORIZED_USER_ID, audio)
    os.remove(audio_path)


# ===== Audio Command =====
@bot.message_handler(commands=['record'])
def record_command(message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        bot.reply_to(message, "Unauthorized access 🚫")
        return
    bot.reply_to(message, "Recording audio for 15 seconds 🎙")
    threading.Thread(target=record_audio).start()


# ===== Shutdown =====
@bot.message_handler(commands=['shutdown'])
def shutdown_pc(message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        bot.reply_to(message, "Unauthorized access 🚫")
        return
    bot.reply_to(message, "Shutting down now 🔴")
    os.system("systemctl poweroff")


# ===== Startup Message =====
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "PC is online and connected!")


def get_wifi_routers():
    routers = []

    try:
        result = subprocess.check_output(
            "nmcli -t -f SSID,BSSID,SIGNAL dev wifi",
            shell=True
        ).decode()

        for line in result.split("\n"):
            if line:
                parts = line.split(":")
                ssid = parts[0]
                bssid = parts[1].replace("\\", "")
                signal = int(parts[2])

                routers.append({
                    "macAddress": bssid,
                    "signalStrength": signal
                })

        return routers

    except Exception as e:
        print("WiFi scan error:", e)
        return []

def get_ip_location():
    try:
        response = requests.get("https://ipapi.co/json/")
        data = response.json()

        city = data.get("city")
        region = data.get("region")
        country = data.get("country_name")
        lat = data.get("latitude")
        lon = data.get("longitude")
        ip = data.get("ip")

        return city, region, country, lat, lon, ip

    except:
        return None, None, None, None, None, None
def get_location(routers):
    try:
        url = "https://location.services.mozilla.com/v1/geolocate?key=test"

        data = {
            "wifiAccessPoints": routers
        }

        response = requests.post(url, json=data)
        result = response.json()

        lat = result["location"]["lat"]
        lon = result["location"]["lng"]

        return lat, lon

    except Exception as e:
        print("Location error:", e)
        return None, None

def send_location():
    routers = get_wifi_routers()

    if routers:
        lat, lon = get_location(routers)

        if lat and lon:
            message = f"""
Laptop Location Detected (WiFi Triangulation)

Latitude: {lat}
Longitude: {lon}

Map:
https://maps.google.com/?q={lat},{lon}
"""

            bot.send_message(AUTHORIZED_USER_ID, message)
            return

    # fallback to IP location
    city, region, country, lat, lon, ip = get_ip_location()

    if lat and lon:
        message = f"""
Laptop Location Detected (IP Based)

IP: {ip}
City: {city}
Region: {region}
Country: {country}

Map:
https://maps.google.com/?q={lat},{lon}
"""

def monitor_wifi():
    last_ssid = None

    while True:
        try:
            result = subprocess.check_output(
                "nmcli -t -f ACTIVE,SSID dev wifi",
                shell=True
            ).decode()

            current_ssid = None

            for line in result.split("\n"):
                if line.startswith("yes"):
                    current_ssid = line.split(":")[1]

            # If new connection detected
            if current_ssid and current_ssid != last_ssid:
                last_ssid = current_ssid

                if internet_available():
                    bot.send_message(
                        AUTHORIZED_USER_ID,
                        f"New WiFi Connected:\n{current_ssid}"
                    )
                else:
                    # save for later
                    with open(SSID_FILE, "w") as f:
                        f.write(current_ssid)

        except Exception as e:
            print("WiFi monitor error:", e)

        time.sleep(10)

        bot.send_message(AUTHORIZED_USER_ID, message)
# ===== Start Bot =====
time.sleep(25)
capture_photo()
if internet_available():
    send_location()
threading.Thread(target=auto_send_photos, daemon=True).start()
threading.Thread(target=monitor_wifi, daemon=True).start()
bot.infinity_polling()

