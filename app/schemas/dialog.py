"""
Общие модели данных для диалогов и диалоговых деревьев
"""
from typing import Optional, List, Dict
from pydantic import Field
from enum import Enum

from .schema import AutoPromptModel
from .character import Character


class BranchType(str, Enum):
    """Типы сюжетных ветвей диалога"""
    MAIN_PATH = ("main", "основная сюжетная линия к цели")
    EXPLORATION = ("exploration", "сюжетная контент-ветвь для изучения мира/NPC")
    DEAD_END = ("dead_end", "тупик, обрывающий диалог")
    LOOP_BACK = ("loop", "возвращает к одному из предыдущих узлов")
    SIDE_QUEST = ("side_quest", "редкая побочная сюжетная ветвь")

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def as_dict(cls) -> Dict:
        return {d.value: d.description for d in cls}

    @classmethod
    def as_prompt(cls) -> str:
        return "\n".join(
            f"- {d.value}: {d.description}"
            for d in cls
        )


class GoalCondition(AutoPromptModel):
    """Условие для достижения цели"""
    description: str = Field(..., description="Описание условия")
    cond_type: Optional[str] = Field(None, description="Тип условия")
    value: Optional[str] = Field(None, description="Значение условия")


class Goal(AutoPromptModel):
    """Цель диалога"""
    goal_type: str = Field(..., description="Тип цели (obtain_item, gather_information, etc.)")
    target: str = Field(..., description="Целевой объект или информация")
    conditions: Optional[List[GoalCondition]] = Field(default_factory=list, description="Условия достижения цели (когда диалог точно прерывается)")
    success_criteria: Optional[List[str]] = Field(default_factory=list, description="Критерии успеха (какие ноды считаем успешно завершенными)")
    difficulty: Optional[int] = Field(1, ge=1, le=5, description="Сложность достижения цели (число от 1 до 5)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "goal_type": "obtain_item",
                "target": "письмо",
                "conditions": [
                    {"description": "игрок должен доказать свою мудрость"},
                    {"description": "решить загадку"}
                ],
                "success_criteria": ["получить письмо", ],
                "difficulty": 2
            }
        }


class Constraints(AutoPromptModel):
    """Ограничения для генерации диалога"""   
    content_rating: Optional[str] = Field(None, description="Возрастной рейтинг контента")
    style: Optional[str] = Field(None, description="Стиль диалога (historical, fantasy, etc.)")


# TODO
class ChoiceEffect(AutoPromptModel):
    """Эффект выбора игрока"""
    efftype: Optional[str] = Field(..., description="Тип эффекта")
    target: Optional[str] = Field(..., description="Цель эффекта")
    value: Optional[str] = Field(None, description="Значение эффекта")


class Choice(AutoPromptModel):
    """Вариант выбора игрока"""
    text: str = Field(..., description="Текст выбора")
    next_node_id: str = Field(..., description="ID следующего узла")
    # conditions: Optional[List[GoalCondition]] = Field(default_factory=list, description="Условия")
    effects: Optional[List[ChoiceEffect]] = Field(default_factory=list, description="Эффекты при выборе")


class NodeMetadata(AutoPromptModel):
    """Метаданные узла диалога (состояние)"""
    branch_type: Optional[BranchType] = Field(default=BranchType.MAIN_PATH, description="Тип ветки")
    difficulty: Optional[int] = Field(None, ge=1, le=5, description="Предполагаемая сложность прохождения узла (число от 1 до 5)")
    goal_progress: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Прогресс к цели")  # TODO
    emotional_state: Optional[str] = Field(None, description="Эмоциональное состояние NPC")  # TODO
    required_items: Optional[List[str]] = Field(default_factory=list, description="Необходимые предметы")  # TODO
    unlocked_info: Optional[List[str]] = Field(default_factory=list, description="Разблокированная информация")  # TODO
    relationship_impact: Optional[Dict[str, float]] = Field(None, description="Влияние на отношения")   # TODO


class DialogBaseNode(AutoPromptModel):
    """Базовый класс для ноды диалогового дерева"""
    node_id: str = Field(..., description="Уникальный идентификатор текущей ноды")
    parent_node_ids: Optional[List[str]] = Field(default_factory=list, description="ID родительских узлов")
    child_node_ids: Optional[List[str]] = Field(default_factory=list, description="ID дочерних нод, на которые ведут варианты действий игрока")
    metadata: Optional[NodeMetadata] = Field(..., description="Метаданные текущей ноды")


class DialogTree(AutoPromptModel):
    """Диалоговое дерево"""
    root_node_id: str = Field(..., description="ID корневого узла")
    nodes: Dict[str, DialogBaseNode] = Field(..., description="Словарь узлов")
    goal_achievement_paths: Optional[List[List[str]]] = Field(None, description="Пути к достижению цели")
    validation_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Оценка валидации")
    metadata: Optional[Dict] = Field(None, description="Дополнительные метаданные для дерева")


class GenerationRequest(AutoPromptModel):
    """Базовый класс для запросов на генерацию"""
    character: Character = Field(..., description="Персонаж для диалога")
    goal: Goal = Field(..., description="Цель диалога")  # TODO: реализовать поддержку нескольких целей
    constraints: Optional[Constraints] = Field(None, description="Ограничения генерации")
    examples: Optional[List[Dict]] = Field(None, description="Примеры диалогов")


class GenerationResponse(AutoPromptModel):
    """Базовый класс для ответов после генерации"""
    dialog_tree: DialogTree = Field(..., description="Диалоговое дерево")
    logs: Optional[List[str]] = Field(None, description="Логи при заполнении")
    recommendations: Optional[List[str]] = Field(None, description="Рекомендации по улучшению")
    generation_time: Optional[float] = Field(None, description="Время заполнения в секундах")
