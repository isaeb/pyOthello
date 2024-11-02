from othello.game import Game
from pathlib import Path


g = Game(Path('WTHOR-1977.pgn').read_text())
print(str(g))