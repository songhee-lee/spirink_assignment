import anthropic
import requests
from typing import List, Dict, Any

from common.anthropic.config import anthropic_settings
from common.logging.config import setup_logging

logger = setup_logging(__name__)

class LLM:
    client = anthropic.Anthropic(
        api_key=anthropic_settings.CLAUDE_API_KEY
    )

    def set_api_key(self, api_key: str) -> bool:
        """
        api key 연결 확인하고 세팅하기
        """
        # 1) api 세팅
        self.api_key = api_key
        anthropic.api_key = self.api_key

        # 2) api key 맞는지 확인
        try :
            headers = {"Authorization" : f"Bearer {self.api_key}"}
            response = requests.get(anthropic_settings.ANTHROPIC_VERIFY_URL, headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Anthropic Authentication Error: {str(e)}")
            return False
        
    def generate(self, messages: List[Dict[str, Any]]) -> str:
        """
        llm 답변 받기 
        messages : 전체 채팅 메세지
        """
        try :
            messages = check_max_tokens(messages, anthropic_settings.ANTHROPIC_LLM_MAX_TOKENS)

            response = self.client.messages.create(
                model=anthropic_settings.ANTHROPIC_LLM_MODEL,
                max_tokens=anthropic_settings.ANTHROPIC_LLM_MAX_TOKENS,
                temperature=anthropic_settings.ANTHROPIC_LLM_TEMPERATURE,
                messages=messages
            )
            return response.content[0].text
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to generate response: {str(e)}")
            return {}

anthropic_llm = LLM()