from langchain.output_parsers.prompts import NAIVE_FIX_PROMPT

MAKE_MOVE_PROMPT = """You are a chess player. Among the legal moves, you should play the best move for {color}. \
The move should be one of these values: [{legal_moves}]

Made moves:
{history} 

{format_instructions} 
"""

ILLEGAL_MOVE_PROMPT = """
{prev_prompt}
Do not play {illegal_move}
"""

NAIVE_FIX_PROMPT = NAIVE_FIX_PROMPT
