import chess
from schemas import Game, Player
from enum import Enum


if __name__ == "__main__":

    player_white, player_black  = Player(chess.WHITE), Player(chess.BLACK)
    game = Game(player_white,
                player_black)
    
    game.start_game()
    