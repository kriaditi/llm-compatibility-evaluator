import os
import json

def load_preferences(path='preferences.json'):
    """Load the user's preferences from a JSON file and return as a string."""
    with open(path, 'r') as f:
        prefs = json.load(f)
    return json.dumps(prefs, indent=2)

def load_text(path):
    """Load raw text from a given file. Returns 'Not provided' if missing."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Not provided."

def load_prompt(path='prompts/match_prompt.txt'):
    """Load the prompt template from a .txt file."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def fill_prompt(template, prefs, linkedin, bio, chats, notes, picture_insight="Not provided", behavior_block="", time_block=""):
    return template.replace("{{PREFERENCES}}", prefs)\
        .replace("{{LINKEDIN}}", linkedin)\
        .replace("{{BIO}}", bio)\
        .replace("{{CHAT}}", chats)\
        .replace("{{NOTES}}", notes)\
        .replace("{{PICTURE_INSIGHT}}", picture_insight)\
        .replace("{{BEHAVIOR_BLOCK}}", behavior_block)\
        .replace("{{TIME_BLOCK}}", time_block)
