import streamlit as st
import streamlit.components.v1 as components
import pandas as pd



#helper functions
from helper.JetvaultApp_helper import get_link_load_config
from helper.JetvaultApp_helper import get_all_db_schema
from helper.JetvaultApp_helper import get_tables_by_schema
from helper.JetvaultApp_helper import get_hub_load_config
from helper.JetvaultApp_helper import make_grid
from helper.JetvaultApp_helper import push_link_load_config


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

st.title("Jetvault Link Load Configuration")



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
df_link_load_config = get_link_load_config()




#build container and colum grid
side_grid = make_grid(1,2)


with side_grid[0][0]:

      with st.expander("Create new Link load"):
            
            #
            # create the whole object for a hub configuration
            #

            #get a list of all available schemas
            df_db_schema = get_all_db_schema()

            #select box for stage schema
            stage_schema = st.selectbox(
                              label = 'Stage Schema',
                              key = 'add_stage_schema',
                              options = df_db_schema
                              )

            # get all tables inside the stage schema
            df_stage_tables = get_tables_by_schema(stage_schema)

            # select box for filtered tables
            stage_table = st.selectbox(
                              label = 'Stage Table',
                              key = 'add_stage_table',
                              options = df_stage_tables
                              )
            
            # filter available hub loads for stage table
            # select source for the hub
            filtered_hub_loads = df_hub_load_config[
                                                      (df_hub_load_config['STAGE_SCHEMA'] == stage_schema) &
                                                      (df_hub_load_config['STAGE_TABLE'] == stage_table)
                                                      ]

            lst_hub = filtered_hub_loads['HUB_NAME'].unique().tolist() 

            if not lst_hub:
                  link_schema = None
            else:
                  link_schema = filtered_hub_loads[filtered_hub_loads['STAGE_TABLE'] == stage_table]['HUB_SCHEMA'].unique().tolist()[0]

            
            # select box for filtered tables
            hub_table_1 = st.selectbox(
                              label = 'Hub Load 1',
                              key = 'add_hub_load_1',
                              options = lst_hub
                              )
            
            # select box for filtered tables
            hub_table_2 = st.selectbox(
                              label = 'Hub Load 2',
                              key = 'add_hub_load_2',
                              options = lst_hub
                              )
            

            # naming for link and link hash key
            link_name = st.text_input(
                              label = 'Link Name',
                              key = 'add_link_name'
                              )

            # naming for link and link hash key
            link_hk = st.text_input(
                              label = 'Link Hash Key',
                              key = 'add_link_hk'
                              )
            

            # Button to save connection info
            if st.button("Save Link Load"):
                  
                  # add entry to data frame
                  new_link_records = [{'STAGE_SCHEMA' : stage_schema,
                                    'STAGE_TABLE' : stage_table,
                                    'LINK_SCHEMA' : link_schema,
                                    'LINK_NAME' : link_name,
                                    'L_COLUMN_NAME' : link_hk,
                                    'REFERENCED_HUB_NAME_1' : hub_table_1,
                                    'REFERENCED_HUB_NAME_2' : hub_table_2                                    
                                    }]
                  
                  # add new hub load to data frame
                  df_link_load_config = pd.concat([df_link_load_config, pd.DataFrame(new_link_records)], ignore_index=True)
                  
                  try:
                        push_link_load_config(df_link_load_config)
                        st.success("Link Load added successfully!")
                  except Exception as e:
                        st.error(f"Error saving configuration: {str(e)}")              

                  


with side_grid[0][1]:

      with st.expander("Delete Link load"):

            #
            # drop object from a hub configuration
            #

            lst_links = df_link_load_config['LINK_NAME'].unique().tolist() 
            

            #select box for sat name
            link_name = st.selectbox(
                              label = 'Link Name:',
                              key = 'delete_sat_name',
                              options = lst_links
                              )


            # Button to save connection info
            if st.button("Delete Link Load"):

                  # delete record in data frame
                  df_link_load_config = df_link_load_config[
                                                (df_link_load_config['LINK_NAME'] != link_name)
                                                ]

                  try:
                        push_link_load_config(df_link_load_config)
                        st.success("Configuration successfully saved to database.")
                  except Exception as e:
                        st.error(f"Error saving configuration: {str(e)}")




# Display the result DataFrame using st.dataframe
st.dataframe(
            data = df_link_load_config,
            use_container_width = True
            )