import streamlit as st
import replicate
import base64

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

# Function to display GIF from URL
def display_gif_from_url(gif_url):
    st.markdown(f'<img src="{gif_url}" alt="Generated GIF">', unsafe_allow_html=True)

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
    display_gif_from_url(gif_url)

    
