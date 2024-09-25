import numpy as np
import tensorflow as tf
from keras import models ,utils ,layers
import pickle

MODEL_PATH = "../models/sentiment_analysis_model_optimized.h5"
# Load the saved model
model = models.load_model(MODEL_PATH)

# Load the TextVectorization layer configuration and weights
with open('../models/vectorizer_config.pickle', 'rb') as handle:
    vectorizer_config = pickle.load(handle)

with open('../models/vectorizer_weights.pickle', 'rb') as handle:
    vectorizer_weights = pickle.load(handle)

# Recreate the TextVectorization layer
vectorizer =layers.TextVectorization.from_config(vectorizer_config)
#vectorizer.set_weights(vectorizer_weights)
vectorizer.set_vocabulary(vectorizer_weights)

def encode_texts(text_list):
    return vectorizer(text_list)

def predict_sentiments(text_list):
    encoded_inputs = encode_texts(text_list)
    predictions = np.argmax(model.predict(encoded_inputs), axis=-1)
    sentiments = []
    for prediction in predictions:
        if prediction == 0:
            sentiments.append("Negative")
        elif prediction == 1:
            sentiments.append("Neutral")
        else:
            sentiments.append("Positive")
    return sentiments