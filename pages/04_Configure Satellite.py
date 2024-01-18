import streamlit as st
import streamlit.components.v1 as components
import pandas as pd




#helper functions
from helper.JetvaultApp_helper import make_grid
from helper.JetvaultApp_helper import get_sat_load_config
from helper.JetvaultApp_helper import get_all_db_schema
from helper.JetvaultApp_helper import get_columns_by_table
from helper.JetvaultApp_helper import get_hub_load_config
from helper.JetvaultApp_helper import push_sat_load_config


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

st.title("Jetvault Satellite Load Configuration")



with st.expander("Information"):
            

      st.markdown("""
            <p>
            
            The Satellite configuration page 
            
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
df_sat_load_config = get_sat_load_config()

# hub load config is also used, to get directly the reference to the existing hub load
df_hub_load_config = get_hub_load_config()



#build container and colum grid
side_grid = make_grid(1,2)



with side_grid[0][0]:

      with st.expander("Create new Satellite load"):

            #
            # create the whole object for a satellite load configuration
            #

            # select hub
            lst_hub_table = df_hub_load_config['HUB_NAME'].unique().tolist()

            hub_name  = st.selectbox(
                              label = 'Hub Name:',
                              key = 'add_hub_name',
                              options = lst_hub_table
                              )
            
            # select source for the hub
            filtered_hub_loads = df_hub_load_config[df_hub_load_config['HUB_NAME'] == hub_name]
            lst_stage_table = filtered_hub_loads['STAGE_TABLE'].unique().tolist()    

            stage_table = st.selectbox(
                              label = 'Stage Table:',
                              key = 'add_stage_table',
                              options = lst_stage_table
                              )       

            # manual input for satellite name
            sat_name = st.text_input(
                              label = 'Satellite Name',
                              key = 'add_sat_name'
                              )


            # attributes
            # get all columns for selected stage table
            stage_schema = filtered_hub_loads[filtered_hub_loads['STAGE_TABLE'] == stage_table]['STAGE_SCHEMA'][0]
            sat_schema = filtered_hub_loads[filtered_hub_loads['STAGE_TABLE'] == stage_table]['HUB_SCHEMA'][0]

            df_attribute_columns = get_columns_by_table(stage_schema, stage_table)


            # multi selection for business key columns of stage table
            attribute_columns = st.multiselect(
                              label = 'Attributes',
                              key = 'add_attirbute_columns',
                              options = df_attribute_columns
                              )


            # Button to save connection info
            if st.button("Save Satellite Load"):

                  # add entry to data frame
                  new_sat_records = [{'STAGE_SCHEMA' : stage_schema,
                                    'STAGE_TABLE' : stage_table,
                                    'SAT_SCHEMA' : sat_schema,
                                    'SAT_NAME' : sat_name,                                    
                                    'REFERENCED_OBJECT_NAME' : hub_name,                                    
                                    'ATTRIBUTES' : ','.join(attribute_columns)
                                    }]
                  
                  # add new hub load to data frame
                  df_sat_load_config = pd.concat([df_sat_load_config, pd.DataFrame(new_sat_records)], ignore_index=True)


                  push_sat_load_config(df_sat_load_config)

                  
                  st.success("Satellite Load added successfully!")



with side_grid[0][1]:

      with st.expander("Delete Satellite load"):

            #
            # drop object from a hub configuration
            #


            # select satellite
            lst_sat_table = df_sat_load_config['SAT_NAME'].unique().tolist()


            #select box for sat name
            sat_name = st.selectbox(
                              label = 'Satellite Name:',
                              key = 'delete_sat_name',
                              options = lst_sat_table
                              )


            # Button to save connection info
            if st.button("Delete Satellite Load"):

                  # delete record in data frame
                  df_sat_load_config = df_sat_load_config[
                                                (df_sat_load_config['SAT_NAME'] != sat_name)
                                                ]


                  try:
                        push_sat_load_config(df_sat_load_config)
                        st.success("Configuration successfully saved to database.")
                  except Exception as e:
                        st.error(f"Error saving configuration: {str(e)}")




# Display the result DataFrame using st.dataframe
st.dataframe(
            data = df_sat_load_config,
            use_container_width = True
            )
