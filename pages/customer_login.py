from utility import st,launch_connection
from menu import registration_menu_with_redirect
mc = launch_connection()
cur = mc.cursor()

registration_menu_with_redirect()
if st.session_state.login_key not in ["Login"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

def customer_login_page():
    # cur=mc.cursor()
    st.header("Customer Login")
    selected_method = st.radio("Choose Login Method:", ["Email", "Phone Number"], key="login_method_key")

    # Input fields based on selected method
    if selected_method == "Email":
        placeholder = "Enter your email address"
    elif selected_method == "Phone Number":
        placeholder = "Enter your phone number"

    inp = st.text_input(placeholder)
    password = st.text_input("Enter your password", type="password")
    
    if "incorrect_attempts" not in st.session_state:
        st.session_state.incorrect_attempts = 0
    
    # Check if the user has made more than 3 incorrect attempts
    if st.session_state.incorrect_attempts >= 3:
        st.warning("You have exceeded the maximum number of login attempts.")
        st.stop()  # Stop further execution of the function
    
    if "record_details" not in st.session_state:
        st.session_state.record_details = None

    
    # Login button
    if st.button("Login"):
        # Add your login logic here
        if inp and password:
            if selected_method == "Email":
                cur.execute("SELECT * from Customer WHERE Email_ID = %s", (inp,))
            elif selected_method == "Phone Number":
                # Add logic for phone number login
                cur.execute("SELECT * from Customer WHERE Contact_Number= %s", (inp,))

            record = cur.fetchall()
            
            if record and record[0][5] == password:
                st.success("Login successful!")
                st.session_state.record_details = record[0]
                st.switch_page("pages/customer_homepage.py")
            else:
                st.session_state.incorrect_attempts += 1
                st.error("Invalid username or password")
if __name__ == "__main__":
    customer_login_page()