import streamlit as st
import pandas as pd

st.set_page_config(
    page_title = 'Multipage',
    page_icon = '?',
    layout = 'wide',
    )

st.sidebar.success('Select a page above')

ratings = {'CPF': [], 'Cash': [], 'Price_Range': [], 'Size_Range': [], 'Costsqm_Range': [], 'Investment_Range': [], 'Floor_Range': [], 'Lease_Range': [], 
           'Age_Range': [], 'Income_Range': [], 'Park_Range': [], 'Mall_Range': [], 'Prisch_Range': [], 'MRT_Range': [], 'Bus_Range': [], 'Price_Rating': [], 
           'Size_Rating': [], 'Costsqm_Rating': [], 'Investment_Rating': [], 'Floor_Rating': [], 'Lease_Rating': [], 'Age_Rating': [], 'Income_Rating': [], 
           'Park_Rating': [], 'Mall_Rating': [], 'Prisch_Rating': [], 'MRT_Rating': [], 'Bus_Rating': []}

######################################################## User Input Form ########################################################
st.title('Singapore Property Purchase Planner')

# HDB Budget Calculator
st.header('1) Please answer these questions to calculate your budget')

grant_dict = {'Single':['Single_40000', 'Single_50000'],  
              'Citizens': ['Family_40000', 'Family_50000'], 
              'PR': ['Family_30000', 'Family_40000'], 
              'Foreigner': ['Family_20000', 'Family_25000'], 
              'Nil' : ['Nil']}


user_age = st.number_input('Age', min_value = 0, value = None)

cpf = st.number_input('CPF Savings', min_value = 0.00, value = None)

cash = st.number_input('Cash Savings', min_value = 0.00, value = None)

grant_rooms = st.selectbox('What type of HDB do you intend to buy?', ('2-Room', '3-Room', '4-Room', '5-Room or larger'), 
                           key = 'rooms', index=None, placeholder="Please Select a Value")

grant_citizen = st.selectbox('Are you a Singapore Citizen or applying with a Singapore Citizen?', ('Yes', 'No'), 
                           key = 'citizen', index=None, placeholder="Please Select a Value")

if grant_citizen == 'Yes':
    grant_first = st.selectbox('Are you a first-time applicant or applying with a first-time applicant?', ('Yes', 'No'), 
                           key = 'first', index=None, placeholder="Please Select a Value")
    if grant_first == 'Yes':
        grant_single = st.selectbox('Are you applying as a couple or as an individual?', ('Couple', 'Individual'), 
                           key = 'single', index=None, placeholder="Please Select a Value")
        if grant_single == 'Individual':
            if user_age >= 35:
                if grant_rooms == '5-Room or larger':
                    grant_indicator = 'Single_25000'
                else:
                    grant_indicator = 'Single_20000'
            else:
                grant_indicator = 'Nil'
        elif grant_single == 'Couple':
            user_citizen = st.selectbox('What is your citizenship?', ('Singapore Citizen', 'PR', 'Foreigner'), 
                           key = 'citizen1', index=None, placeholder="Please Select a Value")
            partner_citizen = st.selectbox("What is your partner's citizenship?", ('Singapore Citizen', 'PR', 'Foreigner'), 
                           key = 'citizen2', index=None, placeholder="Please Select a Value")
            if user_citizen == 'Singapore Citizen' and partner_citizen == 'Singapore Citizen':
                if grant_rooms == '5-Room or larger':
                    grant_indicator = 'Family_40000'
                else:
                    grant_indicator = 'Family_50000'
            elif (user_citizen == 'Singapore Citizen' and partner_citizen == 'PR') or (user_citizen == 'PR' and partner_citizen == 'Singapore Citizen'):
                if grant_rooms == '5-Room or larger':
                    grant_indicator = 'Family_30000'
                else:
                    grant_indicator = 'Family_40000'
            elif (user_citizen == 'Singapore Citizen' and partner_citizen == 'Foreigner') or (user_citizen == 'Foreigner' and partner_citizen == 'Singapore Citizen'):
                if grant_rooms == '5-Room or larger':
                    grant_indicator = 'Family_25000'
                else:
                    grant_indicator = 'Family_20000'
            elif user_citizen in ['PR', 'Foreigner'] and partner_citizen in ['PR', 'Foreigner']:
                st.error('One person needs to be a Citizen', icon="🚨")
    elif grant_first == 'No':
        grant_indicator = 'Nil'
