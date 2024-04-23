import chess
from game import Game
from players import HumanPlayer, LLMPlayer, Model
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    player_white, player_black = LLMPlayer(chess.WHITE,model=Model.LLAMA2_70B), LLMPlayer(color=chess.BLACK,model=Model.LLAMA2_70B)
    game = Game(player_white,
                player_black)
    
    game.start_game()
    