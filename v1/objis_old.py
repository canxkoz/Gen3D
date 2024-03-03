import streamlit as st
import replicate
import base64
import pydeck as pdk
import requests
from pywavefront import Wavefront
from io import BytesIO
import tempfile

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
    gif_url = output[0]  # Assuming the GIF URL is the first element in the output list
    obj_url = output[1]  # Assuming the OBJ URL is the second element in the output list
    
    # Display GIF
    st.write("GIF Output:")
    st.markdown(f'<img src="{gif_url}" alt="Generated GIF">', unsafe_allow_html=True)
    
    # Display OBJ file
    st.write("OBJ Output:")
    st.markdown(f'[Download OBJ file]({obj_url})')

    # Download OBJ file and render as 3D model using pydeck
    with st.spinner('Rendering OBJ file...'):
        obj_data = download_obj_from_url(obj_url)
        if obj_data:
            with tempfile.NamedTemporaryFile(delete=False) as temp_obj_file:
                temp_obj_file.write(obj_data)
                temp_obj_file_path = temp_obj_file.name
            
            obj_parser = Wavefront(temp_obj_file_path)
            vertices = obj_parser.vertices
            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(latitude=0, longitude=0, zoom=6),
                layers=[pdk.Layer(
                    type="PointCloudLayer",
                    data=vertices,
                    get_position="[x, y, z]",
                    get_color=[255, 0, 0],
                    get_radius=10,
                    pickable=True,
                    auto_highlight=True,
                )],
            ))
        else:
            st.error("Failed to download OBJ file.")
