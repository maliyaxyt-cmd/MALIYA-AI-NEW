from flask import Flask, request, jsonify, send_file
from google import genai

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

from config import ak

from memory import (
    add_memory,
    get_memory,
    get_all_memory,
    clear_memory
)

import edge_tts
import asyncio
import os
import uuid


# ==========================================
# Flask
# ==========================================

app = Flask(
    __name__,
    static_folder="web",
    static_url_path=""
)


# ==========================================
# 🔥 Firebase Admin SDK
# ==========================================

try:

    firebase_cred = credentials.Certificate(
        "firebase-adminsdk.json"
    )

    firebase_admin.initialize_app(
        firebase_cred
    )

    print("🔥 Firebase Admin: ON")

except Exception as e:

    print(
        "❌ Firebase Admin error:",
        e
    )


# ==========================================
# Gemini
# ==========================================

client = genai.Client(
    api_key=ak
)

MODEL = "gemini-3.5-flash"


# ==========================================
# 🔊 EDGE TTS
# ==========================================

TTS_VOICE = "si-LK-SameeraNeural"

TTS_RATE = "+15%"

TTS_VOLUME = "+0%"


# ==========================================
# 🔐 VERIFY FIREBASE USER
# ==========================================

def verify_user():

    auth_header = request.headers.get(
        "Authorization",
        ""
    )

    if not auth_header.startswith(
        "Bearer "
    ):

        return None


    id_token = auth_header.split(
        "Bearer ",
        1
    )[1]


    if not id_token:

        return None


    try:

        decoded_token = auth.verify_id_token(
            id_token
        )

        return decoded_token


    except Exception as e:

        print(
            "❌ Firebase token error:",
            e
        )

        return None


# ==========================================
# 🌐 WEB HOME
# ==========================================

@app.route("/")
def home():

    return app.send_static_file(
        "index.html"
    )


