import os
import chromadb
from get_project_root import root_path
from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import NodeWithScore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore


class Chunker:
    def __init__(self, path: str = root_path(ignore_cwd=False)):
        self.db = None
        self.vector_store = None
        self.chroma_collection = None
        self.storage_context = None
        self.embed_model = HuggingFaceEmbedding(model_name=CHUNKER_MODEL_NAME)
        self.data_path = RAG_DATA_PATH
        self.path = path
        self.data_path = os.path.join(path, "rag", "data")
        self.prepared_data_path = os.path.join(self.data_path, "prepared")
        self.new_data_path = os.path.join(self.data_path, "new_files")
        self.chroma_db_path = os.path.join(self.data_path, "chroma_db")
        self.chroma_collection_name = "default"
        self.host = "http://localhost:1234/v1"
        self.index = None

    def init_db(self, k: int):
        """
        Метод подгрузки индексов БД для ускоренной работы
        :param k: Искомое число чанков
        """
        if self.index is None:
            Settings.embed_model = self.embed_model
            self.db = chromadb.PersistentClient(path=self.chroma_db_path)
            self.chroma_collection = self.db.get_or_create_collection(self.chroma_collection_name)
            self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
            self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
            self.index = VectorStoreIndex.from_vector_store(
                self.vector_store, storage_context=self.storage_context, show_progress=True
            )
            self.retrieval_engine = self.index.as_retriever(
                similarity_top_k=k,
                choice_batch_size=k,
            )

    def add_file(self, path: str = ""):
        """
        Метод добавления всех файлов директории new_files в БД
        :param path: Путь до папки, если она будет отлична от стандартной
        """
        path = self.new_data_path if not path else path
        Settings.embed_model = self.embed_model
        documents = SimpleDirectoryReader(path).load_data()

        db_path = os.path.join(self.chroma_db_path, "chroma.sqlite3")
        db = chromadb.PersistentClient(path=db_path)
        chroma_collection = db.get_or_create_collection(self.chroma_collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        VectorStoreIndex.from_documents(
            documents=documents,
            storage_context=storage_context,
            show_progress=True
        )

    def create_chunk_db(self):
        """
        Метод создания базы данных из директории rag/data/prepared
        """
        Settings.embed_model = self.embed_model
        semantic_splitter = SemanticSplitterNodeParser(
            buffer_size=2,
            embed_model=self.embed_model
        )
        documents = SimpleDirectoryReader(self.prepared_data_path).load_data()
        nodes = semantic_splitter.get_nodes_from_documents(documents)

        db_path = os.path.join(self.chroma_db_path, "chroma.sqlite3")
        db = chromadb.PersistentClient(path=db_path)
        chroma_collection = db.get_or_create_collection(self.chroma_collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            show_progress=True
        )

        return index

    def find_best_in_db(self, query: str, k: int, min_score: float = 0.3) -> list[str]:
        """
        Метод поиска наилучших чанков в БД
        :param query: Текстовый запрос, относительно которого ищется документация
        :param k: Максимальное число найденных чанков
        :param min_score: Минимальный рейтинг чанка для добавления в выборку
        :return: Список из найденной документации
        """
        self.init_db(k)
        response = self.retrieval_engine.retrieve(query)

        def make_item(item: NodeWithScore) -> str:
            if item.score < min_score:
                return ""
            meta = item.metadata
            file_info = f"Файл {meta.get('file_name', 'неизвестно')}"
            if "page_label" in meta:
                file_info += f", страница {meta['page_label']}"
            creation_date = meta.get("creation_date", "неизвестна")
            return f"{file_info} | Дата создания: {creation_date}\nСодержание файла: {item.text}"

        return [text for item in response if (text := make_item(item))]

