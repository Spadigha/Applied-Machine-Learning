from flask import Flask, render_template, url_for, request
# Flask: To create flask app
# render_template: To render `Html` templates
# url_for: To access file paths
# request:

import pandas as pd
import numpy as np

# Python NLP library
from nltk.stem.porter import PorterStemmer

# For string operations
import re # Regex to exploit patterns in strings
import string

from sklearn.feature_extraction.text import CountVectorizer
# You may also use Tfidf instead.
from sklearn.linear_model import LogisticRegression # for prediction


# To remove a given pattern in a given string
def remove_pattern(input_text, pattern):
    # store all text with given pattern in it
    # inside a list
    r = re.findall(pattern, input_text)
    
    # loop over all the texts with pattern in the list
    for i in r:
        # substitute a text with given pattern (i)
        # with empty value "" i.e remove it in "input_text"
        # ---------------------------------------------------------
        # re.sub(<where-to-replace-in-main-string>,
        #        <what-to-replace-with-in-main-string>,
        #        <main-string>)
        # ---------------------------------------------------------
        # Note: `i` will not be replaced in <main-string> in-place.
        # Replaced string is returned by re.sub() which is stored
        # in `input_text` i.e original text is overwritten with
        # the replaced one
        input_text = re.sub(i, "", input_text)
    
    return input_text # return replaced string.
    
    
# To count number of punctuations to increase our
# model accuracy
# TBH, it returns percent not count
def count_punct(text):
    num_of_puncts = sum([1 for char in text if char in string.punctuation])
    tota_chars_excluding_spaces = len(text) - text.count(" ")
    percent_of_puncts = round( (num_of_puncts / tota_chars_excluding_spaces), 3) * 100
    return percent_of_puncts

# initialize app
app = Flask(__name__)

# Load data
data = pd.read_csv("../data/sentiment.tsv",sep = '\t')


