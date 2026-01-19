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

    # 3. Submit Tool Result WITHOUT tool_call_id
    print("\n--- 3. Submit Tool Result (Missing ID) ---")
    tool_name = result["tool"]
    tool_output = "A hora é 10:00"
    
    response = requests.post(f"{BASE_URL}/tools/result", json={
        "conversation_id": conversation_id,
        "tool_name": tool_name,
        "tool_output": tool_output
        # MISSING tool_call_id
    })
    print(f"Submit Response: {response.json()}")

    # 4. Follow-up Chat (Should Fail)
    print("\n--- 4. Chat: Confirming... ---")
    response = requests.post(f"{BASE_URL}/chat", json={
        "conversation_id": conversation_id,
        "prompt": "Confirme a hora"
    })
    
    print(f"Response Status: {response.status_code}")
    print(f"Response Text: {response.text}")

finally:
    server_process.terminate()
    server_process.wait()
