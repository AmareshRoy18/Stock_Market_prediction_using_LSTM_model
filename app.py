import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
import math
from keras.models import load_model
import streamlit as st

st.title('Stock Price Prediction')

user_input = st.text_input('Enter Stock Ticker', 'SBIN.NS')

import yfinance as yf
df = yf.download( user_input, start = '2015-01-01', end='2023-05-01')
df.head()

#Describing the data
st.subheader('Data from 2015-2023')
st.write(df.describe())

#Visualization
st.subheader('Closing Price vs Time chart')
fig = plt.figure(figsize =(12,6))
plt.title('Close Price History')
plt.plot(df['Close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price', fontsize=18)
st.pyplot(fig)


st.subheader('100days and 200days moving averages')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize =(12,6))
plt.title('Close Price History')
plt.plot(df.Close)
plt.plot(ma100, 'r')
plt.plot(ma200, 'y')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price', fontsize=18)
plt.legend(['Values', '100 day ma ', '200 days ma'], loc = 'lower right')
st.pyplot(fig)

#Create a new dataframe with only close coloumn
data = df.filter(['Close'])

#Convert the Dataframe to a numpy array
dataset = data.values

#Splitting into training and testing set
train_data_len = math.ceil(len(dataset) * 0.8)
train_data_len

#Scale the Data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(np.array(dataset).reshape(-1,1))

#Create the training dataset and Scaled training dataset
train_data = scaled_data[0:train_data_len, :]
#Split the data into x_train and y_train data sets
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])
    if i<=60:
        print(x_train)
        print(y_train)
        print()


#Convert the x_train and y_train in numpy array
x_train, y_train = np.array(x_train),np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1],1))

#Loading the model
model = load_model('my_final_model.keras')

#Create the testing Dataset
#Create a new array containing scaled values from index
test_data = scaled_data[train_data_len - 60: , :]

#Create the dataset x_test and y_test
x_test = []
y_test = dataset[train_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])
    

#Convert the data into a numpy array
x_test = np.array(x_test)


#Reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

#Get the model predicted values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

#plot the data
train = data[:train_data_len]
valid = data[train_data_len:]
valid['Predictions'] = predictions

#Visulaze the data
st.subheader('Model Prediction')
fig2 = plt.figure(figsize=(12,6))
plt.title('Model')
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Close Price', fontsize = 18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc = 'lower right')
st.pyplot(fig2)