import streamlit as st
import snowflake.connector





#helper functions
#from helper.BTB_app_helper import get_authenticater_config
#from helper.BTB_app_helper import make_grid



st.set_page_config(
         layout="wide",
         page_title="Jetvault App",
         #page_icon="images/BeatTheBookie-Logo.jpg",
         initial_sidebar_state ="expanded"
               )




#
# variable declaration
#



#
# function definitions
#

def save_connection_info():
    st.session_state.snowflake_account = st.text_input("Snowflake Account", key="snowflake_account_key")
    st.session_state.snowflake_user = st.text_input("User", key="snowflake_user_key")
    st.session_state.snowflake_password = st.text_input("Password", type="password", key="snowflake_password_key")
    st.success("Connection info saved!")



def test_connection():
    try:
        conn = snowflake.connector.connect(
            user=st.session_state.snowflake_user,
            password=st.session_state.snowflake_password,
            account=st.session_state.snowflake_account,
            #warehouse='your_warehouse',
            #database='your_database',
            schema='META'
        )
        cursor = conn.cursor()
        st.success("Connection successful!")
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {str(e)}")



# build config for authenticator
# -> not needed here

# 
# side bar configuration
# -> no sidebar

#
# tab definition
# -> no tabs




#
# content
# 

# Streamlit UI
st.title("Snowflake Connection Manager")


with st.expander("Information"):
            

            st.markdown("""
                  <p>
                  Configuring the connection to your Snowflake instance is the first step in working with the Jetvault App.
                  This is needed before continuing with the next steps.
                  
                  </p>
                  """, unsafe_allow_html=True)


# get existing session variables
if "snowflake_account" not in st.session_state:
    st.session_state.snowflake_account = ""
if "snowflake_user" not in st.session_state:
    st.session_state.snowflake_user = ""
if "snowflake_password" not in st.session_state:
    st.session_state.snowflake_password = ""



# Text inputs for Snowflake account, user, and password
st.subheader("Connection Details")
snowflake_account = st.text_input("Snowflake Account", st.session_state.snowflake_account, key="snowflake_account_key")
snowflake_user = st.text_input("User", st.session_state.snowflake_user, key="snowflake_user_key")
snowflake_password = st.text_input("Password", st.session_state.snowflake_password, type="password", key="snowflake_password_key")



# Button to save connection info
if st.button("Save Connection Info"):
    save_connection_info()



# Button to test connection
if st.button("Test Connection"):
    test_connection()