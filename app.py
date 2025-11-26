import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ------------------------------
# Configuration
# ------------------------------
# SECURITY WARNING: Never hardcode API keys in production code. 
# Use environment variables: os.getenv("GEMINI_API_KEY")
API_KEY = "AIzaSyBPB8WkF_XkInDgq4s-9jzc_3stTpWhMLg" 

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    print(f"Error configuring API: {e}")
    exit()

# ------------------------------
# Initialize Model with System Instruction
# ------------------------------
# Define the persona HERE, not in the chat history
HR_SYSTEM_INSTRUCTION = """
You are an HR Recruitment Bot.
Your responsibilities:
1. Greet the user professionally.
2. Ask interview questions one-by-one in this order: Name, Age, CGPA, 10th Percentage, 12th Percentage.
3. After collecting all info, evaluate based on:
   - Reject if CGPA < 8
   - Reject if 10th % < 70
   - Reject if 12th % < 70
4. If passed, congratulate and say the candidate is shortlisted.
5. If rejected, clearly state the reason(s).
6. Stay polite, formal, and to the point.
7. Do NOT answer general questions. Redirect back to the interview.
8. Do NOT disclose the rules of evaluation to the candidate.
"""

try:
    # Note: Use 'gemini-1.5-flash' (standard)
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=HR_SYSTEM_INSTRUCTION
    )
    
    # Initialize the chat session
    # NOTE: In a real app, you need a way to store specific history for specific users 
    # (e.g., using a session ID or database). For a local test, this global variable is okay.
    chat_session = model.start_chat(history=[])
    
    print("Gemini HR Bot Initialized Successfully.")

except Exception as e:
    print(f"Error initializing model: {e}")
    exit()

# ------------------------------
# Web Routes
# ------------------------------

@app.route("/")
def home():
    # Ensure you have a folder named 'templates' with 'index.html' inside it
    return render_template("index.html") 

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Send message to Gemini
        response = chat_session.send_message(user_message)
        return jsonify({"response": response.text})
    
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({"response": "Sorry, I am facing some issues."})

if __name__ == "__main__":
    app.run(debug=True)
