import json
import requests

# url = "http://127.0.0.1:8082/completion"
# params = {"prompt": "Hello, ", "n_predict": 32}
# resp = requests.post(url, json=params)
# content = json.loads(resp.text)["content"]
# print(content)  # sweetie! How can I help you today?

url = "http://127.0.0.1:8082/completion"
# prompt = """### USER: 什麼是語言模型？
prompt = '''<s>[INST] output from 1 to 100 [/INST]'''
### ASSISTANT: """
stop = ["<s>"]
# params = {"prompt": prompt, "stream": True}
params = {"prompt": prompt,
            "stop": stop,
            "temperature":0,
            "n_predict":1024,
            "stream": True
            }
resp = requests.post(url, json=params, stream=True)
for chunk in resp.iter_lines():
    if not chunk:
        continue
    # 會有固定的 "data:" 前綴，需要跳掉 5 個字元
    content = json.loads(chunk[5:])["content"]
    print(end=content, flush=True)