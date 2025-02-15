from flask import Flask, request, jsonify, render_template, session
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

@app.route('/')
def home():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        if 'chat_history' not in session:
            session['chat_history'] = []

        chat_history = session['chat_history']
        
        # Create chat history in the format Gemini expects
        formatted_history = []
        for msg in chat_history:
            formatted_history.append({"role": msg["role"], "parts": [msg["content"]]})

        # Start chat with history
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(f"""You are ZEL, a friendly and helpful AI assistant. Be polite, professional, and provide accurate information.
Always maintain a respectful tone and adapt to the user's style while staying professional.
Here is the user's message: {user_input}""")

        # Update chat history
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "model", "content": response.text})
        session['chat_history'] = chat_history

        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)), debug=False)
