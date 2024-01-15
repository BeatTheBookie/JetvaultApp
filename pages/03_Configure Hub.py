import streamlit as st
import streamlit.components.v1 as components




#helper functions
from helper.JetvaultApp_helper import get_hub_load_config



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


st.title("Jetvault Hub Load Configuration")



with st.expander("Information"):
            

      st.markdown("""
            <p>
            
            bla bla
            
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



#get configuration
df_hub_load_config = get_hub_load_config()



with st.expander("Create new Hub load"):
     
      stage_schema = st.selectbox(
                        label = 'Stage Schema',
                        options = ('test', 'test')
                        )
     
      stage_table = st.selectbox(
                        label = 'Stage Table',
                        options = ('test', 'test')
                        )

      hub_schema = st.selectbox(
                        label = 'Hub Schema',
                        options = ('test', 'test')
                        )
     

      hub_name = st.text_input(
                        label = 'Hub Name'
                        )

      hub_alias = st.text_input(
                        label = 'Hub Alias'
                        )
     
      bk_columns = st.selectbox(
                        label = 'Hub Schema',
                        options = ('test', 'test')
                        )



# Display the result DataFrame using st.dataframe
st.dataframe(df_hub_load_config)