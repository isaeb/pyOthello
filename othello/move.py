from typing import Literal


class Move:
    def __init__(self, notation:str, color:Literal['b', 'w']):
        self.notation = notation
        self.color = color

        columns = 'abcdefgh'
        rows = '12345678'
        self.coordinates = (columns.find(notation[0]), rows.find(notation[1]))
