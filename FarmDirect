# Import necessary libraries
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import hashlib

# Set up database connection
engine = create_engine('sqlite:///farmdirect.db')

# Set up page configuration
st.set_page_config(page_title="FarmDirect", page_icon="🌾", layout="wide")

# Function to create database tables if they don't exist
def create_tables():
    with engine.connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS farmers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                phone TEXT,
                location TEXT,
                description TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
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
                buyer_id INTEGER,
                status TEXT,
                FOREIGN KEY(product_id) REFERENCES products(id),
                FOREIGN KEY(buyer_id) REFERENCES users(id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                sender_id INTEGER,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(order_id) REFERENCES orders(id),
                FOREIGN KEY(sender_id) REFERENCES users(id)
            )
        ''')

# Initialize tables
create_tables()

# Hash passwords for basic authentication
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check login credentials
def login_user(username, password):
    hashed_password = hash_password(password)
    with engine.connect() as conn:
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password)).fetchone()
    return user

# Function to register a new user
def register_user(username, password, role):
    with engine.connect() as conn:
        try:
            conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hash_password(password), role))
            st.success("User registered successfully!")
        except Exception as e:
            st.error(f"Error registering user: {e}")

# Authentication and user role selection
def user_auth():
    st.sidebar.subheader("Login or Register")
    choice = st.sidebar.radio("Select Action", ["Login", "Register"])
    
    if choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.sidebar.success(f"Welcome, {user['username']}!")
            else:
                st.sidebar.error("Invalid credentials!")
    
    elif choice == "Register":
        username = st.sidebar.text_input("New Username")
        password = st.sidebar.text_input("New Password", type="password")
        role = st.sidebar.selectbox("Role", ["Farmer", "Buyer"])
        if st.sidebar.button("Register"):
            register_user(username, password, role.lower())

# Farmer registration function
def farmer_registration():
    st.header("Farmer Registration")
    
    if st.session_state['user']['role'] != 'farmer':
        st.error("Only farmers can register farms.")
        return

    with st.form("register_form"):
        name = st.text_input("Farmer Name")
        phone = st.text_input("Phone Number")
        location = st.text_input("Farm Location")
        description = st.text_area("Description of Farm and Produce")
        submit = st.form_submit_button("Register Farm")

        if submit:
            user_id = st.session_state['user']['id']
            with engine.connect() as conn:
                conn.execute(
                    "INSERT INTO farmers (user_id, name, phone, location, description) VALUES (?, ?, ?, ?, ?)",
                    (user_id, name, phone, location, description)
                )
            st.success("Farm registered successfully!")

# Product listing function
def product_listing():
    st.header("List Your Produce")

    farmer_id = st.session_state['user']['id']  # Assume user is logged in as a farmer
    with st.form("list_product_form"):
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

# Order management function
def manage_orders():
    st.header("Order Management")

    with engine.connect() as conn:
        orders_df = pd.read_sql("SELECT * FROM orders", conn)

    if orders_df.empty:
        st.write("No orders placed yet.")
    else:
        st.write(orders_df)
        st.write("Feature to update order status coming soon!")

# Analytics dashboard function
def analytics_dashboard():
    st.header("Sales Analytics")
    
    with engine.connect() as conn:
        sales_data = pd.read_sql(
            "SELECT p.name, SUM(o.quantity) as total_sold FROM products p JOIN orders o ON p.id = o.product_id GROUP BY p.name",
            conn
        )
    st.bar_chart(sales_data.set_index('name'))

# Main menu navigation logic
def main():
    st.sidebar.title("FarmDirect Navigation")
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user'] = None

    if not st.session_state['logged_in']:
        user_auth()
    else:
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
            analytics_dashboard()

        elif choice == "Profile":
            st.write("Profile management coming soon.")

if __name__ == "__main__":
    main()
