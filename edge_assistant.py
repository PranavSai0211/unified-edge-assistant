import queue
import sounddevice as sd
import json
import pyttsx3
import cv2
import numpy as np
from vosk import Model, KaldiRecognizer
import threading
import time
import random  # Used to simulate sensor data

# Initialize TTS
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Initialize voice recognizer
model = Model(model_name="vosk-model-small-en-us-0.15")  # Download from vosk.ai
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()

# Audio stream thread
def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))

# Start audio stream
def listen_loop():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🎤 Listening for wake word...")
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower()
                if "assistant" in text:
                    speak("Yes, how can I help you?")
                    command_loop()

# Handle commands
def command_loop():
    timeout = time.time() + 10  # 10 seconds window to speak
    while time.time() < timeout:
        data = audio_queue.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower()
            print("User:", text)

            if "face" in text or "camera" in text:
                detect_face()
                break
            elif "temperature" in text:
                sensor_temperature()
                break
            elif "light on" in text:
                speak("Turning the light on.")
                # GPIO.output(light_pin, GPIO.HIGH)
                break
            elif "light off" in text:
                speak("Turning the light off.")
                # GPIO.output(light_pin, GPIO.LOW)
                break
            elif "bye" in text:
                speak("Goodbye.")
                break
            else:
                speak("I didn't understand. Try again.")
                break

# Face detection
def detect_face():
    speak("Opening camera to detect face.")
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
                                         'haarcascade_frontalface_default.xml')

    detected = False
    start = time.time()
    while time.time() - start < 10:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            detected = True

        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    if detected:
        speak("Face detected successfully.")
    else:
        speak("No face detected.")

# Simulated sensor
def sensor_temperature():
    temp = round(random.uniform(20.0, 40.0), 2)
    print(f"Sensor Reading: {temp} °C")
    if temp > 35:
        speak(f"Warning! High temperature detected: {temp} degrees.")
    else:
        speak(f"Current temperature is {temp} degrees.")

# Start assistant
if __name__ == "__main__":
    speak("Edge Assistant Ready.")
    threading.Thread(target=listen_loop, daemon=True).start()
    while True:
        time.sleep(1)
