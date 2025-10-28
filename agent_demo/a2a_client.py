# Created by erainm on 2025/10/28 15:14.
# IDE：PyCharm 
# @Project: agent_project
# @File：a2a_client
# @Description:

import requests
import uuid

def getAgentCard():
    # A2A server endpoint
    SERVER_URL = "http://localhost:8000/.well-known/agent.json"

    # Send the task to the server
    response = requests.get(SERVER_URL)
    # Check the response
    if response.status_code == 200:
        result = response.json()
        agent_message = result
        print(f"Agent card: {agent_message}")
    else:
        print(f"Error: {response.status_code}")

def excuteTask():
    # A2A server endpoint
    SERVER_URL = "http://localhost:8000/tasks/send"


    # Create a simple task
    task_id = str(uuid.uuid4())  # Unique task ID
    task = {
        "task_id": task_id,
        "message": {
            "role": "user",
            "parts": [{"text": "Hi, how are you?"}]
        }
    }


    # Send the task to the server
    response = requests.post(SERVER_URL, json=task)
    # Check the response
    if response.status_code == 200:
        result = response.json()
        #agent_message = result["message"]["parts"][0]["text"]
        agent_message = result
        print(f"Agent replied: {agent_message}")
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    # getAgentCard()
    excuteTask()