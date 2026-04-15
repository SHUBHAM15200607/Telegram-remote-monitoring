🚀 Telegram Remote Monitoring System

A powerful Python-based remote monitoring system that allows you to control and monitor your laptop using a Telegram bot.

---

🔥 Features

- 📸 Capture photos remotely (intruder detection)
- 🌍 Live location tracking (WiFi triangulation + IP fallback)
- 📡 Detect connected WiFi network
- 🎙 Record audio remotely
- 🔌 Shutdown system remotely
- 📤 Auto-send data when internet becomes available
- 🔐 Secure access using authorized Telegram user ID

---

🛠️ Tech Stack

- Python 🐍
- Telegram Bot API 🤖
- Linux 🐧
- OpenCV / fswebcam 📷
- Requests 🌐

---

📂 Project Structure

telegram_remote/
├── main.py
├── utils.py
├── README.md
├── .gitignore

---

⚙️ Setup Instructions

1. Clone the repository:

git clone https://github.com/SHUBHAM15200607/telegram-remote-monitoring.git
cd telegram-remote-monitoring

2. Install dependencies:

pip install -r requirements.txt

3. Add your credentials in code:

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

4. Run the script:

python main.py

---

📸 Screenshots

📍 Location Detection

<img width="225" height="500" alt="Screenshot_20260415-130846" src="https://github.com/user-attachments/assets/042909d1-af3d-44e0-8e1f-a3e2bf31033e" />


📷 Photo Capture

<img width="225" height="500" alt="Screenshot_20260415-122802" src="https://github.com/user-attachments/assets/3a9a979a-e284-40cd-b6eb-4f38bde4a23f" />


🎙 Audio Recording

<img width="225" height="500" alt="Screenshot_20260415-130410" src="https://github.com/user-attachments/assets/f448c911-a3be-47f8-84bd-044b20ca9185" />



🔌 Shutdown system remotely


<img width="225" height="500" alt="Screenshot_20260415-123042" src="https://github.com/user-attachments/assets/358c9212-82ba-4805-b641-f4998da7b400" />













<img width="225" height="173" alt="IMG_20260415_123023851 jpg" src="https://github.com/user-attachments/assets/f18b8705-7c54-4095-8dbc-029b7bc83a72" />






🔐 Security

- Only authorized users can access commands
- Token is not exposed in the repository
- Basic protection implemented against unauthorized access

---

🚀 Future Improvements

- Add live video streaming 📹
- Add face detection 🧠
- Cloud backup ☁️
- Mobile app integration 📱

---

👨‍💻 Author

Developed by Shubham Jangra

---

⭐ Show your support

If you like this project, give it a ⭐ on GitHub!
