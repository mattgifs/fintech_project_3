import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

###########################################################################
# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

############################################################################ The Load_Contract Function
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

###########################################################################
# Define a Python class to represent the Trait struct
###########################################################################
class Trait:
    def __init__(self, name, value, maxSupply, mintedCount):
        self.name = name
        self.value = value
        self.maxSupply = maxSupply
        self.mintedCount = mintedCount

################################################################################
# Register New Artwork
################################################################################
st.title("Purchase Your Wine Membership")

# Load ganache accounts
accounts = w3.eth.accounts

# Customer select from ganache accounts
address = st.selectbox("Select Your Account", options=accounts)

# Define a list of regions (for mockup, replace with contract data)
regions = ['Russian River Valley', 'Napa', 'Champagne', 'Somewhere']

# Customer select from the list of regions
region = st.selectbox("Choose your region:", options=regions)

# Customer selects a trait index (replace with actual trait index options)
traitIndex = st.selectbox("Trait Index:", options=[0, 1])

# Get the trait data for the selected traitIndex
if st.button("Get Trait"):
    selected_trait_index = traitIndex  # Replace this with the selected trait index
    try:
        trait_data = contract.functions.getMembershipInfo(selected_trait_index).call()
        name, value, maxSupply, mintedCount = trait_data
        trait = Trait(name, value, maxSupply, mintedCount)
        st.write("Trait Data:")
        st.write(f"Name: {trait.name}")
        st.write(f"Value: {trait.value}")
        st.write(f"Max Supply: {trait.maxSupply}")
        st.write(f"Spots Remaining: {trait.maxSupply - trait.mintedCount}")
    except Exception as e:
        st.error(f"Error fetching trait data: {str(e)}")

# Mint membership
if st.button("Purchase Membership"):
    # Use the contract to send a transaction to the mintMembership function
    tx_hash = contract.functions.mintMembership(
        address,
        traitIndex
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write(f"Purchase Complete!")

st.markdown("---")

################################################################################
# Back Office
################################################################################
# Insert shipping address to database/dataframe
st.markdown("## Add Your Shipping Information")

st.text_input("First Name")
st.text_input("Last Name")
st.text_input("Address Line 1")
st.text_input("Address Line 2")
st.text_input("City")
st.text_input("State")
st.text_input("ZIP Code")

if st.button("Display"):
    st.write(f"Thanks for submitting your information and joining our club!")
