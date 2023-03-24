import os
import configparser
import json
import httpx
import openai
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

open_ai_api_key = "Enter Your OpenAI API Key Here"
openai.api_key = open_ai_api_key

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class Question(BaseModel):
    text: str

async def fetch_chat_gpt_response(prompt):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {open_ai_api_key}",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a 12th grade teacher."},
            {"role": "user", "content": prompt},
        ],
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"].strip()


@app.post("/ask")
async def ask_question(question: Question):
    # Add your logic to process the question and generate an answer
    prompt = f"{question.text}\n\nAnswer:"
    answer = await fetch_chat_gpt_response(prompt)
    print(answer)
    return {"Answer": answer}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    index_html_path = os.path.join("static", "index.html")
    with open(index_html_path, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)
