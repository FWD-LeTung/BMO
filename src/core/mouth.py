import sounddevice as sd
import numpy as np
import os
import sys
from piper import PiperVoice
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
class BMOMouth:
    def __init__(self, model: str, config: str):
        self.voice = PiperVoice.load(model, config)
        self.sample_rate = self.voice.config.sample_rate
    def speak(self, text: str):
        if not text:
            return
        print("BMO đang nói")
        audio_buffer = []
        for chunk in self.voice.synthesize(text):
            audio_data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            audio_buffer.append(audio_data)
            sample_rate = chunk.sample_rate

        if audio_buffer:
            full_audio = np.concatenate(audio_buffer)       
            sd.play(full_audio, sample_rate)
            sd.wait() 

if __name__ == "__main__":
    MODEL = "models/tts/en_GB-semaine-medium.onnx"
    CONFIG = "models/tts/en_GB-semaine-medium.onnx.json"
    

    if not os.path.exists(MODEL):
        print(f"LỖI: Không tìm thấy file model tại {MODEL}")
    else:
        mouth = BMOMouth(MODEL, CONFIG)
        mouth.speak("Hello, I'm Beemoh, How are you today Finn")