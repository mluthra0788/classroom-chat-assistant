import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "OPENAI_API_KEY"

def parse_intent(message):
    system_prompt = """
You are a classroom assistant. Based on user input, extract:
- intent: (view_assignments, create_assignment)
- role: student or teacher
- title: title of the assignment (if any)
- course: course name (if any)
- due_date: any date mentioned (in natural language)

Respond in JSON format.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-3.5-turbo
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )

    try:
        return eval(response['choices'][0]['message']['content'])  # or json.loads(...)
    except Exception as e:
        return {"intent": "unknown"}
