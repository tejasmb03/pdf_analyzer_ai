from flask import Flask, render_template, request, send_file
import os
import json
import fitz  # PyMuPDF
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
IMAGES_FOLDER = "static/images"  # use static folder so images can be viewed in HTML
OUTPUT_JSON = "extracted_content.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGES_FOLDER, exist_ok=True)

# Load BLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🧠 Loading BLIP on {device}...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

def generate_caption(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt").to(device)
        out = model.generate(**inputs)
        return processor.decode(out[0], skip_special_tokens=True)
    except Exception as e:
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

def analyze_pdf(pdf_path):
    result = []
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()

        image_paths = []
        ai_questions = []

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_ext = base_image["ext"]
            image_path = f"{IMAGES_FOLDER}/page{page_num+1}_image{img_index+1}.{image_ext}"

            with open(image_path, "wb") as f:
                f.write(base_image["image"])
            image_paths.append(image_path)

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

    with open(OUTPUT_JSON, "w", encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return result

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "pdf" not in request.files:
        return "No file uploaded", 400
    pdf_file = request.files["pdf"]
    if pdf_file.filename == "":
        return "No selected file", 400

    file_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(file_path)
    result = analyze_pdf(file_path)
    return render_template("index.html", result=result)

@app.route("/download")
def download():
    return send_file(OUTPUT_JSON, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
