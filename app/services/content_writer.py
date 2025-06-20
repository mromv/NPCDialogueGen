"""
Контент-генератор для узлов дерева
"""
from app.schemas import (
    Choice, DialogNode, ContentGenerationRequest, ContentGenerationResponse
)
from app.utils.prompts import PromptTemplates
from .llm_client import llm_clients


class ContentWriter:
    """Генерирует реплики и выборы для каждого узла в дереве"""

    def __init__(self):
        self.llm = llm_clients.content

    # зарефакторить аргументы и модели данных к ним
    async def _generate_node(
        self,
        node: DialogNode,
        request: ContentGenerationRequest
    ) -> DialogNode:
        """Заполняет один узел содержимым (NPC-реплика и выборы игрока)"""
        tree = request.dialog_tree
        previous_nodes = [
            tree.nodes[nid]
            for nid in node.parent_node_ids
            if nid in tree.nodes
        ]

        prompt = PromptTemplates.node_content_prompt(
            current_node=node,
            previous_nodes=previous_nodes,
            character=request.character
        )

        response = await self.llm.generate(prompt=prompt)

        node.npc_text = response.get("npc_text", "")
        node.choices = [
            Choice(
                text=choice.get("text", ""),
                next_node_id=choice.get("next_node_id", "")
            )
            for choice in response.get("choices", [])
        ]

        return node

    async def fill_dialog_tree(
        self, request: ContentGenerationRequest
    ) -> ContentGenerationResponse:
        """Заполняет все узлы дерева контентом"""
        tree = request.dialog_tree
        for node_id, node in tree.nodes.items():
            filled_node = await self._generate_node(
                node=node,
                request=request
            )
            tree.nodes[node_id] = filled_node

        return ContentGenerationResponse(
            dialog_tree=tree
        )
