"""
Модели данных для приложения
"""
from .character import Character
from .dialog import (
    BranchType, GoalCondition, Goal, Constraints, ChoiceEffect, Choice,
    NodeMetadata, DialogNode, DialogTree    
)

from .tree import (
    TreeGenerationRequest, TreeGenerationResponse
)

from .content import (
    ContentGenerationRequest, ContentGenerationResponse
)

__all__ = [
    'Character', 'BranchType', 'GoalCondition', 'Goal', 'Constraints', 'ChoiceEffect', 'Choice',
    'NodeMetadata', 'DialogNode', 'DialogTree', 'TreeGenerationRequest', 'TreeGenerationResponse',
    'ContentGenerationRequest', 'ContentGenerationResponse',
]
