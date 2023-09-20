# A New Way to Buy Wine
## Fintech Project 3
### Marlon Graves, Maksim Masharuev, Matt Gifford


## Project Idea
- Create a proof of concept for a wine club membership, where each membership is minted as an NFT
- Of available choices, a customer can choose to receive wine from a particular region
- The club member/NFT-holder would be entitled to receive one bottle of wine from that region per month for as long as they hold the NFT
- Build a wine collection that’s the  envy of all your friends 

## Concepts & Tools Used
- Solidity Smart Contracts (ERC721Full) & Remix IDE
- Ganache (for demo customer accounts)
- Metamask (to deploy contract) 
- Pandas
- Streamlit & Streamlit Plots
- SQL (SQLAlchemy, Psycopg2)
- Faker library (to generate fake customer info for demo purchases)

## Components & Repo Locations
- The Smart Contract
    - mem_token_v2.sol
    - Contract is deployed using Remix IDE
- The Store Interface
    - final_store.py
    - images used are located in /images/
    - This is the primary customer-facing "store" interface
    - The functionality present in the code for this interface includes:
        - customer imports and chooses from their accounts
        - checking those account balances
        - customer inputs shipping information
        - customer chooses their preferred region/membership option
        - Purchase button mints the NFT, inserts customer info to database, and updates the customer's account balance
- The Database
    - locally hosted on Matt's computer
    - schema file is customer_data_table.sql
- The Back Office Analytics Dashboard
    - dashboard.py
    - This code queries the database and displays different slices of information on the dashboard
    
## Things We Would Do If We Had More Time
- We used Ganache accounts as our demo customer accounts
    - We’d have to find a way to allow actual customers to connect their own blockchain wallets (e.g. MetaMask)
- Right now, all customer payments go to the contract address itself, as opposed to the contract owner’s address
    - Theoretically, the contract owner should be able to withdraw funds from the contract to their own account, but we were not able to find a way to make this work in time.
- Other functionality that should be added to the smart contract for a live version of this project:
    - More traits - region, varietal, specific winery, vintage, length of membership, price tier, etc. The more specific the customer’s selections can be, the more we can work to ensure authenticity of the wine. 
    - Membership expiration - paying once should not get the customer lifelong access
    - P2P Membership Transfers - one should be able to transfer their membership to another before its expiration


### Note to Future Self
This requires Ganache to be open, Metamask must be used to deploy the contract, and the abi and env files must be updated each time the contract is compiled and deployed.
