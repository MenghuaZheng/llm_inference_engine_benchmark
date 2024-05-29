# remember to run: pip install requests
import requests
import json

# change for your host
VLLM_HOST = "https://autumn-snow-1380.ploomberapp.io"
url = f"http://localhost:8082/v1/completions"

prompt = '''<s>[INST] output from 1 to 100 [/INST]'''

headers = {"Content-Type": "application/json"}
data = {
    "model": "model_executor/models/Llama-2-7b-hf/",
    "max_tokens": 1024,
    "prompt": prompt,
    "temperature": 0
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json()["choices"][0]["text"])