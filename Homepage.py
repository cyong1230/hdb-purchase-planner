import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
from streamlit_star_rating import st_star_rating

st.set_page_config(
    page_title = 'Singapore Property Purchase Planner',
    page_icon = '?',
    layout = 'wide',
    )

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return pd.DataFrame(rows)


#rows = run_query("SELECT COUNT(*) as count_row FROM `skillful-elf-416113.hdb.hdb_resale_final` LIMIT 1000")
#hdb = run_query("SELECT * FROM `skillful-elf-416113.hdb.hdb_resale_final` LIMIT 1000")

# Print results.
# st.write("Total Count: ")
# for row in rows:
#     st.write(row['count_row'])

# hdb = pd.DataFrame(df_dict)

# Getting the floor level
# hdb['first_level'] = hdb['storey_range'].str.extract(r'^(\d{2}).*$')
# hdb['last_level'] = hdb['storey_range'].str.extract(r'^.*(\d{2})$')
# hdb['first_level'] = hdb['first_level'].astype(int)
# hdb['last_level'] = hdb['last_level'].astype(int)
# hdb['level'] = (hdb['first_level'] + hdb['last_level'])/2

#ram = hdb['multiplier_effect'].unique()
# st.write(ram)

# st.write(hdb.head(5))
# st.write(hdb.shape[0])

if "script_runs" not in st.session_state:
    st.session_state.fragment_runs = 0

ratings = {'CPF': [], 'Cash': [], 'Grant_Indicator': [], 'Grant_Amount': [], 'Grant_Rooms': [],
            'Price_Range': [], 'Size_Range': [], 'Costsqm_Range': [], 'Investment_Range': [], 
            'Floor_Range': [], 'Lease_Range': [], 'Age_Range': [], 'Income_Range': [], 
            'Park_Range': [], 'Mall_Range': [], 'Prisch_Range': [], 'MRT_Range': [], 
            'Bus_Range': [], 
            'Price_Rating': [], 'Size_Rating': [], 'Costsqm_Rating': [], 'Investment_Rating': [], 
            'Floor_Rating': [], 'Lease_Rating': [], 'Age_Rating': [], 'Income_Rating': [], 
            'Park_Rating': [], 'Mall_Rating': [], 'Prisch_Rating': [], 'MRT_Rating': [], 
            'Bus_Rating': [],
            'Price_Filter': [], 'Size_Filter': [], 'Costsqm_Filter': [], 'Investment_Filter': [],
            'Floor_Filter': [], 'Lease_Filter': [], 'Age_Filter': [], 'Income_Filter': [],
            'Park_Proximity': [], 'Mall_Proximity': [], 'Primary_School_Proximity': [], 
            'MRT_Proximity': [], 'Bus_Proximity': []}


def click_button():
    st.session_state.fragment_runs += 1

