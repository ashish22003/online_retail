from utility import st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("Home.py", label="Logout",icon="🏠")
    if st.session_state.role in ["Customer"]:
        st.sidebar.page_link("pages/customer_registration.py", label="Register/Login",icon="👤")
    if st.session_state.role in ["Admin"]:
        st.sidebar.page_link("pages/admin_homepage.py", label="Manage Database", icon="🔧")
 


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("Home.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("Home.py")
    menu()

def registration_menu():
 # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/customer_registration.py", label="Back",icon="⬅️")
    if st.session_state.login_key in ["Login"]:
        st.sidebar.page_link("pages/customer_login.py", label="Login",icon="🔑")
    if st.session_state.login_key in ["Register"]:
        st.sidebar.page_link("pages/customer_signup.py", label="Sign-up", icon="🆕")
 
def registration_menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "login_key" not in st.session_state or st.session_state.role is None:
        st.switch_page("pages/customer_registration.py")
    registration_menu()

