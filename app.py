import streamlit as st
import google.generativeai as genai
import os

st.title("🛠️ Gemini API Diagnostics")

# 1. Get API Key
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = os.getenv("GOOGLE_API_KEY")
except:
    pass

if not api_key:
    api_key = st.text_input("Enter your Google API Key manually", type="password")

if st.button("🔍 Scan for Available Models"):
    if not api_key:
        st.error("Please provide an API Key.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            st.info("Contacting Google API...")
            
            # List all models
            all_models = list(genai.list_models())
            
            st.success(f"✅ Connection Successful! Found {len(all_models)} models.")
            
            # Filter for models that can generate content
            chat_models = [m for m in all_models if 'generateContent' in m.supported_generation_methods]
            
            st.write("### 🤖 Models Available to YOU:")
            if not chat_models:
                st.error("No text generation models found. Check your API Key permissions.")
            
            for m in chat_models:
                st.code(f"{m.name}")
                
            st.write("### 🧪 Test A Model")
            test_model = st.selectbox("Select a model to test:", [m.name for m in chat_models])
            
            if st.button("Test This Model"):
                try:
                    model = genai.GenerativeModel(test_model)
                    response = model.generate_content("Hello, are you working?")
                    st.success(f"Response: {response.text}")
                except Exception as e:
                    st.error(f"Failed: {e}")

        except Exception as e:
            st.error(f"❌ Connection Failed: {e}")
            st.warning("If you see a 404 here, your API Key might be invalid or restricted.")