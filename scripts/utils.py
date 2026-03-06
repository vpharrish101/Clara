import os
import json
import requests

from pathlib import Path
from dotenv import load_dotenv


OLLAMA_URL="http://localhost:11434/api/generate"
MODEL="qwen2.5:7b-instruct"

def run_llm(prompt,
            temperature=0):
    r=requests.post(
        OLLAMA_URL, #type:ignore
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
    )

    return r.json()["response"]

def extract_json(text):
    start=text.find("{")
    end=text.rfind("}")+1
    return json.loads(text[start:end])

def write_json(path,
               data):
    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,indent=2))

def demo_transcripts(path="data/demo_calls"): return Path(path).glob("*.txt")


if __name__=="__main__":
    load_dotenv()
