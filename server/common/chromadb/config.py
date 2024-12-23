import os
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()

from library.googlesheets import get_google_sheets_data

class ProductSettings :
    """
    상품에 대한 정보
    """
    COLLECTION_PATH : str

    def __init__(self, collection_path, collection_name, **kwargs) :
        super().__init__(**kwargs)
        
        # 구글 스프레드 시트 별로 상품 정보 받아오기
        GOOGLE_SPREADSHEET_ID_PATH = os.getenv("GOOGLE_SPREADSHEET_ID_PATH")
        spreadsheet_ids = open(GOOGLE_SPREADSHEET_ID_PATH, 'r').readlines()
        self.DATA = []
        for spreadsheet_id in spreadsheet_ids:
            self.DATA.extend(get_google_sheets_data(spreadsheet_id.strip()))
        
        # 상품 정보를 저장할 경로
        self.COLLECTION_PATH = f"{collection_path}/{collection_name}.pkl"


class DatabaseSettings :
    CHROMADB_PATH : str = os.getenv("CHROMADB_PATH")

    PRODUCTS : ProductSettings
    
    def __init__(self, **kwargs) :
        super().__init__(**kwargs)
        self.PRODUCTS = ProductSettings(self.CHROMADB_PATH, "PRODUCTS")
        self.collections = self._initialize_collections()
    
    def _initialize_collections(self) -> Dict[str, Any] :
        """
        DB에 대한 정보를 제외하고 필드 초기화
        """
        collections = {}
        for attr_name, attr_type in self.__annotations__.items():
            if "DB" in attr_name :   # 예외 처리
                continue
            collections[attr_name.lower()] = getattr(self, attr_name)

        return collections

    def get_collection_info(self, collection_name : str) -> Dict[str, Any] :
        """
        특정 collection 불러오기
        """
        return self.collections.get(collection_name.lower(), None)

chromadb_settings = DatabaseSettings()