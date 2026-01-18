import requests
import time
import subprocess
import sys
import json

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
    # 1. Register New Tool
    print("\n--- 1. Register Dynamic Tool (save_user_data) ---")
    tool_def = {
      "name": "save_user_data",
      "description": "Save user data to the database",
      "strict": True,
      "parameters": {
        "type": "object",
        "properties": {
          "address": {
            "type": "string",
            "description": "User's address"
          }
        },
        "additionalProperties": False,
        "required": [
          "address"
        ]
      }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=tool_def)
    print(f"Register Response: {response.json()}")
    if response.status_code != 201:
        print("Failed to register tool")
        sys.exit(1)

    # 2. Create Thread
    print("\n--- 2. Creating Thread ---")
    response = requests.post(f"{BASE_URL}/threads")
    conversation_id = response.json()["conversation_id"]
    print(f"Conversation ID: {conversation_id}")

    # 3. Chat (Trigger Dynamic Tool)
    print("\n--- 3. Chat: Save address ---")
    response = requests.post(f"{BASE_URL}/chat", json={
        "conversation_id": conversation_id,
        "prompt": "Save the address '123 Main St' for the user"
    })
    result = response.json()
    print(f"Response: {result}")
    
    if result.get("type") != "tool_call":
        print("Expected tool_call")
        sys.exit(1)
        
    if result.get("tool") != "save_user_data":
        print(f"Expected tool 'save_user_data', got '{result.get('tool')}'")
        sys.exit(1)

    # 4. Submit Result
    print("\n--- 4. Submit Result ---")
    tool_call_id = result["tool_call_id"]
    response = requests.post(f"{BASE_URL}/tools/result", json={
        "conversation_id": conversation_id,
        "tool_name": "save_user_data",
        "tool_output": "Address saved successfully",
        "tool_call_id": tool_call_id
    })
    print(f"Submit Response: {response.json()}")
    
    # 5. Follow up
    print("\n--- 5. Follow up ---")
    response = requests.post(f"{BASE_URL}/chat", json={
        "conversation_id": conversation_id,
        "prompt": "Did you save it?"
    })
    print(f"Response: {response.json()}")

finally:
    server_process.terminate()
    server_process.wait()
