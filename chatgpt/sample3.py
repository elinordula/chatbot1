import os
import ssl
import nltk
import json
import streamlit as st
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Setting up SSL context for nltk
ssl._create_default_https_context = ssl._create_unverified_context

# Download NLTK tokenizer if not present
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Load intents from a separate JSON file
def load_intents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        intents = json.load(file)
    return intents

# Specify the path to the intents file
intents_file_path = "D:\\Mridula\\stud chatbot\\stupid\\intents.json"  # Update with the actual path
intents = load_intents(intents_file_path)

# Create the vectorizer and classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data for training
tags = []
patterns = []
for intent in intents['intents']:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)

# Training the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

# Compile regex patterns for all intents
compiled_intents = []
for intent in intents['intents']:
    for pattern in intent['patterns']:
        escaped_pattern = re.escape(pattern.lower())
        regex_pattern = r'\b' + escaped_pattern + r'\b'
        compiled_intents.append({
            'tag': intent['tag'],
            'pattern': re.compile(regex_pattern)
        })

# Define the chatbot function
def chatbot(input_text):
    input_text_lower = input_text.lower().strip()

    matched_tags = set()

    # Check for regex matches with compiled patterns
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            regex = re.compile(r'\b' + re.escape(pattern.lower()) + r'\b')
            if regex.search(input_text_lower):
                matched_tags.add(intent['tag'])

    # If any regex matches are found, return responses
    if matched_tags:
        responses = []
        for tag in matched_tags:
            for intent in intents['intents']:
                if intent['tag'] == tag:
                    responses.append(random.choice(intent['responses']))
                    break
        combined_response = "     ".join(responses)
        return combined_response

    # If no regex matches, use the model-based approach
    input_vector = vectorizer.transform([input_text])
    predicted_tag = clf.predict(input_vector)[0]

    # Find the matching intent and return a response
    for intent in intents['intents']:
        if intent['tag'] == predicted_tag:
            return random.choice(intent['responses'])

    return "I'm sorry, I didn't understand that. Can you please rephrase?"

# Streamlit UI for the chatbot
def main():
    st.title("AIML Department Chatbot")
    st.write("Welcome to the AIML department's chatbot. Please type a message and press Enter to start the conversation.")
    
    # Initialize conversation history in session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # User input field
    user_input = st.text_input("You:")

    # If user provides input, generate a response
    if user_input:
        response = chatbot(user_input)
        st.session_state.conversation.append(("You", user_input))
        st.session_state.conversation.append(("Chatbot", response))

    # Display conversation history
    for speaker, message in st.session_state.conversation:
        if speaker == "You":
            st.markdown(f"**{speaker}:** {message}")
        else:
            st.markdown(f"**{speaker}:** {message}")

        # End the conversation if the chatbot says goodbye
        if speaker == "Chatbot" and message.lower() in ['goodbye', 'bye']:
            st.write("Thank you for chatting with me. Have a great day!")
            break

if __name__ == '__main__':
    main()
