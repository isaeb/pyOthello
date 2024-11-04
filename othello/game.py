from othello.move import Move
from othello.board import Board
from typing import Literal


class Game:
    def __init__(self, pgn:str=None, fen:str=None, color='b'):
        # Handle PGN
        self.metadata = create_metadata(pgn)
        self.board = create_board(pgn=pgn, fen=fen)
        self.pgn = create_pgn(self.metadata, self.board.moves)

        # Init Variables
        self.color = color
        self.game_over = False
        self.black_count = 2
        self.white_count = 2
        self.result = None

    def print_board(self):
        print(str(self.board))

    def print_fen(self):
        print(self.board.fen)
    
    def print_pgn(self):
        if len(self.board.moves) > 0:
            print(create_pgn({}, self.board.moves))
    
    def __str__(self):
        return self.pgn

    def get_moves(self) -> list[Move]:
        return self.board.moves
    
    def get_count(self, color:Literal['b', 'w']):
        if color == 'b':
            return self.black_count
        if color == 'w':
            return self.white_count
    
    def set_result(self, result:str, update_pgn=True):
        self.result = result
    
    def make_move(self, move:Move) -> bool:
        if self.result is not None:
            return False
        if type(move) is str:
            color = self.color
            self.color = 'bw'['wb'.find(self.color)]
            if not self.board.has_legal_moves(self.color):
                self.color = 'bw'['wb'.find(self.color)]
            success = self.board.make_move(move, color)
        else:
            success = self.board.make_move(move.notation, move.color)
        
        if not success:
            return False

        # Update counts
        self.game_over = self.board.game_over()
        self.black_count = self.board.get_score('b')
        self.white_count = self.board.get_score('w')

        return True

    def get_metadata(self, key:str=None) -> any:
        if key is None:
            return self.metadata
        else:
            return self.metadata.get(key)
        
    
def create_board(pgn:str=None, fen:str=None, skip:list=['[',']']) -> Board:
    b = Board()
    columns = 'abcdefgh'
    rows = '12345678'
    color = 'b' # Black moves first
    if pgn is not None:
        for line in pgn.splitlines():
            if any([c in line for c in skip]):
                continue

            for text in line.split(' '):
                if len(text) != 2:
                    continue

                text = text.lower()
                if text[0] in columns and text[1] in rows: # text is valid move notation
                    if not b.has_legal_moves(color):
                        color = 'bw'['wb'.find(color)]
                    if not b.make_move(text, color, update_fen=False):
                        # Illegal move attempted
                        break
                    color = 'bw'['wb'.find(color)]
    if fen is not None:
        b.set_position(fen)
    else:
        b.update_fen() 
    return b

def create_metadata(pgn:str, left:str='[', right:str=']', bound:str='"') -> dict:
    metadata = {}
    if pgn is None:
        return metadata
    for line in pgn.splitlines():
        if not left in line or not right in line:
            continue
        if line.find(left) >= line.find(right):
            continue

        text = line[line.index(left)+len(left):line.index(right)]
        if text.count(bound) == 0:
            metadata[text] = None
        elif text.count(bound) == 2:
            value = text[text.find(bound)+len(bound):text.rfind(bound)]
            key = text.split(bound)[0].lstrip().rstrip()
            metadata[key] = value
    return metadata

def create_pgn(metadata:dict={}, moves:list[Move]=[], left:str='[', right:str=']', bound:str='"') -> str:
    text = ''
    for key, value in metadata.items():
        text += f'{left}{key}'
        if value is None:
            text += f'{right}\n'
        else:
            text += f' {bound}{value}{bound}{right}\n'

    move_num = 1
    last_color = 'w'
    for move in moves:
        if move.color == 'b':
            if last_color == 'b':
                text += f'..\n'
                move_num += 1
            text += f'{move_num}. {move.notation} '
        else:
            if last_color == 'w':
                text += f'{move_num}. .. '
            text += f'{move.notation}\n'
            move_num += 1
        last_color = move.color
    return text