elif grant_citizen == 'No':
    grant_indicator = 'Nil'


# User inputs for filtering
st.header('2) Please answer these questions indicating your preferences for your HDB Flat')

# Price
st.subheader('a. Price')
price_range = st.selectbox('Please select your price range', ('0 to 400 Thousand', '400 Thousand to 1 Million', 'More than 1 Million'), 
                           key = 'price', index=None, placeholder="Please Select a Value")
price_rating = st.selectbox('I am willing to pay whatever it takes to obtain the best possible flat. (1 - Not Willing, 10 - Willing)', 
                            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'price1', index=None, placeholder="Please Select a Rating")
st.write('')

# Size
st.subheader('b. Size')
size_range = st.selectbox('Please select your preferred size (sqm)', ('0 to 60 sqm', '60 sqm to 90 sqm', 'More than 90 sqm'), 
                           key = 'size', index=None, placeholder="Please Select a Value")
size_rating = st.selectbox('I prefer to live in a big HDB flat. (1 - Smallest, 10 - Biggest)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'size1', index=None, placeholder="Please Select a Rating")
st.write('')

# Cost per sqm
st.subheader('c. Cost per sqm')
costsqm_range = st.selectbox('Please select your preferred cost per sqm', ('0 to 60 sqm', '60 sqm to 90 sqm', 'More than 90 sqm'), 
                           key = 'costsqm', index=None, placeholder="Please Select a Value")
costsqm_rating = st.selectbox('I prefer the price of HDB flats to scale with its size. (1 - High price per sqm, 10 - Low price per sqm)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'costsqm1', index=None, placeholder="Please Select a Rating")
st.write('')

# Investment
st.subheader('d. Investment')
investment_range = st.selectbox('Please select your preferred investment', ('0 to 60 sqm', '60 sqm to 90 sqm', 'More than 90 sqm'), 
                           key = 'invest', index=None, placeholder="Please Select a Value")
investment_rating = st.selectbox('I view housing as an investment, and I expect high returns in the next 5 years. (1 - Investment does not matter, 10 - Investment matters)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'invest1', index=None, placeholder="Please Select a Rating")
st.write('')

# Floor
st.subheader('e. Floor')
floor_range = st.selectbox('Please select your preferred floor level', ('Low', 'Mid', 'High'), 
                           key = 'floor', index=None, placeholder="Please Select a Value")
floor_rating = st.selectbox('I prefer living on higher floors as opposed to lower floors. (1 - Lowest Floor, 10 - Highest Floor)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'floor1', index=None, placeholder="Please Select a Rating")
st.write('')

# Lease
st.subheader('f. Lease')
lease_range = st.selectbox('Please select your preferred amount of remaining lease', ('0 to 50 Years Left', '50 to 80 Years Left', 'More than 80 Years Left'), 
                           key = 'lease', index=None, placeholder="Please Select a Value")
lease_rating = st.selectbox('The amount of lease left on the HDB flat matters to me. (1 - Lowest Lease Remaining, 10 - Highest Lease Remaining)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'lease1', index=None, placeholder="Please Select a Rating")
st.write('')

# Age
st.subheader('g. Population of Residents')
age_range = st.selectbox('Please select the average age range of the residents residing in the HDB flat', ('Young', 'Mid-Age', 'Elderly'), 
                           key = 'age', index=None, placeholder="Please Select a Value")
age_rating = st.selectbox('I prefer to live in HDB flats with a younger population. (1 - Age Does Not Matter, 10 - Age Matters)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'age1', index=None, placeholder="Please Select a Rating")
st.write('')

# Income
st.subheader('h. Household Income of Residents')
income_range = st.selectbox('Please select the average income level of the residents residing in the HDB flat', ('Low', 'Mid', 'High'), 
                           key = 'income', index=None, placeholder="Please Select a Value")
income_rating = st.selectbox('I prefer to live in HDB flats with a high household income. (1 - Income Does Not Matter, 10 - Income Matters)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'income1', index=None, placeholder="Please Select a Rating")
st.write('')

# Park
st.subheader('i. Proximity to Parks')
park_range = st.selectbox('Please select your preferred proximity to parks', ('Walking Distance', 'A Station Over', 'Does Not Matter'), 
                           key = 'park', index=None, placeholder="Please Select a Value")
park_rating = st.selectbox('Proximity to parks is important to me. (1 - Far, 10 - Close By)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'park1', index=None, placeholder="Please Select a Rating")
st.write('')

# Mall
st.subheader('j. Proximity to Malls')
mall_range = st.selectbox('Please select your preferred proximity to malls', ('Walking Distance', 'A Station Over', 'Does Not Matter'), 
                           key = 'mall', index=None, placeholder="Please Select a Value")
mall_rating = st.selectbox('Proximity to malls is important to me. (1 - Far, 10 - Close By)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'mall1', index=None, placeholder="Please Select a Rating")
st.write('')

# Pri Sch
st.subheader('k. Proximity to Primary Schools')
prisch_range = st.selectbox('Please select your preferred proximity to primary schools', ('Walking Distance', 'A Station Over', 'Does Not Matter'), 
                           key = 'prisch', index=None, placeholder="Please Select a Value")
prisch_rating = st.selectbox('Proximity to primary schools is important to me. (1 - Far, 10 - Close By)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'prisch1', index=None, placeholder="Please Select a Rating")
st.write('')

# MRT
st.subheader('l. Proximity to an MRT Station')
mrt_range = st.selectbox('Please select your preferred proximity to an MRT station', ('Walking Distance', 'A Station Over', 'Does Not Matter'), 
                           key = 'mrt', index=None, placeholder="Please Select a Value")
mrt_rating = st.selectbox('Proximity to an MRT station is important to me. (1 - Far, 10 - Close By)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'mrt1', index=None, placeholder="Please Select a Rating")
st.write('')

# Bus
st.subheader('m. Proximity to a Bus Station')
bus_range = st.selectbox('Please select your preferred proximity to a bus station', ('Walking Distance', 'A Station Over', 'Does Not Matter'), 
                           key = 'bus', index=None, placeholder="Please Select a Value")
bus_rating = st.selectbox('Proximity to a bus interchange is important to me. (1 - Far, 10 - Close By)', 
                           (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'bus1', index=None, placeholder="Please Select a Rating")
st.write('')

variables = [cpf, cash, 
             price_range, size_range, costsqm_range, investment_range, floor_range, lease_range, age_range, 
             price_rating, size_rating, costsqm_rating, investment_rating, floor_rating, lease_rating, age_rating, 
             income_range, park_range, mall_range, prisch_range, mrt_range, bus_range, 
             income_rating, park_rating, mall_rating, prisch_rating, mrt_rating, bus_rating]
submit = 0

if st.button('Submit'):
    for i in variables:
        if i == None:
            st.error('Please complete all required fields', icon="🚨")
            break
        else:
            submit = 1
    
    if submit == 1:
        ratings['CPF'].append(cpf)
        ratings['Cash'].append(cash)

        ratings['Price_Range'].append(price_range)
        ratings['Size_Range'].append(size_range)
        ratings['Costsqm_Range'].append(costsqm_range)
        ratings['Investment_Range'].append(investment_range)
        ratings['Floor_Range'].append(floor_range)
        ratings['Lease_Range'].append(lease_range)
        ratings['Age_Range'].append(age_range)
        ratings['Income_Range'].append(income_range)
        ratings['Park_Range'].append(park_range)
        ratings['Mall_Range'].append(mall_range)
        ratings['Prisch_Range'].append(prisch_range)
        ratings['MRT_Range'].append(mrt_range)
        ratings['Bus_Range'].append(bus_range)

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
        # st.write(ratings) # For printing table (Remove for launch)
        ratings.to_csv('ratings.csv')