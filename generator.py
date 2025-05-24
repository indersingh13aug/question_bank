# app/llm/generator.py

import docx
import PyPDF2
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# HUGGINGFACEHUB_ACCESS_TOKEN='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'
# GEMINI_API_KEY='AIzaSyDd-JR1M20_vGgCtf0LYCEy1p5YFsDy1ts'
ACCESS_TOKEN = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={ACCESS_TOKEN}"

def read_file(file):
    filepath = file.name

    if filepath.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    elif filepath.endswith('.docx'):
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])

    elif filepath.endswith('.pdf'):
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    else:
        return "Unsupported file format."

def generate_mcq(file, complexity, content_type):
    print(file)
    content = read_file(file)

    if not content.strip():
        return "File is empty or could not extract content."

    # API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={ACCESS_TOKEN}"
    headers = {
        # "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"The following is a {content_type}. Generate 5 multiple choice questions with {complexity} complexity:\n\n"
        f"{content}\n\n"
        f"Format:\n"
        f"1. Question text?\n  a) Option A\n  b) Option B\n  c) Option C\n  d) Option D\nAnswer: <correct option>\n"
    )

    # payload = {
    #     "inputs": f"User: {prompt}\nAssistant:",
    #     "parameters": {
    #         "max_new_tokens": 800,
    #         "temperature": 0.7
    #     }
    # }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        # return result[0]['generated_text'].strip().split('Assistant:')[1]
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

def summarize_text(file, word_limit=100, content_type="general"):

    content = read_file(file)
    print(file)

    if not content.strip():
        return "File is empty or could not extract content."

    # API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

    headers = {
        # "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = f"""
        You are an expert in summarizing {content_type.lower()} content.
        Summarize the following text in approximately {word_limit} words. Keep the tone and terminology suitable for the {content_type} domain.

        Text:
        {content}

        Summary:
        """
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        # return result[0]['generated_text'].strip()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"


