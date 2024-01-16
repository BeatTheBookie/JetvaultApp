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
if "snowflake_database" not in st.session_state:
    st.session_state.snowflake_database = ""
if "snowflake_warehouse" not in st.session_state:
    st.session_state.snowflake_warehouse = ""
if "snowflake_schema" not in st.session_state:
    st.session_state.snowflake_schema = ""



# Text inputs for Snowflake account, user, and password
st.subheader("Connection Details")
snowflake_account =     st.text_input("Snowflake Account", st.session_state.snowflake_account)
snowflake_user =        st.text_input("User", st.session_state.snowflake_user)
snowflake_password =    st.text_input("Password", st.session_state.snowflake_password, type="password")
snowflake_database =    st.text_input("Database", st.session_state.snowflake_database)
snowflake_warehouse =   st.text_input("Warehouse", st.session_state.snowflake_warehouse)
snowflake_schema =      st.text_input("Meta data schema", st.session_state.snowflake_schema)



# Button to save connection info
if st.button("Save Connection Info"):
    st.session_state.snowflake_account = snowflake_account
    st.session_state.snowflake_user = snowflake_user
    st.session_state.snowflake_password = snowflake_password
    st.session_state.snowflake_schema = snowflake_schema 
    st.session_state.snowflake_database = snowflake_database
    st.session_state.snowflake_warehouse = snowflake_warehouse
    st.success("Connection info saved!")



# Button to test connection
if st.button("Test Connection"):
    try:
        conn = snowflake.connector.connect(
            user=st.session_state.snowflake_user,
            password=st.session_state.snowflake_password,
            account=st.session_state.snowflake_account,
            warehouse = st.session_state.snowflake_warehouse,
            database=st.session_state.snowflake_database,
            schema=st.session_state.snowflake_schema
        )
        cursor = conn.cursor()
        st.success("Connection successful!")
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {str(e)}")