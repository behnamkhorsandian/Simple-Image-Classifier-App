import streamlit as st
import instructor
from instructor import Image
from pydantic import BaseModel, Field
from typing import Literal
from openai import OpenAI
import base64

# AI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
LLM = "gpt-4.1-nano"

client = instructor.from_openai(OpenAI(api_key=OPENAI_API_KEY))

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Define the Pydantic model for the image classification response
class ImageAnalyzer(BaseModel):
    label: Literal["Dog", "Bird", "Fish", "Cat", "Other"] = Field(..., description="The labels for the image classification task.")   

# Set up the Streamlit app
st.set_page_config(
    page_title="Simple Image Classifier",
    page_icon="👁️",
    layout="centered",
    menu_items={
        'Get Help': 'https://www.behnvm.com',
        'Report a Bug': 'mailto:contact@behnvm.com',
        'About': 'A simple Image Classifier using Instructor, For demo purposes.',
    }
)

st.title("👁️ Simple Image Classifier")

image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
st.divider()

if image_file:
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image = Image.from_base64(f"data:image/jpeg;base64,{image_base64}")

    response, c = client.chat.completions.create_with_completion(
        model=LLM,
        response_model=ImageAnalyzer,
        messages=[
            {"role": "system", "content": "You are an image classifier. Classify the image into one of the provided categories."},
            {"role": "user", "content": [image]},
        ],
        autodetect_images=True
    )

    left_column, right_column = st.columns([1,2])
    left_column.image(image_file, use_container_width=True)
    right_column.subheader("Classification Result")
    right_column.info(f"Label: {response.label}")
else:
    left_column, right_column = st.columns([1,2])
    left_column.container(height=220, border=True)
    right_column.subheader("Classification Result")
    right_column.warning("Please upload an image to classify it.")