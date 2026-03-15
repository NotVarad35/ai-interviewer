import speech_recognition as sr

def test_audio_capture():
    # 1. Initialize the Recognizer
    r = sr.Recognizer()

    # 2. Set the pause threshold to 3 seconds for the interview scenario
    r.pause_threshold = 3.0

    print("Initializing microphone...")
    # 3. Use the default microphone as the audio source
    with sr.Microphone(device_index=1) as source:
        print("Calibrating for ambient noise... Please stay quiet for a second.")
        r.adjust_for_ambient_noise(source, duration=1)
        
        print("\nReady! Read your Homelab script. Then, stay silent for 3 seconds.")
        # audio_data is captured here
        audio_data = r.listen(source)
        
        print("\nAudio capture complete!")

    # --- NEW CODE: SAVE AUDIO TO FILE ---
    filename = "recorded_audio.wav"
    print(f"\nSaving the recorded audio to '{filename}'...")
    
    # Retrieve the raw WAV bytes from the AudioData object
    wav_bytes = audio_data.get_wav_data()
    
    # Open a file in write-binary ("wb") mode and write the bytes
    with open(filename, "wb") as f:
        f.write(wav_bytes)
        
    print("File saved successfully!")

if __name__ == "__main__":
    test_audio_capture()