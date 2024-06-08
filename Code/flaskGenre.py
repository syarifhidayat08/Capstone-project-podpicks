from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

class PodcastRecommender:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.clean_data()
        self.create_tfidf_matrix()
        self.create_similarity_matrix()

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        stop_words = set(stopwords.words('english'))
        text = ' '.join(word for word in text.split() if word not in stop_words)
        return text

    def clean_data(self):
        self.data['Podcast Name'] = self.data['Podcast Name'].apply(self.clean_text)
        self.data['Genre'] = self.data['Genre'].apply(self.clean_text)

    def create_tfidf_matrix(self):
        self.tfidf = TfidfVectorizer()
        self.combined_text = self.data['Genre']
        self.tfidf_matrix = self.tfidf.fit_transform(self.combined_text)

    def create_similarity_matrix(self):
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
        with tf.device('/CPU:0'):
            self.similarity_tensor = tf.convert_to_tensor(self.similarity_matrix)

    def get_top_k_podcasts(self, input_genre, k=5):
        genre_index = self.data[self.data["Genre"] == input_genre].index[0]
        with tf.device('/CPU:0'):
            top_k_values, top_k_indices = tf.nn.top_k(self.similarity_tensor[genre_index], k=k+1)
        top_k_genre = self.data.loc[top_k_indices.numpy()]
        return top_k_genre

# Initialize recommender with the data path
recommender = PodcastRecommender('D:/Capstone/Data/podcasts_data.csv')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        input_genre = data.get('genre', '')
        if not input_genre:
            return jsonify({'error': 'No genre provided'}), 400

        top_k_genre = recommender.get_top_k_podcasts(input_genre)
        response = top_k_genre.to_dict(orient='records')
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
