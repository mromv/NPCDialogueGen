"""
Базовая модель данных, поддерживающая преобразование в текстовый промпт
"""
from typing import List, Dict
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class AutoPromptModel(BaseModel):
    _TAB = "  "
    _BULLET = "- "

    def as_prompt(self, *, _lvl: int = 0) -> str:
        def pad(bul: str = self._BULLET): return self._TAB * _lvl + bul
            
        parts: List[str] = []
        model_fields: Dict[str, FieldInfo] = self.__class__.model_fields
        
        for field_name, field_info in model_fields.items():
            value = getattr(self, field_name)
            if not value:
                continue

            description = field_info.description or field_name.replace("_", " ").capitalize()

            if isinstance(value, BaseModel):
                parts.append(f"{pad()}{description}:")
                parts.append(value.as_prompt(_lvl=_lvl + 1))

            elif isinstance(value, list):
                parts.append(f"{pad()}{description}:")

                for i, item in enumerate(value, 1):
                    parts.append(
                        item.as_prompt(_lvl=_lvl + 1)
                        if isinstance(item, BaseModel)
                        else f"{self._TAB}{pad(str(i))}. {item}"  # в случае списка значений
                    )
            
            elif isinstance(value, dict):
                parts.append(f"{pad()}{description}:")
                for k, v in value.items():
                    parts.append(
                        v.as_prompt(_lvl=_lvl + 1)
                        if isinstance(v, BaseModel)
                        else f"{self._TAB}{pad()}{k}: {v}"
                    )
                    
            else:
                parts.append(f"{pad()}{description}: {value}")

        return "\n".join(parts)
