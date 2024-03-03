from io import BytesIO
import streamlit as st
from PIL import Image
from rembg import remove
import numpy as np
import base64
import replicate
import requests

st.title("Image Background Remover")

# Function to display GIF from URL
def display_gif_from_url(gif_url):
    st.markdown(f'<img src="{gif_url}" alt="Generated GIF">', unsafe_allow_html=True)

# Upload the file
image_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

def upload_img_to_imgbb(image_path):
    url = "https://api.imgbb.com/1/upload"
    api_key = "b4229cf7fd0a31cf38b5e1895545cf0a" # imgbb API key

    with open(image_path, "rb") as file:
        image_data = base64.b64encode(file.read()).decode("utf-8")
        payload = {"key": api_key, "image": image_data}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()
    
# If an image is uploaded, process it
if image_upload is not None:
    # Open the uploaded image
    input_image = Image.open(image_upload)
    
    # Remove the background
    output_image = remove(np.array(input_image))  # Convert PIL image to numpy array
    
    # Convert the output image to PIL Image
    result_img = Image.fromarray(output_image).convert("RGB")

    # Save the image to a file
    result_img.save("no_bg.png")
    
    # Convert the output image to URI for download
    response = upload_img_to_imgbb("no_bg.png")
    final_uri = response['data']['image']['url']
    
    # Display the original and the result side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(input_image, caption='Original Image')
    with col2:
        st.image(result_img, caption='Image without Background')
    
    # Create a download button for the result image
    st.markdown(f'<a href="{final_uri}" download="no_bg.png">Download Image</a>', unsafe_allow_html=True)
    
    # Use the output URI as input for replicate.run()
    output = replicate.run(
        "cjwbw/shap-e:abfc30dc09f51fe27602185f313860c32d501e7a4af6c5a23872eae80e651cb8",
        input={
            "image": final_uri,
            "prompt": "a horse",
            "batch_size": 1,
            "render_mode": "nerf",
            "render_size": 128,
            "guidance_scale": 15
        }
    )

    gif_uri = output[0]
    display_gif_from_url(gif_uri)

