import chess
from enum import Enum
import re
import json
from prompts import MAKE_MOVE_PROMPT, NAIVE_FIX_PROMPT, ILLEGAL_MOVE_PROMPT
from prompt_templates import PROMPT_TEMPLATE
from langchain_community.llms import Replicate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate


class Model(Enum):
    LLAMA_70B = "meta/llama-2-70b-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48"
    LLAMA_13B = "meta/llama-2-13b-chat:56acad22679f6b95d6e45c78309a2b50a670d5ed29a37dd73d182e89772c02f1"
    LLAMA_7B = "meta/llama-2-7b-chat:f1d50bb24186c52daae319ca8366e53debdaa9e0ae7ff976e918df752732ccc4"
    MISTRAL_7B_INSTRUCT_V02 = "mistralai/mistral-7b-instruct-v0.2:f5701ad84de5715051cb99d550539719f8a7fbcf65e0e62a3d1eb3f94720764e"
    

class FalseFormatError(Exception):
    pass

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
    def __init__(self,color:chess.Color,model:Model):
        self.color = color
        self.illegal_move_counter = 0
        self.invalid_move_counter = 0
        self.model = model
        
    def _generate_response_format(self):
        move_schema = ResponseSchema(name="move",
                                     description="The next move")
        output_parser = StructuredOutputParser.from_response_schemas([move_schema])
        format_instructions = output_parser.get_format_instructions()
        return format_instructions
        
    def _make_move_prompt(self,legal_moves,history):
        prompt_template = MAKE_MOVE_PROMPT
        format_instructions = self._generate_response_format()
        prompt = ChatPromptTemplate.from_template(template=prompt_template)
        messages = prompt.format_messages(color=self.get_color(),
                                          legal_moves=legal_moves,
                                          history=history,
                                          format_instructions=format_instructions)
        return messages[0].content
    
    def _fix_prompt(self, completion, error):
        regen_prompt_template = NAIVE_FIX_PROMPT
        format_instructions = self._generate_response_format()
        prompt = ChatPromptTemplate.from_template(template=regen_prompt_template)
        messages = prompt.format_messages(instructions=format_instructions,
                                          completion=completion,
                                          error=error)
        return messages[0].content

    def _illegal_move_prompt(self, prev_prompt, illegal_move):
        illegal_move_template = ILLEGAL_MOVE_PROMPT
        prompt = ChatPromptTemplate.from_template(template=illegal_move_template)
        messages = prompt.format_messages(prev_prompt=prev_prompt,
                                          illegal_move=illegal_move)
        return messages[0].content
        

    def _parse_message(self,message):
        # Extract content between ```
        match = re.findall(r'```json(.*?)```', message, re.DOTALL)[-1]
        if match:
            json_content = match.replace(",","")
            # Parse JSON content
            data = json.loads(json_content)
            return data
        else:
            return None
        
    def _call_model(self,prompt,check_move):
        llm = Replicate(
            model=self.model.value,
            model_kwargs={"temperature": 0.75, 
                          "top_p":0.8,
                          "system_prompt":prompt,
                          "prompt_template": PROMPT_TEMPLATE,
                        }
        )
        try:
            response = llm("")
            move = self._parse_message(response)["move"]
            if check_move(move):
                return move
            else:
                system_prompt = self._illegal_move_prompt(prompt,move)
            return self._call_model(system_prompt,check_move)
        except (json.JSONDecodeError, ValueError) as e:
            system_prompt = self._fix_prompt(completion=response,
                                                    error=str(e))
            return self._call_model(system_prompt)
      
            
            
    def get_move(self,legal_moves,history,check_move):
        system_prompt = self._make_move_prompt(legal_moves,history) 
        move = self._call_model(system_prompt,check_move)
        message = f"{self.get_color().capitalize()} plays: {move}"
        print(message)
        return move