"""
Шаблоны динамических промптов для LLM
"""
import json
from .tree_iterator import get_ancestors
from app.schemas import (
    BranchType, DialogNode, 
    DialogStructureNode, DialogStructureTree,
    TreeGenerationRequest, ContentGenerationRequest,
    TreeValidationRequest
)


class PromptTemplates:
    """Коллекция шаблонов промптов для различных задач"""

    tree_prompt_path = "app/prompts/tree.txt"
    content_generation_prompt_path = "app/prompts/content_generation.txt"
    tree_validator_prompt_path = "app/prompts/tree_validation.txt"
        
    @staticmethod
    def tree_generation_prompt(
        request: TreeGenerationRequest
    ) -> str:
        with open(PromptTemplates.tree_prompt_path, "r", encoding="utf-8") as file:
            prompt_template = file.read()
        
        # пример ноды и дерева
        node_example = DialogStructureNode.model_json_schema().get('example')
        tree_example = DialogStructureTree.model_json_schema().get('example')
        
        data = {
            "character": request.character.as_prompt(),
            "goal": request.goal.as_prompt(),
            "constraints": request.constraints.as_prompt(),
            "branch_types": BranchType.as_prompt(),
            "node_description": DialogStructureNode.model_description(),
            "node_example": json.dumps(node_example, indent=2, ensure_ascii=False),
            "tree_example": json.dumps(tree_example, indent=2, ensure_ascii=False),
        }

        return prompt_template.format(**data)

    @staticmethod
    def node_content_prompt(
        current_node: DialogNode,
        request: ContentGenerationRequest
    ) -> str:
        with open(PromptTemplates.content_generation_prompt_path, "r", encoding="utf-8") as file:
            prompt_template = file.read()
        
        tree = request.dialog_tree
        ancestors = get_ancestors(tree, current_node.node_id, True)
        if ancestors:
            history = ",\n".join([
                json.dumps(node.model_dump(), indent=2, ensure_ascii=False)
                for node in ancestors
            ])
        else:
            history = "Это начало диалога."
        
        # пример диалоговой ноды, которую необходимо сгенерировать
        example = DialogNode.model_json_schema().get('example')

        data = {
            "character": request.character.as_prompt(),
            "goal": request.goal.as_prompt(),
            "branch_types": BranchType.as_prompt(),
            "node_description": DialogNode.model_description(),
            "history": history,
            "node_content": current_node.as_prompt(),
            "response_example": json.dumps(example, indent=2, ensure_ascii=False),
        }

        return prompt_template.format(**data)
    
    @staticmethod
    def tree_validation_prompt(
        request: TreeValidationRequest
    ) -> str:
        """Генерирует промпт для валидации дерева по чеклисту"""
        with open(PromptTemplates.tree_validator_prompt_path, "r", encoding="utf-8") as file:
            prompt_template = file.read()
        
        dialog_tree = request.dialog_tree.model_dump()
        
        data = {
            "character": request.character.as_prompt(),
            "goal": request.goal.as_prompt(),
            "branch_types": BranchType.as_prompt(),
            "node_description": DialogNode.model_description(),
            "constraints": request.constraints.as_prompt(),
            "dialog_tree": json.dumps(dialog_tree, indent=2, ensure_ascii=False),
        }
        
        return prompt_template.format(**data)
