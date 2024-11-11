from langchain_openai import ChatOpenAI
from typing import Optional, Any, List, Dict, ClassVar
from pydantic import BaseModel, Field
import os
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from langchain.schema import BaseMessage, SystemMessage, HumanMessage, AIMessage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class OpenRouterConfig(BaseModel):
    """Configuration for OpenRouter API."""
    api_key: str = Field(..., description="OpenRouter API key")
    base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenRouter API base URL"
    )
    max_retries: int = Field(
        default=3, 
        description="Maximum number of retry attempts",
        ge=1,  # Must be >= 1
        le=5   # Upper limit for retries
    )
    timeout: float = Field(
        default=30.0, 
        description="Request timeout in seconds",
        gt=0  # Must be > 0
    )

class ChatOpenRouter(ChatOpenAI):
    """Enhanced ChatOpenAI class for OpenRouter integration"""
    
    SUPPORTED_MODELS: ClassVar[List[str]] = [
        "google/gemma-2-9b-it:free",
        "liquid/lfm-40b:free",
        "nousresearch/hermes-3-llama-3.1-405b:free",
        "meta-llama/llama-3.1-405b-instruct:free",
        "gryphe/mythomax-l2-13b:free"
    ]

    def __init__(
        self,
        model_name: str,
        openai_api_key: Optional[str] = None,
        openai_api_base: str = "https://openrouter.ai/api/v1",
        config: Optional[OpenRouterConfig] = None,
        **kwargs: Any
    ):
        # Initialize configuration
        router_config = config or OpenRouterConfig(
            api_key=openai_api_key or os.getenv('OPENROUTER_API_KEY'),
            base_url=openai_api_base
        )
        
        self._validate_model(model_name)
        
        # Initialize parent class with router config values
        super().__init__(
            model_name=model_name,
            openai_api_base=router_config.base_url,
            openai_api_key=router_config.api_key,
            timeout=router_config.timeout,
            **kwargs
        )
        
        # Store config after parent initialization
        self._router_config = router_config

    def _validate_model(self, model_name: str) -> None:
        """Validate if the model is supported"""
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Model {model_name} not supported. "
                f"Supported models: {', '.join(self.SUPPORTED_MODELS)}"
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def agenerate_with_retry(self, messages: List[BaseMessage], *args, **kwargs) -> Any:
        """Async generation with retry logic and message conversion."""
        try:
        # Ensure messages are list of BaseMessage
            return await super().agenerate(messages=messages, *args, **kwargs)
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise

    def _convert_message_to_role(self, message: BaseMessage) -> str:
        """Convert a LangChain message type to an OpenAI role."""
        if isinstance(message, SystemMessage):
            return "system"
        elif isinstance(message, HumanMessage):
            return "user"
        elif isinstance(message, AIMessage):
            return "assistant"
        else:
            raise ValueError(f"Unknown message type: {type(message)}")

    @property
    def model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model_name": self.model_name,
            "api_base": self._router_config.base_url,
            "timeout": self._router_config.timeout,
            "max_retries": self._router_config.max_retries
        }

    @classmethod
    def list_supported_models(cls) -> List[str]:
        """Return list of supported models"""
        return cls.SUPPORTED_MODELS

    def update_config(self, **kwargs) -> None:
        """Update configuration parameters."""
        valid_keys = set(self._router_config.__fields__.keys())
        invalid_keys = set(kwargs.keys()) - valid_keys
        
        if invalid_keys:
            raise ValueError(
                f"Invalid configuration parameters: {', '.join(invalid_keys)}. "
                f"Valid parameters are: {', '.join(valid_keys)}"
            )
            
        for key, value in kwargs.items():
            setattr(self._router_config, key, value)