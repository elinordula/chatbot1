import json
import random
from department_data import get_cse_faculty, get_ece_faculty, get_cce_faculty

# Load intents from intents.json
def load_intents():
    with open('intents.json') as file:
        intents = json.load(file)
    return intents

# Get response based on tag
def get_response(tag):
    if tag == "cse faculty_list":
        return get_cse_faculty()
    elif tag == "ece_faculty_list":
        return get_ece_faculty()
    elif tag == "cce_faculty_list":
        return get_cce_faculty()
    else:
        responses = [intent['responses'] for intent in load_intents()['intents'] if intent['tag'] == tag]
        if responses:
            return random.choice(responses[0])
        return "Sorry, I don't have information on that."

# Main chatbot function
def chatbot_response(user_input):
    intents = load_intents()['intents']
    for intent in intents:
        for pattern in intent['patterns']:
            if user_input.lower() in pattern.lower():
                return get_response(intent['tag'])
    return "I'm sorry, I didn't understand that. Can you try again?"

# Test chatbot response
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        response = chatbot_response(user_input)
        print(f"Bot: {response}")
