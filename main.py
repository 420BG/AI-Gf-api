from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Set up Google Gemini AI API Key
GENAI_API_KEY = "AIzaSyAFycS1ppkOm0J4loZ5MO8t8VU86rTYuw8"  # Replace with your real key
genai.configure(api_key=GENAI_API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_message)
    ai_reply = response.text

    return jsonify({"reply": ai_reply})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
