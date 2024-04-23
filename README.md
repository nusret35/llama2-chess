# Llama2 Chess

A Python chess application that utilizes Llama 2 models as LLM players. The goal of this application is to demonstrate the chess skills of Llama 2 models. This repository is a great example for RAG (Retrieval Augmented Generation) implementations and prompt engineering. 

To play the game, run `start_game.py` inside `llama-chess` directory:
```bash
python start_game.py
```

For your information, the chess skills of Llama 2 models are very limited. Their skills are equivalent to 120 ELO player. In the future, I plan to finetune a Llama model to see whether I can turn them into Bobby Fischer. Since I am too lazy, I did not integrate a chess GUI for this application, rather I used Python's chess library. Sometimes the game crashes, as the models do not respond with a proper format. Feel free to send pull requests.

## Requirements

The application uses Replicate's models. To run this application, a Replicate API key is required. Other package requirements are included in `requirements.txt`. Install them by the following command:
```bash
pip install -r requirements.txt
```



