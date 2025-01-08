# Star Size Predictor

This [web application](https://starsizepredictor.streamlit.app/) allows users to predict star sizes based on their brightness using linear regression. It generates a synthetic dataset of stars, which is used to train a model that predicts the size of stars based on their brightness values. This app serves as an educational tool for understanding linear regression and gradient descent in machine learning.

Demonstration of the [web app](https://youtu.be/doK0owyQA14)

## Key Features:
- **Generate Synthetic Dataset**: Users can specify the number of stars they want in the dataset, which includes brightness values and the corresponding true sizes.
- **Linear Regression Predictions**: A linear regression model is used to predict star sizes based on the brightness data.
- **Data Visualization**: The app enables users to plot the predicted data and compare it with actual values to assess model performance.
- **API Documentation**: The backend API is deployed on Render. Explore the API documentation [here](https://star-size-predictor-tl61.onrender.com/docs).

## Why Use a Synthetic Dataset?

The synthetic dataset simulates real-world astronomical data. By introducing noise into a true equation, students can create and use their own data, which helps in visualizing how gradient descent optimizes the model parameters (weights and bias). This project aims to build a foundation for more advanced applications, which will later use actual astronomical data.

## Setup Instructions

To set up the project on your local system, follow these steps:

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Asharu369/project_1.git
```

### Step 2: Create a Virtual Environment

#### For Windows:
```bash
python -m venv venv
```

#### For Linux or macOS:
```bash
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment

#### For Windows:
```bash
venv\Scripts\activate
```

#### For Linux or macOS:
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

Use the `requirements.txt` file to install the necessary dependencies:

#### For Windows:
```bash
python -m pip install -r requirements.txt
```

#### For Linux or macOS:
```bash
pip install -r requirements.txt
```

### Step 5: Start the Backend (FastAPI)

To run the FastAPI backend, execute:

```bash
uvicorn main:app --reload
```

### Step 6: Run the Frontend (Streamlit)

Start the Streamlit frontend with the following command:

```bash
streamlit run frontend.py
```

### Step 7: Use the Web Application

Once both the frontend and backend are running, you can interact with the web application. The application allows you to:
- Upload a CSV file with brightness data to generate star size predictions.
- Plot the predicted star sizes against the actual values.

## API Endpoints

- **POST /predict/**: Upload a CSV file containing brightness values to get a downloadable CSV with predicted star sizes.
- **POST /plot/**: Upload a CSV file to generate a plot comparing actual vs predicted star sizes.

You can access the API documentation and interact with the endpoints [here](https://starsize-predictor.onrender.com/docs).

## Tools Used

- **FastAPI**: For creating the backend API endpoints.
- **Streamlit**: For building and hosting the interactive frontend.
- **Render**: To deploy the backend API.
- **NumPy**: For generating synthetic data.
- **Matplotlib**: For visualizing the regression model and plotting predictions.
- **Pandas**: For handling CSV file reading, writing, and data manipulation.

## Acknowledgments

Thanks to the developers of the libraries used in this project:
- FastAPI
- Streamlit
- NumPy
- Matplotlib
- Pandas
