from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import re
import nltk
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, LSTM, Bidirectional, TimeDistributed
from transformers import BertTokenizer, TFBertModel
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

# Define global variables
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = None
bert_model = TFBertModel.from_pretrained('bert-base-uncased')

def load_dataset(file_path):
    dataset = pd.read_csv(file_path)
    dataset = dataset.sample(frac=1).reset_index(drop=True)
    return dataset

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    stop_words = set(stopwords.words('english') + stopwords.words('indonesian'))
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

def prepare_data(dataset):
    dataset['Podcast Name'] = dataset['Podcast Name'].apply(clean_text)
    dataset['Genre'] = dataset['Genre'].apply(clean_text)
    dataset = dataset.dropna(subset=['Podcast Name'])

    podcast_names = dataset['Podcast Name'].values
    podcast_genres = dataset['Genre'].values
    podcast_descriptions = dataset['Description'].values
    podcast_publishers = dataset['Publisher'].values
    podcast_spotify_urls = dataset['Spotify URL'].values
    podcast_cover_image_urls = dataset['Cover Image URL'].values

    # Encode genres as binary labels (adjust this to fit your actual binary classification needs)
    label_encoder = LabelEncoder()
    podcast_labels = label_encoder.fit_transform(podcast_genres)

    return podcast_names, podcast_labels, podcast_descriptions, podcast_publishers, podcast_spotify_urls, podcast_cover_image_urls

def bert_encode(texts, tokenizer, max_len=512):
    input_ids = []
    attention_masks = []

    for text in texts:
        encoded = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_len,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='tf',
        )
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])

    input_ids = np.array(input_ids).squeeze()
    attention_masks = np.array(attention_masks).squeeze()
    return input_ids, attention_masks

def build_model():
    input_ids = tf.keras.Input(shape=(512,), dtype=tf.int32, name='input_ids')
    attention_mask = tf.keras.Input(shape=(512,), dtype=tf.int32, name='attention_mask')
    
    bert_output = bert_model([input_ids, attention_mask])
    cls_token = bert_output.last_hidden_state[:, 0, :]  # Extract the representation of the [CLS] token
    
    dense_output = Dense(512, activation='relu')(cls_token)
    dropout_output = Dropout(0.5)(dense_output)
    output = TimeDistributed(Dense(vocab_size, activation='softmax'))(dropout_output)
    
    model = tf.keras.Model(inputs=[input_ids, attention_mask], outputs=output)
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

@app.route('/train', methods=['POST'])
def train_model():
    global model
    file_path = request.json['file_path']
    dataset = load_dataset(file_path)
    podcast_names, podcast_labels, podcast_descriptions, podcast_publishers, podcast_spotify_urls, podcast_cover_image_urls = prepare_data(dataset)
    
    input_ids, attention_masks = bert_encode(podcast_names, tokenizer)
    
    X_train, X_test, y_train, y_test = train_test_split(input_ids, podcast_labels, test_size=0.2, random_state=42)
    attention_train, attention_test = train_test_split(attention_masks, test_size=0.2, random_state=42)
    
    model = build_model()
    model.fit([X_train, attention_train], y_train, epochs=3, batch_size=8, validation_data=([X_test, attention_test], y_test))
    
    return jsonify({'message': 'Model trained successfully'})

@app.route('/predict', methods=['POST'])
def predict():
    global model, tokenizer
    data = request.json['data']
    cleaned_data = clean_text(data)
    
    print(f"Cleaned Data: {cleaned_data}")  # Debugging
    
    input_ids, attention_masks = bert_encode([cleaned_data], tokenizer)
    
    print(f"Input IDs: {input_ids}")  # Debugging
    print(f"Attention Masks: {attention_masks}")  # Debugging
    
    predictions = model.predict([input_ids, attention_masks])
    predicted_label = np.round(predictions).astype(int)
    
    print(f"Predicted Label: {predicted_label}")  # Debugging
    
    return jsonify({'prediction': int(predicted_label[0][0])})

if __name__ == '__main__':
    app.run(debug=True)
