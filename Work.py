import streamlit as st
import pandas as pd

ratings = {'Price_Rating': [], 'Size_Rating': [], 'Costsqm_Rating': [], 'Investment_Rating': [], 'Floor_Rating': [], 'Lease_Rating': [], 'Age_Rating': []
           , 'Income_Rating': [], 'Park_Rating': [], 'Mall_Rating': [], 'Prisch_Rating': [], 'MRT_Rating': [], 'Bus_Rating': []}

# User Input Form
st.title('Singapore Property Purchase Planner')
st.subheader('Please answer these questions indicating your preferences for your HDB Flat')

price_rating = st.selectbox('I am willing to pay whatever it takes to obtain the best possible flat. (1 - Not Willing, 10 - Willing)', 
                            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'price', index=None, placeholder="Select Rating")

size_rating = st.selectbox('I prefer to live in a big HDB flat. (1 - Smallest, 10 - Biggest)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'size', index=None, placeholder="Select Rating")

costsqm_rating = st.selectbox('I prefer the price of HDB flats to scale with its size. (1 - High price per sqm, 10 - Low price per sqm)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'costsqm', index=None, placeholder="Select Rating")

investment_rating = st.selectbox('I view housing as an investment, and I expect high returns in the next 5 years. (1 - Investment does not matter, 10 - Investment matters)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'invest', index=None, placeholder="Select Rating")

floor_rating = st.selectbox('I prefer living on higher floors as opposed to lower floors. (1 - Lowest Floor, 10 - Highest Floor)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'floor', index=None, placeholder="Select Rating")

lease_rating = st.selectbox('The amount of lease left on the HDB flat matters to me. (1 - Lowest Lease Remaining, 10 - Highest Lease Remaining)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'lease', index=None, placeholder="Select Rating")

age_rating = st.selectbox('I prefer to live in HDB flats with a younger population. (1 - Age Does Not Matter, 10 - Age Matters)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'age', index=None, placeholder="Select Rating")

income_rating = st.selectbox('I prefer to live in HDB flats with a high household income. (1 - Income Does Not Matter, 10 - Income Matters)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'income', index=None, placeholder="Select Rating")

park_rating = st.selectbox('Proximity to parks is important to me. (1 - Far, 10 - Close By)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'park', index=None, placeholder="Select Rating")

mall_rating = st.selectbox('Proximity to malls is important to me. (1 - Far, 10 - Close By)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'mall', index=None, placeholder="Select Rating")

prisch_rating = st.selectbox('Proximity to primary schools is important to me. (1 - Far, 10 - Close By)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'prisch', index=None, placeholder="Select Rating")

mrt_rating = st.selectbox('Proximity to an MRT station is important to me. (1 - Far, 10 - Close By)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'mrt', index=None, placeholder="Select Rating")

bus_rating = st.selectbox('Proximity to a bus interchange is important to me. (1 - Far, 10 - Close By)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'bus', index=None, placeholder="Select Rating")

if st.button('Submit'):
    ratings['Price_Rating'].append(price_rating)
    ratings['Size_Rating'].append(size_rating)
    ratings['Costsqm_Rating'].append(costsqm_rating)
    ratings['Investment_Rating'].append(investment_rating)
    ratings['Floor_Rating'].append(floor_rating)
    ratings['Lease_Rating'].append(lease_rating)
    ratings['Age_Rating'].append(age_rating)
    ratings['Income_Rating'].append(income_rating)
    ratings['Park_Rating'].append(park_rating)
    ratings['Mall_Rating'].append(mall_rating)
    ratings['Prisch_Rating'].append(prisch_rating)
    ratings['MRT_Rating'].append(mrt_rating)
    ratings['Bus_Rating'].append(bus_rating)
    ratings = pd.DataFrame(ratings)

    st.write(ratings)