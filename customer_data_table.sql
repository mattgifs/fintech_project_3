DROP TABLE if exists customer_data;

CREATE TABLE customer_data(
	tx_id SERIAL PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	street_address VARCHAR,
	city VARCHAR,
	cust_state VARCHAR,
	zip_code INT,
	tx_hash VARCHAR,
	traitIndex INT,
	eth_price FLOAT,
	gas_cost INT
);

SELECT * from customer_data
