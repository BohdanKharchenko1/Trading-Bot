import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Load the test data
test_data = pd.read_csv('test.csv')

# Confirm that the data has been loaded correctly
print(test_data.head())


scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit(test_data[['open', 'high', 'low', 'close', 'volume', 'turnover', 'SMA_5',
                      'SMA_10']])

if len(test_data) < 40:
    raise ValueError("Not enough data to create input sequence for prediction.")

last_intervals = test_data.tail(40)
scaled_last_intervals = scaler.transform(
    last_intervals[['open', 'high', 'low', 'close', 'volume', 'turnover', 'SMA_5', 'SMA_10']])

X_pred = scaled_last_intervals.reshape((1, 40, scaled_last_intervals.shape[1]))

model = load_model('my_model.h5')  # Make sure you provide the correct path

predicted_price_scaled = model.predict(X_pred)


dummy = np.zeros((1, scaled_last_intervals.shape[1]))
dummy[0, 3] = predicted_price_scaled

predicted_price = scaler.inverse_transform(dummy)[0, 3]

print("Predicted next 'close' price:", predicted_price)
