import streamlit as st
import streamlit.components.v1 as components
import pandas as pd



#helper functions
from helper.JetvaultApp_helper import get_stage_config
from helper.JetvaultApp_helper import get_all_db_schema
from helper.JetvaultApp_helper import push_stage_config
from helper.JetvaultApp_helper import make_grid



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


#build container and colum grid
side_grid = make_grid(1,2)



with side_grid[0][0]:

      with st.expander("Add Stage Config:"):

            #
            # create the whole object for a stage configuration
            #

            
            #select box for stage schema
            stage_schema = st.selectbox(
                              label = 'Stage Schema',
                              options = df_db_schema
                              )


            #select box for stage schema
            load_type = st.selectbox(
                              label = 'Load Type:',
                              options=[
                                    "DELTA",
                                    "FULL",
                                    "HISTORY",
                                    ]
                              )
            

            # Button to save connection info
            if st.button("Save Stage Configuration"):
                  
                  # add entry to data frame
                  new_config_record = [{'STAGE_SCHEMA' : stage_schema,
                                    'LOAD_TYPE' : load_type
                                    }]
                  
                  # add new hub load to data frame
                  df_stage_config = pd.concat([df_stage_config, pd.DataFrame(new_config_record)], ignore_index=True)

                  try:
                        push_stage_config(df_stage_config)
                        st.success("Configuration successfully saved to database.")
                  except Exception as e:
                        st.error(f"Error saving configuration: {str(e)}")



with side_grid[0][1]:

      with st.expander("Delete Stage Config"):

            #
            # drop object from a stage configuration
            #

            #select box for stage schema
            stage_schema = st.selectbox(
                              label = 'Stage Schema',
                              options = df_db_schema
                              )
            

             # Button to save connection info
            if st.button("Delete Stage Configuration"):

                  # delete record in data frame
                  df_stage_config = df_stage_config[df_stage_config['STAGE_SCHJEMA'] == stage_schema]
                  
                  try:
                        push_stage_config(df_stage_config)
                        st.success("Configuration successfully saved to database.")
                  except Exception as e:
                        st.error(f"Error saving configuration: {str(e)}")





# Display the result DataFrame using st.dataframe
st.dataframe(
            data = df_stage_config,
            use_container_width = True
            )
   


      