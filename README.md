# AI Interviewer

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent, voice-activated technical interview simulator powered by AI. This application combines local audio processing, offline text-to-speech, and the Google Gemini API to deliver realistic, scenario-based DevOps and technical interviews with automated grading and detailed performance evaluation.

![Application Screenshot](assets/screenshot.png)

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [GUI Mode](#gui-mode)
  - [CLI Mode](#cli-mode)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contributing](#contributing)

---

## Features

✨ **Core Capabilities:**

- 🎙️ **Voice-Activated Interview Loop** - Real-time speech recognition powered by Faster-Whisper for accurate transcription
- 🔊 **Offline Text-to-Speech** - Local TTS synthesis using pyttsx3 (no external API calls required)
- 🤖 **AI-Powered Question Generation** - Dynamic, scenario-based technical questions via Google Gemini API
- 🎨 **Dual Interface** - Choose between intuitive GUI (Tkinter) or lightweight CLI
- ⚡ **Multi-threaded Architecture** - Responsive interface with background processing
- 📊 **Automated Assessment** - SAT-style grading and comprehensive evaluation reports
- 🔐 **Secure API Key Management** - Secure input handling for Google Gemini credentials

---

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.9 or higher** ([Download](https://www.python.org/downloads/))
- **Google Gemini API Key** ([Get one here](https://ai.google.dev/))
- **Audio Hardware** - Working microphone and speaker/headphone output
- **Operating System** - Windows, macOS, or Linux with audio support

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/NotVarad35/ai-interviewer.git
cd ai-interviewer
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install SpeechRecognition
pip install faster-whisper
pip install google-genai
pip install pyttsx3
```

---

## Quick Start

1. **Launch the Application:**

   - **GUI Mode:**
     ```bash
     python "AI Interview GUI.py"
     ```

   - **CLI Mode:**
     ```bash
     python "AI Interview CLI.py"
     ```

2. **Enter Your API Key** - When prompted, securely provide your Google Gemini API key

3. **Begin Interview** - Click "Start Interview" (GUI) or follow CLI prompts

4. **End & Grade** - Press `D` or click "Done & Grade" to complete the interview and receive your assessment

---

## Usage

### GUI Mode

The graphical interface provides an intuitive experience for interview candidates:

```bash
python "AI Interview GUI.py"
```

**Features:**
- Real-time interview status display
- Easy-to-use start/stop controls
- Live transcription display
- Comprehensive grading report upon completion

### CLI Mode

Perfect for developers and those preferring terminal-based interaction:

```bash
python "AI Interview CLI.py"
```

**Features:**
- Lightweight and fast
- Piped input/output support
- Scriptable for batch testing
- Detailed console logging

---

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root to pre-configure settings:

```env
GEMINI_API_KEY=your_api_key_here
INTERVIEW_DURATION=30
VOICE_ENGINE=pyttsx3
```

### Custom Interview Settings

Edit interview parameters in the application files:

- **Question Difficulty** - Modify LLM prompt instructions
- **Interview Duration** - Adjust timeout settings
- **Voice Speed** - Configure text-to-speech rate
- **Professional Domain** - Specify DevOps, Backend, Frontend, etc.

---

## Architecture

```
ai-interviewer/
├── AI Interview GUI.py          # Tkinter-based graphical interface
├── AI Interview CLI.py          # Command-line interface
├── prototype/
│   ├── phase1_audio.py         # Audio capture & processing
│   ├── phase2_transcription.py # Speech-to-text conversion
│   └── phase3_llm.py           # LLM integration & question generation
└── assets/
    └── screenshot.png          # UI preview image
```

---

## Troubleshooting

### Common Issues

**Issue: "No microphone detected"**
- Verify audio device is connected and enabled in system settings
- Check audio drivers are up to date
- Run with elevated permissions if necessary

**Issue: "API Key authentication failed"**
- Confirm API key is valid and active
- Ensure API is enabled in Google Cloud Console
- Check internet connectivity

**Issue: "Transcription is inaccurate"**
- Ensure microphone is close to your mouth (6-12 inches)
- Reduce background noise in recording environment
- Speak clearly and at normal pace

**Issue: Application crashes on startup**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.9+)
- Try reinstalling: `pip install --force-reinstall google-genai`

---

## Future Enhancements

- [ ] Interview question bank database
- [ ] Multiple technical domains (DevOps, Backend, Frontend, etc.)
- [ ] Video interview recording capability
- [ ] Performance analytics dashboard
- [ ] Candidate feedback generation

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

Please ensure your code follows PEP 8 standards and includes appropriate documentation.

---

## Support

Have questions or issues? 

- 📧 Open an [Issue](https://github.com/NotVarad35/ai-interviewer/issues) on GitHub
- 💬 Check existing discussions for common solutions
- 📝 Review the [Troubleshooting](#troubleshooting) section

---

**Made by [NotVarad](https://github.com/NotVarad35)**
