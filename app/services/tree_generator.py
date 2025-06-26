"""
Генератор структуры диалогового дерева
"""
from typing import Dict, Any
from app.schemas import (
    NodeMetadata, DialogStructureNode, DialogStructureTree, 
    TreeGenerationRequest, TreeGenerationResponse
)
from app.utils import PromptFactory
from .llm_client import llm_clients


class TreeGenerator:
    """Генератор структуры диалогового дерева"""
    
    def __init__(self):
        self.llm = llm_clients.tree
    
    async def _generate_tree(
        self,
        request: TreeGenerationRequest
    ) -> Dict[str, Any]:
        """Возвращаем сырую сгенерированную структуру дерева"""
        prompt = PromptFactory.build_prompt("tree_generation", request=request)
        generated_tree = await self.llm.generate(
            prompt=prompt,
        )
        return generated_tree
    
    def _structure_tree(self, generated_tree: Dict[str, Any]) -> DialogStructureTree:
        """Преобразует сгенерированное дерево в DialogTree"""
        nodes = {}
        for node_id, node_info in generated_tree.get("nodes", {}).items():
            meta = node_info.get("metadata", {})
            node_info['metadata'] = NodeMetadata(
                **meta
            )
            
            nodes[node_id] = DialogStructureNode(
                **node_info
            )
        
        return DialogStructureTree(
            root_node_id=generated_tree["root_node_id"],
            nodes=nodes,
            goal_achievement_paths=generated_tree.get("goal_achievement_paths", [])
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
