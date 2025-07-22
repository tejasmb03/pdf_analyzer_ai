import fitz  # PyMuPDF
import os
import json
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# === CONFIG ===
PDF_FILE = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"  # Ensure this file is in your root directory
IMAGES_DIR = "images"
OUTPUT_JSON = "extracted_content.json"

# === SETUP ===
os.makedirs(IMAGES_DIR, exist_ok=True)

# Load PDF
try:
    doc = fitz.open(PDF_FILE)
    print(f"📄 Opened PDF: {PDF_FILE}")
except Exception as e:
    print(f"❌ Failed to open PDF: {e}")
    exit(1)

# Load BLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🧠 Loading BLIP model on device: {device}")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

def generate_caption(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt").to(device)
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        print(f"⚠️ Error generating caption for {image_path}: {e}")
        return "Unable to describe this image."

def generate_mcq_from_caption(caption):
    return {
        "question": "What does this image show?",
        "caption": caption,
        "options": [
            caption,
            "A clock",
            "A grid of shapes",
            "A number sequence"
        ],
        "answer": caption
    }

# === MAIN EXTRACTION ===
result = []

for page_num in range(len(doc)):
    print(f"\n➡️ Processing Page {page_num + 1}/{len(doc)}")
    page = doc[page_num]
    text = page.get_text().strip()

    image_paths = []
    ai_questions = []

    images = page.get_images(full=True)
    print(f"   🖼️ Found {len(images)} image(s)")

    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_ext = base_image["ext"]
        image_path = f"{IMAGES_DIR}/page{page_num+1}_image{img_index+1}.{image_ext}"

        with open(image_path, "wb") as f:
            f.write(base_image["image"])
        image_paths.append(image_path)
        print(f"   📷 Saved image: {image_path}")

        # Generate caption and question
        print(f"   🔍 Generating caption for {image_path}...")
        caption = generate_caption(image_path)
        q = generate_mcq_from_caption(caption)

        ai_questions.append({
            "image": image_path,
            "question": q["question"],
            "caption": caption,
            "options": q["options"],
            "answer": q["answer"]
        })

    result.append({
        "page": page_num + 1,
        "text": text,
        "images": image_paths,
        "ai_generated_questions": ai_questions
    })

# Save JSON output
with open(OUTPUT_JSON, "w", encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(f"\n✅ PDF Analysis Complete! JSON saved to: {OUTPUT_JSON}")
print(f"📂 Extracted images saved to: {IMAGES_DIR}/")
