import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

# Streamlit app configuration
st.set_page_config(
    page_title="Star Size Predictor by Asharu",
    page_icon="🛸",
    layout="centered"
)

# Background image URL (public image from an image hosting site like Pixabay, Unsplash)
background_image_url = "https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569_1280.jpg"

# Inject CSS for the background image
if isinstance(background_image_url, str) and background_image_url.strip():
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("{background_image_url}");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stSidebar"] {{
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
else:
    st.error("Invalid background image URL.")

# App title
st.title("Star Size Predictor by Asharu ✨")

# Instructions
st.markdown(
    """
    <div style="background-color:rgba(0, 0, 255, 0.0); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color:white; text-align:center;">Predict Star Size Based on Brightness</h2>
        <p style="color:white; text-align:center;">
            This app will predict the star size based on its brightness values.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# CSV file format instructions
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
            <a href="https://raw.githubusercontent.com/your-username/your-repo/main/sample.csv" target="_blank" style="color:white;">Download Sample CSV</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# File uploader for users to upload their CSV file
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
        "https://star-size-predictor-tl61.onrender.com/predict/",  # Update with the actual API URL if deployed
        files={"file": uploaded_file.getvalue()}
    )

    if response.status_code == 200:
        predicted_file = BytesIO(response.content)
        predicted_df = pd.read_csv(predicted_file)

        with col2:
            st.write("### Predicted Data:")
            st.dataframe(predicted_df)

        # Plotting button
        if st.button("Plot the Linear Regression"):
            with st.spinner('Generating plot...'):
                predicted_file.seek(0)
                plot_response = requests.post(
                    "https://star-size-predictor-tl61.onrender.com/plot/",  # Update with the actual API URL if deployed
                    files={"file": predicted_file.getvalue()}
                )

                if plot_response.status_code == 200:
                    plot_image = Image.open(BytesIO(plot_response.content))
                    st.write("### Linear Regression Plot:")
                    st.image(plot_image, caption="Linear Regression Analysis", use_container_width=True)
                else:
                    st.error("Failed to generate the plot. Please try again.")
    else:
        st.error("Failed to process the uploaded file. Please check the file format and try again.")

