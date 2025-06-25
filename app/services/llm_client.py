"""
Клиент для работы с OpenAI-совместимыми LLM API, включая DeepSeek
"""
import json
from typing import Dict, Any, Optional, List 
from openai import AsyncOpenAI

from app.utils import SystemPrompts, LLMConfig, settings


"""
TODO: 
1. Поддержку SO в gpt (универсально с DS).
2. Поддержку osmos - опционально выбирать из конфига как гиперпараметр.
"""

class LLMClient:
    """Гибкий клиент для OpenAI/DeepSeek с поддержкой структурированного вывода"""

    def __init__(self, config: Optional[LLMConfig] = None):
        config = config or settings.llm_base

        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens
    
    def resolve_generation_params(self, **kwargs) -> Dict[str, Any]:
        """Собираем параметры генерации"""
        return {
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "top_p": kwargs.get("top_p"),
            "frequency_penalty": kwargs.get("frequency_penalty"),
            "presence_penalty": kwargs.get("presence_penalty")
        }

    async def chat(
        self,
        messages: List[Dict[str, str]],
        response_format: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> str:
        """
        Общий метод для вызова chat completion

        :param messages: Список сообщений (roles: system/user/assistant)
        :param response_format: Формат ответа, например {"type": "json_object"} для структурированного вывода
        """
        params = self.resolve_generation_params(**kwargs)
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format=response_format,
                **params
            )
            return response.choices[0].message.content.strip() if response.choices[0].message.content else ""
        except Exception as e:
            raise RuntimeError(f"LLM API error: {str(e)}")

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Генерация обычного текста"""

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return await self.chat(messages, **kwargs)

    # реализовать через Osmos, а не json-схему
    async def generate_structured_output(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Генерация structured output через JSON-схему"""
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response_text = await self.chat(
            messages=messages,
            response_format={"type": "json_object"},
            **kwargs
        )

        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка разбора JSON: {str(e)}. Ответ: {response_text}")


class BaseLLMGenerator(LLMClient):
    """Базовый класс для специализированных генераторов"""

    def __init__(self, config: Optional[LLMConfig], system_prompt: str):
        super().__init__(config=config)
        self.system_prompt = system_prompt
    
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        return await self.generate_structured_output(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=kwargs.get('temperature'),
            **kwargs
        )


class TreeLLMGenerator(BaseLLMGenerator):
    """Клиент для генерации дерева диалогов"""
    def __init__(self):
        super().__init__(
            config=settings.llm_tree,
            system_prompt=SystemPrompts.tree_generation_prompt
        )


class NodeContentLLMGenerator(BaseLLMGenerator):
    """Клиент для генерации контента в нодах"""
    def __init__(self):
        super().__init__(
            config=settings.llm_content,
            system_prompt=SystemPrompts.content_generation_prompt
        )


# TODO
class MockLLMValidator(BaseLLMGenerator):
    """Реализовать набор клиентов-валидаторов"""
#    system_prompt=SystemPrompts.validation_prompt,
#    temperature=0.2
    pass

# TODO
class MockNodeLLMRegenerator(LLMClient):
    """Реализовать набор перегенерацию деревьев"""
#    system_prompt=SystemPrompts.improve_content_prompt,
#    temperature=0.5
    pass


class LLMClients:
    def __init__(self):
        self.base_client = LLMClient()
        self.tree = TreeLLMGenerator()
        self.content = NodeContentLLMGenerator()


llm_clients = LLMClients()
