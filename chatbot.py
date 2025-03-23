import google.generativeai as genai
from dotenv import load_dotenv
import os

# 🔑 Use your actual API key from MakerSuite
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel("gemini-1.5-pro-latest")
chat = model.start_chat(history=[])

# 🧠 For live chat
def chat_with_ai(user_input):
    try:
        response = chat.send_message(user_input)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini Error: {str(e)}"

# ✅ Still keep this if using reflection feature
def get_ai_feedback(title, planned, actual):
    prompt = f"""
You're a friendly assistant helping ADHD users reflect.

They planned {planned} minutes on "{title}" but spent {actual} minutes.

Give encouraging, short advice to improve time planning.
"""
    return chat_with_ai(prompt)

