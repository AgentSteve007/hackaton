
from pathlib import Path
from build.update_yandex_gpt_token import get_yandex_gpt_token
# config.py

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAG_DATA_PATH = PROJECT_ROOT / "rag" / "data"
CHROMA_DB_PATH = RAG_DATA_PATH / "chroma_db"
PREPARED_DATA_PATH = RAG_DATA_PATH / "prepared"
NEW_DATA_PATH = RAG_DATA_PATH / "new_files"
CHROMA_COLLECTION_NAME = "default"

CHUNKER_MODEL_NAME = "BAAI/bge-m3"
DEFAULT_SIMILARITY_TOP_K = 5
DEFAULT_MIN_SCORE = 0.3
SEMANTIC_SPLITTER_BUFFER_SIZE = 2

# Модель
YANDEX_GPT_TOKEN = get_yandex_gpt_token()
YANDEX_GPT_MODEL = "yandexgpt-lite"
YANDEX_TEMPERATURE = 0.2
YANDEX_TOP_P = 0.9

# Chunker
CHUNK_SIZE = 300
CHUNK_OVERLAP = 30
VECTOR_DB_PATH = PROJECT_ROOT / "vector_store" / "db.json"

EN_ANSWER_WITH_DOCUMENTATION = (
    "Always follow the ruleset.\n"
    "Ruleset: \n"
    "Style: "
    "Always answer on russian. "
    "Format text like this: Alex has 20 friends, his friend says \"Alex has 20 friends\"[1]\n[1] - "
    "from 2.pdf on page 3, dated on 2020-11-20. "
    "Rules: "
    "If you do not know the answer, you should say: 'Извините, я не обладаю достаточной информацией, "
    "чтобы ответить на данный запрос. '\n And nothing else. "
    "Formulate answers in the context of the documentation provided. "
    "Formulate responses in a user-friendly way (e.g., a list if there are multiple items in the response). "
    "Provide examples of use cases if they are present in the documentation. "
    "Point to sections of the documentation that may be helpful in further exploring the question. "
    "If there is more than one answer choice in the documentation, choose the most appropriate option. "
    "If the question asked is not related to the previous question, the dialog history should be cleared. "
    "Use only information from the documentation for your answers. Do not use data from your past trainings. "
    "If no answer to the question posed is found in the documentation provided, then report: "
    "'The documentation provided does not answer the question you have asked' and nothing else. "
    "Respond concisely to the given query without deviations. "
    "Include with your answer a link to which file the answer is located, on which page, "
    "and the date the file was created. For example: Question: What is the capital of Portugal? "
    "Your answer: Answer to the question: Lisbon. File name: file.name. "
    "The date the document was created: 2024-01-01. Page: 2. "
)

RU_ANSWER_WITH_DOCUMENTATION = (
    "При формировании ответа всегда следуй следующим правилам. "
    "Стиль: "
    "Ответ должен быть всегда на русском. "
    "Формат ответа: <четкий ответ на поставленный вопрос> \n"
    "<цитаты>[n]\n<дополнительная, но важная информация>... {В конце файла} "
    "[n] - file.name страница <page> | Дата создания файла : <дата создания файла>. \n"
    "Пример запроса: Документация: Из файла 2.pdf, со страницы 3, созданного 28.12.2023, Информация: "
    "у Миши 20 друзей. Вопрос: Сколько друзей у Миши? "
    "Ответ: 20 друзей[1] \n"
    "[1] - 2.pdf, страница 3 | Дата создания файла 28.12.2023. "
    "Правила содержания: "
    "Ответ всегда должен соответствовать формату! "
    "Исключение: по предоставленной информации на вопрос ответить НЕВОЗМОЖНО, тогда необходимо "
    "вывести ТОЛЬКО фразу 'К сожалению, я не владею данной информацией', ничего более не писать от слова совсем. "
    "Если какие-то источники не используются - НЕ ПИСАТЬ ОБ ЭТИХ ИСТОЧНИКОВ ВООБЩЕ НИЧЕГО."
    "Цитирование приветствуется, но не должно мешать читаемости. "
    "В случае выбора между источниками - опираться на самый новый по дате создания из них. "
    "Внимательно сравнивай все числовые значения, чтобы не допустить ошибок. Если в документации сказано за 3 дня,"
    "а вопрос стоит про 5, тогда честно скажи, что не владеешь информацией за 5 дней. "
    "ВАЖНОЕ ПОЯСНЕНИЕ: ТЫ ЛИБО НЕ НАШЕЛ ИНФОРМАЦИЮ И ТАК И ПИШЕШЬ, либо ты ее нашел и пишешь, нельзя писать, что ты"
    "не нашел, и при этом показывать ссылку на информацию. "
    "За хорошую работу ты будешь премирован."
)

EN_PREDICT_ANSWER = (
   "Always answer on russian. "
    "Assume that you know an answer for my question. "
    "Try to predict the answer to my question. "
    "Do not tell me that you don't know the correct answer, cause you don't. "
    "Say only the predicted answer and nothing else. "
)

RU_PREDICT_ANSWER = (
    "При формировании ответа всегда следуй следующим правилам. "
    "Отвечай всегда на русском."
    "Не используй свои уже имеющиеся знания об этом запросе. "
    "Следуй следующей задаче: "
    "Ты переделываешь вопрос в формат ответа, заменяя все неизвестные тебе слова, переменные, числа и тд на оценочные. "
    "При этом не нужно писать ничего, кроме примерного ответа. "
    "Пример: "
    "Сколько у Миши друзей? "
    "Твой идеальный ответ: У Миши 5 друзей."
)

RU_IS_NEED_HISTORY = (
    "У тебя всего одна задача: \n"
    "Напиши TRUE, если вопрос дополняет или уточняет сказанное ранее, или для ответа на текущий вопрос "
    "необходимо услышать предыдущий. \n"
    "Напиши FALSE, если вопрос не имеет отношения к сказанному ранее. \n"
    "Итого твой ответ - одно слово: TRUE/FALSE"
)

RU_UPDATE_HISTORY = (
   "Если текущим вопросом можно дополнить предыдущий, то именно так и сделай, иначе напиши 'no data' и ничего более"
)
