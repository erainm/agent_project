# Created by erainm on 2025/10/28 15:06.
# IDE：PyCharm 
# @Project: agent_project
# @File：a2a_server
# @Description:
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Define the A2A Task structure
class Task(BaseModel):
    task_id: str
    message: dict

# 实例化FastAPI
app = FastAPI()

# 定义Agent卡（关于agent的元数据）
echo_skill = {
    "name": "echo_query",
    "description": "客户端发出的任何信息，服务器会在前面添加上'Hello! You Said:'之后返回",
    "examples": "客户发了任意一句话",
    "input_modes":["text"],
    "output_modes":["text"],
}

agent_card = {
    "name": "EchoAgent",
    "description": "Echo back your message with a greeting",
    "endpoint":"http://localhost:8000/tasks/send",
    "capabilities":["text"],
    "skills":[echo_skill]
}

# Expose the Agent Card at /.well-known/agent.json
@app.get("/.well-known/agent.json")
async def get_agent_card():
    return agent_card


# Handle incoming tasks
@app.post("/tasks/send")
async def handle_task(task: Task):
    user_message = task.message.get("parts", [{}])[0].get("text", "")
    response = {
        "task_id": task.task_id,
        "status": "completed",
        "message": {
            "role": "agent",
            "parts": [{"text": f"Hello! You said: {user_message}"}]
        }
    }
    return response


# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)