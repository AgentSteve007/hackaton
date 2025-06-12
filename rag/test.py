import time
from rag import Rag
from chunker.chunker import Chunker
# from build.update_yandex_gpt_token import get_yandex_gpt_token


INPUT_PATH = "data/tests/test.txt"
OUTPUT_PATH = "data/tests/ans.txt"
START_INDEX = 160  # начиная с 160-й строки
LIMIT = None       # например, 10 — для отладки; None — чтобы обрабатывать всё

# token = get_yandex_gpt_token()
token = "t1.9euelZqSiYuSx42L..."  # скрыт для безопасности

history = ""
chunker = Chunker()
output = []

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    questions = f.readlines()[START_INDEX:]
    if LIMIT:
        questions = questions[:LIMIT]

for i, question in enumerate(questions, START_INDEX + 1):
    question = question.strip()
    if not question:
        continue

    try:
        start_time = time.time()
        res = Rag.static_query(question, token, chunker=chunker, history=history)
        elapsed = time.time() - start_time

        history = res["history"]
        text = res["answer"].replace("\n", " ")
        output.append(text)

        print(f"[{i}] OK ({elapsed:.2f}s): {question}")

    except Exception as e:
        print(f"[{i}] ERROR: {e}")
        output.append(f"[ERROR] {question}")

# Запись всех ответов
with open(OUTPUT_PATH, "w", encoding="utf-8") as fw:
    fw.write("\n".join(output))
