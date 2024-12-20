from fastapi import FastAPI, File, UploadFile
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Force non-interactive backend to avoid Tkinter issues
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Create an instance of the FastAPI application
app = FastAPI()

# Set up CORS middleware to handle cross-origin requests, enabling interaction with front-end applications.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific origins in production)
    allow_credentials=True,  # Allow cookies and other credentials
    allow_methods=["*"],  # Allow all HTTP methods (e.g., GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

# Constants for the linear regression model (taken from training_star_size_predictor.ipynb)
W = 1.982015  # Coefficient (slope) of the linear regression model
b = 9.500380  # Intercept (bias) of the linear regression model

@app.get('/')
def default():
    """
    Default endpoint to check if the application is running.
    """
    return {'App': 'Running'}

@app.post("/generate-dataset/")
async def generate_dataset(num_stars: int):
    """
    Endpoint to generate a synthetic star dataset based on the number of stars.
    
    Args:
        num_stars (int): Number of stars to generate.

    Returns:
        StreamingResponse: A downloadable CSV file with generated star data.
    """
    np.random.seed(5007)
    X_test = 3 * np.random.rand(num_stars, 1)
    y_test = 9 + 2 * X_test + np.random.rand(num_stars, 1)

    dict_info = {'Brightness': X_test.reshape(-1), 'True Size': y_test.reshape(-1,)}
    input_df = pd.DataFrame(dict_info)

    output = input_df.to_csv(index=False).encode('utf-8')

    return StreamingResponse(
        io.BytesIO(output),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=generated_data.csv"}
    )

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint to perform predictions based on input data from an uploaded CSV file.

    Args:
        file (UploadFile): CSV file containing columns 'inputs' and 'targets'.

    Returns:
        StreamingResponse: A downloadable CSV file with an additional 'predictions' column.
    """
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    df.columns = ['inputs', 'targets']
    df['predictions'] = W * df['inputs'] + b

    output = df.to_csv(index=False).encode('utf-8')
    return StreamingResponse(
        io.BytesIO(output),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=predictions.csv"}
    )

@app.post("/plot/")
async def plot(file: UploadFile = File(...)):
    """
    Endpoint to generate a plot comparing actual targets and predictions based on input data.

    Args:
        file (UploadFile): CSV file containing columns 'inputs' and 'targets'.

    Returns:
        StreamingResponse: A downloadable PNG image file of the plot.
    """
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    plt.figure(figsize=(10, 6))
    plt.scatter(df['inputs'], df['targets'], color='royalblue', label='Actual Targets', marker='x')
    df['predictions'] = W * df['inputs'] + b
    rmse_score = np.mean(np.square(df['predictions'].values - df['targets'].values))
    plt.plot(df['inputs'], df['predictions'], color='k', label='Predictions', linewidth=2)
    plt.title(f'Linear Regression for Stars Data (RMSE: {round(rmse_score, 1)})', color='maroon', fontsize=15)
    plt.xlabel('Brightness', color='m', fontsize=13)
    plt.ylabel('Size', color='m', fontsize=13)
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return StreamingResponse(
        buf,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=plot.png"}
    )

