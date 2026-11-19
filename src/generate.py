import requests
import threading

from src.system_prompt import get_system_prompt
from src.utils import format_response
from src.config import IS_CALL_SUCCESS


def generate_response(query: str, retrieved_chunks: list[dict],
                      params: tuple[str], chat_history: list[dict], 
                      event_obj: threading.Event) -> str:
    
    url, api_key, model = params

    if api_key is None:
        raise ValueError("API_KEY environment variable is not set.")

    system_prompt = get_system_prompt(retrieved_chunks)
    
    headers = {'Authorization': f'Bearer {api_key}'}

    data = {
        "model": f"{model}",
        "messages": [{'role': 'system',
                      'content': f'{system_prompt}'},
                     *chat_history,
                     {'role': 'user',
                      'content': f'{query}'}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != IS_CALL_SUCCESS:
            raise Exception(f"API Error {response.status_code}: {response.text}")
        else: return format_response(response)
            
    finally:
        event_obj.set()
