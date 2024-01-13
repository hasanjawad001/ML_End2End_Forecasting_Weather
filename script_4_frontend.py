import os
import boto3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from dotenv import load_dotenv
import joblib


# Set page configuration
# st.set_page_config(layout="wide")

# Streamlit title
st.title("Predict Temperature!!!")

# Load environment variables
load_dotenv()
# AWS Credentials (ensure these are securely set, for example, as environment variables)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize boto3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2'
)

# Function to download file from S3
def download_file_from_s3(bucket_name, s3_file_key, local_file_name):
    if not os.path.exists(local_file_name):
        s3_client.download_file(bucket_name, s3_file_key, local_file_name)
    else:
        pass
    
# Download the file
bucket_name = 'mle-e2e-2'  # Your S3 bucket name
s3_file_key = 'models/model.pkl'  # S3 file key
if not os.path.exists('models'):
    os.makedirs('models')
local_file_name = 'models/model.pkl'
download_file_from_s3(bucket_name, s3_file_key, local_file_name)

# Load model
model = joblib.load(local_file_name)


# Using columns to create a more compact layout
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    temp_7d_ago = st.number_input("7 days ago (°C):", step=1)
with col2:
    temp_6d_ago = st.number_input("6 days ago (°C):", step=1)
with col3:
    temp_5d_ago = st.number_input("5 days ago (°C):", step=1)
with col4:
    temp_4d_ago = st.number_input("4 days ago (°C):", step=1)
with col5:
    temp_3d_ago = st.number_input("3 days ago (°C):", step=1)
with col6:
    temp_2d_ago = st.number_input("2 days ago (°C):", step=1)
with col7:
    temp_1d_ago = st.number_input("1 day ago (°C):", step=1)

# Predict button
if st.button("Predict Today's Temperature"):
    # Create an array from the input values
    input_features = [temp_1d_ago, temp_2d_ago, temp_3d_ago, temp_4d_ago, temp_5d_ago, temp_6d_ago, temp_7d_ago]
    input_df = pd.DataFrame([input_features], columns=[f'Temp_{i}d_ago' for i in range(1, 8)])
    
    # Make prediction
    predicted_temp = model.predict(input_df)[0]
    
    # Display the prediction
    st.success(f"The predicted temperature for today is: {predicted_temp:.2f} °C")