import os
import ssl
import nltk
import json
import streamlit as st
import random
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
faculty_info = {}  # To store faculty names and their department

for intent in intents['intents']:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)
    
    # Extract faculty names and department
    if intent['tag'] == "cse faculty_list":
        for response in intent['responses']:
            # Split the response by lines to extract faculty names
            faculty_lines = response.split("\n")
            for line in faculty_lines:
                # Assume the format is consistent and extract the name
                if "–" in line:  # Split only if there's a dash indicating a name
                    name = line.split("–")[0].strip()  # Get the name part
                    faculty_info[name] = "CSE Department"  # Map to department

# Training the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

# Define the chatbot function
def chatbot(input_text):
    input_text_lower = input_text.lower().strip()  # Normalize input to lowercase

    # Check for faculty member queries
    for faculty_name in faculty_info.keys():
        if faculty_name.lower() in input_text_lower:
            return f"{faculty_name} - {faculty_info[faculty_name]}"

    # Check for exact matches in the intents
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if input_text_lower == pattern.lower():  # Check for exact match
                return random.choice(intent['responses'])  # Return the matching response immediately

    # If no exact match, use fuzzy matching to find the closest pattern
    closest_matches = difflib.get_close_matches(input_text_lower, [p.lower() for p in patterns], n=1, cutoff=0.6)
    if closest_matches:
        closest_pattern = closest_matches[0]
        # Find the corresponding intent tag
        for intent in intents['intents']:
            if closest_pattern in [p.lower() for p in intent['patterns']]:
                return random.choice(intent['responses'])

    # If no intent is matched, provide a default response
    return "I'm sorry, I didn't understand that. Can you please rephrase?"


# Streamlit UI
def main():
    st.title("AIML Department Chatbot")
    st.write("Welcome to the AIML department's chatbot. Please type a message and press Enter to start the conversation.")
    
    counter = 0
    user_input = st.text_input("You:", key=f"user_input_{counter}")

    if user_input:
        response = chatbot(user_input)
        st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=f"chatbot_response_{counter}")

        if response.lower() in ['goodbye', 'bye']:
            st.write("Thank you for chatting with me. Have a great day!")
            st.stop()

if __name__ == "__main__":  # Correct the main function call
    main()
