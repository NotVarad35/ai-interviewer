import os
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
import speech_recognition as sr
from google import genai
import pyttsx3

# os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

class InterviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Interviewer")
        self.root.geometry("1280x720")

        self.interview_history = []
        self.is_interviewing = False

        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 16), state=tk.DISABLED)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(root, text="Status: Ready", font=("Arial", 20,"bold"), fg="blue")
        self.status_label.pack(pady=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.start_btn = tk.Button(button_frame, text="Start Interview", font=("Arial", 20), bg="green", fg="white", command=self.start_interview_thread)
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.grade_btn = tk.Button(button_frame, text="Done & Grade (Press D)", font=("Arial", 20), bg="red", fg="white", state=tk.DISABLED, command=self.trigger_grading)
        self.grade_btn.pack(side=tk.LEFT, padx=10)

        self.root.bind('<d>', lambda event: self.trigger_grading())
        self.root.bind('<D>', lambda event: self.trigger_grading())
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            self.root.withdraw()
            api_key = simpledialog.askstring("API Key Required", "Please paste your Google Gemini API Key:\n(Visit https://aistudio.google.com to get your key if you don't have one already)", show='*')
            if api_key:
                os.environ["GEMINI_API_KEY"] = api_key.strip()
                self.root.deiconify()
            else:
                self.root.destroy()

    def update_chat(self, speaker, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{speaker}\n{message}\n\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def update_status(self, status_text, color):
        self.status_label.config(text=f"Status: {status_text}", fg=color)

    def start_interview_thread(self):
        self.start_btn.config(state=tk.DISABLED, bg="gray")
        self.grade_btn.config(state=tk.NORMAL)
        self.is_interviewing = True
        self.update_chat("--- SYSTEM ---", "Initializing Interview...")
        threading.Thread(target=self.run_interview_loop, daemon=True).start()

    def trigger_grading(self):
        if self.is_interviewing:
            self.is_interviewing = False
            self.update_status("Calculating Score...", "red")
            self.grade_btn.config(state=tk.DISABLED, bg="gray")
            threading.Thread(target=self.generate_report, daemon=True).start()

    def generate_report(self):
        try:
            client = genai.Client()
            transcript = "\n\n".join(self.interview_history)
            
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
            
            response = client.models.generate_content(model='gemini-2.5-flash', contents=grading_prompt)
            self.update_chat("--- FINAL GRADE REPORT ---", response.text)
            self.update_status("Interview Complete. Check your score!", "blue")
            
        except Exception as e:
            self.update_chat("--- ERROR ---", str(e))

    def run_interview_loop(self):
        try:
            client = genai.Client()
            engine = pyttsx3.init()
            engine.setProperty('rate', engine.getProperty('rate') - 20) 
            r = sr.Recognizer()
            r.pause_threshold = 3.0 
        except Exception as e:
            self.update_chat("--- ERROR ---", str(e))
            return

        candidate_transcript = (
            "In my current homelab setup, I'm running a Proxmox cluster across three bare-metal nodes. "
            "I've segregated my network using pfSense... For storage, I have a TrueNAS virtual machine... "
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

        self.update_status("AI is Thinking...", "orange")
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_1)
            current_question = response.text.replace("*", "").replace("#", "")
        except Exception as e:
            self.update_chat("--- ERROR ---", str(e))
            return

        with sr.Microphone() as source: 
            self.update_status("Calibrating Microphone...", "orange")
            r.adjust_for_ambient_noise(source, duration=1)
            
            while self.is_interviewing:
                self.update_status("AI is Speaking...", "purple")
                self.update_chat("--- AI INTERVIEWER ---", current_question)
                
                engine.say(current_question)
                engine.runAndWait() 
                
                if not self.is_interviewing:
                    break

                self.update_status("LISTENING... (Speak now, pause 3s to finish)", "green")
                try:
                    audio_data = r.listen(source, timeout=10, phrase_time_limit=None)
                except sr.WaitTimeoutError:
                    continue 
                except Exception:
                    break 
                    
                self.update_status("TRANSCRIBING...", "orange")
                try:
                    candidate_answer = r.recognize_faster_whisper(audio_data, model="base")
                    self.update_chat("--- YOU ---", candidate_answer)
                    
                    if not candidate_answer or candidate_answer.isspace():
                        continue
                        
                    self.interview_history.append(f"QUESTION:\n{current_question}\n\nCANDIDATE ANSWER:\n{candidate_answer}\n")
                        
                except sr.UnknownValueError:
                    self.update_chat("--- SYSTEM ---", "Whisper could not understand audio. Try again.")
                    continue
                except Exception as e:
                    self.update_chat("--- ERROR ---", str(e))
                    break

                self.update_status("THINKING...", "orange")
                
                prompt_2 = f"""You are an expert IT interviewer. 
                You just asked: "{current_question}"
                Candidate answered: "{candidate_answer}"
                
                Evaluate the answer. If strong, generate a harder scenario. If weak, ask a fundamental follow-up.
                Acknowledge their answer briefly. ONLY output what you will say next.
                
                RULES:
                1. Be incredibly concise. Keep your entire response under 4 sentences.
                2. DO NOT use markdown formatting, asterisks, or bullet points. Speak in plain conversational text.
                """
                
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_2)
                    current_question = response.text.replace("*", "").replace("#", "")
                except Exception as e:
                    self.update_chat("--- ERROR ---", str(e))
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = InterviewApp(root)
    root.mainloop()