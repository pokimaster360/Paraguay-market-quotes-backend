from enum import IntEnum


DOWN_Dict = {
    'bajando',
    'down',
    'baja'
}
UP_Dict = {
    'subiendo',
    'up',
    'sube',
    'suba'
}
EQUAL_Dict = {
    'igual',
    'equal'
}



class Trend(IntEnum):
    DOWN = -1
    EQUAL = 0
    UP = 1

def normalize_trend(value: str | None) -> Trend | None:
    if value is None:
        return None

    

    
    try:
        value = value.lower().strip()
        
        if value in DOWN_Dict:
            return Trend.DOWN
    
        if value in UP_Dict:
            return Trend.UP
    
        if value in EQUAL_Dict:
            return Trend.EQUAL
    except KeyError:
        raise ValueError(f'Unkown Trend: {value!r}')