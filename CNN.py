import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, MaxPooling1D, Flatten

# Load and preprocess your data from the CSV file
prop = pd.read_csv('Datasets/Final_Chennai.csv')

# Dropping unnecessary columns
prop.drop(columns=['Property_Name', 'Location', 'Availability'], inplace=True)

# Encode categorical columns
le = LabelEncoder()
for column in prop.select_dtypes(include='object').columns:
    prop[column] = le.fit_transform(prop[column])

# Splitting the data into input features and target variable
X = prop.drop('Price_Lakh', axis=1)
y = prop['Price_Lakh']

# Splitting the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)

# Reshape the input data
X_train = X_train.values.reshape(-1, X_train.shape[1], 1)
X_test = X_test.values.reshape(-1, X_test.shape[1], 1)

# Defining CNN model
model = Sequential()
model.add(Conv1D(128, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
model.add(MaxPooling1D(pool_size=2))
# model.add(Conv1D(128, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
# model.add(MaxPooling1D(pool_size=1))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1))  # Output layer

# Compile the model
model.compile(loss='mean_squared_error', optimizer='adam')


# Train the model
model.fit(X_train, y_train, batch_size=32, epochs=500, verbose=1)

# Evaluate the model
train_loss = model.evaluate(X_train, y_train)
test_loss = model.evaluate(X_test, y_test)

# Calculate and print the accuracy
y_train_pred = model.predict(X_train).squeeze()  # Fix the shape of the predicted values
y_test_pred = model.predict(X_test).squeeze()  # Fix the shape of the predicted values

train_accuracy = 1 - np.mean(np.abs(y_train_pred - y_train) / y_train)
test_accuracy = 1 - np.mean(np.abs(y_test_pred - y_test) / y_test)

print("Training Loss: ", train_loss)
print("Test Loss: ", test_loss)
print("Training Accuracy: ", train_accuracy)
print("Test Accuracy: ", test_accuracy)
