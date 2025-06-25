"""
Модели данных для генерации структуры диалогового дерева
"""
from typing import Optional
from pydantic import Field

from .dialog import (
    Constraints, DialogBaseNode, DialogTree, GenerationRequest
)


class StructureConstraints(Constraints):
    """Ограничения при генерации структуры дерева диалогов"""
    max_choices: Optional[int] = Field(3, description="Максимальное количество вариантов выбора для героя в ноде")
    min_choices: Optional[int] = Field(None, description="Минимальное количество вариантов выбора для героя в ноде")

    max_turns: Optional[int] = Field(5, description="Максимальное количество ходов - глубина дерева")
    min_turns: Optional[int] = Field(3, description="Минимальное количество ходов - мин. глубина самого короткого сюжета")

    n_storylines: Optional[int] = Field(1, description="Количество финалов - количество последних узлов дерева")
    min_storylines: Optional[int] = Field(None, description="Минимальное количество финалов")


class DialogStructureNode(DialogBaseNode):
    """Узел диалогового дерева после генерации его структуры"""
    narrative_summary: str = Field(..., description="Краткое описание происходящего события в узле")
    player_goal_hint: str = Field(..., 
        description="Возможная цель игрока в этом узле (может быть несколько вариантов, напр., получить информацию, предметы и т.д.)"
    )
    estimated_num_choices: Optional[int] = Field(None, ge=0, le=4, description="Количество вариантов ответа игрока в этом узле (число от 0 до 4)")

    class Config:
        json_schema_extra = {
            "example": {
                "node_id": "node_2",
                "metadata": {
                    "branch_type": "main",
                    "difficulty": 2,
                },
                "narrative_summary": "...",
                "player_goal_hint": "...",
                "estimated_num_choices": 2,
                "parent_node_ids": ["node_1"],
                "child_node_ids": ["node_4", "node_5"]
            }
        }


class DialogStructureTree(DialogTree):
    """Диалоговое дерево после генерации его структуры"""

    class Config:
        json_schema_extra = {
            "example": {
                "root_node_id": "node_1",
                "nodes": {
                    "node_1": {
                        "node_id": "node_1",
                        "metadata": {
                            "branch_type": "main",
                            "difficulty": 1,
                        },
                        "narrative_summary": "...",
                        "player_goal_hint": "...",
                        "estimated_num_choices": 2,
                        "parent_node_ids": [],
                        "child_node_ids": ["node_2", "node_3"]
                    },
                },
                "goal_achievement_paths": [["node_1", "node_3", "node_4"], ["node_1", "node_2"]]
            }
        }


class TreeGenerationRequest(GenerationRequest):
    """Запрос на генерацию диалога"""
    constraints: Optional[StructureConstraints] = Field(None, description="Ограничения при генерации дерева")
