import os
import pathlib

import csv
import json

from src.config import PROJECT_DIRECTORY_PATH, DATA_DIRECTORY_PATH, KNOWLEDGE_BASE_FILE_PATH


def raw_knowledge_base(path: str) -> list[dict]:

    knowledge_base = []
    game_count = 0

    file_paths = os.listdir(path)

    for file_path in file_paths:
        with open(os.path.join(path, file_path), 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile) 
            field_names = reader.fieldnames

            game_platform = pathlib.Path(file_path).stem  

            for row in reader:
                game_count += 1
                
                game_dict = {'id': f"game_{game_count:04d}", 'description': None,
                             'metadata': {'platform': game_platform}}

                for field in field_names:

                    if field == 'description':
                        game_dict[field] = row[field]
                    
                    else: game_dict['metadata'][field] = row[field]

                knowledge_base.append(game_dict)

    return knowledge_base

def clean_knowledge_base(knowledge_base: list[dict]) -> list[dict]:

    KEYS_LIST = ['released', 'gf_score', 'metascore', 'genre']
    TO_REMOVE = set(['n/a', 'N/A', 'unknown', '', 'NA'])
    
    for game in knowledge_base:
        for key in KEYS_LIST:
            if game['metadata'][key] in TO_REMOVE:
                del game['metadata'][key]

    return knowledge_base

def get_knowledge_base() -> list[dict]:
    if os.path.isfile(KNOWLEDGE_BASE_FILE_PATH):
        with open(KNOWLEDGE_BASE_FILE_PATH, 'r', encoding='utf-8') as file:
            kb = json.load(file)
    else:
        build_path = os.path.join(DATA_DIRECTORY_PATH, 'game-info')
        raw_kb = raw_knowledge_base(build_path)
        kb = clean_knowledge_base(raw_kb)

        with open(KNOWLEDGE_BASE_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(kb, file, indent=2, ensure_ascii=False)

    return kb

def get_corpus(knowledge_base: list[dict]) -> list[str]:
    return [game['description'] for game in knowledge_base]
