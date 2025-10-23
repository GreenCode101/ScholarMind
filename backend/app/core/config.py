# Parsing PDF Configs
START_PAGE = 21
CHUNK_SIZE = 600
CHUNK_OVERLAP = 50

# Remote LLM API
API_KEY = ""

# Local Model Configs
LOCAL_MODEL = 'llama3.2'
TEMPERATURE = 0.7
TOP_P = 0.9
NUM_CTX = 1024
NUM_PREDICT = 256
NUM_THREADS = 4

PROMPT_TEMPLATE = """
You are an assistant that creates educational datasets.
Given the following text, generate:
1. A clear and concise question about the content.
2. A correct answer to that question.
3. A detailed explanation of why that answer is correct.

Text:
{text}

Respond ONLY in Valid JSON format as:
{{
    "question": "...",
    "answer": "...",
    "explanation": "..."
}}
"""

COOLDOWN = True
COOLDOWN_ITERATIONS = 100
COOLDOWN_TIME = 10

MAX_TEMP = 80 
