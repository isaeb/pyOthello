from othello.game import Game
from othello.move import Move
from options import options

class Runner:
    def __init__(self):
        self.game = Game
        self.initialized = False

        # Settings
        self.auto_start_game = False
        self.auto_display_board = True
        self.auto_display_fen = False
        self.auto_display_pgn = False

        if self.auto_start_game:
            self.new_game()
    
    def exit(self):
        quit()

    def display_settings(self, **kwargs):
        print('Settings:')
        print(f'\tauto-start-game:\t{self.auto_start_game}')
        print(f'\tauto-display-board:\t{self.auto_display_board}')
        print(f'\tauto-display-fen:\t{self.auto_display_fen}')
        print(f'\tauto-display-pgn:\t{self.auto_display_pgn}')

    def enable(self, **kwargs):
        if kwargs.get('auto-start-game', False):
            self.auto_start_game = True
        if kwargs.get('auto-display-board', False):
            self.auto_display_board = True
        if kwargs.get('auto-display-fen', False):
            self.auto_display_fen = True
        if kwargs.get('auto-display-pgn', False):
            self.auto_display_pgn = True
    
    def disable(self, **kwargs):
        if kwargs.get('auto-start-game', False):
            self.auto_start_game = False
        if kwargs.get('auto-display-board', False):
            self.auto_display_board = False
        if kwargs.get('auto-display-fen', False):
            self.auto_display_fen = False
        if kwargs.get('auto-display-pgn', False):
            self.auto_display_pgn = False

    def new_game(self, **kwargs):
        if kwargs.get('w', False):
            color = 'w'
        else:
            color = 'b'
        pgn = kwargs.get('pgn')
        if pgn is not None:
            try:
                with open(pgn) as f:
                    self.game = Game(f.read(), color)
            except Exception as e:
                print(e)
        else:
            self.game = Game()

        fen = kwargs.get('fen', '')
        self.initialized = True

        print('New game started.')
        self.auto_display()

    def auto_display(self):
        if self.auto_display_board:
            self.game.print_board()
        if self.auto_display_fen:
            self.game.print_fen()
        if self.auto_display_pgn:
            self.game.print_pgn()

    def move(self, **kwargs):
        if 'color' in kwargs.keys():
            for key in kwargs.keys():
                if key == 'color':
                    break
                self.game.make_move(Move(key, kwargs.get('color')))
        else:
            for key in kwargs.keys():
                self.game.make_move(key)
        self.auto_display()

    def display(self, **kwargs):
        if not self.initialized:
            print('Game not initialized. Try using \'new-game\' first.')
            return
        if kwargs.get('board', False):
            self.game.print_board()
        if kwargs.get('fen', False):
            self.game.print_fen()
        if kwargs.get('pgn', False):
            self.game.print_pgn()


def print_help(command:str=None):
    if command is None:
        s = 'help:\n\tusage: Display information about how to use the program.\n'
        for key in options.keys():
            usage = options[key].get('usage')
            s += f'{key}:\n\tusage: {usage}\n'

            arguments = options[key].get('arguments')
            if len(arguments) == 0:
                continue
            for argument in arguments:
                label = argument.get('label')
                usage = argument.get('usage')
                s += f'\t {label}:\t{usage}\n'
    print(s)

print('Welcome to Othello!\nType \'help\' to learn how to use the program.')
runner = Runner()
while True:
    text = input('> ')
    command = text.split()
    key = command[0]
    args = command[1:]

    try:
        if key == 'help':
            print_help()
            continue
        else:
            func_name = options[key]['function']
            func = getattr(runner, options[key]['function'])
    except:
        print(f'{key} is not a valid command.')
        continue

    kwargs = {}
    for index in range(len(args)):
        arg_value = True
        if args[index].find('-') == 0: # key
            if args[index].find('--') == 0: # arg is string
                arg_value = args[index+1]
        
        arg_name = args[index].lstrip('-')
        kwargs[arg_name] = arg_value
    try:
        func(**kwargs)
    except Exception as e:
        print(e)
    