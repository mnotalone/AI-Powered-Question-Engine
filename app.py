from flask import Flask, request, render_template
import os
import re
import nltk
from nltk.tokenize import word_tokenize
from openai import OpenAI

# Download NLTK data if not present
nltk.download('punkt', quiet=True)

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_question = request.form['question']
        processed_question = preprocess_question(original_question)
        try:
            answer = get_answer_from_llm(processed_question)
        except Exception as e:
            answer = f"Error: {e}"
        return render_template('index.html', original=original_question, processed=processed_question, answer=answer)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
