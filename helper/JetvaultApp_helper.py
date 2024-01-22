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
# cache DB connection to Snowflake
#

@st.cache_resource
def get_db_connection():

    
    try:
        conn = snowflake.connector.connect(
            user=st.session_state.snowflake_user,
            password=st.session_state.snowflake_password,
            account=st.session_state.snowflake_account,
            warehouse = st.session_state.snowflake_warehouse,
            database=st.session_state.snowflake_database,
            schema=st.session_state.snowflake_schema
            )    

        return conn
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None


#
# Get and save stage configuration
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
        query = "SELECT stage_schema, LOAD_TYPE FROM META.LOAD_CONFIG order by stage_schema"

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



#
# Get and save Hub load configuration
#


# get configured stage schema
def get_hub_load_config():
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
        query = """SELECT 
                stage_schema,
                stage_table,
                HUB_SCHEMA,
                hub_name,
                HUB_ALIAS,
                BK_SOURCE_COLUMN_LIST
            FROM 
                meta.HUB_LOAD
            ORDER BY 1,2,4,5"""

        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the connection
        conn.close()

        return df
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None


# write stage config back to the database
def push_hub_load_config(df_hub_config):
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
        conn.cursor().execute("truncate table HUB_LOAD")

        # import data frame in empty table
        success, nchunks, nrows, _ = write_pandas(conn=conn, 
                                                df =  df_hub_config,
                                                table_name = 'HUB_LOAD'
                                                )

        # Close the connection
        conn.close()
        
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None


#
# Get and save Sat load configuration
#


def get_sat_load_config():
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
        query = """SELECT 
                    stage_schema,
                    stage_table,
                    sat_schema,
                    SAT_NAME,
                    REFERENCED_OBJECT_NAME,
                    DELTA_HASH_SRC_COLUMN_LIST
                FROM 
                    META.SATELLITE_LOAD
                ORDER BY 1,2,4"""

        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the connection
        conn.close()

        return df
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None
    


# write stage config back to the database
def push_sat_load_config(df_sat_config):
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
        conn.cursor().execute("truncate table SATELLITE_LOAD")

        # import data frame in empty table
        success, nchunks, nrows, _ = write_pandas(conn=conn, 
                                                df =  df_sat_config,
                                                table_name = 'SATELLITE_LOAD'
                                                )

        # Close the connection
        conn.close()
        
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None



#
# Get and save link load configuration
#

def get_link_load_config():
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
        query = """SELECT 
                    STAGE_SCHEMA,
                    stage_table,
                    link_schema,
                    LINK_NAME,
                    L_COLUMN_NAME link_hash_column,
                    REFERENCED_HUB_NAME_1,
                    REFERENCED_HUB_NAME_2
                FROM 
                    META.LINK_LOAD
                ORDER BY 1,2,4"""

        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the connection
        conn.close()

        return df
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None




# write stage config back to the database
def push_link_load_config(df_link_config):
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
        conn.cursor().execute("truncate table LINK_LOAD")

        # import data frame in empty table
        success, nchunks, nrows, _ = write_pandas(conn=conn, 
                                                df =  df_link_config,
                                                table_name = 'LINK_LOAD'
                                                )

        # Close the connection
        conn.close()
        
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None



#
# Get and save transactional link load configuration
#
    



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
    


# get table for a given schema
def get_tables_by_schema(schema_name):

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
        query = """SELECT 
                    table_name
                FROM 
                    INFORMATION_SCHEMA."TABLES"
                WHERE
                    --exlude stage-views
                    table_name not like 'VW_%' and
                    table_schema = '""" + schema_name + """'
                ORDER BY 1"""

        
        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the connection
        conn.close()

        return df
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None
    


# get table for a given schema
def get_columns_by_table(schema_name, table_name):

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
        query = """SELECT 
                    COLUMN_NAME
                FROM 
                    INFORMATION_SCHEMA."COLUMNS"
                WHERE 
                    table_schema = '""" + schema_name + """'
                    AND table_name =  '""" + table_name + """'
                ORDER BY 1"""

        
        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Close the connection
        conn.close()

        return df
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None
