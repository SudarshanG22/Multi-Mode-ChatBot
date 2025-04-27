
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64  # Required for setting background images
import requests  # For real-time web search integration

# Configure Gemini API Key (Use your own key)
API_KEY = "AIzaSyCn9oQxPToTce3Hq5W8XmPf4x4v_2o2dzk"  # Replace this with your actual API key
genai.configure(api_key=API_KEY)

# Use the correct Gemini model
MODEL_NAME = "models/gemini-1.5-pro-latest"

# Function to chat with Gemini AI
def chat_with_gemini(user_input, image, mode):
    if mode == "Funny Mode 🤣":
        system_message = "You are a comedian AI. Give only funny and light-hearted responses in simple words."
    elif mode == "Mental Mode 🤯":
        system_message = "You are a curious AI. Instead of answering, ask a deep or confusing question related to the topic, using simple language."
    elif mode == "Brilliant Mode 🧠":
        system_message = "You are a helpful AI. Give correct and clear answers using simple words, avoiding complex explanations."
    elif mode == "Code Assistant Mode 💻":
        system_message = "You are a coding assistant. Help with programming-related queries, provide code examples, and debug issues."
    else:
        system_message = "You are a helpful AI. Give correct and clear answers using simple words, avoiding complex explanations."
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        if image:
            image_bytes = image.read()
            image_data = Image.open(io.BytesIO(image_bytes))
            response = model.generate_content([system_message, user_input, image_data])
        else:
            response = model.generate_content(system_message + " " + user_input)
        
        return response.text if response else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Function to encode images to Base64
def get_base64(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

# Load Background Images
main_bg = "6.jpg"   # Your main background image
sidebar_bg = "4.jpg"   # Your sidebar background image

# Convert images to Base64
main_bg_base64 = get_base64(main_bg)
sidebar_bg_base64 = get_base64(sidebar_bg)

# Apply Background Styling
st.markdown(f"""
    <style>
        /* Background Image for Main Chat Area */
        .stApp {{
            background-image: url("data:image/jpg;base64,{main_bg_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Background Image for Sidebar */
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/jpg;base64,{sidebar_bg_base64}");
            background-size: cover;
            background-position: center;
        }}

        /* Sidebar Text Styling (White, Bold & Larger) */
        [data-testid="stSidebar"] * {{
            color: white !important;
            font-weight: bold !important;
            font-size: 18px !important;
        }}

        .stTextArea textarea {{font-size: 18px; height: 80px !important;}}
        .stTextInput input {{font-size: 18px; height: 80px !important; overflow-wrap: break-word;}}
        .stButton button {{border-radius: 10px; padding: 10px; font-size: 18px; background-color: #4CAF50; color: white;}}
        .title-box {{text-align: center; padding: 20px; background-color: #0073e6; color: white; font-size: 42px; font-weight: bold; border-radius: 10px; margin-bottom: 20px; width: 60%; margin-left: auto; margin-right: auto;}}
        .footer {{position: relative; bottom: 0; width: 100%; text-align: center; padding: 15px; background-color: white; font-size: 20px; font-weight: bold; color: black; margin-top: 50px;}}
    </style>
""", unsafe_allow_html=True)

# Sidebar with features
st.sidebar.title("⚙️ Chatbot Settings")
st.sidebar.write("Select your preferred mode and explore features!")

# Chatbot mode selection
mode = st.sidebar.radio("Choose Chat Mode:", ["Funny Mode 🤣", "Mental Mode 🤯", "Brilliant Mode 🧠", "Code Assistant Mode 💻"], index=2)

st.sidebar.subheader("💾 Chat Options")
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.sidebar.success("Chat history cleared!")

st.sidebar.subheader("🌟 About")
st.sidebar.info("This AI chatbot can switch between different modes, providing varied and engaging responses.")

# Main content
st.markdown("<div class='title-box'>Multi Mode Bot</div>", unsafe_allow_html=True)
st.subheader("Choose a mode from the sidebar and start chatting!")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_area("You:", "", height=80, placeholder="Type your message here...")

# Image upload section for chatbot input
uploaded_image = st.file_uploader("📂 Upload an image (optional):", type=["png", "jpg", "jpeg"])

# Generate response
if st.button("Send", use_container_width=True):
    if user_input or uploaded_image:
        # Check for real-time web search mode
        if mode == "Real-time Web Search Mode 🌐":
            response = real_time_web_search(user_input)
        else:
            response = chat_with_gemini(user_input, uploaded_image, mode)
        
        st.session_state.chat_history.append((user_input, response, uploaded_image))
    else:
        st.warning("Please enter a message or upload an image!")

# Display chat history
st.divider()
st.subheader("Chat History")
for user_msg, bot_msg, img in st.session_state.chat_history[::-1]:
    with st.expander(f"👤 You: {user_msg if user_msg else 'Image Uploaded'}", expanded=True):
        if img:
            st.image(img, caption="Uploaded Image", width=500)  # **Increased Image Display Size**
        st.markdown(f"**🤖 Bot ({mode}):** {bot_msg}")

# Footer
st.markdown("""
    <div class='footer'>🤖 AI Chatbot | Developed by Sudarshan with ❤️ using Streamlit</div>
""", unsafe_allow_html=True)
