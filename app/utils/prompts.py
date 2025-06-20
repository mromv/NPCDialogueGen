"""
Шаблоны динамических промптов для LLM
"""
import json
from typing import List, Dict, Any, Optional
from app.schemas import (
    Character, Goal, Constraints, DialogNode,
    TreeGenerationRequest, ContentGenerationRequest
)


# TODO: сложить шаблоны промптов в отдельных файлах в utils/prompts

class PromptTemplates:
    """Коллекция шаблонов промптов для различных задач"""

    ALLOWED_BRANCH_TYPES = {
        "main": "основная линия к цели",
        "exploration": "контент-ветка для изучения мира/NPC",
        "dead_end": "тупик, обрывающий диалог",
        "loop": "возвращает к одному из предыдущих узлов",
        "side_quest": "редкая побочная ветка"
    }
        
    @staticmethod
    def tree_generation_prompt(
        request: TreeGenerationRequest
    ) -> str:
        character: Character = request.character
        goal: Goal = request.goal
        
        goal_conditions = ", ".join([c.description for c in goal.conditions]) if goal.conditions else "отсутствуют"
        success_criteria = ", ".join(goal.success_criteria) if goal.success_criteria else "не указаны"
        constraints_text = request.constraints.as_prompt()
        branch_type_definitions = "\n".join(
            f'    • **{key}** — {desc}' for key, desc in PromptTemplates.ALLOWED_BRANCH_TYPES.items()
        )
        relationships = json.dumps(character.relationships or {}, ensure_ascii=False, indent=2)

        return f"""
Ты — генератор **структуры диалогового дерева** для NPC в сюжетной игре. Не пиши реплики, только метаинформацию (описания, цели, типы веток и связи).

---

## NPC (персонаж):
- Имя: {character.name}
- Цели: {", ".join(character.goals)}
- Личность: {character.personality or "не указана"}
- Эпоха: {character.hist_period or "не указана"}
- География: {character.geography or "не указана"}
- Предыстория: {character.background or "не указана"}
- Стиль речи: {character.speech_style or "не указан"}
- Отношения: {relationships}
- Сценарный текст: {character.scipt_text or "отсутствует"}

---

## Цель диалога:
- Тип: {goal.type}
- Объект: {goal.target}
- Условия достижения: {goal_conditions}
- Критерии успеха: {success_criteria}
- Сложность: {goal.difficulty or 1}/5

{constraints_text}

## Структура узлов:
Каждый узел дерева описывается следующим образом:

```json
{{
  "node_id": "node_1",
  "difficulty": 0,
  "narrative_summary": "Краткое описание происходящего на этом этапе",
  "player_goal_hint": "Что игрок, скорее всего, попытается сделать",
  "branch_type": "main",
  "parent_node_ids": [],
  "child_node_ids": ["node_2", "node_3"],
  "estimated_choices": 3
}}
```

Где:
- node_id:	Уникальный ID узла ("node_3")
- difficulty:	Предполагаемая сложность прохождения узла (число от 1 до 5)
- narrative_summary:	Краткое описание, что происходит в сцене (без конкретных реплик)
- player_goal_hint: Что игрок скорее всего попытается сделать (например: "задать вопрос", "получить предмет")
- branch_type:	Тип ветки (main, exploration, dead_end, loop, side_quest)
- parent_node_ids:	ID всех родителей этого узла (обычно 1)
- child_node_ids:	ID всех детей, на которые ведут choices
- estimated_choices:	Количество вариантов ответа игрока в этом узле (от 2 до 4)

---

## Правила:

- Вариантов выбора в узле: от **2 до 4**.
- Используй **ветки следующих типов** (Все значения 'branch_type' должны быть строго из этого списка):
  {branch_type_definitions}

- Рекомендованные пропорции:
  • dead_end ≈ 10–15% узлов
  • exploration ≈ 20–25% узлов
  • side_quest ≤ 5% (опционально)

---

## Финальный JSON должен иметь такую структуру:
```json
{{
  "root_node_id": "node_1",
  "nodes": {{
    "node_1": {{
      "difficulty": ...,
      "narrative_summary": "...",
      "player_goal_hint": "...",
      "branch_type": "main",
      "parent_node_ids": [...],
      "child_node_ids": [...],
      "estimated_choices": ...
    }},
    ...
  }},
  "estimated_paths_to_goal": [
    ["node_1", "node_3", "node_7"],
    ...
  ],
  "estimated_total_turns": 10
}}
```

---

Верни **только валидный JSON**. Без пояснений, комментариев, текста вне структуры.
"""

    @staticmethod
    def node_content_prompt(
        current_node: DialogNode,
        previous_nodes: List[DialogNode],
        character: Character
    ) -> str:
        
        context_lines = []
        for prev in previous_nodes:
            context_lines.append(f"- {prev.narrative_summary or '[предыдущий шаг]'}")

        return f"""
Ты пишешь диалоговую сцену между игроком и персонажем по имени {character.name}.
## Контекст (история диалога):
{chr(10).join(context_lines) if context_lines else "Это начало диалога."}

---

## Текущий момент:
- Краткое описание: {current_node.narrative_summary or "Не указано"}
- Намерение игрока: {current_node.player_goal_hint or "Не указано"}
- Тип ветки: {current_node.metadata.branch_type.value or "Не указано"}

---

## Задание:
Напиши:
1. Реплику NPC от имени "{character.name}"
2. От 2 до 4 вариантов ответа игрока
3. Укажи, к каким ID нод ведут эти выборы. Используй только те, что есть в child_node_ids: {current_node.child_node_ids})

---

Формат ответа:
```json
{{
  "npc_text": "...",
  "choices": [
    {{
      "text": "...",
      "next_node_id": "..."
    }},
    ...
  ]
}}
```

---
Пиши *только валидный JSON*. Без пояснений, комментариев, текста вне структуры.

"""
