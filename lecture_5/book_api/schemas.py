from pydantic import BaseModel
from typing import Optional

# Базовая схема (общие поля)
class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None

# Для создания книги (без id)
class BookCreate(BookBase):
    pass

# Для обновления книги (все поля необязательны)
class BookUpdate(BaseModel):
    title: str
    author: str
    year: Optional[int] = None

# Для ответа (с id)
class BookOut(BookBase):
    id: int

    class Config:
        from_attributes = True
