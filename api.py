from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import re
import json
import os
from prompt import Prompt

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

app = FastAPI()

class InputRequest(BaseModel):
    input: str

def extract_json_from_string(s):
    # Regular expression to match the JSON part of the string
    json_pattern = re.compile(r'\{.*\}', re.DOTALL)
    
    # Search for the JSON pattern in the string
    match = json_pattern.search(s)
    
    if match:
        json_str = match.group(0)
        return json_str
    else:
        return None

@app.post("/filter/")
async def process_input(input_request: InputRequest):
    try:
        input_text = input_request.input
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": Prompt,
                },
                {
                    "role": "user",
                    "content": input_text}],
            model="llama3-70b-8192",
        )

        response = chat_completion.choices[0].message.content
        response = extract_json_from_string(response)
        response = json.loads(response)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
