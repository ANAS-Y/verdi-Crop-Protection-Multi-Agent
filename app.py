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

# --- 1. Robust Setup ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("⚠️ Google API Key not found. Please set it in Streamlit Secrets.")
        st.stop()
    
    genai.configure(api_key=api_key)

except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# --- 2. Smart Model Selector ---
@st.cache_resource
def get_best_model_name():
    """
    Automatically asks Google API for available models and picks the best one.
    This prevents 404 errors by never guessing a name that doesn't exist.
    """
    try:
        # Get all models that support 'generateContent'
        model_list = list(genai.list_models())
        available_names = [m.name for m in model_list if 'generateContent' in m.supported_generation_methods]
        
        # Priority preferences
        preferences = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-1.0-pro',
            'gemini-pro'
        ]
        
        # 1. Try to find a preferred model in the available list
        for pref in preferences:
            for name in available_names:
                if pref in name:
                    return name # Found a match!
        
        # 2. If no preferences found, take the first available one
        if available_names:
            return available_names[0]
            
        return None
    except Exception as e:
        print(f"Error listing models: {e}")
        return "models/gemini-1.5-flash-latest" # Fallback guess

# Initialize the best model
MODEL_NAME = get_best_model_name()
if not MODEL_NAME:
    st.error("CRITICAL: No Gemini models found available for this API Key.")
    st.stop()

# --- 3. Define Agents ---

def agent_scout(image):
    """
    Agent A: The Scout (Vision)
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
    **Visual Evidence:** [Brief description]
    """
    try:
        # Re-initialize model to be safe
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        # If the text model fails on image, try the legacy vision model fallback
        if "vision" not in MODEL_NAME and ("400" in str(e) or "instrument" in str(e)):
             try:
                 fallback = genai.GenerativeModel('gemini-pro-vision')
                 return fallback.generate_content([prompt, image]).text
             except:
                 pass
        return f"Error in Scout Agent ({MODEL_NAME}): {str(e)}"

def agent_researcher(diagnosis_text):
    """
    Agent B: The Researcher (Logic)
    """
    prompt = f"""
    You are a Senior Agricultural Extension Worker.
    Based on this scout report: 
    '{diagnosis_text}'
    
    Provide an Action Plan for a smallholder farmer in Nigeria.
    1. **Immediate Action:** What should they do today?
    2. **Prevention:** How to stop it next season.
    3. **Warning:** Short SMS alert message.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error in Researcher Agent ({MODEL_NAME}): {str(e)}"

# --- 4. The UI Layout ---

st.title("🌱 Verdi: Autonomous Crop Protection Agent")
st.caption(f"Connected to Brain: {MODEL_NAME}")

st.markdown("""
**Verdi** acts as an AI Agronomist in your pocket. 
Upload a photo of a sick crop, and the Multi-Agent System will diagnose it and prescribe a cure.
""")

# Sidebar
with st.sidebar:
    st.header("About Verdi")
    st.info("Built for the Kaggle AI Agents Intensive.")
    st.success(f"System Online: {MODEL_NAME}")

# Main Area
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Scout Agent Input")
    uploaded_file = st.file_uploader("Take a photo of the leaf", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Crop Image", use_column_width=True)
        
        if st.button("🚀 Launch Analysis Swarm"):
            with st.spinner(f"🤖 Scout Agent analyzing with {MODEL_NAME}..."):
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
                time.sleep(1) 
                treatment = agent_researcher(st.session_state['diagnosis'])
                st.session_state['treatment'] = treatment
                
            st.divider()
            st.markdown("### 💊 Researcher Agent Plan")
            st.markdown(st.session_state['treatment'])
            st.success("✅ Protocol Generated.")

# Footer
st.markdown("---")