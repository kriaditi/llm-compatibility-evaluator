import re
from llm_wrapper import call_mistral
import json

def extract_json_scores(text: str) -> dict:
    import re, json
    try:
        match = re.search(r"{.*}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return {}

def extract_time_gaps(chat: str) -> str:
    """
    Extracts simple gaps in replies based on timestamps.
    Assumes timestamps are in format like: (9:24 AM), (3:46 PM)
    """
    time_pattern = re.findall(r"\((\d{1,2}:\d{2}\s?[APMapm]{2})\)", chat)
    return f"Found {len(time_pattern)} timestamps. Sample: {time_pattern[:5]}"

def summarize_gaps_for_model(chat: str) -> str:
    """
    Extracts timestamps and first 30 characters of each line.
    Prepares a shortened engagement log for GPT to analyze time-based patterns.
    """
    lines = chat.strip().splitlines()
    short_lines = []
    for line in lines:
        line = line.strip()
        match = re.search(r"\b(\d{1,2}:\d{2}\s?[APMapm]{2})\b", line)
        timestamp = match.group(1) if match else ""
        short_lines.append(f"{timestamp} - {line[:30]}")

    short_log = "\n".join(short_lines[-40:])  # Keep last 40 messages max
    return short_log


def analyze_timing(chat: str) -> dict:
    log = summarize_gaps_for_model(chat)

    prompt = f"""
You are analyzing texting patterns between two people.

This is a chat log summary (timestamp + start of message):
{log}

Please assess:
- ghosting_score (0–10): Does either person vanish or delay replies significantly?
- engagement_decay (low/medium/high): Did the enthusiasm or rhythm fade?
- consistency_score (0–10): Were responses paced evenly?
- quickness_score (0–10): Were replies fast?
- comment: What stands out in this timing pattern?

Return valid JSON.
"""

    try:
        response = call_mistral(prompt)
        return extract_json_scores(response)
    except Exception as e:
        print(" Error in time analysis:", e)
        return {}
