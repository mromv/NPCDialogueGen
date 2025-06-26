"""
Базовая модель данных, поддерживающая преобразования в текстовый промпт
"""
from typing import List, Dict, ClassVar
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class AutoPromptModel(BaseModel):
    _TAB: ClassVar[str] = "  "
    _BULLET: ClassVar[str] = "- "

    @classmethod
    def model_description(cls) -> str:
        """Описание всех полей модели"""
        lines = []
        for field_name, field_info in cls.model_fields.items():
            desc = field_info.description or "Описание отсутствует"
            lines.append(f"{cls._BULLET}{str(field_name)}: {desc}")
        return "\n".join(lines)

    def as_prompt(self, exclude_none: bool = True, *, _lvl: int = 0) -> str:
        """Перевод полей экземпляра класса в текстовое представление для промпта"""
        def pad(bul: str = self._BULLET): return self._TAB * _lvl + bul
            
        parts: List[str] = []
        model_fields: Dict[str, FieldInfo] = self.__class__.model_fields
        
        for field_name, field_info in model_fields.items():
            value = getattr(self, field_name)
            if exclude_none and not value:
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
