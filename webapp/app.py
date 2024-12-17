from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize an 8x8 Othello board
def initialize_board():
    board = [['' for _ in range(8)] for _ in range(8)]
    # Set initial pieces in the center
    board[3][3] = 'white'
    board[4][4] = 'white'
    board[3][4] = 'black'
    board[4][3] = 'black'
    return board

# Store the game state
game_state = {
    "board": initialize_board(),
    "moves": []  # List of moves, e.g., "Player 1: D3"
}

@app.route('/')
def main_page():
    """
    Render the main page with the current game state.
    """
    return render_template(
        'main.html',
        board=game_state['board'],
        moves=game_state['moves']
    )

@app.route('/move', methods=['POST'])
def make_move():
    """
    Handle moves made by players.
    """
    data = request.json
    row, col = data.get('row'), data.get('col')
    color = data.get('color')  # "black" or "white"

    if not (0 <= row < 8 and 0 <= col < 8):
        return jsonify({"error": "Invalid move: out of bounds"}), 400

    if game_state['board'][row][col] != '':
        return jsonify({"error": "Invalid move: cell already occupied"}), 400

    # Update the board
    game_state['board'][row][col] = color

    # Add the move to the move list
    game_state['moves'].append(f"{color.capitalize()} to {chr(65 + col)}{row + 1}")

    # Return the updated game state
    return jsonify({
        "board": game_state['board'],
        "moves": game_state['moves']
    })

if __name__ == '__main__':
    app.run(debug=True)
