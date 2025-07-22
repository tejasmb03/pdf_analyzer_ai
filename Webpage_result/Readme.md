# 📄 AI PDF Content Analyzer Web App

This is a Flask-based web application that allows users to upload educational PDFs (such as Olympiad sample papers), extract text and images, and generate AI-based multiple-choice questions (MCQs) using the BLIP image captioning model.

---

## 🚀 Features

- ✅ Upload a PDF from the browser
- ✅ Extract all **text** and **images** from each page
- ✅ Use **BLIP AI model** to caption images
- ✅ Convert captions into **MCQ-style questions**
- ✅ View results directly on the page
- ✅ Download structured results as a JSON file

---

## 📸 Preview

<img src="https://github.com/yourusername/pdf-analyzer-ai/raw/main/demo_screenshot.png" alt="screenshot" width="600">

---

## 🧠 How It Works

1. User uploads a PDF via a web form
2. Server extracts text and images using `PyMuPDF`
3. Each image is passed through the BLIP model to generate captions
4. Captions are used to create multiple-choice questions
5. The output is shown on the page and downloadable as a JSON file

---

## 📦 Requirements

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows

## Install dependencies:

pip install -r requirements.txt

## How to run 

Python app.py