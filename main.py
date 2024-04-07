import chess
from schemas import Game, HumanPlayer, LLMPlayer
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    player_white, player_black = HumanPlayer(chess.WHITE), LLMPlayer(chess.BLACK)
    game = Game(player_white,
                player_black)
    
    game.start_game()
    