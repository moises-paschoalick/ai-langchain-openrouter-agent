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
    print("\n--- 2. Chat: Verifique a hora do sistema ---")
    response = requests.post(f"{BASE_URL}/chat", json={
        "conversation_id": conversation_id,
        "prompt": "Verifique a hora do sistema"
    })
    
    if response.status_code != 200:
        print(f"Error Response: {response.text}")
        sys.exit(1)

    result = response.json()
    print(f"Response: {result}")
    
    if result.get("type") != "tool_call":
        print("Expected tool_call, got something else.")
        sys.exit(1)
    
    tool_call_id = result["tool_call_id"]
    tool_name = result["tool"]
    print(f"Tool Call ID: {tool_call_id}")
    print(f"Tool Name: {tool_name}")
    
    if tool_name != "obter_data_hora_atual":
        print(f"Expected tool 'obter_data_hora_atual', got '{tool_name}'")

    # 3. Submit Tool Result
    print("\n--- 3. Submit Tool Result ---")
    # Simulate the tool execution
    tool_output = "A hora é 14:30"
    print(f"Simulating Tool Output: {tool_output}")
    
    response = requests.post(f"{BASE_URL}/tools/result", json={
        "conversation_id": conversation_id,
        "tool_name": tool_name,
        "tool_output": tool_output,
        "tool_call_id": tool_call_id
    })
    print(f"Submit Response: {response.json()}")

    # 4. Follow-up Chat (Memory Check)
    print("\n--- 4. Chat: A que horas era? ---")
    response = requests.post(f"{BASE_URL}/chat", json={
        "conversation_id": conversation_id,
        "prompt": "A que horas era?"
    })
    
    if response.status_code != 200:
        print(f"Error Response: {response.text}")
        sys.exit(1)
        
    final_result = response.json()
    print(f"Response: {final_result}")
    
    content = final_result.get("content", "")
    if "14:30" in content:
        print("\nSUCCESS: Memory worked! The agent recalled the time.")
    else:
        print("\nFAILURE: The agent did not recall the time correctly.")

finally:
    print("\nStopping server...")
    server_process.terminate()
    server_process.wait()
