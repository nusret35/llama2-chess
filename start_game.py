import chess
from game import Game, HumanPlayer, LLMPlayer
from dotenv import load_dotenv

if __name__ == "__main__":
    REPLICATE_API_TOKEN = input("Enter your Replicate API key: ")
    