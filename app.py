import string
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
from collections import Counter
from flask import Flask, render_template, request
import os
from io import BytesIO
import base64
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer


app = Flask(__name__)

def clean_text(text):
    cleaned_text = text.lower().translate(str.maketrans("", "", string.punctuation))
    return cleaned_text

def tokenize_text(cleaned_text):
    tokenized_words = word_tokenize(cleaned_text)
    return tokenized_words
def sentiment_analyze(sentiment_text):
    score=SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    return score
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_text = request.form['user_text']
        cleaned_text = clean_text(user_text)
        tokenized_words = tokenize_text(cleaned_text)
        final_words = []
        for word in tokenized_words:
            if word not in stopwords.words('english'):
                final_words.append(word)
        emotion_list = []
        with open('emotions.text') as file:
            for line in file:
                clear_line = line.replace(',\n', '').replace("'", "").strip()
                word, emotion = clear_line.split(':')
                if word in final_words:
                    emotion_list.append(emotion)
        word_counts = Counter(emotion_list)
        fig, ax1 = plt.subplots()
        ax1.bar(word_counts.keys(), word_counts.values())
        fig.autofmt_xdate()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        ax=plt.axes()
        ax.set_facecolor("violet")
        plt.show()
        score=sentiment_analyze(cleaned_text)
         # Encode the plot image as base64 string
        plot_image = base64.b64encode(buffer.read()).decode()

        return render_template('result.html', word_counts=word_counts,plot_image=plot_image,score=score)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000,debug=True)
