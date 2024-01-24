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



st.title("Jetvault Business Rule Load Configuration")



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

            #get a list of all available schemas
            df_db_schema = get_all_db_schema()

            #select box for stage schema
            br_schema = st.selectbox(
                              label = 'Business Rule Schema',
                              key = 'add_br_schema',
                              options = df_db_schema
                              )

            # get all tables inside the stage schema
            df_br_tables = get_tables_by_schema(br_schema)

            # select box for filtered tables
            br_table = st.selectbox(
                              label = 'BR Table',
                              key = 'add_br_table',
                              options = df_br_tables
                              )
            
            # hub schema selection based on schema list
            load_type = st.selectbox(
                              label = 'Loading Type',
                              key = 'add_load_type',
                              options = ['Business Rule Load','Access Layer Load']
                              )
            
            if load_type == 'Business Rule Load':
                  
                  #store loading type selection
                  br_stage_load = 1
                  access_layer_load = 0
            
                  #select box for business rule stage schema
                  br_stage_schema = st.selectbox(
                              label = 'Business Rule Stage Schema',
                              key = 'add_br_stage_schema',
                              options = df_db_schema
                              )
                  
                  #empty values for access layer laod
                  access_layer_schema = None
                  access_layer_object_name = None
                  access_layer_load_type = None
                  access_layer_matching_columns = None

            elif load_type == 'Access Layer Load':
                  
                  br_stage_load = 0
                  access_layer_load = 1

                  #select box for access layer schema
                  access_layer_schema = st.selectbox(
                              label = 'Acess Layer Schema',
                              key = 'add_access_layer_schema',
                              options = df_db_schema
                              )
                  

                  access_layer_object_name = st.text_input(
                                                      label = 'Access Layer Object Name',
                                                      key = 'add_access_layer_object_name'
                                                      )

                  access_layer_load_type = st.selectbox(
                                                label = 'Loading Type',
                                                key = 'add_access_layer_load_type',
                                                options = ['CTAS','CVAS']
                                                )
                  
                  access_layer_matching_columns = None

                  #empty values for br stage load
                  br_stage_schema = None

           # Button to save connection info
            if st.button("Save Business Rule Load"):


                  # add entry to data frame
                  new_br_records = [{'BUSINESS_RULE_SCHEMA' : br_schema,
                                    'BUSINESS_RULE_NAME' : br_table,
                                    'ACCESS_LAYER_LOAD' : access_layer_load,
                                    'ACCESS_LAYER_LOAD_TYPE' : access_layer_load_type,
                                    'ACCESS_LAYER_SCHEMA' : access_layer_schema,
                                    'ACCESS_LAYER_OBJECT_NAME' : access_layer_object_name,
                                    'ACCESS_LAYER_MATCHING_COLUMNS' : access_layer_matching_columns,
                                    'BR_STAGE_LOAD' : br_stage_load,
                                    'BR_STAGE_SCHEMA' : br_stage_schema
                                    }]

                  # add new hub load to data frame
                  df_br_config = pd.concat([df_br_config, pd.DataFrame(new_br_records)], ignore_index=True)
                                   
                  
                  push_br_load_config(df_br_config)

                  st.success("Business Rule Load added successfully!")



with side_grid[0][1]:

      with st.expander("Delete Business Rule load"):

            #get a list of all available schemas
            df_db_schema = get_all_db_schema()

            #select box for stage schema
            br_schema = st.selectbox(
                              label = 'Business Rule Schema',
                              key = 'delete_br_schema',
                              options = df_db_schema
                              )

            # get all tables inside the stage schema
            df_br_tables = get_tables_by_schema(br_schema)

            # select box for filtered tables
            br_table = st.selectbox(
                              label = 'Business Rule',
                              key = 'delete_br_table',
                              options = df_br_tables
                              )
            

            # Button to save connection info
            if st.button("Delete Business Rule Load"):

                  # delete record in data frame
                  # delete record in data frame
                  df_br_config = df_br_config[
                                          (df_br_config['BUSINESS_RULE_SCHEMA'] != br_schema) |
                                          (df_br_config['BUSINESS_RULE_NAME'] != br_table)                                          
                                          ]            
                  
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