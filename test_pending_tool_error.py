import requests
import time
import subprocess
import sys

# Start the server
server_process = subprocess.Popen(
    [sys.executable, "app.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print("Starting server...")
time.sleep(5)

BASE_URL = "http://127.0.0.1:5000"

try:
    # 1. Create Thread
    print("\n--- 1. Creating Thread ---")
    response = requests.post(f"{BASE_URL}/threads")
    conversation_id = response.json()["conversation_id"]
    print(f"Conversation ID: {conversation_id}")

    # 2. Chat (Trigger Tool)
    print("\n--- 2. Chat: Verifique a hora ---")
    response = requests.post(f"{BASE_URL}/chat", json={
        "conversation_id": conversation_id,
        "prompt": "Verifique a hora do sistema"
    })
    result = response.json()
    print(f"Response: {result}")
    
    if result.get("type") != "tool_call":
        print("Expected tool_call")
        sys.exit(1)

    # 3. Send New Message WITHOUT submitting tool result
    print("\n--- 3. Send New Message (Skipping Tool Result) ---")
    response = requests.post(f"{BASE_URL}/chat", json={
        "conversation_id": conversation_id,
        "prompt": "Esquece, qual seu nome?"
    })
    
    print(f"Response Status: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    if response.status_code == 400:
        print("\nSUCCESS: Reproduced 400 error (Pending Tool Call)")
    else:
        print("\nFAILURE: Did not reproduce error (or it was handled?)")

finally:
    server_process.terminate()
    server_process.wait()
