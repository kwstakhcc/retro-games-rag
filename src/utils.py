import time
import textwrap
import itertools
import threading
import requests

from src.config import TERM_COLUMNS

def format_response(response: requests.Response) -> str:
    data = response.json()
    generated_answer = data["choices"][0]["message"]["content"]

    width = min(TERM_COLUMNS, 100)

    wrapped = "\n".join(
        textwrap.fill(line, width=width) if line.strip() else ""
        for line in generated_answer.splitlines()
    )

    return f"\n{wrapped}\n"

def print_banner(text: str) -> None:
    width = TERM_COLUMNS
    wrap_width = max(10, width - 6)

    for line in textwrap.wrap(text, width=wrap_width):
        padded = f" {line} "
        remaining = width - len(padded)
        left = remaining // 2
        right = remaining - left
        print("=" * left + padded + "=" * right)

def print_waiting_messages(waiting_messages: list[str], event_obj: threading.Event) -> None:

    max_len = max(len(m) for m in waiting_messages)
    messages_cycler = itertools.cycle(waiting_messages)
    for i, msg in enumerate(messages_cycler):      
        print(f"\r{msg.ljust(max_len)}", end="", flush=True)
        time.sleep(0.2)

        if event_obj.wait(3):
            break
