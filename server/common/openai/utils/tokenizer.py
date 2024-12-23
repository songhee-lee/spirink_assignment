from typing import List, Dict
import tiktoken

from common.openai.config import openai_settings

class Tokenizer :
    """
    토크나이저
    """
    def __init__(self) :
        self.tokenizer = tiktoken.get_encoding(openai_settings.OPENAI_TOKENIZER_MODEL)

    def chunk_text(self, text: str, max_tokens: int) -> Dict[str, List] :
        """
        텍스트를 토큰에 맞게 청킹하기
        text : 텍스트
        max_tokens : 토크나이저의 최대 토큰 개수
        """
        tokens = self.tokenizer.encode(text)
        
        # text를 chunk로 분할
        chunks = []
        for i in range(0, len(tokens), max_tokens) :
            chunk_tokens = tokens[i:i+max_tokens]
            chunks.append(self.tokenizer.decode(chunk_tokens))

        return chunks

    def tokenize_text(self, text: str) -> int :
        """
        텍스트를 토큰화 하기
        text : 텍스트
        """
        tokens = self.tokenizer.encode(text)
        return len(tokens)

openai_tokenizer = Tokenizer()