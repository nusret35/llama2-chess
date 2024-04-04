from enum import Enum
import chess


class Player:

    def __init__(self,color:chess.Color):
        self.color = color

    def get_move(self):
        move = input("What is your move?\n")
        return move

        
class Game:

    board = chess.Board()
    move_counter = 0

    def __init__(self, 
                 player_white:Player, 
                 player_black:Player, 
                 llm_color:chess.Color=chess.BLACK, 
                 turn:chess.Color=chess.WHITE):
        self.player_white = player_white
        self.player_black = player_black
        self.turn = turn
    
    def make_move(self, player:Player, move:str):
        """Player makes move
        """
        if self.turn == player.color:
            # Make the move
            self.board.push_san(move)
            self.turn = not self.turn
            self.move_counter += 1
            print()
            print(self.board)
            print()
    
    def start_game(self):
        while not self.board.is_game_over():

            move_white = self.player_white.get_move()
            self.make_move(player=self.player_white,move=move_white)

            if self.board.is_game_over():
                break
        
            move_black = self.player_black.get_move()
            self.make_move(player=self.player_black,move=move_black)
        
        print("Game finished.")

        
    



