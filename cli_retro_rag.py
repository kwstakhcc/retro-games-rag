import argparse

import os
import threading

from src.data_loader import get_knowledge_base, get_corpus
from src.embed import get_model_and_embeddings
from src.retrieve import retrieval
from src.generate import generate_response

from src.utils import print_banner, print_waiting_messages

from src.config import TERM_COLUMNS
from src.config import API_CALL_PARAMS
from src.config import INTRO_MESSAGE, TYPED_NOTHING_MESSAGE, EXIT_MESSAGE, GOODBYE_MESSAGE
from src.config import FIRST_QUESTION, SECOND_QUESTION
from src.config import CHAT_HISTORY_MAX_SIZE, MESSAGES_KEPT, WAITING_MESSAGES

def main(model_id: str, k: int) -> None:

    chat_history = []
    
    knowledge_base = get_knowledge_base()
    corpus = get_corpus(knowledge_base)

    model, embeddings = get_model_and_embeddings(model_id, corpus)
    
    print_banner(INTRO_MESSAGE)

    query = input(FIRST_QUESTION)

    if query == EXIT_MESSAGE:
        print(GOODBYE_MESSAGE)
        return

    print('\n' + '\u2500' * TERM_COLUMNS + '\n')
    
    while(True):

        while(query == ''):
            query = input(TYPED_NOTHING_MESSAGE)
            print('\n' + '\u2500' * TERM_COLUMNS + '\n')
            if query != '': break

        if query == EXIT_MESSAGE:
            print(GOODBYE_MESSAGE)
            return

        if len(chat_history) > CHAT_HISTORY_MAX_SIZE:
            chat_history = chat_history[-MESSAGES_KEPT:]
            
        chat_history.append({'role': 'user', 'content': query})
        
        retrieved_chunks = retrieval(knowledge_base, model, embeddings, k, query)

        done = threading.Event()                      
        thr = threading.Thread(target=print_waiting_messages, args=(WAITING_MESSAGES, done), daemon=True)
        thr.start()

        generated_response = generate_response(query, retrieved_chunks, API_CALL_PARAMS,
                                               chat_history, done)

        chat_history.append({'role': 'assistant', 'content': generated_response})
        
        print(f"\n\n{generated_response}")

        print('\n' + '\u2500' * TERM_COLUMNS + '\n')

        query = input(SECOND_QUESTION)

        print('\n' + '\u2500' * TERM_COLUMNS + '\n')

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--model', type=str, default='tfidf', help='Type of model to be used for embedding.')
    parser.add_argument('--num_top_chunks', type=int, default=200, help='Number of top relevant chunks retrieved.')

    args = parser.parse_args()

    main(args.model, args.num_top_chunks)
