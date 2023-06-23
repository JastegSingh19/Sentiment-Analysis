# Table of Contents
- [Youtube Comment-Analysis](#youtube-comment-analysis)
- [Flask Website](#flask-website)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Website](#running-the-website)
# <a name="youtube-comment-analysis"></a>Youtube Comment-Analysis
In my project, I utilized the YouTube Data API to fetch comments from a specific video and performed text preprocessing tasks such as cleaning, tokenization, and removal of stopwords. Additionally, I integrated over 100 emojis and 520 words using Python libraries like emoji and regular expressions to identify and extract emojis and stickers from the comments. To analyze the sentiment of the comments, I employed the VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis model, which provided sentiment scores including positive, negative, neutral, and compound scores. To visually represent the emotions detected in the comments, I created a bar graph highlighting the most common emotions. Finally, I developed a Flask web application that offers a user-friendly interface where users can input a YouTube video URL and retrieve sentiment analysis results.
# <a name="flask-website"></a>Flask Website
Thank you for cloning the Flask Website repository! This document will guide you through the steps to run the website locally on your machine.

## <a name="prerequisites"></a>Prerequisites
- Python 3.7 or higher
- pip package manager

## <a name="installation"></a>Installation

1. Clone the repository to your local machine:
$ git clone https://github.com/JastegSingh19/Sentiment-Analysis
2. Navigate to the project directory:
$ cd flask-website
3. Create a virtual environment (optional but recommended):
$ python3 -m venv venv
$ source venv/bin/activate
4. Install the required packages:
$ pip install -r requirements.txt
## Running the Website

1. Start the Flask development server:
$ python app.py
2. Open your web browser and visit the following URL:
http://localhost:8000/
I will be using api calls from diffrent websites to take the reviews of a product or a post and then give it's sentiment
Thank You!
