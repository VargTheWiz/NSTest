from pydantic import BaseModel
from datetime import datetime, date

#джина, вес, дата добавления на склад, дата удаления со склада
class RollBase(BaseModel):
    length: int
    weight: float
    
class Roll(RollBase):
    id: int
    dateadd: datetime 
    dateremove: datetime | None = None #сразу не добавляется как правило
    
    class Config:
        from_attributes = True # миодель будет читаться даже если передается не словарь

class RollCreate(RollBase):
    pass

class RollRemove(BaseModel):#BaseModel потому что поля опциональны кроме даты выноса
    dateremove: datetime
