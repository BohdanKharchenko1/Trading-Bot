import numpy as np
import pandas as pd
from keras.layers import Dense, LSTM, Bidirectional
from keras.metrics import RootMeanSquaredError
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv('new_BTCSDT_1h_data_since_2020.csv')

data.drop(columns=data.columns[0], axis=1, inplace=True)


scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(
    data[['open', 'high', 'low', 'close', 'volume', 'turnover', 'SMA_5', 'SMA_10']].values)

look_back = 40
features_set, labels = [], []
for i in range(look_back, len(scaled_data)):
    features_set.append(scaled_data[i - look_back:i, :])
    labels.append(scaled_data[i, 3])
features_set, labels = np.array(features_set), np.array(labels)
features_set = np.reshape(features_set, (features_set.shape[0], look_back, -1))

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(features_set, labels, test_size=0.2, random_state=42)

# Building the model
model = Sequential([
    Bidirectional(LSTM(units=50, return_sequences=True), input_shape=(look_back, scaled_data.shape[1])),
    Bidirectional(LSTM(units=50)),
    Dense(units=1)
])
model.compile(optimizer='adam', loss='mean_squared_error', metrics=[RootMeanSquaredError()])

# Training
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

# Saving the model
model.save('my_model1.h5')

# Predictions and metrics
predictions = model.predict(X_test)
predictions_reshaped = np.zeros((len(predictions), scaled_data.shape[1]))
predictions_reshaped[:, 3] = predictions.flatten()
predictions_inversed = scaler.inverse_transform(predictions_reshaped)[:, 3]

actual_close_prices = data['close'].iloc[-len(predictions):].values

print(actual_close_prices)
