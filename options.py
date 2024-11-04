options = {
    'new-game': {
        'function': 'new_game',
        'usage': 'Start a new game.',
        'arguments': [
            {
                'label': '--pgn',
                'usage': 'Initialize a game with a pgn.'
            },
            {
                'label': '--fen',
                'usage': 'Initialize a game from an fen.'
            },
            {
                'label': '-w',
                'usage': 'Initialize a game with white to move.(Games are initialized with black to move by default).'
            }
        ]
    },
    'move': {
        'function': 'move',
        'usage': 'Make a move on the current board.',
        'arguments': [
            {
                'label': '--color',
                'usage': 'Make a move with a specific color.'
            }
        ]
    },
    'resign': {
        'function': 'resign',
        'usage': 'Resign the current game.',
        'arguments': [
            {
                'label': '--color',
                'usage': 'Force a specific color to resign.'
            }
        ]
    },
    'draw': {
        'function': 'draw',
        'usage': 'Draw the current game.',
        'arguments': []
    },
    'display': {
        'function': 'display',
        'usage': 'Display information about the current game.',
        'arguments': [
            {
                'label': '-board',
                'usage': 'Display the current position.'
            },
            {
                'label': '-fen',
                'usage': 'Display the fen of the current position.'
            },
            {
                'label': '-pgn',
                'usage': 'Display the pgn of the game.'
            }
        ]
    },
    'display-settings': {
        'function': 'display_settings',
        'usage': 'Display the current settings.',
        'arguments': []
    },
    'enable': {
        'function': 'enable',
        'usage': 'Enable a setting.',
        'arguments': []
    },
    'disable': {
        'function': 'disable',
        'usage': 'Disable a setting.',
        'arguments': []
    },
    'exit': {
        'function': 'exit',
        'usage': 'Exit the program.',
        'arguments': []
    }
}