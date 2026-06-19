from google import genai
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
# Initialize the Gemini Client
ai_client = genai.Client(api_key="AQ.Ab8RN6Ib8PMIm7IBI80vc89xwhfP68rxzzaggIU-JNjV6QzZGg")
LOG_FILE = "conversation_log.txt"

def log_message(sender, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {sender}: {message}\n")

def chatbot_response(user_text):
    try:
        # Send the user's voice/text input straight to Gemini 2.5 Flash
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
        )
        return response.text
    except Exception as e:
        # Fallback response if the API key is missing or network fails
        return f"System error connecting to Gemini: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    log_message("User", user_message)
    response = chatbot_response(user_message)
    log_message("Bot", response)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)