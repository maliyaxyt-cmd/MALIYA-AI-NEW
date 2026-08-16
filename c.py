import sys
import os
import google.generativeai as genai
from config import ak

sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")

genai.configure(api_key=ak)

model = genai.GenerativeModel("gemini-2.5-flash")

history_file = "chat_history.txt"
old_chat = ""

if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as f:
        old_chat = f.read()

chat = model.start_chat()

if old_chat:
    chat.send_message(
        "This is our previous chat history. Remember the context:\n" + old_chat
    )

print("=" * 40)
print("🤖 Maliya AI v1.1")
print("Type 'exit' to quit")
print("=" * 40)

while True:
    msg = input("You: ")

    if msg.lower() == "exit":
        print("Goodbye!")
        break

    try:
        response = chat.send_message(msg)
        print("AI:", response.text)

        with open(history_file, "a", encoding="utf-8") as f:
            f.write("You: " + msg + "\n")
            f.write("AI: " + response.text + "\n\n")

    except Exception as e:
        print("Error:", e)