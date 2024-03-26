import streamlit as st
import pandas as pd

def get_fico_classification(fico_score):
    if fico_score >= 800 and fico_score <= 850:
        return "Exceptional"
    elif fico_score >= 740 and fico_score <= 799:
        return "Very Good"
    elif fico_score >= 670 and fico_score <= 739:
        return "Good"
    elif fico_score >= 580 and fico_score <= 669:
        return "Fair"
    elif fico_score >= 300 and fico_score <= 579:
        return "Poor"

def app():
    # Load data
    info = pd.read_csv(r"C:\Users\Admin\Desktop\Nirma\DBMS\Innovative Assignment\loan_data_train.csv")
    
    # Data preprocessing
    info = info.drop(["Open.CREDIT.Lines", "Revolving.CREDIT.Balance"], axis=1)
    
    # Extract lower bound of FICO range
    info['FICO.Range'] = pd.to_numeric(info['FICO.Range'].str.split('-', expand=True)[0], errors='coerce')

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

    # Determine FICO score classification
    info['FICO.Classification'] = info['FICO.Range'].apply(get_fico_classification)

    st.dataframe(info)
