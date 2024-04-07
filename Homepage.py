import streamlit as st
import pandas as pd

st.set_page_config(
    page_title = 'Singapore Property Purchase Planner',
    page_icon = '?',
    layout = 'wide',
    )

if "script_runs" not in st.session_state:
    st.session_state.fragment_runs = 0

ratings = {'CPF': [], 'Cash': [], 'Grant_Indicator': [], 'Grant_Amount': [], 
            'Price_Range': [], 'Size_Range': [], 'Costsqm_Range': [], 'Investment_Range': [], 
            'Floor_Range': [], 'Lease_Range': [], 'Age_Range': [], 'Income_Range': [], 
            'Park_Range': [], 'Mall_Range': [], 'Prisch_Range': [], 'MRT_Range': [], 
            'Bus_Range': [], 
            'Price_Rating': [], 'Size_Rating': [], 'Costsqm_Rating': [], 'Investment_Rating': [], 
            'Floor_Rating': [], 'Lease_Rating': [], 'Age_Rating': [], 'Income_Rating': [], 
            'Park_Rating': [], 'Mall_Rating': [], 'Prisch_Rating': [], 'MRT_Rating': [], 
            'Bus_Rating': [], 
            'Park_Proximity': [], 'Mall_Proximity': [], 'Primary_School_Proximity': [], 
            'MRT_Proximity': [], 'Bus_Proximity': []}

