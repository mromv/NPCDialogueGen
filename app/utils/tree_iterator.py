"""
Вспомогательные функции для работы с деревом диалогов
"""
from collections import deque
from typing import Optional, List, Set, Union, Iterator
from app.schemas import DialogBaseNode, DialogBaseTree


def get_ancestors(
    tree: DialogBaseTree,
    node_id: str,
    return_objects: bool = False
) -> List[List[str]]:
    """Возвращает все пути от предков до текущего узла не включительно"""
    if node_id not in tree.nodes:
        raise ValueError(f"Node {node_id} is not found in {tree}")
    
    visited: Set[str] = set()
    ancestors = []
    queue = [node_id]
    
    while queue:
        current_id = queue.pop(0)
        current_node = tree.nodes.get(current_id)
        
        if not current_node:
            continue
            
        for parent_id in current_node.parent_node_ids:
            if parent_id not in visited:
                visited.add(parent_id)
                ancestors.append(parent_id)
                queue.append(parent_id)
    
    ancestors = ancestors[::-1]

    if return_objects:
        return [tree.nodes[id_] for id_ in ancestors]
                
    return ancestors


def bfs(
    tree: DialogBaseTree,
    start_node_id: Optional[str] = None,
    yield_objects: bool = False
) -> Iterator[Union[DialogBaseNode, str]]:
    """Обход дерева в ширину"""
    visited = set()
    queue = deque()

    if start_node_id is not None:
        if start_node_id in tree.nodes:
            queue.append(start_node_id)
            visited.add(start_node_id)
        else:
            ValueError(f"Node {start_node_id} is not found in {tree}")

    else:
        if tree.root_node_id in tree.nodes:
            queue.append(tree.root_node_id)
            visited.add(tree.root_node_id)
        for node_id, node in tree.nodes.items():
            if not node.parent_node_ids and node_id != tree.root_node_id:
                queue.append(node_id)
                visited.add(node_id)

    while queue:
        current_id = queue.popleft()
        current_node = tree.nodes[current_id]
        yield current_node if yield_objects else current_id

        for child_id in current_node.child_node_ids:
            if child_id in tree.nodes and child_id not in visited:
                visited.add(child_id)
                queue.append(child_id)
