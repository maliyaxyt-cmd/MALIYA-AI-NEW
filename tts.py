import asyncio
import edge_tts
import pygame
import time
import os

async def create_voice():

    text = "හොඳයි, මම සූදානම්. ඔබට මට කතා කරන්න පුළුවන්."

    communicate = edge_tts.Communicate(
        text,
        "si-LK-SameeraNeural"
    )

    await communicate.save("test_voice.mp3")


# Create voice
asyncio.run(create_voice())

print("✅ Voice created!")

# Start audio
pygame.mixer.init()
pygame.mixer.music.load("test_voice.mp3")
pygame.mixer.music.play()

print("🔊 Playing voice...")

# Wait until finished
while pygame.mixer.music.get_busy():
    time.sleep(0.1)

pygame.mixer.quit()

print("✅ Voice finished!")

# Remove temporary file
if os.path.exists("test_voice.mp3"):
    os.remove("test_voice.mp3")