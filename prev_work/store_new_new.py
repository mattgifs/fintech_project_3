import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
load_dotenv()


###########################################################################
# Display Banner Images on Streamlit Customer Portal
########################################################################### 
    
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


################################################################################
# Register New Artwork
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

# Write traitIndex (mostly for debugging)
# st.write(f"Selected Membership: {traitIndex}")



# Mint membership
if st.button("Purchase Membership"):
    try:
        # Use the contract to send a transaction to the mintMembership function
        tx_hash = contract.functions.mintMembership(
            address,
            traitIndex
        ).transact({'from': address, 'gas': 1000000, 'value': trait_price_wei})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write(f"Purchase Complete!")
        st.markdown(f"Your membership entitles you to receive one bottle of wine from your selected region until the expiration of your membership one year from today.")
        st.markdown(f"Don't forget to add your shipping information below so we know where to send your wine!")
        st.markdown("---")
        st.write("Here is your receipt:")
        st.write(dict(receipt))
        
        # Get wei balance, convert to eth, and round to two decimals
        wall_bal_new = float(round(w3.fromWei(w3.eth.get_balance(address), "ether"),2))
        # Write resulting wall_bal
        st.sidebar.write(f'Your account balance is now:  {wall_bal_new} ETH')
    
    except Exception as e:
        st.error(f"No more memberships of this type!")
        
st.markdown("---")

################################################################################
# Back Office
################################################################################
# Insert shipping address to database/dataframe
st.markdown("## Add Your Shipping Information")

col1, col2 = st.columns([2,2])
col1.text_input("First Name") 
col2.text_input("Last Name")
st.text_input("Street Address")
col1,col2,col3 = st.columns([2,1,1])
col1.text_input("City")
col2.text_input("State")
col3.text_input("ZIP Code")

if st.button("Add Your Info"):
    st.write(f"Thanks for submitting your information and joining our club!")
    

################################################################################
# Display sidebar images
################################################################################

# Display a local image
st.sidebar.image("./images/wine1.png", use_column_width=True)
st.sidebar.image("./images/wine2.png", use_column_width=True)
st.sidebar.image("./images/wine5.png", use_column_width=True)
       

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





