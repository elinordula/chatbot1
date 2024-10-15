from flask import Flask, request, jsonify, render_template
import os
import ssl
import nltk
import json
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
intents_file_path = "D:/Mridula/stud chatbot/stupid/intents.json"
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

# Initialize Flask app
app = Flask(__name__)

# Serve the HTML file (index1.html)
@app.route('/')
def index():
    return render_template('index1.html')  # Make sure 'index1.html' is in the 'templates' folder

# Endpoint for handling chatbot response
@app.route('/get-response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    response = chatbot(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
