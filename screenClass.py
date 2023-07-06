"""
A class to be a container for many boxes
"""
import pygame.event
from typing import Any
from boxClass import Box


class Screen:
    __hidden = False

    def __init__(self, **boxes: 'Box') -> None:
        self.boxes = dict(boxes)

    def hide(self) -> None:
        self.__hidden = True

    def show(self) -> None:
        self.__hidden = False

    def update(self, event: pygame.event.Event) -> Any:
        if self.__hidden:
            return []
        outs = []
        for name_box in self.boxes.items():
            name, box = name_box
            ret = box.update(event)
            if ret is not None:
                outs.append(ret)
        return outs
