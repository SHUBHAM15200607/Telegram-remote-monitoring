import time
import os
import requests

# ====== YOUR TELEGRAM DETAILS ======
BOT_TOKEN = "Your_bot_token_here"
CHAT_ID = "Your_chat_id"

# ====== SETTINGS ======
IMAGE_PATH = "intruder.jpg"
DELAY = 7   # seconds (change between 5-10 if you want)

def capture_photo():
    os.system(f"fswebcam -r 1920x1080 --jpeg 95 --no-banner {IMAGE_PATH}")

def send_photo():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(IMAGE_PATH, "rb") as photo:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": photo})

def main():
    time.sleep(DELAY)
    capture_photo()
    send_photo()

if __name__ == "__main__":
    main()
