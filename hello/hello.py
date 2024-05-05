import json
from difflib import get_close_matches
import os

def load_Brain_base(file_path: str) -> dict:
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                data: dict = json.load(file)
            except json.JSONDecodeError:
                data = {"Questions": []}  # Initialize with default data if JSON decode fails
            return data
    else:
        # Initialize with default data if the file doesn't exist
        return {"Questions": []}

def save_Brain_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, question: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_from_question(question: str, Brain: dict) -> str | None:
    for q in Brain["Questions"]:
        if q["Question"] == question:
            return q["Answer"]

def chat_bot():
    Brain: dict = load_Brain_base('Brain.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break
        best_match: str | None = find_best_match(user_input, [q["Question"] for q in Brain["Questions"]])

        if best_match:
            answer: str = get_answer_from_question(best_match, Brain)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                Brain["Questions"].append({"Question": user_input, "Answer": new_answer})
                save_Brain_base('Brain.json', Brain)
                print('Bot: Thank you, creator')

if __name__ == '__main__':
    chat_bot()
