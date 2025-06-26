"""
Шаблоны динамических промптов для LLM
"""
from abc import ABC, abstractmethod

import json
from typing import List, Literal
from pathlib import Path
from .tree_iterator import get_ancestors, bfs
from app.schemas import (
    BranchType, DialogBaseNode, DialogNode, 
    DialogStructureNode, DialogStructureTree,
    TreeGenerationRequest, ContentGenerationRequest,
    TreeValidationRequest
)

PromptType = Literal["tree_generation", "node_content", "tree_validation"]


class BasePrompt(ABC):
    """Базовый класс для всех промптов"""
    _prompt_dir = Path("app/prompts")

    @classmethod
    def _load_template(cls, filename: str) -> str:
        """Подгружаем текстовый шаблон промпта"""
        path = cls._prompt_dir / filename
        with path.open("r", encoding="utf-8") as file:
            content = file.read()
        return content

    @classmethod
    def _json_nodes(cls, nodes: List[DialogBaseNode], separator: str = ",\n") -> str:
        """Возвращаем промпт с нодами в json-формате"""
        return separator.join(
            json.dumps(node.model_dump(), indent=2, ensure_ascii=False)
            for node in nodes
        )

    @classmethod
    @abstractmethod
    def build(cls, *args, **kwargs) -> str:
        """Генерация финального промпта"""
        ...


class TreeGenerationPrompt(BasePrompt):
    """Генерация дерева"""
    @classmethod
    def build(cls, request: TreeGenerationRequest) -> str:
        template = cls._load_template("tree.txt")

        # примеры заполнения ноды и дерева
        node_example = DialogStructureNode.model_json_schema().get("example")
        tree_example = DialogStructureTree.model_json_schema().get("example")

        data = {
            "character": request.character.as_prompt(),
            "goal": request.goal.as_prompt(),
            "constraints": request.constraints.as_prompt(),
            "branch_types": BranchType.as_prompt(),
            "node_description": DialogStructureNode.model_description(),
            "node_example": json.dumps(node_example, indent=2, ensure_ascii=False),
            "tree_example": json.dumps(tree_example, indent=2, ensure_ascii=False),
        }

        return template.format(**data)


class NodeContentPrompt(BasePrompt):
    """Заполнение нод дерева"""
    max_child_depth = 1

    @classmethod
    def build(cls, current_node: DialogNode, request: ContentGenerationRequest) -> str:
        template = cls._load_template("content_generation.txt")

        tree = request.dialog_tree

        # история и дальнейшая развилка диалога
        ancestors = get_ancestors(tree, current_node.node_id, return_objects=True)
        children = list(
            bfs(tree, current_node.node_id, max_depth=cls.max_child_depth,
                yield_objects=True, exclude_start_node=True)
        )

        example = DialogNode.model_json_schema().get("example")

        data = {
            "character": request.character.as_prompt(),
            "goal": request.goal.as_prompt(),
            "branch_types": BranchType.as_prompt(),
            "node_description": DialogNode.model_description(),
            "history": cls._json_nodes(ancestors) if ancestors else "Это начало диалога.",
            "postfix": cls._json_nodes(children) if children else "Это конец диалога.",
            "node_content": current_node.as_prompt(exclude_none=False),  # include none, чтобы пустые списки попали в промпт
            "response_example": json.dumps(example, indent=2, ensure_ascii=False),
        }

        return template.format(**data)


class TreeValidationPrompt(BasePrompt):
    """Валидация заполненного дерева"""
    @classmethod
    def build(cls, request: TreeValidationRequest) -> str:
        template = cls._load_template("tree_validation.txt")

        data = {
            "character": request.character.as_prompt(),
            "goal": request.goal.as_prompt(),
            "branch_types": BranchType.as_prompt(),
            "constraints": request.constraints.as_prompt(),
            "node_description": DialogNode.model_description(),
            "dialog_tree": json.dumps(request.dialog_tree.model_dump(), indent=2, ensure_ascii=False),
        }

        return template.format(**data)


class PromptFactory:
    @staticmethod
    def build_prompt(prompt_type: PromptType, **kwargs) -> str:
        if prompt_type == "tree_generation":
            request: TreeGenerationRequest = kwargs["request"]
            return TreeGenerationPrompt.build(request)

        elif prompt_type == "node_content":
            current_node: DialogNode = kwargs["current_node"]
            request: ContentGenerationRequest = kwargs["request"]
            return NodeContentPrompt.build(current_node, request)

        elif prompt_type == "tree_validation":
            request: TreeValidationRequest = kwargs["request"]
            return TreeValidationPrompt.build(request)

        else:
            raise ValueError(f"Unknown prompt_type: {prompt_type}")
