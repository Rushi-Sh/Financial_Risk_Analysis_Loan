import pandas as pd
import streamlit as st

def app():
        
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
        st.title("Merged DataFrame with Results:")
        st.dataframe(info)