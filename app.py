import numpy as np
import pandas as pd
import pickle
import streamlit as st
import json
import math
import base64

result = None

with open(r"C:\Users\Hp\Downloads\bangalore_home_prices_model01.pickle", 'rb') as f:
    __model = pickle.load(f)

with open(r"C:\Users\Hp\Downloads\Columns01.json", 'r') as obj:
    __data_columns = json.load(obj)["Columns"]
    __area_types = __data_columns[6:10]
    __locations = __data_columns[10:]


def get_predicted_price(area_type, location, sqft, balcony, bathroom, BHK, park_faci, dist_mainroad):
    try:
        area_index = __data_columns.index(area_type.lower())
        loc_index = __data_columns.index(location.lower())
    except ValueError as e:
        area_index = -1
        loc_index = -1

    lis = np.zeros(len(__data_columns))
    lis[0] = sqft
    lis[1] = bathroom
    lis[2] = balcony
    lis[3] = BHK
    lis[4] = park_faci
    lis[5] = dist_mainroad

    if loc_index >= 0 and area_index >= 0:
        lis[area_index] = 1
        lis[loc_index] = 1

    price = round(__model.predict([lis])[0], 2)
    strp = ' lakhs'

    if math.log10(price) >= 2:
        price = price / 100
        price = round(price, 2)
        strp = " crores"

    return str(price) + strp


def main():
    global result
    st.title("Bangalore House Price Predictor")
    html_temp = """
           <div>
           <h2>Enter your details</h2>
           </div>
           """
    st.markdown(html_temp, unsafe_allow_html=True)
    total_sqft = st.text_input("Total_sqft")
    balcony = st.text_input("Number of Balconies")
    bathroom = st.text_input("Number of Bathrooms")
    BHK = st.text_input("BHK")
    park_faci = st.text_input("Parking Facility (enter 1 for yes and 0 for no)")
    dist_mainroad = st.text_input("Distance from mainroad")
    area_type = st.selectbox("Area Type", __area_types)
    location = st.selectbox("Location", __locations)

    if st.button("Predict"):
        result = get_predicted_price(area_type, location, total_sqft, balcony, bathroom, BHK, park_faci, dist_mainroad)

    st.success(f"Price = {result}")


if __name__ == "__main__":
    main()