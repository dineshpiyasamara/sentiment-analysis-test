import pickle
import re
import numpy as np
import pandas as pd

import nltk
nltk.download('stopwords', download_dir='nltk_data')

with open('nltk_data/corpora/stopwords/english', 'r') as file:
    sw = file.read().splitlines()

with open('static/model/model_pkl', 'rb') as f:
    model = pickle.load(f)

vocab = pd.read_csv('static/model/vocabulary.txt', header=None)
tokens = vocab[0].tolist()


def preprocessing(text):
    data = pd.DataFrame([text])
    data[0] = data[0].apply(lambda x: " ".join(x.lower() for x in x.split()))
    data[0] = data[0].apply(lambda x: " ".join(
        re.sub(r'^https?:\/\/.*[\r\n]*', '', x, flags=re.MULTILINE) for x in x.split()))
    data[0] = data[0].str.replace('[^\w\s]', '')
    data[0] = data[0].str.replace('\d', '')
    data[0] = data[0].apply(lambda x: " ".join(
        x for x in x.split() if x not in sw))
    data = data[0]
    return data


def get_pred(preprocessed_text):
    vectorized_test_lst = []
    for sentence in preprocessed_text:
        sentence_lst = np.zeros(len(tokens))
        for i in range(len(tokens)):
            if tokens[i] in sentence.split():
                sentence_lst[i] = 1
        vectorized_test_lst.append(sentence_lst)
    tested = np.asarray(vectorized_test_lst, dtype=np.float32)
    return model.predict(tested)
