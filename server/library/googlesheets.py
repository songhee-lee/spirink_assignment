import os
from dotenv import load_dotenv
load_dotenv()
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

# 해당 클래스 정의
class Product:
    def __init__(self, category, name, regular_price, discount_price, brand, rating, url, image_url, stock, ranking):
        self.category = category
        self.name = name
        self.regular_price = regular_price
        self.discount_price = discount_price
        self.brand = brand
        self.rating = rating
        self.url = url
        self.image_url = image_url
        self.stock = stock
        self.ranking = ranking

    def get_text(self):
        # 필드를 하나의 텍스트로 반환. 여기서는 쉼표로 구분하여 반환된다고 가정
        return '\n'.join(f"{key}: {value}" for key, value in self.__dict__.items())


def read_sheets(spreadsheet_id):
    GOOGLE_AUTH_PATH = os.getenv("GOOGLE_AUTH_PATH")
    
    # 구글 스프레드시트 API 인증
    creds = Credentials.from_service_account_file(GOOGLE_AUTH_PATH, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    client = gspread.authorize(creds)

    # 스프레드시트 열기
    spreadsheet = client.open_by_key(spreadsheet_id)
    all_data = []

    # 각 시트의 데이터를 읽어오기
    for worksheet in spreadsheet.worksheets():
        records = worksheet.get_all_records()  # 각 시트의 모든 레코드를 가져옴
        for record in records:
            product = Product(
                record.get('소분류', ''), 
                record.get('제품명', ''),
                record.get('정가', 0),
                record.get('할인가', 0),
                record.get('브랜드', ''),
                record.get('고객 리뷰 별점', 0),
                record.get('URL', ''),
                record.get('이미지 URL', ''),
                record.get('재고', 0),
                record.get('랭킹', 0)
            )
            all_data.append(product)

    return all_data