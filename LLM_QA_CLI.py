<<<<<<< HEAD
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
=======
import argparse
import os
import re
import nltk
from nltk.tokenize import word_tokenize
from openai import OpenAI

# Download NLTK data if not present
nltk.download('punkt', quiet=True)

def preprocess_question(question):
    """
    Apply basic preprocessing: lowercasing, tokenization, punctuation removal.
    """
    # Lowercasing
    question = question.lower()
    # Remove punctuation
    question = re.sub(r'[^\w\s]', '', question)
    # Tokenization
    tokens = word_tokenize(question)
    # Join back to string
    processed = ' '.join(tokens)
    return processed

def get_answer_from_llm(processed_question):
    """
    Send the processed question to OpenAI API and get the answer.
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f"Answer the following question: {processed_question}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    answer = response.choices[0].message.content.strip()
    return answer

def main():
    parser = argparse.ArgumentParser(description="Q&A CLI using LLM API")
    parser.add_argument("question", help="The question to ask")
    args = parser.parse_args()

    original_question = args.question
    processed_question = preprocess_question(original_question)

    print(f"Original Question: {original_question}")
    print(f"Processed Question: {processed_question}")

    try:
        answer = get_answer_from_llm(processed_question)
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"Error: {e}")
>>>>>>> ba52850ed498ff5ef49dfd5900aec54063f10fd4

if __name__ == "__main__":
    main()
