🌱 Verdi: The Autonomous Crop Protection AgentVerdi is a Multi-Agent System designed to help farmers in Nigeria and globally diagnose crop diseases in real-time.🚀 FeaturesAgent A (Scout): Uses Computer Vision (Gemini 1.5 Pro) to identify diseases from leaf photos.Agent B (Researcher): Formulates organic and chemical treatment plans.Agent C (Guardian): Generates alert warnings for neighboring farms.🛠️ Tech StackPythonStreamlitGoogle Gemini API📦 How to Run LocallyClone the repo.Install dependencies: pip install -r requirements.txtSet GOOGLE_API_KEY in your environment.Run: streamlit run app.py
---

### **3. Deployment Steps (Step-by-Step)**

#### **Step A: Push to GitHub**
1.  Log in to [GitHub](https://github.com/) and create a **New Repository** (e.g., named `verdi-agri-agent`).
2.  Make it **Public**.
3.  Open your terminal/command prompt in the folder where you saved the files above.
4.  Run these commands:
    ```bash
    git init
    git add .
    git commit -m "Initial commit of Verdi Agent"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/verdi-agri-agent.git
    git push -u origin main
    ```

#### **Step B: Deploy to Streamlit Cloud**
1.  Go to [Streamlit Cloud](https://share.streamlit.io/).
2.  Click **"New App"**.
3.  **Repository:** Select `YOUR_USERNAME/verdi-agri-agent`.
4.  **Branch:** `main`.
5.  **Main file path:** `app.py`.
6.  **⚠️ CRITICAL STEP (Secrets):**
    * Click **"Advanced Settings"**.
    * Find the **"Secrets"** box.
    * Add your Gemini API Key in this exact format:
        ```toml
        GOOGLE_API_KEY = "AIzaSyD-xxxxxxxxxxxxxxxxxxxxxxxx"
