import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def make_prediction(userLikePriceDay,userLikePlaces):
    data = pd.read_csv("hotel.csv")

    plt.scatter(data.userLikePriceDay,data.mivNumber,color = "red")
    plt.xlabel("User Liked Price Day")
    plt.ylabel("MIV Number")

    x = np.array(data.userLikePriceDay.values)
    x

    y = np.array(data.mivNumber.values)
    y

    model = LinearRegression()
    model.fit(data[["userLikePriceDay","userLikePlaces"]],data.mivNumber) #training the model

    predicted_value = model.predict([[userLikePriceDay,userLikePlaces]])
    return predicted_value