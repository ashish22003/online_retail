from utility import st, launch_connection
from menu import registration_menu_with_redirect

mc = launch_connection()
cur = mc.cursor()

if "record_details" not in st.session_state :
    st.session_state.record_details = None 

registration_menu_with_redirect()
if st.session_state.login_key not in ["Register"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

def main():
    st.header("Customer Signup")
    
    # Input fields for customer details
    first_name = st.text_input("First Name")
    middle_name = st.text_input("Middle Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email-ID")
    contact_number = st.text_input("Contact Number")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    payment_mode = st.selectbox("Payment Mode", ["Cash", "Credit Card", "Debit Card", "Net Banking"])

    # Address details
    st.subheader("Address Details")
    address_type = st.radio("Address Type", ["Home", "Work", "Other"])
    house_no = st.text_input("House No")
    street = st.text_input("Street")
    area = st.text_input("Area")
    city = st.text_input("City")
    state = st.text_input("State")
    pincode = st.text_input("Pincode")

    if st.button("Signup"):
        # Check if passwords match
        if password != confirm_password:
            st.error("Passwords do not match")
            return

        # Check if email and contact number are unique
        cur.execute("SELECT * FROM customer WHERE Email_ID = %s", (email,))
        if cur.fetchone():
            st.error("Email already exists. Please use a different email.")
            return

        cur.execute("SELECT * FROM customer WHERE Contact_Number = %s", (contact_number,))
        if cur.fetchone():
            st.error("Contact number already exists. Please use a different number.")
            return

        try:
            # Insert into the customer table
            cur.execute("""
                INSERT INTO customer (First_Name, Middle_Name, Last_Name, Email_ID, Password, Contact_Number, Payment_Mode)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (first_name, middle_name, last_name, email, password, contact_number, payment_mode))

            # Commit changes to the database
            mc.commit()

            # Retrieve customer record
            cur.execute("SELECT * FROM customer WHERE Email_ID = %s", (email,))
            customer_record = cur.fetchone()

            # Insert into the addresses table
            cur.execute("""
                INSERT INTO addresses (Customer_ID, Address_Type, House_No, Street, Area, City, State, Pincode, Contact_Number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (customer_record[0], address_type, house_no, street, area, city, state, pincode, contact_number))

            # Commit changes to the database
            mc.commit()

            st.success("Signup successful!")
            st.session_state.record_details = customer_record
            st.switch_page("pages/customer_homepage.py")
        except Exception as e:
            st.error(f"An error occurred: {e}")
if __name__ == "__main__":
    main()
