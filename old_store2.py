import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st



load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# The Load_Contract Function
################################################################################


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
# Register New Artwork
################################################################################
st.title("Purchase Your Wine Membership")
accounts = w3.eth.accounts
regions = ['Russian River Valley','Napa', 'Champagne', 'Somewhere']

# Use a Streamlit component to get the address of the artwork owner from the user
address = st.selectbox("Select Artwork Owner", options=accounts)
region = st.selectbox("Choose your region:", options=regions)


traitIndex = st.selectbox("Trait Index:", options=[0,1])

if st.button("Purchase Membership"):

    # Use the contract to send a transaction to the registerArtwork function
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
# Display a Token
################################################################################
#st.markdown("## Check Balance of an Account")
st.markdown("## Add Your Shipping Information")

st.text_input("First Name")
st.text_input("Last Name")
st.text_input("Address Line 1")
st.text_input("Address Line 2")
st.text_input("City")
st.text_input("State")
st.text_input("ZIP Code")






selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} tokens")

st.markdown("## Check  Ownership and Display Token")

total_token_supply = contract.functions.totalSupply().call()

token_id = st.selectbox("Artwork Tokens", list(range(total_token_supply)))

if st.button("Display"):
    st.write(f"Thanks for submitting your information and joining our club!")
    
#    # Get the art token owner
#    owner = contract.functions.ownerOf(token_id).call()
#    
#    st.write(f"The token is registered to {owner}")
#
#    # Get the art token's URI
#    token_uri = contract.functions.tokenURI(token_id).call()
#
#    st.write(f"The tokenURI is {token_uri}")
#    st.image(token_uri)
    


        