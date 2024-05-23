from utility import st, launch_connection, session_state
from menu import menu
import base64

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None

# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role

def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role


def main(db):
    st.set_page_config(page_title="Croma's Login Page")

    # Display welcome message and waving gif
    col1, col2 = st.columns([2,1])
    with col1:
        st.title("Welcome to Croma's Online Retail Store!")
    with col2:
        file_ = open("waving_hand.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" width="150">',
            unsafe_allow_html=True,
        )

     # Selectbox to choose role
    st.selectbox(
        "Select your role:",
        [None, "Customer", "Admin"],
        key="_role",
        on_change=set_role,
    )

    menu()  # Render the dynamic menu!

    
    # login_container = st.container()
    # with login_container:
    #     st.write("\n")
    #     st.write("\n")
    #     st.write("\n")  # Add additional line breaks for spacing
    #     st.markdown("<h2 style='font-family: Arial, sans-serif; font-size: 20px; font-weight: bold;'>How would you like to Login?</h2>", unsafe_allow_html=True)  # Decrease font size and stylize font
    #     st.write("\n")
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         f1 = st.button("Admin Login", key="admin_login_button", help="Login as Admin")
    #     with col2:
    #         f2 = st.button("Customer Login", key="customer_login_button", help="Login as Customer")
    #     st.write("\n")
    #     st.write("\n")
    #     st.write("\n")  # Add additional line breaks for spacing

    # # Center the buttons horizontally
    # col1, col2, col3 = st.columns([1, 2, 1])
    # with col1:
    #     st.write("")
    # with col2:
    #     pass  # This column will be the center
    # with col3:
    #     st.write("")

    # # Set session state based on button clicks
    # if f1:
    #     session_state.page = "admin"
    # elif f2:
    #     session_state.page = "customer"
    
    # if hasattr(session_state, "page"):
    #     if session_state.page == "admin":
    #         admin_login()
    #     elif session_state.page == "customer":
    #         customer_login_page()
    
if __name__ == "__main__":

    db = launch_connection()
    main(db)    
    db.close()
