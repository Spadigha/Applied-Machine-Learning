from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import string
import re

from nltk.stem.porter import *
stemmer = PorterStemmer()

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))

def count_punc(text):
    num_of_puncts = sum([1 for char in text if char in string.punctuation])
    tota_chars_excluding_spaces = len(text) - text.count(" ")
    percent_of_puncts = round( (num_of_puncts / tota_chars_excluding_spaces), 3) * 100
    return percent_of_puncts

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


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # USER DATA
        message = request.form['message']

        # predict on user entered data
        df = pd.DataFrame([[message]]) # index(col) 0 : original message
        
        # remove handle
        vecfunc = np.vectorize(remove_pattern)
        df[0] = vecfunc(df[0], "@[\w]*")
        
        #remove puncs, tokenize, stem
        df["tidy"] = df[0].str.replace("[^a-zA-Z#]", " ") 
        tokenized_message = df["tidy"].apply(lambda x: x.split())
        stemmed_message = tokenized_message.apply(lambda x: [stemmer.stem(i) for i in x])

        # convt stemmed message (list of strings) into a string
        for i in range(len(stemmed_message)):
            stemmed_message[i] = ' '.join(stemmed_message[i])
        df["tidy"] = stemmed_message

        # extra cols based on original message
        df['body_len'] = df[0].apply(lambda x: len(x) - x.count(" "))
        df['punc%'] = df[0].apply(lambda x: count_punc(x))

        # based on saved _vectorizer
        scipy_sparse_csr_matrix = model._vectorizer.transform(df['tidy'])
        X = pd.concat([
                    df['body_len'],
                    df['punc%'],
                    pd.DataFrame(scipy_sparse_csr_matrix.toarray())
              ], axis = 1)
        
        my_pred = model.predict(X)

    return render_template('result.html', prediction = my_pred)


if __name__ == "__main__" :
    app.run(debug=True) 