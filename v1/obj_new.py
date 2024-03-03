import streamlit as st
import streamlit.components.v1 as components
import replicate
import base64
import requests
from pywavefront import Wavefront
from io import BytesIO
import tempfile
from obj2html import obj2html

# Define function to run replication
def run_replication(prompt, render_mode, render_size, guidance_scale):
    output = replicate.run(
        "cjwbw/shap-e:5957069d5c509126a73c7cb68abcddbb985aeefa4d318e7c63ec1352ce6da68c",
        input={
            "prompt": prompt,
            "save_mesh": True,
            "batch_size": 1,
            "render_mode": render_mode,
            "render_size": render_size,
            "guidance_scale": guidance_scale
        }
    )
    return output

# Function to download OBJ file from URL
def download_obj_from_url(obj_url):
    response = requests.get(obj_url)
    if response.status_code == 200:
        return response.content
    else:
        return None

# Create Streamlit app
st.title("Replicate your image")

# Input parameters
prompt = st.text_input("Enter prompt", "shark")
render_mode = st.selectbox("Select render mode", ["nerf", "other_render_mode"])
render_size = st.slider("Select render size", 64, 512, 128)
guidance_scale = st.slider("Select guidance scale", 1, 50, 15)

# Run replication when button is clicked
if st.button("Generate 3d"):
    output = run_replication(prompt, render_mode, render_size, guidance_scale)
    obj_url = output[1]  # Assuming the OBJ URL is the second element in the output list
    
    # Download OBJ file
    obj_data = download_obj_from_url(obj_url)
    if obj_data:
        # Save OBJ data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".obj") as temp_obj_file:
            temp_obj_file.write(obj_data)
            temp_obj_file_path = temp_obj_file.name
        
        # Convert OBJ to HTML string with additional options
        html_string = obj2html(
            temp_obj_file_path,
            scale=100,
            font_size=40,
            html_elements_only=True
        )
        
        # Display 3D model in Streamlit
        components.html(html_string, height=600)
    else:
        st.error("Failed to download OBJ file.")
