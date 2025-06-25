"""
Контент-генератор для узлов дерева
"""
from app.schemas import (
    Choice, DialogNode, ContentGenerationRequest, GenerationResponse
)
from app.utils import PromptTemplates, bfs
from .llm_client import llm_clients


class ContentWriter:
    """Генерирует реплики и выборы для каждого узла в дереве"""

    def __init__(self):
        self.llm = llm_clients.content

    async def _generate_node(
        self,
        node: DialogNode,
        request: ContentGenerationRequest
    ) -> DialogNode:
        """Заполняет один узел содержимым (NPC-реплика и выборы игрока)"""
        prompt = PromptTemplates.node_content_prompt(
            current_node=node,
            request=request
        )

        response = await self.llm.generate(prompt=prompt)

        choices = [
            Choice(
                text=choice.get("text", ""),
                next_node_id=choice.get("next_node_id", "")
            ) for choice in response.get("choices", [])
        ]

        node = DialogNode(
            npc_text=response.get("npc_text", ""),
            choices=choices,
            **node.model_dump()
        )

        return node

    async def fill_dialog_tree(
        self, request: ContentGenerationRequest
    ) -> GenerationResponse:
        """Заполняет все узлы дерева контентом"""
        tree = request.dialog_tree
        for node in bfs(tree, yield_objects=True):
            filled_node = await self._generate_node(
                node=node,
                request=request
            )
            tree.nodes[node.node_id] = filled_node

        return GenerationResponse(
            dialog_tree=tree
        )
