import streamlit as st
import streamlit.components.v1 as components




#helper functions
#from helper.BTB_app_helper import get_authenticater_config
#from helper.BTB_app_helper import make_grid



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
#



#
# tab definition
#


tab1, tab2 = st.tabs([
                    "What is the Jetvault App?",
                    "How to use the app?"
                    ])





#
# What is the BeatTheBookie App?
# 

with tab1:
    

    """
        
    ## What is the Jetvault App?

    Here we need some description for the App.
    
    """


#
# How to use the app?
# 

with tab2:
    
    """
        
    ## How to use the Jetvault App?

    Introduction to the Jetvault App

    """