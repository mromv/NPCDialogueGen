from typing import Dict, Any

from app.schemas import TreeValidationRequest, TreeValidationResponse
from app.utils import PromptFactory
from .llm_client import llm_clients


class TreeValidator:
    """Валидатор диалогового дерева"""
    def __init__(self):
        self.llm = llm_clients.tree_validator

    async def _gen_eval(self, request: TreeValidationRequest) -> Dict[str, Any]:
        """Генерация оценок"""
        prompt = PromptFactory.build_prompt("tree_validation", request=request)
        response = await self.llm.generate(prompt=prompt)
        return response
    
    async def validate(self, request: TreeValidationRequest) -> TreeValidationResponse:
        """Логика для определения флага валидности дерева"""
        gen_respose = await self._gen_eval(request)
        scores = gen_respose.get("scores")
        is_valid = False if min(scores.values()) <= 2. else True

        return TreeValidationResponse(
            is_valid=is_valid,
            **gen_respose
        )
