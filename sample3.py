import os
import ssl
import nltk
import json
import streamlit as st
import random
import re
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Setting up SSL context for nltk
ssl._create_default_https_context = ssl._create_unverified_context

# Downloading punkt tokenizer
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Load intents from a separate JSON file
def load_intents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        intents = json.load(file)
    return intents

# Specify the path to the intents file
intents_file_path = "D:\\Mridula\\stud chatbot\\stupid\\intents.json"  # Update this with the actual path
intents = load_intents(intents_file_path)

# Create the vectorizer and classifier
vectorizer = TfidfVectorizer()
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess the data
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

# Precompile regex patterns for all intents
compiled_intents = []
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Escape special regex characters in the pattern
        escaped_pattern = re.escape(pattern.lower())
        # Replace escaped wildcard characters if necessary (e.g., for variable parts)
        # For exact keyword matching, we can use word boundaries
        regex_pattern = r'\b' + escaped_pattern + r'\b'
        compiled_intents.append({
            'tag': intent['tag'],
            'pattern': re.compile(regex_pattern)
        })

# Define the chatbot function with regex for multiple intents
def chatbot(input_text):
    input_text_lower = input_text.lower().strip()  # Convert input to lowercase and strip whitespace

    matched_tags = set()

    # Iterate over all compiled regex patterns to find matches
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # Compile regex for the current pattern
            # Using word boundaries to match whole words
            regex = re.compile(r'\b' + re.escape(pattern.lower()) + r'\b')
            if regex.search(input_text_lower):
                matched_tags.add(intent['tag'])

    # If matched_tags is not empty, fetch responses for all matched intents
    if matched_tags:
        responses = []
        for tag in matched_tags:
            # Find the intent with the matching tag
            for intent in intents['intents']:
                if intent['tag'] == tag:
                    responses.append(random.choice(intent['responses']))
                    break
        # Join responses with five spaces
        combined_response = "     \n \n".join(responses)
        return combined_response

    # If no regex matches, fallback to the existing model-based approach
    # Vectorize the input and predict the intent
    input_vector = vectorizer.transform([input_text])
    predicted_tag = clf.predict(input_vector)[0]

    # Find the intent with the predicted tag
    for intent in intents['intents']:
        if intent['tag'] == predicted_tag:
            return random.choice(intent['responses'])

    # If no intent is matched, provide a default response
    return "I'm sorry, I didn't understand that. Can you please rephrase?"

# Streamlit UI
def main():
    st.title("AIML Department Chatbot")
    st.write("Welcome to the AIML department's chatbot. Please type a message and press Enter to start the conversation.")
    
    # Initialize session state for conversation history
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    user_input = st.text_input("You:")

    if user_input:
        response = chatbot(user_input)
        st.session_state.conversation.append(("You", user_input))
        st.session_state.conversation.append(("Chatbot", response))

    # Display the conversation
    for speaker, message in st.session_state.conversation:
        if speaker == "You":
            st.markdown(f"**{speaker}:** {message}")
        else:
            st.markdown(f"**{speaker}:** {message}")

        # If the chatbot says goodbye, stop the conversation
        if speaker == "Chatbot" and message.lower() in ['goodbye', 'bye']:
            st.write("Thank you for chatting with me. Have a great day!")
            break

if __name__ == '__main__':
    main()
