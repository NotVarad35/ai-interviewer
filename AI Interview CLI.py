import os
import speech_recognition as sr
from google import genai
import pyttsx3

# os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

def main_interview_loop():
    print("Visit https://aistudio.google.com to get your Google Gemini API Key if you don't have one already.")
    api_key =input("API Key Required, Please paste your Google Gemini API Key here: ").strip()
    if api_key.startswith("AIza") and len(api_key) == 39:
        os.environ["GEMINI_API_KEY"] = api_key.strip()
    elif not api_key:
        print("API Key is required to proceed.")
        return
    else:
        print("API Key is invalid. Please provide a valid Google Gemini API Key.")
        return
    os.environ["GEMINI_API_KEY"] = api_key.strip()
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Failed to initialize Gemini Client. Error: {e}")
        return

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 20)

    r = sr.Recognizer()
    r.pause_threshold = 3.0

    interview_history = []

    print("=====================================================")
    print(" SYSTEM: Initializing Interview. Generating Scenario...")
    print("=====================================================\n")

    candidate_transcript = (
        "In my current homelab setup, I'm running a Proxmox cluster across three bare-metal nodes. "
        "I've segregated my network using pfSense... For storage, I have a TrueNAS "
        "virtual machine... I host most of my services using Docker, exposed via Traefik. "
        "Lately, I've been expanding my setup with Jellyfin, Immich, and the full ARR stack, "
        "but I'm running into permission denied errors with my TrueNAS SMB shares."
    )

    prompt_1 = f"""You are an expert IT technical interviewer evaluating a senior professional. 
    Based on the following transcript, generate one highly realistic, complex troubleshooting 
    scenario involving Docker volume mapping, TrueNAS permissions, and reverse proxy routing.
    End your response with a direct question asking how they would resolve it.
    
    RULES:
    1. Be incredibly concise. Keep your entire response under 4 sentences.
    2. DO NOT use markdown formatting, asterisks, or bullet points. Speak in plain conversational text.
    
    Candidate Transcript: "{candidate_transcript}"
    """

    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_1)
        current_question = response.text.replace("*", "").replace("#", "")
    except Exception as e:
        print(f"Failed to reach Gemini API: {e}")
        return

    print("SYSTEM: Calibrating microphone for background noise...\n")
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        
        while True:
            print("\n--- AI INTERVIEWER ---")
            print(current_question)
            print("----------------------")
            
            engine.say(current_question)
            engine.runAndWait()
            
            print("\n[LISTENING... Speak your answer clearly. Pause for 3 seconds when finished.]")
            print("[Press Ctrl+C in the terminal to END the interview and get your Score]")
            
            try:
                audio_data = r.listen(source)
            except KeyboardInterrupt:
                print("\n\n[System: Interview terminated by user. Proceeding to Grading...]")
                break
                
            print("[TRANSCRIBING...]")
            try:
                candidate_answer = r.recognize_faster_whisper(audio_data, model="base")
                print(f"\n--- YOU (Transcribed) ---\n{candidate_answer}\n-------------------------")
                
                if not candidate_answer or candidate_answer.isspace():
                    continue
                
                interview_history.append(f"QUESTION:\n{current_question}\n\nCANDIDATE ANSWER:\n{candidate_answer}\n")
                
            except sr.UnknownValueError:
                print("\n[System: Whisper could not understand the audio. Please try again.]")
                continue
            except Exception as e:
                print(f"\n[System Error during transcription: {e}]")
                break

            print("[THINKING... Evaluating your answer and generating next question...]")
            
            prompt_2 = f"""You are an expert IT interviewer. 
            You just asked the candidate this scenario: "{current_question}"
            The candidate provided this verbal answer: "{candidate_answer}"
            
            Task:
            1. Evaluate the answer internally.
            2. If the answer is strong, generate a new scenario that is significantly harder or pivots to a related technology.
            3. If the answer is weak or incomplete, ask a follow-up question to test their fundamental baseline knowledge of the concepts they missed.
            4. Keep it conversational. Acknowledge their answer briefly.
            
            RULES:
            1. Be incredibly concise. Keep your entire response under 4 sentences.
            2. DO NOT use markdown formatting, asterisks, or bullet points. Speak in plain conversational text.
            ONLY output what you, the interviewer, will say next. Do not output your internal grading.
            """
            
            try:
                response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_2)
                current_question = response.text.replace("*", "").replace("#", "")
            except Exception as e:
                print(f"Failed to reach Gemini API: {e}")
                break

    if len(interview_history) > 0:
        print("\n=====================================================")
        print(" SYSTEM: Calculating your Final Grade...")
        print("=====================================================\n")
        
        transcript = "\n\n".join(interview_history)
        
        grading_prompt = f"""
        You are a strict but fair IT certification examiner. The interview is now over. 
        Here is the transcript of the questions you asked and the candidate's verbal answers:
        
        {transcript}
        
        Please provide a final grading report formatted exactly like this:
        
        FINAL SCORE: [Calculate a score out of 100 based on technical accuracy and troubleshooting logic]
        
        SCORE CALCULATION & RUBRIC: 
        [Explain step-by-step how you deducted or awarded points. Be specific about what they missed or got right in their answers.]
        
        IDEAL ANSWERS:
        [For every question asked in the transcript, provide a concise summary of what the perfect, ideal answer would have been.]
        """
        
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=grading_prompt)
            print("\n--- FINAL GRADE REPORT ---")
            print(response.text)
            print("-------------------------------\n")
            print("Interview Complete. Check your score above!")
            
        except Exception as e:
            print(f"Failed to grade interview: {e}")
    else:
        print("\nNot enough conversation data to generate a grade report. Goodbye!")

if __name__ == "__main__":
    main_interview_loop()