import streamlit as st
from PIL import Image
from deep_translator import GoogleTranslator
import io
import requests
from database import (
    create_database,
    register_user,
    login_user,
    create_history_table,
    save_prompt,
    get_prompt_history
)
from auth import auth_page
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()
create_database()
create_history_table()



# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)
st.markdown("""
<style>

.main{
    padding-top:20px;
}

div.stButton > button{
    width:100%;
    height:50px;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
}

.stTextInput input{
    border-radius:10px;
}

div[data-testid="metric-container"]{
    border-radius:15px;
    padding:15px;
    border:1px solid #ddd;
    box-shadow:0px 3px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)
if "history" not in st.session_state:
    st.session_state.history = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False




if not os.path.exists("gallery"):
    os.makedirs("gallery")




# -----------------------------
# TITLE
# -----------------------------
if not st.session_state.logged_in:
    auth_page()
    st.stop()
st.markdown("""
<h1 style='text-align:center;
color:#4F46E5;
font-size:45px;'>
 AI Image Generator
</h1>

<p style='text-align:center;
font-size:20px;
color:gray;'>
Generate stunning AI images from your imagination ✨
</p>
""", unsafe_allow_html=True)
col1, col2 = st.columns([8, 2])

with col1:
    st.write(f"👋 Welcome, {st.session_state.username}")

with col2:
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.pop("username", None)
        st.rerun()

st.markdown("### 💡 Example Prompts")

col1, col2 = st.columns(2)

with col1:
    if st.button("🐘 Baby Elephant"):
        prompt = "A cute baby elephant walking in a green forest"

    if st.button("🏰 Magical Castle"):
        prompt = "A magical castle on floating islands"

with col2:
    if st.button("🌆 Cyberpunk City"):
        prompt = "A futuristic cyberpunk city at night"

    if st.button("🐶 Cute Puppy"):
        prompt = "A cute puppy playing in a garden"
# Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.write(
    "Model: Stable Diffusion XL"
)

st.sidebar.write(
    "Framework: Streamlit"
)

st.sidebar.write(
    "AI: Diffusion Model"
)
st.sidebar.title("🎨 AI Image Generator")

st.sidebar.write("Example Prompts")

st.sidebar.code("""
A futuristic city at sunset

A cute baby elephant in a forest

A magical castle on floating islands

A cyberpunk Chennai at night
                
""")

st.write("Generate AI Images using Stable Diffusion")

# -----------------------------
# PROMPT INPUT

prompt = st.text_area(
    "✨ Describe your image",
    height=120,
    placeholder="Example: A futuristic city at sunset..."
)
style = st.selectbox(
    "🎨 Choose Image Style",
    [
        "Realistic",
        "Anime",
        "3D Render",
        "Watercolor",
        "Oil Painting",
        "Fantasy",
        "Cyberpunk",
        "Pixel Art"
    ]
)
tanglish_dict = {
    "yaanai": "elephant",
    "kutty": "cute",
    "naai": "dog",
    "poonai": "cat",
    "kaadu": "forest",
    "malai": "mountain",
    "kadal": "sea",
    "mazhai": "rain",
    "kovil": "temple",
    "paravai": "bird",
    "singam": "lion",
    "puli": "tiger",
    "maadu": "cow",
    "erumai": "buffalo",
    "chennai": "Chennai city",
    "night": "night",
    "vimanam": "airplane",
    "car": "car",
    "veedu": "house",
    "maram": "tree"
}
def convert_tanglish(prompt):

    words = prompt.lower().split()

    converted = []

    for word in words:
        converted.append(
            tanglish_dict.get(word, word)
        )

    return " ".join(converted)


from PIL import Image
import requests
import io

def generate_image(prompt):
    try:
        encoded_prompt = urllib.parse.quote(prompt)

        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

        response = requests.get(url)

        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            return image
        else:
            st.error("Failed to generate image.")
            return None

    except Exception as e:
        st.error(f"Error: {e}")
        return None

    return image
if st.button("🚀 Generate Image"):

    if prompt:

        with st.spinner("Generating Image..."):

            try:
                english_prompt = GoogleTranslator(
                    source="auto",
                    target="en"
                ).translate(prompt)

            except Exception:
                english_prompt = convert_tanglish(prompt)

            final_prompt = (
                f"{english_prompt}, {style}, "
                "highly detailed, 8K, masterpiece"
            )

            st.info(f"Prompt Sent to AI:\n{final_prompt}")

            image = generate_image(final_prompt)

            if image is None:
                st.stop()
                
            save_prompt(
    st.session_state.username,
    final_prompt
)

            username = st.session_state.username

            user_folder = os.path.join("gallery", username)

            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            image_count = len(os.listdir(user_folder)) + 1
            filename = os.path.join(user_folder, f"image_{image_count}.png")

            image.save(filename)

            st.success("Image Generated Successfully!")

            st.image(image)

            buf = io.BytesIO()
            image.save(buf, format="PNG")

            st.download_button(
                label="📥 Download Image",
                data=buf.getvalue(),
                file_name="generated_image.png",
                mime="image/png"
            )

    else:
        st.warning("Please enter a prompt.")

username = st.session_state.username
user_folder = os.path.join("gallery", username)

if not os.path.exists(user_folder):
    os.makedirs(user_folder)

images = os.listdir(user_folder)

if images:

    cols = st.columns(3)

    for i, img in enumerate(images):

        image_path = os.path.join(user_folder, img)

        with cols[i % 3]:

            st.image(image_path, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                with open(image_path, "rb") as file:
                    st.download_button(
                        "📥",
                        file,
                        file_name=img,
                        mime="image/png",
                        key=f"download_{img}"
                    )

            with col2:
                if st.button("🗑️ Delete", key=f"delete_{img}"):

                    os.remove(image_path)

                    st.success("Image Deleted Successfully!")

                    st.rerun()

else: 
     st.info("No images found.") 
     
st.markdown("## 📜 Prompt History")

history = get_prompt_history(st.session_state.username)

if history:
    for i, item in enumerate(history, 1):
        st.write(f"{i}. {item[0]}")
else:
    st.info("No prompt history yet.")