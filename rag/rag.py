from llm.llm_methods import answer_with_documentation, predict_answer, add_context_to_query
from chunker.chunker import Chunker
from get_project_root import root_path


class Rag:
    """
    Основной класс, реализующий работу с RAG моделью
    """

    @staticmethod
    def static_query(q: str, token: str, chunker: Chunker = Chunker(),
                     k: int = 2, history: str = "") -> dict[str, str | Chunker]:
        """
        Метод получения ответа на запрос по имеющейся документации

        :param q: Текстовый вопрос по документации
        :param token: Токен доступа к модели Yandex GPT
        :param chunker: Объект класса Chunker, необходимый для работы с БД
        :param k: Количество искомых отрывков на один запрос
        :param history: История предыдущих вопросов
        :return: Словарь с ключами "answer" и "history", содержащими ответ и обновлённую историю
        """
        # Попытка привязать текущий вопрос к предыдущей истории
        new_q = add_context_to_query(q, history=history, yandex_gpt=token)
        if "no data" not in new_q:
            q = new_q
        else:
            history = ""

        # Прогнозирование, как мог бы выглядеть вопрос иначе
        q_gen = predict_answer(q, yandex_gpt=token)

        # Поиск подходящих фрагментов по исходному и сгенерированному запросу
        q_docs = chunker.find_best_in_db(query=q, k=k)
        q_gen_docs = chunker.find_best_in_db(query=q_gen, k=k)

        # Объединение результатов поиска
        all_docs = []
        if isinstance(q_docs, list):
            all_docs.extend(q_docs)
        else:
            all_docs.append(q_docs)

        if isinstance(q_gen_docs, list):
            all_docs.extend(q_gen_docs)
        else:
            all_docs.append(q_gen_docs)

        # Ответ по документации
        answer = answer_with_documentation(all_docs, q, yandex_gpt=token)

        # Обновление истории
        history += f"Вопрос: {q}| Ответ: {answer}\n"

        return {
            "answer": answer if "К сожалению, я" not in answer else "К сожалению, я не владею данной информацией.",
            "history": history
        }

    @staticmethod
    def push_new_files_to_db(chunker: Chunker = Chunker()):
        """
        Метод добавления всех элементов папки rag/data/new_files в БД

        :param chunker: Объект класса Chunker для работы с векторной БД
        """
        chunker.add_file()
