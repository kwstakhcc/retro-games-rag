from src.config import INSTRUCTIONS

def get_game_info(chunk: dict) -> str:
    game_info = f"[Source ID: {chunk['id']}] "
    meta_dict = chunk['metadata']
    last_key = list(meta_dict.keys())[-1]
    
    for field in meta_dict.keys():
        last_key = list(meta_dict.keys())[-1]
        if field == last_key: game_info += f"{field.title()}: {meta_dict[field]}"
        else: game_info += f"{field.title()}: {meta_dict[field]} - "

    game_info += f"Description: {chunk['description']} - "
    return game_info

def get_context(retrieved_chunks: list[dict]) -> str:
    context = ""
    for chunk in retrieved_chunks:
        game_info = get_game_info(chunk)
        context += f"{game_info} --- "
    return context

def get_system_prompt(retrieved_chunks: list[dict]) -> str:
    context = get_context(retrieved_chunks)
    system_prompt = f"{INSTRUCTIONS}CONTEXT:\n{context}\n\n"
    return system_prompt
