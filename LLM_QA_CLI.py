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

if __name__ == "__main__":
    main()
