from schemas import Player
from langchain_community.llms import Replicate


class LLMPlayer(Player):
    
    def _generate_prompt(self,legal_moves,game_history):

        color = self._get_color()
        system_prompt = f"""You are a chess player. Among the legal moves, you should play the best move for {color}.
                        The output should look like this: 
                        {color.capitalize()} plays: move
                        The move should be one of these values: {legal_moves}
                        Only output the selected item with no note or explanation.
                        
                        Made moves:
                        {game_history}
                        """
        return system_prompt


    def get_move(self,legal_moves,game_history):
        system_prompt = self._generate_prompt(legal_moves,game_history)
        llm = Replicate(
            model="meta/llama-2-7b-chat:f1d50bb24186c52daae319ca8366e53debdaa9e0ae7ff976e918df752732ccc4",
            model_kwargs={"temperature": 0.75, "max_length": 10, "top_p":1, "system_prompt":system_prompt}
        )
        response = llm("").strip()
        move = response.split(" ")[2]
        print(response)

        return move

    

    