"""
Модели данных для приложения
"""
from .character import Character
from .dialog import (
    BranchType, GoalCondition, Goal, Constraints, ChoiceEffect, 
    Choice, NodeMetadata, DialogBaseNode, DialogTree,
    GenerationRequest, GenerationResponse
)

from .tree import (
    StructureConstraints, DialogStructureNode, DialogStructureTree, TreeGenerationRequest
)

from .content_tree import (
    DialogNode, ContentGenerationRequest
)


__all__ = [
    'Character', 'BranchType', 'GoalCondition', 'Goal', 'Constraints', 'ChoiceEffect', 'Choice',
    'NodeMetadata', 'DialogBaseNode', 'DialogTree', 'GenerationRequest', 'GenerationResponse',
    'StructureConstraints', 'DialogStructureNode', 'DialogStructureTree', 'TreeGenerationRequest', 
    'DialogNode','ContentGenerationRequest'
]
