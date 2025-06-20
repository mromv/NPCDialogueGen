import asyncio
from app.schemas import (
    Character, Goal, Constraints,
    TreeGenerationRequest, TreeGenerationResponse,
    ContentGenerationRequest, ContentGenerationResponse,
)
from app.services.tree_generator import TreeGenerator
from app.services.content_writer import ContentWriter

async def test_dialog_generation():
    # generators init
    tree = TreeGenerator()
    content_writer = ContentWriter()

    # input example
    char = Character(**Character.Config.json_schema_extra["example"])
    goal = Goal(**Goal.Config.json_schema_extra["example"])
    const = Constraints(max_turns=5)

    request = TreeGenerationRequest(character=char, goal=goal, constraints=const)
    dialog_tree: TreeGenerationResponse = await tree.generate_structure_tree(request)

    content_request = ContentGenerationRequest(
        dialog_tree=dialog_tree.dialog_tree, 
        character=char
    )

    filled_dialog_tree: ContentGenerationResponse = await content_writer.fill_dialog_tree(
        request=content_request
    )

    print(filled_dialog_tree)
    return filled_dialog_tree

if __name__ == "__main__":
    asyncio.run(test_dialog_generation())
    