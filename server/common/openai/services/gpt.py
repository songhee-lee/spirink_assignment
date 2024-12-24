import openai
from typing import List, Dict, Any

from common.openai.config import openai_settings
from common.logging.config import setup_logging

logger = setup_logging(__name__)

class LLM:
    def set_api_key(self, api_key: str) -> bool:
        """
        api key 연결 확인하고 세팅하기
        """
        # 1) api 세팅
        self.api_key = api_key
        openai.api_key = api_key

        # 2) api key 맞는지 확인
        try :
            openai.Engine.list()
            return True
        except openai.error.AuthenticationError as e:
            logger.error(f"OpenAI AuthenticationError : {str(e)}")
            return False

    def generate(self, messages: List[Dict[str, Any]]) -> str:
        """
        llm 답변 받기 
        messages : 전체 채팅 메세지
        """
        response = openai.ChatCompletion.create(
            model=openai_settings.OPENAI_LLM_MODEL,
            messages=messages,
            temperature=openai_settings.OPENAI_LLM_TEMPERATURE,
            max_tokens=openai_settings.OPENAI_LLM_MAX_TOKENS
        )

        try :
            return response.choices[0].message["content"]
        except :
            logger.error(f"response is not valid. {response}")
            return {}

openai_llm = LLM()