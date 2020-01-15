# -------------------------------------------------------------
# See detailed analysis in .ipynb file in ./
# -------------------------------------------------------------



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
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder() # for one hot encoding

import pickle5 as pickle


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
def count_punc(text):
    num_of_puncts = sum([1 for char in text if char in string.punctuation])
    tota_chars_excluding_spaces = len(text) - text.count(" ")
    percent_of_puncts = round( (num_of_puncts / tota_chars_excluding_spaces), 3) * 100
    return percent_of_puncts

# Load data
data = pd.read_csv("./data/sentiment.tsv",sep = '\t')
# name cols
data.columns = ["label", "body_text"]

# encode `labels` col
data['label'] = data['label'].map({'pos': 0, 'neg': 1})
# 1 --> Positive
# 0 --> Negative

# Remove twitter hadles
vecfunc = np.vectorize(remove_pattern)
data['handle_removed'] = vecfunc(data["body_text"], "@[\w]*")

# remove punctuations
data['puncs_removed'] = data['handle_removed'].str.replace("[^a-zA-Z#]", " ")

# Tokenize before stemming. 
# Tokenize: Split into particular words i.e into list
tokenized_tweet = data['puncs_removed'].apply(lambda x: x.split())

# Stemming
from nltk.stem.porter import *
stemmer = PorterStemmer()
# Iterate over every word in each list 
# So that `having` and `have` both can be converted into `have`
stemmed_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x])

# convert list of words into a line
for i in range(len(stemmed_tweet)):
    stemmed_tweet[i] = ' '.join(stemmed_tweet[i])
data["stemmed_tweet"] = stemmed_tweet

# To increase acc. score,
# add length column for original body
data['body_len'] = data["body_text"].apply(lambda x: len(x) - x.count(" ")) 
# add `percent_of_puncs` col
data['punc%'] = data["body_text"].apply(lambda x: count_punc(x))

# COUNT VECTORIZER
# -------------------------------------
# Counts number of occurances in a row.
from sklearn.feature_extraction.text import CountVectorizer
bow_vectorizer = CountVectorizer(stop_words='english')

#transform
bow = bow_vectorizer.fit_transform(data['stemmed_tweet'])

X_features = pd.concat([
                    data['body_len'],
                    data['punc%'],
                    pd.DataFrame(bow.toarray()) # convt to df
              ], axis = 1)
y = data['label']

model = LogisticRegression(C=0.1, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=1000,
                   multi_class='auto', n_jobs=None, penalty='l2',
                   random_state=None, solver='lbfgs', tol=0.0001, verbose=0,
                   warm_start=False)


# split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_features, y, test_size=0.33, random_state=42)

# Train on whole dataset
#model.fit(X_features, y)
model.fit(X_train, y_train)

#save vectorizer
model._vectorizer = bow_vectorizer

#save model
pickle.dump(model, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))


# test dataset
print(model.predict(X_test))
print(model.score(X_test, y_test))


# ------------------test-on-single-message----------------------------------
# -------------------------------------------------------------------------- 
message = '@ram ... i SOOOOOO .. wanted Labron an nem 2go to the finals &amp;beat up on Kobe an nem.. dammit. go magic..... '
df = pd.DataFrame([[message]])
#print(df.head())

vecfunc = np.vectorize(remove_pattern)
df[0] = vecfunc(df[0], "@[\w]*")
#print(df.head())

df["tidy"] = df[0].str.replace("[^a-zA-Z#]", " ")
#print(df.head())

tokenized_message = df["tidy"].apply(lambda x: x.split())
#print(tokenized_message.head())

from nltk.stem.porter import *
stemmer = PorterStemmer()
stemmed_message = tokenized_message.apply(lambda x: [stemmer.stem(i) for i in x])
#print(stemmed_message.head())

for i in range(len(stemmed_message)):
    stemmed_message[i] = ' '.join(stemmed_message[i])
df["tidy"] = stemmed_message
#print(df.head())

df['body_len'] = df[0].apply(lambda x: len(x) - x.count(" "))
df['punc%'] = df[0].apply(lambda x: count_punc(x))
#print(df["body_len"].head())
#print(df["punc%"].head())

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(stop_words='english')
#scipy_sparse_csr_matrix = cv.transform(df['tidy'])
scipy_sparse_csr_matrix = model._vectorizer.transform(df['tidy']) # use `transform` instead of `fit_transform
                                                                  # as we are using saved `vectorizer`

X = pd.concat([
                    df['body_len'],
                    df['punc%'],
                    pd.DataFrame(scipy_sparse_csr_matrix.toarray())
              ], axis = 1)

#print(X.head())

print(model.predict(X))
