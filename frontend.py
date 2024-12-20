import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from PIL import Image

# Streamlit app configuration
st.set_page_config(
    page_title="Star Size Predictor by Asharu",
    page_icon="🌌",
    layout="centered"
)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Predict"])

# Background image URL (public image from an image hosting site like Pixabay, Unsplash)
background_image_url = "https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569_1280.jpg"

# Inject CSS for the background image
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
    .stSidebar {{
        background-color: rgba(0, 0, 0, 0.6);  /* Set the sidebar background to be transparent */
    }}
    .title {{
        font-family: 'Arial', sans-serif;
        color: #fff;
        text-align: center;
    }}
    .section-header {{
        background-color: rgba(76, 175, 80, 0.7);
        padding: 10px;
        color: white;
        border-radius: 5px;
    }}
    .file-instructions {{
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
        padding: 20px;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Home Page Content
if page == "Home":
    st.title("Welcome to Star Size Predictor 🌟")
    st.markdown(
        """
        **Star Size Predictor** uses machine learning to predict the size of stars based on their brightness.
        
        ### Instructions:
        1. **Generate Dataset**: Enter the number of stars you want to generate using a simple random generator.
        2. **Make Predictions**: Upload your dataset and the app will predict the size of the stars based on brightness.
        3. **View Results**: After uploading your data, the app will display the predicted results and show a graphical plot.
        
        ### Features:
        - Download sample CSV for testing.
        - Generate a random dataset based on brightness and star size.
        - Upload your own dataset for prediction.
        - Get predictions and a linear regression plot.
        
        
        """
    )
    
    st.markdown(
        """
        <div style="background-color: rgba(0, 0, 0, 0.6); padding: 20px; border-radius: 10px; margin-top: 20px;">
            <p style="color:white; text-align:center;">
                Developed by <strong>Muhammed Asharudheen</strong> as part of the ML4A Training Program at Spartifical.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Prediction Page Content
elif page == "Predict":
    st.title("Star Size Predictor by Asharu 🛸")

    # Sidebar input for the number of stars to generate
    num_stars = st.sidebar.number_input("Enter the number of stars to generate:", min_value=100, max_value=1000, value=500, step=50)

    # Add an informative section using st.expander
    with st.expander("How does this work?"):
        st.markdown(
            """
            This application predicts the size of stars based on their brightness using a linear regression model.
            The dataset is generated randomly, and the model is trained on this data.
            
            **Steps:**
            1. **Generate Dataset**: Enter the number of stars you want to generate.
            2. **Make Predictions**: Upload your dataset.
            3. **View Results**: See predicted values and a graphical plot.
            """
        )

    # Add CSV file format instructions inside an expandable section
    with st.expander("CSV File Format Instructions"):
        st.markdown(
            """
            Your CSV file should have two columns:
            - **Brightness**: The brightness of the stars.
            - **True Size**: The actual size of the stars.
            
            The app will process this data to predict star sizes based on brightness.
            """
        )

    # Provide the download button for the sample CSV
    sample_csv_url = "https://raw.githubusercontent.com/Asharu369/project_1/main/input_star_data.csv"
    sample_csv = requests.get(sample_csv_url).content

    st.download_button(
        label="📥 Download Sample CSV",
        data=sample_csv,
        file_name="input_star_data.csv",
        mime="text/csv"
    )

    # Provide a button to generate the dataset
    if st.button("Generate Dataset"):
        # Simulate dataset generation based on the input number of stars
        N_SAMPLES = num_stars

        # Generate Data
        X_test = 3 * np.random.rand(N_SAMPLES, 1)
        y_test = 9 + 2 * X_test + np.random.rand(N_SAMPLES, 1)

        # Convert arrays into dict
        dict_info = {'Brightness': X_test.reshape(-1), 'True Size': y_test.reshape(-1,)}
        
        # Convert dict to pandas dataframe
        input_df = pd.DataFrame(dict_info)

        # Provide a download button for the generated dataset
        st.write("### Generated Dataset:")
        st.dataframe(input_df)

        # Save and provide download link for generated CSV
        csv_data = input_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Generated Dataset",
            data=csv_data,
            file_name="generated_star_data.csv",
            mime="text/csv"
        )

    # File uploader and result display section
    uploaded_file = st.file_uploader(
        "Upload your CSV file:", type=["csv"], help="Upload a file with 'inputs' and 'targets' columns."
    )

    if uploaded_file:
        st.write(f"**Uploading file:** {uploaded_file.name}")
        uploaded_file.seek(0)  # Reset the file pointer

        # Read the uploaded file into a Pandas DataFrame
        original_df = pd.read_csv(uploaded_file)

        # Display the uploaded dataset
        st.write("### Original Data:")
        st.dataframe(original_df)

        # Make prediction and plot
        st.write("### Predictions and Plot")
        # Send the file to the FastAPI predict endpoint (replace with actual URL)
        response = requests.post(
            "https://your-backend-url.onrender.com/predict/",  # Replace with your FastAPI URL
            files={"file": uploaded_file.getvalue()}
        )

        if response.status_code == 200:
            predicted_file = BytesIO(response.content)
            predicted_df = pd.read_csv(predicted_file)
            st.write("### Predicted Data:")
            st.dataframe(predicted_df)

            # Plotting button
            if st.button("Plot the Linear Regression"):
                with st.spinner('Generating plot...'):
                    predicted_file.seek(0)
                    plot_response = requests.post(
                        "https://your-backend-url.onrender.com/plot/",  # Replace with your FastAPI URL
                        files={"file": predicted_file.getvalue()}
                    )

                    if plot_response.status_code == 200:
                        plot_image = Image.open(BytesIO(plot_response.content))
                        st.image(plot_image, caption="Linear Regression Analysis", use_container_width=True)
                    else:
                        st.error("Failed to generate the plot. Please try again.")
        else:
            st.error("Failed to process the uploaded file. Please check the file format and try again.")

    # Footer with project info
    st.markdown(
        """
        <div style="background-color:#333; color:white; padding: 10px; text-align:center;">
            <p>This project is developed by <strong>Muhammed Asharudheen</strong> as part of the ML4A Training Program at Spartifical.</p>
        </div>
        """,
        unsafe_allow_html=True
    )




