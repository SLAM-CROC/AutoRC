# AutoRC - Autonomous RC Car Project 🚗💨

AutoRC is an open-source Raspberry Pi-based **RC car framework** designed to help students build **autonomous vehicles** using Raspberry Pi, Pygame, and Pigpio.

## **✨ Features**
- ✅ **Raspberry Pi-based** control with `Pygame`
- ✅ **Pigpio** for PWM motor control
- ✅ **Camera recording** with `PiRecording.py`
- ✅ **Modular and Extendable** for AI & ML features
- ✅ **Systemd support** for auto-start on boot

---

## **⚙️ Setup Instructions**

### **1️⃣ Clone this Repository**
Open a terminal on your Raspberry Pi and run:

```bash
git clone https://github.com/YOUR_USERNAME/AutoRC.git
cd AutoRC
```

### **2️⃣ Install Dependencies**
Make sure your system is up to date and install the required libraries:

```bash
sudo apt update
sudo apt install -y python3-pigpio python3-pygame
```

### **3️⃣ Enable `pigpiod` (Required for PWM Control)**
Start the **Pigpio daemon** and enable it to start at boot:

```bash
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

### **4️⃣ Run the Program**
Execute the RC Car program manually:

```bash
python3 src/PWMDriving.py
```

---

## **🛠️ Setting Up Auto Start with Systemd**
To **automatically start AutoRC on boot**, follow these steps:

### **1️⃣ Create a Systemd Service**
Run:
```bash
sudo nano /etc/systemd/system/autorc.service
```
Paste the following content:
```ini
[Unit]
Description=AutoRC - Autonomous RC Car Service
After=network.target pigpiod.service

[Service]
ExecStart=/usr/bin/python3 /home/pi/AutoRC/src/PWMDriving.py
WorkingDirectory=/home/pi/AutoRC
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi
Environment="PATH=/usr/bin:/usr/local/bin"

[Install]
WantedBy=multi-user.target
```
**Note:** Make sure the paths match your actual file locations!

### **2️⃣ Enable and Start the Service**
Run:
```bash
sudo systemctl daemon-reload
sudo systemctl enable autorc.service
sudo systemctl start autorc.service
```

### **3️⃣ Check the Service Status**
To verify if it's running:
```bash
sudo systemctl status autorc.service
```

To restart:
```bash
sudo systemctl restart autorc.service
```

To stop:
```bash
sudo systemctl stop autorc.service
```

---

## **🧑‍💻 Contributing**
Students can modify and extend the `src/` files to add **new features** like:
- 🏆 **Obstacle Avoidance** (Using ultrasonic or LiDAR sensors)
- 🤠 **Self-driving AI** (Machine learning integration)
- 🎤 **Voice-Controlled RC Car** (Using speech recognition)

---

## **📝 License**
This project is licensed under the **MIT License**.

---

## **📩 Support & Contact**
If you have any issues, open a GitHub **issue** or contact me via **[GitHub Discussions](https://github.com/YOUR_USERNAME/AutoRC/discussions)**.

---

## **🚀 Let's Build the Future of RC Cars!**
Happy coding! 🤖💡