# ==========================================
# 💬 CHAT API
# ==========================================

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    try:

        # ==================================
        # Verify User
        # ==================================

        user = verify_user()


        if not user:

            return jsonify({

                "success": False,

                "error":
                    "Authentication required"

            }), 401


        # ==================================
        # Firebase UID
        # ==================================

        user_id = user.get(
            "uid"
        )


        if not user_id:

            return jsonify({

                "success": False,

                "error":
                    "User ID not found"

            }), 401


        # ==================================
        # Request Data
        # ==================================

        data = request.get_json()


        if not data:

            return jsonify({

                "success": False,

                "error":
                    "No data received"

            }), 400


        user_text = data.get(
            "message",
            ""
        ).strip()


        if not user_text:

            return jsonify({

                "success": False,

                "error":
                    "Message is empty"

            }), 400


        # ==================================
        # 🧠 USER MEMORY
        # ==================================

        memory = get_memory(
            user_id
        )


        # ==================================
        # Gemini Prompt
        # ==================================

        prompt = f"""
You are Maliya AI.

You are a friendly personal AI assistant.

Rules:

- If the user speaks Sinhala, reply in Sinhala.
- Be natural and helpful.
- Keep answers reasonably concise because the answer may be spoken aloud.
- Use previous conversation when useful.
- Do not mention the memory system.
- Do not reveal private user information.
- Treat the current user as the owner of their own conversation.

Previous conversation:

{memory}

Current user message:

{user_text}

Answer the user.
"""


        # ==================================
        # 🤖 Gemini
        # ==================================

        response = client.models.generate_content(

            model=MODEL,

            contents=prompt

        )


        answer = (

            response.text
            if response.text
            else ""

        ).strip()


        if not answer:

            return jsonify({

                "success": False,

                "error":
                    "Gemini returned an empty answer"

            }), 500


        # ==================================
        # 🧠 SAVE USER MEMORY
        # ==================================

        add_memory(

            user_id,

            user_text,

            answer

        )


        # ==================================
        # Return Answer
        # ==================================

        return jsonify({

            "success": True,

            "answer": answer

        })


    except Exception as e:

        print(
            "❌ CHAT ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ==========================================
# 🔊 TEXT TO SPEECH API
# ==========================================

@app.route(
    "/api/tts",
    methods=["POST"]
)
def text_to_speech():

    try:

        # ==================================
        # Verify User
        # ==================================

        user = verify_user()


        if not user:

            return jsonify({

                "success": False,

                "error":
                    "Authentication required"

            }), 401


        # ==================================
        # Request
        # ==================================

        data = request.get_json()


        if not data:

            return jsonify({

                "success": False,

                "error":
                    "No data received"

            }), 400


        text = data.get(
            "text",
            ""
        ).strip()


        if not text:

            return jsonify({

                "success": False,

                "error":
                    "Text is empty"

            }), 400


        # ==================================
        # Limit extremely large text
        # ==================================

        text = text[:5000]


        # ==================================
        # Temporary audio filename
        # ==================================

        filename = (
            "tts_" +
            str(uuid.uuid4()) +
            ".mp3"
        )


        filepath = os.path.join(
            os.getcwd(),
            filename
        )


        # ==================================
        # Generate Sinhala Voice
        # ==================================

        async def generate_voice():

            communicate = edge_tts.Communicate(

                text,

                TTS_VOICE,

                rate=TTS_RATE,

                volume=TTS_VOLUME

            )

            await communicate.save(
                filepath
            )


        asyncio.run(
            generate_voice()
        )


        # ==================================
        # Check file
        # ==================================

        if not os.path.exists(
            filepath
        ):

            return jsonify({

                "success": False,

                "error":
                    "Voice file was not created"

            }), 500


        print(
            "🔊 Sinhala TTS generated:",
            filepath
        )


        # ==================================
        # Send MP3
        # ==================================

        return send_file(

            filepath,

            mimetype="audio/mpeg",

            as_attachment=False,

            download_name="maliya_ai.mp3"

        )


    except Exception as e:

        print(
            "❌ TTS ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ==========================================
# 🧠 GET USER MEMORY
# ==========================================

@app.route(
    "/api/memory",
    methods=["GET"]
)
def memory_api():

    try:

        # ==================================
        # Verify User
        # ==================================

        user = verify_user()


        if not user:

            return jsonify({

                "success": False,

                "error":
                    "Authentication required"

            }), 401


        # ==================================
        # User ID
        # ==================================

        user_id = user.get(
            "uid"
        )


        # ==================================
        # Get Memory
        # ==================================

        memories = get_all_memory(
            user_id
        )


        return jsonify({

            "success": True,

            "memory": memories

        })


    except Exception as e:

        print(
            "❌ MEMORY ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ==========================================
# 🗑️ CLEAR USER MEMORY
# ==========================================

@app.route(
    "/api/memory/clear",
    methods=["POST"]
)
def clear_memory_api():

    try:

        # ==================================
        # Verify User
        # ==================================

        user = verify_user()


        if not user:

            return jsonify({

                "success": False,

                "error":
                    "Authentication required"

            }), 401


        # ==================================
        # User ID
        # ==================================

        user_id = user.get(
            "uid"
        )


        # ==================================
        # Clear Memory
        # ==================================

        clear_memory(
            user_id
        )


        return jsonify({

            "success": True,

            "message":
                "Memory cleared"

        })


    except Exception as e:

        print(
            "❌ CLEAR MEMORY ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ==========================================
# 🚀 SERVER
# ==========================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "🤖 MALIYA AI WEB SERVER"
    )

    print(
        "🌐 http://127.0.0.1:5000"
    )

    print(
        "🔐 Firebase Authentication: ON"
    )

    print(
        "💬 Chat API: ON"
    )

    print(
        "🧠 User Memory: ON"
    )

    print(
        "🔊 Sinhala TTS: ON"
    )

    print(
        "🎙️ Voice:",
        TTS_VOICE
    )

    print(
        "🤖 Gemini Model:",
        MODEL
    )

    print("=" * 60)


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )