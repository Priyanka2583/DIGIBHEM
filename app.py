from flask import Flask, request, jsonify, render_template
import random
import nltk
from nltk.tokenize import word_tokenize
import os

app = Flask(__name__)

# Download necessary NLTK data
nltk.download('punkt')

# Define paths to the data files
MOVIE_LINES_PATH = 'data/movie_lines.txt'
MOVIE_CONVERSATIONS_PATH = 'data/movie_conversations.txt'

# Load and process the dataset
def load_movie_lines():
    lines = {}
    with open(MOVIE_LINES_PATH, 'r', encoding='iso-8859-1') as file:
        for line in file:
            parts = line.split(' +++$+++ ')
            if len(parts) == 5:
                lines[parts[0]] = parts[4].strip()
    return lines

def load_conversations(lines):
    conversations = []
    with open(MOVIE_CONVERSATIONS_PATH, 'r', encoding='iso-8859-1') as file:
        for line in file:
            parts = line.split(' +++$+++ ')
            if len(parts) == 4:
                conv_ids = eval(parts[3])
                conv_lines = [lines[line_id] for line_id in conv_ids if line_id in lines]
                if len(conv_lines) > 1:
                    for i in range(len(conv_lines) - 1):
                        conversations.append((conv_lines[i], conv_lines[i + 1]))
    return conversations

def retrieve_response(user_input):
    user_input_tokens = word_tokenize(user_input.lower())
    responses = []
    for question, answer in conversations:
        question_tokens = word_tokenize(question.lower())
        if set(user_input_tokens).intersection(question_tokens):
            responses.append(answer)
    if responses:
        return random.choice(responses)
    else:
        return "I don't understand."

# Load the dataset
movie_lines = load_movie_lines()
conversations = load_conversations(movie_lines)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = retrieve_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
