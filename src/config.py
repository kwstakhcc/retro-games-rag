import os
import shutil

PROJECT_DIRECTORY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIRECTORY_PATH = os.path.join(PROJECT_DIRECTORY_PATH, 'data')
MODELS_DIRECTORY_PATH = os.path.join(PROJECT_DIRECTORY_PATH, 'models')
KNOWLEDGE_BASE_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, 'knowledge_base.json')

# ---------------------------------------------------------------------------------------------------

KNOWLEDGE_BASE_VALUES_TO_REMOVE = {'n/a', 'unknown', '', 'na'}

# ---------------------------------------------------------------------------------------------------

URL = 'https://openrouter.ai/api/v1/chat/completions'
API_KEY = os.environ.get('OPENROUTER_API_KEY')
MODEL = 'openrouter/free'

API_CALL_PARAMS = (URL, API_KEY, MODEL)

IS_CALL_SUCCESS = 200

HF_ACCESS_TOKEN = os.environ.get('HF_TOKEN')

# ---------------------------------------------------------------------------------------------------

INTRO_AND_GOAL = """You are a retro gaming assistant.
                    Use ONLY the context provided to you at the end,
                    to produce an answer."""

INSTRUCTION_TEXT = """Answer the question clearly.
                      Cite the Source IDs used. If the answer isn't in the context,
                      say 'Not covered.' Note that in the context below,
                      the symbol '---' is used as a separator to distinguish between information
                      regarding different games.
                      """

INSTRUCTIONS = f"{INTRO_AND_GOAL}\n\nINSTRUCTIONS:\n{INSTRUCTION_TEXT}\n\n"

# ---------------------------------------------------------------------------------------------------

TERM_COLUMNS = shutil.get_terminal_size().columns

INTRO_MESSAGE = "Howdy there! I identify as an expert in information retrieval regarding retro games. Type 'quit' to exit. "
TYPED_NOTHING_MESSAGE = "\n# You typed nothing! Try one more time! : "
EXIT_MESSAGE = 'quit'
GOODBYE_MESSAGE = "\n# So long pal. Take care!\n"
FIRST_QUESTION = "\n# What would you like to know about retro games? : "
SECOND_QUESTION = "\n# What would you like to uncover next? : "


CHAT_HISTORY_MAX_SIZE = 1500
MESSAGES_KEPT = 15
WAITING_MESSAGES = ["Grabbing a super mushroom...", "Searching for the master sword...",
                    "Destroying Neo Cortex's Facilities...", "Conquering Bowser's Castle...",
                    "Performing a backwards long jump...", "Collecting wumpa fruits..."]

# ---------------------------------------------------------------------------------------------------
