import streamlit as st
import joblib
import pandas as pd
from features import extract_features

st.set_page_config(page_title="AI Phishing Detector", page_icon="🛡️", layout="centered")

st.title("Phishing URL Detector")

# Load model only once when the app starts (@st.cache_resource)
@st.cache_resource
def load_model():
    return joblib.load('phishing_model.pkl')

model = load_model()

url = st.text_input("Enter URL to check:", placeholder="https://example.com")

if st.button("Check URL", type="primary"):
    if url:
        with st.spinner("Analyzing URL with AI..."):
            features = extract_features(url)
            feature_df = pd.DataFrame([features])
            
            pred = model.predict(feature_df)[0]
            prob = model.predict_proba(feature_df)[0][1]
            
            if pred == 1:
                st.error(f"🚨 HIGH RISK - PHISHING DETECTED ({prob:.1%} confidence)")
            else:
                st.success(f"✅ SAFE - Legitimate site ({(1-prob):.1%} confidence)")
            
            st.subheader("Features extracted:")
            st.json(features)
    else:
        st.warning("Please enter a URL")

