# 📄 AI-Based PDF Content Analyzer with Image Question Generation

This Python script processes a PDF containing educational content (e.g., Olympiad papers), extracts all text and images from each page, and generates AI-based image questions using the BLIP (Bootstrapped Language Image Pretraining) model by Salesforce.

---

## 🚀 Features

- ✅ Extracts **text** from each PDF page
- ✅ Extracts and saves **images** from the PDF
- ✅ Uses **BLIP** to caption each image
- ✅ Converts captions into **multiple-choice questions**
- ✅ Outputs a structured **JSON file** with all extracted content and questions

---

## 🧠 How It Works

1. Reads the PDF (`sample.pdf`)
2. Iterates over each page
3. Extracts:
   - Text content
   - Images (saved as `.png`, `.jpeg`, etc.)
4. Passes each image through the **BLIP AI model**
5. Constructs MCQ-style questions from the captions
6. Saves output to:
   - `images/` folder (image files)
   - `extracted_content.json` (results)

---

## 🧩 Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt

---

## How to run the file

python app.py
