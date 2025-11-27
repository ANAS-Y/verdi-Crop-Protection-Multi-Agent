import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- Page Config ---
st.set_page_config(
    page_title="Verdi: AI Agronomist",
    page_icon="🌱",
    layout="wide"
)

# --- 1. Setup & Secrets Management ---
try:
    # Try getting the key from Streamlit secrets (Cloud) or Environment (Local)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("⚠️ Google API Key not found. Please set it in Streamlit Secrets.")
        st.stop()
    
    genai.configure(api_key=api_key)
    
    # FIX: Changed from 'gemini-1.5-pro-latest' to 'gemini-1.5-flash'
    # 'gemini-1.5-flash' is the most stable and fastest model for this competition.
    # You can also try 'gemini-1.5-pro' if flash is too simple, but Flash is safer for errors.
    model = genai.GenerativeModel('gemini-1.5-flash')

except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()


# --- 2. Define Agents ---

def agent_scout(image):
    """
    Agent A: The Scout (Vision)
    Analyzes the image using Gemini 1.5 Flash.
    """
    prompt = """
    You are an expert Agronomist specializing in African crops. 
    Analyze this image strictly.
    1. Identify the crop (e.g., Cassava, Maize, Yam).
    2. Identify the specific disease or pest (e.g., Cassava Mosaic Disease, Fall Armyworm, Healthy).
    3. Estimate severity (Low, Medium, High).
    
    Output strictly in this format:
    **Crop:** [Name]
    **Diagnosis:** [Disease Name]
    **Severity:** [Level]
    **Visual Evidence:** [Brief description of what you see, e.g., yellow mottling, lesions]
    """
    # Streamlit passes a PIL Image, Gemini accepts it directly
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error in Scout Agent: {str(e)}"

def agent_researcher(diagnosis_text):
    """
    Agent B: The Researcher (Logic & Tools)
    Takes the diagnosis and finds a solution.
    """
    prompt = f"""
    You are a Senior Agricultural Extension Worker.
    Based on this scout report: 
    '{diagnosis_text}'
    
    Provide an Action Plan for a smallholder farmer in Nigeria.
    1. **Immediate Action:** What should they do today? (Organic/Chemical options).
    2. **Prevention:** How to stop it next season.
    3. **Warning:** If severity is High, write a short SMS alert message they can send to neighbors.
    
    Keep it practical and easy to understand.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error in Researcher Agent: {str(e)}"

# --- 3. The UI Layout ---

st.title("🌱 Verdi: Autonomous Crop Protection Agent")
st.markdown("""
**Verdi** acts as an AI Agronomist in your pocket. 
Upload a photo of a sick crop, and the Multi-Agent System will diagnose it and prescribe a cure.
""")

# Sidebar for Context
with st.sidebar:
    st.header("About Verdi")
    st.info("Built for the Kaggle AI Agents Intensive.")
    st.markdown("### Agents Active:")
    st.success("✅ Scout (Vision)")
    st.success("✅ Researcher (Logic)")
    st.success("✅ Guardian (Alerts)")

# Main Area
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Scout Agent Input")
    uploaded_file = st.file_uploader("Take a photo of the leaf", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Crop Image", use_column_width=True)
        
        if st.button("🚀 Launch Analysis Swarm"):
            with st.spinner("🤖 Scout Agent is analyzing visual patterns..."):
                # Call Agent A
                diagnosis = agent_scout(image)
                st.session_state['diagnosis'] = diagnosis
                st.session_state['run_researcher'] = True

with col2:
    st.subheader("2. Agent Swarm Results")
    
    if 'diagnosis' in st.session_state:
        st.markdown("### 👁️ Scout Agent Report")
        st.markdown(st.session_state['diagnosis'])
        
        if st.session_state.get('run_researcher'):
            with st.spinner("🧠 Researcher Agent is formulating treatment plan..."):
                time.sleep(1) # UX pause
                # Call Agent B
                treatment = agent_researcher(st.session_state['diagnosis'])
                st.session_state['treatment'] = treatment
                
            st.divider()
            st.markdown("### 💊 Researcher Agent Plan")
            st.markdown(st.session_state['treatment'])
            st.success("✅ Diagnosis & Treatment Protocol Generated.")

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini 1.5 Flash | Kaggle Agents Capstone")