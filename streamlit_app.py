import streamlit as st
import whisper
import os
import subprocess

st.set_page_config(page_title="HustleStudio Suite", page_icon="🚀", layout="centered")
st.title("🚀 HustleStudio Suite")
st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")

# Create the clean product tab structure
tab1, tab2, tab3 = st.tabs(["🎨 Tool 1: AI Animation Gen", "💡 Tool 2: Viral Hooks", "🎬 Tool 3: Caption King"])

# ==========================================
# TOOL 1: TEMPLATE-DRIVEN ANIMATION GENERATOR
# ==========================================
with tab1:
    st.subheader("🎨 Tool 1: AI Video & Animation Generator")
    st.markdown("Type a keyword prompt to watch the cloud pull a smooth, high-fidelity cinematic video loop instantly.")
    
    video_prompt = st.text_input("Describe the scene you want to animate:", placeholder="Try keywords like: 'robot', 'car', 'space', 'cyberpunk'...", key="animation_prompt_field")
    
    if st.button("🚀 Generate AI Animation"):
        if not video_prompt.strip():
            st.warning("⚠️ Please type an animation prompt first.")
        else:
            with st.spinner("🎨 Parsing creative layers and loading cinematic file..."):
                p_lower = video_prompt.lower()
                
                # Standalone database links containing premium, pre-rendered AI animation assets 
                # This guarantees 1-second load times without ever hitting network timeout crashes!
                video_url = None
                
                if "robot" in p_lower:
                    video_url = "https://mixkit.co"
                    st.success("🤖 Detected Concept: Futuristic Dancing Robot Scenario")
                elif "car" in p_lower or "drive" in p_lower or "nairobi" in p_lower:
                    video_url = "https://mixkit.co"
                    st.success("🚗 Detected Concept: Cyberpunk Neon City Drift")
                elif "space" in p_lower or "galaxy" in p_lower or "stars" in p_lower:
                    video_url = "https://mixkit.co"
                    st.success("🌌 Detected Concept: Cosmic Wormhole Warp")
                else:
                    # Universal premium default background abstract loop if keywords match generally
                    video_url = "https://mixkit.co"
                    st.success("✨ Detected Concept: High-Definition Abstract Creative Loop")
                
                if video_url:
                    # Render the crisp video directly to the user's mobile or computer browser layout screen
                   st.video(video_url, format="video/mp4", start_time=0, loop=True, autoplay=True)

                    st.caption("💡 Tip for creators: You can download this custom background layout file right from the video player settings dropdown icon menu box panel window.")

# ==========================================
# TOOL 2: KENYAN VIRAL HOOKS
# ==========================================
with tab2:
    st.subheader("💡 Tool 2: Viral Hook Bot")
    st.markdown("Beat creative block instantly. Get hooks tailored for local audiences.")
    topic = st.text_input("What is your video about? (e.g., 'selling shoes')", key="hooks_topic_field")
    
    if st.button("⚡ Generate Hooks") and topic.strip():
        t = topic.strip()
        st.markdown(f"### 🚀 Viral Hooks Generated for: '{t}'")
        st.markdown(f"1. **🚨 USIWAHI jaribu {t} hapa Kenya kabla ujue hii siri...**")
        st.markdown(f"2. **💡 Mbona hakuna mtu anakuambia ukweli kuhusu {t}?**")
        st.markdown(f"3. **🤫 Hii hapa siri ya {t} yenye matajiri wa Nairobi hawataki ujue.**")

# ==========================================
# TOOL 3: CAPTION KING
# ==========================================
with tab3:
    st.subheader("🎬 Tool 3: Caption King")
    st.markdown("Upload your video file to burn clean, styled titles.")
    
    col1, col2 = st.columns(2)
    with col1:
        font_style = st.selectbox("🔤 Font", ["Impact", "Arial", "Trebuchet MS"])
    with col2:
        text_position = st.selectbox("📍 Position", ["Bottom Center", "Middle Center", "Top Center"])
        
    uploaded_file = st.file_uploader("Upload Video (MP4)", type=["mp4"], key="video_uploader_field")






     
                
        
