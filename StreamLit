import streamlit as st
import pandas as pd
import io

def main():
    # Title of the app
    st.title("Simple Streamlit App")
    
    # Section 1: Input an integer number
    st.header("Step 1: Input an Integer")
    user_number = st.number_input("Enter an integer:", min_value=0, value=0, step=1)
    st.write(f"You entered: {user_number}")
    
    # Section 2: Upload a CSV file
    st.header("Step 2: Upload a CSV File")
    uploaded_file = st.file_uploader("Upload a CSV file:", type=["csv"])
    
    if uploaded_file:
        # Read the uploaded CSV
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded CSV file preview:")
        st.write(df)
        
        # Modify the dataframe if needed (example: add the user_number as a new column)
        df['User Number'] = user_number
        
        # Section 3: Download the modified CSV file
        st.header("Step 3: Download the Modified CSV File")
        csv = df.to_csv(index=False)
        b64 = io.BytesIO(csv.encode()).getvalue()
        
        st.download_button(
            label="Download Modified CSV",
            data=b64,
            file_name="modified_file.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
