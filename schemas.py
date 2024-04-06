from enum import Enum
import chess


class Player:

    def __init__(self,color:chess.Color):
        self.color = color

    def _get_color(self):
        return "white" if self.color else "black" 
    
    def get_move(self,legal_moves,history=None):
        print(legal_moves)
        input_str = f"{self._get_color().capitalize()} plays: "
        move = input(input_str)
        return move

        
class Game:

    board = chess.Board()
    move_counter = 0
    game_history = ""
    turn = chess.WHITE


    def __init__(self, 
                 player_white:Player, 
                 player_black:Player):
        self.player_white = player_white
        self.player_black = player_black

    def _get_legal_moves(self):
        legal_moves = ""
        for move in self.board.legal_moves:
            legal_moves += f"{move}, "
        
        return legal_moves

    def _update_move_history(self,move):
        if self.turn == chess.WHITE:
            self.game_history += f"{move}, "
        else:
            self.game_history += f"{move}\n"
    
    def make_move(self, player:Player, move:str):
        """Player makes move
        """
        if self.board.turn == player.color:
            # Make the move
            try:
                self.board.push_san(move)
                print(f"\n{self.board}\n")
                self.move_counter += 1 
            except chess.IllegalMoveError:
                message = f"Tried illegal move: {move}. Try again."
                print(message)
                new_move = player.get_move(self.board.legal_moves,self.game_history)
                self.make_move(player,new_move)
    
    def start_game(self):
        while not self.board.is_game_over():

            move_white = self.player_white.get_move(self._get_legal_moves(),
                                                    self.game_history)
            self._update_move_history(move_white)
            self.make_move(player=self.player_white,move=move_white)

            if self.board.is_game_over():
                break

            move_black = self.player_black.get_move(self._get_legal_moves(),
                                                    self.game_history)
            self._update_move_history(move_black)
            self.make_move(player=self.player_black,move=move_black)
        
        print("Game finished.")

        
    



