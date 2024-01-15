import streamlit as st
import streamlit.components.v1 as components
import pandas as pd




#helper functions
from helper.JetvaultApp_helper import get_hub_load_config
from helper.JetvaultApp_helper import get_all_db_schema
from helper.JetvaultApp_helper import get_tables_by_schema
from helper.JetvaultApp_helper import get_columns_by_table
from helper.JetvaultApp_helper import push_hub_load_config


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

      #get a list of all available schemas
      df_db_schema = get_all_db_schema()
      
      #select box for stage schema
      stage_schema = st.selectbox(
                        label = 'Stage Schema',
                        options = df_db_schema
                        )
      
      # get all tables inside the stage schema
      df_stage_tables = get_tables_by_schema(stage_schema)

      # select box for filtered tables
      stage_table = st.selectbox(
                        label = 'Stage Table',
                        options = df_stage_tables
                        )
      
      # hub schema selection based on schema list
      hub_schema = st.selectbox(
                        label = 'Hub Schema',
                        options = df_db_schema
                        )
     
      # manual input for hub name
      hub_name = st.text_input(
                        label = 'Hub Name'
                        )

      # manual input for hub alias
      hub_alias = st.text_input(
                        label = 'Hub Alias'
                        )
      
      # get all columns for selected stage table
      df_bk_columns = get_columns_by_table(stage_schema, stage_table)
     
      # multi selection for business key columns of stage table
      bk_columns = st.multiselect(
                        label = 'Business Key',
                        options = df_bk_columns
                        )
      

      st.write(bk_columns)


      # Button to save connection info
      if st.button("Save Hub Load"):

            # add entry to data frame
            new_hub_records = [
                              {'STAGE_SCHEMA' : stage_schema},
                              {'STAGE_TABLE' : stage_table},
                              {'HUB_SCHEMA' : hub_schema},
                              {'HUB_NAME' : hub_name},
                              {'HUB_ALIAS' : hub_alias},
                              #{'BK_SOURCE_COLUMN_LIST' : bk_columns}]
                              {'BK_SOURCE_COLUMN_LIST' : ','.join(bk_columns)}
                              ]
            
            # add new hub load to data frame
            df_hub_load_config = pd.concat([df_hub_load_config, pd.DataFrame(new_hub_records)], ignore_index=True)
            
            push_hub_load_config(df_hub_load_config)

            st.success("Hub Load added successfully!")


# Display the result DataFrame using st.dataframe
st.dataframe(df_hub_load_config)