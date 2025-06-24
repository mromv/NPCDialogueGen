"""
Модели данных для генерации диалогового дерева
"""
from typing import Optional, List, Dict
from pydantic import Field

from .schema import AutoPromptModel
from .dialog import Constraints, Goal, DialogTree
from .character import Character


class TreeGenerationRequest(AutoPromptModel):
    """Запрос на генерацию диалога"""
    character: Character = Field(..., description="Персонаж для диалога")
    goal: Goal = Field(..., description="Цель диалога")  # TODO: реализовать поддержку нескольких целей
    constraints: Optional[Constraints] = Field(None, description="Ограничения генерации")
    examples: Optional[List[Dict]] = Field(None, description="Примеры диалогов")


class TreeGenerationResponse(AutoPromptModel):
    """Ответ со сгенерированным диалоговым деревом"""
    dialog_tree: DialogTree = Field(..., description="Сгенерированное диалоговое дерево")
    logs: Optional[List[str]] = Field(None, description="Логи генерации дерева")
    recommendations: Optional[List[str]] = Field(None, description="Рекомендации по улучшению")
    generation_time: Optional[float] = Field(None, description="Время генерации дерева в секундах")
