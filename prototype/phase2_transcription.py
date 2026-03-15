import speech_recognition as sr

def test_transcription():
    # 1. Initialize the Recognizer
    r = sr.Recognizer()
    r.pause_threshold = 3.0

    print("Initializing microphone...")
    # NOTE: If you found a specific device_index earlier, add it here: sr.Microphone(device_index=X)
    with sr.Microphone(device_index=1) as source:
        print("Calibrating for ambient noise... Please stay quiet.")
        r.adjust_for_ambient_noise(source, duration=1)
        
        print("\nReady! Speak into the microphone and then pause for 3 seconds.")
        audio_data = r.listen(source)
        
        print("\nAudio capture complete! Sending to Faster-Whisper...")

    # --- PHASE 2: TRANSCRIPTION ---
    try:
        print("Transcribing... (Note: It will download the AI model the very first time you run this)")
        
        # recognize_faster_whisper handles the raw AudioData object natively
        transcript = r.recognize_faster_whisper(
            audio_data, 
            model="base" # The "base" model is a good balance of speed and accuracy
        )
        
        print("\n--- Transcription Result ---")
        print(f"'{transcript}'")
        print("----------------------------")
        
        # A quick diagnostic check for our audio troubleshooting
        if not transcript or transcript.isspace():
            print("\n[Diagnostic] The transcript was completely blank. Your microphone recorded pure silence.")
            print("[Diagnostic] We will need to fix the Windows/Hardware mic input before moving to Phase 3.")
            
    except sr.UnknownValueError:
        print("Whisper could not understand the audio (it might be silent or too muffled).")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_transcription()