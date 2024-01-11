import streamlit as st
import streamlit.components.v1 as components




#helper functions
from helper.JetvaultApp_helper import get_stage_config
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

st.title("Jetvault Stage Schema Configuration")


with st.expander("Information"):
            

      st.markdown("""
            <p>
            
            For each stage schema, which should be used during the Data Vault configuration.
            Following loading types can be defined for each schema:
                  - DELTA:   new and changed records are loaded into the Data Vault tables
                  - FULL:    additionally adds a delete recognition to the loading process
                  - HISTORY: Stage tables contain a complate history inclusive the DWH_VALID_FROM column
            
            </p>
            """, unsafe_allow_html=True)
            


# only continue if sesssion state contains the connection information
if "snowflake_account" not in st.session_state or \
   "snowflake_user" not in st.session_state or \
   "snowflake_password" not in st.session_state or \
   "snowflake_database" not in st.session_state or \
   "snowflake_schema" not in st.session_state:
    st.error("No connection information. Please save Snowflake connection information first.")
    st.stop()



# Streamlit UI
st.title("Snowflake Data Editor")

df_stage_config = get_stage_config()
   
# Display the result DataFrame using st.dataframe
st.dataframe(df_stage_config)
