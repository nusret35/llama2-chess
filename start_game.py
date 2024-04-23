import chess
from game import Game
from players import Player,Model,LLMPlayer,HumanPlayer
import os

if __name__ == "__main__":

    REPLICATE_API_TOKEN = input("\nEnter your Replicate API key: ")

    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

    llm_dict = {
        1:Model.LLAMA2_7B,
        2:Model.LLAMA2_13B,
        3:Model.LLAMA2_70B
    }
    
    player_white, player_black = Player(color=chess.WHITE), Player(color=chess.BLACK)
    game_name = ""
    mode = int(input(f"\nChoose game mode:\n\n(1) Human vs. LLM\n(2) LLM vs. LLM\nPress other keys to quit\n\nEnter: "))

    if mode == 1:
        white_player_option = int(input(f"\nWho plays white:\n\n(1) Human\n(2) LLM\n Press other keys to quit\n\nEnter: "))
        if white_player_option == 1:
            player_white = HumanPlayer(color=chess.WHITE)
            model_selection = int(input("\nWhich LLM should play black:\n\n (1) LLAMA2 7B\n (2) LLAMA2 13B\n (3) LLAMA2 70B\n\nEnter: "))
            player_black = LLMPlayer(color=chess.BLACK, model=llm_dict[model_selection])
            game_name = f"Human vs. {llm_dict[model_selection].name}"
            
        elif white_player_option == 2:
            model_selection = int(input("\nWhich LLM should play white:\n\n (1) LLAMA2 7B\n (2) LLAMA2 13B\n (3) LLAMA2 70B\n\nEnter: "))
            player_white = LLMPlayer(color=chess.WHITE, model=llm_dict[model_selection])
            player_black = HumanPlayer(color=chess.BLACK)
            game_name = f"{llm_dict[model_selection].name} vs. Human"
        
    elif mode == 2:
        model_selection1 = int(input("\nWhich LLM should play white:\n\n (1) LLAMA2 7B\n (2) LLAMA2 13B\n (3) LLAMA2 70B\n\nEnter: "))
        model_selection2 = int(input("\nWhich LLM should play black:\n\n (1) LLAMA2 7B\n (2) LLAMA2 13B\n (3) LLAMA2 70B\n\nEnter: "))
        player_white = LLMPlayer(color=chess.WHITE, model=llm_dict[model_selection1])
        player_black = LLMPlayer(color=chess.BLACK, model=llm_dict[model_selection2])
        game_name = f"{llm_dict[model_selection1].name} vs. {llm_dict[model_selection2].name}"

    game = Game(player_white,player_black)

    print("Game starting...\n\n")
    print(game_name)
    game.start_game()