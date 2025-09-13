# granite_model.py
import requests, json

HF_API_URL_BASE = "https://api-inference.huggingface.co/models/"

def rewrite_with_granite(prompt: str, hf_api_key: str, model_id: str):
    headers = {"Authorization": f"Bearer {hf_api_key}", "Content-Type": "application/json"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 800, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }
    url = HF_API_URL_BASE + model_id
    resp = requests.post(url, headers=headers, data=json.dumps(payload))
    if resp.status_code == 200:
        try:
            res = resp.json()
            if isinstance(res, list) and "generated_text" in res[0]:
                return res[0]["generated_text"]
            return resp.text
        except:
            return resp.text
    else:
        print("Granite error:", resp.text)
        return None


