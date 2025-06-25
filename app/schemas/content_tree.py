"""
Модели данных для генерации контента в узлах дерева диалогов
"""
from typing import Optional, List
from pydantic import Field

from .dialog import (
    Choice, DialogTree, GenerationRequest
)

from .tree import DialogStructureNode


class DialogNode(DialogStructureNode):
    """Узел диалогового дерева"""
    npc_text: Optional[str] = Field(default_factory=str, description="Реплика NPC (ее необходимо сгенерировать)")
    choices: Optional[List[Choice]] = Field(default_factory=list, description="Варианты ответов игрока (их необходимо сгенерировать)")

    class Config:
        json_schema_extra = {
            "example": {
                "npc_text": "...",
                "choices": [{
                    "text": "...",
                    "next_node_id": "node_2"
                }]
            },

            "node_structure": {
                "node_id": "node_2",
                "metadata": {
                    "branch_type": "main",
                    "difficulty": 2,
                },
                "narrative_summary": "...",
                "npc_text": "...",
                "player_goal_hint": "...",
                "choices": ["вариант ответа 1", "вариант ответа 2"],
                "estimated_num_choices": 2,
                "parent_node_ids": ["node_1"],
                "child_node_ids": ["node_4", "node_5"]
            }
        }


class ContentGenerationRequest(GenerationRequest):
    """Запрос на заполнение дерева"""
    dialog_tree: DialogTree = Field(..., description="Сгенерированное диалоговое дерево")
