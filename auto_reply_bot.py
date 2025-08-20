import pyautogui
import pyperclip
import time
from openai import OpenAI

client = OpenAI(
  api_key="Your open ai Api key"
)

# Small delay before starting (so you can prepare)
time.sleep(3)

def get_last_sender(chat_log: str) -> str | None:
    """Return the sender of the last message in chat_log"""
    lines = [line.strip() for line in chat_log.splitlines() if line.strip()]
    
    if not lines:
        return None
    
    last_message = lines[-1]
    
    if "] " in last_message and ":" in last_message:
        sender_part = last_message.split("] ", 1)[1]
        actual_sender = sender_part.split(":", 1)[0].strip()
        return actual_sender
    
    return None

# Step 1: Click on the icon
pyautogui.click(1005, 1059)
time.sleep(1)  # wait for app to open


while True:
    # Step 2: Drag to select text
    pyautogui.moveTo(680, 231)
    pyautogui.dragTo(1739, 936, duration=1, button='left')
    time.sleep(0.5)

    # Step 3: Copy to clipboard
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.click(704, 234)
    time.sleep(0.5)

    # Step 4: Get chat history
    chat_history = pyperclip.paste()
    print("✅ Copied text:", chat_history)

    # Get last sender dynamically
    last_sender = get_last_sender(chat_history)
    print("👤 Last sender:", last_sender)

    # Respond only if last sender is NOT Night_hawk (to avoid replying to yourself)
    if last_sender and last_sender != "Night_hawk":
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a person named Night_hawk. You speak Hinglish, are from India, and a coder. Analyze the chat history and respond naturally like Night_hawk. Output only the response (no name or timestamp)."},
                {"role": "user", "content": chat_history}
            ]
        )
        response = completion.choices[0].message.content.strip()
        pyperclip.copy(response)

        # Step 6: Paste reply into chat
        pyautogui.click(783, 992)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        print(f"✅ Response sent to {last_sender}:", response)
