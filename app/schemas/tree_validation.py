from typing import Dict, Optional
from pydantic import Field

from .schema import AutoPromptModel
from .dialog import DialogBaseTree, GenerationBaseRequest
from .tree import StructureConstraints


class TreeValidationRequest(GenerationBaseRequest):
    """Запрос на валидацию дерева"""
    dialog_tree: DialogBaseTree = Field(..., description="Диалоговое дерево для валидации")
    constraints: Optional[StructureConstraints] = Field(None, description="Ограничения при генерации дерева")


class TreeValidationResponse(AutoPromptModel):
    """Результат валидации дерева по чеклисту"""
    scores: Dict[str, int] = Field(..., description="Оценки по чеклисту (1-5)")
    comments: Dict[str, str] = Field(..., description="Комментарии к решению")
    is_valid: Optional[bool] = Field(None, description="Результат валидации (True/False)")
