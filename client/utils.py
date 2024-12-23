import requests
import os
from dotenv import load_dotenv
load_dotenv()

def send_api(data, path) :
    """
    API 요청 보내는 함수
    data : request data
    path : API 경로
    """
    url = os.getenv('API_HOST') + path
    headers = {
        "Content-Type" :  "application/json", 
        "accept" : "application/json"
    }

    try :
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e :
        return {"error" : e}