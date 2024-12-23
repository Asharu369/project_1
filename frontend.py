import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Set the page configuration
st.set_page_config(
    page_title="Star Size Predictor",
    page_icon="🌌",
    layout="centered"
)

# Background image URL
background_image_url = "https://cdn.pixabay.com/photo/2017/08/30/01/05/milky-way-2695569_1280.jpg"

# Inject CSS for background image and footer
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_image_url}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stSidebar"] {{
    background-color: rgba(0, 0, 0, 0.5);
}}
.gray-container {{
    background-color: rgba(255, 255, 255, 0.8); 
    color: black;
    padding: 10px;
    border-radius: 10px;
    font-size: 18px;
    line-height: 1.6;
}}
.footer {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: black;
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    border-top: 1px solid #ccc;
}}
.stButton>button {{
    background-color: #4CAF50;
    color: white;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Home Page
def home_page():
    st.markdown('<h1 style="color:white;">Welcome to Star Size Predictor </h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="color:white;">
        <p>This application predicts the size of stars based on their brightness using a linear regression model. 
        The dataset is generated randomly, and the model is trained on this data.</p>
        <div style="color:white;">
        <h4><u>Instructions:</u></h4>
        <ol>
            <li><strong>Create Dataset</strong>: Enter the number of stars you want to generate.</li>
            <li><strong>Generate Predictions</strong>: Click the button to generate predictions for the stars based on their brightness.</li>
            <li><strong>View Plot</strong>: Click on the "Plot" button to get the linear regression plot for the prediction results.</li>
        </ol>
        <h4><u>Features:</u></h4>
        <ol>
            <li>Generate a random dataset based on brightness and star size.</li>
            <li>Get predictions based on your generated data.</li>
            <li>View the graphical plot.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        This project is developed by <strong>Muhammed Asharudheen</strong> as part of the ML4A Training Program at Spartifical.
    </div>          
    """, unsafe_allow_html=True)

# Predict Page
def predict_page():
    st.markdown('<h1 style="color:white;">Star Size Predictor </h1>', unsafe_allow_html=True)

    # API endpoints
    CREATE_DATA_ENDPOINT = "https://star-size-predictor-tl61.onrender.com/create_data/"
    PREDICT_ENDPOINT = "https://star-size-predictor-tl61.onrender.com/predict/"
    PLOT_ENDPOINT = "https://star-size-predictor-tl61.onrender.com/plot/"

    # Initialize session states
    if 'generated_df' not in st.session_state:
        st.session_state.generated_df = None
    if 'predicted_df' not in st.session_state:
        st.session_state.predicted_df = None

    # User input for number of samples
    st.markdown("<h4>Generate the Star Dataset</h4>", unsafe_allow_html=True)
    n_samples = st.number_input("Enter the number of stars:", min_value=10, value=500)

    if st.button("Create Dataset and Generate Predictions"):
        with st.spinner("Generating dataset..."):
            try:
                response = requests.post(CREATE_DATA_ENDPOINT, params={"n_samples": n_samples})
                response.raise_for_status()
                st.session_state.generated_df = pd.read_csv(BytesIO(response.content))

                with st.spinner("Generating predictions..."):
                    prediction_response = requests.post(
                        PREDICT_ENDPOINT,
                        files={"file": BytesIO(response.content)}
                    )
                    prediction_response.raise_for_status()
                    st.session_state.predicted_df = pd.read_csv(BytesIO(prediction_response.content))
            except requests.exceptions.RequestException as e:
                st.error(f"Error while communicating with the server: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    # Display generated and predicted dataframes side by side
    if st.session_state.generated_df is not None and st.session_state.predicted_df is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Generated Dataset")
            st.dataframe(st.session_state.generated_df)
        with col2:
            st.write("### Predicted Data")
            st.dataframe(st.session_state.predicted_df)

    # Plotting section
    if st.session_state.predicted_df is not None:
        if st.button("Plot the Linear Regression"):
            with st.spinner("Generating plot..."):
                try:
                    csv_data = st.session_state.predicted_df.to_csv(index=False).encode('utf-8')
                    plot_response = requests.post(PLOT_ENDPOINT, files={"file": csv_data})
                    plot_response.raise_for_status()
                    st.image(BytesIO(plot_response.content))
                except requests.exceptions.RequestException as e:
                    st.error(f"Error while generating plot: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

# Streamlit pages
PAGES = {
    "Home": home_page,
    "Predict": predict_page,
}

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", list(PAGES.keys()))
PAGES[page]()





