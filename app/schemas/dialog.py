"""
Модели данных для диалогов и диалоговых деревьев
"""
from pydantic import Field
from typing import List, Dict, Optional
from enum import Enum

from .schema import AutoPromptModel
from .character import Character


class BranchType(str, Enum):
    """Типы веток диалога"""
    MAIN_PATH = "main"  # основная сюжетная линия диалога, ведущая к главной цели
    EXPLORATION = "exploration"  # ветки для изучения мира/персонажа
    DEAD_END = "dead_end"  # тупиковая ветка, обрывающая диалог
    LOOP_BACK = "loop"  # ветки, возвращающие игрока к предыдущим нодам
    SIDE_QUEST = "side_quest"  # что-нибудь редкое


class GoalCondition(AutoPromptModel):
    """Условие для достижения цели"""
    description: str = Field(..., description="Описание условия")
    cond_type: Optional[str] = Field(None, description="Тип условия")
    value: Optional[str] = Field(None, description="Значение условия")


class Goal(AutoPromptModel):
    """Цель диалога"""
    type: str = Field(..., description="Тип цели (obtain_item, gather_information, etc.)")
    target: str = Field(..., description="Целевой объект или информация")
    conditions: Optional[List[GoalCondition]] = Field(default_factory=list, description="Условия достижения цели (когда диалог точно прерывается)")
    success_criteria: Optional[List[str]] = Field(default_factory=list, description="Критерии успеха (какие ноды считаем успешно завершенными)")
    difficulty: Optional[int] = Field(1, ge=1, le=5, description="Сложность достижения цели")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "obtain_item",
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
    max_turns: Optional[int] = Field(5, description="Максимальное количество ходов - глубина дерева")
    min_turns: Optional[int] = Field(3, description="Минимальное количество ходов - мин. глубина самого короткого сюжета")
    n_storylines: Optional[int] = Field(1, description="Количество финалов")
    min_storylines: Optional[int] = Field(3, description="Минимальное количество финалов")
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
    difficulty: Optional[int] = Field(None, ge=1, le=5, description="Сложность узла")
    goal_progress: Optional[float] = Field(default=0.0, ge=0.0, le=1.0, description="Прогресс к цели")  # TODO
    emotional_state: Optional[str] = Field(None, description="Эмоциональное состояние NPC")  # TODO
    required_items: Optional[List[str]] = Field(default_factory=list, description="Необходимые предметы")  # TODO
    unlocked_info: Optional[List[str]] = Field(default_factory=list, description="Разблокированная информация")  # TODO
    relationship_impact: Optional[Dict[str, float]] = Field(None, description="Влияние на отношения")   # TODO


class DialogNode(AutoPromptModel):
    """Узел диалогового дерева"""
    node_id: str = Field(..., description="Уникальный идентификатор узла")
    npc_text: Optional[str] = Field(default_factory=str, description="Реплика NPC")
    choices: Optional[List[Choice]] = Field(default_factory=list, description="Варианты ответов игрока")
    metadata: Optional[NodeMetadata] = Field(..., description="Метаданные узла")

    parent_node_ids: Optional[List[str]] = Field(default_factory=list, description="ID родительских узлов")
    child_node_ids: Optional[List[str]] = Field(default_factory=list, description="ID дочерних узлов")

    narrative_summary: Optional[str] = Field(None, description="Краткое описание происходящего в узле")
    player_goal_hint: Optional[str] = Field(None, description="Что игрок, вероятно, попытается сделать на этом этапе")


class DialogTree(AutoPromptModel):
    """Диалоговое дерево"""
    root_node_id: str = Field(..., description="ID корневого узла")
    nodes: Dict[str, DialogNode] = Field(..., description="Словарь узлов")
    goal_achievement_paths: Optional[List[List[str]]] = Field(None, description="Пути к достижению цели")
    validation_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Оценка валидации")
    metadata: Optional[Dict] = Field(None, description="Дополнительные метаданные для дерева")


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


# TODO: здесь требуется разбиение на более мелкие классы (и в промпт цель прокинуть)
class ContentGenerationRequest(AutoPromptModel):
    """Запрос на заполнение дерева"""
    dialog_tree: DialogTree = Field(..., description="Сгенерированное диалоговое дерево")
    character: Character = Field(..., description="Персонаж для диалога")
    # goal: Goal = Field(..., description="Цель диалога")  # TODO: реализовать поддержку нескольких целей


class ContentGenerationResponse(AutoPromptModel):
    """Ответ со сгенерированным диалоговым деревом с заполненным репликами"""
    dialog_tree: DialogTree = Field(..., description="Заполненное диалоговое дерево")
    logs: Optional[List[str]] = Field(None, description="Логи при заполнении")
    generation_time: Optional[float] = Field(None, description="Время заполнения в секундах")
