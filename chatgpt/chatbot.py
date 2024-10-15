# chatbot.py

import nltk
from nltk.tokenize import word_tokenize
import string

# Download NLTK data files (only the first time)
nltk.download('punkt')

from department_data import departments, member_to_departments

def preprocess(text):
    """
    Lowercase the text and remove punctuation.
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def extract_name(tokens):
    """
    Extract the name from the tokens.
    Assumes the name is the word(s) after 'does' or 'belong to'.
    """
    if 'does' in tokens:
        idx = tokens.index('does')
        # Assume the name follows 'does'
        name_tokens = tokens[idx + 1:]
        # Remove common stopwords
        stopwords = {'belong', 'to', 'department'}
        name = ' '.join([token for token in name_tokens if token not in stopwords])
        return name.strip()
    elif 'belong' in tokens:
        idx = tokens.index('belong')
        name_tokens = tokens[idx + 1:]
        stopwords = {'to', 'department'}
        name = ' '.join([token for token in name_tokens if token not in stopwords])
        return name.strip()
    elif 'is' in tokens:
        idx = tokens.index('is')
        name_tokens = tokens[idx + 1:]
        stopwords = {'in', 'which', 'department'}
        name = ' '.join([token for token in name_tokens if token not in stopwords])
        return name.strip()
    else:
        # Fallback: assume the last word is the name
        return tokens[-1] if tokens else ""

def get_intent(user_input):
    """
    Determine the intent of the user input.
    Returns a tuple (intent, data).
    """
    tokens = word_tokenize(preprocess(user_input))
    
    # Define keywords for intents
    list_keywords = {"what", "list", "give", "show", "all", "members", "in", "department", "of"}
    find_keywords = {"which", "does", "belong", "to", "department", "belongs", "is"}

    # Intent: List all members of a department
    if any(word in tokens for word in ["what", "list", "give", "show", "all"]):
        for department in departments.keys():
            department_tokens = department.replace("_", " ").split()
            if any(token in department_tokens for token in tokens):
                return ("list_members_intent", department)
    
    # Intent: Find department of a specific member
    if any(word in tokens for word in ["which", "does", "belong", "belongs", "is"]):
        name = extract_name(tokens)
        if name:
            return ("find_department_intent", name)
    
    return ("unknown_intent", None)

def respond(intent, data):
    """
    Generate a response based on the intent and data.
    """
    if intent == "list_members_intent":
        department = data
        # Capitalize department name appropriately
        department_display = format_department_name(department)
        members = departments.get(department, [])
        if members:
            response = f"The members of the {department_display} Department are:\n" + "\n".join(members)
        else:
            response = f"I don't have information about the {department_display} Department."
        return response
    
    elif intent == "find_department_intent":
        name_query = data.lower()
        matching_departments = set()
        matching_members = []

        for member_full_name, deps in member_to_departments.items():
            if name_query in member_full_name:
                matching_departments.update(deps)
                matching_members.append(member_full_name)
        
        if matching_departments:
            if len(matching_departments) == 1:
                # Single department
                department_display = format_department_name(next(iter(matching_departments)))
                response = f"The name '{data}' belongs to the {department_display} Department."
            else:
                # Multiple departments
                departments_display = ", ".join([format_department_name(dep) for dep in sorted(matching_departments)])
                response = f"The name '{data}' belongs to the following departments: {departments_display}."
            return response
        else:
            return f"I couldn't find any departments for the name '{data}'. Please check the name and try again."
    
    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

def format_department_name(department_key):
    """
    Customize the display format for department names.
    """
    format_mapping = {
        "cse": "CSE",
        "ece": "ECE",
        "cce": "CCE (Computer and Communication)",
        "ee_vlsi_d&t": "EE VLSI D&T",
        "ec_vlsi": "EC VLSI",
        "csbs": "CSBS (Computer Science and Business Systems)",
        "ai_ds": "AI&DS (Artificial Intelligence and Data Science)",
        "cse_ai_ml": "CSE (AI&ML)",
        "mechanical": "Mechanical"
    }
    return format_mapping.get(department_key, department_key.upper())

def chatbot():
    """
    Main chatbot loop.
    """
    print("Hello! I'm DepartmentBot. You can ask me about department members or which department a member belongs to.")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("DepartmentBot: Goodbye!")
            break
        intent, data = get_intent(user_input)
        response = respond(intent, data)
        print(f"DepartmentBot: {response}\n")

if __name__ == "__main__":
    chatbot()
