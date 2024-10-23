import chess
from Evaluator import Evaluator 

# determines which move should be made
class MoveMaker:
    # depth_function(int) -> int: given the number of pieces on the board, determines at what depth the minimax algorithm should search
    # make_move(chess.BitBoard) -> chess.Move: given a board, returns the best move to make, kickstarts search
    # search(int, chess.Board) -> int: recursive function that implements the minimax algorithm

    num_searched = 0

    def depth_function(num_pieces: int) -> int:
        return int((-0.06 * num_pieces) + 5.95)
    
    def make_move(board: chess.Board) -> chess.Move:
        num_pieces = len(board.piece_map())
        depth = MoveMaker.depth_function(num_pieces)
        color = board.turn

        alpha = float('-inf')
        beta  = float('-inf')
        
        best_move = None
        best_eval = float('-inf')

        for move in board.legal_moves:
            if not best_move:
                best_move = move
            
            board.push(move)
            eval = -1 * MoveMaker.search(depth - 1, board, alpha, beta)
            if eval > best_eval:
                best_eval = eval
                best_move = move
            board.pop()

            if color == chess.WHITE:
                alpha = max(alpha, eval)
                if -1 * beta <= alpha:
                    break
            else:
                beta = max(beta, eval)
                if -1 * alpha <= beta:
                    break
        
        print(f'depth searched: {depth}')
        print(f'alpha number searched: {MoveMaker.num_searched}')
        MoveMaker.num_searched = 0
        return best_move

    def search(depth: int, board: chess.Board, alpha: int, beta: int) -> int:
        # base cases
        if board.is_game_over():
            MoveMaker.num_searched += 1
            return float('-inf')
        if depth == 0:
            MoveMaker.num_searched += 1
            return Evaluator.evaluate(board)
        
        color = board.turn
        
        most_significant_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = -1 * MoveMaker.search(depth - 1, board, alpha, beta)
            most_significant_eval = max(most_significant_eval, eval)
            board.pop()

            # overly complicated alpha beta pruning because evaluate is color-dependent
            if color == chess.WHITE:
                alpha = max(alpha, eval)
                if -1 * beta <= alpha:
                    break
            else:
                beta = max(beta, eval)
                if -1 * alpha <= beta:
                    break
        return most_significant_eval



def main():
    board = chess.Board()
    board.push_san("e4")
    board.push_san("e5")

    board.push_san("Nf3")
    board.push_san("Na6")
    print(MoveMaker.make_move(board))

def test():
    board = chess.Board()
    board.push_san("e4")
    board.push_san("d5")
    board.push_san("a3")
    print(MoveMaker.make_move(board))