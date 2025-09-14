import os

def get_all_text(folder, extensions=(".txt",)) -> str:
    """Reads and concatenates all text files from a folder."""
    texts = []
    if not os.path.exists(folder):
        return "No text directory found."
    for fname in os.listdir(folder):
        if fname.lower().endswith(extensions):
            try:
                with open(os.path.join(folder, fname), "r", encoding="utf-8") as f:
                    texts.append(f.read().strip())
            except Exception as e:
                print(f" Error reading {fname}: {e}")
    return "\n\n".join(texts) if texts else "No text files found."

def get_all_images(folder, extensions=(".png", ".jpg", ".jpeg")) -> list:
    """Returns all image file paths from a folder."""
    if not os.path.exists(folder):
        return []
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(extensions)]
