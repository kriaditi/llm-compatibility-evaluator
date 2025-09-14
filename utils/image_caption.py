import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

from llm_wrapper import call_mistral

def tag_vibe(caption: str) -> str:
    """Tag vibe based on keywords in the caption, fallback to LLM if undefined."""
    caption_lower = caption.lower()
    
    if any(word in caption_lower for word in ["mountain", "trail", "backpack", "hike", "snow"]):
        return " Explorer"
    elif any(word in caption_lower for word in ["gym", "weights", "fitness", "workout", "muscle"]):
        return " Fitness"
    elif any(word in caption_lower for word in ["suit", "office", "formal", "tie", "desk"]):
        return " Corporate"
    elif any(word in caption_lower for word in ["beach", "surf", "sunset", "relax"]):
        return " Chill"
    elif any(word in caption_lower for word in ["mirror", "selfie", "bathroom", "glasses"]):
        return " Selfie-heavy"
    else:
        # Fallback to LLM-generated vibe
        prompt = f"Suggest a one- or two-word vibe label (emoji + short description) for this image caption:\n'{caption}'"
        vibe = call_mistral(prompt).strip()
        return vibe

def generate_tagged_picture_insights(folder_path: str) -> str:
    """Generate caption + vibe tag for each image and return formatted summary."""
    insights = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, file)
            try:
                image = Image.open(image_path).convert('RGB')
                inputs = processor(images=image, return_tensors="pt")
                output = model.generate(**inputs)
                caption = processor.decode(output[0], skip_special_tokens=True)
                vibe = tag_vibe(caption)
                insights.append(f"- {file}: {caption} → **{vibe}**")
            except Exception as e:
                insights.append(f"- {file}: [Error processing image: {e}]")

    return "\n".join(insights) if insights else "No pictures provided."
