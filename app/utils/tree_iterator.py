"""
Вспомогательные функции для работы с деревом диалогов
"""
from collections import deque
from typing import Optional, List, Tuple, Set, Union, Iterator
from app.schemas import DialogBaseNode, DialogBaseTree


def get_ancestors(
    tree: DialogBaseTree,
    node_id: str,
    max_depth: Optional[int] = None,
    return_objects: bool = False
) -> List[List[str]]:
    """Возвращает все пути от предков до текущего узла не включительно"""
    if node_id not in tree.nodes:
        raise ValueError(f"Node {node_id} is not found in {tree}")

    visited: Set[str] = set()
    ancestors = []
    queue: List[Tuple[str, int]] = [(node_id, 0)]

    while queue:
        current_id, depth = queue.pop(0)
        current_node = tree.nodes.get(current_id)

        if not current_node:
            continue

        if max_depth is not None and depth >= max_depth:
            continue

        for parent_id in current_node.parent_node_ids:
            if parent_id not in visited:
                visited.add(parent_id)
                ancestors.append(parent_id)
                queue.append((parent_id, depth + 1))

    ancestors = ancestors[::-1]

    if return_objects:
        return [tree.nodes[id_] for id_ in ancestors]

    return ancestors


def bfs(
    tree: DialogBaseTree,
    start_node_id: Optional[str] = None,
    max_depth: Optional[int] = None,
    yield_objects: bool = False,
    exclude_start_node: bool = False
) -> Iterator[Union[DialogBaseNode, str]]:
    """Обход дерева в ширину с ограничением по глубине"""
    visited = set()
    queue = deque()

    def enqueue(node_id: str, depth: int):
        if node_id not in visited and node_id in tree.nodes:
            visited.add(node_id)
            queue.append((node_id, depth))

    if start_node_id is not None:
        if start_node_id in tree.nodes:
            enqueue(start_node_id, 0)
        else:
            raise ValueError(f"Node {start_node_id} is not found in {tree}")
    else:
        if tree.root_node_id in tree.nodes:
            enqueue(tree.root_node_id, 0)
        for node_id, node in tree.nodes.items():
            if not node.parent_node_ids and node_id != tree.root_node_id:
                enqueue(node_id, 0)

    while queue:
        current_id, depth = queue.popleft()
        current_node = tree.nodes[current_id]

        if start_node_id and exclude_start_node and current_id == start_node_id:
            pass
        else:
            yield current_node if yield_objects else current_id

        if max_depth is not None and depth >= max_depth:
            continue

        for child_id in current_node.child_node_ids:
            enqueue(child_id, depth + 1)
