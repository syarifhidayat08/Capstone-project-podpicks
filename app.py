from flask import Flask, request, jsonify
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import joblib
import numpy as np
from google.cloud import firestore
import pandas as pd
from sklearn.utils import shuffle
import re
import nltk
from nltk.corpus import stopwords

# Initialize Flask app
app = Flask(_name_)


bert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Set up Firestore authentication
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./path/to/model/json"

# Initialize Firestore client
db = firestore.Client()

# Function to clean text
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = text.strip()  # Remove leading and trailing whitespace
    stop_words = set(stopwords.words('english'))
    text = ' '.join(word for word in text.split() if word not in stop_words)  # Remove stop words
    return text

# Function to fetch podcast data from Firestore
def fetch_podcast_data():
    podcasts_ref = db.collection('podcast_data')
    docs = podcasts_ref.stream()

    data = []
    for doc in docs:
        podcast_dict = doc.to_dict()
        podcast_dict['id'] = doc.id  # Add document ID to the podcast dictionary
        data.append(podcast_dict)

    dataset = pd.DataFrame(data)
    dataset = shuffle(dataset).reset_index(drop=True)  # Shuffle dataset

    # Clean the dataset
    dataset['Podcast Name'] = dataset['Podcast Name'].apply(clean_text)
    dataset['Genre'] = dataset['Genre'].apply(clean_text)

    # Drop rows with NaN values in 'Podcast Name' column
    podcast_data = dataset.dropna(subset=['Podcast Name'])

    # Extract relevant columns
    podcast_names = podcast_data['Podcast Name'].values
    podcast_descriptions = podcast_data['Description'].values
    podcast_publishers = podcast_data['Publisher'].values
    podcast_spotify_urls = podcast_data['Spotify URL'].values
    podcast_cover_image_urls = podcast_data['Cover Image URL'].values
    podcast_ids = podcast_data['id'].values  # Extract document IDs

    # Encode podcast names using Sentence-BERT
    podcast_embeddings = bert_model.encode(podcast_names, convert_to_tensor=True)

    return {
        'names': podcast_names,
        'descriptions': podcast_descriptions,
        'publishers': podcast_publishers,
        'spotify_urls': podcast_spotify_urls,
        'cover_image_urls': podcast_cover_image_urls,
        'embeddings': podcast_embeddings,
        'ids': podcast_ids  # Include document IDs in the returned data
    }

# Fetch podcast data from Firestore
podcast_data = fetch_podcast_data()

podcast_names = podcast_data['names']
podcast_descriptions = podcast_data['descriptions']
podcast_publishers = podcast_data['publishers']
podcast_spotify_urls = podcast_data['spotify_urls']
podcast_cover_image_urls = podcast_data['cover_image_urls']
podcast_embeddings = podcast_data['embeddings']
podcast_ids = podcast_data['ids']  # Retrieve document IDs

# Function to search for similar podcasts
@app.route('/search', methods=['GET'])
def search_podcasts():
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    query_embedding = bert_model.encode([query], convert_to_tensor=True)
    cosine_scores = cosine_similarity(query_embedding, podcast_embeddings)

    # Get the indices of all podcasts sorted by similarity
    sorted_indices = np.argsort(cosine_scores[0])[::-1]

    # Retrieve the top 5 unique podcasts
    seen = set()
    similar_podcasts = []
    for idx in sorted_indices:
        if len(similar_podcasts) >= 5:
            break
        podcast_name = podcast_names[idx]
        if podcast_name not in seen:
            seen.add(podcast_name)
            similar_podcasts.append({
                'ID': podcast_ids[idx],  # Include document ID
                'Name': podcast_name,
                'Description': podcast_descriptions[idx],
                'Publisher': podcast_publishers[idx],
                'Spotify URL': podcast_spotify_urls[idx],
                'Cover Image URL': podcast_cover_image_urls[idx]
            })

    return jsonify(similar_podcasts)

# Ensure the Flask app runs only if this script is executed directly
if _name_ == '_main_':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)