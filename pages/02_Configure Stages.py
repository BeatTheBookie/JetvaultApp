import streamlit as st
import streamlit.components.v1 as components




#helper functions
from helper.JetvaultApp_helper import get_stage_config
from helper.JetvaultApp_helper import get_all_db_schema
from helper.JetvaultApp_helper import push_stage_config




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





#get configuration
df_stage_config = get_stage_config()

#get available db schemas
df_db_schema = get_all_db_schema()
lst_db_schema = df_db_schema['SCHEMA_NAME'].to_list()


   
# Display the result DataFrame using st.dataframe
df_stage_config = st.data_editor(df_stage_config,
                                    num_rows = "dynamic",
                                    column_config={
                                         "STAGE_SCHEMA": st.column_config.SelectboxColumn(
                                                "Stage Schema",
                                                help="Name of the stage schema",
                                                options=lst_db_schema,
                                                required=True
                                          ),
                                          "LOAD_TYPE": st.column_config.SelectboxColumn(
                                                "Load Type",
                                                help="Loading type for the stage schema",
                                                width="medium",
                                                options=[
                                                "DELTA",
                                                "FULL",
                                                "HISTORY",
                                                ],
                                                required=True,
                                          )}
                                    )


# Button to test connection
if st.button("Save configuration"):
      try:
            push_stage_config(df_stage_config)
            st.success("Configuration saved to database.")
      except Exception as e:
            st.error(f"Error saving configuration: {str(e)}")
      