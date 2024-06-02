import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
import nltk
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from gensim.models import KeyedVectors


nltk.download('stopwords')
stop_words = set(stopwords.words('indonesian'))

# Fungsi untuk membersihkan teks
def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'\d+', '', text)  # Hapus angka
        text = re.sub(r'\s+', ' ', text)  # Hapus spasi berlebih
        text = text.lower()  # Ubah teks menjadi huruf kecil
        text = re.sub(r'[^\w\s]', '', text)  # Hapus tanda baca
        text = ' '.join([word for word in text.split() if word not in stop_words])  # Hapus stopwords
        return text
    return ''

# Load the dataset
data = pd.read_csv('../Data/podcasts_data.csv')
data.head()

data['combined_features'] = data['Genre'].astype(str) + ' ' + data['Podcast Name'].astype(str) + ' ' + data['Description'].astype(str) + ' ' + data['Publisher'].astype(str)
data['combined_features'] = data['combined_features'].apply(clean_text)
data['combined_features'].fillna('', inplace=True)

# Tokenize the text
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['combined_features'])
vocab_size = len(tokenizer.word_index) + 1

# Convert text data to sequences
sequences = tokenizer.texts_to_sequences(data['combined_features'])

# Pad sequences to ensure uniform length
max_sequence_length = max([len(seq) for seq in sequences])
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='post')

# Load pretrained FastText embeddings
embedding_path = 'cc.id.300.vec'  # Path to FastText embeddings
word_vectors = KeyedVectors.load_word2vec_format(embedding_path)

# Create embedding matrix
embedding_dim = 300
embedding_matrix = np.zeros((vocab_size, embedding_dim))

for word, i in tokenizer.word_index.items():
    if word in word_vectors:
        embedding_matrix[i] = word_vectors[word]
    else:
        embedding_matrix[i] = np.random.normal(size=(embedding_dim,))

# Free memory
del word_vectors

# Convert target variable to numeric
label_column = 'Genre'
labels = pd.get_dummies(data[label_column])