from llm_wrapper import call_mistral
import json
import re

from llm_wrapper import call_mistral
import json
import re

def extract_json_scores(text: str) -> dict:
    try:
        match = re.search(r"{.*}", text, re.DOTALL)
        return json.loads(match.group()) if match else {}
    except:
        return {}

def analyze_behavior(chat_text: str) -> dict:
    """
    Analyzes chat for tone, emotional availability, wit, and love bombing.
    Returns scores from 0–10 and an objective comment.
    """

    prompt = f"""
You are a sharp, clinical relationship behavior analyst.

Evaluate the following chat log between two people. For each metric, give a score from 0–10 (where 10 is very high) and a short explanation.

- tone: How warm, respectful, and human is the conversation?
- emotional_availability: Does either person show vulnerability or emotionally intelligent replies?
- wit: Are replies clever, playful, humorous?
- love_bombing: Any signs of intense affection followed by silence or emotional drop?

Then provide a short objective comment about behavioral patterns.

Chat:
{chat_text}

Return your response in strict JSON format like:
{{
  "tone": 8,
  "emotional_availability": 7,
  "wit": 6,
  "love_bombing": 9,
  "comment": "He complimented a lot in early chats then ghosted twice. Signs of inconsistency despite emotional clarity."
}}
"""

    try:
        response = call_mistral(prompt)
        return extract_json_scores(response)
    except Exception as e:
        print(" Error in behavior scoring:", e)
        return {}
