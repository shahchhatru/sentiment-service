from fastapi import FastAPI
from pydantic import BaseModel
from app.services.sentiment import analyze_sentiment

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze(input: TextInput):
    result = analyze_sentiment(input.text)
    return {"input": input.text, "result": result}
