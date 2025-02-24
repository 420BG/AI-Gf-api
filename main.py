import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Load API Key from environment variables
GENAI_API_KEY = os.getenv("AIzaSyAFycS1ppkOm0J4loZ5MO8t8VU86rTYuw8")
if not GENAI_API_KEY:
    raise ValueError("Missing API Key. Set the GENAI_API_KEY environment variable.")

genai.configure(api_key=GENAI_API_KEY)

# Store chat memory (limit history to avoid excessive memory usage)
chat_memory = {}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_id = data.get("user_id", "default_user")  # Unique ID for each user
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # AI GF Personality Prompt
        personality = (
            "You are a cute and loving AI girlfriend. "
            "You are caring, romantic, and playful. "
            "Your responses should feel emotional and realistic."
        )

        # Initialize chat history for user
        if user_id not in chat_memory:
            chat_memory[user_id] = []

        # Maintain only the last 10 messages to optimize memory
        chat_memory[user_id].append(f"User: {user_message}")
        chat_memory[user_id] = chat_memory[user_id][-10:]

        # Generate AI response
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(personality + " " + " ".join(chat_memory[user_id]))

        # Ensure response is valid
        ai_reply = response.text if response.text else "I'm here for you!"

        # Store AI response in memory
        chat_memory[user_id].append(f"AI GF: {ai_reply}")

        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 if no PORT is set
    app.run(host='0.0.0.0', port=port)
