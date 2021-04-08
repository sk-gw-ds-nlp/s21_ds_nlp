from flask import Flask
app = Flask(__name__)

import spacy

nlp = spacy.load("en")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('submit_doc')
def submit_doc():
    # pull doc as submitted
    
    return tbd