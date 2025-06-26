"""
Модели данных для приложения
"""
from .character import Character
from .dialog import (
    BranchType, GoalCondition, Goal, Constraints, ChoiceEffect, 
    Choice, NodeMetadata, DialogBaseNode, DialogBaseTree
)

from .tree import (
    StructureConstraints, DialogStructureNode, DialogStructureTree, 
    TreeGenerationRequest, TreeGenerationResponse
)

from .content_tree import (
    DialogNode, DialogTree, ContentGenerationRequest, ContentGenerationResponse
)

from .tree_validation import (
    TreeValidationRequest, TreeValidationResponse
)


__all__ = [
    'Character', 'BranchType', 'GoalCondition', 'Goal', 'Constraints', 'ChoiceEffect',
    'Choice', 'NodeMetadata', 'DialogBaseNode', 'DialogBaseTree',
    'StructureConstraints', 'DialogStructureNode', 'DialogStructureTree', 'TreeGenerationRequest', 'TreeGenerationResponse',
    'DialogNode', 'DialogTree', 'ContentGenerationRequest', 'ContentGenerationResponse',
    'TreeValidationRequest', 'TreeValidationResponse'
]
