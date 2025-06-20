"""
Генератор структуры диалогового дерева
"""
from typing import Dict, Any, List, Optional
from app.schemas import (
    BranchType, DialogNode, DialogTree, NodeMetadata,
    TreeGenerationRequest, TreeGenerationResponse
)
from app.utils.prompts import PromptTemplates
from .llm_client import llm_clients


class TreeGenerator:
    """Генератор структуры диалогового дерева"""
    
    def __init__(self):
        self.llm = llm_clients.tree
    
    async def _generate_tree(
        self,
        request: TreeGenerationRequest
    ) -> Dict[str, Any]:
        """Возвращаем сырую сгенерированную структуру"""
        prompt = PromptTemplates.tree_generation_prompt(request)
        generated_tree = await self.llm.generate(
            prompt=prompt,
        )
        return generated_tree
    
    def _structure_tree(self, generated_tree) -> DialogTree:
        """Преобразует сгенерированное дерево в DialogTree"""
        nodes = {}
        for node_id, node_info in generated_tree.get("nodes", {}).items():
            branch_type = BranchType(node_info.get("branch_type", "main"))

            metadata = NodeMetadata(
                branch_type=branch_type,
                difficulty=node_info.get("level", 1)
            )
            
            nodes[node_id] = DialogNode(
                node_id=node_id,
                npc_text="",
                choices=[],
                metadata=metadata,
                parent_node_ids=node_info.get("parent_node_ids", []),
                child_node_ids=node_info.get("child_node_ids", []),
                narrative_summary=node_info.get("narrative_summary"),
                player_goal_hint=node_info.get("player_goal_hint")
            )
        
        return DialogTree(
            root_node_id=generated_tree["root_node_id"],
            nodes=nodes,
            goal_achievement_paths=generated_tree.get("estimated_paths_to_goal", [])
        )
    
    async def generate_structure_tree(
        self,
        request: TreeGenerationRequest
    ) -> TreeGenerationResponse:
        """Генерация DialogGenerationResponse"""
        generated_tree = await self._generate_tree(request)
        dialog_tree = self._structure_tree(generated_tree)
        return TreeGenerationResponse(
            dialog_tree=dialog_tree
        )
