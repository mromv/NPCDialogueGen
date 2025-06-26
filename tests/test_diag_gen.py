import asyncio
from app.schemas import (
    Character, Goal, StructureConstraints,
    TreeGenerationRequest, TreeGenerationResponse,
    ContentGenerationRequest, ContentGenerationResponse,
    TreeValidationRequest, TreeValidationResponse
)
from app.services import (
    TreeGenerator, ContentWriter, TreeValidator
)


async def test_dialog_generation():
    # generators init
    tree = TreeGenerator()
    content_writer = ContentWriter()
    tree_validator = TreeValidator()

    # input example
    character = Character(**Character.Config.json_schema_extra["example"])
    goal = Goal(**Goal.Config.json_schema_extra["example"])
    tree_constraints = StructureConstraints(max_turns=5)

    # tree generation
    tree_request = TreeGenerationRequest(
        character=character,
        goal=goal, 
        onstraints=tree_constraints
    )
    dialog_tree: TreeGenerationResponse = await tree.generate_structure_tree(tree_request)

    # nodes content generation
    content_request = ContentGenerationRequest(
        dialog_tree=dialog_tree.dialog_tree,
        character=character,
        goal=goal,
    )

    filled_dialog_tree: ContentGenerationResponse = await content_writer.fill_dialog_tree(
        request=content_request
    )

    # tree validation
    tree_validation_request = TreeValidationRequest(
        character=character,
        goal=goal,
        constraints=tree_constraints,
        dialog_tree=filled_dialog_tree.dialog_tree
    )
    tree_validation: TreeValidationResponse = await tree_validator.validate(tree_validation_request)

    print(filled_dialog_tree)
    print(tree_validation)
    return filled_dialog_tree


if __name__ == "__main__":
    asyncio.run(test_dialog_generation())
    