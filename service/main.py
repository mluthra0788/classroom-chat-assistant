from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import openai
import os
from auth import get_credentials
from assignmentSvc import get_service, get_student_assignments
from intent import parse_intent
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    role: str

# Setup Google Classroom API service
# creds = get_credentials(scopes=[
#     "https://www.googleapis.com/auth/classroom.coursework.students",
#     "https://www.googleapis.com/auth/classroom.coursework.me",
#     "https://www.googleapis.com/auth/classroom.courses.readonly"
# ])

creds = get_credentials(scopes=[
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly'
])
service = get_service(creds)

# --------- Mock Data for Testing (replace with real API calls in production) ---------- #
mock_assignments = [
    {"course": "AI", "title": "Intro to Neural Nets", "due": "2025-06-10"},
    {"course": "ML", "title": "SVM Classifier", "due": "2025-06-12"},
    {"course": "AI", "title": "CNN Project", "due": "2025-06-14"},
]

# --------- RAG Workflow --------- #

def retrieve_context(intent: str, role: str, parsed: dict):
    if intent == "view_assignments":
        # return mock_assignments  # replace with real call: get_student_assignments(service)
        return get_student_assignments(service)
    return []

def generate_response_with_rag(user_query: str, context_data: List[dict]) -> str:
    context_str = "\n".join(
        f"- {item['title']} (Course: {item['course']}, Due: {item.get('due', 'N/A')})"
        for item in context_data
    )

    prompt = f"""
You are a helpful Google Classroom assistant.
The user asked: \"{user_query}\"

Here is some relevant context from their account:
{context_str}

Now answer the user's query clearly and helpfully based on the context above.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Google Classroom chatbot assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content']

# --------- FastAPI Endpoint --------- #

@app.post("/chat")
def chatbot(req: ChatRequest):
    parsed = parse_intent(req.message)
    intent = parsed.get("intent")
    role = parsed.get("role", req.role)

    context_data = retrieve_context(intent, role, parsed)
    final_response = generate_response_with_rag(req.message, context_data)

    return {"response": final_response}
