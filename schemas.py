from enum import Enum
import chess
from langchain_community.llms import Replicate


class Player:
    def __init__(self,color:chess.Color):
        self.color = color
        self.illegal_move_counter = 0
        self.invalid_move_counter = 0

    def get_color(self): return "white" if self.color else "black" 
    
    def get_illegal_move_count(self): return self.illegal_move_counter

    def get_invalid_move_count(self): return self.invalid_move_counter
    
    def get_move(self, legal_moves, history=None):
        raise NotImplementedError("Subclasses must implement this method.")
    
    def increment_illegal_move_counter(self):
        self.illegal_move_counter += 1
    
    def reset_illegal_move_counter(self):
        self.illegal_move_counter = 0

    def incremenet_invalid_move_counter(self):
        self.invalid_move_counter += 1
    
    def reset_invalid_move_counter(self):
        self.invalid_move_counter = 0


class HumanPlayer(Player):
    def get_move(self,legal_moves,history=None):
        print(legal_moves)
        input_str = f"{self.get_color().capitalize()} plays: "
        move = input(input_str)
        return move


class LLMPlayer(Player):
    def _generate_prompt(self,legal_moves,history):
        color = self.get_color()
        system_prompt = (f"You are a chess player. Among the legal moves, you should play the best move for {color}. "
        f"The output should look like this:\n"
        f"\"{color.capitalize()} plays: move\"\n"
        f"The move should be one of these values: {legal_moves}\n"
        f"Only output the selected item with no note or explanation.\n"
        f"Made moves:\n"
        f"{history}")
                        
        return system_prompt

    def get_move(self,legal_moves,history):
        system_prompt = self._generate_prompt(legal_moves,history)
        llm = Replicate(
            model="meta/llama-2-7b-chat:f1d50bb24186c52daae319ca8366e53debdaa9e0ae7ff976e918df752732ccc4",
            model_kwargs={"temperature": 0.75, 
                          "max_length": 20, 
                          "top_p":0.8, 
                          "system_prompt":system_prompt
                          }
        )
        response = llm("").strip()
        move = response.split(" ")[2]
        print(response)

        return move

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
        assert get_counter() < 3, f"{color} makes {error_type} moves 3 times in a row."
    
    def _handle_illegal_move(self,player,move):
        self._check_move_error_(player.get_illegal_move_count,
                                player.increment_illegal_move_counter,
                                player.get_color(),
                                move,
                                "illegal")
        new_move = player.get_move(self.get_legal_moves(),
                                    self.game_history)
        self.make_move(player,new_move)

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
    
    def make_move(self, player:Player):
        """Player makes move
        """
        if self.board.turn == player.color:
            # Make the move
            move = player.get_move(legal_moves=self.get_legal_moves(),
                                   history=self.game_history)
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
            
    def start_game(self):
        while not self.board.is_game_over():
            self.make_move(player=self.player_white)
            if self.board.is_game_over():
                break
            self.make_move(player=self.player_black)
        
        print("Game finished.")

        
    



