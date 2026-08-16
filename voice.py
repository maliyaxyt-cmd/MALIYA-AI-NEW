import sys
import asyncio
import os
import time
import threading
import queue

import speech_recognition as sr
from google import genai
from config import ak
import edge_tts
import pygame

from memory import add_memory, get_memory


# ==================================================
# UTF-8 / Sinhala
# ==================================================

sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")


# ==================================================
# Gemini
# ==================================================

client = genai.Client(api_key=ak)

MODEL = "gemini-3.5-flash"


# ==================================================
# Microphone
# ==================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5


# ==================================================
# Sinhala Voice
# ==================================================

VOICE = "si-LK-SameeraNeural"

VOICE_RATE = "+15%"
VOICE_VOLUME = "+5%"


# ==================================================
# Control
# ==================================================

stop_event = threading.Event()

speaking = False

program_running = True


# ==================================================
# Keyboard Queue
# ==================================================

keyboard_queue = queue.Queue()


def keyboard_listener():

    global program_running

    while program_running:

        try:

            text = input()

            if text.strip():

                keyboard_queue.put(
                    text.strip()
                )

        except EOFError:

            break

        except Exception:

            break


# ==================================================
# Create Voice
# ==================================================

async def create_voice(text):

    file_name = "ai_voice.mp3"

    communicate = edge_tts.Communicate(
        text,
        VOICE,
        rate=VOICE_RATE,
        volume=VOICE_VOLUME
    )

    await communicate.save(file_name)

    return file_name


# ==================================================
# Stop Speaking Listener
# ==================================================

def listen_for_stop(source):

    global speaking

    stop_recognizer = sr.Recognizer()

    stop_recognizer.energy_threshold = 250
    stop_recognizer.dynamic_energy_threshold = True
    stop_recognizer.pause_threshold = 0.4
    stop_recognizer.phrase_threshold = 0.2
    stop_recognizer.non_speaking_duration = 0.3

    while speaking and program_running:

        try:

            audio = stop_recognizer.listen(
                source,
                timeout=0.5,
                phrase_time_limit=3
            )

            try:

                text = stop_recognizer.recognize_google(
                    audio,
                    language="en-US"
                ).lower().strip()

            except sr.UnknownValueError:

                continue

            if (
                "stop speaking" in text
                or "stop talking" in text
                or text == "stop"
            ):

                stop_event.set()

                try:

                    pygame.mixer.music.stop()

                except Exception:

                    pass

                break

        except sr.WaitTimeoutError:

            continue

        except Exception:

            continue


# ==================================================
# Speak
# ==================================================

def speak(text, source):

    global speaking

    audio_file = None

    try:

        stop_event.clear()

        speaking = True

        audio_file = asyncio.run(
            create_voice(text)
        )

        pygame.mixer.init()

        pygame.mixer.music.load(
            audio_file
        )

        pygame.mixer.music.play()

        listener_thread = threading.Thread(
            target=listen_for_stop,
            args=(source,),
            daemon=True
        )

        listener_thread.start()

        while pygame.mixer.music.get_busy():

            if stop_event.is_set():

                break

            time.sleep(0.05)

        pygame.mixer.music.stop()

        time.sleep(0.1)

        pygame.mixer.quit()

        speaking = False

        if stop_event.is_set():

            print("⏹️ Speaking stopped.")

        else:

            print("✅ Answer finished.")

        if (
            audio_file
            and os.path.exists(audio_file)
        ):

            os.remove(audio_file)

    except Exception as e:

        speaking = False

        try:

            pygame.mixer.music.stop()
            pygame.mixer.quit()

        except Exception:

            pass

        print("🔊 Voice error:", e)

        if (
            audio_file
            and os.path.exists(audio_file)
        ):

            try:

                os.remove(audio_file)

            except Exception:

                pass


# ==================================================
# Gemini + Memory
# ==================================================

def ask_gemini(text):

    try:

        print("🧠 Maliya AI thinking...")

        memory = get_memory()

        prompt = f"""
You are Maliya AI, a friendly personal AI assistant.

Important instructions:

- Understand the user's current message.
- Use previous conversation only when it is relevant.
- Reply naturally.
- If the user speaks Sinhala, reply in Sinhala.
- Keep answers reasonably concise because the answer will be spoken aloud.
- Do not mention this memory system.

Previous conversation:
{memory}

Current user message:
{text}

Now answer the current user message.
"""

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        answer = response.text.strip()

        if not answer:

            return None

        return answer

    except Exception as e:

        print("❌ Gemini error:", e)

        return None


# ==================================================
# Start
# ==================================================

print("=" * 50)

print("🤖 Maliya AI Voice Assistant")

print("🎤 Microphone: ON")

print("⌨️ Keyboard: ON")

print("🧠 Memory: ON")

print("🔊 Sinhala Voice: ON")

print("⚡ Voice Speed: +15%")

print("🛑 Say 'stop speaking' to stop voice")

print("🚪 Type 'exit' or 'quit' to close")

print("=" * 50)


# ==================================================
# Main Program
# ==================================================

try:

    with sr.Microphone() as source:

        print("\n🎧 Microphone calibrating...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        print("✅ Microphone ready!")

        keyboard_thread = threading.Thread(
            target=keyboard_listener,
            daemon=True
        )

        keyboard_thread.start()


        while program_running:

            text = None


            # ======================================
            # Keyboard input
            # ======================================

            try:

                text = keyboard_queue.get_nowait()

                print("⌨️ You:", text)

            except queue.Empty:

                pass


            # ======================================
            # Microphone input
            # ======================================

            if text is None:

                try:

                    audio = recognizer.listen(
                        source,
                        timeout=0.5,
                        phrase_time_limit=10
                    )

                except sr.WaitTimeoutError:

                    continue


                try:

                    text = recognizer.recognize_google(
                        audio,
                        language="si-LK"
                    )

                except sr.UnknownValueError:

                    continue

                except sr.RequestError:

                    continue


                text = text.strip()

                if not text:

                    continue

                print("👤 You:", text)


            # ======================================
            # Exit
            # ======================================

            if text.lower() in [
                "exit",
                "quit"
            ]:

                program_running = False

                print(
                    "👋 Maliya AI stopped."
                )

                break


            # ======================================
            # Gemini
            # ======================================

            answer = ask_gemini(text)

            if not answer:

                continue


            # ======================================
            # Answer
            # ======================================

            print("\n🤖 Maliya AI:")

            print(answer)


            # ======================================
            # Save Memory
            # ======================================

            add_memory(
                text,
                answer
            )


            # ======================================
            # Voice
            # ======================================

            print(
                "\n🔊 Maliya AI speaking..."
            )

            speak(
                answer,
                source
            )


except KeyboardInterrupt:

    program_running = False

    print(
        "\n👋 Maliya AI stopped."
    )