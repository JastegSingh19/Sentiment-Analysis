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
import googleapiclient.discovery
import re
import emoji

app = Flask(__name__)

def clean_text(text):
    cleaned_text = text.lower().translate(str.maketrans("", "", string.punctuation))
    cleaned_text=cleaned_text.replace('\n\n', '')
    cleaned_text=cleaned_text.strip()
    return cleaned_text

def tokenize_text(cleaned_text):
    tokenized_words = word_tokenize(cleaned_text)
    return tokenized_words
def sentiment_analyze(sentiment_text):
    score=SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    return score
def youtube_response(id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDckDdv1EnENKj8qWFcBXLsXKjaZbu0amI"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=id,
        maxResults = 100
    )
    response = request.execute()
    return response



def extract_video_id(url):
    video_id = None
    pattern = r"(?:v=|v\/|embed\/|youtu.be\/|\/v\/|\/embed\/|\/youtu.be\/|\/watch\?v=|\&v=|\/watch\?vi=|\/watch\?feature=player_embedded&v=|%2Fvideos%2F|embed%2F|vi%2F|v%2F|e\/|watch\?v%3D|youtu.be%2F|%2Fv%2F|embed%2F|%2Fvi%2F)([^#\&\?\/\s]*)"
    matches = re.findall(pattern, url)

    if matches:
        video_id = matches[0]

    return video_id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_url = request.form['user_text']
        if not user_url:
            error_message = "Please provide a valid YouTube URL."
            return render_template('index.html', error_message=error_message)
        id=extract_video_id(user_url)
        response=youtube_response(id)
        all_comments = ""

        # Assuming the response is stored in the 'response' variable
        if 'items' in response:
            for item in response['items']:
                if 'snippet' in item and 'topLevelComment' in item['snippet']:
                    comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
                    all_comments += comment

        print(all_comments)
        cleaned_text = clean_text(all_comments)
        print(cleaned_text)
        tokenized_words = tokenize_text(cleaned_text)

        final_words = []
        for word in tokenized_words:
            if word not in stopwords.words('english'):
                final_words.append(word)
        for character in cleaned_text:
            if emoji.emoji_count(character) > 0:
                final_words.append(character)
        emotion_list = []
        with open('emotions.text') as file:
            for line in file:
                clear_line = line.replace(',\n', '').replace("'", "").strip()
                word, emotion = clear_line.split(':')
                if word in final_words:
                    emotion_list.append(emotion)
        with open('stickers.text') as file:
            for line in file:
                clear_line = line.replace(',\n', '').replace("'", "").strip()
                word, emotion = clear_line.split(':')
                print(word)
                if word in final_words:
                    emotion_list.append(emotion)
        print(final_words)
        word_counts = Counter(emotion_list)
        fig, ax1 = plt.subplots()
        ax1.bar(word_counts.keys(), word_counts.values())
        fig.autofmt_xdate()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        ax=plt.axes()
        ax.set_facecolor("violet")
        score=sentiment_analyze(cleaned_text)
         # Encode the plot image as base64 string
        plot_image = base64.b64encode(buffer.read()).decode()

        return render_template('result.html', word_counts=word_counts,plot_image=plot_image,score=score)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000,debug=True)
