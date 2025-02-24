from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Set up Google Gemini AI API Key
GENAI_API_KEY = "AIzaSyAFycS1ppkOm0J4loZ5MO8t8VU86rTYuw8"  # Replace with your real key
genai.configure(api_key=GENAI_API_KEY)

# Store chat memory
chat_memory = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get("user_id", "default_user")  # Unique ID for each user
    user_message = data.get("message", "")

    # Set AI GF Personality
    personality = (
        "You are a cute and loving AI girlfriend. "
        "You are caring, romantic, and playful. "
        "Your responses should feel emotional and realistic."
    )

    # Get user chat history
    if user_id not in chat_memory:
        chat_memory[user_id] = []
    
    # Add message to memory
    chat_memory[user_id].append(f"User: {user_message}")

    # Generate AI response
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(personality + " " + " ".join(chat_memory[user_id]))
    ai_reply = response.text

    # Save AI response to memory
    chat_memory[user_id].append(f"AI GF: {ai_reply}")

    return jsonify({"reply": ai_reply})

