import pandas as pd
import streamlit as st
import database,data_analytics,home_page,loan_risk_predictor
from streamlit_option_menu import option_menu

# Create a sidebar navigation
with st.sidebar:
    selection = option_menu(
        menu_title="Navigation Pane", 
        options=['Home', 'Database', 'Analytics','Loan Risk Predictor'],
        icons=["house","database","bar-chart-line"],
        menu_icon="cast",
        default_index=0)

# Render different pages based on selection
if selection == 'Home':
    st.title('Home')
    home_page.app()

elif selection == 'Database':
    st.title('Database')
    database.app()
     
elif selection == 'Analytics':
    st.title('Analytics')
    data_analytics.app()

elif selection == 'Loan Risk Predictor':
    st.title('Loan Risk Predictor')
    loan_risk_predictor.app()

