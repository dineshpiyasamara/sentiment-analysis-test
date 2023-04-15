from flask import Flask, render_template, request, redirect
from helper import preprocessing, get_pred
from logger import logging

app = Flask(__name__)

logging.info("App started")

data = dict()
reviews = []
negative = 0
positive = 0


@app.route('/')
def index():
    data['reviews'] = reviews
    data['negative'] = negative
    data['positive'] = positive
    logging.info("Index page is open")
    return render_template('index.html', data=data)


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    logging.info("Get text from form: " + text)

    preprocessed_text = preprocessing(text)
    logging.info("Text preprocessed")

    pred = get_pred(preprocessed_text)
    logging.info("Prediction: " + str(pred))

    if pred == 1:
        global negative
        negative += 1
    else:
        global positive
        positive += 1
    reviews.insert(0, text)
    logging.info("Review added")

    return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
