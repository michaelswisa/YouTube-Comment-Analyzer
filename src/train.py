import os
import numpy as np
import tensorflow as tf
from keras import layers, models, regularizers
import pickle
import pandas as pd

# Parameters
VOCAB_SIZE = 10000
MAX_LEN = 250
EMBEDDING_DIM = 16
MODEL_PATH = './models/sentiment_analysis_model_optimized.h5'

file_path = r'./data/data.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')
df_shuffled = data.sample(frac=1).reset_index(drop=True)

texts = df_shuffled.iloc[:, -1].values
labels = df_shuffled.iloc[:, 0].apply(lambda x: 0 if x == 0 else 1 if x == 2 else 2).values

# Text vectorization layer
vectorizer = layers.TextVectorization(max_tokens=VOCAB_SIZE, output_sequence_length=MAX_LEN)
vectorizer.adapt(texts)

# Vectorize the texts
padded_sequences = vectorizer(texts)

# Save the vectorizer configuration and weights
vectorizer_config = vectorizer.get_config()
vectorizer_weights = vectorizer.get_weights()

with open('./models/vectorizer_config.pickle', 'wb') as handle:
    pickle.dump(vectorizer_config, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./models/vectorizer_weights.pickle', 'wb') as handle:
    pickle.dump(vectorizer.get_vocabulary(), handle, protocol=pickle.HIGHEST_PROTOCOL)

# Split data into training and test sets (more balanced)
split_index = int(0.8 * len(padded_sequences))  # 80% training, 20% test
train_data = padded_sequences[:split_index]
test_data = padded_sequences[split_index:]
train_labels = labels[:split_index]
test_labels = labels[split_index:]

# Check if saved model exists
if os.path.exists(MODEL_PATH):
    print("Loading saved model...")
    model = models.load_model(MODEL_PATH)
else:
    print("Training a new model...")

    # Define the model with improvements
    model = models.Sequential([
        layers.Embedding(VOCAB_SIZE, EMBEDDING_DIM, input_length=MAX_LEN),
        layers.SpatialDropout1D(0.2),  # Spatial Dropout to prevent overfitting in Embedding
        layers.Bidirectional(layers.LSTM(64, return_sequences=True)),  # LSTM for capturing sequence information
        layers.GlobalMaxPooling1D(),  # Global max pooling to reduce dimensionality
        layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001)),  # L2 regularization
        layers.Dropout(0.5),  # Dropout to prevent overfitting
        layers.Dense(3, activation='softmax')  # 3 classes: negative, neutral, positive
    ])

    # Compile the model with a custom optimizer and learning rate
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train the model with early stopping and learning rate reduction on plateau
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    lr_reduction = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-6)

    model.fit(
        train_data, train_labels,
        epochs=15,  # Increased epochs for potential better learning
        batch_size=64,  # Adjusted batch size
        validation_split=0.2,  # 20% of training data for validation
        shuffle=True,
        callbacks=[early_stopping, lr_reduction]
    )

    # Save the trained model
    model.save(MODEL_PATH)

# Evaluate on test data
loss, accuracy = model.evaluate(test_data, test_labels)
print(f"Test accuracy: {accuracy * 100:.2f}%")

# Updated encode_text function
def encode_text(text):
    return vectorizer(tf.convert_to_tensor([text]))

# Interactive loop for predictions
while True:
    user_input = input("Enter a sentence for sentiment analysis (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    encoded_input = encode_text(user_input)

    prediction = np.argmax(model.predict(encoded_input))
    print(prediction)

    if prediction == 0:
        print("Sentiment: Negative")
    elif prediction == 1:
        print("Sentiment: Neutral")
    else:
        print("Sentiment: Positive")
