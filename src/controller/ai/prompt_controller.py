import httpx
from loguru import logger
from src.helper.config import Config

class PromptController:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise ValueError("An instance of PromptController already exists.")
        
        self.config = Config()
        self.client = httpx.AsyncClient(timeout=None)  # Use AsyncClient
        self.headers = {'Content-Type': 'application/json'}

    async def send_prompt(self, prompt: str) -> str:
        body = {"prompt": prompt}
        try:
            response = await self.client.post(self.config.api_endpoint, headers=self.headers, json=body)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"Prompt HTTP Error: {e}")
        except httpx.RequestError as e:
            logger.error(f"Prompt Request Error: {e}")
        except Exception as e:
            logger.error(f"Unexpected prompt error: {e}")
        return None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=None)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()