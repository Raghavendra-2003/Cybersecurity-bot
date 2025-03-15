import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# Debugging step: Print environment variables to check if OPENAI_API_KEY is set
print("🔹 Available Environment Variables:", os.environ.keys())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("🚨 ERROR: OPENAI_API_KEY is missing! Check your Render environment variables.")
    raise ValueError("Missing OpenAI API Key! Set it in Render's environment variables.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask_bot():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )
        return jsonify({"response": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
