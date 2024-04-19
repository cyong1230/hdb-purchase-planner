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

if "script_runs" not in st.session_state:
    st.session_state.fragment_runs = 0

def click_button():
    st.session_state.fragment_runs += 1

def click_button2():
    st.session_state.fragment_runs -= 1

@st.experimental_fragment
def fragment():
    global costsqm_rating
    global grant_rooms
    global budget
    global costsqm_rating
    global size_rating
    global investment_range
    global investment_range2
    global investment_rating
    global floor_range
    global floor_rating
    global lease_rating
    global age_range
    global age_rating
    global income_rating
    global mrt_rating
    global bus_rating
    global park_rating
    global mall_rating
    global prisch_rating

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
                        grant_indicator = 'Nil_age35'
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
            budget = int((cash+cpf)*5 + grant_amount)
            st.header('You are eligible to purchase a resale HDB with the following budget')
            st.write(':one: Eligible for a {0} grant of ${1}'.format(grant_indicator,grant_amount))
            st.write(':two: Eligible for a loan amount of ${0}'.format(int(loan)))
            st.write(':three: Total cash and cpf proceeds of ${0}'.format(int(cash+cpf)))
            st.subheader(':arrow_right: Your max HDB budget is ${0}'.format(int(budget)))

            st.button("Next", on_click=click_button)
        elif grant_indicator == 'Nil':
            st.header(':neutral_face: You are not eligible to purchase a resale HDB')
        elif grant_indicator == 'Nil_age35':
            st.header(':neutral_face: You must be over 35 years old to purchase a resale HDB as a single')


    elif st.session_state.fragment_runs == 1:
        st.write("#")

        # test values
        # grant_rooms = "4 ROOM"
        # budget = 1020000

        hdb = run_query("SELECT * FROM `skillful-elf-416113.hdb.hdb_resale_final` LIMIT 1000")
        if grant_rooms == '5 ROOM or larger':
            hdb = run_query(f"SELECT COUNT(DISTINCT full_addr) as count_row FROM `skillful-elf-416113.hdb.hdb_resale_final` WHERE flat_type != '{grant_rooms}' and predicted_price <= SAFE_CAST('{budget}' as INT64) LIMIT 100")
        else:
            hdb = run_query(f"SELECT COUNT(DISTINCT full_addr) as count_row FROM `skillful-elf-416113.hdb.hdb_resale_final` WHERE flat_type = '{grant_rooms}' and predicted_price <= SAFE_CAST('{budget}' as INT64) LIMIT 100")

        st.info(f"There are {hdb['count_row'][0]} of {grant_rooms} HDB flats that can meet your max budget of ${budget}.", icon="ℹ️")
        st.header('Find out your top 10 choices by indicating your preferences (1 star - Not Important, 10 stars - Very Important)')

        st.write("#")
        # Budget
        budget2 = st.slider('Your Preferred Budget ($): ', 0, budget, budget)
        budget2 = int(budget2)

        # Cost per sqm (sort by score computed by rating*normalised, then sort final results using price_per_sqm_normalized from low to high)
        st.subheader('1. I prefer flats that are value for money.')
        costsqm_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='costsqm_rating')
        st.write("#")

        # Size (sort by score computed by rating*normalised, then sort final results using floor_area_sqm from high to low)
        st.subheader('2. I prefer flats that are huge.')
        size_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='size_rating')
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
        investment_range2 = prox_invest(investment_range)
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
        st.write("#")
        
        # Lease (sort by score computed by rating*normalised, then sort final results using remaining_mths_left_asof_2024 from high to low)
        st.subheader('5. I am looking for flats with a long lease.')
        lease_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='lease_rating')
        st.write("#")

        # Age (sort by score computed by rating*normalised, then sort final results using avg_age_by_pa from high to low)
        st.subheader('6. I prefer to live in an area with a ')
        c7, c8 = st.columns((1,3))
        with c7:
            age_range = st.selectbox('age', ('Young population', 'Mid-Age population', 'Elderly population'), key = 'age_range', index=0, placeholder="", label_visibility="collapsed")

        with c8:
            st.write("#")

        age_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='age_rating')
        st.write("#")

        # Income (sort by score computed by rating*normalised, then sort final results using median_hhi_by_pa from high to low)
        st.subheader('7. I prefer to live in an area with a high median household income.')
        income_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='income_rating')
        st.write("#")

        # MRT (sort by score computed by rating*normalised, then sort final results using dist_hdb_to_mrt from low to high)
        st.subheader('8. I prefer to stay within 10 mins walking distance to the nearest MRT station.')
        mrt_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='mrt_rating')
        st.write("#")

        # Bus (sort by score computed by rating*normalised, then sort final results using dist_hdb_to_bus from low to high)
        st.subheader('9. I prefer to stay within 10 mins walking distance to the nearest bus interchange.')
        bus_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='bus_rating')
        st.write("#")

        # Park (sort by score computed by rating*normalised, then sort final results using dist_hdb_to_park from low to high)
        st.subheader('10. I prefer to stay within 10 mins walking distance to the nearest park.')
        park_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='park_rating')
        st.write("#")

        # Mall (sort by score computed by rating*normalised, then sort final results using dist_hdb_to_mall from low to high)
        st.subheader('11. I prefer to stay within 10 mins walking distance to the nearest shopping mall.')
        mall_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='mall_rating')
        st.write("#")

        # Pri Sch (sort by score computed by rating*normalised, then sort final results using dist_hdb_to_prisch from low to high)
        st.subheader('12. I prefer to stay within 10 mins walking distance to the nearest primary school.')
        prisch_rating = st_star_rating(label='',maxValue=10, defaultValue=5, size=20, key='prisch_rating')
        st.write("#")

        st.button("Generate My Personalized HDB Recommendation", on_click=click_button)

    else:
        st.write("#")
        st.title('Your Personalized HDB Recommendation')

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
                WHERE flat_type = '{grant_rooms}' and predicted_price <= SAFE_CAST('{budget2}' AS FLOAT64)
                GROUP BY
                full_addr
                ,flat_type
                ),
                t2 AS (
                SELECT *,
                CASE WHEN t1.investment_rate >= SAFE_CAST('{investment_range2}' AS FLOAT64) THEN 1 ELSE 0.8 END AS investment_weightage_multiplier,
                CASE WHEN t1.population_age = '{age_range}' THEN 1 ELSE 0.98 END AS population_weightage_multiplier,
                CASE WHEN t1.dist_hdb_to_mrt <= 800 THEN 1 ELSE 0.3 END AS dist_hdb_to_mrt_multiplier,
                CASE WHEN t1.dist_hdb_to_bus <= 800 THEN 1 ELSE 0.2 END AS dist_hdb_to_bus_multiplier,
                CASE WHEN t1.dist_hdb_to_park <= 800 THEN 1 ELSE 0.2 END AS dist_hdb_to_park_multiplier,
                CASE WHEN t1.dist_hdb_to_mall <= 800 THEN 1 ELSE 0.2 END AS dist_hdb_to_mall_multiplier,
                CASE WHEN t1.dist_hdb_to_prisch <= 800 THEN 1 ELSE 0.3 END AS dist_hdb_to_prisch_multiplier,
                FROM t1
                )
                SELECT
                town,
                block,
                street_name,
                flat_type,
                ROUND(floor_area_sqm,0) AS floor_area_sqm,
                ROUND(predicted_price,2) AS predicted_price,
                CONCAT("$",ROUND(price_per_sqm,2)) AS price_per_sqm,
                CONCAT(ROUND((investment_rate)*100,2),"%") AS expected_return_in_5yr,
                remaining_yrs_left_asof_2024 AS lease,
                population_age,
                CONCAT("$",median_hhi_by_pa) AS median_hhi_by_pa,
                mrt_name AS nearest_mrt,
                ROUND(dist_hdb_to_mrt,2) AS dist_to_mrt_m,
                bus_interchange AS nearest_bus_interchange,
                ROUND(dist_hdb_to_bus,2) AS dist_to_bus_m,
                park AS nearest_park,
                ROUND(dist_hdb_to_park,2) AS dist_to_park_m,
                mall AS nearest_mall,
                ROUND(dist_hdb_to_mall,2) AS dist_to_mall_m,
                pri_school AS nearest_primary_school,
                ROUND(dist_hdb_to_prisch,2) AS dist_to_prisch_m,
                lat,
                lon,
                ROUND((
                SAFE_CAST('{costsqm_rating}' AS FLOAT64) * price_per_sqm_normalized * 0.8 +
                SAFE_CAST('{size_rating}' AS FLOAT64) * floor_area_sqm_normalized +
                SAFE_CAST('{investment_rating}' AS FLOAT64) * investment_weightage_multiplier * investment_rate +
                SAFE_CAST('{lease_rating}' AS FLOAT64) * remaining_mths_lease_normalized +
                SAFE_CAST('{age_rating}' AS FLOAT64) * population_weightage_multiplier * avg_age_by_pa_normalized +
                SAFE_CAST('{income_rating}' AS FLOAT64) * median_hhi_by_pa_normalized +
                SAFE_CAST('{mrt_rating}' AS FLOAT64) * dist_hdb_to_mrt_multiplier * dist_hdb_to_mrt_normalized +
                SAFE_CAST('{bus_rating}' AS FLOAT64) * dist_hdb_to_bus_multiplier * dist_hdb_to_bus_normalized +
                SAFE_CAST('{park_rating}' AS FLOAT64) * dist_hdb_to_park_multiplier * dist_hdb_to_park_normalized +
                SAFE_CAST('{mall_rating}' AS FLOAT64) * dist_hdb_to_mall_multiplier * dist_hdb_to_mall_normalized +
                SAFE_CAST('{prisch_rating}' AS FLOAT64) * dist_hdb_to_prisch_multiplier * dist_hdb_to_prisch_normalized),2) AS score
                FROM t2
                ORDER BY score DESC, price_per_sqm_normalized, floor_area_sqm_normalized DESC, investment_rate DESC, remaining_mths_lease_normalized DESC, dist_hdb_to_mrt_normalized, dist_hdb_to_bus_normalized, dist_hdb_to_park_normalized, dist_hdb_to_mall_normalized, dist_hdb_to_prisch_normalized
                LIMIT 10
                         """)

        hdb3 = hdb2[['town', 'block', 'street_name', 'predicted_price', 'flat_type', 'floor_area_sqm', 'price_per_sqm', 'expected_return_in_5yr', 'lease', 'population_age', 'median_hhi_by_pa', 'nearest_mrt', 'dist_to_mrt_m',
                     'nearest_bus_interchange', 'dist_to_bus_m', 'nearest_park', 'dist_to_park_m', 'nearest_mall', 'dist_to_mall_m', 'nearest_primary_school', 'dist_to_prisch_m', 'score']]

        # Output Table
        st.subheader('Your top 10 most recommended HDB Flats to purchase')
        st.info(f'''  
        Based on your budget of ${budget2} to purchase a {grant_rooms} HDB flat, and your preferences:
        - I prefer flats that are value for money.     {costsqm_rating} / 10
        - I prefer flats that are huge.     {size_rating} / 10
        - I view housing as an investment, and I expect high returns in the next 5 years, with at least {investment_range2}     {investment_rating} / 10
        - I prefer flats that are located on the {floor_range}     {floor_rating} / 10
        - I am looking for flats with a long lease.     {lease_rating} / 10
        - I prefer to live in an area with a {age_range}.     {age_rating} / 10
        - I prefer to live in an area with a high median household income.     {income_rating} / 10
        - I prefer to stay within 10 mins walking distance to the nearest MRT station.     {mrt_rating} / 10
        - I prefer to stay within 10 mins walking distance to the nearest bus interchange.     {bus_rating} / 10
        - I prefer to stay within 10 mins walking distance to the nearest park.     {park_rating} / 10
        - I prefer to stay within 10 mins walking distance to the nearest shopping mall.     {mall_rating} / 10
        - I prefer to stay within 10 mins walking distance to the nearest primary school.     {prisch_rating} / 10
        ''' )
        st.button("Try again with other preferences", on_click=click_button2)
        st.dataframe(hdb2)

        # Output Map
        st.subheader('Map location')
        st.map(hdb2,
            latitude='lat',
            longitude='lon',)
        

fragment()