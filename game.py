import chess
from players import Player

class Game:
    def __init__(self, player_white:Player, player_black:Player):
        self.player_white = player_white
        self.player_black = player_black
        self.board = chess.Board()
        self.move_counter = 0
        self.game_history = ""

    def _update_move_history(self,move):
        if self.board.turn == chess.WHITE:
            self.game_history += f"{move}, "
        else:
            self.game_history += f"{move}\n"
    
    def _check_move_error_(self,get_counter,increment_counter,color,move,error_type):
        message = f"Tried an {error_type} move: {move}. Try again."
        print(message)
        increment_counter()
        assert get_counter() < 3, f"{color} makes {error_type} moves 3 times in a row. "
    
    def _handle_illegal_move(self,player,move):
        self._check_move_error_(player.get_illegal_move_count,
                                player.increment_illegal_move_counter,
                                player.get_color(),
                                move,
                                "illegal")
        
        self.make_move(player)

    def _handle_invalid_move(self,player,move):
        self._check_move_error_(player.get_invalid_move_count,
                                player.incremenet_invalid_move_counter,
                                player.get_color(),
                                move,
                                "invalid")
        new_move = player.get_move(self.get_legal_moves(),
                                    self.game_history)
        self.make_move(player,new_move)

    def get_legal_moves(self):
        legal_moves = ""
        for move in self.board.legal_moves:
            legal_moves += f"{move}, "
        
        return legal_moves
    
    def _push_move(self,player:Player,move:str):
        try:
            self.board.push_san(move)
            print(f"\n{self.board}\n")
            player.reset_illegal_move_counter()
            player.reset_invalid_move_counter()
            self._update_move_history(move)
            self.move_counter += 1 
        except chess.IllegalMoveError:
            self._handle_illegal_move(player,move)
        except chess.InvalidMoveError:
            self._handle_invalid_move(player,move)

    def _is_move_legal(self,move_str):
        move = chess.Move.from_uci(move_str)
        return self.board.is_legal(move)
        
    def make_move(self, player:Player):
        """Player makes move
        """
        if self.board.turn == player.color:
            # Make the move
            move = player.get_move(legal_moves=self.get_legal_moves(),
                                   history=self.game_history,
                                   check_move=self._is_move_legal)
            self._push_move(player,move)
            
    def start_game(self):
        while not self.board.is_game_over():
            print("White's turn")
            print(f"Legal moves: {self.get_legal_moves()}")
            self.make_move(player=self.player_white)
            if self.board.is_game_over():
                break
            print("Black's turn")
            print(f"Legal moves: {self.get_legal_moves()}")
            self.make_move(player=self.player_black)

        print("Game finished.")
        self.board.result
        print()