@st.experimental_fragment
def fragment():
    # submit  = 0
    global ratings

    if st.session_state.fragment_runs == 0:
        ######################################################## User Input Form ########################################################
        st.title('Singapore Property Purchase Planner')

        # HDB Budget Calculator
        st.header('1) Please answer these questions to calculate your budget')

        grant_indicator = ''


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
                            grant_indicator = 'Singles'
                            grant_amount = 25000
                        else:
                            grant_indicator = 'Singles'
                            grant_amount = 20000
                    else:
                        grant_indicator = 'Nil'
                elif grant_single == 'Couple':
                    user_citizen = st.selectbox('What is your citizenship?', ('Singapore Citizen', 'PR', 'Foreigner'), 
                                key = 'citizen1', index=None, placeholder="Please Select a Value")
                    partner_citizen = st.selectbox("What is your partner's citizenship?", ('Singapore Citizen', 'PR', 'Foreigner'), 
                                key = 'citizen2', index=None, placeholder="Please Select a Value")
                    if user_citizen == 'Singapore Citizen' and partner_citizen == 'Singapore Citizen':
                        if grant_rooms == '5-Room or larger':
                            grant_indicator = 'Family'
                            grant_amount = 40000
                        else:
                            grant_indicator = 'Family'
                            grant_amount = 50000
                    elif (user_citizen == 'Singapore Citizen' and partner_citizen == 'PR') or (user_citizen == 'PR' and partner_citizen == 'Singapore Citizen'):
                        if grant_rooms == '5-Room or larger':
                            grant_indicator = 'Family'
                            grant_amount = 30000
                        else:
                            grant_indicator = 'Family'
                            grant_amount = 40000
                    elif (user_citizen == 'Singapore Citizen' and partner_citizen == 'Foreigner') or (user_citizen == 'Foreigner' and partner_citizen == 'Singapore Citizen'):
                        if grant_rooms == '5-Room or larger':
                            grant_indicator = 'Family'
                            grant_amount = 25000
                        else:
                            grant_indicator = 'Family'
                            grant_amount = 20000
                    elif user_citizen in ['PR', 'Foreigner'] and partner_citizen in ['PR', 'Foreigner']:
                        st.error('One person needs to be a Citizen', icon="🚨")
            elif grant_first == 'No':
                grant_indicator = 'Nil'
        elif grant_citizen == 'No':
            grant_indicator = 'Nil'

        if grant_indicator in ['Singles', 'Family']:
            loan = (cash+cpf)*4
            budget = (cash+cpf)*5 + grant_amount
            st.header('You are eligible to purchase a resale HDB with the following budget')
            st.write(':one: Eligible for a {0} grant of ${1}'.format(grant_indicator,grant_amount))
            st.write(':two: Eligible for a loan amount of ${0}'.format(int(loan)))
            st.write(':three: Total cash and cpf proceeds of ${0}'.format(int(cash+cpf)))
            st.subheader(':arrow_right: Your max HDB budget is ${0}'.format(int(budget)))

            ratings['CPF'].append(cpf)
            ratings['Cash'].append(cash)
            ratings['Grant_Indicator'].append(grant_indicator)
            ratings['Grant_Amount'].append(grant_amount)

            st.session_state.fragment_runs += 1
            st.button("Next")
        elif grant_indicator == 'Nil':
            st.header(':neutral_face: You are not eligible to purchase a resale HDB')


    # elif st.session_state.fragment_runs == 1:
    #     # User inputs for filtering
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')

    #     # Price
    #     st.subheader('a. Price')
    #     price_range = st.selectbox('Please select your price range', ('0 to 400 Thousand', '400 Thousand to 1 Million', 'More than 1 Million'), 
    #                             key = 'price', index=None, placeholder="Please Select a Value")
    #     price_rating = st.selectbox('I am willing to pay whatever it takes to obtain the best possible flat. (1 - Not Willing, 10 - Willing)', 
    #                                 (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'price1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 1/13')

    #     if price_range != None and price_rating != None:
    #         ratings['Price_Range'].append(price_range)
    #         ratings['Price_Rating'].append(price_rating)

    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 2:
    #     # Size
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('b. Size')
    #     size_range = st.selectbox('Please select your preferred size (sqm)', ('0 to 60 sqm', '60 sqm to 90 sqm', 'More than 90 sqm'), 
    #                             key = 'size', index=None, placeholder="Please Select a Value")
    #     size_rating = st.selectbox('I prefer to live in a big HDB flat. (1 - Smallest, 10 - Biggest)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'size1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 2/13')

    #     if size_range != None and size_rating != None:
    #         ratings['Size_Range'].append(size_range)
    #         ratings['Size_Rating'].append(size_rating)

    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 3:

    #     # Cost per sqm
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('c. Cost per sqm')
    #     costsqm_range = st.selectbox('Please select your preferred cost per sqm', ('0 to 60 sqm', '60 sqm to 90 sqm', 'More than 90 sqm'), 
    #                             key = 'costsqm', index=None, placeholder="Please Select a Value")
    #     costsqm_rating = st.selectbox('I prefer the price of HDB flats to scale with its size. (1 - High price per sqm, 10 - Low price per sqm)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'costsqm1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 3/13')

    #     if costsqm_range != None and costsqm_rating != None:
    #         ratings['Costsqm_Range'].append(costsqm_range)
    #         ratings['Costsqm_Rating'].append(costsqm_rating)

    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 4:

    #     # Investment
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('d. Investment')
    #     investment_range = st.selectbox('Please select your preferred investment', ('0 to 60 sqm', '60 sqm to 90 sqm', 'More than 90 sqm'), 
    #                             key = 'invest', index=None, placeholder="Please Select a Value")
    #     investment_rating = st.selectbox('I view housing as an investment, and I expect high returns in the next 5 years. (1 - Investment does not matter, 10 - Investment matters)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'invest1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 4/13')

    #     if investment_range != None and investment_rating != None:  
    #         ratings['Investment_Range'].append(investment_range)
    #         ratings['Investment_Rating'].append(investment_rating)
  
    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 5:

    #     # Floor
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('e. Floor')
    #     floor_range = st.selectbox('Please select your preferred floor level', ('Low', 'Mid', 'High'), 
    #                             key = 'floor', index=None, placeholder="Please Select a Value")
    #     floor_rating = st.selectbox('I prefer living on higher floors as opposed to lower floors. (1 - Lowest Floor, 10 - Highest Floor)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'floor1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 5/13')

    #     if floor_range != None and floor_rating != None:
    #         ratings['Floor_Range'].append(floor_range)
    #         ratings['Floor_Rating'].append(floor_rating)
           
    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 6:

    #     # Lease
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('f. Lease')
    #     lease_range = st.selectbox('Please select your preferred amount of remaining lease', ('0 to 50 Years Left', '50 to 80 Years Left', 'More than 80 Years Left'), 
    #                             key = 'lease', index=None, placeholder="Please Select a Value")
    #     lease_rating = st.selectbox('The amount of lease left on the HDB flat matters to me. (1 - Lowest Lease Remaining, 10 - Highest Lease Remaining)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'lease1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 6/13')

    #     if lease_range != None and lease_rating != None:
    #         ratings['Lease_Range'].append(lease_range)
    #         ratings['Lease_Rating'].append(lease_rating)

    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 7:

    #     # Age
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('g. Population of Residents')
    #     age_range = st.selectbox('Please select the average age range of the residents residing in the HDB flat', ('Young', 'Mid-Age', 'Elderly'), 
    #                             key = 'age', index=None, placeholder="Please Select a Value")
    #     age_rating = st.selectbox('I prefer to live in HDB flats with a younger population. (1 - Age Does Not Matter, 10 - Age Matters)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'age1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 7/13')

    #     if age_range != None and age_rating != None:
    #         ratings['Age_Range'].append(age_range)
    #         ratings['Age_Rating'].append(age_rating)

    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 8:

    #     # Income
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('h. Household Income of Residents')
    #     income_range = st.selectbox('Please select the average income level of the residents residing in the HDB flat', ('Low', 'Mid', 'High'), 
    #                             key = 'income', index=None, placeholder="Please Select a Value")
    #     income_rating = st.selectbox('I prefer to live in HDB flats with a high household income. (1 - Income Does Not Matter, 10 - Income Matters)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'income1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 8/13')

    #     if income_range != None and income_rating != None:
    #         ratings['Income_Range'].append(income_range)
    #         ratings['Income_Rating'].append(income_rating)

    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 9:

    #     # Park
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('i. Proximity to Parks')
    #     park_range = st.selectbox('Please select your preferred proximity to parks', ('Walking Distance', 'A Station Over', 'Does Not Matter'), 
    #                             key = 'park', index=None, placeholder="Please Select a Value")
    #     park_rating = st.selectbox('Proximity to parks is important to me. (1 - Far, 10 - Close By)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'park1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 9/13')

    #     if park_range != None and park_rating != None:
    #         ratings['Park_Range'].append(park_range)
    #         ratings['Park_Rating'].append(park_rating)

    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 10:

    #     # Mall
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('j. Proximity to Malls')
    #     mall_range = st.selectbox('Please select your preferred proximity to malls', ('Walking Distance', 'A Station Over', 'Does Not Matter'), 
    #                             key = 'mall', index=None, placeholder="Please Select a Value")
    #     mall_rating = st.selectbox('Proximity to malls is important to me. (1 - Far, 10 - Close By)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'mall1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 10/13')

    #     if mall_range != None and mall_rating != None:
    #         ratings['Mall_Range'].append(mall_range)
    #         ratings['Mall_Rating'].append(mall_rating)

    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 11:

    #     # Pri Sch
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('k. Proximity to Primary Schools')
    #     prisch_range = st.selectbox('Please select your preferred proximity to primary schools', ('Walking Distance', 'A Station Over', 'Does Not Matter'), 
    #                             key = 'prisch', index=None, placeholder="Please Select a Value")
    #     prisch_rating = st.selectbox('Proximity to primary schools is important to me. (1 - Far, 10 - Close By)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'prisch1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 11/13')

    #     if prisch_range != None and prisch_rating != None:
    #         ratings['Prisch_Range'].append(prisch_range)
    #         ratings['Prisch_Rating'].append(prisch_rating)

    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 12:

    #     # MRT
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('l. Proximity to an MRT Station')
    #     mrt_range = st.selectbox('Please select your preferred proximity to an MRT station', ('Walking Distance', 'A Station Over', 'Does Not Matter'), 
    #                             key = 'mrt', index=None, placeholder="Please Select a Value")
    #     mrt_rating = st.selectbox('Proximity to an MRT station is important to me. (1 - Far, 10 - Close By)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'mrt1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 12/13')

    #     if mrt_range != None and mrt_rating != None:
    #         ratings['MRT_Range'].append(mrt_range)
    #         ratings['MRT_Rating'].append(mrt_rating)

    #         st.session_state.fragment_runs += 1
    #         st.button("Next")

    # elif st.session_state.fragment_runs == 13:

    #     # Bus
    #     st.header('2) Please answer these questions indicating your preferences for your HDB Flat')
    #     st.subheader('m. Proximity to a Bus Station')
    #     bus_range = st.selectbox('Please select your preferred proximity to a bus station', ('Walking Distance', 'A Station Over', 'Does Not Matter'), 
    #                             key = 'bus', index=None, placeholder="Please Select a Value")
    #     bus_rating = st.selectbox('Proximity to a bus interchange is important to me. (1 - Far, 10 - Close By)', 
    #                             (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), key = 'bus1', index=None, placeholder="Please Select a Rating")
    #     st.write('Progress: 13/13')

    #     if bus_range != None and bus_rating != None:
    #         ratings['Bus_Range'].append(bus_range)
    #         ratings['Bus_Rating'].append(bus_rating)

    #         st.session_state.fragment_runs += 1
    #         st.subheader('Thank you for submitting, please click the button below to proceed to your personalized HDB recommendation')
    #         st.button("My Personalized HDB Recommendation")




        # if st.button('Submit'):
            # ratings['CPF'].append(cpf)
            # ratings['Cash'].append(cash)
            # ratings['Grant_Indicator'].append(grant_indicator)
            # ratings['Grant_Amount'].append(grant_amount)

            # ratings['Price_Range'].append(price_range)
            # ratings['Size_Range'].append(size_range)
            # ratings['Costsqm_Range'].append(costsqm_range)
            # ratings['Investment_Range'].append(investment_range)
            # ratings['Floor_Range'].append(floor_range)
            # ratings['Lease_Range'].append(lease_range)
            # ratings['Age_Range'].append(age_range)
            # ratings['Income_Range'].append(income_range)
            # ratings['Park_Range'].append(park_range)
            # ratings['Mall_Range'].append(mall_range)
            # ratings['Prisch_Range'].append(prisch_range)
            # ratings['MRT_Range'].append(mrt_range)
            # ratings['Bus_Range'].append(bus_range)

            # ratings['Price_Rating'].append(price_rating)
            # ratings['Size_Rating'].append(size_rating)
            # ratings['Costsqm_Rating'].append(costsqm_rating)
            # ratings['Investment_Rating'].append(investment_rating)
            # ratings['Floor_Rating'].append(floor_rating)
            # ratings['Lease_Rating'].append(lease_rating)
            # ratings['Age_Rating'].append(age_rating)
            # ratings['Income_Rating'].append(income_rating)
            # ratings['Park_Rating'].append(park_rating)
            # ratings['Mall_Rating'].append(mall_rating)
            # ratings['Prisch_Rating'].append(prisch_rating)
            # ratings['MRT_Rating'].append(mrt_rating)
            # ratings['Bus_Rating'].append(bus_rating)

            # ratings = pd.DataFrame(ratings)
            # # st.write(ratings) # For printing table (Remove for launch)
            # ratings.to_csv('ratings.csv')

            # st.session_state.fragment_runs += 1
            # st.subheader('Thank you for submitting, please click the button below to proceed to your personalized HDB recommendation')
            # st.button("My Personalized HDB Recommendation")

    else:
        st.title('Your personalized HDB Recommendation')

        # ratings = pd.read_csv("ratings.csv")
        hdb = pd.read_csv("hdb.csv")
        del hdb['Unnamed: 0']


        ######################################################## Budget Calculator ########################################################
        if ratings['Grant_Indicator'][0] in ['Singles', 'Family']:
            loan = (ratings['Cash'][0]+ratings['CPF'][0])*4
            budget = (ratings['Cash'][0]+ratings['CPF'][0])*5 + ratings['Grant_Amount'][0]
            st.header('You are eligible to purchase a resale HDB with the following budget')
            st.write(':one: Eligible for a {0} grant of ${1}'.format(ratings['Grant_Indicator'][0],ratings['Grant_Amount'][0]))
            st.write(':two: Eligible for a loan amount of ${0}'.format(int(loan)))
            st.write(':three: Total cash and cpf proceeds of ${0}'.format(int(ratings['Cash'][0]+ratings['CPF'][0])))
            st.subheader(':arrow_right: Your max HDB budget is ${0}'.format(int(budget)))
        else:
            st.subheader('Your Estimated Budget for your HDB is $0.')


        ######################################################## Visualization ########################################################
        # Prepping main table
        hdb['score'] = ((hdb['predicted_price_normalized']*ratings['Price_Rating'][0]) + (hdb['price_per_sqm_normalized']*ratings['Costsqm_Rating'][0]) + 
                        (hdb['projected_5_years_normalized']*ratings['Investment_Rating'][0]) + (hdb['storey_range_normalized']*ratings['Floor_Rating'][0]) + 
                        (hdb['remaining_mths_lease_normalized']*ratings['Lease_Rating'][0]) + (hdb['avg_age_by_pa_normalized']*ratings['Age_Rating'][0]) + 
                        (hdb['median_hhi_by_pa_normalized']*ratings['Income_Rating'][0]) + (hdb['dist_hdb_to_park_normalized']*ratings['Park_Rating'][0]) + 
                        (hdb['dist_hdb_to_mall_normalized']*ratings['Mall_Rating'][0]) + (hdb['dist_hdb_to_prisch_normalized']*ratings['Prisch_Rating'][0]) + 
                        (hdb['dist_hdb_to_mrt_normalized']*ratings['MRT_Rating'][0]) + (hdb['dist_hdb_to_bus_normalized']*ratings['Bus_Rating'][0]))

        hdb = hdb[['town', 'flat_type', 'block', 'street_name', 'flat_model', 'resale_price', 'floor_area_sqm', 'price_per_sqm', 'storey_range', 'remaining_mths_left_asof_2024', 'avg_age_by_pa', 'median_hhi_by_pa', 'dist_hdb_to_park', 'dist_hdb_to_mall', 'dist_hdb_to_prisch', 'dist_hdb_to_mrt', 'dist_hdb_to_bus', 'lat', 'lon', 'score']]
        # st.write(hdb.head(5))
        # def prox(x):
        #     if x <= 500:
        #         return 'Walking Distance'
        #     elif x <= 1000:
        #         return 'A Station Over'
        #     else:
        #         return 'Does Not Matter'

        # hdb['Park_Proximity'] = hdb.dist_hdb_to_park.apply(prox)
        # hdb['Mall_Proximity'] = hdb.dist_hdb_to_mall.apply(prox)
        # hdb['Primary_School_Proximity'] = hdb.dist_hdb_to_prisch.apply(prox)
        # hdb['MRT_Proximity'] = hdb.dist_hdb_to_mrt.apply(prox)
        # hdb['Bus_Proximity'] = hdb.dist_hdb_to_bus.apply(prox)

        def prox(x):
            if x == 'Walking Distance':
                return 500
            elif x == 'A Station Over':
                return 1000
            else:
                return 100000
        ram = prox(ratings['Park_Range'[0]])
        st.write(ram)
        # ratings['Park_Proximity'] = ratings.Park_Range.apply(prox)
        # ratings['Mall_Proximity'] = ratings.Mall_Range.apply(prox)
        # ratings['Primary_School_Proximity'] = ratings.Prisch_Range.apply(prox)
        # ratings['MRT_Proximity'] = ratings.MRT_Range.apply(prox)
        # ratings['Bus_Proximity'] = ratings.Bus_Range.apply(prox)
        ratings['Park_Proximity'].append(prox(ratings['Park_Range'[0]]))
        ratings['Mall_Proximity'].append(prox(ratings['Mall_Range'[0]]))
        ratings['Primary_School_Proximity'].append(prox(ratings['Prisch_Range'[0]]))
        ratings['MRT_Proximity'].append(prox(ratings['MRT_Range'[0]]))
        ratings['Bus_Proximity'].append(prox(ratings['Bus_Range'[0]]))
        # st.write(hdb.head(20)) # For printing table (Remove for launch)
        # st.write(ratings.head()) # For printing table (Remove for launch)

        # Filtering main table based on user input
        hdb2 = hdb[(hdb['dist_hdb_to_park'] <= ratings['Park_Proximity'][0]) 
                & (hdb['dist_hdb_to_mall'] <= ratings['Mall_Proximity'][0]) 
                & (hdb['dist_hdb_to_prisch'] <= ratings['Primary_School_Proximity'][0]) 
                & (hdb['dist_hdb_to_mrt'] <= ratings['MRT_Proximity'][0]) 
                & (hdb['dist_hdb_to_bus'] <= ratings['Bus_Proximity'][0])]

        # st.write(hdb2.head(10)) # For printing table (Remove for launch)

        # Dynamic filtering for user
        # ram_filter = st.checkbox('Select Town', options=list(hdb2['town'].unique()), default=list(hdb2['town'].unique()))
        # with st.expander("Choose columns"):
        #     town_filter = st.multiselect('Select Town', options=list(hdb2['town'].unique()), default=None)

        town_filter = st.multiselect('Select Town', options=list(hdb2['town'].unique()), default=list(hdb2['town'].unique()))
        flat_type_filter = st.multiselect('Select Flat Type', options=list(hdb2['flat_type'].unique()), default=list(hdb2['flat_type'].unique()))

        park_filter = st.slider("Select the HDB's proximity to a park", min_value = hdb2.dist_hdb_to_park.min(), max_value = hdb2.dist_hdb_to_park.max(), value = hdb2.dist_hdb_to_park.max())
        mall_filter = st.slider("Select the HDB's proximity to a mall", min_value = hdb2.dist_hdb_to_mall.min(), max_value = hdb2.dist_hdb_to_mall.max(), value = hdb2.dist_hdb_to_mall.max())
        prisch_filter = st.slider("Select the HDB's proximity to a Primary School", min_value = hdb2.dist_hdb_to_prisch.min(), max_value = hdb2.dist_hdb_to_prisch.max(), value = hdb2.dist_hdb_to_prisch.max())
        mrt_filter = st.slider("Select the HDB's proximity to an MRT Station", min_value = hdb2.dist_hdb_to_mrt.min(), max_value = hdb2.dist_hdb_to_mrt.max(), value = hdb2.dist_hdb_to_mrt.max())
        bus_filter = st.slider("Select the HDB's proximity to a Bus Station", min_value = hdb2.dist_hdb_to_bus.min(), max_value = hdb2.dist_hdb_to_bus.max(), value = hdb2.dist_hdb_to_bus.max())

        # Final Dataframe
        filtered_hdb = hdb2[hdb2['town'].isin(town_filter) 
                            & hdb2['flat_type'].isin(flat_type_filter) 
                            & (hdb2['dist_hdb_to_park'] <= park_filter) 
                            & (hdb2['dist_hdb_to_mall'] <= mall_filter) 
                            & (hdb2['dist_hdb_to_prisch'] <= prisch_filter) 
                            & (hdb2['dist_hdb_to_mrt'] <= mrt_filter) 
                            & (hdb2['dist_hdb_to_bus'] <= bus_filter)]

        # st.write(filtered_hdb.head(5))
        filtered_hdb = filtered_hdb.sort_values(by=['score'], ascending=False)
        filtered_hdb = filtered_hdb.reset_index(drop=True)
        filtered_hdb.index = filtered_hdb.index + 1
        # filtered_hdb = filtered_hdb.head(10)
        # st.write(filtered_hdb.head(5))
        # Output Table
        st.write('Your top 10 most recommended HDB Flats')
        st.dataframe(filtered_hdb)

        # Output Map
        st.write('Location')
        st.map(filtered_hdb,
            latitude='lat',
            longitude='lon',)

fragment()