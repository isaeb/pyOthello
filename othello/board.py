from othello.move import Move
from typing import Literal

class Board:
    def __init__(self):
        # Init variables
        self.moves = []
        self.board = init_board()
        self.fen = create_fen(self.board)
    
    def __str__(self):
        s = ''
        for row in range(8):
            for col in range(8):
                val = self.board[col][row]
                if val == '':
                    s += '⛶'
                else:
                    s += '○●'['bw'.find(val)]
                s += ' '
            s += '\n'
        return s
    
    def has_legal_moves(self, color:Literal['b', 'w']):
        for col in 'abcdefgh':
            for row in '1234567':
                if is_legal(self.board, col+row, color):
                    return True
        return False

    def make_move(self, coordinate:str, color:Literal['b', 'w'], update_fen:bool=True, update_pgn=True, update_move_list:bool=True) -> bool:
        if not is_legal(self.board, coordinate, color):
            return False

        c = 'abcdefgh'.find(coordinate[0])
        r = int(coordinate[1])-1
        other_color = 'wb'['bw'.find(color)]
        for dx in [1, 0, -1]:
            for dy in [1, 0, -1]:
                if dx == 0 and dy == 0:
                    continue
                coordinates = []
                cursor_col = c + dx
                cursor_row = r + dy
                if not legal_coordinate(cursor_col, cursor_row):
                    continue
                if self.board[cursor_col][cursor_row] == '':
                    continue
                while self.board[cursor_col][cursor_row] == other_color:
                    coordinates.append((cursor_col, cursor_row))
                    cursor_col += dx
                    cursor_row += dy
                    if not legal_coordinate(cursor_col, cursor_row):
                        coordinates = []
                        break
                    if self.board[cursor_col][cursor_row] == color:
                        for coord in coordinates:
                            self.board[coord[0]][coord[1]] = color
                        self.board[c][r] = color
                        break
        if update_fen:
            self.fen = create_fen(self.board)
        if update_move_list:
            self.moves.append(Move(coordinate, color))
        if update_pgn:
            self = create_pgn(self.moves)
        return True

def create_pgn(moves:list[Move]):
    s = ''
    move_num = 1
    last_move = 'w'
    for move_num, move in enumerate(moves, start=1):
        if move.color == 'b':
            s += f'{move_num}. {move.notation}'
            if last_move == 'b':
                s += '...\n'
        else:
            if last_move == 'w':
                s += f'{move_num}. ...'
            s += f' {move.notation}\n'

def is_legal(board:list[list[str]], coordinate:str, color:Literal['b', 'w']) -> bool:
    c = 'abcdefgh'.find(coordinate[0])
    r = int(coordinate[1])-1
    other_color = 'wb'['bw'.find(color)]

    if not legal_coordinate(c, r):
        return False
    
    if board[c][r] != '':
        return False
        
    for dx in [1, 0, -1]:
        for dy in [1, 0, -1]:
            if dx == 0 and dy == 0:
                continue
            cursor_col = c + dx
            cursor_row = r + dy
            if not legal_coordinate(cursor_col, cursor_row):
                continue
            while board[cursor_col][cursor_row] == other_color:
                cursor_col += dx
                cursor_row += dy
                if not legal_coordinate(cursor_col, cursor_row):
                    break
                if board[cursor_col][cursor_row] == color:
                    return True

def legal_coordinate(column:int, row:int):
    if column < 0 or column > 7:
        return False
    if row < 0 or row > 7:
        return False
    return True

def create_fen(board:list[list[str]]):
    fen = ''
    whitespace = 0
    for row in range(8):
        for col in range(8):
            val = board[col][row]
            if val == '':
                whitespace += 1
            else:
                if whitespace > 0:
                    fen += str(whitespace)
                    whitespace = 0
                char = 'dD'['bw'.find(val)]
                fen += char
        if whitespace > 0:
            fen += str(whitespace)
            whitespace = 0
        if row < 7:
            fen += '/'
    return fen

def init_board() -> list[list[str]]:
    board = [['' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'w'
    board[4][3] = 'b'
    board[3][4] = 'b'
    board[4][4] = 'w'
    return board
