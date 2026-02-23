import sounddevice as sd
import soundfile as sf
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

def test_microphone_basic():
    print("\nBMO's mic checking...")
    try:
        device = sd.query_devices()
        default_input = sd.default.device[0]
        print("BMO is listening.")
        return True
    except Exception as e:
        print(f"BMO is deaf: {e}!!!")
        return False
    
def test_record_and_play(duration = 5):
    print(f"Talk something in {duration} seconds... ")
    try:
        recording = sd.rec(int(duration*16000),
                           samplerate=16000,
                           channels=1,
                           dtype='int16')
        sd.wait()
        print("Done Recording!")
        
        output_file = Path("data/recording/test_raw.wav")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        print("Saving...")
        sf.write(str(output_file), recording, 16000)
        print(f"\nSave test recording at: {output_file}")
        print("\nPlayback what BMO heard...")
        sd.play(recording, 16000)
        sd.wait()
        print("\nDone!")

        return recording
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def main():
    print("-"*50)
    print("BMO - Microphone Checking")
    print("-"*50)

    if not test_microphone_basic():
        print("Microphone not working!")
        return
    
    test_record_and_play(5)
    print("\n"+ "-"*50)
    print("End of testing.")

if __name__ == "__main__":
    main()
