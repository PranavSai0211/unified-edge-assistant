# 🧰 Hardware Setup Guide for Unified Edge Assistant

This guide helps you set up the required hardware to run your Edge AI Assistant on a Raspberry Pi or other Single Board Computer (SBC).

---

## 🖥️ Recommended SBCs
- **Raspberry Pi 4** (4GB or 8GB)
- Jetson Nano (for GPU-accelerated workloads)
- Rock Pi (with Ubuntu/Debian-based OS)

---

## 🎤 Audio Hardware
- **USB Microphone**: Plug-and-play (e.g., Fifine, Blue Snowball)
- **Speaker/3.5mm Audio Out**: For TTS responses

## 🎥 Camera
- USB webcam or Pi Camera Module
- Required for face/object detection with OpenCV

---

## 📟 Sensors (Optional but Recommended)

### 1. DHT22 - Temperature & Humidity
**Wiring:**
- VCC → 3.3V or 5V
- GND → GND
- Data → GPIO4 (or any digital pin)
- Pull-up resistor (4.7kΩ) between VCC and Data

### 2. PIR Motion Sensor
**Wiring:**
- VCC → 5V
- OUT → GPIO17
- GND → GND

### 3. Relay Module (for automation)
**Wiring:**
- IN → GPIO (e.g., GPIO18)
- VCC → 5V
- GND → GND
- Connect load (light, fan) to relay terminals

---

## 🪛 GPIO Control (Python)
Use `RPi.GPIO` or `gpiozero` libraries to control relays, lights, or read sensor data.

```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)  # Turn ON
```

---

## ⚙️ Software Preparation
```bash
sudo apt update && sudo apt install python3-pip python3-opencv espeak libespeak1
pip install
