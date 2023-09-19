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


###########################################################################
# Display Banner Images on Streamlit Customer Portal
########################################################################### 
    
# Create six columns
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Display Top Images
with col1:
    st.image("./images/wine1.png")

with col2:
    st.image("./images/wine2.png")
    
with col3:
    st.image("./images/wine10.png")
    
with col4:
    st.image("./images/wine8.png")
    
with col5:
    st.image("./images/wine9.png")
    
with col6:
    st.image ("./images/wine3.png")

###########################################################################
# Define and connect a new Web3 provider
###########################################################################
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

###########################################################################
# The Load_Contract Function
###########################################################################
@st.cache_resource()
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/mem_token_abi.json')) as f:
        mem_token_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=mem_token_abi
    )

    return contract

contract = load_contract()

################################################################################
# Customer Payment Method Selection
################################################################################
st.title("Purchase Your Wine Membership")

# Load ganache accounts
accounts = w3.eth.accounts[4:]

# Customer select from ganache accounts
st.sidebar.markdown("## Add Payment Method")
address = st.sidebar.selectbox("Select Your Account", options=accounts)
if st.sidebar.button("Get Balance"):
    # Get wei balance, convert to eth, and round to two decimals
    wall_bal = float(round(w3.fromWei(w3.eth.get_balance(address), "ether"),2))
    # Write resulting wall_bal
    st.sidebar.write(f'Your current balance is:  {wall_bal} ETH')

################################################################################
# Populate Dropdown with Available Membership Options (Traits)
################################################################################
    
# Define dictionary to hold formatted trait info & traitIndex values
mem_options = {}

# Initialize empty traitIndex
traitIndex = 0

# Use for loop to call all available traits from the deployed contract
for ele in list(range(0, 5)):
    # Call the membership info by element
    trait_data = contract.functions.getMembershipInfo(ele).call()
    # Save the values to trait_data
    name, Price, maxSupply, mintedCount = trait_data
    # Call trait price in wei 
    trait_price_wei = w3.toWei(Price, 'wei')
    # Convert price to ETH
    trait_price_eth= w3.fromWei(trait_price_wei, 'ether') 
    # Format the trait_data for display in dropdown
    trait_form = f' {name} | Price: {trait_price_eth} ETH | Remaining: {maxSupply - mintedCount}/{maxSupply}'
    # Add the trait_form and the ele (traitIndex) to the mem_options dictionary 
    mem_options[trait_form] = ele

# Customer selects from the list of regions
region = st.selectbox("Choose your membership:", options=list(mem_options.keys()))

# Update traitIndex based on the selected option
traitIndex = mem_options[region]

# Call trait price in wei for selected traitIndex
trait_price_wei = w3.toWei(contract.functions.getMembershipInfo(traitIndex).call()[1], 'wei')

# Convert price to ETH
trait_price_eth= w3.fromWei(trait_price_wei, 'ether') 

################################################################################
# Customer Inserts Shipping Information
################################################################################
st.markdown("### Add Your Shipping Information")

col1, col2 = st.columns([2,2])
first_name = col1.text_input("First Name") 
last_name = col2.text_input("Last Name")
street_address = st.text_input("Street Address")

col1,col2,col3 = st.columns([2,1,1])
city = col1.text_input("City")
state = col2.text_input("State")
zip_code = col3.text_input("ZIP Code")

################################################################################
# Minting Membership, Inserting Record into Database 
################################################################################

# Mint membership
if st.button("Purchase Membership"):
    try:
        # Use the contract to send a transaction to the mintMembership function
        tx_hash = contract.functions.mintMembership(
            address,
            traitIndex
        ).transact({'from': address, 'gas': 1000000, 'value': trait_price_wei})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        
        # Store other values for db insert
        tx_hash_value=receipt['transactionHash'].hex()
        traitIndex_value=traitIndex
        eth_price_value=trait_price_eth
        gas_cost_value= receipt['gasUsed']

        # Create postgres engine
        engine = create_engine("postgresql://postgres:postgres@localhost:5432/fintech_project_3")

        try:
            # Connect to database
            connection = psycopg2.connect(
                dbname="fintech_project_3",
                user="postgres",
                password="postgres",
                host="localhost",
                port=5432
            )

            cursor = connection.cursor()

            insert_query = """
            INSERT INTO customer_data (first_name, last_name, street_address, city, cust_state, zip_code, tx_hash, traitIndex, eth_price, gas_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            data_to_insert = (first_name, last_name, street_address, city, state, zip_code, tx_hash_value, traitIndex_value, eth_price_value, gas_cost_value)

            cursor.execute(insert_query, data_to_insert)
            connection.commit()
            
            print("Data inserted successfully.")
       
        except psycopg2.Error as e:
            connection.rollback()
            print("Error inserting data:", e)
        
        finally:
            cursor.close()
            connection.close()
        
        # Provide Purchase Confirmation to Customer 
        st.write(f"Purchase Complete!")
        st.markdown(f"Your membership entitles you to receive one bottle of wine per month from your selected region until the expiration of your membership one year from today.")

        st.markdown("---")
        st.write("Here is your receipt:")
        st.write(dict(receipt))
        
        
        # Update Customer Account Balance on Sidebar
        
        # Get wei balance, convert to eth, and round to two decimals
        wall_bal_new = float(round(w3.fromWei(w3.eth.get_balance(address), "ether"),2))
        # Write resulting wall_bal
        st.sidebar.write(f'Your account balance is now:  {wall_bal_new} ETH')
    
    except Exception as e:
        st.error(f"No more memberships of this type!")
        

###########################################################################
# Display Sidebar Images Below Customer Payment Selection Interface
########################################################################### 

st.sidebar.image("./images/wine1.png", use_column_width=True)
st.sidebar.image("./images/wine2.png", use_column_width=True)
st.sidebar.image("./images/wine5.png", use_column_width=True)