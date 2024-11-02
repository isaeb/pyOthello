from othello.move import Move
from othello.board import Board


class Game:
    def __init__(self, pgn:str='', color='b'):
        # Handle PGN
        self.metadata = create_metadata(pgn)
        self.board = create_board(pgn)
        self.pgn = create_pgn(self.metadata, self.board.moves)

        # Init Variables
        self.color = color

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
    
    def make_move(self, move:Move) -> bool:
        if type(move) is str:
            color = self.color
            self.color = 'bw'['wb'.find(self.color)]
            if not self.board.has_legal_moves(self.color):
                self.color = 'bw'['wb'.find(self.color)]
            return self.board.make_move(move, color)
        return self.board.make_move(move.notation, move.color)

    def get_metadata(self, key:str=None) -> any:
        if key is None:
            return self.metadata
        else:
            return self.metadata.get(key)
        
    
def create_board(pgn:str, skip:list=['[',']']) -> Board:
    b = Board()
    columns = 'abcdefgh'
    rows = '12345678'
    color = 'b' # Black moves first
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
                    return b
                color = 'bw'['wb'.find(color)]
    return b

def create_metadata(pgn:str, left:str='[', right:str=']', bound:str='"') -> dict:
    metadata = {}
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
                text += f'...\n'
                move_num += 1
            text += f'{move_num}. {move.notation} '
        else:
            if last_color == 'w':
                text += f'{move_num}. ... '
            text += f'{move.notation}\n'
            move_num += 1
        last_color = move.color
    return text
