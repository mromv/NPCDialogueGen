import asyncio
from app.schemas import (
    Character, Goal, StructureConstraints,
    TreeGenerationRequest, ContentGenerationRequest,
    GenerationResponse
)
from app.services import TreeGenerator, ContentWriter


async def test_dialog_generation():
    # generators init
    tree = TreeGenerator()
    content_writer = ContentWriter()

    # input example
    character = Character(**Character.Config.json_schema_extra["example"])
    goal = Goal(**Goal.Config.json_schema_extra["example"])
    tree_constraints = StructureConstraints(max_turns=5)

    tree_request = TreeGenerationRequest(character=character, goal=goal, constraints=tree_constraints)
    dialog_tree: GenerationResponse = await tree.generate_structure_tree(tree_request)

    content_request = ContentGenerationRequest(
        dialog_tree=dialog_tree.dialog_tree,
        character=character,
        goal=goal,
    )

    filled_dialog_tree: GenerationResponse = await content_writer.fill_dialog_tree(
        request=content_request
    )

    print(filled_dialog_tree)
    return filled_dialog_tree

if __name__ == "__main__":
    asyncio.run(test_dialog_generation())
    