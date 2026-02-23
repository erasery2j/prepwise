from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def career_advice(profile: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional career advisor."},
            {"role": "user", "content": profile}
        ]
    )
    return response.choices[0].message.content

def interview_feedback(answer: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict technical interviewer."},
            {"role": "user", "content": answer}
        ]
    )
    return response.choices[0].message.content
