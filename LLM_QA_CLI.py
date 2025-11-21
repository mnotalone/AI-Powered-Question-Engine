import os
import json
import requests
from dotenv import load_dotenv
import re

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL")

# ---------------------------------------
# Text Preprocessing
# ---------------------------------------
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = " ".join(text.split())        # Remove extra spaces
    return text

# ---------------------------------------
# Send request to HuggingFace Router API
# ---------------------------------------
def ask_llm(question):
    if not HF_API_KEY:
        return "Error: HF_API_KEY is missing."

    url = "https://router.huggingface.co/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": HF_MODEL,
        "messages": [
            {"role": "user", "content": question}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        return f"Error: HF API returned {response.status_code} - {response.text}"

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except:
        return "Error: Unexpected HF API response format.\n" + json.dumps(data, indent=2)

# ---------------------------------------
# CLI Application
# ---------------------------------------
def main():
    print("LLM Q&A CLI — type 'exit' to quit\n")

    while True:
        q = input("Enter question: ").strip()
        if q.lower() == "exit":
            break

        processed = preprocess(q)
        print(f"[Processed] {processed}")

        answer = ask_llm(processed)
        print("\n[Answer]", answer, "\n")

if __name__ == "__main__":
    main()