@st.experimental_fragment
def fragment():
    global ratings
    global hdb

    if st.session_state.fragment_runs == 0:
        ############################ User Input Form ############################
        st.title('Singapore Property Purchase Planner')

        # HDB Budget Calculator
        st.header('Please answer these questions to calculate your budget')

        grant_indicator = ''


        user_age = st.number_input('Age', min_value = 0, value = None)

        cpf = st.number_input('CPF Savings', min_value = 0.00, value = None)

        cash = st.number_input('Cash Savings', min_value = 0.00, value = None)

        grant_rooms = st.selectbox('What type of HDB do you intend to buy?', ('2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM or larger'), 
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
                        if grant_rooms == '5 ROOM or larger':
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
                        if grant_rooms == '5 ROOM or larger':
                            grant_indicator = 'Family'
                            grant_amount = 40000
                        else:
                            grant_indicator = 'Family'
                            grant_amount = 50000
                    elif (user_citizen == 'Singapore Citizen' and partner_citizen == 'PR') or (user_citizen == 'PR' and partner_citizen == 'Singapore Citizen'):
                        if grant_rooms == '5 ROOM or larger':
                            grant_indicator = 'Family'
                            grant_amount = 30000
                        else:
                            grant_indicator = 'Family'
                            grant_amount = 40000
                    elif (user_citizen == 'Singapore Citizen' and partner_citizen == 'Foreigner') or (user_citizen == 'Foreigner' and partner_citizen == 'Singapore Citizen'):
                        if grant_rooms == '5 ROOM or larger':
                            grant_indicator = 'Family'
                            grant_amount = 25000
                        else:
                            grant_indicator = 'Family'
                            grant_amount = 20000
                    elif user_citizen in ['PR', 'Foreigner'] and partner_citizen in ['PR', 'Foreigner']:
                        st.error('One person needs to be a Singapore Citizen', icon="🚨")
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
            ratings['Price_Range'].append(int(budget))
            ratings['Grant_Rooms'].append(grant_rooms)

            st.button("Next", on_click=click_button)
        elif grant_indicator == 'Nil':
            st.header(':neutral_face: You are not eligible to purchase a resale HDB')


    elif st.session_state.fragment_runs == 1:
        st.write("#")
        # test values
        # ratings['Price_Range'].append(int(1000000))
        # ratings['Grant_Rooms'].append("4 ROOM")

        # hdb = run_query("SELECT * FROM `skillful-elf-416113.hdb.hdb_resale_final` LIMIT 1000")
        if ratings['Grant_Rooms'][0] == '5 ROOM or larger':
            hdb = run_query(f"SELECT COUNT(DISTINCT full_addr) as count_row FROM `skillful-elf-416113.hdb.hdb_resale_final` WHERE flat_type != '{ratings['Grant_Rooms'][0]}' and predicted_price <= SAFE_CAST('{ratings['Price_Range'][0]}' as INT64) LIMIT 100")
        else:
            hdb = run_query(f"SELECT COUNT(DISTINCT full_addr) as count_row FROM `skillful-elf-416113.hdb.hdb_resale_final` WHERE flat_type = '{ratings['Grant_Rooms'][0]}' and predicted_price <= SAFE_CAST('{ratings['Price_Range'][0]}' as INT64) LIMIT 100")

        st.info(f"There are {hdb['count_row'][0]} of {ratings['Grant_Rooms'][0]} HDB flats that can meet your budget of ${ratings['Price_Range'][0]}.", icon="ℹ️")
        st.header('Find out your top 10 choices by indicating your preferences (1 star - Not Important, 10 stars - Very Important)')
        # st.header('Please indicate your housing preferences and their importance to find out your top 10 choices (1 star - Not Important, 10 stars - Very Important)')

        st.write("#")

        # Cost per sqm (sort price_per_sqm_normalized from high to low)
        st.subheader('1. I prefer flats that are value for money.')
        costsqm_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='costsqm_rating')
        ratings['Costsqm_Rating'].append(costsqm_rating)

        st.write("#")

        # Size (sort floor_area_sqm from high to low)
        st.subheader('2. I prefer flats that are huge.')
        size_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='size_rating')
        ratings['Size_Rating'].append(size_rating)

        st.write("#")

        # Investment
        st.subheader('3. I view housing as an investment, and I expect high returns in the next 5 years, at least ')
        c1, c2 = st.columns((1,3))
        with c1:
            investment_range = st.selectbox('investment', ('10% growth', '20% growth', '30% growth'), key = 'investment_range', index=1, placeholder="", label_visibility="collapsed")

        with c2:
            st.write("#")

        investment_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='investment_rating')

        ratings['Investment_Range'].append(investment_range)
        ratings['Investment_Rating'].append(investment_rating)
        st.write("#")

        # Floor
        st.subheader('4. I prefer flats that are located on the ')
        c4, c5 = st.columns((1,3))
        with c4:
            floor_range = st.selectbox('floor', ('Low floors', 'Mid floors', 'High floors'), key = 'floor_range', index=2, placeholder="", label_visibility="collapsed")

        with c5:
            st.write("#")

        floor_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='floor_rating')

        ratings['Floor_Range'].append(floor_range)
        ratings['Floor_Rating'].append(floor_rating)
        st.write("#")
        
        # Lease
        st.subheader('5. I am looking for areas with a long lease.')
        lease_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='lease_rating')
        ratings['Lease_Rating'].append(lease_rating)
        st.write("#")

        # Age
        st.subheader('6. I prefer to live in flats with a ')
        c7, c8 = st.columns((1,3))
        with c7:
            age_range = st.selectbox('age', ('Young population', 'Mid-Age population', 'Elderly population'), key = 'age_range', index=0, placeholder="", label_visibility="collapsed")

        with c8:
            st.write("#")

        age_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='age_rating')

        ratings['Floor_Range'].append(age_range)
        ratings['Age_Rating'].append(age_rating)
        st.write("#")

        # Income
        st.subheader('7. I prefer to live in HDB flats with a high household income.')
        income_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='income_rating')
        ratings['Income_Rating'].append(income_rating)
        st.write("#")

        # MRT
        st.subheader('8. I prefer to stay within 10 mins walking distance to the nearby MRT.')
        mrt_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='mrt_rating')
        ratings['MRT_Rating'].append(mrt_rating)
        st.write("#")

        # Bus
        st.subheader('9. I prefer to stay within 10 mins walking distance to the nearby bus interchange.')
        bus_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='bus_rating')
        ratings['Bus_Rating'].append(bus_rating)
        st.write("#")

        # Park
        st.subheader('10. I prefer to stay within 10 mins walking distance to the nearby park.')
        park_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='park_rating')
        ratings['Park_Rating'].append(park_rating)
        st.write("#")

        # Mall
        st.subheader('11. I prefer to stay within 10 mins walking distance to the nearby shopping mall.')
        mall_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='mall_rating')
        ratings['Mall_Rating'].append(mall_rating)
        st.write("#")

        # Pri Sch
        st.subheader('12. I prefer to stay within 10 mins walking distance to the nearby primary school.')
        prisch_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='prisch_rating')
        ratings['Prisch_Rating'].append(prisch_rating)
        st.write("#")

        st.button("Generate My Personalized HDB Recommendation", on_click=click_button)

    else:

        st.title('Your personalized HDB Recommendation')

        ############################ Visualization ############################
        # Prepping main table
        # hdb['score'] = ((hdb['predicted_price_normalized']*ratings['Price_Rating'][0]) + (hdb['price_per_sqm_normalized']*ratings['Costsqm_Rating'][0]) + 
        #                 (hdb['projected_5_years_normalized']*ratings['Investment_Rating'][0]) + (hdb['storey_range_normalized']*ratings['Floor_Rating'][0]) + 
        #                 (hdb['remaining_mths_lease_normalized']*ratings['Lease_Rating'][0]) + (hdb['avg_age_by_pa_normalized']*ratings['Age_Rating'][0]) + 
        #                 (hdb['median_hhi_by_pa_normalized']*ratings['Income_Rating'][0]) + (hdb['dist_hdb_to_park_normalized']*ratings['Park_Rating'][0]) + 
        #                 (hdb['dist_hdb_to_mall_normalized']*ratings['Mall_Rating'][0]) + (hdb['dist_hdb_to_prisch_normalized']*ratings['Prisch_Rating'][0]) + 
        #                 (hdb['dist_hdb_to_mrt_normalized']*ratings['MRT_Rating'][0]) + (hdb['dist_hdb_to_bus_normalized']*ratings['Bus_Rating'][0]) +
        #                 (hdb['floor_area_sqm_normalized']*ratings['Floor_Rating'][0]))

        # hdb = hdb[['town', 'flat_type', 'block', 'street_name', 'flat_model', 'resale_price', 'floor_area_sqm', 'price_per_sqm', 'storey_range', 'remaining_mths_left_asof_2024', 'avg_age_by_pa', 'median_hhi_by_pa', 'floor_area_sqm_normalized', 'dist_hdb_to_park', 'dist_hdb_to_mall', 'dist_hdb_to_prisch', 'dist_hdb_to_mrt', 'dist_hdb_to_bus', 'lat', 'lon', 'score']]

        # def prox_price(x):
        #     if x == '0 to 400 Thousand':
        #         return 400000
        #     elif x == '400 Thousand to 650 Thousand':
        #         return 650000
        #     else:
        #         return 1000000000000
            
        # def prox_size(x):
        #     if x == '0 to 70 sqm':
        #         return 70
        #     elif x == '70 sqm to 100 sqm':
        #         return 100
        #     else:
        #         return 10000

        # def prox_costsqm(x):
        #     if x == '0 to 4500':
        #         return 4500
        #     elif x == '4500 to 6000':
        #         return 6000
        #     else:
        #         return 10000000
            
        # def prox_floor(x):
        #     if x == 'Low':
        #         return 5
        #     elif x == 'Mid':
        #         return 11
        #     else:
        #         return 100
            
        # def prox_lease(x):
        #     if x == '0 to 60 Years Left':
        #         return 60
        #     elif x == '60 to 80 Years Left':
        #         return 80
        #     else:
        #         return 1000
            
        # def prox_age(x):
        #     if x == 'Young':
        #         return 38
        #     elif x == 'Mid-Age':
        #         return 43
        #     else:
        #         return 1000
            
        # def prox_income(x):
        #     if x == '0 to 6500':
        #         return 6500
        #     elif x == '6500 to 8500':
        #         return 8500
        #     else:
        #         return 10000000

        # def prox(x):
        #     if x == 'Walking Distance':
        #         return 500
        #     elif x == 'A Station Over':
        #         return 1000
        #     else:
        #         return 100000

        # ratings['Price_Filter'].append(prox_price(ratings['Price_Range'][0]))
        # ratings['Size_Filter'].append(prox_size(ratings['Size_Range'][0]))
        # ratings['Costsqm_Filter'].append(prox_costsqm(ratings['Costsqm_Range'][0]))
        # # ratings['Investment_Filter'].append(prox_investment(ratings['Investment_Range'][0]))
        # # ratings['Floor_Filter'].append(prox_floor(ratings['Floor_Range'][0]))
        # ratings['Lease_Filter'].append(prox_lease(ratings['Lease_Range'][0]))
        # ratings['Age_Filter'].append(prox_age(ratings['Age_Range'][0]))
        # ratings['Income_Filter'].append(prox_income(ratings['Income_Range'][0]))        
        # ratings['Park_Proximity'].append(prox(ratings['Park_Range'][0]))
        # ratings['Mall_Proximity'].append(prox(ratings['Mall_Range'][0]))
        # ratings['Primary_School_Proximity'].append(prox(ratings['Prisch_Range'][0]))
        # ratings['MRT_Proximity'].append(prox(ratings['MRT_Range'][0]))
        # ratings['Bus_Proximity'].append(prox(ratings['Bus_Range'][0]))

        

        # # Filtering main table based on user input
        # hdb2 = hdb[(hdb['resale_price'] <= ratings['Price_Filter'][0]) 
        #         & (hdb['floor_area_sqm'] <= ratings['Size_Filter'][0]) 
        #         & (hdb['price_per_sqm'] <= ratings['Costsqm_Filter'][0]) 
        #         & (hdb['remaining_mths_left_asof_2024'] <= ratings['Lease_Filter'][0]) 
        #         & (hdb['avg_age_by_pa'] <= ratings['Age_Filter'][0]) 
        #         & (hdb['median_hhi_by_pa'] <= ratings['Income_Filter'][0]) 
        #         & (hdb['dist_hdb_to_park'] <= ratings['Park_Proximity'][0]) 
        #         & (hdb['dist_hdb_to_mall'] <= ratings['Mall_Proximity'][0]) 
        #         & (hdb['dist_hdb_to_prisch'] <= ratings['Primary_School_Proximity'][0]) 
        #         & (hdb['dist_hdb_to_mrt'] <= ratings['MRT_Proximity'][0]) 
        #         & (hdb['dist_hdb_to_bus'] <= ratings['Bus_Proximity'][0])]

        # # town_filter = st.multiselect('Select Town', options=list(hdb2['town'].unique()), default=list(hdb2['town'].unique()))
        # # flat_type_filter = st.multiselect('Select Flat Type', options=list(hdb2['flat_type'].unique()), default=list(hdb2['flat_type'].unique()))

        # # price_filter = st.slider("Select the HDB's Price", min_value = hdb2.resale_price.min(), max_value = hdb2.resale_price.max(), value = hdb2.resale_price.max())
        # # size_filter = st.slider("Select the HDB's Size", min_value = hdb2.floor_area_sqm.min(), max_value = hdb2.floor_area_sqm.max(), value = hdb2.floor_area_sqm.max())
        # # costsqm_filter = st.slider("Select the HDB's Cost Per Sqm", min_value = hdb2.price_per_sqm.min(), max_value = hdb2.price_per_sqm.max(), value = hdb2.price_per_sqm.max())
        # # lease_filter = st.slider("Select the HDB's Remaining Lease", min_value = hdb2.remaining_mths_left_asof_2024.min(), max_value = hdb2.remaining_mths_left_asof_2024.max(), value = hdb2.remaining_mths_left_asof_2024.max())
        # # age_filter = st.slider("Select the HDB's Population's Average Age", min_value = hdb2.avg_age_by_pa.min(), max_value = hdb2.avg_age_by_pa.max(), value = hdb2.avg_age_by_pa.max())
        # # income_filter = st.slider("Select the HDB's Average Income Level", min_value = hdb2.median_hhi_by_pa.min(), max_value = hdb2.median_hhi_by_pa.max(), value = hdb2.median_hhi_by_pa.max())
        
        # # park_filter = st.slider("Select the HDB's proximity to a park", min_value = hdb2.dist_hdb_to_park.min(), max_value = hdb2.dist_hdb_to_park.max(), value = hdb2.dist_hdb_to_park.max())
        # # mall_filter = st.slider("Select the HDB's proximity to a mall", min_value = hdb2.dist_hdb_to_mall.min(), max_value = hdb2.dist_hdb_to_mall.max(), value = hdb2.dist_hdb_to_mall.max())
        # # prisch_filter = st.slider("Select the HDB's proximity to a Primary School", min_value = hdb2.dist_hdb_to_prisch.min(), max_value = hdb2.dist_hdb_to_prisch.max(), value = hdb2.dist_hdb_to_prisch.max())
        # # mrt_filter = st.slider("Select the HDB's proximity to an MRT Station", min_value = hdb2.dist_hdb_to_mrt.min(), max_value = hdb2.dist_hdb_to_mrt.max(), value = hdb2.dist_hdb_to_mrt.max())
        # # bus_filter = st.slider("Select the HDB's proximity to a Bus Station", min_value = hdb2.dist_hdb_to_bus.min(), max_value = hdb2.dist_hdb_to_bus.max(), value = hdb2.dist_hdb_to_bus.max())

        # # Final Dataframe
        # filtered_hdb = hdb2[hdb2['town'].isin(town_filter) 
        #                     & hdb2['flat_type'].isin(flat_type_filter) 
        #                     & (hdb2['resale_price'] <= price_filter) 
        #                     & (hdb2['floor_area_sqm'] <= size_filter) 
        #                     & (hdb2['price_per_sqm'] <= costsqm_filter) 
        #                     & (hdb2['remaining_mths_left_asof_2024'] <= lease_filter) 
        #                     & (hdb2['avg_age_by_pa'] <= age_filter) 
        #                     & (hdb2['median_hhi_by_pa'] <= income_filter)
        #                     & (hdb2['dist_hdb_to_park'] <= park_filter) 
        #                     & (hdb2['dist_hdb_to_mall'] <= mall_filter) 
        #                     & (hdb2['dist_hdb_to_prisch'] <= prisch_filter) 
        #                     & (hdb2['dist_hdb_to_mrt'] <= mrt_filter) 
        #                     & (hdb2['dist_hdb_to_bus'] <= bus_filter)]

        # filtered_hdb = filtered_hdb.sort_values(by=['score'], ascending=False)
        # filtered_hdb = filtered_hdb.reset_index(drop=True)
        # filtered_hdb.index = filtered_hdb.index + 1

        # # Output Table
        # st.table(ratings)
        
        # st.write('Your top 10 most recommended HDB Flats')
        # st.dataframe(filtered_hdb)

        # # Output Map
        # st.write('Location')
        # st.map(filtered_hdb,
        #     latitude='lat',
        #     longitude='lon',)

fragment()