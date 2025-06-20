"""
Модели данных для приложения
"""
from .character import Character, PlayerProfile
from .dialog import (
    BranchType, GoalCondition, Goal, Constraints, ChoiceEffect, Choice,
    NodeMetadata, DialogNode, DialogTree,
    TreeGenerationRequest, TreeGenerationResponse,
    ContentGenerationRequest, ContentGenerationResponse
)

__all__ = [
    # Character models
    'Character', 'PlayerProfile',
    
    # Dialog models
    'BranchType', 'GoalCondition', 'Goal', 'Constraints', 'ChoiceEffect', 'Choice',
    'NodeMetadata', 'DialogNode', 'DialogTree', 'TreeGenerationRequest', 'TreeGenerationResponse',
    'ContentGenerationRequest', 'ContentGenerationResponse'
]

