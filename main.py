import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
import pandas as pd

# Function to preprocess data
def preprocess_data(df, sequence_length):
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[['Open']])

    X, y = [], []
    for i in range(len(df_scaled) - sequence_length):
        X.append(df_scaled[i:i + sequence_length])
        y.append(df_scaled[i + sequence_length])
    X, y = np.array(X), np.array(y)

    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    return scaler, X_train, X_test, y_train, y_test

# Function to train LSTM model
# def train_lstm_model(X_train, y_train):
#     model = Sequential()
#     model.add(LSTM(50, activation='sigmoid', return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
#     model.add(LSTM(50, activation='sigmoid'))
#     model.add(Dense(1))
#     model.compile(optimizer=Adam(learning_rate=0.001), loss=MeanSquaredError())
#     model.fit(X_train, y_train, epochs=150, batch_size=32, verbose=2)
#     return model

# Function to save model to HDF5 file
def save_model_to_h5(model, filename):
    model.save(filename)

# Function to load model from HDF5 file
def load_model_from_h5(filename):
    return load_model(filename)

# Sample usage
if __name__ == "__main__":
    # Example usage
    sequence_length = 10  # Example sequence length
    
    model = load_model('trained_model.keras')
    df = pd.read_csv('NABIL.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df = df.dropna()

    scaler, X_train, _, y_train, _ = preprocess_data(df, sequence_length)
    model = train_lstm_model(X_train, y_train)
    
    # predict tomorrow's price
    latest_data = df.tail(sequence_length)
    latest_scaled = scaler.transform(latest_data[['Open']])
    latest_scaled = np.array(latest_scaled).reshape((1, sequence_length, 1))
    tomorrow_prediction = model.predict(latest_scaled)
    tomorrow_prediction = scaler.inverse_transform(tomorrow_prediction)
    print(tomorrow_prediction[0][0])

    