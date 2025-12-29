import os
import sys
from dotenv import load_dotenv
from python_agent.agent import root_agent








from fastapi import FastAPI
from pydantic import BaseModel
from hr_policy_agent.agent import root_agent   # your agent

app = FastAPI()

class ChatRequest(BaseModel):
    user_message: str

@app.post("/chat")
def chat(req: ChatRequest):

    response = root_agent.run(req.user_message)

    # IMPORTANT: if tool call exists, ADK will run it automatically.
    # You do not need extra code here.

    return response





# Load environment variables
load_dotenv()

def main():
    print("Welcome to the HR Policy Chatbot!")
    print("Type 'exit' or 'quit' to stop.\n")
    
    # Simple interaction loop using generate_content (if supported) or similar
    # Since the user primarily uses adk web, this is a fallback reference.
    print("Agent is ready for requests via ADK Web.")

if __name__ == "__main__":
    main()
