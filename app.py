### Health Management APP
from dotenv import load_dotenv

load_dotenv()  ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input_prompt,image):
    model=genai.GenerativeModel('gemini-3.6-flash')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
    Finally you can also mention whether the food is healthy or not and also mention the percentage split of the 
    ratio of carbohydrates,fats,sugar,fibres and other important things required in our diet

"""

##initialize our streamlit app

st.set_page_config(
    page_title="Calories Advisor App",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- CUSTOM STYLING -----------------------------
st.markdown("""
<style>
    /* Force the browser + Streamlit's own CSS variables into light mode.
       This is the root cause fix: Streamlit's dark theme feeds a dark
       background into every component (header, uploader, etc.) via these
       variables, which is why per-component overrides kept losing. */
    html, body, :root {
        color-scheme: light !important;
        --background-color: #f7faf7 !important;
        --secondary-background-color: #ffffff !important;
        --text-color: #1a1a1a !important;
        --primary-color: #1f8a3d !important;
    }

    /* Overall app background */
    .stApp {
        background: linear-gradient(180deg, #f7faf7 0%, #eef6ee 100%) !important;
    }

    /* Force readable dark text everywhere in the main content area,
       regardless of whether the user has light or dark theme enabled */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] div,
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] h5,
    [data-testid="stAppViewContainer"] h6 {
        color: #1a1a1a !important;
    }

    /* Sidebar: force a light background + dark readable text */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e7f1e7;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }

    /* Top toolbar/header strip (was showing as a black bar).
       Covers both current and older Streamlit test-ids/classes. */
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    header {
        background: #f7faf7 !important;
        background-color: #f7faf7 !important;
    }
    header[data-testid="stHeader"] *,
    div[data-testid="stToolbar"] * {
        color: #1a1a1a !important;
        fill: #1a1a1a !important;
    }

    /* File uploader drop-zone (was showing as a black box).
       Covers both current and older Streamlit test-ids. */
    div[data-testid="stFileUploader"] section,
    div[data-testid="stFileUploaderDropzone"],
    div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"] {
        background: #f4faf5 !important;
        background-color: #f4faf5 !important;
        border: 2px dashed #7ee08a !important;
        border-radius: 12px !important;
    }
    div[data-testid="stFileUploader"],
    div[data-testid="stFileUploader"] * {
        color: #1a1a1a !important;
        background-color: transparent;
    }
    div[data-testid="stFileUploader"] section {
        background-color: #f4faf5 !important;
    }
    div[data-testid="stFileUploader"] button,
    div[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: 1px solid #34c759 !important;
        border-radius: 8px !important;
        color: #1a1a1a !important;
    }
    /* uploaded-file chip (name/size row) */
    div[data-testid="stFileUploaderFile"],
    div[data-testid="stFileUploaderFileData"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: 1px solid #e7f1e7 !important;
        border-radius: 8px !important;
        color: #1a1a1a !important;
    }

    /* Hero header (white text stays white, higher specificity than the rule above) */
    .hero {
        background: linear-gradient(135deg, #1f8a3d 0%, #34c759 55%, #7ee08a 100%);
        padding: 2.2rem 2rem;
        border-radius: 18px;
        margin-bottom: 1.6rem;
        box-shadow: 0 10px 30px rgba(31, 138, 61, 0.25);
    }
    .hero h1, .hero p {
        color: #ffffff !important;
    }
    .hero h1 {
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
    }
    .hero p {
        margin-top: 0.4rem;
        font-size: 1.02rem;
        opacity: 0.95;
    }

    /* Bordered containers (our "cards") */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border-radius: 16px !important;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        border: 1px solid #e7f1e7 !important;
    }

    /* Primary button */
    div.stButton > button {
        background: linear-gradient(135deg, #1f8a3d, #34c759);
        color: #ffffff !important;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1.4rem;
        width: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 4px 14px rgba(31, 138, 61, 0.35);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(31, 138, 61, 0.45);
    }
    div.stButton > button p {
        color: #ffffff !important;
    }

    /* Response box */
    .response-box {
        background: #ffffff;
        border-left: 5px solid #34c759;
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        color: #1a1a1a;
    }
    .response-box * {
        color: #1a1a1a !important;
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------------------- SIDEBAR -----------------------------
with st.sidebar:
    st.markdown("### 🥗 About")
    st.write(
        "Upload a photo of your meal and get an instant AI-powered "
        "breakdown of calories, individual food items, and a healthiness "
        "verdict — powered by Gemini."
    )
    st.markdown("---")
    st.markdown("### 📋 How it works")
    st.markdown(
        "1. **Upload** a clear photo of your plate\n"
        "2. Click **Analyze My Meal**\n"
        "3. Get itemized **calories** + a **nutrition split**"
    )
    st.markdown("---")
    st.caption("Tip: good lighting and a top-down shot give the most accurate results.")

# ----------------------------- HERO HEADER -----------------------------
st.markdown("""
<div class="hero">
    <h1>🥗 Calories Advisor App</h1>
    <p>Snap it, upload it, and let AI tell you exactly what's on your plate.</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------- MAIN LAYOUT -----------------------------
col1, col2 = st.columns([1, 1.15], gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### 📸 Upload Your Meal")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        image=""
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_container_width=True)
        else:
            st.info("No image uploaded yet — drag and drop a photo of your meal above.")

        submit=st.button("🔍 Analyze My Meal")

with col2:
    with st.container(border=True):
        st.markdown("### 🧾 Nutrition Report")

        ## If submit button is clicked
        if submit:
            if uploaded_file is None:
                st.warning("Please upload an image first.")
            else:
                with st.spinner("Analyzing your meal... 🍽️"):
                    image_data=input_image_setup(uploaded_file)
                    response=get_gemini_repsonse(input_prompt,image_data)
                st.success("Analysis complete!")
                st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
        else:
            st.write("Your calorie breakdown and nutrition insights will appear here after you upload a photo and click **Analyze My Meal**.")
