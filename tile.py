ACTIVATED_COLOR = (128, 128, 128)  # gray


class Tile:
    def __init__(self, pos: dict, color: tuple) -> None:
        self._pos = pos
        self._visited = False
        self._color = color
        self._step = 1

    def set_step(self, step: int):
        self._step = step

    def get_step(self) -> int:
        """step count

        Returns:
            int: step count
        """
        return self._step

    def get_color(self) -> tuple:
        return self._color

    def set_color(self, color: tuple):
        self._color = color

    def set_state(self, status: bool) -> None:
        self._visited = status
        if self._visited is True:
            self._color = ACTIVATED_COLOR

    def is_visited(self) -> bool:
        return self._visited
