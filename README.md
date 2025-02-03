# AutoRC - Autonomous RC Car Project 🚗💨

AutoRC is an open-source Raspberry Pi-based **RC car framework** designed to help build **autonomous vehicles** using Raspberry Pi, Pygame, and Pigpio.

## **✨ Features**
- ✅ **Raspberry Pi-based** control with `Pygame`
- ✅ **Pigpio** for PWM motor control
- ✅ **Camera recording** with `PiRecording.py`
- ✅ **Modular and Extendable** for AI & ML features
- ✅ **Systemd support** for auto-start on boot

---

## **⚙️ Setup Instructions**

### **1️ Clone this Repository**
Open a terminal on your Raspberry Pi and run:

```bash
git clone https://github.com/YOUR_USERNAME/AutoRC.git
cd AutoRC
```

### **2️ Install Dependencies**
Make sure your system is up to date and install the required libraries:

```bash
sudo apt update
sudo apt install -y python3-pigpio python3-pygame
```

### **3️ Enable `pigpiod` (Required for PWM Control)**
Start the **Pigpio daemon** and enable it to start at boot:

```bash
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

### **4️ Run the Program**
Execute the RC Car program manually:

```bash
python3 src/PiCarDriving.py
```

---

## ** Setting Up Auto Start with Systemd**
To **automatically start AutoRC on boot**, follow these steps:

### **1️ Create a Systemd Service**
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
ExecStart=/usr/bin/python3 /home/pi/AutoRC/src/PiCarDriving.py
WorkingDirectory=/home/pi/AutoRC
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi
Environment="PATH=/usr/bin:/usr/local/bin"

[Install]
WantedBy=multi-user.target
```
**Note:** Make sure the paths match your actual file locations! User match your Pi user name!

### **2️ Enable and Start the Service**
Run:
```bash
sudo systemctl daemon-reload
sudo systemctl enable autorc.service
sudo systemctl start autorc.service
```

### **3️ Check the Service Status**
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

## ** Contributing**
Developer can modify and extend the `src/` files to add **new features** like:
- 🏆 **Obstacle Avoidance** 
- 🤠 **Self-driving AI** 
- 🎤 **Voice-Controlled RC Car**

---

## ** License**
This project is licensed under the **MIT License**.

---

## ** Support & Contact**
If you have any issues, contact us via **zhaos98@mcmaster.ca**; **maginnit@mcmaster.ca**.

---


