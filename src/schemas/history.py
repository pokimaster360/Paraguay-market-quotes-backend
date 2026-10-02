from pydantic import BaseModel

class HistoryPoint(BaseModel):
    created_at: str
    buy: str
    sell: str
    house: str