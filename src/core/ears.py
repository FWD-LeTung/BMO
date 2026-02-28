import os
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
from faster_whisper import WhisperModel


class BMOEars:
    def __init__(self, model_size: str ="tiny.en", device ="cpu", compute_type="int8"):
        self.model = WhisperModel(model_size,
                                  device=device,
                                  compute_type=compute_type
                                  )
        self.sample_rate = 16000
        self.duration = 5

    def record(self):
        recording = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32"
        )
        sd.wait()
        return recording.flatten()
    
    def transcribe(self, audio):
        segments, info = self.model.transcribe(audio, beam_size=1, language="en")

        full_text = ""
        for segment in segments:
            full_text += segment.text

        return full_text
    
    def listen(self):
        audio = self.record()
        text = self.transcribe(audio=audio)
        if not text:
            print("BMO không nghe thấy gì cả")
            return
        else:
            print(f"BMO nghe thấy: {text}")
        return text

if __name__ == "__main__":
    ears = BMOEars()
    print("Bắt đầu nghe trong 5s:...")
    ears.listen()