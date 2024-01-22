import streamlit as st
import streamlit.components.v1 as components
import pandas as pd



#helper functions
from helper.JetvaultApp_helper import make_grid
from helper.JetvaultApp_helper import get_all_db_schema
from helper.JetvaultApp_helper import get_tables_by_schema
from helper.JetvaultApp_helper import get_br_load_config
from helper.JetvaultApp_helper import push_br_load_config






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
df_br_config = get_br_load_config()



#build container and colum grid
side_grid = make_grid(1,2)


with side_grid[0][0]:

      with st.expander("Create new Business Rule load"):
           

           # Button to save connection info
            if st.button("Save Hub Load"):
                                   
                  
                  push_br_load_config(df_br_config)

                  st.success("Hub Load added successfully!")



with side_grid[0][1]:

      with st.expander("Delete Business Rule load"):


            # Button to save connection info
            if st.button("Delete Business Rule Load"):

                  # delete record in data frame
                  
                  
                  
                  try:
                        push_br_load_config(df_br_config)
                        st.success("Configuration successfully saved to database.")
                  except Exception as e:
                        st.error(f"Error saving configuration: {str(e)}")




# Display the result DataFrame using st.dataframe
st.dataframe(
            data = df_br_config,
            use_container_width = True
            )