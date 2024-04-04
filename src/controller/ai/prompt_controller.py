import httpx, uuid
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
            raise ValueError("An instance of PromptController already exists. Use PromptController.get_instance() to get that instance.")
        
        self.config = Config()
        self.client = httpx.Client(timeout=None)  # Set a reasonable timeout
        self.headers = {
            'Content-Type': 'application/json',
        }

    async def get_prompt(self, prompt: str) -> str:
        body, request_uuid = {"prompt": prompt}, uuid.uuid4()
        try:
            response = await self.client.post(self.config.api_endpoint, headers=self.headers, json=body)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for prompt with UUID {request_uuid}: {e}")
        except httpx.RequestError as e:
            logger.error(f"Request error for prompt with UUID {request_uuid}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for prompt with UUID {request_uuid}: {e}")
        return None

    def __del__(self):
        if self.client:
            self.client.aclose()  # Properly close the client on object deletion