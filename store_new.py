import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
load_dotenv()


###########################################################################
# Display Images on Streamlit Customer Portal
###########################################################################

# Display a local image
st.sidebar.image("./images/wine1.png", use_column_width=True)
st.sidebar.image("./images/wine2.png", use_column_width=True)
st.sidebar.image("./images/wine5.png", use_column_width=True)
    
    
# Create six columns
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Display images in columns
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
    try:
        # Use the contract to send a transaction to the mintMembership function
        tx_hash = contract.functions.mintMembership(
        address,
        traitIndex
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
        st.write(f"Purchase Complete!")
    except Exception as e:
        st.error(f"No more memberships of this type!")
        
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

    
# Open the images you want to stack
# image1 = Image.open("image1/wine1.png")
# image2 = Image.open("image2/wine2.png")


# # # Get the dimensions of the images
# width1, height1 = image1.size
# width2, height2 = image2.size

# # Calculate the total width and height for the new image
# total_width = max(width1, width2)
# total_height = height1 + height2


# # Create a new image with the calculated dimensions and a white background
# new_image = Image.new("RGB", (total_width, total_height), (255, 255, 255))

# # Paste the first image at the top of the new image
# new_image.paste(image1, (0, 0))

# # Paste the second image below the first image
# new_image.paste(image2, (0, height1))


# # Save or display the vertically stacked image
# new_image.save("stacked_image.png")
# new_image.show()
# In this script:

# We open the two images you want to vertically stack using the Pillow library.

# We get the dimensions (width and height) of each image.

# We calculate the total width and height needed for the new image, ensuring it's wide enough to accommodate both images vertically.

# We create a new image with the calculated dimensions and set it to have a white background.

# We paste the first image at the top of the new image (at position (0, 0)).

# We paste the second image below the first image (at position (0, height1)).

# Finally, we can save the vertically stacked image to a file and display it using .show().

# Make sure to replace "image1.png" and "image2.png" with the actual file paths of the images you want to stack. This script will create a new image ("stacked_image.png") that vertically stacks the two input images.





