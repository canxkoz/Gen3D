from io import BytesIO
import streamlit as st
from PIL import Image
from rembg import remove
import numpy as np

st.title("Image Background Remover")

# Upload the file
image_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Function to convert image for download
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# If an image is uploaded, process it
if image_upload is not None:
    # Open the uploaded image
    input_image = Image.open(image_upload)
    
    # Convert the image to RGBA if it's not already
    if input_image.mode != 'RGBA':
        input_image = input_image.convert('RGBA')
    
    # Remove the background
    output_image = remove(np.array(input_image))  # Convert PIL image to numpy array
    
    # Convert the output image to PIL Image
    result_img = Image.fromarray(output_image)
    
    # Convert the output image to BytesIO for download
    final_img = convert_image(result_img)
    
    # Display the original and the result side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(input_image, caption='Original Image')
    with col2:
        st.image(result_img, caption='Image without Background')
    
    # Create a download button for the result image
    st.download_button(
        label="Download Image",
        data=final_img,
        file_name="no_bg.png",
        mime="image/png"
    )

