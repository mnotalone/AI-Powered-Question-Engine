import os
from flask import Flask, request, render_template, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3-8B-Instruct")

app = Flask(__name__)

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"answer": "Please provide a question."})

    payload = {
        "inputs": question,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }

    hf_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

    try:
        response = requests.post(hf_url, headers=HEADERS, json=payload)
        if response.status_code != 200:
            return jsonify({"answer": f"Hugging Face API error {response.status_code} - {response.text}"})
        
        result = response.json()
        # Extract generated text
        answer = ""
        if isinstance(result, list) and result and "generated_text" in result[0]:
            answer = result[0]["generated_text"]
        elif "generated_text" in result:
            answer = result["generated_text"]
        else:
            answer = str(result)

        # Remove question repetition if needed
        if answer.lower().startswith(question.lower()):
            answer = answer[len(question):].strip()

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Server error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
