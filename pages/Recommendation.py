import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title('Your personalized HDB Recommendation')

ratings = pd.read_csv(r"C:\Users\B_Ash\HDB\ratings.csv")
hdb = pd.read_csv(r"C:\Users\B_Ash\HDB\hdb.csv")
del hdb['Unnamed: 0']


######################################################## Budget Calculator ########################################################
if ratings['CPF'][0] >= 0 or ratings['Cash'][0]:
    budget = (ratings['Cash'][0]+ratings['CPF'][0])*5
    st.subheader('Your Estimated Budget for your HDB is $%d.' % budget)
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

ratings['Park_Proximity'] = ratings.Park_Range.apply(prox)
ratings['Mall_Proximity'] = ratings.Mall_Range.apply(prox)
ratings['Primary_School_Proximity'] = ratings.Prisch_Range.apply(prox)
ratings['MRT_Proximity'] = ratings.MRT_Range.apply(prox)
ratings['Bus_Proximity'] = ratings.Bus_Range.apply(prox)

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