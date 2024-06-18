from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, TimeDistributed, Bidirectional, Dropout
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.utils import shuffle
from sentence_transformers import SentenceTransformer
from keras import backend as K
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords

# Initialize Flask app
app = Flask(__name__)

nltk.download('stopwords')

# Global variables to store data and models
tokenizer = None
model = None
bert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
podcast_names = None
podcast_descriptions = None
podcast_publishers = None
podcast_spotify_urls = None
podcast_cover_image_urls = None
podcast_embeddings = None

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

# Route for uploading dataset and training the model
@app.route('/upload', methods=['GET', 'POST'])
def upload_and_train():
    global tokenizer, model, podcast_names, podcast_descriptions, podcast_publishers, podcast_spotify_urls, podcast_cover_image_urls, podcast_embeddings

    if request.method == 'POST':
        # Load the dataset
        file = request.files['file']
        dataset = pd.read_csv(file)
        dataset = shuffle(dataset)

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

        # Tokenization and Vectorization
        tokenizer = Tokenizer(oov_token="<OOV>")
        tokenizer.fit_on_texts(podcast_names)

        # Convert podcast names to sequences of integers
        sequences = tokenizer.texts_to_sequences(podcast_names)

        # Pad sequences to have the same length
        max_length = max(len(seq) for seq in sequences)
        padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post')

        # Get the vocabulary size for the embedding layer
        vocab_size = len(tokenizer.word_index) + 1

        # Build the model
        model = Sequential([
            Embedding(input_dim=vocab_size, output_dim=128, input_length=max_length),
            Bidirectional(LSTM(64, return_sequences=True)),
            Dropout(0.5),
            Bidirectional(LSTM(64, return_sequences=True)),
            Dropout(0.5),
            TimeDistributed(Dense(vocab_size, activation='softmax'))
        ])

        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.summary()

        # Prepare labels to match the output shape of the model
        labels = np.expand_dims(padded_sequences, axis=-1)

        # Train the model
        model.fit(padded_sequences, labels, epochs=30, batch_size=128, validation_split=0.2)

        # Encode podcast names using Sentence-BERT
        podcast_embeddings = bert_model.encode(podcast_names, convert_to_tensor=True)

        return jsonify({"message": "Model trained successfully!"})
    return render_template('upload.html')

# Function to search for similar podcasts
@app.route('/search', methods=['GET'])
def search_podcasts():
    global podcast_embeddings

    query = request.args.get('query')
    top_k = int(request.args.get('top_k', 5))

    query_embedding = bert_model.encode([query], convert_to_tensor=True)
    cosine_scores = cosine_similarity(query_embedding, podcast_embeddings)

    # Get the top_k similar podcasts
    top_k_indices = np.argsort(cosine_scores[0])[-top_k:][::-1]

    # Retrieve the corresponding podcast names
    similar_podcasts = [{
        'Name': podcast_names[idx],
        'Description': podcast_descriptions[idx],
        'Publisher': podcast_publishers[idx],
        'Spotify URL': podcast_spotify_urls[idx],
        'Cover Image URL': podcast_cover_image_urls[idx]
    } for idx in top_k_indices]

    return jsonify(similar_podcasts)

if __name__ == '__main__':
    app.run(debug=True)
