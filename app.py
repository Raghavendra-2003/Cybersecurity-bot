from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable frontend communication

# OpenAI API Key (Render environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/ask', methods=['POST'])
def ask_bot():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )
        return jsonify({"response": response["choices"][0]["message"]["content"]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
