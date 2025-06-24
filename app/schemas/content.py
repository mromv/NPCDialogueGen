"""
Модели данных для генерации контента
"""
from typing import Optional, List
from pydantic import Field

from .schema import AutoPromptModel
from .dialog import DialogTree
from .character import Character


class ContentGenerationRequest(AutoPromptModel):
    """Запрос на заполнение дерева"""
    dialog_tree: DialogTree = Field(..., description="Сгенерированное диалоговое дерево")
    character: Character = Field(..., description="Персонаж для диалога")
    # goal: Goal = Field(..., description="Цель диалога")  # TODO: реализовать поддержку нескольких целей (в промпт)


class ContentGenerationResponse(AutoPromptModel):
    """Ответ со сгенерированным диалоговым деревом с заполненным репликами"""
    dialog_tree: DialogTree = Field(..., description="Заполненное диалоговое дерево")
    logs: Optional[List[str]] = Field(None, description="Логи при заполнении")
    generation_time: Optional[float] = Field(None, description="Время заполнения в секундах")
