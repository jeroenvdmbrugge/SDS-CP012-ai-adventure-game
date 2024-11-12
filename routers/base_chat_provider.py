from abc import ABC, abstractmethod
from typing import List
from langchain.schema import BaseMessage
from pydantic import SecretStr

class BaseChatProvider(ABC):
    """Abstract base class for chat providers"""
    
    @abstractmethod
    async def agenerate_with_retry(self, messages: List[List[BaseMessage]], *args, **kwargs):
        """Generate response with retry logic"""
        pass
    
    @abstractmethod
    def list_supported_models(self) -> List[str]:
        """List supported models for this provider"""
        pass
    
    @property
    @abstractmethod
    def model_info(self):
        """Get model information"""
        pass
