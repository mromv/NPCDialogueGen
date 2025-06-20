"""
Модели данных для персонажей
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class Character(BaseModel):
    """Модель NPC-персонажа для генерации диалогов"""
    name: str = Field(..., description="Имя персонажа")
    goals: List[str] = Field(..., description="Цели персонажа")
    personality: Optional[str] = Field(None, description="Описание личности персонажа")
    hist_period: Optional[str] = Field(None, description="Исторический период")
    geography: Optional[str] = Field(None, description="Местонахождение персонажа")
    background: Optional[str] = Field(None, description="Предыстория персонажа")
    speech_style: Optional[str] = Field(None, description="Стиль речи персонажа")
    relationships: Optional[Dict[str, str]] = Field(None, description="Отношения персонажа")

    scipt_text: Optional[str] = Field(None, description="Любой текст сценариста, передается в промпт явно.")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Старый мудрец",
                "goals": ["Поделиться опытом", "Сообщить информацию из письма"],
                "personality": "мудрый, загадочный, немного ворчливый",
                "hist_period": "третий век до нашей эры",
                "geography": "Месопотамия",
                "background": "хранитель древних знаний, умеет видеть будущее",
                "speech_style": "архаичный, использует метафоры",
                "relationships": {
                    "игрок": "друг"
                },
                "scipt_text": "умирает во время диалога, не успев сообщить, что было в письме"
            }
        }
