import streamlit as st
import csv
import pandas as pd


# Function to process the text file and extract required data
def process_txt_file(file_content):
    top_energy = None
    bottom_energy = None
    second_column_values = []

    for line in file_content.splitlines():
        # Split each line by whitespace
        parts = line.split()
        # Skip lines that do not contain exactly two parts
        if len(parts) != 2:
            continue
        try:
            # Parse the first and second columns as float and int respectively
            energy_value = float(parts[0])
            count_value = int(parts[1])

            # Track top and bottom energy levels
            if top_energy is None or energy_value > top_energy:
                top_energy = energy_value
            if bottom_energy is None or energy_value < bottom_energy:
                bottom_energy = energy_value

            # Add the second column (count_value) to the list
            second_column_values.append(count_value)

        except ValueError:
            # Skip lines that cannot be parsed
            continue

    return top_energy, bottom_energy, second_column_values


# Function to save second column values to CSV
def save_to_csv(values):
    # Create a DataFrame to convert to CSV
    df = pd.DataFrame(values, columns=['Second Column Values'])
    return df.to_csv(index=False)


# Streamlit app layout
st.title("Peakaboo Data Formatter")

# Upload file
uploaded_file = st.file_uploader("Upload a .txt file from Bruker Esprit", type=["txt"])

if uploaded_file is not None:
    # Process the uploaded file
    file_content = uploaded_file.read().decode("utf-8")
    top_energy, bottom_energy, second_column_values = process_txt_file(file_content)

    # Display the top and bottom energy levels
    st.write(f"Bottom Energy Level: {bottom_energy}")
    st.write(f"Top Energy Level: {top_energy}")

    # Provide CSV for download
    csv = save_to_csv(second_column_values)
    st.download_button(label="Download CSV", data=csv, file_name="second_column_values.csv", mime="text/csv")
