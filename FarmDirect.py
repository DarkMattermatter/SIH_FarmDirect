# Import necessary libraries
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Set up database connection
engine = create_engine('sqlite:///farmdirect.db')

# Set up page configuration
st.set_page_config(page_title="FarmDirect", page_icon="🌾", layout="wide")

# Function to create database tables if they don't exist
def create_tables():
    with engine.connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS farmers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                location TEXT,
                description TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER,
                name TEXT,
                quantity REAL,
                price REAL,
                FOREIGN KEY(farmer_id) REFERENCES farmers(id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                buyer_name TEXT,
                status TEXT,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        ''')

# Initialize tables
create_tables()

# Farmer registration function
def farmer_registration():
    st.header("Farmer Registration")
    
    with st.form("register_form"):
        name = st.text_input("Farmer Name")
        phone = st.text_input("Phone Number")
        location = st.text_input("Farm Location")
        description = st.text_area("Description of Farm and Produce")
        submit = st.form_submit_button("Register")

        if submit:
            with engine.connect() as conn:
                conn.execute(
                    "INSERT INTO farmers (name, phone, location, description) VALUES (?, ?, ?, ?)",
                    (name, phone, location, description)
                )
            st.success("Registration Successful!")

# Product listing function
def product_listing():
    st.header("List Your Produce")
    
    with st.form("list_product_form"):
        farmer_id = st.number_input("Farmer ID", step=1)
        product_name = st.text_input("Product Name")
        quantity = st.number_input("Quantity (kg)")
        price = st.number_input("Price per kg ($)")
        submit = st.form_submit_button("List Product")

        if submit:
            with engine.connect() as conn:
                conn.execute(
                    "INSERT INTO products (farmer_id, name, quantity, price) VALUES (?, ?, ?, ?)",
                    (farmer_id, product_name, quantity, price)
                )
            st.success("Product listed successfully!")

# Display available products and enable negotiation
def display_products():
    st.header("Available Products")
    
    with engine.connect() as conn:
        df = pd.read_sql(
            "SELECT p.id, f.name as farmer_name, p.name, p.quantity, p.price FROM products p JOIN farmers f ON p.farmer_id = f.id",
            conn
        )
    st.dataframe(df)

    if not df.empty:
        selected_product = st.selectbox("Select Product to Buy", df["id"])
        if st.button("Contact Farmer"):
            st.info("Contact farmer to negotiate price.")

# Order management function (placeholder for expansion)
def manage_orders():
    st.header("Order Management")
    
    with engine.connect() as conn:
        orders_df = pd.read_sql("SELECT * FROM orders", conn)
    
    if orders_df.empty:
        st.write("No orders placed yet.")
    else:
        st.write(orders_df)
        st.write("Feature to update order status coming soon!")

# Main menu navigation logic
menu = ["Home", "Farmer Registration", "Product Listings", "Order Management", "Analytics", "Profile"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.title("Welcome to FarmDirect")
    st.write("Connecting farmers directly with consumers.")
    st.image("https://source.unsplash.com/1600x900/?farm,market,agriculture", caption="Empowering Farmers and Consumers")

elif choice == "Farmer Registration":
    farmer_registration()

elif choice == "Product Listings":
    product_listing()

elif choice == "Order Management":
    manage_orders()

elif choice == "Analytics":
    st.write("Coming Soon: Analytics dashboard for farmers and buyers.")

elif choice == "Profile":
    st.write("Profile management coming soon.")
