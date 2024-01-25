import streamlit as st
import streamlit.components.v1 as components
import pandas as pd




#helper functions
from helper.JetvaultApp_helper import get_hub_load_config
from helper.JetvaultApp_helper import get_all_db_schema
from helper.JetvaultApp_helper import get_tables_by_schema
from helper.JetvaultApp_helper import get_columns_by_table
from helper.JetvaultApp_helper import push_hub_load_config
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


#build container and colum grid
side_grid = make_grid(1,2)


with side_grid[0][0]:

      with st.expander("Create new Hub load"):

            #
            # create the whole object for a hub configuration
            #

            #get a list of all available schemas
            df_db_schema = get_all_db_schema()
            
            #select box for stage schema
            stage_schema = st.selectbox(
                              label = 'Stage Schema',
                              key = 'add_stage_schema',
                              options = df_db_schema,
                              index = 9
                              )
            
            # get all tables inside the stage schema
            df_stage_tables = get_tables_by_schema(stage_schema)

            if df_stage_tables is not None:

                  # select box for filtered tables
                  stage_table = st.selectbox(
                                    label = 'Stage Table',
                                    key = 'add_stage_table',
                                    options = df_stage_tables
                                    )
            
            else:
                  stage_table = None
            
            st.write('test:',stage_table)
            
            # hub schema selection based on schema list
            hub_schema = st.selectbox(
                              label = 'Hub Schema',
                              key = 'add_hub_schema',
                              options = df_db_schema
                              )
      
            # manual input for hub name
            hub_name = st.text_input(
                              label = 'Hub Name',
                              key = 'add_hub_name'
                              )

            # manual input for hub alias
            hub_alias = st.text_input(
                              label = 'Hub Alias',
                              key = 'add_hub_alias'
                              )

            if hub_alias == "":
                  hub_alias = None


            if stage_table is not None:
            
                  # get all columns for selected stage table
                  df_bk_columns = get_columns_by_table(stage_schema, stage_table)

            else:
                  df_bk_columns = None

            
            # multi selection for business key columns of stage table

            bk_columns = st.multiselect(
                              label = 'Business Key',
                              key = 'add_bk_columns',
                              options = df_bk_columns
                              )
      

            # Button to save connection info
            if st.button("Save Hub Load"):

                  # add entry to data frame
                  new_hub_records = [{'STAGE_SCHEMA' : stage_schema,
                                    'STAGE_TABLE' : stage_table,
                                    'HUB_SCHEMA' : hub_schema,
                                    'HUB_NAME' : hub_name,
                                    'HUB_ALIAS' : hub_alias,
                                    #{'BK_SOURCE_COLUMN_LIST' : bk_columns}]
                                    'BK_SOURCE_COLUMN_LIST' : ','.join(bk_columns)
                                    }]
                  
                  # add new hub load to data frame
                  df_hub_load_config = pd.concat([df_hub_load_config, pd.DataFrame(new_hub_records)], ignore_index=True)
                  
                  push_hub_load_config(df_hub_load_config)

                  st.success("Hub Load added successfully!")

with side_grid[0][1]:

      with st.expander("Delete Hub load"):
            

            #
            # drop object from a hub configuration
            #

            #select box for stage schema
            stage_schema = st.selectbox(
                              label = 'Stage Schema:',
                              key = 'delete_stage_schema',
                              options = df_hub_load_config['STAGE_SCHEMA'].unique().tolist()
                              )
            
            filterd_stage_schema_df = df_hub_load_config[df_hub_load_config['STAGE_SCHEMA'] == stage_schema]
            lst_stage_table = filterd_stage_schema_df['STAGE_TABLE'].unique().tolist()

            
            stage_table = st.selectbox(
                              label = 'Stage Table:',
                              key = 'delete_stage_table',
                              options = lst_stage_table
                              )
            

            filtered_stage_table_df = filterd_stage_schema_df[(filterd_stage_schema_df['STAGE_TABLE'] == stage_table)]
            lst_hub_name = filtered_stage_table_df['HUB_NAME'].unique().tolist()


            hub_name = st.selectbox(
                              label = 'Hub Name:',
                              key = 'delete_hub_name',
                              options = lst_hub_name
                              )


            # Button to save connection info
            if st.button("Delete Hub Load"):

                  # delete record in data frame
                  df_hub_load_config = df_hub_load_config[
                                                (df_hub_load_config['STAGE_SCHEMA'] != stage_schema) |
                                                (df_hub_load_config['STAGE_TABLE'] != stage_table) |
                                                (df_hub_load_config['HUB_NAME'] != hub_name)
                                                ]
                  

                  try:
                        push_hub_load_config(df_hub_load_config)
                        st.success("Configuration successfully saved to database.")
                  except Exception as e:
                        st.error(f"Error saving configuration: {str(e)}")




# Display the result DataFrame using st.dataframe
st.dataframe(
            data = df_hub_load_config,
            use_container_width = True
            )