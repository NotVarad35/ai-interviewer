# AI DevOps Interviewer

An automated, voice-activated technical interview simulator. This application leverages local audio capture, offline text-to-speech, and the Google Gemini large language model to generate and conduct highly realistic, scenario-based DevOps interviews.

![Application Screenshot](assets/screenshot.png)

## Features

* Voice-activated continuous interview loop using SpeechRecognition.
* Local, offline text-to-speech synthesis using pyttsx3.
* Dynamic, scenario-based question generation utilizing the Google Gemini API.
* Threaded graphical user interface built with Tkinter.
* Automated SAT-style grading and evaluation report generation upon interview completion.

## Prerequisites

* Python 3.9 or higher
* Active Google Gemini API Key
* A working microphone and audio output device

## Installation

Clone the repository to your local machine:

git clone https://github.com/NotVarad35/ai-interviewer.git
cd ai-interviewer

Create a virtual environment and install the required dependencies:

pip install SpeechRecognition
pip install faster-whisper
pip install google-genai
pip install pyttsx3

## Usage

Execute the AI Interviewer GUI or AI Interviewer CLI main application file:

python main.py

Upon launching, the application will prompt you to securely enter your Google Gemini API key. Click "Start Interview" to begin the continuous evaluation loop. Press "D" or click the "Done & Grade" button to terminate the interview and receive your quantitative assessment.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
