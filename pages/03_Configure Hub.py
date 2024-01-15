import streamlit as st
import streamlit.components.v1 as components




#helper functions
from helper.JetvaultApp_helper import get_hub_load_config
from helper.JetvaultApp_helper import get_all_db_schema
from helper.JetvaultApp_helper import get_tables_by_schema
from helper.JetvaultApp_helper import get_columns_by_table


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

      #
      # create the whole object for a hub configuration
      #

      df_db_schema = get_all_db_schema()
     
      stage_schema = st.selectbox(
                        label = 'Stage Schema',
                        options = df_db_schema
                        )
      
      df_stage_tables = get_tables_by_schema(stage_schema)

     
      stage_table = st.selectbox(
                        label = 'Stage Table',
                        options = df_stage_tables
                        )

      hub_schema = st.selectbox(
                        label = 'Hub Schema',
                        options = df_db_schema
                        )
     
      hub_name = st.text_input(
                        label = 'Hub Name'
                        )

      hub_alias = st.text_input(
                        label = 'Hub Alias'
                        )
      
      df_bk_columns = get_columns_by_table(stage_schema, stage_table)
     
      bk_columns = st.multiselect(
                        label = 'Business Key',
                        options = df_bk_columns
                        )


      # Button to save connection info
      if st.button("Save Hub Load"):
            st.success("Hub Load added successfully!")


# Display the result DataFrame using st.dataframe
st.dataframe(df_hub_load_config)