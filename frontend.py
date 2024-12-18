import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

# Streamlit app configuration
st.set_page_config(
    page_title="Star Size Predictor by Asharu",
    page_icon="🛸",  # UFO emoji
    layout="centered"
)

# Background image URL (public image from an image hosting site like Pixabay, Unsplash)
background_image_url = "https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569_1280.jpg"

# Add background image using custom CSS
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center center;
        height: 100vh;
        background-repeat: no-repeat;
        background-attachment: fixed;
        padding-top: 0;
    }}
    .sidebar .sidebar-content {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, 
    unsafe_allow_html=True
)

# App title
st.title("Star Size Predictor by Asharu ✨")

# Blue container with white text description
st.markdown(
    """
    <div style="background-color:blue; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color:white; text-align:center;">Predict Star Size Based on Brightness</h2>
        <p style="color:white; text-align:center;">
            This app will predict the star size based on its brightness values.
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Black container with white text showing CSV format instructions
st.markdown(
    """
    <div style="background-color:black; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color:white; text-align:center;">CSV File Format Instructions</h2>
        <p style="color:white;">
            Your CSV file should have two columns:
        </p>
        <ul style="color:white;">
            <li><strong>First column</strong>: Brightness of the stars</li>
            <li><strong>Second column</strong>: Respective size of the stars</li>
        </ul>
        <p style="color:white; text-align:center;">
            To test this application you can download a sample CSV file attached here:
        </p>
        <p style="color:white; text-align:center;">
            <a href="https://example.com/sample.csv" target="_blank" style="color:white;">Download Sample CSV</a>
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# File uploader widget for users to upload their CSV file
uploaded_file = st.file_uploader(
    "Upload your CSV file:", type=["csv"], help="Upload a file with 'inputs' and 'targets' columns."
)

if uploaded_file:
    # Reset file pointer before reading
    uploaded_file.seek(0)
    
    # Read the uploaded file into a Pandas DataFrame
    original_df = pd.read_csv(uploaded_file)

    # Create two columns for side-by-side display
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Original Data:")
        st.dataframe(original_df)

    # Send the file to the FastAPI `predict` endpoint
    uploaded_file.seek(0)  # Reset file pointer before sending to API
    response = requests.post(
        "http://localhost:8000/predict/",  # Update with the actual API URL if deployed
        files={"file": uploaded_file.getvalue()}
    )

    # Check for a valid response from the API
    if response.status_code == 200:
        # Read the predictions from the API response
        predicted_file = BytesIO(response.content)
        predicted_df = pd.read_csv(predicted_file)

        with col2:
            st.write("### Predicted Data:")
            st.dataframe(predicted_df)

        # Add a button to trigger the `plot` endpoint
        if st.button("Plot the Linear Regression"):
            # Show the spinner while waiting for the plot to generate
            with st.spinner('Generating plot...'):
                # Send the predicted CSV file to the plot endpoint
                predicted_file.seek(0)  # Reset the pointer of the predicted file before sending
                plot_response = requests.post(
                    "http://localhost:8000/plot/",  # Update with the actual API URL if deployed
                    files={"file": predicted_file.getvalue()}
                )

                # Check for a valid response from the API
                if plot_response.status_code == 200:
                    # Display the plot from the API response
                    plot_image = Image.open(BytesIO(plot_response.content))
                    st.write("### Linear Regression Plot:")
                    # Update use_column_width to use_container_width
                    st.image(plot_image, caption="Linear Regression Analysis", use_container_width=True)
                else:
                    st.error("Failed to generate the plot. Please try again.")
    else:
        st.error("Failed to process the uploaded file. Please check the file format and try again.")

