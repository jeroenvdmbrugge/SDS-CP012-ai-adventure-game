from abc import ABC, abstractmethod
from typing import List, Dict, Any, ClassVar
from langchain.schema import BaseMessage, SystemMessage, HumanMessage, AIMessage
from pydantic import SecretStr

class BaseChatProvider(ABC):
    """Abstract base class for chat providers"""
    
    SUPPORTED_MODELS: ClassVar[List[str]] = []
    
    @abstractmethod
    async def agenerate_with_retry(self, messages: List[List[BaseMessage]], *args, **kwargs):
        """Generate response with retry logic"""
        pass
    
    @classmethod
    def list_supported_models(cls) -> List[str]:
        """List supported models for this provider"""
        return cls.SUPPORTED_MODELS
    
    @property
    @abstractmethod
    def model_info(self) -> Dict[str, Any]:
        """Get model information"""
        pass

    def _validate_model(self, model_name: str) -> None:
        """Validate if the model is supported"""
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Model {model_name} not supported. "
                f"Supported models: {', '.join(self.SUPPORTED_MODELS)}"
            )

    @staticmethod
    def _convert_message_to_role(message: BaseMessage) -> str:
        """Convert a LangChain message type to an OpenAI role."""
        if isinstance(message, SystemMessage):
            return "system"
        elif isinstance(message, HumanMessage):
            return "user"
        elif isinstance(message, AIMessage):
            return "assistant"
        else:
            raise ValueError(f"Unknown message type: {type(message)}")
