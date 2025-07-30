import streamlit as st
import instructor
from instructor import Image
from pydantic import BaseModel, Field, create_model
from typing import Literal, get_args
from openai import OpenAI
import base64

# AI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
LLM = "gpt-4.1-nano"

client = instructor.from_openai(OpenAI(api_key=OPENAI_API_KEY))

def image_to_base64(image_path):
    """Convert an image file to a base64 encoded string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def get_image_analyzer_model(labels):
    """Dynamically create a Pydantic model with a Literal label field based on user-selected labels."""
    if not labels:
        labels = ["Need to select or create labels"]
    return create_model(
        "ImageAnalyzer",
        label=(Literal[tuple(labels)], Field(..., description="The labels for the image classification task."))
    )


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
st.markdown(
    """
    This is a simple image classification app that uses Instructor to classify images into predefined categories.
    You can upload an image and select the labels for the classification task.
    """
)

with st.form("image_classification_form"):
    image_file = st.file_uploader("Upload an image for classification:", type=["jpg", "jpeg", "png"])
    image_labels = st.multiselect(
        label="Labels for Image Classification (Max 5 selections)",
        options=[],
        max_selections=5,
        accept_new_options=True,
    )   

    if st.form_submit_button("Classify", type="primary"):
        if not image_file:
            st.error("Please upload an image file.")
            st.stop()
        if not image_labels:
            st.error("Please select at least one label for classification.")
            st.stop()
        
        with st.spinner("Classifying the image..."):
            image_bytes = image_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            image = Image.from_base64(f"data:image/jpeg;base64,{image_base64}")

            # Dynamically create the ImageAnalyzer model based on selected labels
            ImageAnalyzer = get_image_analyzer_model(image_labels)

            response, c = client.chat.completions.create_with_completion(
                model=LLM,
                response_model=ImageAnalyzer,
                messages=[
                    {"role": "system", "content": f"You are an image classifier. Classify the image into one of the provided categories: {', '.join(image_labels) if image_labels else 'No categories available'}."},
                    {"role": "user", "content": [image]},
                ],
                autodetect_images=True
            )

            if response:
                left_column, right_column = st.columns([1,2])
                left_column.image(image_file, use_container_width=True)
                right_column.subheader("Classification Result")
                right_column.info(f"Label: {response.label}")