# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sUoTNaTowBqYIGVLrZobsqXnzoV0_4l9
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("project1.csv")

df.head(20)

df = df.drop('id', axis=1)

df.head(10)

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
Time=le.fit_transform(df['time'])
AreaType=le.fit_transform(df['areatype'])

df['time']=Time
df['areatype']=AreaType

df.head(4)

df.head(18)

from sklearn import linear_model

x=df[['time','aqi','areatype','hours']]
y=df['price']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 100)

regr = linear_model.LinearRegression()
regr.fit(x, y)

print(regr.predict([[2,250,0,1]]))


color={
    "delhi":2,
    "mumbai":1,
    "New York":2

}

from flask import Flask,jsonify,request
import requests

app=Flask(__name__)

received_arrays=[]

#@app.route('/api/prd')
@app.route('/api/prd', methods=['POST'])
def process_array():
    try:
        # Get the JSON data from the request body
        request_data = request.json

        

        base_url = "https://api.waqi.info"
        token = "ee0c40c8c70b6b75820180c6f60d1571c76ee0c5"

        city = request_data.get("city")
        price = int(request_data.get("price"))
        if price is None or city is None:
            return jsonify({"error": "Both 'price' and 'city' are required fields."}), 400
        color_code=int(color.get(city))
        r = requests.get(base_url + f"/feed/{city}/?token={token}")

        ans="City: {}, Air quality index: {}".format(r.json()['data']['city']['name'], r.json()['data']['aqi'])
        parts = ans.split(':')

# Extract the AQI part and remove leading/trailing spaces
        aqi_part = parts[-1].strip()

# Convert the AQI to an integer
        aqi = int(aqi_part)
        arr=[1,aqi,color_code,price]
        # Check if the request data is a list (array)
        if isinstance(arr, list):
            #python_list = request_data.tolist()
            #json_data = json.dumps(python_list)
            # Process the array data as needed
            result = regr.predict([arr])
            ans={
                "ans": result[0]
            }
            return ans
        else:
            return jsonify({'error': 'Input must be a JSON array'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)