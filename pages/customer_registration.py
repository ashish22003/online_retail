from utility import ms,st
from menu import registration_menu, menu_with_redirect


menu_with_redirect()
# Verify the user's role
if st.session_state.role != "Customer":
    st.warning("You do not have permission to view this page.")
    st.stop()

# Initialize st.session_state.login_key to None
# st.session_state.login_key = None
if "login_key" not in st.session_state:
    st.session_state.login_key = None
st.session_state.input_choice = st.session_state.login_key

def set_key():
    # Callback function to save the role selection to Session State
    st.session_state.login_key = st.session_state.input_choice

def main():
    st.title("Customer Login")
    st.selectbox(
        "Welcome to Croma:",
        [None, "Login", "Register"],
        key="input_choice",
        on_change=set_key,
    )
    print( st.session_state )
    registration_menu()

if __name__ == "__main__":
    main()