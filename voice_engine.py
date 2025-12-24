import pyttsx3
import whisper
import sounddevice as sd
import numpy as np
import queue
import sys

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print(f"AI: {text}")
    engine.say(text)
    engine.runAndWait()

print("Loading Whisper model... (this happens only once)")
model = whisper.load_model("base") 

def listen():
    q = queue.Queue()
    
    def callback(indata, frames, time, status):
        if status: print(status, file=sys.stderr)
        q.put(indata.copy())

    print("\nListening... (Speak now)")
    duration = 5 
    fs = 16000 
    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        sd.sleep(int(duration * 1000))
        
    audio_data = []
    while not q.empty():
        audio_data.append(q.get())
    
    data = np.concatenate(audio_data, axis=0).flatten()
    data = data.astype(np.float32)
    
    result = model.transcribe(data)
    text = result['text'].strip()
    print(f"You said: {text}")
    return text