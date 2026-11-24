import chess
import tkinter as tk

VALUES = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 320,
          chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}
CENTER = [chess.D4, chess.E4,  chess.D5, chess.E5]

def evaluate(board):
    if board.is_checkmate():
        return-99999
    if board.is_game_over():
        return  0 # stalemate or a draw
    score = 0
    for square, piece in board.piece_map().items():
        value = VALUES[piece.piece_type] + (20 if square in CENTER else 0)
        score += value if piece.color == board.turn else -value
    return score

def search(board, depth, alpha = -100000, beta = 100000):
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    for move in board.legal_moves:
        board.push(move)
        score = -search(board, depth - 1, -beta, -alpha)
        board.pop()
        if score >= beta:
            return beta # opponent whould never allow this stop looking
        alpha=max(alpha, score)

    return alpha

def best_move(board, depth=3):
    def score(move):
        board.push(move)
        result = -search(board, depth - 1)
        board.pop()
        return result
    return max(board.legal_moves, key=score)

# board window

SIZE = 90
LIGHT, DARK, PICKED = "#EEEED2", "#769656", "#F6F669"

board = chess.Board()
selected = None

root = tk.Tk()
root.title("Chess Bot")
canavs = tk.Canvas(root, width =8 * SIZE, height =8 * SIZE, highlightthickness=0)
canavs.pack()

def draw():
    canavs.delete("all")
    for square in chess.SQUARES:
        x = chess.square_file(square) *SIZE
        y = (7 - chess.square_rank(square)) * SIZE
        light = (chess.square_file(square) + chess.square_rank(square)) % 2 == 1
        color = PICKED if square == selected else LIGHT if light else DARK
        canavs.create_rectangle(x, y, x + SIZE, y + SIZE, fill=color, outline="")
        piece = board.piece_at(square)
        if piece:
            canavs.create_text(x + SIZE / 2, y +SIZE /2, text=piece.unicode_symbol(),
                               font=("Arial", int(SIZE * 0.7)), fill="Black")

    if board.is_game_over():
        canavs.create_text(4 * SIZE, 4 * SIZE, text="Game over: " + board.result(),
                           font=("Arial", 40, "bold"), fill="Red")

def click(event):
    global selected
    if board.is_game_over() or board.turn != chess.WHITE:
        return
    square =chess.square(event.x // SIZE, 7- event.y // SIZE)
    piece = board.piece_at(square)

    if piece and piece.color == chess.WHITE:
        selected = square
    elif selected is not None:
        move = chess.Move(selected, square)
        if chess.Move(selected, square, chess.QUEEN) in board.legal_moves:
            move = chess.Move(selected, square, chess.QUEEN)
        selected = None
        if move in board.legal_moves:
             board.push(move)
             root.after(100, bot_turn)

    draw()

def bot_turn():
    if not board.is_game_over():
        board.push(best_move(board))
    draw()

canavs.bind("<Button-1>", click)
draw()
root.mainloop()

