import os
import ssl
import nltk
import json
import streamlit as st
import random
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
intents_file_path = "D:\Mridula\stud chatbot\stupid\intents.json"  # Update this with the actual path
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

# Define the chatbot function
def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response

# Streamlit UI
def main():
    st.title("Chatbot")
    st.write("Welcome to the chatbot. Please type a message and press Enter to start the conversation.")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Use a counter to create a unique key for user input
    user_input = st.text_input("You:", key=f"user_input_{len(st.session_state.chat_history)}")

    if user_input:
        response = chatbot(user_input)
        st.session_state.chat_history.append({"user": user_input, "bot": response})
        
        # Display chat history
        for chat in st.session_state.chat_history:
            st.write(f"You: {chat['user']}")
            st.write(f"Bot: {chat['bot']}")

        if response.lower() in ['goodbye', 'bye']:
            st.write("Thank you for chatting with me. Have a great day!")
            st.stop()

if __name__ == '__main__':
    main()
