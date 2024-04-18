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

        # Cost per sqm (sort by score computed by rating*normalised, then sort final results using price_per_sqm_normalized from low to high)
        st.subheader('1. I prefer flats that are value for money.')
        costsqm_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='costsqm_rating')
        ratings['Costsqm_Rating'].append(costsqm_rating)

        st.write("#")

        # Size (sort by score computed by rating*normalised, then sort final results using floor_area_sqm from high to low)
        st.subheader('2. I prefer flats that are huge.')
        size_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='size_rating')
        ratings['Size_Rating'].append(size_rating)

        st.write("#")

        # Investment (add weightage to the rating with selected investment percentage (10%, 20%, 30%) - multiplier_effect, sort by score computed by rating*normalised (times 2?), then sort final results using multiplier_effect from high to low)
        st.subheader('3. I view housing as an investment, and I expect high returns in the next 5 years, with at least ')
        c1, c2 = st.columns((1,3))
        with c1:
            investment_range = st.selectbox('investment', ('10% growth', '20% growth', '30% growth'), key = 'investment_range', index=1, placeholder="", label_visibility="collapsed")

        with c2:
            st.write("#")

        def prox_invest(x):
            if x == '10% growth':
                return 0.1
            elif x == '20% growth':
                return 0.2
            else:
                return 0.3
            
        investment_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='investment_rating')

        ratings['Investment_Range'].append(prox_invest(investment_range))
        ratings['Investment_Rating'].append(investment_rating)
        st.write("#")

        # Floor (add weightage to the rating with selected floors - storey_range_score (1 - low floor, 2 - mid floor, 3,4 - high floor),  sort by score computed by updated_weightage*normalised)
        # Floor will affect the predicted price only (based on the average predicted price for respective floor storey)
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
        
        # Lease (sort by score computed by rating*normalised, then sort final results using remaining_mths_left_asof_2024 from high to low)
        st.subheader('5. I am looking for flats with a long lease.')
        lease_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='lease_rating')
        ratings['Lease_Rating'].append(lease_rating)
        st.write("#")

        # Age (sort by score computed by rating*normalised, then sort final results using avg_age_by_pa from high to low)
        st.subheader('6. I prefer to live in an area with a ')
        c7, c8 = st.columns((1,3))
        with c7:
            age_range = st.selectbox('age', ('Young population', 'Mid-Age population', 'Elderly population'), key = 'age_range', index=0, placeholder="", label_visibility="collapsed")

        with c8:
            st.write("#")

        age_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='age_rating')

        ratings['Age_Range'].append(age_range)
        ratings['Age_Rating'].append(age_rating)
        st.write("#")

        # Income (sort by score computed by rating*normalised, then sort final results using median_hhi_by_pa from high to low)
        st.subheader('7. I prefer to live in an area with a high median household income.')
        income_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='income_rating')
        ratings['Income_Rating'].append(income_rating)
        st.write("#")

        # MRT (sort by score computed by rating*normalised, then sort final results using dist_hdb_to_mrt from low to high)
        st.subheader('8. I prefer to stay within 10 mins walking distance to the nearest MRT station.')
        mrt_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='mrt_rating')
        ratings['MRT_Rating'].append(mrt_rating)
        st.write("#")

        # Bus (sort by score computed by rating*normalised, then sort final results using dist_hdb_to_bus from low to high)
        st.subheader('9. I prefer to stay within 10 mins walking distance to the nearest bus interchange.')
        bus_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='bus_rating')
        ratings['Bus_Rating'].append(bus_rating)
        st.write("#")

        # Park (sort by score computed by rating*normalised, then sort final results using dist_hdb_to_park from low to high)
        st.subheader('10. I prefer to stay within 10 mins walking distance to the nearest park.')
        park_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='park_rating')
        ratings['Park_Rating'].append(park_rating)
        st.write("#")

        # Mall (sort by score computed by rating*normalised, then sort final results using dist_hdb_to_mall from low to high)
        st.subheader('11. I prefer to stay within 10 mins walking distance to the nearest shopping mall.')
        mall_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='mall_rating')
        ratings['Mall_Rating'].append(mall_rating)
        st.write("#")

        # Pri Sch (sort by score computed by rating*normalised, then sort final results using dist_hdb_to_prisch from low to high)
        st.subheader('12. I prefer to stay within 10 mins walking distance to the nearest primary school.')
        prisch_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='prisch_rating')
        ratings['Prisch_Rating'].append(prisch_rating)
        st.write("#")

        st.button("Generate My Personalized HDB Recommendation", on_click=click_button)

    else:

        st.title('Your personalized HDB Recommendation')

        ############################ Visualization ############################

        hdb2 = run_query(f"""
            WITH t1 AS (
                SELECT
                full_addr
                ,flat_type
                ,MIN(town) AS town
                ,MIN(block) AS block
                ,MIN(street_name) AS street_name
                ,MIN(floor_area_sqm) AS floor_area_sqm
                ,MIN(postal) AS postal
                ,MIN(lat) AS lat
                ,MIN(lon) AS lon
                ,MIN(remaining_yrs_left_asof_2024) AS remaining_yrs_left_asof_2024
                ,MIN(remaining_mths_left_asof_2024) AS remaining_mths_left_asof_2024
                ,MIN(pln_area_n) AS pln_area_n
                ,MIN(subzone_n) AS subzone_n
                ,MIN(mrt_name) AS mrt_name
                ,MIN(dist_hdb_to_mrt) AS dist_hdb_to_mrt
                ,MIN(bus_interchange) AS bus_interchange
                ,MIN(dist_hdb_to_bus) AS dist_hdb_to_bus
                ,MIN(pri_school) AS pri_school
                ,MIN(dist_hdb_to_prisch) AS dist_hdb_to_prisch 
                ,MIN(avg_age_by_pa) AS avg_age_by_pa
                ,CASE
                WHEN MIN(avg_age_by_pa) <= 38 THEN "Young population"
                WHEN MIN(avg_age_by_pa) > 38 AND MIN(avg_age_by_pa) <= 43  THEN "Mid-Age population"
                ELSE "Elderly population" END AS population_age
                ,MIN(median_hhi_by_pa) AS median_hhi_by_pa
                ,MIN(park) AS park
                ,MIN(dist_hdb_to_park) AS dist_hdb_to_park
                ,MIN(mall) AS mall
                ,MIN(dist_hdb_to_mall) AS dist_hdb_to_mall
                ,MIN(dist_hdb_to_park_normalized) AS dist_hdb_to_park_normalized
                ,MIN(dist_hdb_to_mall_normalized) AS dist_hdb_to_mall_normalized
                ,MIN(dist_hdb_to_prisch_normalized) AS dist_hdb_to_prisch_normalized
                ,MIN(dist_hdb_to_mrt_normalized) AS dist_hdb_to_mrt_normalized
                ,MIN(dist_hdb_to_bus_normalized) AS dist_hdb_to_bus_normalized
                ,MIN(projected_5_years_normalized) AS projected_5_years_normalized
                ,MIN(avg_age_by_pa_normalized) AS avg_age_by_pa_normalized
                ,MIN(median_hhi_by_pa_normalized) AS median_hhi_by_pa_normalized
                ,MIN(remaining_mths_lease_normalized) AS remaining_mths_lease_normalized
                ,MIN(floor_area_sqm_normalized) AS floor_area_sqm_normalized
                ,MIN(multiplier_effect-1) AS investment_rate
                ,AVG(price_per_sqm) AS price_per_sqm
                ,AVG(price_per_sqm_normalized) AS price_per_sqm_normalized
                ,AVG(predicted_price) AS predicted_price
                ,AVG(projected_5_years) AS projected_5_years
                FROM `skillful-elf-416113.hdb.hdb_resale_final`
                WHERE flat_type = '4 ROOM' and predicted_price <= 800000
                GROUP BY
                full_addr
                ,flat_type
                ),
                t2 AS (
                SELECT *,
                CASE WHEN t1.investment_rate >= SAFE_CAST('{ratings['Investment_Range'][0]}' AS FLOAT64) THEN 1 ELSE 0.8 END AS investment_weightage_multiplier,
                CASE WHEN t1.population_age = '{ratings['Age_Range'][0]}' THEN 1 ELSE 0.8 END AS population_weightage_multiplier
                FROM t1
                )
                SELECT
                town,
                block,
                street_name,
                flat_type,
                ROUND(floor_area_sqm,0) AS floor_area_sqm,
                CONCAT("$",ROUND(price_per_sqm,2)) AS price_per_sqm,
                CONCAT(ROUND((investment_rate-1)*100,2),"%") AS expected_return_in_5yr,
                remaining_yrs_left_asof_2024 AS lease,
                population_age,
                median_hhi_by_pa,
                mrt_name AS nearest_mrt,
                bus_interchange AS nearest_bus_interchange,
                park AS nearest_park,
                mall AS nearest_mall,
                pri_school AS nearest_primary_school,
                lat,
                lon,
                ROUND((
                SAFE_CAST('{ratings['Costsqm_Rating'][0]}' AS FLOAT64) * price_per_sqm_normalized +
                SAFE_CAST('{ratings['Size_Rating'][0]}' AS FLOAT64) * floor_area_sqm_normalized +
                SAFE_CAST('{ratings['Investment_Rating'][0]}' AS FLOAT64) * investment_weightage_multiplier * investment_rate +
                SAFE_CAST('{ratings['Lease_Rating'][0]}' AS FLOAT64) * remaining_mths_lease_normalized +
                SAFE_CAST('{ratings['Age_Rating'][0]}' AS FLOAT64) * population_weightage_multiplier * avg_age_by_pa_normalized +
                SAFE_CAST('{ratings['Income_Rating'][0]}' AS FLOAT64) * median_hhi_by_pa_normalized +
                SAFE_CAST('{ratings['MRT_Rating'][0]}' AS FLOAT64) * dist_hdb_to_mrt_normalized +
                SAFE_CAST('{ratings['Bus_Rating'][0]}' AS FLOAT64) * dist_hdb_to_bus_normalized +
                SAFE_CAST('{ratings['Park_Rating'][0]}' AS FLOAT64) * dist_hdb_to_park_normalized +
                SAFE_CAST('{ratings['Mall_Rating'][0]}' AS FLOAT64) * dist_hdb_to_mall_normalized +
                SAFE_CAST('{ratings['Prisch_Rating'][0]}' AS FLOAT64) * dist_hdb_to_prisch_normalized),2) AS score
                FROM t2
                ORDER BY score DESC, price_per_sqm_normalized, floor_area_sqm_normalized DESC, investment_rate DESC, remaining_mths_lease_normalized DESC, dist_hdb_to_mrt_normalized, dist_hdb_to_bus_normalized, dist_hdb_to_park_normalized, dist_hdb_to_mall_normalized, dist_hdb_to_prisch_normalized
                LIMIT 10
                         """)

        hdb3 = hdb2[['town', 'block', 'street_name', 'flat_type', 'floor_area_sqm', 'price_per_sqm', 'expected_return_in_5yr', 'lease', 'population_age', 'median_hhi_by_pa', 'nearest_mrt','nearest_bus_interchange', 'nearest_park', 'nearest_mall', 'nearest_primary_school','score']]
        
        # Output Table
        st.subheader('Your top 10 most recommended HDB Flats')
        st.dataframe(hdb3)

        # Output Map
        st.subheader('Map location')
        st.map(hdb2,
            latitude='lat',
            longitude='lon',)
        

fragment()