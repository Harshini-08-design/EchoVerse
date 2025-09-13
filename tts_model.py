# tts_model.py
import requests

def tts_with_hf(text: str, hf_api_key: str, model_id: str):
    headers = {"Authorization": f"Bearer {hf_api_key}"}
    payload = {"inputs": text}
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 200:
        return resp.content  # audio bytes
    else:
        print("TTS error:", resp.text)
        return None


