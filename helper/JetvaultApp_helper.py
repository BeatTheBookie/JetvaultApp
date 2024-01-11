import streamlit as st
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas



# make any grid with a function
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid



#
# Functions to get data from database
#



# get configured stage schema
def get_stage_config():
    try:
        conn = snowflake.connector.connect(
            user=st.session_state.snowflake_user,
            password=st.session_state.snowflake_password,
            account=st.session_state.snowflake_account,
            warehouse = st.session_state.snowflake_warehouse,
            database=st.session_state.snowflake_database,
            schema=st.session_state.snowflake_schema
            )            

        # Your SQL query
        query = "SELECT stage_schema, LOAD_TYPE FROM META.LOAD_CONFIG"

        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the connection
        conn.close()

        return df
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None
        

# write stage config back to the database
def push_stage_config(df_stage_config):
    try:
        conn = snowflake.connector.connect(
            user=st.session_state.snowflake_user,
            password=st.session_state.snowflake_password,
            account=st.session_state.snowflake_account,
            warehouse = st.session_state.snowflake_warehouse,
            database=st.session_state.snowflake_database,
            schema=st.session_state.snowflake_schema
            )            

        # truncate table
        conn.cursor().execute("truncate table LOAD_CONFIG")

        # import data frame in empty table
        success, nchunks, nrows, _ = write_pandas(conn=conn, 
                                                df =  df_stage_config,
                                                table_name = 'LOAD_CONFIG'
                                                )

        # Close the connection
        conn.close()
        
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None



# get all available schemas in 
def get_all_db_schema():
    try:
        conn = snowflake.connector.connect(
            user=st.session_state.snowflake_user,
            password=st.session_state.snowflake_password,
            account=st.session_state.snowflake_account,
            warehouse = st.session_state.snowflake_warehouse,
            database=st.session_state.snowflake_database,
            schema=st.session_state.snowflake_schema
            )            

        # Your SQL query
        query = "SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA"

        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the connection
        conn.close()

        return df
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None