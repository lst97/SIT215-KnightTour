
ACTIVATED_COLOR = (128, 128, 128)
class Tile:
    def __init__(self, pos:dict, color:tuple) -> None:
        self._pos = pos
        self._is_activated = False
        self._color = color
        self._step = 1
    
    def set_step(self, step:int):
        self._step = step
    
    def get_step(self):
        return self._step

    def get_step(self):
        return self._step

    def get_color(self):
        return self._color
        
    def set_color(self, color:tuple):
        self._color = color

    def set_status(self, status):
        self._is_activated = status
        if(self._is_activated is True):
            self._color = ACTIVATED_COLOR

    def get_status(self) -> bool:
        return self._is_activated
