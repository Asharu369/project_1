import streamlit as st
import pandas as pd
import time
import requests
import io

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
    .footer {{
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Backend URL (update if your backend is deployed)
backend_url = "https://star-size-predictor-tl61.onrender.com"

# Home Page Content
if page == "Home":
    st.title("Welcome to Star Size Predictor 🌟")
    st.markdown(
        """
        **Star Size Predictor** uses machine learning to predict the size of stars based on their brightness.
        
        ### Instructions:
        1. **Create Dataset**: Enter the number of stars you want to generate.
        2. **Generate Predictions**: Click the button to generate predictions for the stars based on their brightness.
        3. **View Plot**: Click on the "Plot" button to get the linear regression plot for the prediction results.
        
        ### Features:
        - Generate a random dataset based on brightness and star size.
        - Get predictions based on your generated data.
        - View results alongside the plot.
    """
    )

    # Footer with project info on Home page
    st.markdown(
        """
        <div class="footer">
            <p>This project is developed by <strong>Muhammed Asharudheen</strong> as part of the ML4A Training Program at Spartifical.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Prediction Page Content
elif page == "Predict":
    st.title("Star Size Predictor by Asharu")

    # Sidebar input for the number of stars to generate
    num_stars = st.sidebar.number_input("Enter the number of stars to generate:", min_value=100, max_value=1000, value=500, step=50)

    # Add an informative section using st.expander
    with st.expander("How does this work?"):
        st.markdown(
            """
            This application predicts the size of stars based on their brightness using a linear regression model.
            The dataset is generated randomly, and the model is trained on this data.
            
            **Steps:**
            1. **Create Dataset**: Enter the number of stars you want to generate.
            2. **Generate Predictions**: Click on the "Generate Datasets" button.
            3. **View Results**: See predicted values and a graphical plot.
            """
        )

    # Create a button to generate the dataset and predictions
    if st.button("Generate Datasets"):
        # Make a request to the backend to generate the dataset
        response = requests.post(f"{backend_url}/generate-dataset/", json={"num_stars": num_stars})

        if response.status_code == 200:
            # Load the original dataset
            input_df = pd.read_csv(io.BytesIO(response.content))

            # Show message that predictions are being generated
            with st.spinner("Generating predictions..."):
                time.sleep(2)  # Simulate the time it takes to generate predictions

                # Make a request to the backend to generate predictions
                predict_response = requests.post(f"{backend_url}/predict/", files={"file": io.BytesIO(response.content)})

                if predict_response.status_code == 200:
                    predicted_df = pd.read_csv(io.BytesIO(predict_response.content))

                    # Display the datasets side by side using columns
                    col1, col2 = st.columns(2)



