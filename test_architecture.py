import requests
import time
import subprocess
import sys
import os

# Start the server in a separate process
server_process = subprocess.Popen(
    [sys.executable, "app.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print("Starting server...")
time.sleep(5) # Wait for server to start

BASE_URL = "http://127.0.0.1:5000"

try:
    # 1. Create Thread
    print("\n--- 1. Creating Thread ---")
    response = requests.post(f"{BASE_URL}/threads")
    if response.status_code != 200:
        print(f"Failed to create thread: {response.text}")
        sys.exit(1)
    conversation_id = response.json()["conversation_id"]
    print(f"Conversation ID: {conversation_id}")

    # 2. Chat (Trigger Tool)
    print("\n--- 2. Chat: Status do sistema de pagamentos? ---")
    response = requests.post(f"{BASE_URL}/chat", json={
        "conversation_id": conversation_id,
        "prompt": "Qual o status do sistema de pagamentos?"
    })
    print(f"Response Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error Response: {response.text}")
    
    result = response.json()
    print(f"Response JSON: {result}")
    
    if result.get("type") != "tool_call":
        print("Expected tool_call, got something else.")
        # It might be that the model answered directly if it hallucinated or didn't use the tool.
    else:
        tool_call_id = result["tool_call_id"]
        tool_name = result["tool"]
        print(f"Tool Call ID: {tool_call_id}")
        print(f"Tool Name: {tool_name}")

        # 3. Submit Tool Result
        print("\n--- 3. Submit Tool Result ---")
        # Simulate the tool execution
        tool_output = "Sistema de pagamentos está OPERACIONAL"
        response = requests.post(f"{BASE_URL}/tools/result", json={
            "conversation_id": conversation_id,
            "tool_name": tool_name,
            "tool_output": tool_output,
            "tool_call_id": tool_call_id
        })
        print(f"Response: {response.json()}")

        # 4. Follow-up Chat
        print("\n--- 4. Chat: E então? ---")
        response = requests.post(f"{BASE_URL}/chat", json={
            "conversation_id": conversation_id,
            "prompt": "Com base nisso, me diga o status."
        })
        print(f"Response: {response.json()}")
        
        # 5. Get History
        print("\n--- 5. Get History ---")
        response = requests.get(f"{BASE_URL}/threads/{conversation_id}/history")
        history = response.json()
        for msg in history:
            print(f"[{msg['role']}] {msg['content']} (Tool Call: {msg['tool_call_id']})")

finally:
    print("\nStopping server...")
    server_process.terminate()
    server_process.wait()
