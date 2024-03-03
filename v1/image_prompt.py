

from io import BytesIO
import streamlit as st
from PIL import Image
from rembg import remove
import numpy as np
import base64

st.title("Image Background Remover")

# Upload the file
image_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Function to convert image for download
def convert_image_to_uri(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    data_uri = base64.b64encode(byte_im).decode('utf-8')
    return f"data:image/png;base64,{data_uri}"

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
    
    # Convert the output image to URI for download
    final_uri = convert_image_to_uri(result_img)
    
    # Display the original and the result side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(input_image, caption='Original Image')
    with col2:
        st.image(result_img, caption='Image without Background')
    
    # Create a download button for the result image
    st.markdown(f'<a href="{final_uri}" download="no_bg.png">Download Image</a>', unsafe_allow_html=True)

from io import BytesIO
import streamlit as st
from PIL import Image
from rembg import remove
import numpy as np
import base64
import replicate

st.title("Image Background Remover")

# Upload the file
image_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Function to convert image for download
def convert_image_to_uri(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    data_uri = base64.b64encode(byte_im).decode('utf-8')
    return f"data:image/png;base64,{data_uri}"

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
    
    # Convert the output image to URI for download
    final_uri = convert_image_to_uri(result_img)
    
    # Display the original and the result side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(input_image, caption='Original Image')
    with col2:
        st.image(result_img, caption='Image without Background')
    
    # Create a download button for the result image
    st.markdown(f'<a href="{final_uri}" download="no_bg.png">Download Image</a>', unsafe_allow_html=True)
    
    # Print the final URI
    st.write("Final URI:", final_uri)
    
    # Use the output URI as input for replicate.run()
    output = replicate.run(
        "cjwbw/shap-e:abfc30dc09f51fe27602185f313860c32d501e7a4af6c5a23872eae80e651cb8",
        input={
            "image": final_uri,
            "prompt": "",
            "batch_size": 1,
            "render_mode": "nerf",
            "render_size": 256,
            "guidance_scale": 3
        }
    )

    # Check if output contains image data
    if 'image' in output:
        # Display the output image
        st.image(output['image'], caption='Output from Replicate')
    else:
        st.error("Error processing image with Replicate API")

