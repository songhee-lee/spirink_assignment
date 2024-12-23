import os
import pickle
import chromadb
from typing import List

from server.common.chromadb.config import chromadb_settings
from server.common.openai.services.embedding import text_to_embedding
from server.common.logging.config import setup_logging

logger = setup_logging(__name__)

class DataBase :
    def load_data(self, file_path) :
        """
        저장된 DB 불러오기
        """
        if os.path.exists(file_path) :
            with open(file_path, "rb") as f :
                return pickle.load(f)
        return False

    def add_to_chromadb(self, documents: List[str], embeddings: List[List[float]], ids: List[str]) -> None:
        """
        ChromaDB에 데이터 추가
        documents: 문서 리스트
        embeddings: 문서 임베딩 리스트
        """
        self.collection.add(
            documents=documents, 
            embeddings=embeddings,
            ids=ids
        )

    def load_database(self, collection_name : str) :
        """
        DB 기본 세팅
        """

        # ChromaDB 클라이언트 설정
        logger.debug(f"ChromaDB client set : {chromadb_settings.CHROMADB_PATH}")
        client = chromadb.PersistentClient(path=chromadb_settings.CHROMADB_PATH)
        try :
            self.collection = client.get_collection(collection_name)
            logger.debug(f"Load {collection_name}...")
        
        except Exception :
            # ChromaDB 클라이언트 생성하기
            self.collection = client.create_collection(collection_name)
            collection_info = chromadb_settings.get_collection_info(collection_name)

            # 기존에 저장된 collection이 있는지 확인하기
            collection_data = self.load_data(collection_info.COLLECTION_PATH)
            if collection_data :
                logger.debug("기존 DB 로딩...")
                self.add_to_chromadb(collection_data["documents"], collection_data["embeddings"], collection_data["ids"]) 
            
            # 새로운 collection에 임베딩 데이터 추가하기
            else :
                data = collection_info.DATA
                if not data :
                    return False
                
                documents = []
                embeddings = []
                ids = []
                
                for idx, d in enumerate(data):
                    text = d.get_text()
                    embedding = text_to_embedding(text)
                    documents.append(text)
                    embeddings.append(embedding)
                    ids.append(str(idx))

                logger.debug("새로운 DB 생성...")
                self.add_to_chromadb(documents, embeddings, ids)

                # DB 저장하기
                with open(collection_info.COLLECTION_PATH, "wb") as f:
                    pickle.dump({"documents" : documents, "embeddings" : embeddings, "ids":ids}, f)
        return self.collection
        
    def get_relevant_context(self, collection_name, query: str, k=3) -> List[str]:
        """
        RAG - 관련 컨텍스트 찾기
        query: 사용자 쿼리
        """
        self.load_database(collection_name)

        query_embedding = text_to_embedding(query)
        result = self.collection.query(query_embeddings=[query_embedding], n_results=k)
        logger.debug(f"RAG 응답\n- query: {query}\n- response: {result}")
        return [doc[0] for doc in result["documents"]]


# DB 인스턴스 생성
chroma_db = DataBase()