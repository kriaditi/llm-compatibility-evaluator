import os
import re
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from llm_wrapper import call_mistral
from collections import Counter
from input_handler import get_all_text, get_all_images
from image_caption import generate_tagged_picture_insights
from PIL import Image
import pytesseract
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load BLIP model once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def remove_redundant_lines(text: str) -> str:
    """
    Removes repetitive lines, empty lines, and near-duplicates.
    """
    lines = text.splitlines()
    seen = set()
    result = []
    for line in lines:
        cleaned = line.strip()
        if cleaned and cleaned.lower() not in seen:
            result.append(cleaned)
            seen.add(cleaned.lower())
    return "\n".join(result)

def extract_keywords(text: str, top_k=8) -> list:
    """Extracts capitalized keywords from text for professional insight."""
    words = re.findall(r'\b[A-Z][a-zA-Z]+\b', text)
    common = Counter(words).most_common(top_k)
    return [word for word, _ in common]

def extract_text_from_image(image_path: str) -> str:
    """Extracts raw text from an image using OCR."""
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f" Error reading image: {e}"

def clean_extracted_text(text: str) -> str:
    """Removes irrelevant lines commonly found in UI screenshots (e.g., LinkedIn headers)."""
    lines = text.splitlines()
    cleaned = [
        line for line in lines
        if line.strip() and not line.lower().startswith((
            "start a conversation", "highlights", "activity", "chat", 
            "message", "liked your photo", "posts", "images", "profile"
        ))
    ]
    return "\n".join(cleaned).strip()

def summarize_profile_text(text: str) -> str:
    """Summarizes the cleaned text using Mistral."""
    if len(text.strip()) < 50:
        return "No valid summary content found."

    prompt = f"""
You are summarizing a user's professional profile or dating bio extracted from an image.

Summarize the following text in 3–5 lines. Focus on tone, subject matter, and clarity.

Avoid referencing UI elements or social platform context.

Text:
{text}
"""
    return call_mistral(prompt)

def get_profile_summary(folder_path: str) -> str:
    """
    Returns a merged summary from all .txt and image files in a folder.
    Combines cleaned OCR content and text summarization for prompt use.
    """
    from input_handler import get_all_text, get_all_images
    from image_caption import generate_tagged_picture_insights

    # 1. Get and clean text
    merged_text = get_all_text(folder_path)
    if merged_text.strip() and merged_text != "No text files found.":
        text_summary = summarize_profile_text(merged_text)
    else:
        text_summary = ""

    # 2. Extract and clean image-based text
    image_files = get_all_images(folder_path)
    extracted_from_images = []
    for img in image_files:
        raw = extract_text_from_image(img)
        cleaned = clean_extracted_text(raw)
        if cleaned:
            extracted_from_images.append(cleaned)

    if extracted_from_images:
        combined_img_text = "\n".join(extracted_from_images)
        image_summary = summarize_profile_text(combined_img_text)
    else:
        image_summary = ""

    # 3. Caption/tag images
    if image_files:
        picture_insight = generate_tagged_picture_insights(folder_path)
    else:
        picture_insight = "No pictures provided."

    # 4. Merge everything into one final summary
    summary_block = f"""
{text_summary}

{image_summary}

Picture Vibes:
{picture_insight}
""".strip()

    return summary_block

def get_linkedin_summary(folder_path: str) -> str:
    """
    Uses OCR on screenshots + optional .txt file in the folder.
    Summarizes into a clean, professional LinkedIn-style paragraph.
    """

    all_texts = []

    # 1. Add .txt file content (if available)
    txt_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".txt")]
    for txt_file in txt_files:
        try:
            with open(os.path.join(folder_path, txt_file), "r", encoding="utf-8") as f:
                all_texts.append(f.read().strip())
        except:
            continue

    # 2. OCR all images (jpg/png)
    img_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    for img_file in img_files:
        try:
            raw = extract_text_from_image(os.path.join(folder_path, img_file))
            cleaned = clean_extracted_text(raw)
            if cleaned:
                all_texts.append(cleaned)
        except:
            continue

    # 3. Merge all into one block
    combined = "\n".join(all_texts).strip()

    if not combined:
        return "No LinkedIn information available."

    # 4. Summarize with Mistral
    prompt = f"""
    The following text is extracted from a LinkedIn profile via OCR and/or uploaded text:

    {combined}

    Summarize this profile professionally.
    Focus on job title, company, education, and relevant expertise.
    Output should be short, polished, and LinkedIn-ready.
    """

    try:
        summary = call_mistral(prompt).strip()
        return summary
    except Exception as e:
        return f" Failed to summarize LinkedIn profile: {e}"

def get_dating_bio_summary(folder_path: str) -> str:
    """
    Uses OCR on images and any .txt files to generate a concise dating bio summary
    using Mistral for contextual understanding.
    """
    all_texts = []

    # 1. Load all .txt files
    txt_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".txt")]
    for txt_file in txt_files:
        try:
            with open(os.path.join(folder_path, txt_file), "r", encoding="utf-8") as f:
                all_texts.append(f.read().strip())
        except:
            continue

    # 2. OCR all image files
    img_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    for img_file in img_files:
        try:
            raw = extract_text_from_image(os.path.join(folder_path, img_file))
            cleaned = clean_extracted_text(raw)
            if cleaned:
                all_texts.append(cleaned)
        except:
            continue

    # 3. Merge all text (prioritizing OCR context)
    combined = "\n".join(all_texts).strip()

    if not combined:
        return "No dating profile info found."

    # 4. Summarize using Mistral
    prompt = f"""
    The following text is extracted from a dating profile via OCR or text:

    {combined}

    Summarize the user's dating profile in a concise, informative way.
    Focus on intent, personality, and important lifestyle facts.
    """

    try:
        summary = call_mistral(prompt).strip()
        return summary
    except Exception as e:
        return f" Failed to summarize dating bio: {e}"

