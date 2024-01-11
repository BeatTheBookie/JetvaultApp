import streamlit as st
import pandas as pd
import snowflake.connector



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
                #warehouse='your_warehouse',
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