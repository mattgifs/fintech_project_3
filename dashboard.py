import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from PIL import Image
load_dotenv()

#Title the dashboard
st.title("Wine Membership Dashboard")
st.markdown('---')


################################################################
# Query Customer Datatable, add to dataframe
################################################################

# Create postgres engine
engine = create_engine("postgresql://postgres:postgres@localhost:5432/fintech_project_3")

# Write the query
query = """
SELECT * FROM customer_data
"""

# Create a DataFrame from the query result.
df = pd.read_sql(query, engine)
df.set_index('tx_id',inplace=True)


################################################################
# Custom dataframes & Plots
################################################################

col1,col2 = st.columns(2)

# Setup df to track sales by Membership Type/Region
grouped_df = df.groupby('traitindex').size().reset_index(name='count')
grouped_df = grouped_df.sort_values(by='traitindex', ascending=True)
regions = {
    0:"Russian River Valley",
    1:"Napa Valley",
    2:"Oregon",
    3:"Columbia Valley",
    4:"Finger Lakes"
}
grouped_df['Region'] = grouped_df['traitindex'].map(regions)
grouped_df.set_index('Region',inplace=True)
grouped_df.sort_values('traitindex',ascending=True)

#Plot Count of Memberships sold by region
col1.markdown('#### Memberships Sold by Region')
col1.bar_chart(grouped_df,y='count', use_container_width=True)



# Cumsum amount raised from sales
df["ETH Raised"] = df['eth_price'].cumsum()

# Cumsum gas fees incurred
df["Cumulative Gas"] = df['gas_cost'].cumsum()

#Plot Cumulative Gas Fees Incurred & Cumulative ETH Raised 
col2.markdown('#### Cumulative Gas Fees Incurred')
col2.line_chart(df['Cumulative Gas'])

st.markdown('#### Cumulative ETH Raised')
st.line_chart(df['ETH Raised'])


# Display full customer_data dataframe
st.markdown('#### Transactions')
st.dataframe(data=df,use_container_width=False)