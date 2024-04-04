from schemas import Player
from langchain_community.llms import Replicate


class LLMPlayer(Player):

    llm = Replicate(
        model="meta/llama-2-7b-chat:f1d50bb24186c52daae319ca8366e53debdaa9e0ae7ff976e918df752732ccc4",
        model_kwargs={"temperature": 0.75, "max_length": 100, "top_p":1}
    )
    
    def _generate_prompt(self,moves,move):

        color = "white" if self.color else "black" 
        system_prompt = f"""You are a chess player. You are playing the {self.color}.
                        moves: d4 Nc6 e4 e5 f4 f6 dxe5 fxe5 fxe5 Nxe5 Qd4 Nc6 Qe5+ Nxe5 c4
                        Output the next move for {self.color}.
                        """
        prompt = f"""What is the next move for {self.color}? Just output the move.
                """

    def get_move(self):
        print()


    