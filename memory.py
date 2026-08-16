import json
import os
from datetime import datetime


# ==========================================
# Memory Folder
# ==========================================

MEMORY_FOLDER = "memory"


# Create memory folder automatically
os.makedirs(
    MEMORY_FOLDER,
    exist_ok=True
)


# ==========================================
# Get User Memory File
# ==========================================

def get_memory_file(user_id):

    # Firebase UID is used as the filename
    return os.path.join(
        MEMORY_FOLDER,
        f"{user_id}.json"
    )


# ==========================================
# Load Memory
# ==========================================

def load_memory(user_id):

    memory_file = get_memory_file(user_id)

    if not os.path.exists(memory_file):
        return []

    try:

        with open(
            memory_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except Exception as e:

        print(
            "❌ Memory load error:",
            e
        )

        return []


# ==========================================
# Save Memory
# ==========================================

def save_memory(user_id, data):

    memory_file = get_memory_file(user_id)

    with open(
        memory_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


# ==========================================
# Add Conversation
# ==========================================

def add_memory(
    user_id,
    user_text,
    ai_answer
):

    memories = load_memory(
        user_id
    )

    memories.append({

        "time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "user":
            user_text,

        "assistant":
            ai_answer

    })


    # Keep latest 100 conversations

    memories = memories[-100:]


    save_memory(
        user_id,
        memories
    )


# ==========================================
# Get Memory
# ==========================================

def get_memory(user_id):

    memories = load_memory(
        user_id
    )

    if not memories:

        return (
            "No previous conversation."
        )


    recent = memories[-20:]


    text = ""


    for item in recent:

        text += (

            f"User: "
            f"{item.get('user', '')}\n"

            f"Assistant: "
            f"{item.get('assistant', '')}\n\n"

        )


    return text


# ==========================================
# Get All Memory
# ==========================================

def get_all_memory(user_id):

    return load_memory(
        user_id
    )


# ==========================================
# Clear Memory
# ==========================================

def clear_memory(user_id):

    save_memory(
        user_id,
        []
    )


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    print(
        "🧠 Maliya AI User Memory"
    )

    test_user = "test-user"

    memories = load_memory(
        test_user
    )

    print(
        f"Saved conversations: "
        f"{len(memories)}"
    )