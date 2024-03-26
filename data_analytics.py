import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

def app():
    selection1 = option_menu(menu_title="Analytics Navigator",
                             options=['Loan purpose', 'Property status', 'Annual Interest Rate','Loan Amount'],
                             icons=['list-check','building-fill','piggy-bank-fill','cash-stack'],
                             menu_icon="menu-button",
                             default_index=0,
                             orientation="horizontal")

    # Load data
    info = pd.read_csv(r"C:\Users\Admin\Desktop\Nirma\DBMS\Innovative Assignment\loan_data_train.csv")
    
    # Data preprocessing
    info = info.drop(["Open.CREDIT.Lines", "Revolving.CREDIT.Balance"], axis=1)
    
    # Calculate principle amount per month
    info["Amount.Funded.By.Investors"] = pd.to_numeric(info["Amount.Funded.By.Investors"], errors='coerce')
    info["Loan.Length"] = pd.to_numeric(info["Loan.Length"], errors='coerce')
    principle_amount_per_month = info["Amount.Funded.By.Investors"] / info["Loan.Length"]

    # Calculate interest per month
    info["Interest.Rate"] = pd.to_numeric(info["Interest.Rate"], errors='coerce').astype(float)
    interest_per_month = (info["Interest.Rate"] * 100) / 12

    # Calculate total amount to be paid per month
    amount_to_be_paid_per_month = principle_amount_per_month + (principle_amount_per_month * interest_per_month)

    # Calculate earnings per month
    earning_per_month = info["Monthly.Income"]

    # Calculate the difference between earnings and payments
    can_borrower_pay = earning_per_month - amount_to_be_paid_per_month

    # Create a DataFrame to store the results
    results_df = pd.DataFrame(columns=["Result"])

    # Populate the DataFrame with YES and NO values
    for i in range(len(info)):
        if can_borrower_pay[i] < 0:
            results_df.loc[i, "Result"] = "NO"
        else:
            results_df.loc[i, "Result"] = "YES"

    # Concatenate the results DataFrame with the original DataFrame
    info = pd.concat([info, results_df], axis=1)
    info["Can Borrower Pay"] = can_borrower_pay
    info["Amount to be Paid per Month"] = amount_to_be_paid_per_month
    info["Interest per Month"] = interest_per_month

    # Display the merged DataFrame using Streamlit components
    # st.title("Merged DataFrame with Results:")
    # st.dataframe(info)

    # Number of People Who are able to repay the loan
    result_counts = info["Result"].value_counts()

    no_of_yes = result_counts.get("YES",0)
    no_of_nos = result_counts.get("NO",0)

    # State wise number of people who can repay the loan amount

    loan_purposes = [
        "car",
        "credit_card",
        "debt_consolidation",
        "educational",
        "home_improvement",
        "house",
        "major_purchase",
        "medical",
        "renewable_energy",
        "small_business",
        "vacation",
        "wedding"
    ]

    if selection1 == 'Loan purpose':
        
        selected_purpose = st.selectbox("Select Loan Purpose", loan_purposes)
        
        if selected_purpose:
            st.header(f"State-wise Loan Taken For {selected_purpose.replace('_', ' ').title()}")
            loans_df = info[info["Loan.Purpose"] == selected_purpose]
            state_loan_counts = loans_df["State"].value_counts()
            st.bar_chart(state_loan_counts)
        
        print_states()

    # State wise status of borrower's property
        
    property_status = [
        "MORTGAGE",
        "RENT",
        "OWN"
    ]

    if selection1 == 'Property status':
        
        selected_purpose1 = st.selectbox("Select The Borrower's Property Status", property_status)
        
        if selected_purpose1:
            st.header(f"State-wise Borrower's Property Status As {selected_purpose1.lower()}")
            property_df = info[info["Home.Ownership"] == selected_purpose1]
            state_property_count = property_df["State"].value_counts()
            st.bar_chart(state_property_count)
        
        print_states()

    
    if selection1 == 'Annual Interest Rate':
        statewise_interest = info.groupby("State")["Interest.Rate"].agg(['sum', 'count'])
        statewise_interest['average_interest_rate'] = (statewise_interest['sum'] / statewise_interest['count'])*100
        st.write("State-wise Annual Interest Rate Analysis")
        st.bar_chart(statewise_interest['average_interest_rate'])

        print_states()
    
    if selection1 == 'Loan Amount':
        statewise_loan_amount = info.groupby("State")["Amount.Funded.By.Investors"].agg(['sum', 'count'])
        statewise_loan_amount['average_loan_amount'] = statewise_loan_amount['sum'] / statewise_loan_amount['count']
        st.write("State-wise Loan Amount Analysis")
        st.bar_chart(statewise_loan_amount['average_loan_amount'])

        print_states()


def print_states():
    states_dict = {
        "AL": "Alabama",
        "CA": "California",
        "CT": "Connecticut",
        "FL": "Florida",
        "GA": "Georgia",
        "IL": "Illinois",
        "KS": "Kansas",
        "MD": "Maryland",
        "MI": "Michigan",
        "MN": "Minnesota",
        "NC": "North Carolina",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "PA": "Pennsylvania",
        "TX": "Texas",
        "VA": "Virginia",
        "WI": "Wisconsin",
        "WV": "West Virginia"
    }

    states_df = pd.DataFrame(list(states_dict.items()), columns=['Abbreviation', 'State'])

    st.title("States in America by Abbreviations")
    st.table(states_df)

    