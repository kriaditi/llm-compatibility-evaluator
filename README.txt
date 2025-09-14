TITLE OF THE WORK:

#LLM-Based Compatibility Evaluator
AI-powered compatibility analysis from preferences, bios, chats, and pictures.
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

DESCRIPTION:
An AI-powered system that evaluates compatibility between two people using preferences, bios, chats, and pictures.
It combines LLM reasoning, OCR, behavioral analysis, and time-aware scoring to produce structured compatibility reports.

Features
Preference Matching → Compares user’s dealbreakers and must-haves against the other profile.
Bio & LinkedIn Analysis → Summarizes education, career, and intent from text or screenshots (OCR).
Chat Analysis → Extracts tone, maturity, ghosting patterns, and consistency from conversations.
Behavioral Scoring → Evaluates emotional availability, wit, grammar, maturity, and overall vibe.
Time-Aware Scoring → Detects ghosting, engagement decay, love-bombing, and reply quickness.
Picture Insights + Vibe Check → Captions photos and tags them as Explorer, Fitness, Chill, Corporate, etc.
Structured Report → Red flags, compatibility %, preference breakdown, and final verdict.

Advantages
Holistic → Goes beyond bios by combining preferences + chats + images.
Explainable → Instead of black-box answers, it breaks down scores and reasoning.
Scalable → Works with text, screenshots, or multiple data sources.
Customizable → Preferences are fully user-defined (preferences.json).
Offline-first → Supports local LLMs (Mistral / Phi via Ollama) for privacy and control.

---

GETTING STARTED:

To run the project:

1. Clone or unzip the project folder.
2. Add your inputs under the /data folder:
   - /linkedin/ → pictures or .txt
   - /dating_app/ → screenshots or .txt
   - /chats/ → screenshots or chat transcripts
   - /pictures/ → profile vibe pictures
   - preferences.json → your custom criteria
3. Run Final_Script.ipynb using Jupyter Lab or Notebook.

---

INSTALLING:

# Create environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# (Manual) Install Ollama for local LLM inference:
# https://ollama.ai
ollama run mistral

---

EXECUTION DETAILS:

To run compatibility analysis:

Step 1. Place all user-specific input files in their respective folders.
Step 2. Run Final_Script.ipynb (pipeline) from notebook. (Make sure Ollama is installed (for running local LLMs like Mistral).)
jupyter lab notebook/final_script.ipynb
Step 3. The notebook will:

1. Load preferences (preferences.json)
2. Summarize LinkedIn & Dating Bio (text + OCR)
3. Parse chats (text + screenshots) and summarize
4. Apply time-aware scoring and behavioral scoring
5. Add any personal notes for the person (if any)
6. Analyze profile pictures (vibe tagging)
7. Fill the GPT prompt
8. Generate final compatibility verdict
9. Save result as report_TIMESTAMP.md and update history.json (can be used later for fine-tuning purpose)
Note: No internet or cloud model is needed. Model used: Mistral (via Ollama)

Outputs:

reports/report_YYYY-MM-DD.md → Human-readable report
results/history.json → Structured logs (future fine-tuning dataset)

---

INPUT & OUTPUT EXAMPLES

Sample Inputs:
1. preferences.json
{
  "preferences": {
    "personality_traits": ["tall", "emotionally available", "mature", "witty"],
    "intent": "long-term relationship",
    "income_min": 1000000,
    "substance_use": { "smoking": "no", "alcohol": "no", "drugs": "no" }
  }
}

2. chat.txt
You: Hey, how was your day?
Him: Not bad, lots of meetings. What about you?
You: Gym and then work.
Him: You’re so consistent. I admire that.

3. linkedin.txt or profile image (OCR detected):
Senior Consultant at Anthology
MBA – IIM Udaipur | B.Tech – MIT
Based in Hyderabad


Sample Output:

{
  "compatibility_score": 82,
  "red_flags": ["Delayed replies noticed", "Intent not clearly expressed"],
  "match_breakdown": {
    "emotionally_available": 7,
    "income_match": 10,
    "intent_alignment": 6,
    "wit": 8
  },
  "behavior_scores": {
    "tone": 8,
    "emotional_availability": 6,
    "wit": 7,
    "love_bombing": 4,
    "comment": "Warm tone, but emotionally reserved and inconsistent."
  },
  "time_scores": {
    "ghosting_score": 6,
    "engagement_decay": "medium",
    "quickness_score": 5,
    "consistency_score": 6,
    "comment": "Pauses in reply, then bursts. Signs of slow disengagement."
  },
  "verdict": "Pause",
  "gpt_advice": "He’s friendly but unclear. You can ask directly — or pull back."
}

---

Future Insights
Fine-Tuning (LoRA/QLoRA) → Train a lightweight model on 10+ personal profiles to reduce prompt size and personalize results.
Pattern Recognition → Identify recurring patterns (e.g., ghosting trends, communication mismatches) across multiple matches.
Interactive GPT Layer → Suggest real-time chat responses to improve engagement.
Deeper Image Understanding → Profile picture clustering & pattern matching (explorer vs. fitness vibes).
Web App / GUI → Upload preferences + profiles and instantly get a compatibility report.

---

AUTHOR DETAILS:

Aditi Kumari
https://www.linkedin.com/in/aditi-kumari1996/ 
AI/ML Enthusiast | Building with LLMs
Open to collaborations, contributions, and feedback.
Country: India
Date of Completion: July 2025

---

NATURE OF WORK:

- Original software logic (written in Python)
- Custom prompts for GPT/LLM reasoning
- Behavioral + time-aware scoring modules
- Data formatting and visualization of AI-generated compatibility evaluations

---

PROGRAMMING LANGUAGE / TOOLS:

- Python 3.x
- Local LLM (Mistral via Ollama)
- Hugging Face Transformers
- Jupyter Notebook
- Tesseract OCR
- OpenCV / PIL

---

RIGHTS & LICENSE:

This project is released under the MIT License.
You are free to use, modify, and distribute it, with attribution.

---

FILES INCLUDED:

/data/
  /linkedin/
    profile.txt
    profile1.png
  /dating_app/
    bio.txt
    bio1.jpg
  /chats/
    chat1.txt
    chat2.png
preferences.json
/utils/
  behavior_scoring.py
  time_scoring.py
  image_to_text.py
  image_caption.py
  input_handler.py
  llm_wrapper.py
  gpt_utils.py
/notebook/
	Final_Script.ipynb
/prompts/
	match_prompt.txt
/reports/ (sample)
/results/ (sample)
README.txt
requirements.txt

---
